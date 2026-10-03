#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUST 浏览器界面汉化工具
https://github.com/cjhdevact/GUST-Chinese

适配提交：ec3493ca0cb592bfec661a19581af73aaccdaa1e

用法:
    python GUST-Chinese.py index.html                  # 原地替换，自动备份 .bak
    python GUST-Chinese.py index.html --dry-run        # 只预览，不写文件
    python GUST-Chinese.py index.html -o out.html      # 指定输出文件
    python GUST-Chinese.py index.html --keep-emoji     # 保留 emoji
    python GUST-Chinese.py index.html --keep-watermark # 保留主页水印
"""

import re
import sys
import argparse
from pathlib import Path
from collections import OrderedDict

# ═══════════════════════════════════════════════════════════════════
#  可配置项
# ═══════════════════════════════════════════════════════════════════
COMMIT_HASH     = 'ec3493ca0cb592bfec661a19581af73aaccdaa1e'

# ─────────────────────────────────────────────
#  搜索引擎开关
# ─────────────────────────────────────────────
ADD_BAIDU_ENGINE    = True   # True = 在搜索引擎下拉列表中增加百度选项
USE_BING_AS_DEFAULT = True   # True = 将默认搜索引擎改为必应（Bing）

# ═══════════════════════════════════════════════════════════════════
#  替换表
#  - 长 key 自动优先匹配，所以 'Fallback WISP Server' 不会被 'WISP Server' 抢
#  - key 里的空白会被灵活匹配（换行、多空格均可命中）
# ═══════════════════════════════════════════════════════════════════
REPLACEMENTS = OrderedDict([

    # ═══════════════════════════════════════════════════════════
    #  HTML title="..." 属性
    # ═══════════════════════════════════════════════════════════
    ('<title>GUST Browser</title>',         '<title>GUST 浏览器</title>'),
    ('title="Scroll tabs left"',            'title="向左滚动标签页"'),
    ('title="Scroll tabs right"',           'title="向右滚动标签页"'),
    ('title="New tab (Ctrl+T)"',            'title="新建标签页 (Ctrl+T)"'),
    ('title="Browser metrics"',             'title="浏览器指标"'),
    ('title="Toggle fullscreen (F11)"',     'title="切换全屏 (F11)"'),
    ('title="Exit fullscreen (F11)"',       'title="退出全屏 (F11)"'),
    ('title="Recent history (Alt+H)"',      'title="最近历史 (Alt+H)"'),
    ('title="Reload (Ctrl+R)"',             'title="刷新 (Ctrl+R)"'),
    ('title="Stop loading"',                'title="停止加载"'),
    ('title="Back"',                        'title="后退"'),
    ('title="Forward"',                     'title="前进"'),
    ('title="Home"',                        'title="主页"'),
    ('title="Search or enter address"',     'title="搜索或输入网址"'),
    ('title="Bookmark (Ctrl+D)"',           'title="收藏 (Ctrl+D)"'),
    ('title="Bookmark this page (Alt+D)"',  'title="收藏此页 (Alt+D)"'),
    ('title="Remove bookmark (Alt+D)"',     'title="移除收藏 (Alt+D)"'),
    ('title="Go"',                          'title="前往"'),
    ('title="Show bookmarks bar"',          'title="显示书签栏"'),
    ('title="Hide bookmarks bar"',          'title="隐藏书签栏"'),
    ('title="Settings"',                    'title="设置"'),
    ('title="Toggle logs (Ctrl+Shift+I)"',  'title="切换日志 (Ctrl+Shift+I)"'),
    ('title="Toggle elements inspector"',   'title="切换元素检查器"'),
    ('title="Toggle ad/tracker blocking"',  'title="切换广告/跟踪器拦截"'),
    ('title="Copy logs"',                   'title="复制日志"'),
    ('title="Clear logs"',                  'title="清空日志"'),
    ('title="Toggle auto-scroll"',          'title="切换自动滚动"'),
    ('title="Auto-scroll on"',              'title="自动滚动已开"'),
    ('title="Auto-scroll off"',             'title="自动滚动已关"'),
    ('title="Refresh elements"',            'title="刷新元素"'),
    ('title="Toggle details panel"',        'title="切换详情面板"'),
    ('title="Change background"',           'title="更改背景"'),
    ('title="Change wallpaper"',            'title="更改壁纸"'),
    ('title="Reset to default gradient"',   'title="重置为默认渐变"'),
    ('title="View on GitHub"',              'title="在 GitHub 上查看"'),
    ('title="Reset to default"',            'title="重置为默认"'),
    ('title="Reset to defaults"',           'title="重置为默认值"'),
    ('title="Reset shortcut"',              'title="重置快捷键"'),
    ('title="Edit shortcut"',               'title="编辑快捷键"'),
    ('title="Remove bookmark"',             'title="移除书签"'),
    ('title="Remove favorite"',             'title="移除收藏"'),
    ('title="Save"',                        'title="保存"'),
    ('title="Decrease"',                    'title="减少"'),
    ('title="Increase"',                    'title="增加"'),
    ('title="Clear"',                       'title="清空"'),
    ('title="Mute tab"',                    'title="静音标签页"'),
    ('title="Unmute tab"',                  'title="取消静音"'),
    ('title="Add Bookmark"',                'title="添加书签"'),
    ('title="Add favorite"',                'title="添加收藏"'),
    ('title="Maximum 5 favorites"',         'title="最多 5 个收藏"'),
    ('title="Reset zoom (click)"',          'title="重置缩放（点击）"'),
    ('title="Fit to window"',               'title="适应窗口"'),
    ('title="Fit to width"',                'title="适应宽度"'),
    ('title="First page"',                  'title="首页"'),
    ('title="Previous page"',               'title="上一页"'),
    ('title="Next page"',                   'title="下一页"'),
    ('title="Last page"',                   'title="末页"'),
    ('title="Zoom in"',                     'title="放大"'),
    ('title="Zoom out"',                    'title="缩小"'),
    ('title="Reset zoom"',                  'title="重置缩放"'),
    ('title="Download PDF"',                'title="下载 PDF"'),
    ('title="Save User-Agents"',            'title="保存 User-Agent"'),
    ('title="Save allowlist"',              'title="保存白名单"'),
    ('title="Save Rules"',                  'title="保存规则"'),

    # ═══════════════════════════════════════════════════════════
    #  HTML placeholder="..."
    # ═══════════════════════════════════════════════════════════
    ('placeholder="Search or enter address"',    'placeholder="搜索或输入网址"'),
    ('placeholder="Filter…"',                    'placeholder="筛选…"'),
    ('placeholder="Filter tags, attrs…"',        'placeholder="筛选标签、属性…"'),
    ('placeholder="Or paste image URL here..."', 'placeholder="或在此粘贴图片网址…"'),
    ('placeholder="Bookmark name"',              'placeholder="书签名称"'),
    ('placeholder="Name (optional)"',            'placeholder="名称（可选）"'),
    ('placeholder="Search languages..."',        'placeholder="搜索语言…"'),
    ('placeholder="URL"',                        'placeholder="网址"'),

    # ═══════════════════════════════════════════════════════════
    #  HTML 文本节点 - 顶栏
    # ═══════════════════════════════════════════════════════════
    ('>Ready<',                     '>就绪<'),
    ('>Protected<',                 '>已保护<'),
    ('>Paused<',                    '>已暂停<'),
    ('>New Tab</span>',             '>新标签页</span>'),
    ('drop to navigate',            '拖放到此处导航'),

    # ═══════════════════════════════════════════════════════════
    #  HTML 文本节点 - 日志面板
    # ═══════════════════════════════════════════════════════════
    ('>Logs<',                      '>日志<'),
    ('>Logs <',                     '>日志 <'),
    ('>All<',                       '>全部<'),
    ('>Info<',                      '>信息<'),
    ('</i> Info<',                  '</i> 信息<'),
    ('>OK<',                        '>成功<'),
    ('</i> OK<',                    '</i> 成功<'),
    ('>Warn<',                      '>警告<'),
    ('</i> Warn<',                  '</i> 警告<'),
    ('>Err<',                       '>错误<'),
    ('</i> Err<',                   '</i> 错误<'),
    ('>Stream<',                    '>流<'),
    ('</i> Stream<',                '</i> 流<'),
    ('>No matching entries<',       '>无匹配条目<'),
    ('0 requests',                  '0 个请求'),

    # ═══════════════════════════════════════════════════════════
    #  HTML 文本节点 - 元素检查器
    # ═══════════════════════════════════════════════════════════
    ('>Elements<',                  '>元素<'),
    ('>Styles<',                    '>样式<'),
    ('>Box<',                       '>盒模型<'),
    ('>Attrs<',                     '>属性<'),
    ('> Copy Selector<',            '> 复制选择器<'),
    ('> Copy HTML<',                '> 复制 HTML<'),
    ('> Copy Text<',                '> 复制文本<'),
    ('> Scroll Into View<',         '> 滚动到视图<'),
    ('> Hide Element<',             '> 隐藏元素<'),

    # ═══════════════════════════════════════════════════════════
    #  HTML 文本节点 - 右键菜单
    # ═══════════════════════════════════════════════════════════
    ('>Reload</span>',              '>刷新</span>'),
    ('>Reload Tab</span>',          '>刷新标签页</span>'),
    ('>Mute Tab</span>',            '>静音标签页</span>'),
    ('>Unmute Tab</span>',          '>取消静音</span>'),
    ('>Back</span>',                '>后退</span>'),
    ('>Forward</span>',             '>前进</span>'),
    ('>Bookmark Page</span>',       '>收藏此页</span>'),
    ('>Remove Bookmark</span>',     '>移除收藏</span>'),
    ('>Copy URL</span>',            '>复制网址</span>'),
    ('>Settings</span>',            '>设置</span>'),
    ('>Close Tab</span>',           '>关闭标签页</span>'),

    # ═══════════════════════════════════════════════════════════
    #  HTML 文本节点 - 站点信息弹窗
    # ═══════════════════════════════════════════════════════════
    ('>Connection Info<',           '>连接信息<'),
    ('>Host</span>',                '>主机</span>'),
    ('>Protocol</span>',            '>协议</span>'),
    ('>Ad Block</span>',            '>广告拦截</span>'),
    ('>Cookies</span>',             '>Cookie</span>'),
    ('>Cache</span>',               '>缓存</span>'),
    ('>Copy URL<',                  '>复制网址<'),
    ('</i> Copy URL<',              '</i> 复制网址<'),
    ('>Close<',                     '>关闭<'),

    # ═══════════════════════════════════════════════════════════
    #  HTML 文本节点 - 广告拦截弹窗
    # ═══════════════════════════════════════════════════════════
    ('>Gust Adblock<',              '>Gust 广告拦截<'),
    ('>Protection Active<',         '>防护已启用<'),
    ('>Protection Paused<',         '>防护已暂停<'),
    ('>Paused for this site<',      '>此网站已暂停<'),
    ('>Pause for this site<',       '>对此网站暂停<'),
    ('>Re-enable for this site<',   '>对此网站重新启用<'),
    ('> Manage Filters &amp; Settings <',
                                    '> 管理过滤器和设置 <'),
    ('> Manage Filters & Settings <',
                                    '> 管理过滤器和设置 <'),
    ('elements blocked on this page',   '个元素已在此页拦截'),

    # ═══════════════════════════════════════════════════════════
    #  HTML 文本节点 - 历史记录
    # ═══════════════════════════════════════════════════════════
    ('>Recent History<',            '>最近历史<'),
    ('>Last 20 visited sites<',     '>最近访问的 20 个网站<'),
    ('>No history yet<',            '>暂无历史记录<'),

    # ═══════════════════════════════════════════════════════════
    #  HTML 文本节点 - 壁纸弹窗
    # ═══════════════════════════════════════════════════════════
    ('>Change background<',         '>更改背景<'),
    ('</i> Random',                 '</i> 随机'),
    ('</i> Upload',                 '</i> 上传'),
    ('>Reset<',                     '>重置<'),
    ('>Cancel<',                    '>取消<'),
    ('>Apply URL<',                 '>应用网址<'),

    # ═══════════════════════════════════════════════════════════
    #  HTML 文本节点 - 收藏 / 书签弹窗
    # ═══════════════════════════════════════════════════════════
    ('>Add Favorite<',              '>添加收藏<'),
    ('>Add<',                       '>添加<'),
    ('>Add Bookmark<',              '>添加书签<'),
    ('>Save<',                      '>保存<'),
    ('Add favorite',                '添加收藏'),
    ('Add Favorite',                '添加收藏'),
    ('Maximum 5 favorites',         '最多 5 个收藏'),

    # ═══════════════════════════════════════════════════════════
    #  HTML 文本节点 - 快捷键编辑弹窗
    # ═══════════════════════════════════════════════════════════
    ('>Edit Keyboard Shortcut<',    '>编辑键盘快捷键<'),
    ('>Save Shortcut<',             '>保存快捷键<'),
    ('Press <b>Alt + Key</b> to set the new shortcut.',
                                    '按 <b>Alt + 按键</b> 设置新的快捷键。'),
    ('>Waiting for input...<',      '>等待输入…<'),

    # ═══════════════════════════════════════════════════════════
    #  HTML 文本节点 - 指标弹窗
    # ═══════════════════════════════════════════════════════════
    ('Browser Metrics',             '浏览器指标'),
    ('>Refresh<',                   '>刷新<'),

    # ═══════════════════════════════════════════════════════════
    #  设置侧边栏
    # ═══════════════════════════════════════════════════════════
    ('>Connection<',                '>连接<'),
    ('>Search<',                    '>搜索<'),
    ('>Privacy<',                   '>隐私<'),
    ('>Files &amp; Media<',         '>文件与媒体<'),
    ('>Appearance<',                '>外观<'),
    ('>Home Screen<',               '>主页<'),
    ('>Shortcuts<',                 '>快捷键<'),
    ('>Language<',                  '>语言<'),
    ('>Fallback<',                  '>回退<'),
    ('>Tutorial<',                  '>教程<'),
    ('>About<',                     '>关于<'),

    # ═══════════════════════════════════════════════════════════
    #  设置卡片头
    # ═══════════════════════════════════════════════════════════
    ('Fallback WISP Server',            '回退 WISP 服务器'),
    ('WISP Server',                     'WISP 服务器'),
    ('Concurrent Requests',             '并发请求'),
    ('WebRTC Blocking',                 'WebRTC 拦截'),
    ('Smart Request Headers',           '智能请求头'),
    ('Default Search Engine',           '默认搜索引擎'),
    ('Tab Favicons',                    '标签页图标'),
    ('Privacy & Blocking',              '隐私与拦截'),
    ('User-Agent Spoofing',             'User-Agent 伪装'),
    ('Blocklist & Filters',             '黑名单与过滤器'),
    ('Custom Filter Rules',             '自定义过滤规则'),
    ('Tab Caching',                     '标签页缓存'),
    ('Resource Cache',                  '资源缓存'),
    ('Cached Resources',                '已缓存资源'),
    ('Font Size',                       '字体大小'),
    ('Panel Widths',                    '面板宽度'),
    ('Panel Position',                  '面板位置'),
    ('Fullscreen on Launch',            '启动时全屏'),
    ('Keyboard Shortcuts',              '键盘快捷键'),
    ('Bookmarks Bar',                   '书签栏'),
    ('New Tab Wallpaper',               '新标签页壁纸'),
    ('Home Page Clock',                 '主页时钟'),
    ('Interactive Tour',                '交互式导览'),
    ('About Gust',                      '关于 Gust'),
    ('Fallback Behaviour',              '回退行为'),
    ('Retry Policy',                    '重试策略'),
    ('Error Triggers',                  '错误触发条件'),
    ('Advanced Rendering',              '高级渲染'),
    ('Media Range Requests',            '媒体范围请求'),
    ('Unknown File Types',              '未知文件类型'),
    ('PDF Viewer',                      'PDF 查看器'),
    ('Image Viewer',                    '图片查看器'),
    ('Video Player',                    '视频播放器'),
    ('Audio Player',                    '音频播放器'),
    ('Text / Code Viewer',              '文本 / 代码查看器'),
    ('Paused Sites (Allowlist)',        '暂停站点（白名单）'),

    # ═══════════════════════════════════════════════════════════
    #  关于页面标题
    # ═══════════════════════════════════════════════════════════
    ('How it works',                    '工作原理'),
    ('Page rendering',                  '页面渲染'),
    ('Privacy &amp; limitations',       '隐私与限制'),
    ('Credits',                         '致谢'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 危险按钮
    # ═══════════════════════════════════════════════════════════
    ('</i> Clear Cache',                '</i> 清空缓存'),
    ('</i> Reset All',                  '</i> 全部重置'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 连接页
    # ═══════════════════════════════════════════════════════════
    ('>WebSocket URL<',                  '>WebSocket 地址<'),
    ('Current server shown above',       '当前服务器显示在上方'),
    ('Idle threads',                     '空闲线程'),
    ('Active threads',                   '活跃线程'),
    ('Max simultaneous requests when page is loaded (default: 3). Lower = less background CPU.',
                                         '页面加载完成后的最大并发请求数（默认：3）。数值越低，后台 CPU 占用越少。'),
    ('Max simultaneous requests during page load (default: 6). Higher = faster loads but more CPU.',
                                         '页面加载期间的最大并发请求数（默认：6）。数值越高加载越快，但 CPU 占用更多。'),
    ('Block WebRTC connections',         '拦截 WebRTC 连接'),
    ('Prevents sites from establishing direct peer-to-peer connections that bypass the WISP tunnel and could expose your real IP address. Off by default — may break video calls and real-time apps.',
                                         '阻止网站建立绕过 WISP 隧道的直接点对点连接（可能暴露你的真实 IP）。默认关闭 — 开启后可能导致视频通话和实时应用失效。'),
    ('Spoof Sec-Fetch &amp; Referer headers',
                                         '伪造 Sec-Fetch 与 Referer 请求头'),
    ('Synthesize correct <code>Sec-Fetch-Site</code>, <code>Sec-Fetch-Mode</code>, <code>Sec-Fetch-Dest</code>, and <code>Referer</code> headers based on request context. Fixes CDNs and APIs that reject requests with incorrect fetch metadata.',
                                         '根据请求上下文合成正确的 <code>Sec-Fetch-Site</code>、<code>Sec-Fetch-Mode</code>、<code>Sec-Fetch-Dest</code> 和 <code>Referer</code> 请求头。修复因 fetch 元数据不正确而拒绝请求的 CDN 和 API。'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 搜索页
    # ═══════════════════════════════════════════════════════════
    ('Enable spellcheck',                '启用拼写检查'),
    ('Check spelling in text fields and textareas (e.g. search bar, forms).',
                                         '在输入框和文本域中检查拼写（如搜索栏、表单）。'),
    ('Proxy favicons through WISP',      '通过 WISP 代理图标'),
    ("Fetch tab favicons through the WISP server instead of Google's favicon service. More private, but slightly slower.",
                                         '通过 WISP 服务器获取标签页图标，而不是使用 Google 的图标服务。更私密，但略慢。'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 隐私页
    # ═══════════════════════════════════════════════════════════
    ('Ad &amp; Tracker Blocking',        '广告与跟踪器拦截'),
    ('Ad & Tracker Blocking',            '广告与跟踪器拦截'),
    ('Blocks analytics, ads, and tracking scripts',
                                         '拦截分析、广告和跟踪脚本'),
    ('Adblock is paused on these sites. One hostname per line. Use "Pause for this site" in the shield popup to add sites.',
                                         '广告拦截在这些站点上暂停。每行一个主机名。可在盾牌弹窗中使用「对此网站暂停」来添加站点。'),
    ('Request User-Agent',               '请求 User-Agent'),
    ('Sent as the <code>User-Agent</code> HTTP header for all proxied requests.',
                                         '作为所有代理请求的 <code>User-Agent</code> HTTP 请求头发送。'),
    ('Page navigator.userAgent',         '页面 navigator.userAgent'),
    ('Overrides <code>navigator.userAgent</code> inside loaded pages.',
                                         '覆盖加载页面内的 <code>navigator.userAgent</code>。'),
    ('Enter CSS selectors to hide (one per line).',
                                         '输入要隐藏的 CSS 选择器（每行一个）。'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 缓存页
    # ═══════════════════════════════════════════════════════════
    ('Keep tabs loaded in background',   '在后台保持标签页加载'),
    ("When enabled, switching between tabs won't reload them. Disable to save memory.",
                                         '启用后，切换标签页不会重新加载。关闭可节省内存。'),
    ('Calculating...',                   '计算中…'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 外观页
    # ═══════════════════════════════════════════════════════════
    ('Adjust text size across the entire interface',
                                         '调整整个界面的文字大小'),
    ('Remember panel widths',            '记住面板宽度'),
    ('When enabled, panel widths are saved. When disabled, they reset to default on close.',
                                         '启用后，面板宽度会被保存。关闭后，关闭时重置为默认值。'),
    ('Panels on the left',               '面板位于左侧'),
    ('Move the Logs and Elements panels to the left side of the browser window instead of the right.',
                                         '将日志和元素面板移到浏览器窗口左侧。'),
    ('Start in fullscreen',              '启动进入全屏'),
    ('Automatically enter fullscreen on your first click or keypress after opening Gust.',
                                         '打开 Gust 后，首次点击或按键时自动进入全屏。'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 快捷键页
    # ═══════════════════════════════════════════════════════════
    ('Enable keyboard shortcuts',        '启用键盘快捷键'),
    ('When off, all Alt + key shortcuts are disabled.',
                                         '关闭后，所有 Alt + 按键快捷键都将禁用。'),
    ('>Reload Page</span>',              '>刷新页面</span>'),
    ('>Focus URL Bar</span>',            '>聚焦地址栏</span>'),
    ('>Toggle Logs</span>',              '>切换日志</span>'),
    ('>Element Inspector</span>',        '>元素检查器</span>'),
    ('>Metrics</span>',                  '>指标</span>'),
    ('>Toggle Fullscreen</span>',        '>切换全屏</span>'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 主页
    # ═══════════════════════════════════════════════════════════
    ('Show Bookmarks Bar',               '显示书签栏'),
    ('Always show the bookmarks bar below the address bar',
                                         '始终在地址栏下方显示书签栏'),
    ('Background image',                 '背景图片'),
    ('Show clock on new tab',            '在新标签页上显示时钟'),
    ('Display current time and date on the home screen',
                                         '在主页上显示当前时间和日期'),
    ('24-hour clock',                    '24 小时制'),
    ('Show time in 24-hour format (e.g. 14:30 instead of 2:30 PM)',
                                         '以 24 小时制显示时间（例如 14:30 而非 2:30 PM）'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 语言
    # ═══════════════════════════════════════════════════════════
    ('Preferred language',               '首选语言'),
    ('Choose the language for the interface and spellcheck when supported.',
                                         '选择界面和拼写检查所用的语言（若支持）。'),
    ('System default',                   '系统默认'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 教程页
    # ═══════════════════════════════════════════════════════════
    ('Walk through 16 steps covering navigation, search, bookmarks, ad blocking, metrics, browser logs, page inspector, tabs, and the new tab page. Takes under a minute.',
                                         '用 16 个步骤带你了解导航、搜索、书签、广告拦截、指标、浏览器日志、页面检查器、标签页和新标签页。不到一分钟。'),
    ('Under a minute',                   '不到一分钟'),
    ('Start Tour',                       '开始导览'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 回退
    # ═══════════════════════════════════════════════════════════
    ('Enable fallback on load error',    '加载失败时启用回退'),
    ('When a page fails to load (network error, bad status, timeout), automatically retry using the fallback proxy before showing an error page.',
                                         '页面加载失败时（网络错误、状态码异常、超时），在显示错误页面前自动使用回退代理重试。'),
    ('Log retries',                      '记录重试'),
    ('All fallback retry attempts are always written to the request log, including which WISP server was used.',
                                         '所有回退重试都会记录到请求日志中，包括使用的是哪个 WISP 服务器。'),
    ('always on',                        '始终开启'),
    ('Fallback WebSocket URL',           '回退 WebSocket 地址'),
    ('Used only when the primary WISP server is unreachable or returns an error. Leave blank to disable.',
                                         '仅当主 WISP 服务器无法访问或返回错误时使用。留空则禁用。'),
    ('Max retry attempts (main)',        '最大重试次数（主）'),
    ('How many times Gust retries on the primary WISP server before switching to the fallback.',
                                         '切换到回退服务器前在主 WISP 服务器上重试的次数。'),
    ('Max retry attempts (fallback)',    '最大重试次数（回退）'),
    ('How many times Gust will attempt the fallback WISP before giving up and showing an error.',
                                         '显示错误前在回退 WISP 上尝试的次数。'),
    ('Retry delay (seconds)',            '重试延迟（秒）'),
    ('Wait time between each retry attempt before switching to the fallback server.',
                                         '切换到回退服务器前，每次重试之间的等待时间。'),
    ('Fallback on HTTP 5xx errors',      'HTTP 5xx 错误时回退'),
    ('Retry via fallback when the origin server returns a 500-level status code.',
                                         '源服务器返回 5xx 状态码时通过回退重试。'),
    ('Fallback on timeout',              '超时时回退'),
    ('Retry via fallback when the primary server exceeds the connection timeout.',
                                         '主服务器连接超时时通过回退重试。'),
    ('Fallback on DNS failure',          'DNS 失败时回退'),
    ('Retry via fallback when the hostname cannot be resolved.',
                                         '主机名无法解析时通过回退重试。'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 文件与媒体
    # ═══════════════════════════════════════════════════════════
    ('Script tags loaded per page',      '每页加载的脚本标签数'),
    ('Maximum number of <code>&lt;script src&gt;</code> tags loaded when rendering a page. Higher values help complex React / Next.js / Vite apps but use more memory. Default: 250.',
                                         '渲染页面时加载的 <code>&lt;script src&gt;</code> 标签最大数量。数值越高越有利于复杂的 React / Next.js / Vite 应用，但占用内存更多。默认：250。'),
    ('Images prefetched per page',       '每页预取的图片数'),
    ('Maximum number of images fetched and inlined before the page is displayed. Lower values speed up initial load on image-heavy sites; higher values improve visual completeness. Default: 300.',
                                         '页面显示前预取并内联的图片最大数量。数值越低，图片多的网站初始加载越快；数值越高，视觉完整度越高。默认：300。'),
    ('Enable Range request support',     '启用 Range 请求支持'),
    ('Forward <code>Range</code> headers and handle <code>206 Partial Content</code> responses. Fixes video/audio seeking and embedded media playback on most sites.',
                                         '转发 <code>Range</code> 请求头并处理 <code>206 Partial Content</code> 响应。修复大多数网站上的视频/音频拖动和嵌入式媒体播放。'),
    ('Auto-download unknown files',      '自动下载未知文件'),
    ("When Gust receives a file it can't display (e.g. .zip, .exe), automatically trigger a browser download instead of showing an error page.",
                                         '当 Gust 收到无法显示的文件（如 .zip、.exe）时，自动触发浏览器下载，而不是显示错误页。'),
    ('Built-in PDF viewer',              '内置 PDF 查看器'),
    ('Render PDF files inline using a built-in viewer powered by PDF.js instead of downloading them.',
                                         '使用基于 PDF.js 的内置查看器内联渲染 PDF 文件，而不是下载它们。'),
    ('Built-in image viewer',            '内置图片查看器'),
    ('Display images (PNG, JPEG, GIF, WebP, SVG…) in a clean fullscreen viewer with zoom and pan.',
                                         '在简洁的全屏查看器中显示图片（PNG、JPEG、GIF、WebP、SVG…），支持缩放和平移。'),
    ('Built-in video player',            '内置视频播放器'),
    ('Play video files (MP4, WebM, OGG…) in a built-in player with controls.',
                                         '使用内置播放器播放视频文件（MP4、WebM、OGG…），带控制栏。'),
    ('Built-in audio player',            '内置音频播放器'),
    ('Play audio files (MP3, OGG, FLAC, WAV…) in a styled player instead of downloading.',
                                         '使用样式化的播放器播放音频文件（MP3、OGG、FLAC、WAV…），而不是下载。'),
    ('Built-in text viewer',             '内置文本查看器'),
    ('Display plain text, JSON, XML, CSV, and source code files inline with syntax-aware formatting.',
                                         '内联显示纯文本、JSON、XML、CSV 和源代码文件，并带语法感知格式化。'),

    # ═══════════════════════════════════════════════════════════
    #  教程弹窗按钮
    # ═══════════════════════════════════════════════════════════
    ('>Skip tour<',                      '>跳过导览<'),
    ('>Next<',                           '>下一步<'),
    ('>Back<',                           '>上一步<'),
    ("</i>Done'",                        "</i>完成'"),
    ("'Next <i class=\"fas fa-arrow-right\"></i>'",
                                         "'下一步 <i class=\"fas fa-arrow-right\"></i>'"),

    # ═══════════════════════════════════════════════════════════
    #  教程弹窗标题（JS 字符串）
    # ═══════════════════════════════════════════════════════════
    ("title: 'Welcome to GUST'",            "title: '欢迎使用 GUST'"),
    ("title: 'Navigation Buttons'",         "title: '导航按钮'"),
    ("title: 'Address and Search Bar'",     "title: '地址与搜索栏'"),
    ("title: 'Bookmarks'",                  "title: '书签'"),
    ("title: 'Recent History'",             "title: '最近历史'"),
    ("title: 'Ad and Tracker Blocking'",    "title: '广告与跟踪器拦截'"),
    ("title: 'Browser Logs'",               "title: '浏览器日志'"),
    ("title: 'Page Inspector'",             "title: '页面检查器'"),
    ("title: 'Settings'",                   "title: '设置'"),
    ("title: 'Change Wallpaper'",           "title: '更改壁纸'"),
    ("title: \"You're all set!\"",          "title: '大功告成！'"),

    # ═══════════════════════════════════════════════════════════
    #  关于页面正文
    # ═══════════════════════════════════════════════════════════
    ("Gust is a <strong style=\"color:var(--tx);\">static</strong> web proxy browser that runs entirely inside a single HTML file.",
                                        'Gust 是一个完全运行在单个 HTML 文件内的<strong style="color:var(--tx);">静态</strong> Web 代理浏览器。'),
    ("When you navigate to a URL, Gust fetches the target site's HTML, CSS, scripts, and assets through <em>Wisp</em>, then rewrites all resource URLs and injects them into a sandboxed iframe.",
                                        '当你导航到一个网址时，Gust 会通过 <em>Wisp</em> 获取目标站点的 HTML、CSS、脚本和资源，然后重写所有资源 URL 并将其注入到沙盒 iframe 中。'),
    ("Gust can be run inside any HTML editor, <code style=\"background:var(--bg3); padding:2px 6px; border-radius:4px; font-size:12px;\">iframe</code>, file, or blob. It's ultra lightweight, packed with features, and is near impossible to block for admins.",
                                        'Gust 可运行在任何 HTML 编辑器、<code style="background:var(--bg3); padding:2px 6px; border-radius:4px; font-size:12px;">iframe</code>、文件或 blob 中。它极其轻量，功能丰富，管理员几乎无法屏蔽。'),
    ("All network requests are tunnelled through a <strong style=\"color:var(--tx);\">WISP WebSocket server</strong>.",
                                        '所有网络请求都通过 <strong style="color:var(--tx);">WISP WebSocket 服务器</strong>隧道传输。'),
    ("Your browser opens a WebSocket to the WISP endpoint, which forwards TCP/TLS connections on your behalf.",
                                        '你的浏览器会向 WISP 端点打开一个 WebSocket，由其代为转发 TCP/TLS 连接。'),
    ("The actual HTTP fetching is handled by <strong style=\"color:var(--tx);\">libcurl.js</strong> &mdash; a port of the curl HTTP library compiled to WebAssembly &mdash; giving full HTTPS, redirect, and cookie support inside the browser context.",
                                        '实际的 HTTP 请求由 <strong style="color:var(--tx);">libcurl.js</strong> 处理 &mdash; 它是 curl HTTP 库编译为 WebAssembly 的移植版 &mdash; 在浏览器上下文中提供完整的 HTTPS、重定向和 Cookie 支持。'),
    ("Fetched HTML is parsed and rewritten in JavaScript. CSS stylesheets and scripts are loaded through the proxy and injected inline or as Blob URLs.",
                                        '获取的 HTML 由 JavaScript 解析并重写。CSS 样式表和脚本通过代理加载，并以内联或 Blob URL 的形式注入。'),
    ("Images, fonts, and other assets have their URLs rewritten to route through the same proxy pipeline.",
                                        '图片、字体和其他资源的 URL 被重写，以通过同一代理管道路由。'),
    ("The final document is rendered inside a sandboxed <code style=\"background:var(--bg3); padding:2px 6px; border-radius:4px; font-size:12px;\">iframe</code> using a generated Blob URL.",
                                        '最终文档使用生成的 Blob URL 在沙盒 <code style="background:var(--bg3); padding:2px 6px; border-radius:4px; font-size:12px;">iframe</code> 中渲染。'),
    ("Because requests flow through the WISP server, your real IP is not exposed to the sites you visit.",
                                        '由于请求流经 WISP 服务器，你的真实 IP 不会暴露给你访问的站点。'),
    ("However, the WISP server operator may be able to see your traffic.",
                                        '但 WISP 服务器运营者可能看到你的流量。'),
    ("Some complex web features (native WebSockets from within pages, WebRTC, service workers) cannot be fully proxied and may not work.",
                                        '一些复杂的 Web 特性（页面内的原生 WebSocket、WebRTC、Service Worker）无法完全代理，可能无法工作。'),
    ("JavaScript inside the iframe is fully sandboxed from the parent page.",
                                        'iframe 内的 JavaScript 与父页面完全隔离。'),
    ('WebSocket proxy tunnelling',      'WebSocket 代理隧道'),
    ('curl compiled to WebAssembly',    'curl 编译为 WebAssembly'),
    ('v4.2.67 · PDF rendering engine',  'v4.2.67 · PDF 渲染引擎'),
    ('v6.5.1 · Icon library',           'v6.5.1 · 图标库'),
    ('v2.1.11 · ISO language codes',    'v2.1.11 · ISO 语言代码'),
    ('Monospace font (code viewer)',    '等宽字体（代码查看器）'),
    ('UI font via Google Fonts',        '通过 Google Fonts 加载的界面字体'),
    ('Proxy cache, storage, sessions',  '代理缓存、存储、会话'),

    # ═══════════════════════════════════════════════════════════
    #  JS 字符串字面量 - 状态 / 通用
    # ═══════════════════════════════════════════════════════════
    ('"Ready"',                     '"就绪"'),
    ('"Protected"',                 '"已保护"'),
    ('"Paused"',                    '"已暂停"'),
    ('"New Tab"',                   '"新标签页"'),
    ("'New Tab'",                   "'新标签页'"),
    ('"Not secure"',                '"不安全"'),
    ('"Loading..."',                '"加载中…"'),
    ('"Stopped"',                   '"已停止"'),
    ('"Error"',                     '"错误"'),
    ('"Copied!"',                   '"已复制！"'),
    ('</i> Copied!<',               '</i> 已复制!<'),
    ('"Aborted"',                   '"已中止"'),
    ('"Starting..."',               '"正在启动…"'),
    ('"Cache initialized"',         '"缓存已初始化"'),
    ('"Page ready"',                '"页面就绪"'),
    ('"Logs cleared"',              '"日志已清空"'),
    ('"Logs copied to clipboard"',  '"日志已复制到剪贴板"'),
    ('"Custom filters saved"',      '"自定义过滤器已保存"'),
    ('"Failed to save filters"',    '"保存过滤器失败"'),
    ('"Browser reset initiated..."','"浏览器重置已开始…"'),
    ('"URL copied to clipboard"',   '"网址已复制到剪贴板"'),
    ('"Failed to copy URL"',        '"复制网址失败"'),

    # ═══════════════════════════════════════════════════════════
    #  JS 字符串字面量 - 错误类型
    # ═══════════════════════════════════════════════════════════
    ('"Connection Error"',          '"连接错误"'),
    ('"DNS Resolution Failed"',     '"DNS 解析失败"'),
    ('"Connection Timeout"',        '"连接超时"'),
    ('"Connection Refused"',        '"连接被拒绝"'),
    ('"SSL/TLS Error"',             '"SSL/TLS 错误"'),
    ('"Network Error"',             '"网络错误"'),
    ('"Request Blocked"',           '"请求被拦截"'),
    ('"Page Not Found"',            '"页面未找到"'),
    ('"Internal Server Error"',     '"服务器内部错误"'),
    ('"Access Forbidden"',          '"访问被禁止"'),
    ('"Connection Interrupted"',    '"连接已中断"'),
    ('"Error Loading Page"',        '"加载页面出错"'),
    ('"Unknown Gust Page"',         '"未知的 Gust 页面"'),
    ('"Unknown Settings Page"',     '"未知的设置页面"'),
    ('"Invalid Internal URL"',      '"无效的内部网址"'),

    # ═══════════════════════════════════════════════════════════
    #  JS - 广告拦截
    # ═══════════════════════════════════════════════════════════
    ('"Protection Active"',         '"防护已启用"'),
    ('"Protection Paused"',         '"防护已暂停"'),
    ('"Paused for this site"',      '"此网站已暂停"'),
    ("'Pause for this site'",       "'对此网站暂停'"),
    ("'Re-enable for this site'",   "'对此网站重新启用'"),
    ("'Protection Active'",         "'防护已启用'"),
    ("'Protection Paused'",         "'防护已暂停'"),
    ("'Paused for this site'",      "'此网站已暂停'"),
    ("'Protected'",                 "'已保护'"),
    ("'Paused'",                    "'已暂停'"),
    ("'Mute Tab'",                  "'静音标签页'"),
    ("'Unmute Tab'",                "'取消静音'"),
    ("'Bookmark Page'",             "'收藏此页'"),
    ("'Remove Bookmark'",           "'移除收藏'"),
    ("'Toggle fullscreen (F11)'",   "'切换全屏 (F11)'"),
    ("'Exit fullscreen (F11)'",     "'退出全屏 (F11)'"),
    ('"Mute Tab"',                  '"静音标签页"'),
    ('"Unmute Tab"',                '"取消静音"'),
    ('"Bookmark Page"',             '"收藏此页"'),
    ('"Remove Bookmark"',           '"移除收藏"'),
    ('"Toggle fullscreen (F11)"',   '"切换全屏 (F11)"'),
    ('"Exit fullscreen (F11)"',     '"退出全屏 (F11)"'),
    ('"Bookmark this page (Alt+D)"',  '"收藏此页 (Alt+D)"'),
    ('"Remove bookmark (Alt+D)"',     '"移除收藏 (Alt+D)"'),
    ("'Auto-scroll on'",              "'自动滚动已开'"),
    ("'Auto-scroll off'",             "'自动滚动已关'"),
    ("'Unmute tab'",                  "'取消静音'"),
    ("'Mute tab'",                    "'静音标签页'"),
    ('"Add Bookmark"',                '"添加书签"'),
    ('"Add favorite"',                '"添加收藏"'),
    ('"Maximum 5 favorites"',         '"最多 5 个收藏"'),

    # ═══════════════════════════════════════════════════════════
    #  JS - 日志消息
    # ═══════════════════════════════════════════════════════════
    ("'WISP connection lost, reconnecting...'", "'WISP 连接断开，正在重连…'"),
    ("'WISP reconnect failed after 3 attempts: '", "'WISP 重连 3 次失败: '"),
    ("'WISP reconnect attempt '",   "'WISP 第 '"),
    ("' failed, retrying...'",      "' 次重连失败，重试中…'"),
    ("'Reconnected to WISP (attempt '", "'已重连 WISP（第 '"),
    ('WISP switched to <span',      'WISP 已切换到 <span'),
    ("'WISP reconnect failed: '",   "'WISP 重连失败: '"),
    ('Loaded: ` + url',             '已加载: ` + url'),
    ('"Loaded: "',                  '"已加载: "'),
    ('Failed: ` + e.message',       '失败: ` + e.message'),
    ('<span>Loaded: ',              '<span>已加载: '),
    ('<span>Failed: ',              '<span>失败: '),
    ('Blocked ad:',                 '已拦截广告:'),
    ('Blocked tracker:',            '已拦截跟踪器:'),
    ('>Blocked:</span>',            '>已拦截:</span>'),
    ('Cosmetic filter:',            '外观过滤:'),
    ('WS error:',                   'WebSocket 错误:'),
    ('WS failed:',                  'WebSocket 失败:'),
    ('CSS err: ',                   'CSS 错误: '),
    ('IMG err: ',                   '图片错误: '),
    ('Downloaded: ',                '已下载: '),
    ("'Download failed: '",         "'下载失败: '"),
    ('[Page] ',                     '[页面] '),
    ("'Shortcut reset: '",          "'快捷键已重置: '"),
    ('Shortcut updated: ',          '快捷键已更新: '),

    # ═══════════════════════════════════════════════════════════
    #  JS - 站点信息动态文案
    # ═══════════════════════════════════════════════════════════
    ('"Gust Browser"',              '"Gust 浏览器"'),
    ('"Internal page"',             '"内部页面"'),
    ('"Internal"',                  '"内部"'),
    ('>Internal</span>',            '>内部</span>'),
    ('"Connection is proxied"',     '"连接已代理"'),
    ('"Your real IP is hidden from this site"', '"你的真实 IP 对此站点隐藏"'),
    ('"Connection not secure"',     '"连接不安全"'),
    ('"This site uses an unencrypted connection"', '"此站点使用未加密连接"'),
    ('"Connection info"',           '"连接信息"'),
    ('"HTTPS - Encrypted"',         '"HTTPS - 已加密"'),
    ('>HTTPS - Encrypted</span>',   '>HTTPS - 已加密</span>'),
    ('"HTTP - Not encrypted"',      '"HTTP - 未加密"'),
    ('>HTTP - Not encrypted</span>', '>HTTP - 未加密</span>'),
    ('"Page failed to load"',       '"页面加载失败"'),
    ('"An error occurred while loading this page"', '"加载此页面时出错"'),
    ('"Connection error"',          '"连接错误"'),
    ('>Connection error</span>',    '>连接错误</span>'),
    ('"None"',                      '"无"'),
    ('>None</span>',                '>无</span>'),
    ('"Empty"',                     '"空"'),
    ('>Empty</span>',               '>空</span>'),
    ('"N/A"',                       '"不可用"'),
    ('>N/A</span>',                 '>不可用</span>'),
    ("'just now'",                  "'刚刚'"),
    ("'m ago'",                     "' 分钟前'"),
    ("'h ago'",                     "' 小时前'"),
    ("'d ago'",                     "' 天前'"),
    ('"Custom wallpaper set"',      '"已设置自定义壁纸"'),
    ('"Using default gradient"',    '"使用默认渐变"'),
    ('Custom wallpaper set',        '已设置自定义壁纸'),
    ('Using default gradient',      '使用默认渐变'),

    # ═══════════════════════════════════════════════════════════
    #  JS - 指标弹窗
    # ═══════════════════════════════════════════════════════════
    ("'clock', 'Uptime'",           "'clock', '运行时长'"),
    ("'since load'",                "'自加载起'"),
    ("'layer-group', 'Open Tabs'",  "'layer-group', '打开的标签页'"),
    ("tabCount === 1 ? 'tab' : 'tabs'", "tabCount === 1 ? '个' : '个'"),
    ("'bolt', 'Active Requests'",   "'bolt', '活跃请求'"),
    ("'idle'",                      "'空闲'"),
    ("`+${queued} queued`",         "`+${queued} 排队中`"),
    ("'database', 'Page Cache'",    "'database', '页面缓存'"),
    ("'in-memory entries'",         "'内存中的条目'"),
    ("'JS Heap'",                   "'JS 堆内存'"),
    ('>JS Heap</span>',             '>JS 堆内存</span>'),
    ("'Not available'",             "'不可用'"),
    ('>Not available</span>',       '>不可用</span>'),
    ("'of ${fmtBytes(memTotal)}'",  "'共 ${fmtBytes(memTotal)}'"),
    ('>of ${fmtBytes(memTotal)}<',  '>共 ${fmtBytes(memTotal)}<'),
    ("metricSection('Network'",     "metricSection('网络'"),
    ("metricSection('Storage'",     "metricSection('存储'"),
    ("metricSection('Page Performance'", "metricSection('页面性能'"),
    ("'WISP endpoint'",             "'WISP 端点'"),
    ("'Connection type'",           "'连接类型'"),
    ("'Round-trip time'",           "'往返时间'"),
    ("'Downlink'",                  "'下行速度'"),
    ("'Used'",                      "'已使用'"),
    ("'Quota'",                     "'配额'"),
    ("'Page load time'",            "'页面加载时间'"),
    ("'First contentful paint'",    "'首次内容绘制'"),
    ("'Resources loaded'",          "'已加载资源'"),
    ("'Cookie store'",              "'Cookie 存储'"),
    ("' transferred)'",             "' 已传输)'"),
    (' transferred)',               ' 已传输)'),
    ("' origins'",                  "' 个来源'"),

    # ═══════════════════════════════════════════════════════════
    #  JS - 文件查看器
    # ═══════════════════════════════════════════════════════════
    ('>Loading PDF\\u2026<',        '>正在加载 PDF...<'),
    ('>Failed to load PDF<',        '>PDF 加载失败<'),
    ('"Decoding PDF\\u2026"',       '"正在解码 PDF..."'),
    ('"Rendering pages\\u2026"',    '"正在渲染页面..."'),
    ('"Loading\\u2026"',            '"加载中..."'),
    ('>Loading\\u2026</div>',       '>加载中...</div>'),
    ('> Fit<',                      '> 适应宽度<'),
    ('>Fit</button>',               '>适应</button>'),
    ('> Download</button>',         '> 下载</button>'),
    ('> Download PDF<',             '> 下载 PDF<'),
    ('> Wrap<',                     '> 自动换行<'),
    ('>Wrap</button>',              '>自动换行</button>'),
    ('> Copy<',                     '> 复制<'),
    ('>Copy</button>',              '>复制</button>'),
    ('"Failed to load image"',      '"图片加载失败"'),
    ('>Cannot Open File<',          '>无法打开文件<'),
    ("Gust doesn\\'t have a built-in viewer for this file type.",
                                    'Gust 没有此文件类型的内置查看器。'),
    ("<strong style=\"color:#b8c4d0\">Auto-download</strong>",
                                    '<strong style="color:#b8c4d0">自动下载</strong>'),
    ('in Files &amp; Media settings to download it instead.',
                                    '可在「文件与媒体」设置中启用来下载它。'),
    ('> Go Back<',                  '> 返回<'),
    ('>Go Back</button>',           '>返回</button>'),
    ('> File Settings<',            '> 文件设置<'),
    ('>File Settings</button>',     '>文件设置</button>'),
    ('> Download File<',            '> 下载文件<'),
    ('>Download File</button>',     '>下载文件</button>'),

    # ═══════════════════════════════════════════════════════════
    #  JS - 错误页面
    # ═══════════════════════════════════════════════════════════
    ('<title>Error - Gust Browser</title>', '<title>错误 - Gust 浏览器</title>'),
    ('>Try these steps<',           '>请尝试以下步骤<'),
    ('> Reload Page <',             '> 重新加载 <'),
    ('> Open Logs <',               '> 打开日志 <'),

    # ═══════════════════════════════════════════════════════════
    #  设置页标签标题（模板字符串）
    # ═══════════════════════════════════════════════════════════
    ('Settings - ${',               '设置 - ${'),
    ('`Settings - ',                '`设置 - '),

    # ═══════════════════════════════════════════════════════════
    #  GitHub 仓库地址替换
    # ═══════════════════════════════════════════════════════════
    ('window.open("https://github.com/nautilus-os/GUST"',
     'window.open("https://github.com/cjhdevact/GUST-Chinese"'),

    # ═══════════════════════════════════════════════════════════
    #  教程 body 段落
    # ═══════════════════════════════════════════════════════════
    ("A fast, private browser by Nautilus Labs. This tour covers all the key controls and takes under a minute, and can be restarted anytime from Settings.",
     'Nautilus Labs 出品的快速、私密浏览器。本导览涵盖所有关键控件，不到一分钟即可完成，随时可从设置中重新开始。该版本由 CJH 翻译。'),
    ("Back (<i class=\"fas fa-arrow-left\" style=\"font-size:0.8em;\"></i>), forward (<i class=\"fas fa-arrow-right\" style=\"font-size:0.8em;\"></i>), reload and home. The home button returns to the new tab page, and you can pause a page reloading by clicking the square in its place.",
     '后退、前进、刷新和主页。主页按钮返回新标签页，点击方形按钮可暂停页面重新加载。'),
    ("Type a URL or search term and press Enter. The lock icon shows connection security, and clicking on it shows site info. The bookmark icon saves the current page instantly.",
     '输入网址或搜索词后按回车。锁形图标显示连接安全性，点击可查看站点信息。书签图标可立即收藏当前页面。'),
    ("Bookmark the current page with this button or Ctrl+D. Your bookmarks appear in the bar below the address bar. Right-click any bookmark to edit or remove it.",
     '用此按钮或 Ctrl+D 收藏当前页面。书签显示在地址栏下方的书签栏中。右键点击书签可编辑或移除。'),
    ("Jump back to recently visited pages. If you close a tab by accident, open history to recover the URL. No browsing data ever leaves your device, or is saved longer than 10 entries.",
     '快速回到最近访问的页面。如果不小心关闭了标签页，可打开历史记录恢复网址。浏览数据不会离开你的设备，最多保存 10 条。'),
    ("GUST blocks ads and trackers by default. The badge shows your current status. Click on it to toggle it off if a site is not loading correctly.",
     'GUST 默认拦截广告和跟踪器。徽章显示当前状态。如果某站点加载异常，点击可关闭拦截。'),
    ("Live stats at a glance: active requests, queue depth, memory, cache hit rate, network info and page performance. Useful for debugging slow sites.",
     '实时统计一览：活跃请求、队列深度、内存、缓存命中率、网络信息和页面性能。对调试缓慢站点很有用。'),
    ("Opens the request log panel. See every fetch, cache hit, blocked tracker and error in real time. Essential for diagnosing proxy or network issues.",
     '打开请求日志面板。实时查看每次请求、缓存命中、被拦截的跟踪器和错误。诊断代理或网络问题的必备工具。'),
    ("Inspect the live DOM of any page. Browse the element tree, view computed styles, box model and attributes. Works even if devtools are disabled in your browser.",
     '检查任意页面的实时 DOM。浏览元素树，查看计算样式、盒模型和属性。即使浏览器禁用了开发者工具也能使用。'),
    ("Open a new tab with this button or Alt+T. Tabs show favicons and scroll horizontally when you have many open. Use the <i class=\"fas fa-arrow-left\"></i> <i class=\"fas fa-arrow-right\"></i> arrows to scroll them.",
     '用此按钮或 Alt+T 打开新标签页。标签页显示网站图标，数量多时可水平滚动。使用左右箭头滚动它们。'),
    ("Configure the WISP server, search engine, wallpaper, font size, cache, shortcuts and more. You can also read about Gust or restart the tutorial from here.",
     '配置 WISP 服务器、搜索引擎、壁纸、字体大小、缓存、快捷键等。也可以在此了解 Gust 或重新开始导览。'),
    ("Click the chevron to show or hide the bookmarks bar if it takes up too much space. To reenable click the down chevron that appears next to settings.",
     '如果书签栏占用空间太大，点击箭头显示或隐藏它。要重新启用，点击设置旁边出现的向下箭头。'),
    ("Pin your most-visited sites as favorites on the new tab page for instant access. You can add up to 5.",
     '将最常访问的网站固定为新标签页上的收藏，方便快速访问。最多可添加 5 个。'),
    ("Customize the new tab page background. Upload any image, use a random stock image, paste an image URL, or reset to the default gradient.",
     '自定义新标签页背景。可上传任意图片、使用随机库存图片、粘贴图片网址，或重置为默认渐变。'),
    ("GUST is open source. Click to view the repository, report issues, or contribute.",
     'GUST 是开源的。点击查看仓库、报告问题或贡献代码。'),
    ("That's the full tour! GUST is made with lots of love by the Nautilus Labs dev team, and we'd be overjoyed if you gave our repository a star on GitHub. Enjoy the experience!",
     '导览到此结束！GUST 由 Nautilus Labs 开发团队倾心打造，如果你能在 GitHub 上给我们的仓库点个星，我们会非常开心。祝你使用愉快！'),

])


# ═══════════════════════════════════════════════════════════════════
#  根据开关动态追加的替换规则
# ═══════════════════════════════════════════════════════════════════

# ── 开关 1：添加百度搜索引擎 ──────────────────────────────────
if ADD_BAIDU_ENGINE:
    REPLACEMENTS.update(OrderedDict([
        ('bing: "https://www.bing.com/search?q="',
         'bing: "https://www.bing.com/search?q=",\n    baidu: "https://www.baidu.com/s?wd="'),
        ('<button data-engine="bing">Bing</button>',
         '<button data-engine="bing">Bing</button>\n                                    <button data-engine="baidu">百度</button>'),
        ('{ key: "bing", name: "Bing", url: SEARCH_ENGINES.bing }',
         '{ key: "bing", name: "Bing", url: SEARCH_ENGINES.bing },\n                    { key: "baidu", name: "百度", url: SEARCH_ENGINES.baidu }'),
        ("const engineNames = { brave: 'Brave', bing: 'Bing' };",
         "const engineNames = { brave: 'Brave', bing: 'Bing', baidu: '百度' };"),
    ]))

# ── 开关 2：将默认搜索引擎改为必应 ─────────────────────────────
if USE_BING_AS_DEFAULT:
    REPLACEMENTS.update(OrderedDict([
        ("ls.getItem('gust:engine:v1') || 'brave'; } catch { return 'brave'; }",
         "ls.getItem('gust:engine:v1') || 'bing'; } catch { return 'bing'; }"),
        ('<span id="ntEngineLabel">Brave</span>',
         '<span id="ntEngineLabel">Bing</span>'),
        ("selectedEngine = 'brave';",
         "selectedEngine = 'bing';"),
        ("ls.setItem('gust:engine:v1', 'brave');",
         "ls.setItem('gust:engine:v1', 'bing');"),
        ("engineNames[selectedEngine] || 'Brave'",
         "engineNames[selectedEngine] || 'Bing'"),
    ]))


# ═══════════════════════════════════════════════════════════════════
#  清理永远不会命中的冗余规则（仅为了让报告更干净，不影响功能）
# ═══════════════════════════════════════════════════════════════════
for _dead_key in [
    '>Cache<',                       # 已被 >Cache</span> 覆盖
    'Blocklist & Filter',            # 源码里只有 Filters
    'Privacy & limitations',         # 源码里是 &amp; 形式
    'Save Rules',                    # 源码里只有 title="Save Rules"
    '>Done<',                        # 已被 </i>Done' 覆盖
    "'Ready'",                       # 源码里是 "Ready"
    '"Loading…"',                    # 源码里是 "Loading..."
]:
    REPLACEMENTS.pop(_dead_key, None)


# ═══════════════════════════════════════════════════════════════════
#  水印移除规则
# ═══════════════════════════════════════════════════════════════════
WATERMARK_PATTERNS = [
    re.compile(r'<div\s+id="gustCredit"[^>]*>.*?</div>', re.DOTALL | re.IGNORECASE),
]


# ═══════════════════════════════════════════════════════════════════
#  Emoji 清理规则
# ═══════════════════════════════════════════════════════════════════
EMOJI_PATTERNS = [
    re.compile(r'[\U0001F300-\U0001F5FF]'),
    re.compile(r'[\U0001F600-\U0001F64F]'),
    re.compile(r'[\U0001F680-\U0001F6FF]'),
    re.compile(r'[\U0001F700-\U0001F77F]'),
    re.compile(r'[\U0001F780-\U0001F7FF]'),
    re.compile(r'[\U0001F800-\U0001F8FF]'),
    re.compile(r'[\U0001F900-\U0001F9FF]'),
    re.compile(r'[\U0001FA00-\U0001FA6F]'),
    re.compile(r'[\U0001FA70-\U0001FAFF]'),
    re.compile(r'[\U00002600-\U000026FF]'),
    re.compile(r'[\U00002700-\U000027BF]'),
    re.compile(r'[\U0001F1E6-\U0001F1FF]'),
    re.compile(r'[\U0000FE00-\U0000FE0F]'),
    re.compile(r'[\U0001F3FB-\U0001F3FF]'),
    re.compile(r'\u2764[\uFE0F]?'),
    re.compile(r'\u200D'),
]


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
    """把任意空白序列压成单个空格，用于反查替换表"""
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


def strip_watermark(html: str, counts: dict) -> str:
    for pat in WATERMARK_PATTERNS:
        html, n = pat.subn('', html)
        if n:
            counts['__watermark__'] = counts.get('__watermark__', 0) + n
    return html


def strip_emoji(html: str, counts: dict) -> str:
    total = 0
    for pat in EMOJI_PATTERNS:
        html, n = pat.subn('', html)
        total += n
    if total:
        counts['__emoji__'] = total
    return html


def inject_translator_credit(html: str, counts: dict) -> str:
    """
    在关于页面「工作原理」标题上方注入两行署名。
    所有配置都定义在函数内部，完全自包含。
    """
    # ── 内部配置 ──────────────────────────────────────────────
    translator_name = 'GUST-Chinese'
    translator_url  = 'https://github.com/cjhdevact/GUST-Chinese'
    commit_hash     = COMMIT_HASH   # 从全局读取；若想彻底自包含，改成字符串即可
    # ──────────────────────────────────────────────────────────

    # 已注入过就跳过，防止重复
    if translator_name in html and '提交翻译' in html:
        return html

    line1 = (
        f'由 <a href="{translator_url}" target="_blank" rel="noopener noreferrer" '
        f'style="color:var(--ac);text-decoration:none;">{translator_name}</a> 实现翻译'
    )
    line2 = f'基于 {commit_hash} 提交翻译'

    # 锚点：汉化后的「工作原理」标题 div（含 fa-globe 图标）
    pattern = re.compile(
        r'(<div[^>]*>\s*<i class="fas fa-globe" style="color:var\(--ac\);"></i>\s*工作原理)',
        re.DOTALL
    )

    def _repl(m):
        counts['__translator__'] = counts.get('__translator__', 0) + 1
        block = (
            f'<div style="margin-bottom:2px;">{line1}</div>\n'
            f'                                        '
            f'<div style="margin-bottom:10px;">{line2}</div>\n'
            f'                                        '
        )
        return block + m.group(1)

    return pattern.sub(_repl, html, count=1)


# ═══════════════════════════════════════════════════════════════════
#  主流程
# ═══════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="GUST 浏览器界面汉化 + 去水印 + 去 Emoji 工具")
    ap.add_argument("input", help="输入 HTML 文件")
    ap.add_argument("-o", "--output", help="输出文件（默认覆盖输入并备份 .bak）")
    ap.add_argument("--dry-run", action="store_true", help="仅显示替换统计，不写文件")
    ap.add_argument("--keep-emoji", action="store_true", help="保留 emoji（默认清除）")
    ap.add_argument("--keep-watermark", action="store_true",
                    help="保留主页右下角的水印（默认移除）")
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

    if not args.keep_watermark:
        result = strip_watermark(result, counts)

    if not args.keep_emoji:
        result = strip_emoji(result, counts)

    result = inject_translator_credit(result, counts)

    # ── 报告 ─────────────────────────────────
    print()
    print("=" * 78)
    print(f"  GUST 汉化 + 去水印 + 去 Emoji 报告  ({src.name})")
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

    wm = counts.get('__watermark__', 0)
    if wm:
        total += wm
        print(f"  [OK] {wm:>3}x 水印 <div id=\"gustCredit\"> 已移除")

    if not args.keep_emoji:
        em = counts.get('__emoji__', 0)
        if em:
            total += em
            print(f"  [OK] {em:>3}x Emoji / 装饰性符号已清除")

    tr = counts.get('__translator__', 0)
    if tr:
        total += tr
        print(f"  [OK] {tr:>3}x 翻译者信息已注入「工作原理」上方")

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