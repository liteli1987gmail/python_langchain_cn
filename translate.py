import os
from api import OpenAIapi
import json
import time
from datetime import datetime

initbatch_size = 4
maxtokens = 10000
mdx_dict = ""
error_parse = {}
done_filenames = []
translated_parse_dict = {}
target_lang = 'Chinese'

input_folder = 'update_docs/docs/'
output_folder = input_folder + '_to_' +  target_lang


def read_mdx_files_from_folder(folder_path):
    """
    Read all .md and .mdx files from a given folder and its subfolders.
    Returns a dictionary containing filenames, file hierarchy, and file content.
    """
    mdx_dict = {}

    # Traverse the folder to find all .md and .mdx files
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith(('.md', '.mdx')):
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, folder_path)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                mdx_dict[relative_path] = content.replace("\n", "$n").replace(":", "$:")

    return mdx_dict

# Test the function
# Replace 'your_folder_path' with the path of the folder you want to read
# folder_path = 'your_folder_path'
# mdx_dict = read_mdx_files_from_folder('./temp/transformer/internal')
# # print(mdx_dict)

examples_json = """
"{"relative_path.md": "<!--版权信息$n$n-->$n$n# 管道的实用工具$n$n本页列出了库提供的所有用于管道的实用函数。$n$n如果您正在研究库中的模型代码，那么这些函数大多数情况下是有用的。$n$n$n## 这是二号标题$n$n[[这是代码]] pipelines.ArgumentHandler$n$n","relative_path_other.md":"import CodeBlock from "@theme/CodeBlock";$n$n### 应用场景$n$n"}"
"""

# 构造翻译指令和MDX内容的组合
prefix = f"""Please identify and translate into {target_lang} only the natural language sentences in the following file content.
Recognize that metadata, code blocks, components, and semantic tags, and begin with '[[',and begin with '<',and begin with 'import' are non-natural language elements and should not be translated.
Headings, paragraphs, ordered lists, unordered lists, and block quotes in Markdown syntax are considered natural language and should be translated.
The output follow this format example:{examples_json}.Should be translated content is:
"""

# translated_dict = json.loads(OpenAIapi(prompt))
# print(translated_dict)

# Main function to handle the entire workflow
def process_files_in_batches(input_folder, output_folder):
    # Read all .md and .mdx files into a large dictionary
    mdx_dict = read_mdx_files_from_folder(input_folder)
    
    # Split the large dictionary into smaller batches
    items = list(mdx_dict.items())

    # 设置初始批次数量
    # batch_size=initbatch_size
    # i = 0
    translate_loop(items,output_folder)

def translate_loop(items_list,output_folder):
    # 初始化配置
    items = items_list
    batch_size=initbatch_size
    i = 0

    while i < len(items):

        # batch_dict = json.dumps(dict(items[i:i + batch_size]))

        # time.sleep(30)
        batch_items = items[i:i + batch_size] if batch_size > 0 else [items[i]]

        if len(batch_items) == 1:
            # 对单一元素进行特殊处理
            batch_dict = json.dumps({batch_items[0][0]: batch_items[0][1]})
        else:
            # 对多个元素进行常规处理
            # batch_dict = json.dumps(dict(batch_items))
            batch_dict = json.dumps(batch_items)

        # 检查batch_dict长度如果总的字符大于8000，只取1个文件
        if len(batch_dict) >= maxtokens:
            print(f"{len(batch_dict) >= maxtokens}")
            batch_size = 1
            batch_dict = json.dumps(items[i:i + batch_size])
            print(f"{batch_size}")
        elif len(batch_dict) < maxtokens:    
            batch_size += 1

        i += batch_size
            
        # Translate the batch (you would call your translation API here)
        # For the sake of this example, let's assume translated_batch = batch_dict
        surfix = f"""-content start-
                {batch_dict}
                -content end-
                翻译时保留所有的符号,所有符号均为英文模式。your json result is:"""
        prejson = OpenAIapi(prefix+surfix)
        print(f"""返回：prejson是否成功： {'{' and '}' in prejson}""")

        if not '}' in prejson :
            time.sleep(10)
            print(f""" '400' or '999' or '429'""")
            try:
                batch_dict = json.loads(batch_dict)
                # error_parse.update(batch_dict)
            except UnboundLocalError as e:
                print(f"Failed to parse data : {e}")
                continue     
        else:
            try:
                print(f"api返回的内容：{prejson}")
                translated_batch = json.loads(prejson)

                # Write the translated files back to the output folder
                write_translated_files_to_folder(translated_batch, output_folder)

            except json.JSONDecodeError as e:
                # error_parse.update(batch_dict)
                print(f"Failed to parse data : {error_parse}")
                continue  # 继续处理下一个数据项


def write_translated_files_to_folder(translated_dict, output_folder):
    """
    Write the translated content back to .md and .mdx files.
    The files are saved in the specified output folder, preserving the original file hierarchy.
    """
    for relative_path, content in translated_dict.items():
        full_output_path = os.path.join(output_folder, relative_path)
        done_filenames.append(full_output_path)
        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)  # Create directories if they don't exist
        with open(full_output_path, 'w', encoding='utf-8') as f:
            print(f"写入文件的内容：{content}")
            f.write(content.replace("$n", "\n").replace("$:",":"))
            translated_dict = {}


def fail_loop(timestamp_path,maxtokens):

    translate_loop(error_parse,output_folder)

    #  未能调试成功，本想要读取失败的内容再次翻译
    maxtokens = maxtokens + 2000
    with open(timestamp_path, 'r', encoding='utf-8') as f:
        fail_content_list = json.load(f)

        
        # json_dict = json.loads(fail_content_list)
         
        parsed_dicts = [{key: value} for key, value in fail_content_list.items()]
        print(f"是数组内字典parsed_dicts{parsed_dicts}")
        translate_loop(parsed_dicts,output_folder)     

def main():
    # 翻译
    process_files_in_batches(input_folder,output_folder)

    # Generate a timestamp string with a precision up to seconds
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create a filename using the timestamp
    
    filename = f'{input_folder}_failed_{timestamp_str}.json'

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(error_parse))

    with open('./done.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(done_filenames))

    # 翻译失败的文件再次翻译
    fail_loop(filename,maxtokens)    

if __name__ == "__main__":
    main()
    # fail_loop('./en_docs/codingcrashcourses8533_failed_2023-09-10_21-50-30.json',8000)