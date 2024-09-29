import os
import json
from bs4 import BeautifulSoup

# 输入文件夹路径
input_folder = '/Users/massif/Desktop/1/'
# 输出文件夹路径
output_folder = '/Users/massif/Desktop/output_folder'

# 检查输出文件夹是否存在，如果不存在则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历输入文件夹中的每个文件
for filename in os.listdir(input_folder):
    # 构建输入文件的完整路径
    input_file_path = os.path.join(input_folder, filename)

    # 检查文件是否为 JSON 文件
    if filename.endswith('.json'):
        # 获取文件名（去掉文件扩展名）
        folder_name = os.path.splitext(filename)[0]
        # 构建输出文件夹的完整路径
        output_subfolder = os.path.join(output_folder, folder_name)

        # 检查输出子文件夹是否存在，如果不存在则创建
        if not os.path.exists(output_subfolder):
            os.makedirs(output_subfolder)

        # 读取 JSON 文件内容并按行处理
        with open(input_file_path, 'r', encoding='utf-8') as json_file:
            lines = json_file.readlines()
            for line in lines:
                try:
                    # 尝试解析 JSON 对象
                    data = json.loads(line)
                    # 获取文件名为 title 的内容并简化
                    title = data.get('title', 'Untitled').strip()[:20]  # 限制文件名长度为20
                    # 获取文件内容为 title 和 content 的内容合并
                    content = f"{data.get('title', '')}\n{data.get('content', '')}"

                    # 使用 BeautifulSoup 解析 HTML 内容，并获取文本
                    soup = BeautifulSoup(content, 'html.parser')
                    text_content = soup.get_text()

                    # 构建输出 txt 文件的完整路径
                    output_file_path = os.path.join(output_subfolder, f"{title}.txt")

                    # 将文本内容写入输出 txt 文件
                    with open(output_file_path, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(text_content)
                except json.JSONDecodeError:
                    # 如果解析失败，则忽略该行
                    continue

print("所有文件已生成。")
