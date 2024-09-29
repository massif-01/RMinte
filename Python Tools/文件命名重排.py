import os
import shutil


def rename_and_copy_files(src_folder, dst_folder):
    # 检查源文件夹是否存在
    if not os.path.exists(src_folder):
        print(f"源文件夹 {src_folder} 不存在。")
        return

    # 如果目标文件夹不存在，则创建目标文件夹
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    # 获取源文件夹中的所有文件
    files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]

    # 按文件名排序
    files.sort()

    # 遍历所有文件，并按顺序重命名和复制
    for index, filename in enumerate(files, start=1):
        # 获取文件的后缀名
        file_extension = os.path.splitext(filename)[1]
        # 构建新的文件名
        new_filename = f"{index}{file_extension}"
        # 构建源文件和目标文件的完整路径
        src_file_path = os.path.join(src_folder, filename)
        dst_file_path = os.path.join(dst_folder, new_filename)

        # 复制文件并重命名
        shutil.copy2(src_file_path, dst_file_path)
        print(f"文件 {filename} 已重命名为 {new_filename} 并复制到目标文件夹。")

    print("所有文件已成功重命名并复制到目标文件夹。")


# 示例用法
src_folder = "/Users/massif/Desktop/1/"  # 替换为源文件夹的路径
dst_folder = "/Users/massif/Desktop/output/"  # 替换为目标文件夹的路径
rename_and_copy_files(src_folder, dst_folder)
