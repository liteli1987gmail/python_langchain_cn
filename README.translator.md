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

# 总之是运行这个文件后，获得_dist项目，是所有的docs的文件。

    - docs_skeleton 是mdx
    - snippets 是mdx, 公共用于导入
    - extras 是ipynb

# 中英文混排问题

    npx md-padding README.md

