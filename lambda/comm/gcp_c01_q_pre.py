



from db_connect import DatabaseConnection 
import json


with open('d:/lyon_study/quiz_check/quiz_check_fun/db/gcp-c01-t12.json','r',encoding='utf-8') as file:
    content = file.read()

Q_PREFIX='GCP_C01_Q_T12'
db = DatabaseConnection()
db.connect()

# db.execute_delete('delete from  quiz.check_question where id like %s ',(f'{Q_PREFIX}%',))
# db.execute_delete('delete from  quiz.check_refer where question_id like %s ',(f'{Q_PREFIX}%',))

ques= json.loads(content)
cnt = 0
for q in ques:
    qn =q[0]
    id = Q_PREFIX + qn['question_number']
    desc = qn['question_description'] +'<br/><br/>'
    ops = qn['options']
    correct_answer = qn['correct_answer']
    typ ='S' if len(correct_answer)<2 else 'M'
    answer = []
    for op in ops:
        answer.append(op)
    answer = sorted(answer)    
    ops_a = []
    ops_pair =[]
    for an in answer:
        ops_a.append('%s) %s' %(an, ops[an]))
        ops_pair.append('%s:%s'%(an,an))
    op_part = '<br/><br/>'.join(ops_a) +'<br/><br/>'

    content = '<h3> %s </h3> <p>%s</p> ' %(desc, op_part)
    db.execute_insert('''INSERT INTO quiz.check_question (id, content, options, answer, type) VALUES
    (%s, %s , %s, %s, %s )''',(id, content, '\;'.join(ops_pair),'\;'.join(correct_answer),typ,))
    db.execute_insert('''INSERT INTO quiz.check_refer (ref_id, question_id, type) VALUES
                      (%s,%s,%s)''',('0003',id, 'ACTIVITY',))

    print('''INSERT INTO quiz.check_question (id, content, options, answer, type) VALUES
    (%s, %s , %s, %s, %s )'''%(id, content, '\;'.join(ops_pair),'\;'.join(correct_answer),typ,))
    print('''INSERT INTO quiz.check_refer (ref_id, question_id, type) VALUES
                      (%s,%s,%s)'''%('0003',id, 'ACTIVITY',))
    cnt = cnt+1

db.commit()
db.close()
print(cnt)

    

