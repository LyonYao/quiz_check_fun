import os
from bs4 import BeautifulSoup
import json
import html as ht
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
root_dir = os.path.dirname(os.path.dirname(current_dir))
def read_html(file_path):
    with open(os.path.join(root_dir,'db','original',file_path), 'r', encoding='utf-8') as file:
        ctx= file.read()
    return ctx

def parse_questions(html):
    
    #html = ht.unescape(html)
    soup = BeautifulSoup(html, 'html.parser')
    questions_container = soup.find('div', {'id': 'content_views'})
  
    # questions_container.findChildren('[]')
    p_tags = questions_container.find_all('p')
    
    questions = []
    question = None
    for p in p_tags:
        text = p.get_text()
        if any(text.strip().startswith(str(i)) for i in range(1000)):
            # 新的问题开始
            if question is not None:  # 如果不是第一个问题，则添加前一个问题到列表
                questions.append(question)
            question_number = ''.join(filter(str.isdigit, text.split('、')[0]))
            question_description = ''.join(text.split('、')[1:]).replace(r'\n',' <br/>')
            question = {
                "question_number": question_number,
                "question_description": question_description,
                "options": {},
                "correct_answer": []
            }
        elif text.startswith(('A', 'B', 'C', 'D', 'E', 'F','G','H')):
            # 处理选项
            option_letter = text[0]
            option_text = text[2:]
            question["options"][option_letter] = option_text
            if '<span style="background-color:#00ff00;">' in str(p):
                # 高亮表示正确答案
                question["correct_answer"].append(option_letter)
       
                
    if question is not None:  # 添加最后一个收集到的问题
        questions.append(question)
    soup.clear()    
    return questions

def save_to_file(sorted_data, filename='ali-aca-1.json'):
   # sorted_data = sorted(sorted_data, key=lambda x: int(x['question_number']))
    with open(os.path.join(root_dir,'db',filename), 'w', encoding='utf-8') as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=4)


import requests
from bs4 import BeautifulSoup

def fetch_webpage(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        
        # 检查请求是否成功
        if response.status_code == 200:
            print(f"获取成功{url}" )
            return response.text
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"请求过程中出现错误: {e}")
        return None

    finally: 
        response.close()
def save_to_file_1(content, file_path='webpage.html'):
    if os.path.exists(file_path):
        os.remove(file_path)
    soup = BeautifulSoup(content, 'html.parser')
    questions_container = soup.find('div', {'id': 'content_views'})
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(questions_container)) 



html_file_paths = ('https://blog.csdn.net/lx1056212225/article/details/143787469',
                   'https://blog.csdn.net/lx1056212225/article/details/143801355',
                   'https://blog.csdn.net/lx1056212225/article/details/143976501',
                   'https://blog.csdn.net/lx1056212225/article/details/144134090',
                   'https://blog.csdn.net/lx1056212225/article/details/144186387',
                   'https://blog.csdn.net/lx1056212225/article/details/144406416',
                   'https://blog.csdn.net/lx1056212225/article/details/144564097',)

# for i in range(0, len(html_file_paths)):
#     html_txt = fetch_webpage(html_file_paths[i])
#     save_to_file_1(html_txt,os.path.join(root_dir,
#                                          'db','original','ali-aca-csdn-'+(html_file_paths[i]).replace('https://blog.csdn.net/lx1056212225/article/details/','')+'.html'))

rslt=[]
for i in range(0, len(html_file_paths)):
    rslt.append(parse_questions(read_html('ali-aca-csdn-'+(html_file_paths[i]).replace('https://blog.csdn.net/lx1056212225/article/details/','')+'.html')))

save_to_file(rslt)

print("数据已成功解析并保存到文件")

