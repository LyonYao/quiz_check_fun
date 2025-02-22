



from db_connect import DatabaseConnection 
import json


with open('d:/lyon_study/quiz_check/quiz_check_fun/db/ali-aca-1.json','r',encoding='utf-8') as file:
    content = file.read()

ALI_ACA='ALI_ACA_Q'
db = DatabaseConnection()
db.connect()

db.execute_delete('delete from  quiz.check_question where id like %s ',(f'{ALI_ACA}%',))
db.execute_delete('delete from  quiz.check_refer where question_id like %s ',(f'{ALI_ACA}%',))

ques= json.loads(content)
cnt = 0
tmp = [it for sub1 in ques  for it in sub1]
for q in tmp:
    qn =q
    id = ALI_ACA + qn['question_number']
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
                      (%s,%s,%s)''',('0004',id, 'ACTIVITY',))

    print('''INSERT INTO quiz.check_question (id, content, options, answer, type) VALUES
    (%s, %s , %s, %s, %s )'''%(id, content, '\;'.join(ops_pair),'\;'.join(correct_answer),typ,))
    print('''INSERT INTO quiz.check_refer (ref_id, question_id, type) VALUES
                      (%s,%s,%s)'''%('0004',id, 'ACTIVITY',))
    cnt = cnt+1

db.commit()
db.close()
print(cnt)

    

