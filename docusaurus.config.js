/* eslint-disable global-require,import/no-extraneous-dependencies */

// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion
// eslint-disable-next-line import/no-extraneous-dependencies
const { ProvidePlugin } = require("webpack");
const path = require("path");

const examplesPath = path.resolve(__dirname, ".", "examples", "src");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "🦜️🔗 Langchain",
  tagline: "Langchain中文网 跟着langchain学AI应用开发",
  favicon: "img/favicon.ico",
  customFields: {
    mendableAnonKey: process.env.MENDABLE_ANON_KEY,
  },
  scripts: [
    "img/hmbd.js"
  ],
  // Set the production url of your site here
  url: "https://js.langchain.com.cn",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: "/",

  onBrokenLinks: "ignore",
  onBrokenMarkdownLinks: "ignore",

  plugins: [
    () => ({
      name: "custom-webpack-config",
      configureWebpack: () => ({
        plugins: [
          new ProvidePlugin({
            process: require.resolve("process/browser"),
          }),
        ],
        resolve: {
          fallback: {
            path: false,
            url: false,
          },
          alias: {
            "@examples": examplesPath
          },
        },
        module: {
          rules: [
            {
              test: examplesPath,
              use: ["json-loader", "./code-block-loader.js"],
            },
            {
              test: /\.m?js/,
              resolve: {
                fullySpecified: false,
              },
            },
            {
              test: /\.ts$/,
              use: 'raw-loader'
            }
          ],
        },
      }),
    }),
  ],

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          editUrl: "https://github.com/liteli1987gmail/js-langchain-CN/tree/main/",
          remarkPlugins: [
            [require("@docusaurus/remark-plugin-npm2yarn"), { sync: true }],
          ],
          async sidebarItemsGenerator({
            defaultSidebarItemsGenerator,
            ...args
          }) {
            const sidebarItems = await defaultSidebarItemsGenerator(args);
            sidebarItems.forEach((subItem) => {
              // This allows breaking long sidebar labels into multiple lines
              // by inserting a zero-width space after each slash.
              if (
                "label" in subItem &&
                subItem.label &&
                subItem.label.includes("/")
              ) {
                // eslint-disable-next-line no-param-reassign
                subItem.label = subItem.label.replace(/\//g, "/\u200B");
              }
            });
            return sidebarItems;
          },
        },
        pages: {
          remarkPlugins: [require("@docusaurus/remark-plugin-npm2yarn")],
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      prism: {
        theme: require("prism-react-renderer/themes/vsLight"),
        darkTheme: require("prism-react-renderer/themes/vsDark"),
      },
      image: "img/parrot-chainlink-icon.png",
      metadata: [
        { name: 'keywords', content: 'langchain,LLM,chatGPT,应用开发' },
        {
          name: 'description', content: 'LangChain中文站，助力大语言模型LLM应用开发、chatGPT应用开发。'
        }],
      navbar: {
        title: "LangChain 🦜️🔗 中文网，跟着LangChain一起学LLM/GPT开发",
        items: [
          {
            href: "https://docs.langchain.com/docs/",
            label: "Concepts",
            position: "left",
          },
          {
            href: "https://www.langchain.com.cn/",
            label: "Python Docs",
            position: "left",
          },
          {
            to: "/docs/",
            label: "JS/TS Docs",
            position: "left",
          },
          // Please keep GitHub link to the right for consistency.
          {
            href: "https://github.com/liteli1987gmail/js-langchain-CN",
            label: "GitHub",
            position: "right",
          },
        ],
      },
      footer: {
        style: "light",
        links: [
          {
            title: "Community",
            items: [
              {
                label: "Langchain英文官网",
                href: "https://www.Langchain.com",
              },
              {
                label: "Langchain GitHub",
                href: "https://github.com/hwchase17/langchain",
              },
              {
                label: "LLM/GPT应用外包开发",
                href: "http://www.r-p-a.com/llm-gpt-kaifa/",
              }
            ],
          },
          {
            title: "LLM/GPT生态",
            items: [
              {
                label: "OpenAI 文档",
                href: "https://www.openaidoc.com.cn"
              },
              {
                label: "Milvus 文档",
                href: "https://www.milvus-io.com"
              },
              {
                label: "Pinecone 文档",
                href: "https://www.pinecone-io.com/"
              }
            ]
          },
          {
            title: "GitHub",
            items: [
              {
                label: "Python",
                href: "https://github.com/liteli1987gmail/langchainzh",
              },
              {
                label: "JS/TS",
                href: "https://github.com/liteli1987gmail/js-langchain-CN",
              },
            ],
          },
          {
            title: "LangChain技术交流社群",
            items:[
             {html: `
              <img src="https://pic1.zhimg.com/80/v2-31131dcb1732cb5bca7c182c9e8da046_r.jpg" alt="扫我，入群" width="280" height="330"/>`
            } ]
            
          }
        ],
        // logo: {
        //   alt: 'LangChain中文网',
        //   // src: 'img/quncode.png',
        //   src:'https://pic1.zhimg.com/80/v2-31131dcb1732cb5bca7c182c9e8da046_r.jpg',
        //   width: 320,
        //   height: 380,
        // },
        copyright: `Copyright © ${new Date().getFullYear()} LangChain中文网. 沪ICP备2023014280号-3`,
      },
    }),
};

module.exports = config;
