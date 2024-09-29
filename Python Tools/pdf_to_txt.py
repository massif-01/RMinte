import os
import re
import fitz  # PyMuPDF
from opencc import OpenCC  # 使用纯 Python 实现的 opencc


def clean_text(text):
    """清理文本中的多余空格和换行符"""
    # 替换多个空格为一个空格
    text = re.sub(r'\s+', ' ', text)
    # 去除开头和结尾的空格
    text = text.strip()
    return text


def convert_traditional_to_simplified(text):
    """将繁体文本转换为简体文本"""
    converter = OpenCC('t2s')  # 使用纯 Python 实现的 opencc
    simplified_text = converter.convert(text)
    return simplified_text


def convert_pdf_to_txt(pdf_file_path, output_folder):
    """将单个PDF文件转换为TXT文件"""
    try:
        pdf_document = fitz.open(pdf_file_path)
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        # 调试输出: 打印提取的文本长度
        print(f"提取的文本长度: {len(text)}")

        if not text.strip():
            print(f"警告: {pdf_file_path} 中未提取到任何文本")
            return

        # 清理文本
        cleaned_text = clean_text(text)

        # 将繁体文本转换为简体文本
        simplified_text = convert_traditional_to_simplified(cleaned_text)

        # 获取PDF文件的名称并替换后缀为txt
        base_name = os.path.basename(pdf_file_path)
        txt_file_name = os.path.splitext(base_name)[0] + '.txt'
        txt_file_path = os.path.join(output_folder, txt_file_name)

        # 将文本写入TXT文件
        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(simplified_text)

        print(f"已生成文件: {txt_file_path}")
    except Exception as e:
        print(f"处理文件 {pdf_file_path} 时出错: {e}")


def process_pdfs(input_path, output_folder):
    """处理单个PDF文件或文件夹中的所有PDF文件"""
    if not os.path.exists(input_path):
        print(f"输入路径不存在: {input_path}")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    if os.path.isfile(input_path):
        if input_path.endswith('.pdf'):
            print(f"处理单个文件: {input_path}")
            convert_pdf_to_txt(input_path, output_folder)
        else:
            print(f"输入路径不是PDF文件: {input_path}")
    else:
        pdf_files = [file for file in os.listdir(input_path) if file.endswith('.pdf')]
        if not pdf_files:
            print(f"在输入文件夹 {input_path} 中未找到任何PDF文件")
            return

        for root, _, files in os.walk(input_path):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_file_path = os.path.join(root, file)
                    print(f"处理文件: {pdf_file_path}")
                    convert_pdf_to_txt(pdf_file_path, output_folder)


# 示例用法
input_path = '/Users/massif/Desktop/1/'  # 修改为实际PDF文件路径或PDF文件夹路径
output_folder = '/Users/massif/Desktop/output'  # 修改为实际输出文件夹路径

# 调用函数处理单个PDF文件或文件夹中的PDF文件
process_pdfs(input_path, output_folder)

print("处理完成。")
