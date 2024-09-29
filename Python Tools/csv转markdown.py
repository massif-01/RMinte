import csv
import os
import re
import sys

# 增加CSV字段大小限制
csv.field_size_limit(sys.maxsize)

# 定义输入CSV文件路径或文件夹路径
csv_path = '/Users/massif/Desktop/1.csv'  # 修改为实际路径
# 定义输出Markdown文件的根目录
output_root_dir = '/Users/massif/Desktop/output/'  # 修改为实际路径
# 定义拆分后的小CSV文件的目录
split_dir = '/Users/massif/Desktop/split_csv/'  # 修改为实际路径

# 每个小CSV文件包含的记录数
split_size = 2000

# 如果输出根目录不存在，则创建
if not os.path.exists(output_root_dir):
    os.makedirs(output_root_dir)

# 如果拆分目录不存在，则创建
if not os.path.exists(split_dir):
    os.makedirs(split_dir)


# 拆分CSV文件的函数
def split_csv_file(input_file, output_dir, chunk_size):
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        chunk_number = 0
        current_chunk = []

        for i, row in enumerate(csv_reader):
            current_chunk.append(row)
            if (i + 1) % chunk_size == 0:
                chunk_number += 1
                output_file = os.path.join(output_dir, f'chunk_{chunk_number}.csv')
                with open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
                    csv_writer = csv.writer(output_csv)
                    csv_writer.writerow(header)
                    csv_writer.writerows(current_chunk)
                current_chunk = []

        if current_chunk:
            chunk_number += 1
            output_file = os.path.join(output_dir, f'chunk_{chunk_number}.csv')
            with open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
                csv_writer = csv.writer(output_csv)
                csv_writer.writerow(header)
                csv_writer.writerows(current_chunk)


# 删除文本中的HTML、JavaScript代码以及"附件"及其后内容的函数
def clean_content(content):
    # 删除HTML标签
    content = re.sub(r'<[^>]+>', '', content)
    # 删除JavaScript代码
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    # 删除"附件"及其后内容
    content = re.sub(r'附件.*', '', content)
    # 删除特定JavaScript代码块
    content = re.sub(r'var s = .*?with\(document\)0\[\(getElementsByTagName\(\'head\'\)\[0\]\|\|body\)\.appendChild\(createElement\(\'script\'\)\)\.src=.*?\];', '', content, flags=re.DOTALL)
    return content


# 生成Markdown文件的函数
def process_csv_file(csv_file_path, output_dir):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)  # 跳过表头
        for row in csv_reader:
            # 获取文件名（去掉可能存在的前后空格）
            file_name = row[0].strip()
            # 获取文件内容
            file_content = row[1]

            # 当A列无文件名时，采用B列内容的前20个字符作为文件名
            if not file_name:
                file_name = file_content[:20].strip()

            # 替换文件名中的非法字符
            file_name = "".join(x for x in file_name if x.isalnum() or x in (" ", "_")).rstrip()

            # 清理文件内容
            file_content = clean_content(file_content)

            # 定义Markdown文件的完整路径
            md_file_path = os.path.join(output_dir, f"{file_name}.md")

            # 确保Markdown文件的目录存在
            md_file_dir = os.path.dirname(md_file_path)
            if not os.path.exists(md_file_dir):
                os.makedirs(md_file_dir)

            # 写入Markdown文件
            with open(md_file_path, 'w', encoding='utf-8') as mdfile:
                mdfile.write(f"# {file_name}\n\n{file_content}")


# 处理指定文件或文件夹中的所有CSV文件
def process_csv_path(path, output_root_dir, split_dir, split_size):
    if os.path.isfile(path):
        csv_file_path = path
        output_dir = os.path.join(output_root_dir, os.path.splitext(os.path.basename(path))[0])

        # 如果输出目录不存在，则创建
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if not os.path.exists(csv_file_path):
            print(f"错误: 找不到指定的CSV文件: {csv_file_path}")
        else:
            try:
                # 先尝试直接处理原始CSV文件
                process_csv_file(csv_file_path, output_dir)
            except csv.Error as e:
                if 'field larger than field limit' in str(e):
                    print(f"检测到字段大小超出限制，开始拆分CSV文件: {csv_file_path}")
                    # 拆分CSV文件
                    split_csv_file(csv_file_path, split_dir, split_size)
                    # 处理每个拆分后的CSV文件
                    for chunk_file in os.listdir(split_dir):
                        chunk_file_path = os.path.join(split_dir, chunk_file)
                        process_csv_file(chunk_file_path, output_dir)
                else:
                    raise e
    elif os.path.isdir(path):
        for file_name in os.listdir(path):
            if file_name.endswith('.csv'):
                csv_file_path = os.path.join(path, file_name)
                output_dir = os.path.join(output_root_dir, os.path.splitext(file_name)[0])

                # 如果输出目录不存在，则创建
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                if not os.path.exists(csv_file_path):
                    print(f"错误: 找不到指定的CSV文件: {csv_file_path}")
                else:
                    try:
                        # 先尝试直接处理原始CSV文件
                        process_csv_file(csv_file_path, output_dir)
                    except csv.Error as e:
                        if 'field larger than field limit' in str(e):
                            print(f"检测到字段大小超出限制，开始拆分CSV文件: {csv_file_path}")
                            # 拆分CSV文件
                            split_csv_file(csv_file_path, split_dir, split_size)
                            # 处理每个拆分后的CSV文件
                            for chunk_file in os.listdir(split_dir):
                                chunk_file_path = os.path.join(split_dir, chunk_file)
                                process_csv_file(chunk_file_path, output_dir)
                        else:
                            raise e

    print("所有文件已生成。")


# 主程序逻辑
process_csv_path(csv_path, output_root_dir, split_dir, split_size)
