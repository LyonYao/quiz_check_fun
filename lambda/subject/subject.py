from flask import Blueprint, jsonify, request

from comm.db_connect import DatabaseConnection

subject = Blueprint('subject', __name__)
__ENDPOINT_PRE__ = '/api/subject/'


@subject.route('%slist' % __ENDPOINT_PRE__, methods=['POST'])
def list():
    aid = request.json.get('aid')
    if not aid:
        return jsonify({'error': 'ID is required'}), 400
    db_conn = DatabaseConnection()
    db_conn.connect()
    result = db_conn.execute_query('''SELECT id, activity_id, title, description,status 
	FROM quiz.subject_summary where activity_id =%s and status in(%s,%s) order by id''', (aid,'V','C',))
    data = []
    for row in result:
        data.append({
            'id': row[0],
            'activity_id': row[1],
            'title': row[2],
            'description': row[3],
            'status': row[4]
        })
    db_conn.close()
    return jsonify(data)



@subject.route('%scontent' % __ENDPOINT_PRE__, methods=['POST'])
def content_by_id():
    sub_id = request.json.get('id')
    if not sub_id:
        return jsonify({'error': 'ID is required'}), 400
    db_conn = DatabaseConnection()
    db_conn.connect()
    result = db_conn.execute_query('''SELECT  sub.id, sub.title, sub.description, con.content
    FROM quiz.subject_summary sub left join quiz.subject_content con on
                                   sub.id=con.subject_id  WHERE sub.id= %s ''', (sub_id,))
    data = []
    for row in result:
        data.append({
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'content': row[3]
        })
    db_conn.close()
    return jsonify(data)

@subject.route('%sget' % __ENDPOINT_PRE__, methods=['POST'])
def get_subject_by_id():
    subject_id = request.json.get('id')
    if not subject_id:
        return jsonify({'error': 'ID is required'}), 400
    db_conn = DatabaseConnection()
    db_conn.connect()
    result = db_conn.execute_query('''SELECT id, activity_id, title, description,status
	FROM quiz.subject_summary where  id=%s limit 1''', (subject_id,))
    if not result:
        db_conn.close()
        return jsonify({'error': 'subject not found'}), 404
    row = result[0]
    data = {
        'id': row[0],
        'activity_id': row[1],
        'title': row[2],
        'description': row[3],
        'status': row[4]
    }
    db_conn.close()
    return jsonify(data)

