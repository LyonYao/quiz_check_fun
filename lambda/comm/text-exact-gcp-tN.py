import re
import json
def extract_questions_and_answers(text):
    # 定义正则表达式模式来匹配从 "Topic 1 Question" 到 "Correct Answer:" 的内容
    pattern = re.compile(r"(Topic\s+12\s+Question\s+#\d+[\s\S]*?Correct Answer:\s*[A-Z]+(?:, [A-Z]+)*)", re.DOTALL)
    
 

    # 使用正则表达式查找所有匹配的部分
    matches = pattern.findall(text)
    
    questions = []
    
    for match in matches:
        question_data = {}
        
        # 提取问题编号
        question_number = re.search(r'Topic\s+12\s+Question\s+#(\d+)', match).group(1)
        question_data['question_number'] = question_number
        
        # 提取问题描述
        question_description = re.search(r'Question #\d+\n(.*?)(?=\n[A-Z]\.)', match, re.DOTALL).group(1).strip()
        question_data['question_description'] = question_description.replace('\n','  ')
        
        # 提取选项 re.findall(r'([A-Z])\. (.*?)(?=\n[A-Z]\.|Correct Answer:|$)', match, re.DOTALL)
        options = re.findall(r'(?<!\w)([A-Z])\. (.*?)(?=\n(?<![A-Z])[A-Z]\.|Correct Answer:|$)', match, re.DOTALL)
        question_data['options'] = {option[0]: option[1].strip().replace('\n','  ') for option in options}
        
        # 提取正确答案
        correct_answer = re.search(r'Correct Answer:\s*([A-Z]+(?:, [A-Z]+)*)', match).group(1)
        question_data['correct_answer'] = [c  for c in ''.join([ans.strip() for ans in correct_answer.split(', ')])]
        
        questions.append(question_data)
    
    return questions
kind= 'gcp'
def process_questions():
    with open('d:/lyon_study/quiz_check/quiz_check_fun/db/%s-c01-clean-t12.txt' %kind, 'r', encoding='utf-8') as file:
        content = file.read()
    
    qs= json.loads(content)
    rls=[]
    for q in qs:
        rls.append(extract_questions_and_answers(q))
    return rls
# Example usage
 
structured_data = process_questions()

with open('d:/lyon_study/quiz_check/quiz_check_fun/db/%s-c01-t12.json' % kind,'w',encoding='utf-8') as f:
    f.write(json.dumps(structured_data, indent=2, ensure_ascii=False))