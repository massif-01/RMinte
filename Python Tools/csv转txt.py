import csv
import os
import sys

# 增加CSV字段大小限制
csv.field_size_limit(sys.maxsize)

# 定义输入CSV文件夹的路径
csv_folder_path = '/Users/massif/Desktop/1/'  # 修改为实际路径
# 定义输出TXT文件的根目录
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


# 生成TXT文件的函数
def process_csv_file(csv_file_path, output_dir):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)  # 跳过表头
        for row in csv_reader:
            # 获取文件名（去掉可能存在的前后空格）
            file_name = row[0].strip()
            # 获取文件内容
            file_content = row[1]

            # 当A列无文件名时，采用B列内容的前30个字符作为文件名
            if not file_name:
                file_name = file_content[:30].strip()

            # 替换文件名中的非法字符
            file_name = "".join(x for x in file_name if x.isalnum() or x in (" ", "_")).rstrip()

            # 定义TXT文件的完整路径
            txt_file_path = os.path.join(output_dir, f"{file_name}.txt")

            # 确保TXT文件的目录存在
            txt_file_dir = os.path.dirname(txt_file_path)
            if not os.path.exists(txt_file_dir):
                os.makedirs(txt_file_dir)

            # 写入TXT文件
            with open(txt_file_path, 'w', encoding='utf-8') as txtfile:
                txtfile.write(file_content)


# 处理指定文件夹中的所有CSV文件
def process_csv_folder(folder_path, output_root_dir, split_dir, split_size):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(folder_path, file_name)
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
process_csv_folder(csv_folder_path, output_root_dir, split_dir, split_size)
