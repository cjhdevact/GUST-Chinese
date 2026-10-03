#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUST Patcher 界面汉化工具
https://github.com/cjhdevact/GUST-Chinese

适配提交：78df43014334176ca000bb252efc1185beb893a7

用法:
    python GUST-Patcher-Chinese.py GUST-Patcher.html                  # 原地替换，自动备份 .bak
    python GUST-Patcher-Chinese.py GUST-Patcher.html --dry-run        # 只预览
    python GUST-Patcher-Chinese.py GUST-Patcher.html -o out.html      # 指定输出
    python GUST-Patcher-Chinese.py GUST-Patcher.html --keep-made-with # 保留 "Made with by Nautilus Labs"
    python GUST-Patcher-Chinese.py GUST-Patcher.html --keep-github-url # 保留原 GitHub URL
    python GUST-Patcher-Chinese.py GUST-Patcher.html --no-credit      # 不注入翻译者信息
"""

import re
import sys
import argparse
from pathlib import Path
from collections import OrderedDict

# ═══════════════════════════════════════════════════════════════════
#  可配置项
# ═══════════════════════════════════════════════════════════════════
INJECT_TRANSLATOR_CREDIT = True    # 首页 tagline 下方注入翻译者信息
REMOVE_MADE_WITH_CREDIT  = True    # 移除标题栏 "Made with by Nautilus Labs"
REPLACE_GITHUB_URL       = True    # 替换显示用 GitHub URL

TRANSLATOR_NAME = 'GUST-Chinese'
GITHUB_REPO_URL = 'https://github.com/cjhdevact/GUST-Chinese'
GITHUB_DISPLAY  = 'github.com/cjhdevact/GUST-Chinese'

# ── 源码获取地址（用于修改 Patcher 拉取 GUST 源码的 URL） ──
SOURCE_RAW_URL = 'https://raw.githubusercontent.com/cjhdevact/GUST-Chinese/main/index-CHS.html'
SOURCE_GH_URL  = 'https://github.com/cjhdevact/GUST-Chinese/raw/refs/heads/main/index-CHS.html'
SOURCE_PROXY   = 'https://gh-proxy.com/'

# ═══════════════════════════════════════════════════════════════════
#  替换表
# ═══════════════════════════════════════════════════════════════════
REPLACEMENTS = OrderedDict([

    # ═══════════════════════════════════════════════════════════
    #  页面标题
    # ═══════════════════════════════════════════════════════════
    ('<title>GUST Patcher</title>',       '<title>GUST 定制器</title>'),

    # ═══════════════════════════════════════════════════════════
    #  标题栏按钮
    # ═══════════════════════════════════════════════════════════
    ('</i> Refresh Source<',              '</i> 刷新源码<'),
    ('</i> Paste Source<',                '</i> 粘贴源码<'),
    ('</i> Download Patched GUST<',       '</i> 下载定制版 GUST<'),

    # ═══════════════════════════════════════════════════════════
    #  title="..." 属性
    # ═══════════════════════════════════════════════════════════
    ('title="View GUST on GitHub"',       'title="在 GitHub 上查看 GUST"'),
    ('title="Paste GUST source manually"','title="手动粘贴 GUST 源码"'),
    ('title="Please apply a patch"',      'title="请应用至少一个补丁"'),

    # ═══════════════════════════════════════════════════════════
    #  品牌副标题
    # ═══════════════════════════════════════════════════════════
    ('<span class="brand-sub gust-sub-anim">Patcher</span>',
                                          '<span class="brand-sub gust-sub-anim">定制器</span>'),
    ('<span class="hp-brand-sub gust-sub-anim">Patcher</span>',
                                          '<span class="hp-brand-sub gust-sub-anim">定制器</span>'),

    # ═══════════════════════════════════════════════════════════
    #  加载遮罩
    # ═══════════════════════════════════════════════════════════
    ('>Fetching GUST source…<',           '>正在获取 GUST 源码…<'),
    ('>Connecting…<',                     '>正在连接…<'),

    # ═══════════════════════════════════════════════════════════
    #  侧边栏分区标签
    # ═══════════════════════════════════════════════════════════
    ('>Patcher<',                         '>定制器<'),
    ('>Core Features<',                   '>核心功能<'),

    # ═══════════════════════════════════════════════════════════
    #  侧边栏导航项（含新 AI Assistant）
    # ═══════════════════════════════════════════════════════════
    ('<span class="nav-label">Home</span>',        '<span class="nav-label">主页</span>'),
    ('<span class="nav-label">Connection</span>',  '<span class="nav-label">连接</span>'),
    ('<span class="nav-label">Fallback</span>',    '<span class="nav-label">回退</span>'),
    ('<span class="nav-label">AI Assistant</span>','<span class="nav-label">AI 助手</span>'),
    ('<span class="nav-label">Search</span>',      '<span class="nav-label">搜索</span>'),
    ('<span class="nav-label">Privacy</span>',     '<span class="nav-label">隐私</span>'),
    ('<span class="nav-label">Cache</span>',       '<span class="nav-label">缓存</span>'),
    ('<span class="nav-label">Files &amp; Media</span>',
                                                    '<span class="nav-label">文件与媒体</span>'),
    ('<span class="nav-label">Appearance</span>',  '<span class="nav-label">外观</span>'),
    ('<span class="nav-label">Home Screen</span>', '<span class="nav-label">主页设置</span>'),
    ('<span class="nav-label">Shortcuts</span>',   '<span class="nav-label">快捷键</span>'),
    ('<span class="nav-label">Language</span>',    '<span class="nav-label">语言</span>'),
    ('<span class="nav-label">Tutorial</span>',    '<span class="nav-label">教程</span>'),
    ('<span class="nav-label">Tab System</span>',  '<span class="nav-label">标签页系统</span>'),
    ('<span class="nav-label">Ad Blocker</span>',  '<span class="nav-label">广告拦截</span>'),
    ('<span class="nav-label">Dev Tools</span>',   '<span class="nav-label">开发者工具</span>'),
    ('<span class="nav-label">Metrics</span>',     '<span class="nav-label">指标</span>'),

    # ═══════════════════════════════════════════════════════════
    #  首页 - Hero 区
    # ═══════════════════════════════════════════════════════════
    ('>Customize your GUST build before you download it.<',
                                          '>下载前自定义你的 GUST 构建版本。<'),

    # ═══════════════════════════════════════════════════════════
    #  首页 - 预设卡片
    # ═══════════════════════════════════════════════════════════
    ('>Base GUST<',                         '>基础版 GUST<'),
    ('<span class="recommended-badge"><i class="fas fa-star" style="font-size:8px;"></i> Recommended</span>',
                                            '<span class="recommended-badge"><i class="fas fa-star" style="font-size:8px;"></i> 推荐</span>'),
    ('>Straight from GitHub<',              '>直接来自 GitHub<'),
    ("Download the latest unmodified GUST source directly from the official GitHub repository with no custom patches applied. The most stable version of GUST, and the team at Nautilus Labs's recommended build.",
                                            '直接从官方 GitHub 仓库下载最新未修改的 GUST 源码，不应用任何自定义补丁。这是最稳定的 GUST 版本，也是 Nautilus Labs 团队推荐的构建版本。'),

    ('</i> Download Base GUST',             '</i> 下载基础版 GUST'),
    ('</i> Download GUST Lite<',            '</i> 下载 GUST 精简版<'),
    ('</i> Fetching…',                      '</i> 正在获取…'),

    ('>GUST Lite<',                         '>GUST 精简版<'),
    ('>Trimmed-down build<',                '>精简构建<'),
    ('Removes thread controls, favicon proxying, WebRTC blocking, smart request headers, spellcheck, request &amp; page user-agent spoofing, dev console logs, dev inspector, metrics, and the language picker.',
                                            '移除线程控制、网站图标代理、WebRTC 拦截、智能请求头、拼写检查、请求与页面 User-Agent 伪装、开发者控制台日志、元素检查器、指标和语言选择器。'),

    # ═══════════════════════════════════════════════════════════
    #  通用按钮 / 标签
    # ═══════════════════════════════════════════════════════════
    ('>Select all<',                        '>全选<'),
    ('>None<',                              '>全不选<'),

    # ═══════════════════════════════════════════════════════════
    #  Section 标题
    # ═══════════════════════════════════════════════════════════
    ('<div class="section-title">Language</div>',    '<div class="section-title">语言</div>'),
    ('<div class="section-title">AI Assistant</div>','<div class="section-title">AI 助手</div>'),
    ('<div class="section-title">Connection</div>',  '<div class="section-title">连接</div>'),
    ('<div class="section-title">Fallback WISP</div>','<div class="section-title">回退 WISP</div>'),
    ('<div class="section-title">Search</div>',      '<div class="section-title">搜索</div>'),
    ('<div class="section-title">Privacy</div>',     '<div class="section-title">隐私</div>'),
    ('<div class="section-title">Cache</div>',       '<div class="section-title">缓存</div>'),
    ('<div class="section-title">Files &amp; Media</div>', '<div class="section-title">文件与媒体</div>'),
    ('<div class="section-title">Appearance</div>',  '<div class="section-title">外观</div>'),
    ('<div class="section-title">Home Screen</div>', '<div class="section-title">主页设置</div>'),
    ('<div class="section-title">Shortcuts</div>',   '<div class="section-title">快捷键</div>'),
    ('<div class="section-title">Tutorial</div>',    '<div class="section-title">教程</div>'),
    ('<div class="section-title">Tab System</div>',  '<div class="section-title">标签页系统</div>'),
    ('<div class="section-title">Ad Blocker</div>',  '<div class="section-title">广告拦截</div>'),
    ('<div class="section-title">Dev Tools</div>',   '<div class="section-title">开发者工具</div>'),
    ('<div class="section-title">Metrics</div>',     '<div class="section-title">指标</div>'),

    # ═══════════════════════════════════════════════════════════
    #  Sidebar Master 栏
    # ═══════════════════════════════════════════════════════════
    ('>Show Language in Settings Sidebar<',   '>在设置侧边栏显示「语言」<'),
    ("Uncheck to remove the <strong>Language</strong> entry from GUST's Settings sidebar. The language picker panel will be hidden and its nav entry removed entirely.",
                                            '取消勾选即从 GUST 设置侧边栏中移除 <strong>语言</strong> 入口。语言选择面板将被隐藏，导航项也会被完全移除。'),

    ('>Show Connection in Settings Sidebar<', '>在设置侧边栏显示「连接」<'),
    ("Uncheck to remove the <strong>Connection</strong> entry from GUST's Settings sidebar. WISP URL, thread controls, WebRTC blocking, and smart headers will all be hidden from Settings and locked to their defaults.",
                                            '取消勾选即从 GUST 设置侧边栏中移除 <strong>连接</strong> 入口。WISP 地址、线程控制、WebRTC 拦截和智能请求头都将从设置中隐藏，并锁定为默认值。'),

    ('>Show Fallback in Settings Sidebar<',   '>在设置侧边栏显示「回退」<'),
    ("Uncheck to remove the <strong>Fallback</strong> entry from GUST's Settings sidebar. The fallback toggle, fallback WISP URL, retry policy, and error triggers will all be hidden from Settings.",
                                            '取消勾选即从 GUST 设置侧边栏中移除 <strong>回退</strong> 入口。回退开关、回退 WISP 地址、重试策略和错误触发条件都将从设置中隐藏。'),

    # ── 新增：AI Assistant 侧边栏主控 ──
    ('>Show AI Assistant in Settings Sidebar<', '>在设置侧边栏显示「AI 助手」<'),
    ("Uncheck to remove the <strong>AI Assistant</strong> entry from GUST's Settings sidebar and hide the AI toolbar button entirely. The assistant panel and all its settings will be inaccessible.",
                                            '取消勾选即从 GUST 设置侧边栏中移除 <strong>AI 助手</strong> 入口，并完全隐藏 AI 工具栏按钮。助手面板及其所有设置将无法访问。'),

    ('>Show Search in Settings Sidebar<',     '>在设置侧边栏显示「搜索」<'),
    ("Uncheck to remove the <strong>Search</strong> entry from GUST's Settings sidebar. The search engine picker, spellcheck toggle, and favicon proxy option will all be hidden from Settings.",
                                            '取消勾选即从 GUST 设置侧边栏中移除 <strong>搜索</strong> 入口。搜索引擎选择器、拼写检查开关和网站图标代理选项都将从设置中隐藏。'),

    ('>Show Privacy in Settings Sidebar<',    '>在设置侧边栏显示「隐私」<'),
    ("Uncheck to remove the <strong>Privacy</strong> entry from GUST's Settings sidebar. Ad blocking, user-agent spoofing, and custom filter rules will all be hidden from Settings.",
                                            '取消勾选即从 GUST 设置侧边栏中移除 <strong>隐私</strong> 入口。广告拦截、User-Agent 伪装和自定义过滤规则都将从设置中隐藏。'),

    ('>Show Cache in Settings Sidebar<',      '>在设置侧边栏显示「缓存」<'),
    ("Uncheck to remove the <strong>Cache</strong> entry from GUST's Settings sidebar. Tab caching and the Clear Cache / Reset Everything buttons will both be hidden from Settings.",
                                            '取消勾选即从 GUST 设置侧边栏中移除 <strong>缓存</strong> 入口。标签页缓存和「清空缓存 / 全部重置」按钮都将从设置中隐藏。'),

    ('>Show Files &amp; Media in Settings Sidebar<',
                                            '>在设置侧边栏显示「文件与媒体」<'),
    ("Uncheck to remove the <strong>Files &amp; Media</strong> entry from GUST's Settings sidebar. Range requests, auto-download, and all inline viewer toggles (PDF, image, video, audio, text) will be hidden from Settings.",
                                            '取消勾选即从 GUST 设置侧边栏中移除 <strong>文件与媒体</strong> 入口。Range 请求、自动下载，以及所有内联查看器开关（PDF、图片、视频、音频、文本）都将从设置中隐藏。'),

    ('>Show Appearance in Settings Sidebar<', '>在设置侧边栏显示「外观」<'),
    ("Uncheck to remove the <strong>Appearance</strong> entry from GUST's Settings sidebar. Font size, panel width persistence, panel position, and fullscreen-on-launch will all be hidden from Settings.",
                                            '取消勾选即从 GUST 设置侧边栏中移除 <strong>外观</strong> 入口。字体大小、面板宽度记忆、面板位置以及启动时全屏都将从设置中隐藏。'),

    ('>Show Home Screen in Settings Sidebar<',
                                            '>在设置侧边栏显示「主页设置」<'),
    ("Uncheck to remove the <strong>Home Screen</strong> entry from GUST's Settings sidebar. The bookmarks bar toggle, wallpaper controls, and clock options will all be hidden from Settings.",
                                            '取消勾选即从 GUST 设置侧边栏中移除 <strong>主页设置</strong> 入口。书签栏开关、壁纸控制和时钟选项都将从设置中隐藏。'),

    ('>Show Shortcuts in Settings Sidebar<',  '>在设置侧边栏显示「快捷键」<'),
    ("Uncheck to remove the <strong>Shortcuts</strong> entry from GUST's Settings sidebar. The keyboard shortcuts enable/disable toggle and the full key binding list will be hidden from Settings.",
                                            '取消勾选即从 GUST 设置侧边栏中移除 <strong>快捷键</strong> 入口。键盘快捷键启用开关和完整的按键绑定列表都将从设置中隐藏。'),

    ('>Show Tutorial in Settings Sidebar<',   '>在设置侧边栏显示「教程」<'),
    ("Uncheck to remove the <strong>Tutorial</strong> entry from GUST's Settings sidebar. The tutorial overlay, auto-launch on first load, and the restart button in Settings will all be hidden.",
                                            '取消勾选即从 GUST 设置侧边栏中移除 <strong>教程</strong> 入口。教程浮层、首次加载时自动启动，以及设置中的重启按钮都将被隐藏。'),

    # ═══════════════════════════════════════════════════════════
    #  卡片头
    # ═══════════════════════════════════════════════════════════
    ('</i> Language',                       '</i> 语言'),
    ('</i> Context',                        '</i> 上下文'),   # 新增：AI Assistant 面板内的卡片头
    ('</i> WISP Server',                    '</i> WISP 服务器'),
    ('</i> Concurrent Requests',            '</i> 并发请求'),
    ('</i> WebRTC Blocking',                '</i> WebRTC 拦截'),
    ('</i> Smart Request Headers',          '</i> 智能请求头'),
    ('</i> Fallback Toggle',                '</i> 回退开关'),
    ('</i> Fallback WISP URL',              '</i> 回退 WISP 地址'),
    ('</i> Retry Policy',                   '</i> 重试策略'),
    ('</i> Error Triggers',                 '</i> 错误触发条件'),
    ('</i> Default Search Engine',          '</i> 默认搜索引擎'),
    ('</i> Custom Search Engine',           '</i> 自定义搜索引擎'),
    ('</i> Spellcheck <span class="broken-tag">[BROKEN]</span>',
                                            '</i> 拼写检查 <span class="broken-tag">[已损坏]</span>'),
    ('</i> Tab Favicons',                   '</i> 标签页图标'),
    ('</i> Privacy &amp; Blocking',         '</i> 隐私与拦截'),
    ('</i> User-Agent Spoofing',            '</i> User-Agent 伪装'),
    ('</i> Blocklist &amp; Filters',        '</i> 黑名单与过滤器'),
    ('</i> Tab Caching',                    '</i> 标签页缓存'),
    ('</i> Resource Cache',                 '</i> 资源缓存'),
    ('</i> Advanced Rendering',             '</i> 高级渲染'),
    ('</i> Media Range Requests',           '</i> 媒体范围请求'),
    ('</i> Unknown File Types',             '</i> 未知文件类型'),
    ('</i> PDF Viewer',                     '</i> PDF 查看器'),
    ('</i> Image Viewer',                   '</i> 图片查看器'),
    ('</i> Video Player',                   '</i> 视频播放器'),
    ('</i> Audio Player',                   '</i> 音频播放器'),
    ('</i> Text / Code Viewer',             '</i> 文本 / 代码查看器'),
    ('</i> Font Size',                      '</i> 字体大小'),
    ('</i> Panel Widths',                   '</i> 面板宽度'),
    ('</i> Panel Position',                 '</i> 面板位置'),
    ('</i> Fullscreen on Launch',           '</i> 启动时全屏'),
    ('</i> Bookmarks Bar',                  '</i> 书签栏'),
    ('</i> New Tab Wallpaper',              '</i> 新标签页壁纸'),
    ('</i> Home Page Clock',                '</i> 主页时钟'),
    ('</i> Keyboard Shortcuts',             '</i> 键盘快捷键'),
    ('</i> Interactive Tutorial',           '</i> 交互式教程'),
    ('</i> Tab System',                     '</i> 标签页系统'),
    ('</i> Ad Blocker',                     '</i> 广告拦截'),
    ('</i> Browser Logs',                   '</i> 浏览器日志'),
    ('</i> Page Inspector',                 '</i> 页面检查器'),
    ('</i> Browser Metrics',                '</i> 浏览器指标'),

    # ═══════════════════════════════════════════════════════════
    #  patch-row 标签
    # ═══════════════════════════════════════════════════════════
    ('>Preferred language picker<',         '>首选语言选择器<'),
    # ── 新增：AI Assistant 面板内的 patch-row ──
    ('>Page context by default<',           '>默认使用页面上下文<'),
    ('>WebSocket URL input<',               '>WebSocket 地址输入框<'),
    ('>Idle &amp; active thread steppers<', '>空闲与活跃线程步进器<'),
    ('>Block WebRTC connections<',          '>拦截 WebRTC 连接<'),
    ('>Spoof Sec-Fetch &amp; Referer headers<', '>伪造 Sec-Fetch 与 Referer 请求头<'),
    ('>Enable fallback WISP switch<',       '>启用回退 WISP 开关<'),
    ('>Fallback server URL input<',         '>回退服务器地址输入框<'),
    ('>Main &amp; fallback retry counters + delay<', '>主服务器与回退重试次数 + 延迟<'),
    ('>5xx / timeout / DNS trigger toggles<','>5xx / 超时 / DNS 触发开关<'),
    ('>Search engine picker<',              '>搜索引擎选择器<'),
    ('>Custom search engine card<',         '>自定义搜索引擎卡片<'),
    ('>Enable spellcheck <span class="broken-tag">broken</span><',
                                            '>启用拼写检查 <span class="broken-tag">已损坏</span><'),
    ('>Proxy favicons through WISP<',       '>通过 WISP 代理网站图标<'),
    ('>Ad &amp; Tracker Blocking toggle<',  '>广告与跟踪器拦截开关<'),
    ('>"Pause for this site" button<',      '>"对此网站暂停" 按钮<'),
    ('>Paused sites allowlist<',            '>暂停站点白名单<'),
    ('>Request User-Agent field<',          '>请求 User-Agent 字段<'),
    ('>Page navigator.userAgent field<',    '>页面 navigator.userAgent 字段<'),
    ('>Custom Filter Rules textarea<',      '>自定义过滤规则文本框<'),
    ('>Keep tabs loaded in background<',    '>在后台保持标签页加载<'),
    ('>Clear Cache &amp; Reset All buttons<','>清空缓存与全部重置按钮<'),
    ('>Script &amp; image render limits<',  '>脚本与图片渲染上限<'),
    ('>Enable Range request support<',      '>启用 Range 请求支持<'),
    ('>Auto-download unknown files<',       '>自动下载未知文件<'),
    ('>Built-in PDF viewer<',               '>内置 PDF 查看器<'),
    ('>Built-in image viewer<',             '>内置图片查看器<'),
    ('>Built-in video player<',             '>内置视频播放器<'),
    ('>Built-in audio player<',             '>内置音频播放器<'),
    ('>Built-in text viewer<',              '>内置文本查看器<'),
    ('>Font size slider<',                  '>字体大小滑块<'),
    ('>Remember panel widths<',             '>记住面板宽度<'),
    ('>Panels on the left<',                '>面板位于左侧<'),
    ('>Start in fullscreen<',               '>启动进入全屏<'),
    ('>Show Bookmarks Bar<',                '>显示书签栏<'),
    ('>Background image controls<',         '>背景图片控制<'),
    ('>Show clock on new tab<',             '>在新标签页显示时钟<'),
    ('>24-hour clock<',                     '>24 小时制<'),
    ('>Enable shortcuts toggle + shortcut list<', '>启用快捷键开关 + 快捷键列表<'),
    ('>Include tutorial overlay &amp; steps<','>包含教程浮层与步骤<'),
    ('>Auto-start on first load<',          '>首次加载时自动启动<'),
    ('>Tutorial nav entry in Settings<',    '>设置中的教程导航项<'),
    ('>Drag-to-reorder tabs<',              '>拖拽重新排序标签页<'),
    ('>Right-click context menu on tabs<',  '>标签页右键菜单<'),
    ('>Audio mute controls on tabs<',       '>标签页音频静音控制<'),
    ('>Adblock shield toolbar button &amp; panel<', '>广告拦截盾牌工具栏按钮与面板<'),
    ('>Log panel &amp; toolbar toggle button<', '>日志面板与工具栏切换按钮<'),
    ('>Element inspector panel &amp; toolbar button<', '>元素检查器面板与工具栏按钮<'),
    ('>Metrics modal &amp; toolbar button<','>指标弹窗与工具栏按钮<'),

    # ═══════════════════════════════════════════════════════════
    #  patch-row 描述
    # ═══════════════════════════════════════════════════════════
    ('Removes the language selector from Settings.',
                                            '从设置中移除语言选择器。'),

    # ── 新增：AI Assistant 的 patch-row 描述 ──
    ('<strong>Uncheck to disable</strong> the "Page Context by default" setting and remove its toggle from Settings › AI Assistant. The assistant will never automatically receive the current page\'s content when opened.',
                                            '<strong>取消勾选即禁用</strong>「默认使用页面上下文」设置，并从设置 › AI 助手中移除其开关。助手打开时将不再自动接收当前页面的内容。'),

    ('<strong>Uncheck to remove</strong> the WISP server URL input from Settings. The default server (wss://wisp.mercurywork.shop/) will always be used with no way to change it at runtime.',
                                            '<strong>取消勾选即移除</strong> 设置中的 WISP 服务器地址输入框。将始终使用默认服务器（wss://wisp.mercurywork.shop/），运行时无法更改。'),
    ('<strong>Uncheck to remove</strong> the thread count controls and retry counters from Settings. Defaults (idle: 3, active: 6, retries: 3) will be locked in permanently.',
                                            '<strong>取消勾选即移除</strong> 设置中的线程数控制和重试计数器。默认值（空闲：3、活跃：6、重试：3）将被永久锁定。'),
    ('<strong>Uncheck to disable</strong> WebRTC blocking and remove its toggle from Settings. P2P connections will be able to bypass the WISP proxy and may leak the real IP.',
                                            '<strong>取消勾选即禁用</strong> WebRTC 拦截并移除设置中的开关。P2P 连接将可以绕过 WISP 代理，可能泄露真实 IP。'),
    ('<strong>Uncheck to disable</strong> smart header spoofing and remove its toggle from Settings. Some CDNs may reject requests with missing or incorrect fetch metadata headers.',
                                            '<strong>取消勾选即禁用</strong> 智能请求头伪装并移除设置中的开关。部分 CDN 可能会拒绝缺失或错误的 fetch 元数据请求。'),
    ('<strong>Uncheck to permanently disable</strong> the entire fallback system and remove its toggle from Settings. If the primary WISP fails, GUST will show an error immediately with no retry or fallback attempt.',
                                            '<strong>取消勾选即永久禁用</strong> 整个回退系统并移除设置中的开关。如果主 WISP 失败，GUST 将立即显示错误，不进行任何重试或回退尝试。'),
    ('<strong>Uncheck to remove</strong> the fallback WISP URL input, save, and reset buttons from Settings. No fallback server can be configured at runtime — only useful if the fallback toggle is kept enabled.',
                                            '<strong>取消勾选即移除</strong> 设置中的回退 WISP 地址输入框、保存和重置按钮。运行时无法配置回退服务器——仅在保留回退开关启用时有用。'),
    ('<strong>Uncheck to remove</strong> the main retry attempts, fallback retry attempts, and retry delay steppers from Settings. Defaults (3 main retries, 3 fallback retries, 3s delay) will be locked in permanently.',
                                            '<strong>取消勾选即移除</strong> 设置中的主服务器重试次数、回退重试次数和重试延迟步进器。默认值（主服务器 3 次重试、回退 3 次重试、3 秒延迟）将被永久锁定。'),
    ('<strong>Uncheck to remove</strong> the error trigger switches from Settings. Fallback will trigger on all generic connection errors by default (5xx and timeout triggers default on, DNS trigger default off).',
                                            '<strong>取消勾选即移除</strong> 设置中的错误触发开关。默认情况下，回退会在所有通用连接错误时触发（5xx 和超时触发器默认开启，DNS 触发器默认关闭）。'),
    ('<strong>Uncheck to remove</strong> the search engine selector from Settings. Brave Search will be locked in as the default with no way to change it.',
                                            '<strong>取消勾选即移除</strong> 设置中的搜索引擎选择器。Brave 搜索将被锁定为默认，无法更改。'),
    ("<strong>Uncheck to remove</strong> the custom search engine config card from Settings. The <strong>Custom</strong> option will still appear in the engine picker but its name/URL card will be hidden.",
                                            '<strong>取消勾选即移除</strong> 设置中的自定义搜索引擎配置卡片。<strong>自定义</strong> 选项仍会出现在引擎选择器中，但其名称/网址卡片将被隐藏。'),
    ("<strong>Uncheck to remove</strong> the spellcheck toggle from Settings. Only affects GUST's own UI inputs — spellcheck inside proxied pages cannot be controlled and remains non-functional.",
                                            '<strong>取消勾选即移除</strong> 设置中的拼写检查开关。仅影响 GUST 自身的界面输入框——代理页面内的拼写检查无法控制，且一直处于失效状态。'),
    ("<strong>Uncheck to disable</strong> favicon proxying through WISP and remove its toggle from Settings. Google's favicon service will be used instead — favicons may not load on some networks.",
                                            '<strong>取消勾选即禁用</strong> 通过 WISP 代理网站图标，并移除设置中的开关。将改用 Google 的图标服务——在某些网络环境下图标可能无法加载。'),
    ('<strong>Uncheck to permanently disable</strong> ad/tracker blocking and remove its toggle from Settings and the toolbar. Cannot be re-enabled at runtime.',
                                            '<strong>取消勾选即永久禁用</strong> 广告/跟踪器拦截，并从设置和工具栏中移除其开关。运行时无法重新启用。'),
    ('<strong>Uncheck to remove</strong> the per-site pause button from the adblock toolbar popup. Users will only be able to globally disable ad blocking, not pause it per-site.',
                                            '<strong>取消勾选即移除</strong> 广告拦截工具栏弹窗中的按站点暂停按钮。用户将只能全局禁用广告拦截，而不能按站点暂停。'),
    ('<strong>Uncheck to remove</strong> the paused-sites textarea from Settings › Privacy. Sites cannot be individually allowlisted from the Settings page — only via the toolbar popup button (if kept above).',
                                            '<strong>取消勾选即移除</strong> 设置 › 隐私中的暂停站点文本框。无法从设置页面单独加入白名单——只能通过工具栏弹窗按钮（如果保留了上面的选项）。'),
    ("<strong>Uncheck to remove</strong> the request UA input from Settings. The browser's native User-Agent will be sent on all proxy requests.",
                                            '<strong>取消勾选即移除</strong> 设置中的请求 UA 输入框。所有代理请求将发送浏览器原生的 User-Agent。'),
    ('<strong>Uncheck to remove</strong> the page UA input from Settings. The real browser value will be exposed to pages via navigator.userAgent.',
                                            '<strong>取消勾选即移除</strong> 设置中的页面 UA 输入框。真实浏览器值将通过 navigator.userAgent 暴露给页面。'),
    ('<strong>Uncheck to remove</strong> the custom CSS filter textarea from Settings. Per-page hide rules cannot be added or edited at runtime.',
                                            '<strong>取消勾选即移除</strong> 设置中的自定义 CSS 过滤文本框。运行时无法添加或编辑按页面隐藏规则。'),
    ('<strong>Uncheck to permanently disable</strong> tab caching and remove its toggle from Settings. Background tabs will always be fully reloaded when switched to.',
                                            '<strong>取消勾选即永久禁用</strong> 标签页缓存并移除设置中的开关。切换到后台标签页时将始终重新完整加载。'),
    ('<strong>Uncheck to remove</strong> the Clear Cache and Reset Everything buttons from Settings. Cached data can only be cleared by wiping browser storage manually.',
                                            '<strong>取消勾选即移除</strong> 设置中的「清空缓存」和「全部重置」按钮。缓存数据只能通过手动清除浏览器存储来清除。'),
    ('<strong>Uncheck to remove</strong> the script tag limit and image prefetch limit steppers from Settings. Defaults (250 scripts, 300 images) will be locked in permanently.',
                                            '<strong>取消勾选即移除</strong> 设置中的脚本标签上限和图片预取上限步进器。默认值（250 个脚本、300 张图片）将被永久锁定。'),
    ('<strong>Uncheck to disable</strong> Range requests and remove their toggle from Settings. Seeking in video and audio will not work.',
                                            '<strong>取消勾选即禁用</strong> Range 请求并移除设置中的开关。视频和音频的拖动定位将不可用。'),
    ('<strong>Uncheck to disable</strong> auto-downloading of unknown MIME types and remove the toggle from Settings. Unknown file types will fail silently instead of downloading.',
                                            '<strong>取消勾选即禁用</strong> 未知 MIME 类型文件的自动下载，并移除设置中的开关。未知文件类型将静默失败而不是下载。'),
    ('<strong>Uncheck to disable</strong> the PDF viewer and remove its toggle from Settings. PDF files will be downloaded instead of opening inline.',
                                            '<strong>取消勾选即禁用</strong> PDF 查看器并移除设置中的开关。PDF 文件将被下载而不是内联打开。'),
    ('<strong>Uncheck to disable</strong> the image viewer and remove its toggle from Settings. Images will open as raw files or download rather than rendering inline.',
                                            '<strong>取消勾选即禁用</strong> 图片查看器并移除设置中的开关。图片将作为原始文件打开或下载，而不是内联渲染。'),
    ('<strong>Uncheck to disable</strong> the video player and remove its toggle from Settings. Video files will not play inline.',
                                            '<strong>取消勾选即禁用</strong> 视频播放器并移除设置中的开关。视频文件将无法内联播放。'),
    ('<strong>Uncheck to disable</strong> the audio player and remove its toggle from Settings. Audio files will not play inline.',
                                            '<strong>取消勾选即禁用</strong> 音频播放器并移除设置中的开关。音频文件将无法内联播放。'),
    ('<strong>Uncheck to disable</strong> the text/code viewer and remove its toggle from Settings. Plain text and code files will be downloaded instead of rendering.',
                                            '<strong>取消勾选即禁用</strong> 文本/代码查看器并移除设置中的开关。纯文本和代码文件将被下载而不是渲染。'),
    ('<strong>Uncheck to remove</strong> the font size slider from Settings. UI text size will be locked at the default with no way to adjust it.',
                                            '<strong>取消勾选即移除</strong> 设置中的字体大小滑块。界面文字大小将锁定为默认值，无法调整。'),
    ('<strong>Uncheck to disable</strong> panel width persistence and remove its toggle from Settings. Panels will reset to default width on every load.',
                                            '<strong>取消勾选即禁用</strong> 面板宽度记忆并移除设置中的开关。面板将在每次加载时重置为默认宽度。'),
    ('<strong>Uncheck to disable</strong> the left-panels option and remove its toggle from Settings. Panels will always be on the right.',
                                            '<strong>取消勾选即禁用</strong> 左侧面板选项并移除设置中的开关。面板将始终位于右侧。'),
    ('<strong>Uncheck to disable</strong> auto-fullscreen on launch and remove its toggle from Settings. GUST will always open in a normal window.',
                                            '<strong>取消勾选即禁用</strong> 启动时自动全屏并移除设置中的开关。GUST 将始终以普通窗口打开。'),
    ('<strong>Uncheck to disable</strong> the bookmarks bar and remove its toggle from Settings. Bookmarks will only be accessible via the history panel.',
                                            '<strong>取消勾选即禁用</strong> 书签栏并移除设置中的开关。书签将只能通过历史记录面板访问。'),
    ('<strong>Uncheck to remove</strong> the wallpaper change and reset buttons from Settings. The new tab background will be locked to the default gradient.',
                                            '<strong>取消勾选即移除</strong> 设置中的壁纸更改和重置按钮。新标签页背景将锁定为默认渐变。'),
    ('<strong>Uncheck to permanently hide</strong> the clock on the new tab page and remove its toggle from Settings.',
                                            '<strong>取消勾选即永久隐藏</strong> 新标签页上的时钟并移除设置中的开关。'),
    ('<strong>Uncheck to disable</strong> 24-hour format and remove its toggle from Settings. The clock will always display in 12-hour format.',
                                            '<strong>取消勾选即禁用</strong> 24 小时制并移除设置中的开关。时钟将始终以 12 小时制显示。'),
    ('<strong>Uncheck to permanently disable</strong> keyboard shortcuts and remove the enable/disable toggle and key binding list from Settings.',
                                            '<strong>取消勾选即永久禁用</strong> 键盘快捷键，并从设置中移除启用/禁用开关和按键绑定列表。'),
    ('<strong>Uncheck to remove</strong> the guided tour overlay entirely and pre-mark it as done so it never appears. When unchecked, the two options below are also forced off.',
                                            '<strong>取消勾选即完全移除</strong> 引导教程浮层，并预先标记为已完成，使其永不出现。取消勾选时，下面两个选项也会被强制关闭。'),
    ('<strong>Uncheck to suppress</strong> the tutorial auto-launch on first open by pre-seeding the done flag. The overlay is still present if triggered manually from Settings.',
                                            '<strong>取消勾选即抑制</strong> 首次打开时自动启动教程（通过预置完成标记）。如果从设置中手动触发，浮层仍然存在。'),
    ('<strong>Uncheck to remove</strong> the Tutorial nav item from the Settings sidebar so users cannot manually re-launch the tour.',
                                            '<strong>取消勾选即移除</strong> 设置侧边栏中的「教程」导航项，用户将无法手动重新启动教程。'),
    ('<strong>Uncheck to disable</strong> tab dragging by blocking the pointer events that drive it. Tabs cannot be grabbed or reordered — no ghost, no slot indicator, no reorder.',
                                            '<strong>取消勾选即禁用</strong> 标签页拖拽（通过拦截驱动拖拽的指针事件）。标签页将无法抓取或重新排序——没有拖拽幽灵、没有占位指示器、无法排序。'),
    ('<strong>Uncheck to remove</strong> the tab context menu element. Right-clicking a tab will do nothing.',
                                            '<strong>取消勾选即移除</strong> 标签页右键菜单。右键点击标签页将无任何反应。'),
    ('<strong>Uncheck to hide</strong> the mute icon on tabs that are playing audio. Audio will still play — it just cannot be muted from the tab strip.',
                                            '<strong>取消勾选即隐藏</strong> 正在播放音频的标签页上的静音图标。音频仍会播放——只是无法从标签栏静音。'),
    ('<strong>Uncheck to remove</strong> the shield toolbar button and the floating adblock modal that shows per-page block counts and the on/off power button.',
                                            '<strong>取消勾选即移除</strong> 盾牌工具栏按钮和浮动广告拦截弹窗（显示每页拦截计数和开关电源按钮）。'),
    ('<strong>Uncheck to hide</strong> the logs toolbar button and the log panel. Real-time request logging will be completely unavailable to the user.',
                                            '<strong>取消勾选即隐藏</strong> 日志工具栏按钮和日志面板。用户将完全无法使用实时请求日志。'),
    ('<strong>Uncheck to hide</strong> the inspector toolbar button and the elements panel. DOM and CSS inspection will be completely unavailable to the user.',
                                            '<strong>取消勾选即隐藏</strong> 检查器工具栏按钮和元素面板。用户将完全无法进行 DOM 和 CSS 检查。'),
    ('<strong>Uncheck to hide</strong> the metrics toolbar button and the stats popup. Live performance and network data will be completely unavailable to the user.',
                                            '<strong>取消勾选即隐藏</strong> 指标工具栏按钮和统计弹窗。用户将完全无法查看实时性能和网络数据。'),

    # ═══════════════════════════════════════════════════════════
    #  状态栏
    # ═══════════════════════════════════════════════════════════
    ('>Loading source…<',                   '>正在加载源码…<'),
    ('>Enabled:<',                          '>已启用：<'),
    ('>Patches removed:<',                  '>已移除补丁：<'),
    ('>File size:<',                        '>文件大小：<'),

    # ═══════════════════════════════════════════════════════════
    #  教程按钮
    # ═══════════════════════════════════════════════════════════
    ('>Skip tour<',                         '>跳过导览<'),
    ('>Back<',                              '>上一步<'),
    ('>Next<',                              '>下一步<'),
    ('>Done<',                              '>完成<'),
    ("'Next <i class=\"fas fa-arrow-right\" style=\"margin-left:5px;\"></i>'",
                                            "'下一步 <i class=\"fas fa-arrow-right\" style=\"margin-left:5px;\"></i>'"),
    ("'<i class=\"fas fa-check\" style=\"margin-right:5px;\"></i>Done'",
                                            "'<i class=\"fas fa-check\" style=\"margin-right:5px;\"></i>完成'"),

    # ═══════════════════════════════════════════════════════════
    #  教程弹窗
    # ═══════════════════════════════════════════════════════════
    ("title: 'Welcome to GUST Patcher'",    "title: '欢迎使用 GUST 定制器'"),
    ("body: 'Build a custom version of GUST with only the features you want. This quick tour covers all the key controls.'",
                                            "body: '构建只包含你所需功能的 GUST 定制版。本快速导览涵盖所有关键控件。'"),
    ("title: 'Feature Sidebar'",            "title: '功能侧边栏'"),
    ("body: 'Browse all patchable features by category — Connection, Search, Privacy, Cache, and more. Click any category to see its patches.'",
                                            "body: '按分类浏览所有可定制的功能——连接、搜索、隐私、缓存等。点击任意分类查看其补丁。'"),
    ("title: 'Refresh Source'",             "title: '刷新源码'"),
    ("body: 'Fetches the latest GUST source from GitHub. Also resets all checkboxes back to the default base GUST configuration.'",
                                            "body: '从 GitHub 获取最新的 GUST 源码。同时将所有复选框重置为基础 GUST 的默认配置。'"),
    ("title: 'Paste Source'",               "title: '粘贴源码'"),
    ("body: 'Can\\'t fetch automatically? Paste the raw GUST HTML here manually. Download it from GitHub and paste the whole file in.'",
                                            "body: '无法自动获取？在此手动粘贴原始的 GUST HTML。从 GitHub 下载后将整个文件粘贴进来。'"),
    ("title: 'GUST on GitHub'",             "title: 'GitHub 上的 GUST'"),
    ("body: \"GUST is fully open source, and you can view GUST's full source code, report issues, or download GUST directly from the GitHub repository. If you like this project, please leave a star on the repository!\"",
                                            "body: 'GUST 完全开源，你可以查看完整源代码、反馈问题，或直接从 GitHub 仓库下载 GUST。如果你喜欢这个项目，请在仓库上点个星！'"),
    ("title: 'Download GUST'",              "title: '下载 GUST'"),
    ("body: 'Once the source is loaded, click here to build and download your custom patched GUST. You must uncheck at least one patch to enable this button — if you want the unmodified build, use the <strong>Base GUST</strong> card on the home screen instead.'",
                                            "body: '源码加载完成后，点击此处构建并下载你的自定义 GUST。必须至少取消勾选一个补丁才能启用此按钮——如果你想要未修改的构建，请使用主页上的 <strong>基础版 GUST</strong> 卡片。'"),
    ("title: 'Quick Presets'",              "title: '快速预设'"),
    ("body: 'Need a fast start? Grab <strong>Base GUST</strong> straight from GitHub, or <strong>GUST Lite</strong> — a trimmed build with bloat already removed.'",
                                            "body: '需要快速开始？直接获取来自 GitHub 的 <strong>基础版 GUST</strong>，或 <strong>GUST Lite</strong>——已经移除了冗余功能的精简构建。'"),
    ("title: 'Default selections = base GUST'", "title: '默认选择 = 基础版 GUST'"),
    ("body: 'All currently checked patches represent the default base GUST build. Uncheck anything you want to remove before downloading.'",
                                            "body: '当前所有已勾选的补丁代表默认的基础版 GUST 构建。下载前取消勾选你想移除的任何项。'"),

    # ═══════════════════════════════════════════════════════════
    #  JS 状态消息
    # ═══════════════════════════════════════════════════════════
    ("'Source not loaded yet.'",            "'源码尚未加载。'"),
    ("'Please apply a patch'",              "'请应用至少一个补丁'"),
    ("'Connecting...'",                     "'正在连接...'"),
    ("'Fetching from GitHub Raw...'",       "'正在从 GitHub Raw 获取...'"),
    ("'Fetching via jsDelivr CDN...'",      "'正在通过 jsDelivr CDN 获取...'"),
    ("'Fetching via codetabs proxy...'",    "'正在通过 codetabs 代理获取...'"),
    ("'Fetching via allorigins...'",        "'正在通过 allorigins 获取...'"),
    ("'Fetching via gh-proxy proxy...'",    "'正在通过 gh-proxy 代理获取...'"),
    ("'Source loaded -- '",                 "'源码已加载 -- '"),
    ("'All fetch attempts failed -- open DevTools (F12) for details.'",
                                            "'所有获取尝试均失败 -- 打开开发者工具 (F12) 查看详情。'"),
    ("'Could not load GUST source'",        "'无法加载 GUST 源码'"),
    ("'Pasted content does not look like valid GUST source — check you copied the full file.'",
                                            "'粘贴的内容看起来不是有效的 GUST 源码——请检查是否复制了完整文件。'"),
    ("'Source loaded from paste — '",       "'源码已从粘贴内容加载 — '"),
    ("'This does not look like valid GUST source — make sure you copied the complete index.html file.'",
                                            "'这看起来不是有效的 GUST 源码——请确认你复制了完整的 index.html 文件。'"),
    ("'Building patched GUST...'",          "'正在构建定制版 GUST...'"),
    ("'Downloaded GUST-Patched.html - '",   "'已下载 GUST-Patched.html - '"),
    ("'removed by patcher'",                "'已被定制器移除'"),
    ("'broken'",                            "'已损坏'"),

    # ═══════════════════════════════════════════════════════════
    #  Paste 弹窗
    # ═══════════════════════════════════════════════════════════
    ('>Paste GUST Source<',                 '>粘贴 GUST 源码<'),
    ('Download <code style="background:var(--bg3);padding:1px 5px;border-radius:4px;">index.html</code> from <a href="https://github.com/nautilus-os/GUST" target="_blank" style="color:var(--ac)">github.com/nautilus-os/GUST</a> then paste the full file contents below.',
     '从 <a href="https://github.com/cjhdevact/GUST-Chinese" target="_blank" style="color:var(--ac)">github.com/cjhdevact/GUST-Chinese</a> 下载 <code style="background:var(--bg3);padding:1px 5px;border-radius:4px;">index.html</code>，然后将完整的文件内容粘贴到下方。'),
    ('placeholder="Paste the full GUST HTML here…"',
                                            'placeholder="在此粘贴完整的 GUST HTML…"'),
    ('>Cancel<',                            '>取消<'),
    ('</i> Load Source<',                   '</i> 加载源码<'),
    ('> Load Source<',                      '> 加载源码<'),
    ('> Use Pasted Source<',                '> 使用粘贴的源码<'),
    ('> Use Pasted Source',                 '> 使用粘贴的源码'),

    # ═══════════════════════════════════════════════════════════
    #  错误提示框
    # ═══════════════════════════════════════════════════════════
    ('>All fetch attempts failed (likely a network/CORS restriction).<',
                                            '>所有获取尝试均失败（可能是网络/CORS 限制）。<'),
    ('>Or paste the GUST source manually below:<',
                                            '>或在下方手动粘贴 GUST 源码：<'),
    ("placeholder=\"Paste the full GUST HTML here (download from github.com/nautilus-os/GUST)…\"",
                                            "placeholder=\"在此粘贴完整的 GUST HTML（从 GitHub 下载）…\""),
                                            
    # ═══════════════════════════════════════════════════════════
    #  侧边栏分区标签（补充）
    # ═══════════════════════════════════════════════════════════
    ('<div class="sidebar-core-label">Settings</div>',
     '<div class="sidebar-core-label">设置</div>'),

])


# ═══════════════════════════════════════════════════════════════════
#  GitHub 显示 URL 替换（可选）
# ═══════════════════════════════════════════════════════════════════
if REPLACE_GITHUB_URL:
    REPLACEMENTS.update(OrderedDict([
        ("'https://github.com/nautilus-os/GUST'",   f"'{GITHUB_REPO_URL}'"),
        ('"https://github.com/nautilus-os/GUST"',   f'"{GITHUB_REPO_URL}"'),
        ('>github.com/nautilus-os/GUST<',           f'>{GITHUB_DISPLAY}<'),
    ]))


# ═══════════════════════════════════════════════════════════════════
#  "Made with ... by Nautilus Labs" 移除规则
# ═══════════════════════════════════════════════════════════════════
MADE_WITH_PATTERNS = [
    re.compile(
        r'<div\s+style="[^"]*top:3px;"[^>]*>\s*Made with\s+<i[^>]*>\s*</i>\s*by\s+'
        r'<strong[^>]*>\s*Nautilus Labs\s*</strong>\s*</div>',
        re.DOTALL
    ),
]


# ═══════════════════════════════════════════════════════════════════
#  源码获取渠道常量
# ═══════════════════════════════════════════════════════════════════
NEW_ATTEMPTS = (
    "const attempts = [\n"
    "    {label:'正在从 GitHub Raw 获取...',       url: RAW_URL,  opts: {headers:{'Accept':'text/html,application/xhtml+xml'}}},\n"
    "    {label:'正在通过 gh-proxy 代理获取...',     url: 'https://gh-proxy.com/' + RAW_URL, opts:{}},\n"
    "  ];"
)


# ═══════════════════════════════════════════════════════════════════
#  工具函数
# ═══════════════════════════════════════════════════════════════════

def key_to_pattern(key: str) -> str:
    """把 key 里的空白转成 \\s+，让换行和多个空格也能匹配"""
    parts = []
    last_ws = False
    for ch in key:
        if ch.isspace():
            if not last_ws:
                parts.append(r'\s+')
                last_ws = True
        else:
            parts.append(re.escape(ch))
            last_ws = False
    return ''.join(parts)


def normalize_ws(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip()


def build_pattern(replacements):
    patterns = [key_to_pattern(k)
                for k in sorted(replacements.keys(), key=len, reverse=True)]
    return re.compile("|".join(patterns))


def localize(text: str, replacements, pattern, counts: dict) -> str:
    norm_map = {normalize_ws(k): v for k, v in replacements.items()}

    def _repl(m):
        matched = m.group(0)
        key = normalize_ws(matched)
        if key in norm_map:
            counts[key] = counts.get(key, 0) + 1
            return norm_map[key]
        return matched

    return pattern.sub(_repl, text)


def strip_made_with(html: str, counts: dict) -> str:
    total = 0
    for pat in MADE_WITH_PATTERNS:
        html, n = pat.subn('', html)
        total += n
    if total:
        counts['__made_with__'] = total
    return html


def rewrite_source_urls(html: str, counts: dict) -> str:
    """修改 Patcher 拉取 GUST 源码的 URL 与获取渠道。"""
    n_raw = n_gh = n_att = n_hard = 0

    html, n1 = re.subn(
        r"const\s+RAW_URL\s*=\s*'[^']*';",
        f"const RAW_URL = '{SOURCE_RAW_URL}';",
        html, count=1
    )
    n_raw += n1

    html, n2 = re.subn(
        r"const\s+GH_URL\s*=\s*'[^']*';",
        f"const GH_URL  = '{SOURCE_GH_URL}';",
        html, count=1
    )
    n_gh += n2

    html, n3 = re.subn(
        r"const\s+attempts\s*=\s*\[[\s\S]*?\n\s*\];",
        NEW_ATTEMPTS,
        html, count=1
    )
    n_att += n3

    html, n4 = re.subn(
        r"fetch\('https://cdn\.jsdelivr\.net/gh/nautilus-os/GUST@main/index\.html',\s*\{cache:'no-store'\}\)",
        "fetch(RAW_URL, {cache:'no-store'})",
        html, count=1
    )
    n_hard += n4

    html, n5 = re.subn(
        r"window\.open\('https://github\.com/nautilus-os/GUST/raw/refs/heads/main/index\.html','_blank'\)",
        "window.open(GH_URL,'_blank')",
        html, count=1
    )
    n_hard += n5

    if n_raw:  counts['__raw_url__']  = n_raw
    if n_gh:   counts['__gh_url__']   = n_gh
    if n_att:  counts['__attempts__'] = n_att
    if n_hard: counts['__hardcoded_url__'] = n_hard
    return html


def inject_translator_credit(html: str, counts: dict) -> str:
    """在首页 tagline 下方注入一行署名。"""
    translator_name = 'GUST-Chinese'
    translator_url  = GITHUB_REPO_URL

    if translator_name in html and '实现翻译' in html:
        return html

    line = (
        f'由 <a href="{translator_url}" target="_blank" rel="noopener noreferrer" '
        f'style="color:var(--ac);text-decoration:none;">{translator_name}</a> 实现翻译'
    )

    pattern = re.compile(
        r'(<div class="homepage-tagline">[^<]*</div>)',
        re.DOTALL
    )

    def _repl(m):
        counts['__translator__'] = counts.get('__translator__', 0) + 1
        block = (
            m.group(1)
            + '\n    <div style="font-size:12px;color:var(--tx3);'
            + 'margin-top:12px;text-align:center;">'
            + line
            + '</div>'
        )
        return block

    return pattern.sub(_repl, html, count=1)


# ═══════════════════════════════════════════════════════════════════
#  主流程
# ═══════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="GUST Patcher 界面汉化工具（新版）")
    ap.add_argument("input", help="输入 HTML 文件（GUST-Patcher.html）")
    ap.add_argument("-o", "--output", help="输出文件（默认覆盖输入并备份 .bak）")
    ap.add_argument("--dry-run", action="store_true", help="仅显示替换统计，不写文件")
    ap.add_argument("--keep-made-with", action="store_true",
                    help='保留标题栏 "Made with ❤ by Nautilus Labs"')
    ap.add_argument("--keep-github-url", action="store_true",
                    help="保留原 GitHub URL（不替换为 fork）")
    ap.add_argument("--no-credit", action="store_true",
                    help="不注入翻译者信息")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.is_file():
        print(f"[ERROR] 找不到文件: {src}")
        sys.exit(1)

    text = src.read_text(encoding="utf-8")
    original_len = len(text)

    pattern = build_pattern(REPLACEMENTS)
    counts = {}
    result = localize(text, REPLACEMENTS, pattern, counts)

    result = rewrite_source_urls(result, counts)

    if REMOVE_MADE_WITH_CREDIT and not args.keep_made_with:
        result = strip_made_with(result, counts)

    if INJECT_TRANSLATOR_CREDIT and not args.no_credit:
        result = inject_translator_credit(result, counts)

    # ── 报告 ─────────────────────────────────
    print()
    print("=" * 78)
    print(f"  GUST Patcher 汉化报告  ({src.name})")
    print("=" * 78)

    total = 0
    hit, miss = 0, 0
    for old, new in REPLACEMENTS.items():
        key = normalize_ws(old)
        n = counts.get(key, 0)
        if n > 0:
            hit += 1
            total += n
            tag = "[OK]"
        else:
            miss += 1
            tag = "[--]"
        o = old if len(old) <= 44 else old[:41] + "..."
        n_ = new if len(new) <= 44 else new[:41] + "..."
        print(f"  {tag} {n:>3}x {o:<46} -> {n_}")

    for tag_key, label in [
        ('__raw_url__',        'const RAW_URL 已指向 cjhdevact/GUST-Chinese'),
        ('__gh_url__',         'const GH_URL 已指向 cjhdevact/GUST-Chinese'),
        ('__attempts__',       '获取渠道已精简为 GitHub Raw + gh-proxy'),
        ('__hardcoded_url__',  'downloadBaseGUST 硬编码 URL 已清理'),
        ('__made_with__',      '标题栏 Made with by Nautilus Labs 已移除'),
        ('__translator__',     '翻译者信息已注入首页 tagline 下方'),
    ]:
        v = counts.get(tag_key, 0)
        if v:
            total += v
            print(f"  [OK] {v:>3}x {label}")

    print("-" * 78)
    print(f"  命中规则 {hit} 条，共替换 {total} 处；未命中 {miss} 条")
    print(f"  文件大小: {original_len:,} -> {len(result):,} 字节")
    print("=" * 78)

    if args.dry_run:
        print("\n  [dry-run] 未写入任何文件\n")
        return

    if args.output:
        out = Path(args.output)
    else:
        backup = src.with_suffix(src.suffix + ".bak")
        if not backup.exists():
            backup.write_text(text, encoding="utf-8")
            print(f"\n  [备份] 已备份原文件 -> {backup.name}")
        else:
            print(f"\n  [备份] 备份已存在 -> {backup.name}（跳过）")
        out = src

    out.write_text(result, encoding="utf-8")
    print(f"  [完成] 已写入 -> {out.name}\n")


if __name__ == "__main__":
    main()