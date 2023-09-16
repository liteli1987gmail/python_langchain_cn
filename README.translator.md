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
    

