/**
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 *
 * @format
 */

import React from "react";
import { Redirect } from "@docusaurus/router";

export default function Home() {
  return <Redirect to="docs/" />;
}



// import React from 'react';
// import clsx from 'clsx';
// import Link from '@docusaurus/Link';
// import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
// import Layout from '@theme/Layout';
// import HomepageFeatures from '@site/src/components/HomepageFeatures';

// import styles from './index.module.css';

// function HomepageHeader() {
//   const {siteConfig} = useDocusaurusContext();
//   return (
//     <header className={clsx('hero hero--primary', styles.heroBanner)}>
//       <div className="container">
//         <h1 className="hero__title">{siteConfig.tag}</h1>
//         {/* <p className="hero__subtitle">{siteConfig.tagline}</p> */}
//         <div className={styles.buttons}>
//           <Link
//             className="button button--secondary button--lg"
//             to="/docs/">
//             {siteConfig.tagline} - 5分钟上手 ⏱️
//           </Link>
//         </div>
//         <div className={styles.introwrap}>
//         <p> 🚀  <Link className="button button--secondary button--lg" to="https://python.langchain.com.cn/docs/get_started/introduction"> Langchain 中文文档 PYTHON 版本</Link></p>
//         <p> 📚  <Link className="button button--secondary button--lg" to="https://js.langchain.com.cn/docs/"> Langchain 中文文档 JS/TS 版本</Link></p>
//         <p> 📃  <Link className="button button--secondary button--lg" to="https://cookbook.langchain.com.cn/docs/"> Langchain COOKBOOK 教程</Link></p>
//         <p> 🚀  <Link className="button button--secondary button--lg" to="https://docs.langchain.com.cn/docs/"> Langchain Concepts 关键概念</Link></p>

//         </div>
//         <div className={styles.introwrap}>
//           <img src='https://pic1.zhimg.com/80/v2-31131dcb1732cb5bca7c182c9e8da046_r.jpg'></img>
//         </div>
//       </div>
//     </header>
//   );
// }

// export default function Home() {
//   const {siteConfig} = useDocusaurusContext();
//   return (
//     <Layout
//       title={`${siteConfig.title}`}
//       description="LangChain Concepts 中文文档教程 <head />">
//       <HomepageHeader />
//     </Layout>
//   );
// }
