import os
import shutil

# 定义输入文件夹的路径
input_folder = '/Users/massif/Desktop/1/'  # 修改为实际路径
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
all_folder = os.path.join(desktop_path, 'all')

def get_all_files(input_folder):
    """获取输入文件夹及其二级文件夹中的所有文件"""
    all_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

def create_subfolders_and_move_files(input_folder, all_folder, group_size=200):
    """将文件按每200个分组，放入新的子文件夹，并将这些子文件夹放入'all'文件夹"""
    if not os.path.exists(all_folder):
        os.makedirs(all_folder)

    all_files = get_all_files(input_folder)
    all_files.sort()  # 可选：排序文件以确定分组的顺序

    for i in range(0, len(all_files), group_size):
        group = all_files[i:i+group_size]
        subfolder_name = str(i // group_size + 1)
        subfolder_path = os.path.join(all_folder, subfolder_name)

        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

        for file_path in group:
            file_name = os.path.basename(file_path)
            dest_file_path = os.path.join(subfolder_path, file_name)
            shutil.move(file_path, dest_file_path)

    print(f"所有文件已成功分组并移动到 '{all_folder}' 文件夹中。")

# 调用函数执行文件分组和移动
create_subfolders_and_move_files(input_folder, all_folder)

print("处理完成。")
