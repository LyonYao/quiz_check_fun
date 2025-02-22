import uuid
from flask import Blueprint, jsonify, request
import pytz

from comm.db_connect import DatabaseConnection
import random

checker = Blueprint('checker', __name__)
__ENDPOINT_PRE__ = '/api/checker/'


@checker.route('%slist' % __ENDPOINT_PRE__, methods=['POST'])
def list():
    aid = request.json.get('aid')
    # sid: sid, aid: aid, registration_code: registrationCode
    sid = request.json.get('sid')
    reg_code = request.json.get('registration_code')
    if not aid or not reg_code:
        return jsonify({'error': 'ID or reg code is required'}), 400
    db_conn = DatabaseConnection()
    db_conn.connect()
    result = db_conn.execute_query('''SELECT b.reg_name,b.reg_code, a.question_count
	FROM quiz.activity_reg b,quiz.activity_summary a  where b.activity_id =%s 
                                   and b.reg_code=%s and b.activity_id=a.id limit 1''', (aid, reg_code,))
    if len(result) == 0:
        db_conn.close()
        return jsonify({'error': 'you have no registration'}), 400
    reg_name = result[0][0]
    reg_code = result[0][1]
    q_cnt_for_u = result[0][2]
    result = db_conn.execute_query('''SELECT id, type, ref_id, reg_code, created_at, 
                                   updated_at, completed_at, status, score ,current_answer_idx
                                   FROM quiz.check_record where ref_id in(%s,%s) and reg_code=%s and status='N' order by created_at desc limit 1''', (aid,sid, reg_code,))
    
    has_record = False
    current_answer_idx = 0
    if len(result) == 1:
        check_id=result[0][0]
        start_time=result[0][4]
        checker_type = result[0][1]
        current_answer_idx = result[0][9]
        ref_id = result[0][2]
        has_record = True
        pass
    if not has_record:
        
        checker_type = 'SUBECT'
        if sid:
            result = db_conn.execute_query('''SELECT b.id, b.content,b.options,b.answer,b.type 
            FROM quiz.check_refer a,quiz.check_question b  where a.ref_id =%s and a.question_id=b.id''', (sid,))
        if len(result) == 0:
            result = db_conn.execute_query('''SELECT b.id, b.content,b.options,b.answer,b.type 
            FROM quiz.check_refer a,quiz.check_question b  where a.ref_id =%s and a.question_id=b.id''', (aid,))
            checker_type = 'ACTIVITY'
        if len(result) == 0:
            db_conn.close()
            return jsonify({'error': 'no question found for choosed item'}), 400
        check_id = str(uuid.uuid4()).replace('-','')[:31]
        ref_id = sid if checker_type == 'SUBECT' else aid
        
        ## loop question in result and save in a array for using
        questions = []
        for row in result:
            questions.append({
            'id': row[0],
            'content': row[1],
            'options': row[2],
            'answer': row[3], 
            'type': row[4]
            })
        q_count = len(result)
        
        ## radomly select q_cnt_for_u questions from questions, if q_cnt_for_u > q_count, then q_cnt_for_u = q_count
        if q_cnt_for_u > q_count:
            q_cnt_for_u = q_count
        selected_questions = random.sample(questions, q_cnt_for_u)
        for question in selected_questions:
            db_conn.execute_insert('''INSERT INTO quiz.check_answer (id,question_id, record_id, content, options, answer,type,
                                   created_at) VALUES(%s, %s,%s, %s,  %s, %s,%s, now());''',
                       (str(uuid.uuid4()).replace('-','')[:31],question['id'], check_id, question['content'], question['options'], 
                        question['answer'],question['type'], ))
        if checker_type == 'SUBECT':
            db_conn.execute_insert('''INSERT INTO quiz.check_record (id, type, ref_id, activity_id,  reg_code, created_at, 
                                   updated_at, status, score,question_count,name ) VALUES (%s, %s, %s, %s, %s, now(),now(), %s, %s, %s,
                                   (SELECT title FROM quiz.subject_summary WHERE id = %s))''',
                              (check_id, checker_type,ref_id , aid, reg_code, 'N', -1, q_cnt_for_u, ref_id))
        else:
            db_conn.execute_insert('''INSERT INTO quiz.check_record (id, type, ref_id, activity_id,  reg_code, created_at, 
                                   updated_at, status, score,question_count,name) VALUES (%s, %s, %s, %s, %s, now(),now(), %s, %s, %s,
                                   (SELECT name FROM quiz.activity_summary WHERE id = %s))''',
                              (check_id, checker_type,ref_id , aid, reg_code, 'N', -1, q_cnt_for_u, ref_id))
        db_conn.commit()
        from datetime import datetime
        start_time = datetime.now().astimezone(tz=pytz.timezone('Asia/Hong_Kong'))
    result = db_conn.execute_query('''SELECT b.id, b.content,b.options, b.type,b.result,b.question_id
            FROM quiz.check_answer b where b.record_id =%s order by b.id limit 100''', (check_id,)) 
    data = []
    idx = 0
    for row in result:
        opts = row[2].split('\;')
        optRslt = []
        for opt in opts:
            val_lab =opt.split(':')
            optRslt.append({
                'value':val_lab[0],
                'label': val_lab[1]}
            )
        data.append({
            'idx': idx,
            'id': row[0],
            'content': row[1],
            'options': optRslt, 
            'type': row[3],
            'result': row[4].split('\;') if row[4] else [],
            'question_id': row[5]
        })
        idx += 1
    
    db_conn.close()
    return jsonify({'questions': data, 'check_id': check_id, 'reg_name': reg_name, 
                    'reg_code': reg_code,'start_time': start_time,'checker_type': checker_type,ref_id:ref_id,
                    'current_answer_idx': current_answer_idx})



