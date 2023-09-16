#!/bin/bash

# 创建 update_docs 文件夹
rm -rf ./update_docs/
mkdir -p update_docs

# 读取 untracked_files.txt，并将每个文件复制到 update_docs 文件夹
while IFS= read -r file; do
    # 创建目标目录
    mkdir -p "update_docs/$(dirname "$file")"
    # 复制文件
    cp "$file" "update_docs/$file"
done < untracked_files.txt

# 运行 ./dotranslate.py
python ./translate.py



