from concurrent.futures import ThreadPoolExecutor
import requests
import os
import shutil
import json
from api import OpenAIapi
import time
from datetime import datetime

target_lang = "Chinese"
examples_json = """
"{"relative_path.md": "<!--版权信息$n$n-->$n$n# 管道的实用工具$n$n本页列出了库提供的所有用于管道的实用函数。$n$n如果您正在研究库中的模型代码，那么这些函数大多数情况下是有用的。$n$n$n## 这是二号标题$n$n[[这是代码]] pipelines.ArgumentHandler$n$n","relative_path_other.md":"import CodeBlock from "@theme/CodeBlock";$n$n### 应用场景$n$n"}"
"""

# 构造翻译指令和MDX内容的组合
prefix = f"""Please identify and translate into {target_lang} only the natural language sentences in the following file content.
Recognize that metadata, code blocks, components, and semantic tags, and begin with '[[',and begin with '<',and begin with 'import' are non-natural language elements and should not be translated.
Headings, paragraphs, ordered lists, unordered lists, and block quotes in Markdown syntax are considered natural language and should be translated.
The output follow this format example:{examples_json}.
should be translated content is:
"""
# 存储失败和成功的文件路径
failed_files = []
successful_files = []

# 重试次数
RETRY_COUNT = 3

# 批量大小
BATCH_SIZE = 10

def translate_file(file_path):
    global failed_files, successful_files
    retry = 0

    while retry < RETRY_COUNT:
        try:
            # 读取文件内容
            with open(file_path, 'r') as f:
                content = f.readlines()

            surfix = f"""
                ---content start---
                {file_path:content_dict}
                ---content end---
                翻译时保留所有的符号,所有符号均为英文模式。your json result is:"""
            prejson = OpenAIapi(prefix+surfix)

            print(f"""返回：{prejson}""")
            # API请求来翻译内容

            if len(prejson) > 4:
                # 创建备份
                shutil.copy(file_path, f"{file_path}.backup")

                # 覆盖原文件
                translated_content = json.loads(prejson[file_path])
                with open(file_path, 'w') as f:
                    f.writelines(translated_content)

                successful_files.append(file_path)
                break
            else:
                retry += 1
        except Exception as e:
            print(f"An error occurred: {e}")
            retry += 1

    if retry == RETRY_COUNT:
        failed_files.append(file_path)

# 获取目标文件夹内的所有文件
target_folder = "your_folder_path"
all_files = [os.path.join(target_folder, f) for f in os.listdir(target_folder) if os.path.isfile(os.path.join(target_folder, f))]

# 分批处理文件
for i in range(0, len(all_files), BATCH_SIZE):
    batch_files = all_files[i:i+BATCH_SIZE]

    # 使用线程池来并发处理文件
    with ThreadPoolExecutor() as executor:
        executor.map(translate_file, batch_files)

# 保存成功和失败的文件信息
with open("successful_files.json", "w") as f:
    json.dump(successful_files, f)

with open("failed_files.json", "w") as f:
    json.dump(failed_files, f)

print("Translation completed.")
print("Successful files:", successful_files)
print("Failed files:", failed_files)
