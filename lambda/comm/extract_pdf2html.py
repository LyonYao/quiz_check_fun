import fitz 

import os
import tempfile
def pdf_to_html(pdf_path, html_path):
    document = fitz.open(pdf_path)
    text = ""
    
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text("html")

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(text)


# 获取当前脚本所在的目录
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
root_dir = os.path.dirname(os.path.dirname(current_dir))
file = 'professional_cloud_architect_exam_guide_english'

# 调用函数进行转换
pdf_to_html(os.path.join(root_dir, 'db', file + '.pdf'), os.path.join(root_dir, 'db', file + '.html'))
print(f"转换完成: {os.path.join(root_dir, 'db', file + '.html')}")