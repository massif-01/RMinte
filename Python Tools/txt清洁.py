import os
import re

# 定义输入文件夹的路径
input_folder = '/Users/massif/Desktop/4/'  # 修改为实际路径
extra_blank_lines_report_path = '/Users/massif/Desktop/extra_blank_lines_report.txt'  # 定义报告文件的路径
deletion_report_file_path = '/Users/massif/Desktop/deletion_report.txt'  # 定义删除报告文件的路径
code_report_file_path = '/Users/massif/Desktop/code_detection_report.txt'  # 定义代码检测报告文件的路径
js_code_removal_report_path = '/Users/massif/Desktop/js_code_removal_report.txt'  # 定义JS代码移除报告文件的路径

def remove_extra_blank_lines(file_path):
    """读取文件，删除多余的空行并重新写入文件"""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    has_blank_line = False
    found_extra_blank_lines = False

    for line in lines:
        if line.strip() == '':
            if not has_blank_line:
                new_lines.append(line)
                has_blank_line = True
            else:
                found_extra_blank_lines = True
        else:
            new_lines.append(line)
            has_blank_line = False

    # 重新写入文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

    return found_extra_blank_lines

def is_chinese(text):
    """检查文本是否包含中文字符"""
    return re.search(r'[\u4e00-\u9fff]', text) is not None

def contains_code(text):
    """检查文本是否包含可执行的代码"""
    code_patterns = [
        r'\bdef\b', r'\bclass\b',  # Python
        r'\bfunction\b', r'\bvar\b', r'\blet\b', r'\bconst\b',  # JavaScript
        r'#!/bin/bash', r'#!/usr/bin/env'  # Shell
    ]
    for pattern in code_patterns:
        if re.search(pattern, text):
            return True
    return False

def remove_js_code(text):
    """移除文本中的JavaScript代码"""
    js_code_pattern = r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>'
    new_text, num_subs = re.subn(js_code_pattern, '', text, flags=re.IGNORECASE)
    return new_text, num_subs > 0

def process_txt_files(input_folder, extra_blank_lines_report_path, deletion_report_file_path, code_report_file_path, js_code_removal_report_path):
    """处理文件夹中的所有TXT文件，删除多余空行并生成报告；检测并删除空文档、不包含中文内容的文档以及包含可执行代码的文档，并生成报告；删除JS代码并生成报告"""
    files_with_extra_blank_lines = []
    deleted_files = []
    code_files = []
    js_code_removed_files = []

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)

                # 删除多余空行
                if remove_extra_blank_lines(file_path):
                    files_with_extra_blank_lines.append(file_path)

                # 检查文件是否为空
                if os.path.getsize(file_path) == 0:
                    print(f"删除空文件: {file_path}")
                    deleted_files.append(file_path)
                    os.remove(file_path)
                    continue

                # 检查文件内容是否包含中文
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not is_chinese(content):
                        print(f"删除不包含中文内容的文件: {file_path}")
                        deleted_files.append(file_path)
                        os.remove(file_path)
                        continue

                # 检查文件内容是否包含可执行代码
                if contains_code(content):
                    print(f"删除包含可执行代码的文件: {file_path}")
                    code_files.append(file_path)
                    os.remove(file_path)
                    continue

                # 删除JS代码
                new_content, js_code_removed = remove_js_code(content)
                if js_code_removed:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    js_code_removed_files.append(file_path)

    # 生成多余空行报告
    with open(extra_blank_lines_report_path, 'w', encoding='utf-8') as report_file:
        report_file.write("包含多余空行的文件列表:\n")
        for file_path in files_with_extra_blank_lines:
            report_file.write(f"{file_path}\n")
    print(f"多余空行报告已生成: {extra_blank_lines_report_path}")

    # 生成删除报告
    with open(deletion_report_file_path, 'w', encoding='utf-8') as report_file:
        report_file.write("删除的文件列表:\n")
        for file_path in deleted_files:
            report_file.write(f"{file_path}\n")
    print(f"删除报告已生成: {deletion_report_file_path}")

    # 生成代码检测报告
    with open(code_report_file_path, 'w', encoding='utf-8') as report_file:
        report_file.write("包含可执行代码的文件列表（并已删除）:\n")
        for file_path in code_files:
            report_file.write(f"{file_path}\n")
    print(f"代码检测报告已生成: {code_report_file_path}")

    # 生成JS代码移除报告
    with open(js_code_removal_report_path, 'w', encoding='utf-8') as report_file:
        report_file.write("移除JS代码的文件列表:\n")
        for file_path in js_code_removed_files:
            report_file.write(f"{file_path}\n")
    print(f"JS代码移除报告已生成: {js_code_removal_report_path}")

# 调用函数处理文件夹中的TXT文件
process_txt_files(input_folder, extra_blank_lines_report_path, deletion_report_file_path, code_report_file_path, js_code_removal_report_path)

print("处理完成。")
