import re
import json

def process_questions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    pattern = re.compile(r"(Topic\s+5\s+Question\s+#\d+[\s\S]*?Correct Answer:\s*[A-Z]+)", re.DOTALL)
    
    matches = pattern.findall(content)
    
    return matches
kind ='gcp'
# Example usage
file_path = 'd:/lyon_study/quiz_check/quiz_check_fun/db/%s-c01.txt' %kind
structured_data = process_questions(file_path)

with open('d:/lyon_study/quiz_check/quiz_check_fun/db/%s-c01-clean-t5.txt' %kind,'w',encoding='utf-8') as f:
    f.write(json.dumps(structured_data, indent=2, ensure_ascii=False))