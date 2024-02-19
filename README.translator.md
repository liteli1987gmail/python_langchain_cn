## 翻译程序使用说明


## 总之是运行这个文件后，获得_dist项目，是所有的docs的文件。

    - docs_skeleton 是mdx
    - snippets 是mdx, 公共用于导入
    - extras 是ipynb

## 中英文混排问题

    npx md-padding README.md

## 提交检测流程
    - 先检查修改后，做一次commit
    - 使用git将commit的文件路径保存到a_list.txt文件。`git show --pretty="" --name-only 7b36c51e01a4a44207476927f0594283a5c8fcc7`
    - git bash终端上执行 `sh extra_file.sh` 执行剩余文档的翻译工作。

## update_docs 来源
    - 根据上游仓库的新版本更新记录。比对当前版本和新拉取的版本的不同的文件地址。`git diff COMMIT_HASH^ COMMIT_HASH --name-only`

    - 获取文件地址之后，将该地址复制到b_list.txt中保存。

## 文档框架

```
mkdir _dist
cp -r {docs_skeleton,snippets} _dist
mkdir -p _dist/docs_skeleton/static/api_reference
cd api_reference
poetry run make html
cp -r _build/* ../_dist/docs_skeleton/static/api_reference
cd ..
cp -r extras/* _dist/docs_skeleton/docs
cd _dist/docs_skeleton
poetry run nbdoc_build
yarn install
yarn start
````
    
# LangChain 模板的翻译处理
- 先要在Langchain仓库中下载最新文档，找到根目录下的/templates文件夹。复制到翻译程序文件夹中。
- 在该文件夹下，找到所有的README文件，以及图片文件。
- 提取README文件的代码如下：
```
import os
import shutil

def copy_md_files(source_dir, target_dir):
    # 如果目标文件夹不存在，则创建
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 遍历源文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.md') or file.endswith('.mdx'):
                # 获取文件的上一级文件夹名字
                parent_folder_name = os.path.basename(root)
                # 构建目标文件的完整路径
                target_file_path = os.path.join(target_dir, f"{parent_folder_name}.md")
                # 构建源文件的完整路径
                source_file_path = os.path.join(root, file)
                # 复制并重命名文件
                shutil.copy(source_file_path, target_file_path)
                print(f"复制文件 {source_file_path} 到 {target_file_path}")

# 源文件夹路径
source_dir = './docs/templates'
# 目标文件夹路径
target_dir = './templates'

# 调用函数进行文件复制
copy_md_files(source_dir, target_dir)
```

- 执行翻译该文件夹下所有的文件
- 将翻译好的文件夹复制到 /docs/下，即为 `./docs/templates`
- 将图片复制到 `static/img`下，并且将代码中的图片路径替换为`/img/xxx.png`
