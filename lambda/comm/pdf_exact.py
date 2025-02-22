from PyPDF2 import PdfReader
import os
def read_pdf(file_path):
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    root_dir = os.path.dirname(os.path.dirname(current_dir))
    with open(os.path.join(root_dir,'db','gcp-c01.txt'),'wt',encoding='utf-8') as f1:
        with open(os.path.join(root_dir,'db',file_path), 'rb') as file:
            reader =PdfReader(file)
            for page_num in range( len(reader.pages)):
                page = reader.pages[page_num]
                f1.write(page.extract_text())

if __name__ == "__main__":
    pdf_path = 'gcp-1.pdf'
    read_pdf(pdf_path)