@checker.route('%scomplete' % __ENDPOINT_PRE__, methods=['POST'])
def content_by_id():
    sub_id = request.json.get('id')
    answers = request.json.get('result')
    record_id = request.json.get('record_id')
    current_answer_idx = request.json.get('current_answer_idx',0)
    if not answers or not record_id or len(answers) == 0:
        return jsonify({'error': 'Answers and record ID are required'}), 400
    db_conn = DatabaseConnection()
    db_conn.connect()
    result = db_conn.execute_query('''SELECT b.id, b.content,b.options, b.type,b.result,b.question_id, b.answer
        FROM quiz.check_answer b where b.record_id =%s order by b.id limit 100''', (record_id,))
    if len(result) == 0:
        db_conn.close()
        return jsonify({'error': 'Invaklid request'}), 400
    q_cnt = 0
    real_answers = {}
    for row in result:
        q_cnt += 1
        real_answers[row[0]] = row[6].split('\;') if row[6] else []

    right_count = 0
    for answer in answers:
        u_answer = answer.get('answer', [])
        id = answer.get('question_id')
        if id  in real_answers:
            if set(real_answers[id]) == set(u_answer):
                right_count += 1
        answer_values = '\;'.join(u_answer)
        db_conn.execute_update('''UPDATE quiz.check_answer SET result = %s, updated_at =now()
                                WHERE record_id = %s AND id = %s''',
                               (answer_values, record_id, id))
    
    right_percent = (int)((right_count / q_cnt) * 100) if q_cnt > 0 else 0
    db_conn.execute_update('''UPDATE quiz.check_record SET completed_at = now(),current_answer_idx=%s, status = %s, score=%s  WHERE id = %s''',
                           (current_answer_idx,'C',right_percent, record_id))
    db_conn.commit()
    db_conn.close()
    return jsonify({'message': 'Check completed'})



@checker.route('%ssave' % __ENDPOINT_PRE__, methods=['POST'])
def save():
    sub_id = request.json.get('id')
    answers = request.json.get('result')
    record_id = request.json.get('record_id')
    current_answer_idx = request.json.get('current_answer_idx',0)
    if not answers or not record_id or len(answers) == 0:
        return jsonify({'error': 'Answers and record ID are required'}), 400
    if not answers or   len(answers) == 0:
        return jsonify({'error': 'No Answer you have selected'}), 400
    db_conn = DatabaseConnection()
    db_conn.connect()
    for answer in answers:
        id = answer.get('question_id')
        answer_values = '\;'.join(answer.get('answer', []))
        db_conn.execute_update('''UPDATE quiz.check_answer SET result = %s, updated_at =now() WHERE record_id = %s AND id = %s''',
                               (answer_values, record_id, id))
    db_conn.execute_update('''UPDATE quiz.check_record SET updated_at = now(),current_answer_idx=%s WHERE id = %s''',
                           (current_answer_idx, record_id))
    db_conn.commit()
    db_conn.close()
    return jsonify({'message': 'Save completed'})


