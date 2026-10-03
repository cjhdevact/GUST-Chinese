<div align="center">

# GUST

![version](https://img.shields.io/badge/version-1.0-blue?style=flat-square)
![license](https://img.shields.io/badge/license-AGPLv3-green?style=flat-square)
![no service workers](https://img.shields.io/badge/service%20workers-absolutely%20not-red?style=flat-square)
![totally working svg](https://img.shields.io/badge/svg%20functionality-gorgeous%20and%20beautiful-blue?style=flat-square)

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

## 为什么学校封不掉它

市面上所有 Web 代理都依赖一样东西——**Service Worker**（服务工作者），一种在网络请求到达浏览器之前拦截请求的后台脚本。它是任何 Web 代理的核心组件，负责与服务器通信并转发你的请求，但 Service Worker **始终需要一个在线服务器才能运行**。这意味着传统代理只在特定 URL 上托管时才能工作，一旦这个 URL 被封，代理就死了。你大概很熟悉这场与管理员之间的猫鼠游戏——有人做了个链接，用个一两天，然后就被封了。

校园网络过滤器、管理员安装的浏览器扩展（比如 Securly、Lightspeed Systems、Linewize、Blocksi 等等），以及管理员控制的浏览器（比如 Chromebook MDM 策略）恰恰最擅长做这种事。学校维护着封禁列表，每天往里加新站点。很多过滤扩展还有更高级的功能——读取链接元数据来识别代理特征并自动加入封禁列表。还有更多扩展会限制后台能运行什么，这正是当前所有代理站点的最大死穴。

**GUST 完全不用 Service Worker**。下面是我们想出来的替代方案：

<img width="1440" height="1040" alt="image" src="https://github.com/user-attachments/assets/f5403020-c0b4-4d89-b795-cfa11b898c78" /><br>

取而代之，它使用 **libcurl.js**——一个编译为 WebAssembly 的完整 HTTP 库——通过一种叫 WISP 协议的 WebSocket 隧道直接发起请求。（感谢 Mercury Workshop 的贡献）整个代理引擎作为纯 JavaScript 运行在单个 HTML 文件内。这意味着：

- ✅ **可以作为本地文件运行**（`file://`），没有服务器、没有域名可封
- ✅ **可以托管在任何静态文件能放的地方**：GitHub Pages、Vercel、Netlify、U 盘、Google 文档、Google 协作平台……
- ✅ **可以托管在 JSDelivr 或 CDN 上**，因为整个站点可以通过一个 SVG 文件加载
- ✅ **没有 Service Worker 可封**，因为它根本没注册过
- ✅ **可以被重命名、嵌入 iframe，或被另一个 HTML 文件包裹**，让过滤器无从下手
- ✅ **可以粘贴进任何在线所见即所得 HTML 编辑器**，因为它就是内联了 CSS 和 JS 的 HTML
- ✅ **可以被编译成 blob: 或 data: URL 打开**，毕竟它还是 HTML
- ✅ **可以写入 about:blank 页面后在那里使用**，不用我再说为什么了吧

一句话概括：大多数拦截器只能封 URL，而 GUST 是一个**文件**。你没法封一个文件而不严重破坏学生用户体验，就算他们真这么干了——HTML 可以被托管或打开在任何东西里。它是万维网的骨架。不用再打地鼠、不用再猫抓老鼠地找未封链接、不用再等学校封掉它们了！

---

## 截图

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/93db1bf0-2e4e-431e-a273-79f9229df4f4" />
<img width="1919" height="969" alt="image" src="https://github.com/user-attachments/assets/fcc15a77-dde1-4d22-bfc7-d809acfe2891" />
<img width="1920" height="973" alt="image" src="https://github.com/user-attachments/assets/c1388250-65a4-4878-9481-a2539c33079e" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3d332a9f-7713-419d-9350-bbe6c104a892" />
<img width="1920" height="973" alt="image" src="https://github.com/user-attachments/assets/3254ba60-0636-4ae9-962c-7173c0b358de" />
<img width="1920" height="973" alt="image" src="https://github.com/user-attachments/assets/0914ae53-eb7c-432a-9566-55c6923818ed" />
<img width="1920" height="973" alt="image" src="https://github.com/user-attachments/assets/17fb9ac8-15c8-4881-b65f-a0dc92324256" />

---

## 工作原理

当你输入一个 URL，GUST 会通过 WebAssembly HTTP 客户端获取整个页面，重写每一个资源 URL，注入代理运行时脚本，并把结果渲染到一个沙盒 iframe 里。需要特别说明的是：**iframe 纯粹用于沙盒隔离**，你在 GUST 里访问的站点其实已经被代理过了。而在其他低质量的、自称可以不用 Service Worker 的"代理"里，iframe 往往只是简单指向另一个 URL（例如 `<iframe src="https://blocked-site.com">`），完全没有额外的重写或代理。这立刻就失败了，因为过滤器能看见发往被封域名的请求并直接掐掉。而在 GUST 内部，它通过 Wisp 隧道获取原始数据，并清洗代码，把每一个链接和资源都重定向回自己，然后把这份修改过的载荷注入 iframe 作为沙盒环境。这保证了被代理站点可以运行自己的脚本和样式，同时不会破坏 GUST 界面、不会把你的真实活动泄露给网络过滤器，也保证过滤器能看见的**唯一请求就是发往 Wisp 服务器的请求**。具体流程如下：

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

下载 `index.html`，用任意现代浏览器打开。就这样。整个配置流程就这样。

**方式二：托管它**

把 `index.html` 丢到任意静态托管上。GitHub Pages、Vercel、Cloudflare Pages、Netlify、你学校 2003 年就上线至今还在跑的免费托管。都能用。

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