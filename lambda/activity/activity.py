from flask import Blueprint, jsonify, request

from comm.db_connect import DatabaseConnection
import random
import string
import uuid

activity = Blueprint('activity', __name__)
__ENDPOINT_PRE__ = '/api/activity/'


@activity.route('%slist' % __ENDPOINT_PRE__, methods=['POST'])
def list():
    db_conn = DatabaseConnection()
    db_conn.connect()
    result = db_conn.execute_query('''SELECT id, name, start_time, end_time, status, location, description, fee, 
                                   created_at, updated_at, created_by, updated_by, visible,can_check,can_reg,can_preview_q
	FROM quiz.activity_summary where visible =%s order by id''', ('Y',))
    data = []
    for row in result:
        data.append({
            'id': row[0],
            'name': row[1],
            'start_time': row[2],
            'end_time': row[3],
            'status': row[4],
            'location': row[5],
            'description': row[6],
            'fee': row[7],
            'created_at': row[8],
            'updated_at': row[9],
            'created_by': row[10],
            'updated_by': row[11],
            'visiable': row[12],
            'can_check': row[13]== 'Y',
            'can_reg': row[14] == 'Y',
            'can_preview_q':row[15]=='Y'
        })
    db_conn.close()
    return jsonify(data)



@activity.route('%scontent' % __ENDPOINT_PRE__, methods=['POST'])
def content_by_id():
    content_id = request.json.get('id')
    if not content_id:
        return jsonify({'error': 'ID is required'}), 400
    db_conn = DatabaseConnection()
    db_conn.connect()
    result = db_conn.execute_query('''SELECT  act.id, act.name, con.content
    FROM quiz.activity_summary act left join quiz.activity_content con on
                                   act.id=con.activity_id  WHERE act.id= %s AND 
                                   act.visible = %s''', (content_id, 'Y'))
    data = []
    for row in result:
        data.append({
            'id': row[0],
            'name': row[1],
            'content': row[2]
        })
    db_conn.close()
    return jsonify(data)

@activity.route('%sget' % __ENDPOINT_PRE__, methods=['POST'])
def get_activity_by_id():
    activity_id = request.json.get('id')
    if not activity_id:
        return jsonify({'error': 'ID is required'}), 400
    db_conn = DatabaseConnection()
    db_conn.connect()
    result = db_conn.execute_query('''SELECT id, name, start_time, end_time, status, location, description, fee, 
                                   created_at, updated_at, created_by, updated_by, visible,can_check,can_reg,
                                   can_preview_q
    FROM quiz.activity_summary WHERE id = %s AND visible = %s limit 1''', (activity_id, 'Y'))
    if not result:
        db_conn.close()
        return jsonify({'error': 'Activity not found'}), 404
    row = result[0]
    data = {
        'id': row[0],
        'name': row[1],
        'start_time': row[2],
        'end_time': row[3],
        'status': row[4],
        'location': row[5],
        'description': row[6],
        'fee': row[7],
        'created_at': row[8],
        'updated_at': row[9],
        'created_by': row[10],
        'updated_by': row[11],
        'visible': row[12],
        'can_check':  row[13]== 'Y',
        'can_reg': row[14] == 'Y',
        'can_preview_q':row[15]=='Y'
    }
    db_conn.close()
    return jsonify(data)


@activity.route('%sreg' % __ENDPOINT_PRE__, methods=['POST'])
def reg():
    activity_id = request.json.get('id')
    reg_name = request.json.get('name')
    if not activity_id:
        return jsonify({'error': 'ID is required'}), 400
    if not reg_name:
        return jsonify({'error': 'name is required'}), 400

    db_conn = DatabaseConnection()
    db_conn.connect()
    result = db_conn.execute_query('''SELECT  count(0) 
        FROM quiz.activity_summary act WHERE id= %s  ''', (activity_id,))
    if result[0][0] == 0:
        db_conn.close()
        return jsonify({'error': 'invalid ID'}), 400
    reg_cde_tmp = reg_name.replace(" ", "").upper()
    if len(reg_cde_tmp) ==0:
        return jsonify({'error': 'name is required'}), 400
    while True:
        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        reg_tmp  =reg_cde_tmp + random_code
        result = db_conn.execute_query('''SELECT  count(0) 
        FROM quiz.activity_reg act WHERE activity_id= %s AND 
                                    reg_code = %s''', (activity_id, reg_tmp,))
        if result[0][0] == 0:
            break
    reg_uuid = str(uuid.uuid4()).replace('-','')[:31]
    db_conn.execute_insert('''INSERT INTO quiz.activity_reg (id,activity_id, reg_code, reg_name, reg_time)
                           values(%s, %s, %s, %s, now())''', (reg_uuid, activity_id, reg_tmp, reg_name,))
    db_conn.commit()
    db_conn.close()
    return jsonify({'reg_code': reg_tmp})