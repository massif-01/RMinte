import os
from docx import Document

# 定义输入文件夹的路径
input_folder = '/Users/massif/Desktop/1/'  # 修改为实际路径
output_folder = '/Users/massif/Desktop/output/'  # 输出文件夹路径

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

def convert_doc_to_txt(doc_path, output_folder):
    """将doc文件转换为txt文件"""
    # 检查文件是否存在
    if not os.path.exists(doc_path):
        print(f"文件不存在: {doc_path}")
        return

    # 提取文件名
    file_name = os.path.splitext(os.path.basename(doc_path))[0]
    txt_file_path = os.path.join(output_folder, f"{file_name}.txt")

    try:
        if doc_path.endswith('.docx'):
            doc = Document(doc_path)
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                for para in doc.paragraphs:
                    txt_file.write(para.text + '\n')
            # 删除临时的 .docx 文件
            os.remove(doc_path)
        elif doc_path.endswith('.doc'):
            doc = Document(doc_path)
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                for para in doc.paragraphs:
                    txt_file.write(para.text + '\n')
    except Exception as e:
        print(f"无法转换文件 {doc_path}: {e}")

# 遍历文件夹中的doc文件
for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.lower().endswith(('.doc', '.docx')):
            doc_path = os.path.join(root, file)
            convert_doc_to_txt(doc_path, output_folder)

print("处理完成。")
