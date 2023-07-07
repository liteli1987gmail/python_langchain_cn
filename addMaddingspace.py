import os
import subprocess

# 指定 cn_docs 文件夹的路径
folder_path = './snippets/'

# 遍历 cn_docs 文件夹下的每个文件
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        # 构建文件的完整路径
        file_path = os.path.join(root, file_name)
        print(file_path)
        
        # 构建要执行的命令
        command = f'npx md-padding -i {file_path}'
        
        # 执行命令
        subprocess.run(command, shell=True)