@checker.route('%shistory' % __ENDPOINT_PRE__, methods=['POST'])
def history_list():
    reg_code = request.json.get('registration_code')
    if not reg_code:
        return jsonify({'error': 'reg code is required'}), 400
    aId = request.json.get('aId')
    if not aId:
        return jsonify({'error': 'acitivity id is required'}), 400
    
    db_conn = DatabaseConnection()
    db_conn.connect()
    result = db_conn.execute_query('''SELECT a.reg_name, a.reg_code, b.name
	FROM quiz.activity_reg a, quiz.activity_summary b where a.activity_id =%s and a.reg_code=%s and a.activity_id=b.id limit 1''', (aId, reg_code,))
    if len(result) == 0:
        db_conn.close()
        return jsonify({'error': 'you have no registration'}), 400
    reg_name = result[0][0]
    activity_name = result[0][2]


    result = db_conn.execute_query('''SELECT a.id, a.type, a.ref_id, a.reg_code, a.created_at, 
                                   a.updated_at, a.completed_at, a.status, a.score, a.question_count, a.name
                                   FROM quiz.check_record a where a.reg_code=%s and a.activity_id=%s and status='C' order by a.created_at desc ''', (reg_code, aId,))
    data = []
    ### get all questions, set duration is completed_at - created_at as minutes 
    for row in result:
        check_id = row[0]
        reg_code = row[3]
        created_at = row[4]
        completed_at = row[6]
        status = row[7]
        score = row[8]
        question_count = row[9]
        name = row[10]
        duration = (completed_at - created_at).seconds // 60
        data.append({
            'id': check_id,
            'created_at': created_at,
            'completed_at': completed_at,
            'status': status,
            'score': score,
            'duration': duration,
            'question_count': question_count,
            'name': name
        })
        
    
    db_conn.close()
    return jsonify({'reg_name': reg_name, 'activity_name': activity_name, 'history': data})


@checker.route('%shistory-item' % __ENDPOINT_PRE__, methods=['POST'])
def history_item():
    registration_code = request.json.get('registration_code')
    check_id = request.json.get('check_id')
    if not registration_code or not check_id:
        return jsonify({'error': 'Registration code and check ID are required'}), 400
    db_conn = DatabaseConnection()
    db_conn.connect()
    result=db_conn.execute_query('''select 1 from quiz.check_record  WHERE id = %s and reg_code=%s 
                           and status='C' ''', (check_id, registration_code,))
    if len(result) == 0:
        db_conn.close()
        return jsonify({'error': 'Invalid Parameter...'}), 400

    result = db_conn.execute_query('''SELECT b.id, b.content,b.options, b.type,b.result,b.question_id, b.answer
            FROM quiz.check_answer b where b.record_id =%s order by b.id limit 100''', (check_id,))
    data = []
    idx = 0
    for row in result:
        opts = row[2].split('\;')
        optRslt = []
        for opt in opts:
            val_lab =opt.split(':')
            optRslt.append({
                'value':val_lab[0],
                'label': val_lab[1]}
            )
        data.append({
            'idx': idx,
            'id': row[0],
            'content': row[1],
            'options': optRslt, 
            'type': row[3],
            'result': row[4].split('\;') if row[4] else [],
            'question_id': row[5],
            'answer': row[6].split('\;') if row[6] else []
        })
        idx += 1
    return jsonify({'questions': data, 'check_id': check_id})



@checker.route('%sq-preview' % __ENDPOINT_PRE__, methods=['POST'])
def q_preview():
    q_id = request.json.get('q_id')
    if not q_id :
        return jsonify({'error': 'ID are required'}), 400
    db_conn = DatabaseConnection()
    db_conn.connect()
    result = db_conn.execute_query('''SELECT b.id, b.content,b.options,b.answer,b.type 
    FROM quiz.check_question b  where b.id =%s limit 1''', (q_id,))
    db_conn.close()
    if len(result) == 0:
        return jsonify({'error': 'no question found'}), 400
    optRslt = []
    for opt in result[0][2].split('\;') if result[0][2] else []:
        val_lab =opt.split(':')
        optRslt.append({
            'value':val_lab[0],
            'label': val_lab[1]}
        )
    return jsonify({'question': {
        'id': result[0][0],
        'content': result[0][1],
        'options': optRslt,
        'answer': result[0][3].split('\;') if result[0][3] else [], 
        'type': result[0][4]
        }})

@checker.route('%sq-list-preview' % __ENDPOINT_PRE__, methods=['POST'])
def list_preview():
    a_id = request.json.get('a_id')
    type = request.json.get('type')
    s_id = request.json.get('s_id')
    if not a_id or not type :
        return jsonify({'error': 'ID and type are required'}), 400
    try :
        db_conn = DatabaseConnection()
        db_conn.connect()
        result = db_conn.execute_query('''SELECT 1 
            FROM quiz.activity_summary where id =%s and can_preview_q='Y' ''', (a_id,))
        if len(result) == 0:
            return jsonify({'error': 'this activity is not allowed to view questions'}), 400
        result = db_conn.execute_query('''SELECT b.id  
        FROM quiz.check_refer a,quiz.check_question b  where a.ref_id =%s and a.question_id=b.id order by b.id''', 
        (a_id if  type == 'ACTIVITY' else s_id,))
      
        if len(result) == 0:
            return jsonify({'error': 'no question found for choosed item'}), 400
        
        questions = []
        for row in result:
            questions.append(row[0])
        return jsonify({'questions':questions})

    finally:
        db_conn.close()