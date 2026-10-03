<div align="center">

# GUST

![版本](https://img.shields.io/badge/version-2.0-blue?style=flat-square)
![许可证](https://img.shields.io/badge/license-AGPLv3-green?style=flat-square)
![无 Service Worker](https://img.shields.io/badge/service%20workers-absolutely%20not-red?style=flat-square)
![SVG 完美运行](https://img.shields.io/badge/svg%20functionality-gorgeous%20and%20beautiful-blue?style=flat-square)

</div>

---

## 相关链接

- 中文翻译仓库：https://github.com/cjhdevact/GUST-Chinese
- 上游原仓库：https://github.com/nautilus-os/GUST

---

## 这是什么？

GUST 是一个功能齐全的 Web 代理，**完整运行在单个 HTML 文件内**，无需任何安装、托管或终端操作即可使用。它由 Nautilus Labs 团队开发，目标是替代现有的所有其他代理，并彻底终结校园网络封锁代理的猫鼠游戏。

浏览器打开 `index-CHS.html` 即可使用。

---

## 工作原理

当你输入一个 URL，GUST 会通过 WebAssembly HTTP 客户端获取整个页面，重写每一个资源 URL，注入代理运行时脚本，并把结果渲染到一个沙盒 iframe 里。需要特别说明的是：**iframe 纯粹用于沙盒隔离**，你在 GUST 里访问的站点其实已经被代理过了。而在其他低质量的、自称可以不用 Service Worker 的“代理”里，iframe 往往只是简单指向另一个 URL（例如 `<iframe src="https://blocked-site.com">`），完全没有额外的重写或代理。这立刻就失败了，因为过滤器能看见发往被封域名的请求并直接掐掉。而在 GUST 内部，它通过 Wisp 隧道获取原始数据，并清洗代码，把每一个链接和资源都重定向回自己，然后把这份修改过的载荷注入 iframe 作为沙盒环境。这保证了被代理站点可以运行自己的脚本和样式，同时不会破坏 GUST 界面、不会把你的真实活动泄露给网络过滤器，也保证过滤器能看见的**唯一请求就是发往 Wisp 服务器的请求**。具体流程如下：

<img width="1440" height="1178" alt="image" src="https://github.com/user-attachments/assets/c2cbd934-4c5f-4341-95ae-190c9f66d828" /><br>

GUST 加载的每个页面在**任何其他脚本运行之前**都会被注入一小段脚本。这段脚本拦截了页面几乎所有试图逃出代理的方式：`location.href`、`window.open`、表单提交、`XMLHttpRequest`、`fetch`、`WebSocket`、`Worker`、`EventSource`、history API 的 push、锚点点击，甚至现代 SPA 使用的 Navigation API。它还会伪装 `document.cookie`、`localStorage`、`sessionStorage` 和 IndexedDB，让页面觉得自己就在真实源上。所有网络流量都经过 WISP WebSocket 服务器，所以你访问的站点永远看不到你的真实 IP。WISP 服务器充当 TCP/TLS 中继，目标服务器只能看到中继的地址，看不到你的。你可以自建 WISP 服务器，也可以使用公共的，GUST 在设置里支持服务器切换。

---

## SVG 是怎么工作的

如你所知，GUST 被设计成运行在单个 HTML 文件里。按照这个逻辑，我们把资源拆分成各自独立的文件——CSS 和 JS 各一份。然后，我们在 `.svg` 文件里使用 `<foreignObject>` 来加载其中的 HTML，同时利用 SVG 所用的 HTML 架构。最后，在加载之前确保所有内容都是 XML 安全的，避免 JavaScript 执行时出错。

---

## 功能特性

GUST 的功能比一个代理严格来说需要的还要多，但我们希望你的代理浏览器体验尽可能接近你的日常浏览器。

**浏览器体验**
- 多标签页浏览，支持拖拽排序、静音和标签页缓存
- 书签栏，支持网站图标
- 新标签页，带收藏夹、时钟和可自定义壁纸
- 最近浏览历史（本地存储）
- 地址栏集成搜索引擎（Brave、Bing）
- 所有常见导航按钮

**隐私与拦截**
- 内置广告与跟踪器拦截器，支持外观过滤和自定义 CSS 过滤规则
- User-Agent 伪装（请求头和 `navigator.userAgent`）
- WebRTC 拦截，防止 IP 泄露
- 按源隔离的 Cookie 罐

**开发者工具**
- 实时请求日志，带过滤、搜索和类型徽章
- DOM 元素检查器，带样式、盒模型和属性面板
- 浏览器指标面板（堆内存、缓存、网络、页面性能）
- 可拖拽调整的侧边面板，支持左右位置切换

**文件处理**
- 内置 PDF 查看器（PDF.js，分页 + 缩放）
- 内置图片查看器（缩放、平移、下载）
- 内置视频和音频播放器
- 内置文本/代码查看器，带语法高亮
- Range 请求支持，视频可拖动定位
- 文件下载通过 GUST 代理

**设置项**
- WISP 服务器配置，带实例级存储隔离
- 并发请求线程控制
- 字体大小滑块、面板宽度记忆
- 书签栏开关、时钟格式（12/24 小时制）
- 键盘快捷键编辑器
- 完整重置选项（出问题的时候用，有时候确实会出问题）
- 一大堆选项，兄弟你自己看吧（28 个选项！）

---

## 快速开始

**方式一：直接打开文件**

下载 `index-CHS.html`，用任意现代浏览器打开。就这样。整个配置流程就这样。

**方式二：托管它**

把 `index-CHS.html` 丢到任意静态托管上。GitHub Pages、Vercel、Cloudflare Pages、Netlify。都能用。

**方式三：嵌入它**

把它作为 `<iframe>` 放进另一个 HTML 文件里。从 Blob URL 里也行。从 data URI 里也行（虽然会很大）。基本上放哪儿都行。

---

## 技术栈

| 库 | 版本 | 用途 |
|---------|---------|---------|
| libcurl.js | latest | HTTP 客户端（WebAssembly） |
| WISP protocol | — | WebSocket TCP 隧道 |
| PDF.js | 4.2.67 | 浏览器内 PDF 渲染 |
| Font Awesome | 6.5.1 | 图标 |
| JetBrains Mono | — | 等宽字体 |
| Space Grotesk | — | 界面字体 |
| iso-639-1 | 2.1.11 | 语言代码（用于目前损坏的语言功能） |

---

## 致谢

| 姓名 | 他们实际做了什么 |
|--------|----------------------|
| **lanefiedler** | 构建了原始代理框架和 UI 外壳，成为今日 GUST 的基础 |
| **dinguschan** | 重新设计了浏览器界面，重写了代理 JS 的大部分，添加了目前大部分功能 |
| **x8rr** | 将 GUST 移植到 SVG、Bug 反馈、协助、以及本 README 的部分内容 |
| **Mercury Workshop** | 创造了 WISP 协议——让这一切成为可能的 WebSocket 隧道层 |
| **ading2210** | 构建了 libcurl.js——即编译为 WebAssembly 的 curl（绝对的神助攻） |
| **Mozilla Foundation** | PDF.js，说真的我没法从零写一整个 PDF 处理器，那太多了而且这个已经存在了 |

---

## 已知 Bug 和限制

- 某些复杂的 Web 特性无法完全代理：页面内的原生 WebSocket、WebRTC（可通过设置主动拦截）、以及被代理页面内的 Service Worker
- 有些链接在 GUST 内部无法跳转。目前只能把链接拖到地址栏 :/
- 语言/拼写检查功能在设置里标注为 `[已损坏]`。我们知道的，以后会修
- JavaScript 极重的 SPA 在导航拦截方面可能会有边缘情况

---

<div align="center">

由 Nautilus Labs 用 ❤️ 打造

简体中文翻译由 [cjhdevact](https://github.com/cjhdevact) 完成

</div>
