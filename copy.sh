#!/bin/bash
# 定义源目录和目标目录
SOURCE_DIR="D:/liteli/chatGPT/Code/langchain/docs/extras"
TARGET_DIR="./docs"

# 清空或创建目标目录
# rm -rf $TARGET_DIR
mkdir -p $TARGET_DIR

# 使用jupyter nbconvert将.ipynb文件转换为.md格式
# 这里的find命令会递归地查找所有.ipynb文件并转换它们
find $SOURCE_DIR -name "*.ipynb" -exec jupyter nbconvert --to markdown {} \;

# 使用find和tar命令将转换后的.md文件复制到目标目录
# 首先，查找所有.md文件并将它们打包为一个tar文件
find $SOURCE_DIR -name "*.md" -print | tar -cvzf md_files.tar.gz -T -

# 然后，将tar文件解压缩到目标目录中，并去掉不必要的路径部分
tar -xvzf md_files.tar.gz --strip-components=7 -C $TARGET_DIR

# 删除临时的tar文件
rm md_files.tar.gz

# 生成包含所有未跟踪文件的 untracked_files.txt
git status --porcelain | awk '$1 == "??"{print $2}' > untracked_files.txt

# 创建 update_docs 文件夹
mkdir -p update_docs

# 读取 untracked_files.txt，并将每个文件复制到 update_docs 文件夹
while IFS= read -r file; do
    # 创建目标目录
    mkdir -p "update_docs/$(dirname "$file")"
    # 复制文件
    cp "$file" "update_docs/$file"
done < untracked_files.txt