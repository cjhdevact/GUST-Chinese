#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUST 浏览器 SVG 版本汉化工具
https://github.com/cjhdevact/GUST-Chinese

适配提交：78df43014334176ca000bb252efc1185beb893a7

用法:
    # 一次处理所有文件
    python GUST-SVG-Chinese.py site.svg static/js.js static/css.css

    # 分别处理
    python GUST-SVG-Chinese.py site.svg
    python GUST-SVG-Chinese.py static/js.js

    # 预览
    python GUST-SVG-Chinese.py site.svg --dry-run

    # 自动扫描
    python GUST-SVG-Chinese.py --auto

    # 保留 emoji
    python GUST-SVG-Chinese.py site.svg --keep-emoji
"""

import re
import sys
import io
import argparse
from pathlib import Path
from collections import OrderedDict

# ── 强制 stdout/stderr 使用 UTF-8（解决 Windows GBK 控制台报 UnicodeEncodeError）──
try:
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
except Exception:
    pass


# ═══════════════════════════════════════════════════════════════════
#  可配置项
# ═══════════════════════════════════════════════════════════════════
COMMIT_HASH = '78df43014334176ca000bb252efc1185beb893a7'

TRANSLATOR_NAME = 'GUST-Chinese'
GITHUB_REPO_URL = 'https://github.com/cjhdevact/GUST-Chinese'
GITHUB_DISPLAY  = 'github.com/cjhdevact/GUST-Chinese'

# 搜索引擎开关
ADD_BAIDU_ENGINE    = True
USE_BING_AS_DEFAULT = True


# ═══════════════════════════════════════════════════════════════════
#  主替换表（HTML + SVG + JS 通用）
# ═══════════════════════════════════════════════════════════════════
REPLACEMENTS = OrderedDict([

    # ═══════════════════════════════════════════════════════════
    #  HTML <title> 与页面标题
    # ═══════════════════════════════════════════════════════════
    ('<title>GUST Browser</title>',         '<title>GUST 浏览器</title>'),
    ('<title>Error - Gust Browser</title>', '<title>错误 - Gust 浏览器</title>'),

    # ═══════════════════════════════════════════════════════════
    #  HTML title="..." 属性
    # ═══════════════════════════════════════════════════════════
    ('title="Scroll tabs left"',            'title="向左滚动标签页"'),
    ('title="Scroll tabs right"',           'title="向右滚动标签页"'),
    ('title="New tab (Ctrl+T)"',            'title="新建标签页 (Ctrl+T)"'),
    ('title="Browser metrics"',             'title="浏览器指标"'),
    ('title="Toggle fullscreen (F11)"',     'title="切换全屏 (F11)"'),
    ('title="Toggle fullscreen (Alt+K / F11)"','title="切换全屏 (Alt+K / F11)"'),
    ('title="Exit fullscreen (F11)"',       'title="退出全屏 (F11)"'),
    ('title="Recent history (Alt+H)"',      'title="最近历史 (Alt+H)"'),
    ('title="Reload (Ctrl+R)"',             'title="刷新 (Ctrl+R)"'),
    ('title="Stop loading"',                'title="停止加载"'),
    ('title="Back"',                        'title="后退"'),
    ('title="Forward"',                     'title="前进"'),
    ('title="Home"',                        'title="主页"'),
    ('title="Search or enter address"',     'title="搜索或输入网址"'),
    ('title="Find in page (Alt+F)"',        'title="在页面中查找 (Alt+F)"'),
    ('title="Bookmark (Ctrl+D)"',           'title="收藏 (Ctrl+D)"'),
    ('title="Bookmark this page (Alt+D)"',  'title="收藏此页 (Alt+D)"'),
    ('title="Remove bookmark (Alt+D)"',     'title="移除收藏 (Alt+D)"'),
    ('title="Go"',                          'title="前往"'),
    ('title="Show bookmarks bar"',          'title="显示书签栏"'),
    ('title="Hide bookmarks bar"',          'title="隐藏书签栏"'),
    ('title="Extensions"',                  'title="扩展"'),
    ('title="Settings"',                    'title="设置"'),
    ('title="Toggle logs (Ctrl+Shift+I)"',  'title="切换日志 (Ctrl+Shift+I)"'),
    ('title="Toggle elements inspector"',   'title="切换元素检查器"'),
    ('title="Toggle GUST Assistant (Alt+A)"','title="切换 GUST 助手 (Alt+A)"'),
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
    ('title="Previous match"',              'title="上一个匹配"'),
    ('title="Next match"',                  'title="下一个匹配"'),
    ('title="Close find bar"',              'title="关闭查找栏"'),
    ('title="Search tabs"',                 'title="搜索标签页"'),
    ('title="GUST Shields"',                'title="GUST 防护"'),
    ('title="Customize and control"',       'title="自定义和控制"'),
    ('title="Menu"',                        'title="菜单"'),
    ('title="You"',                         'title="你"'),
    ('title="Profile"',                     'title="个人资料"'),

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
    ('placeholder="Find in page"',               'placeholder="在页面中查找"'),
    ('placeholder="Search tabs"',                'placeholder="搜索标签页"'),
    ('placeholder="Ask something…"',             'placeholder="问点什么…"'),
    ('placeholder="Ask something..."',           'placeholder="问点什么…"'),
    ('placeholder="Ask somthing…"',              'placeholder="问点什么…"'),

    # ═══════════════════════════════════════════════════════════
    #  顶栏 / 状态
    # ═══════════════════════════════════════════════════════════
    ('>Ready<',                     '>就绪<'),
    ('>Protected<',                 '>已保护<'),
    ('>Disabled<',                  '>已禁用<'),
    ('>Paused<',                    '>已暂停<'),
    ('>New Tab</span>',             '>新标签页</span>'),
    ('>drop to navigate</span>',    '>拖放到此处导航</span>'),
    ('drop to navigate',            '拖放到此处导航'),

    # ═══════════════════════════════════════════════════════════
    #  日志面板
    # ═══════════════════════════════════════════════════════════
    ('>Logs<',                      '>日志<'),
    ('>Logs <',                     '>日志 <'),
    ('>All<',                       '>全部<'),
    ('>All</button>',               '>全部</button>'),
    ('>Info<',                      '>信息<'),
    ('</i> Info<',                  '</i> 信息<'),
    ('>Info</button>',              '>信息</button>'),
    ('>OK<',                        '>成功<'),
    ('</i> OK<',                    '</i> 成功<'),
    ('>OK</button>',                '>成功</button>'),
    ('>Warn<',                      '>警告<'),
    ('</i> Warn<',                  '</i> 警告<'),
    ('>Warn</button>',              '>警告</button>'),
    ('>Err<',                       '>错误<'),
    ('</i> Err<',                   '</i> 错误<'),
    ('>Err</button>',               '>错误</button>'),
    ('>Stream<',                    '>流<'),
    ('</i> Stream<',                '</i> 流<'),
    ('>Stream</button>',            '>流</button>'),
    ('>No matching entries<',       '>无匹配条目<'),
    ('0 requests',                  '0 个请求'),

    # ═══════════════════════════════════════════════════════════
    #  元素检查器
    # ═══════════════════════════════════════════════════════════
    ('>Elements<',                  '>元素<'),
    ('>Styles<',                    '>样式<'),
    ('>Styles</button>',            '>样式</button>'),
    ('>Box<',                       '>盒模型<'),
    ('>Box</button>',               '>盒模型</button>'),
    ('>Attrs<',                     '>属性<'),
    ('>Attrs</button>',             '>属性</button>'),
    ('> Copy Selector<',            '> 复制选择器<'),
    ('</i> Copy Selector</button>', '</i> 复制选择器</button>'),
    ('> Copy HTML<',                '> 复制 HTML<'),
    ('</i> Copy HTML</button>',     '</i> 复制 HTML</button>'),
    ('> Copy Text<',                '> 复制文本<'),
    ('</i> Copy Text</button>',     '</i> 复制文本</button>'),
    ('> Scroll Into View<',         '> 滚动到视图<'),
    ('</i> Scroll Into View</button>','</i> 滚动到视图</button>'),
    ('> Hide Element<',             '> 隐藏元素<'),
    ('</i> Hide Element</button>',  '</i> 隐藏元素</button>'),

    # ═══════════════════════════════════════════════════════════
    #  右键菜单
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
    ('>New Tab</span>',             '>新建标签页</span>'),

    # ═══════════════════════════════════════════════════════════
    #  站点信息弹窗
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
    ('</i> Close<',                 '</i> 关闭<'),

    # ═══════════════════════════════════════════════════════════
    #  广告拦截弹窗
    # ═══════════════════════════════════════════════════════════
    ('>Gust Adblock<',              '>Gust 广告拦截<'),
    ('>Protection Active<',         '>防护已启用<'),
    ('>Protection Disabled<',       '>防护已禁用<'),
    ('>Protection Paused<',         '>防护已暂停<'),
    ('>Paused for this site<',      '>此网站已暂停<'),
    ('>Pause for this site<',       '>对此网站暂停<'),
    ('>Re-enable for this site<',   '>对此网站重新启用<'),
    ('> Manage Filters &amp; Settings <','> 管理过滤器和设置 <'),
    ('> Manage Filters & Settings <','> 管理过滤器和设置 <'),
    ('Manage Filters &amp; Settings','管理过滤器和设置'),
    ('elements blocked on this page','个元素已在此页拦截'),

    # ═══════════════════════════════════════════════════════════
    #  历史记录
    # ═══════════════════════════════════════════════════════════
    ('>Recent History<',            '>最近历史<'),
    ('>Last 20 visited sites<',     '>最近访问的 20 个网站<'),
    ('>No history yet<',            '>暂无历史记录<'),

    # ═══════════════════════════════════════════════════════════
    #  壁纸弹窗
    # ═══════════════════════════════════════════════════════════
    ('>Change background<',         '>更改背景<'),
    ('</i> Random',                 '</i> 随机'),
    ('</i> Upload',                 '</i> 上传'),
    ('>Reset<',                     '>重置<'),
    ('>Cancel<',                    '>取消<'),
    ('>Apply URL<',                 '>应用网址<'),

    # ═══════════════════════════════════════════════════════════
    #  收藏 / 书签弹窗
    # ═══════════════════════════════════════════════════════════
    ('>Add Favorite<',              '>添加收藏<'),
    ('>Add<',                       '>添加<'),
    ('>Add Bookmark<',              '>添加书签<'),
    ('>Save<',                      '>保存<'),
    ('Add favorite',                '添加收藏'),
    ('Add Favorite',                '添加收藏'),
    ('Maximum 5 favorites',         '最多 5 个收藏'),

    # ═══════════════════════════════════════════════════════════
    #  快捷键编辑弹窗
    # ═══════════════════════════════════════════════════════════
    ('>Edit Keyboard Shortcut<',    '>编辑键盘快捷键<'),
    ('>Save Shortcut<',             '>保存快捷键<'),
    ('Press <b>Alt + Key</b> to set the new shortcut.',
                                    '按 <b>Alt + 按键</b> 设置新的快捷键。'),
    ('>Waiting for input...<',      '>等待输入…<'),

    # ═══════════════════════════════════════════════════════════
    #  指标弹窗
    # ═══════════════════════════════════════════════════════════
    ('Browser Metrics',             '浏览器指标'),
    ('>Refresh<',                   '>刷新<'),

    # ═══════════════════════════════════════════════════════════
    #  Find bar
    # ═══════════════════════════════════════════════════════════
    ('Search within the current page','在当前页面中搜索'),
    ('No matches for',               '无匹配：'),
    ('Match',                        '匹配'),

    # ═══════════════════════════════════════════════════════════
    #  设置侧边栏
    # ═══════════════════════════════════════════════════════════
    ('>Skins<',                     '>皮肤<'),
    ('>Connection<',                '>连接<'),
    ('>Connection</span>',          '>连接</span>'),
    ('>AI Assistant<',              '>AI 助手<'),
    ('>Search<',                    '>搜索<'),
    ('>Search</span>',              '>搜索</span>'),
    ('>Privacy<',                   '>隐私<'),
    ('>Privacy</span>',             '>隐私</span>'),
    ('>Files &amp; Media<',         '>文件与媒体<'),
    ('>Files &amp; Media</span>',   '>文件与媒体</span>'),
    ('>Appearance<',                '>外观<'),
    ('>Appearance</span>',          '>外观</span>'),
    ('>Home Screen<',               '>主页<'),
    ('>Home Screen</span>',         '>主页</span>'),
    ('>Shortcuts<',                 '>快捷键<'),
    ('>Shortcuts</span>',           '>快捷键</span>'),
    ('>Language<',                  '>语言<'),
    ('>Language</span>',            '>语言</span>'),
    ('>Fallback<',                  '>回退<'),
    ('>Fallback</span>',            '>回退</span>'),
    ('>Tutorial<',                  '>教程<'),
    ('>Tutorial</span>',            '>教程</span>'),
    ('>About<',                     '>关于<'),
    ('>About</span>',               '>关于</span>'),

    # ═══════════════════════════════════════════════════════════
    #  设置卡片头
    # ═══════════════════════════════════════════════════════════
    ('Fallback WISP Server',        '回退 WISP 服务器'),
    ('WISP Server',                 'WISP 服务器'),
    ('WISP Pool (Round-Robin)',     'WISP 池（轮询）'),
    ('Concurrent Requests',         '并发请求'),
    ('WebRTC Blocking',             'WebRTC 拦截'),
    ('Smart Request Headers',       '智能请求头'),
    ('Default Search Engine',       '默认搜索引擎'),
    ('Custom Search Engine',        '自定义搜索引擎'),
    ('Tab Favicons',                '标签页图标'),
    ('Privacy & Blocking',          '隐私与拦截'),
    ('Privacy &amp; Blocking',      '隐私与拦截'),
    ('User-Agent Spoofing',         'User-Agent 伪装'),
    ('Blocklist & Filters',         '黑名单与过滤器'),
    ('Blocklist &amp; Filters',     '黑名单与过滤器'),
    ('Custom Filter Rules',         '自定义过滤规则'),
    ('Tab Caching',                 '标签页缓存'),
    ('Resource Cache',              '资源缓存'),
    ('Cached Resources',            '已缓存资源'),
    ('Font Size',                   '字体大小'),
    ('Panel Widths',                '面板宽度'),
    ('Panel Position',              '面板位置'),
    ('Fullscreen on Launch',        '启动时全屏'),
    ('Keyboard Shortcuts',          '键盘快捷键'),
    ('Bookmarks Bar',               '书签栏'),
    ('New Tab Wallpaper',           '新标签页壁纸'),
    ('Home Page Clock',             '主页时钟'),
    ('Interactive Tour',            '交互式导览'),
    ('About Gust',                  '关于 Gust'),
    ('Fallback Behaviour',          '回退行为'),
    ('Retry Policy',                '重试策略'),
    ('Error Triggers',              '错误触发条件'),
    ('Advanced Rendering',          '高级渲染'),
    ('Media Range Requests',        '媒体范围请求'),
    ('Unknown File Types',          '未知文件类型'),
    ('PDF Viewer',                  'PDF 查看器'),
    ('Image Viewer',                '图片查看器'),
    ('Video Player',                '视频播放器'),
    ('Audio Player',                '音频播放器'),
    ('Text / Code Viewer',          '文本 / 代码查看器'),
    ('Paused Sites (Allowlist)',    '暂停站点（白名单）'),
    ('Browser Skin',                '浏览器皮肤'),
    ('Identity',                    '身份'),
    ('Opera GX Extras',             'Opera GX 附加功能'),
    ('GUST+ Studio',                'GUST+ 工作室'),
    ('GUST+ Toolbar &amp; Modules', 'GUST+ 工具栏与模块'),
    ('GUST+ Toolbar & Modules',     'GUST+ 工具栏与模块'),
    ('GUST+ Color Lab',             'GUST+ 颜色实验室'),
    ('GUST+ Shape &amp; Type',      'GUST+ 形状与字体'),
    ('GUST+ Shape & Type',          'GUST+ 形状与字体'),
    ('Provider',                    '提供商'),
    ('Context',                     '上下文'),

    # Spellcheck 标题（含 [broken] 标签）
    (' Spellcheck <span style="font-size:10px;font-weight:700;color:#ff4444;margin-left:4px;">[broken]</span>',
     ' 拼写检查 <span style="font-size:10px;font-weight:700;color:#ff4444;margin-left:4px;">[已损坏]</span>'),
    ('>Spellcheck<',                '>拼写检查<'),
    ('>Spellcheck <',               '>拼写检查 <'),
    ('[broken]',                    '[已损坏]'),

    # ═══════════════════════════════════════════════════════════
    #  关于页面标题（Credits 用 </i> 前缀匹配）
    # ═══════════════════════════════════════════════════════════
    ('>How it works<',              '>工作原理<'),
    ('>Page rendering<',            '>页面渲染<'),
    ('>Privacy &amp; limitations<', '>隐私与限制<'),
    ('>Privacy & limitations<',     '>隐私与限制<'),
    ('</i> Credits',                '</i> 致谢'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 危险按钮
    # ═══════════════════════════════════════════════════════════
    ('</i> Clear Cache',            '</i> 清空缓存'),
    ('</i> Reset All',              '</i> 全部重置'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 连接页
    # ═══════════════════════════════════════════════════════════
    ('>WebSocket URL<',             '>WebSocket 地址<'),
    ('Current server shown above',  '当前服务器显示在上方'),
    ('Enable pool round-robin',     '启用池轮询'),
    ('Not benchmarked yet',         '尚未基准测试'),
    ('Idle threads',                '空闲线程'),
    ('Active threads',              '活跃线程'),
    ('Max simultaneous requests when page is loaded (default: 3). Lower = less background CPU.',
                                    '页面加载完成后的最大并发请求数（默认：3）。数值越低，后台 CPU 占用越少。'),
    ('Max simultaneous requests during page load (default: 6). Higher = faster loads but more CPU.',
                                    '页面加载期间的最大并发请求数（默认：6）。数值越高加载越快，但 CPU 占用更多。'),
    ('Block WebRTC connections',    '拦截 WebRTC 连接'),
    ('Prevents sites from establishing direct peer-to-peer connections that bypass the WISP tunnel and could expose your real IP address. Off by default — may break video calls and real-time apps.',
                                    '阻止网站建立绕过 WISP 隧道的直接点对点连接（可能暴露你的真实 IP）。默认关闭 — 开启后可能导致视频通话和实时应用失效。'),
    ('Spoof Sec-Fetch &amp; Referer headers', '伪造 Sec-Fetch 与 Referer 请求头'),
    ('Spoof Sec-Fetch & Referer headers',     '伪造 Sec-Fetch 与 Referer 请求头'),
    ('Synthesize correct <code>Sec-Fetch-Site</code>, <code>Sec-Fetch-Mode</code>, <code>Sec-Fetch-Dest</code>, and <code>Referer</code> headers based on request context. Fixes CDNs and APIs that reject requests with incorrect fetch metadata.',
                                    '根据请求上下文合成正确的 <code>Sec-Fetch-Site</code>、<code>Sec-Fetch-Mode</code>、<code>Sec-Fetch-Dest</code> 和 <code>Referer</code> 请求头。修复因 fetch 元数据不正确而拒绝请求的 CDN 和 API。'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - AI 助手
    # ═══════════════════════════════════════════════════════════
    ('Page context by default',     '默认使用页面上下文'),
    ('Automatically enable Page Context when the assistant opens.',
                                    '打开助手时自动启用页面上下文。'),
    ('GUST Assistant <span style="font-size:10px;font-weight:700;color:#ff4444;margin-left:4px;">[experimental]</span>',
     'GUST 助手 <span style="font-size:10px;font-weight:700;color:#ff4444;margin-left:4px;">[实验性]</span>'),
    ("Ask questions about the page you're browsing, get help with site content, or just chat.",
     '就你正在浏览的页面提问、获取站点内容帮助，或者只是聊天。'),
    ('>GUST Assistant</h3>',        '>GUST 助手</h3>'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 搜索页
    # ═══════════════════════════════════════════════════════════
    ('Engine Name',                 '引擎名称'),
    ('Search URL',                  '搜索网址'),
    ('Display name for the custom engine in the picker.',
                                    '自定义搜索引擎在选择器中的显示名称。'),
    ('Use <code>{q}</code> as the query placeholder. Only used when <strong>Custom</strong> engine is selected.',
                                    '使用 <code>{q}</code> 作为查询占位符。仅在选中 <strong>自定义</strong> 引擎时使用。'),
    ('Enable spellcheck',           '启用拼写检查'),
    ('Check spelling in text fields and textareas (e.g. search bar, forms).',
                                    '在输入框和文本域中检查拼写（如搜索栏、表单）。'),
    ('Proxy favicons through WISP', '通过 WISP 代理图标'),
    ("Fetch tab favicons through the WISP server instead of Google's favicon service. More private, but slightly slower.",
                                    '通过 WISP 服务器获取标签页图标，而不是使用 Google 的图标服务。更私密，但略慢。'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 隐私页
    # ═══════════════════════════════════════════════════════════
    ('Ad &amp; Tracker Blocking',   '广告与跟踪器拦截'),
    ('Ad & Tracker Blocking',       '广告与跟踪器拦截'),
    ('Blocks analytics, ads, and tracking scripts',
                                    '拦截分析、广告和跟踪脚本'),
    ('Adblock is paused on these sites. One hostname per line. Use "Pause for this site" in the shield popup to add sites.',
                                    '广告拦截在这些站点上暂停。每行一个主机名。可在盾牌弹窗中使用「对此网站暂停」来添加站点。'),
    ('Request User-Agent',          '请求 User-Agent'),
    ('Sent as the <code>User-Agent</code> HTTP header for all proxied requests.',
                                    '作为所有代理请求的 <code>User-Agent</code> HTTP 请求头发送。'),
    ('Page navigator.userAgent',    '页面 navigator.userAgent'),
    ('Overrides <code>navigator.userAgent</code> inside loaded pages.',
                                    '覆盖加载页面内的 <code>navigator.userAgent</code>。'),
    ('Enter CSS selectors to hide (one per line).',
                                    '输入要隐藏的 CSS 选择器（每行一个）。'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 缓存页
    # ═══════════════════════════════════════════════════════════
    ('Keep tabs loaded in background','在后台保持标签页加载'),
    ("When enabled, switching between tabs won't reload them. Disable to save memory.",
                                    '启用后，切换标签页不会重新加载。关闭可节省内存。'),
    ('Calculating...',              '计算中…'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 外观页
    # ═══════════════════════════════════════════════════════════
    ('Adjust text size across the entire interface',
                                    '调整整个界面的文字大小'),
    ('Remember panel widths',       '记住面板宽度'),
    ('When enabled, panel widths are saved. When disabled, they reset to default on close.',
                                    '启用后，面板宽度会被保存。关闭后，关闭时重置为默认值。'),
    ('When enabled, panel widths are saved. When , they reset to default on close.',
                                    '启用后，面板宽度会被保存。关闭后，关闭时重置为默认值。'),
    ('Panels on the left',          '面板位于左侧'),
    ('Move side panels to the left side of the browser window instead of the right.',
                                    '将侧边面板移到浏览器窗口左侧。'),
    ('Move the Logs and Elements panels to the left side of the browser window instead of the right.',
                                    '将日志和元素面板移到浏览器窗口左侧。'),
    ('Start in fullscreen',         '启动进入全屏'),
    ('Automatically enter fullscreen on your first click or keypress after opening Gust.',
                                    '打开 Gust 后，首次点击或按键时自动进入全屏。'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 皮肤页
    # ═══════════════════════════════════════════════════════════
    ('Disguise GUST as another browser. Tabs, toolbar, menus and browser-specific extras are all re-dressed to match the real thing.',
                                    '将 GUST 伪装成其他浏览器。标签页、工具栏、菜单和浏览器特有的附加功能都会重新打扮以匹配真实产品。'),
    ('Match User-Agent to skin',    'User-Agent 与皮肤匹配'),
    ('UI sound effects',            '界面音效'),
    ('Color theme',                 '颜色主题'),
    ('Tab strip',                   '标签栏'),
    ('Toolbar',                     '工具栏'),
    ('Address bar',                 '地址栏'),
    ('Browser menu',                '浏览器菜单'),
    ('Home screen',                 '主页'),
    ('Sidebar',                     '侧边栏'),
    ('Preset',                      '预设'),
    ('Copy',                        '复制'),
    ('Paste',                       '粘贴'),
    ('Reset everything',            '重置全部'),
    ('Core palette',                '核心调色板'),
    ('Borrowed-part colors',        '借用部件的颜色'),
    ('Show all',                    '显示全部'),
    ('Reset colors',                '重置颜色'),
    ('Corner radius',               '圆角半径'),
    ('Density',                     '密度'),
    ('Tab width',                   '标签宽度'),
    ('Font size',                   '字体大小'),
    ('UI font',                     '界面字体'),
    ('Address bar hint',            '地址栏提示'),

    # ═══════════════════════════════════════════════════════════
    #  GUST+ 模块名列表
    # ═══════════════════════════════════════════════════════════
    ("'Menu button (⋮)'",           "'菜单按钮 (⋮)'"),
    ("'Profile avatar'",            "'个人资料头像'"),
    ("'Extensions button'",         "'扩展按钮'"),
    ("'Tab search (Chrome)'",       "'标签页搜索 (Chrome)'"),
    ("'Shields chip (Brave)'",      "'防护标签 (Brave)'"),
    ("'Rewards triangle (Brave)'",  "'奖励三角 (Brave)'"),
    ("'Shields toolbar button'",    "'防护工具栏按钮'"),
    ("'O-menu button (Opera GX)'",  "'O 菜单按钮 (Opera GX)'"),
    ("'Back button'",               "'后退按钮'"),
    ("'Forward button'",            "'前进按钮'"),
    ("'Reload button'",             "'刷新按钮'"),
    ("'Home button'",               "'主页按钮'"),
    ("'Security chip'",             "'安全标签'"),
    ("'Bookmark star'",             "'书签星标'"),
    ("'Find-in-page button'",       "'页面查找按钮'"),
    ("'Go arrow'",                  "'前往箭头'"),
    ("'History button'",            "'历史按钮'"),
    ("'Fullscreen button'",         "'全屏按钮'"),
    ("'Metrics button'",            "'指标按钮'"),
    ("'Settings gear'",             "'设置齿轮'"),
    ("'Dev-logs button'",           "'开发日志按钮'"),
    ("'Inspector button'",          "'检查器按钮'"),
    ("'AI assistant button'",       "'AI 助手按钮'"),
    ("'Adblock pill'",              "'广告拦截胶囊'"),
    ("'Status pill'",               "'状态胶囊'"),
    ("'Tab hover cards (Chrome)'",  "'标签悬停卡片 (Chrome)'"),
    ("'UI sound effects (Opera GX)'", "'界面音效 (Opera GX)'"),
    ("'Background music (Opera GX)'", "'背景音乐 (Opera GX)'"),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 快捷键页
    # ═══════════════════════════════════════════════════════════
    ('Enable keyboard shortcuts',   '启用键盘快捷键'),
    ('When off, all Alt + key shortcuts are disabled.',
                                    '关闭后，所有 Alt + 按键快捷键都将禁用。'),
    ('When off, all Alt + key shortcuts are .',
                                    '关闭后，所有 Alt + 按键快捷键都将禁用。'),
    ('>Reload Page</span>',         '>刷新页面</span>'),
    ('>Focus URL Bar</span>',       '>聚焦地址栏</span>'),
    ('>Toggle Logs</span>',         '>切换日志</span>'),
    ('>Element Inspector</span>',   '>元素检查器</span>'),
    ('>Metrics</span>',             '>指标</span>'),
    ('>Toggle Fullscreen</span>',   '>切换全屏</span>'),
    ('>Find in Page</span>',        '>在页面中查找</span>'),
    ('>AI Assistant</span>',        '>AI 助手</span>'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 主页
    # ═══════════════════════════════════════════════════════════
    ('Show Bookmarks Bar',          '显示书签栏'),
    ('Always show the bookmarks bar below the address bar',
                                    '始终在地址栏下方显示书签栏'),
    ('Background image',            '背景图片'),
    ('Show clock on new tab',       '在新标签页上显示时钟'),
    ('Display current time and date on the home screen',
                                    '在主页上显示当前时间和日期'),
    ('24-hour clock',               '24 小时制'),
    ('Show time in 24-hour format (e.g. 14:30 instead of 2:30 PM)',
                                    '以 24 小时制显示时间（例如 14:30 而非 2:30 PM）'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 语言
    # ═══════════════════════════════════════════════════════════
    ('Preferred language',          '首选语言'),
    ('Choose the language for the interface and spellcheck when supported.',
                                    '选择界面和拼写检查所用的语言（若支持）。'),
    ('System default',              '系统默认'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 教程页
    # ═══════════════════════════════════════════════════════════
    ('Walk through 18 steps covering navigation, search, bookmarks, ad blocking, metrics, browser logs, page inspector, tabs, and the new tab page. Takes under a minute.',
                                    '用 18 个步骤带你了解导航、搜索、书签、广告拦截、指标、浏览器日志、页面检查器、标签页和新标签页。不到一分钟。'),
    ('Walk through 16 steps covering navigation, search, bookmarks, ad blocking, metrics, browser logs, page inspector, tabs, and the new tab page. Takes under a minute.',
                                    '用 16 个步骤带你了解导航、搜索、书签、广告拦截、指标、浏览器日志、页面检查器、标签页和新标签页。不到一分钟。'),
    ('Under a minute',              '不到一分钟'),
    ('Start Tour',                  '开始导览'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 回退
    # ═══════════════════════════════════════════════════════════
    ('Enable fallback on load error','加载失败时启用回退'),
    ('When a page fails to load (network error, bad status, timeout), automatically retry using the fallback proxy before showing an error page.',
                                    '页面加载失败时（网络错误、状态码异常、超时），在显示错误页面前自动使用回退代理重试。'),
    ('Log retries',                 '记录重试'),
    ('All fallback retry attempts are always written to the request log, including which WISP server was used.',
                                    '所有回退重试都会记录到请求日志中，包括使用的是哪个 WISP 服务器。'),
    ('always on',                   '始终开启'),
    ('Fallback WebSocket URL',      '回退 WebSocket 地址'),
    ('Used only when the primary WISP server is unreachable or returns an error. Leave blank to disable.',
                                    '仅当主 WISP 服务器无法访问或返回错误时使用。留空则禁用。'),
    ('Max retry attempts (main)',   '最大重试次数（主）'),
    ('How many times Gust retries on the primary WISP server before switching to the fallback.',
                                    '切换到回退服务器前在主 WISP 服务器上重试的次数。'),
    ('Max retry attempts (fallback)','最大重试次数（回退）'),
    ('How many times Gust will attempt the fallback WISP before giving up and showing an error.',
                                    '显示错误前在回退 WISP 上尝试的次数。'),
    ('Retry delay (seconds)',       '重试延迟（秒）'),
    ('Wait time between each retry attempt before switching to the fallback server.',
                                    '切换到回退服务器前，每次重试之间的等待时间。'),
    ('Fallback on HTTP 5xx errors', 'HTTP 5xx 错误时回退'),
    ('Retry via fallback when the origin server returns a 500-level status code.',
                                    '源服务器返回 5xx 状态码时通过回退重试。'),
    ('Fallback on timeout',         '超时时回退'),
    ('Retry via fallback when the primary server exceeds the connection timeout.',
                                    '主服务器连接超时时通过回退重试。'),
    ('Fallback on DNS failure',     'DNS 失败时回退'),
    ('Retry via fallback when the hostname cannot be resolved.',
                                    '主机名无法解析时通过回退重试。'),

    # ═══════════════════════════════════════════════════════════
    #  设置 - 文件与媒体
    # ═══════════════════════════════════════════════════════════
    ('Script tags loaded per page', '每页加载的脚本标签数'),
    ('Images prefetched per page',  '每页预取的图片数'),
    ('Enable Range request support','启用 Range 请求支持'),
    ('Forward <code>Range</code> headers and handle <code>206 Partial Content</code> responses. Fixes video/audio seeking and embedded media playback on most sites.',
                                    '转发 <code>Range</code> 请求头并处理 <code>206 Partial Content</code> 响应。修复大多数网站上的视频/音频拖动和嵌入式媒体播放。'),
    ('Auto-download unknown files', '自动下载未知文件'),
    ("When Gust receives a file it can't display (e.g. .zip, .exe), automatically trigger a browser download instead of showing an error page.",
                                    '当 Gust 收到无法显示的文件（如 .zip、.exe）时，自动触发浏览器下载，而不是显示错误页。'),
    ('Built-in PDF viewer',         '内置 PDF 查看器'),
    ('Render PDF files inline using a built-in viewer powered by PDF.js instead of downloading them.',
                                    '使用基于 PDF.js 的内置查看器内联渲染 PDF 文件，而不是下载它们。'),
    ('Built-in image viewer',       '内置图片查看器'),
    ('Display images (PNG, JPEG, GIF, WebP, SVG…) in a clean fullscreen viewer with zoom and pan.',
                                    '在简洁的全屏查看器中显示图片（PNG、JPEG、GIF、WebP、SVG…），支持缩放和平移。'),
    ('Built-in video player',       '内置视频播放器'),
    ('Play video files (MP4, WebM, OGG…) in a built-in player with controls.',
                                    '使用内置播放器播放视频文件（MP4、WebM、OGG…），带控制栏。'),
    ('Built-in audio player',       '内置音频播放器'),
    ('Play audio files (MP3, OGG, FLAC, WAV…) in a styled player instead of downloading.',
                                    '使用样式化的播放器播放音频文件（MP3、OGG、FLAC、WAV…），而不是下载。'),
    ('Built-in text viewer',        '内置文本查看器'),
    ('Display plain text, JSON, XML, CSV, and source code files inline with syntax-aware formatting.',
                                    '内联显示纯文本、JSON、XML、CSV 和源代码文件，并带语法感知格式化。'),

    # ═══════════════════════════════════════════════════════════
    #  教程弹窗按钮
    # ═══════════════════════════════════════════════════════════
    ('>Skip tour<',                 '>跳过导览<'),
    ('>Skip tour</button>',         '>跳过导览</button>'),
    ('>Next<',                      '>下一步<'),
    ('>Next</button>',              '>下一步</button>'),
    ('>Back<',                      '>上一步<'),
    ('>Back</button>',              '>上一步</button>'),
    ("</i>Done'",                   "</i>完成'"),
    ("'Next <i class=\"fas fa-arrow-right\"></i>'",
                                    "'下一步 <i class=\"fas fa-arrow-right\"></i>'"),

    # ═══════════════════════════════════════════════════════════
    #  教程弹窗标题
    # ═══════════════════════════════════════════════════════════
    ("title: 'Welcome to GUST'",            "title: '欢迎使用 GUST'"),
    ("title: 'Navigation Buttons'",         "title: '导航按钮'"),
    ("title: 'Address and Search Bar'",     "title: '地址与搜索栏'"),
    ("title: 'Find in Page'",               "title: '在页面中查找'"),
    ("title: 'Bookmarks'",                  "title: '书签'"),
    ("title: 'Recent History'",             "title: '最近历史'"),
    ("title: 'Ad and Tracker Blocking'",    "title: '广告与跟踪器拦截'"),
    ("title: 'Browser Logs'",               "title: '浏览器日志'"),
    ("title: 'Page Inspector'",             "title: '页面检查器'"),
    ("title: 'GUST Assistant'",             "title: 'GUST 助手'"),
    ("title: 'New Tab'",                    "title: '新建标签页'"),
    ("title: 'Settings'",                   "title: '设置'"),
    ("title: 'Change Wallpaper'",           "title: '更改壁纸'"),
    ("title: 'Extensions'",                 "title: '扩展'"),
    ("title: \"You're all set!\"",          "title: '大功告成！'"),

    # ═══════════════════════════════════════════════════════════
    #  教程正文
    # ═══════════════════════════════════════════════════════════
    ("A fast, private browser by Nautilus Labs. This tour covers all the key controls and takes under a minute, and can be restarted anytime from Settings.",
     'Nautilus Labs 出品的快速、私密浏览器。本导览涵盖所有关键控件，不到一分钟即可完成，随时可从设置中重新开始。该版本由 CJH 翻译。'),
    ("Back (<i class=\"fas fa-arrow-left\" style=\"font-size:0.8em;\"></i>), forward (<i class=\"fas fa-arrow-right\" style=\"font-size:0.8em;\"></i>), reload and home. The home button returns to the new tab page, and you can pause a page reloading by clicking the square in its place.",
     '后退、前进、刷新和主页。主页按钮返回新标签页，点击方形按钮可暂停页面重新加载。'),
    ("Type a URL or search term and press Enter. The lock icon shows connection security, and clicking on it shows site info. The bookmark icon saves the current page instantly.",
     '输入网址或搜索词后按回车。锁形图标显示连接安全性，点击可查看站点信息。书签图标可立即收藏当前页面。'),
    ("Search for text on the active page. Toggle the find bar with this button, Alt+F, or Ctrl+F. You can go to the next or previous match using the arrow buttons or Enter/Shift+Enter.",
     '在当前页面中搜索文本。使用此按钮、Alt+F 或 Ctrl+F 切换查找栏。可以使用箭头按钮或 Enter/Shift+Enter 转到下一个或上一个匹配项。'),
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
    ("Pin your most-visited sites as favorites on the new tab page for instant access. You can add up to 5. Discord Anywhere — a full Discord client built into GUST — comes pinned by default.",
     '将最常访问的网站固定为新标签页上的收藏，方便快速访问。最多可添加 5 个。GUST 内置的 Discord Anywhere 客户端已默认固定。'),
    ("Pin your most-visited sites as favorites on the new tab page for instant access. You can add up to 5.",
     '将最常访问的网站固定为新标签页上的收藏，方便快速访问。最多可添加 5 个。'),
    ("Customize the new tab page background. Upload any image, use a random stock image, paste an image URL, or reset to the default gradient.",
     '自定义新标签页背景。可上传任意图片、使用随机库存图片、粘贴图片网址，或重置为默认渐变。'),
    ("GUST is open source. Click to view the repository, report issues, or contribute.",
     'GUST 是开源的。点击查看仓库、报告问题或贡献代码。'),
    ("That's the full tour! GUST is made with lots of love by the Nautilus Labs dev team, and we'd be overjoyed if you gave our repository a star on GitHub. Enjoy the experience!",
     '导览到此结束！GUST 由 Nautilus Labs 开发团队倾心打造，如果你能在 GitHub 上给我们的仓库点个星，我们会非常开心。祝你使用愉快！'),
    ("Access the extensions menu to manage installed add-ons, launch extension popups, and install new ones from the built-in store.",
     '打开扩展按钮以管理已安装的附加组件、启动扩展弹窗，并从内置商店安装新扩展。'),
    ("Open the extensions button to manage installed add-ons, launch extension popups, and install new ones from the built-in store.",
     '打开扩展按钮以管理已安装的附加组件、启动扩展弹窗，并从内置商店安装新扩展。'),
    ("Opens the AI sidebar. Ask questions about the current page, or just use it like a normal AI chatbot.",
     '打开 AI 侧边栏。可以就当前页面提问，也可以像普通 AI 聊天机器人一样使用。'),

    # ═══════════════════════════════════════════════════════════
    #  JS 字符串 - 状态 / 通用
    # ═══════════════════════════════════════════════════════════
    ('"Ready"',                     '"就绪"'),
    ('"Protected"',                 '"已保护"'),
    ('"Disabled"',                  '"已禁用"'),
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
    ("'Starting...'",               "'正在启动…'"),
    ('"Cache initialized"',         '"缓存已初始化"'),
    ("'Cache initialized'",         "'缓存已初始化'"),
    ('"Page ready"',                '"页面就绪"'),
    ('"Logs cleared"',              '"日志已清空"'),
    ('"Logs copied to clipboard"',  '"日志已复制到剪贴板"'),
    ('"Custom filters saved"',      '"自定义过滤器已保存"'),
    ('"Failed to save filters"',    '"保存过滤器失败"'),
    ('"Browser reset initiated..."','"浏览器重置已开始…"'),
    ('"URL copied to clipboard"',   '"网址已复制到剪贴板"'),
    ('"Failed to copy URL"',        '"复制网址失败"'),
    ('"Cache cleared"',             '"缓存已清空"'),
    ('"Invalid URL"',               '"无效网址"'),

    # ═══════════════════════════════════════════════════════════
    #  JS - 错误类型
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
    ('"Protection Disabled"',       '"防护已禁用"'),
    ('"Protection Paused"',         '"防护已暂停"'),
    ('"Paused for this site"',      '"此网站已暂停"'),
    ("'Pause for this site'",       "'对此网站暂停'"),
    ("'Re-enable for this site'",   "'对此网站重新启用'"),
    ("'Protection Active'",         "'防护已启用'"),
    ("'Protection Disabled'",       "'防护已禁用'"),
    ("'Protection Paused'",         "'防护已暂停'"),
    ("'Paused for this site'",      "'此网站已暂停'"),
    ("'Protected'",                 "'已保护'"),
    ("'Disabled'",                  "'已禁用'"),
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
    ('"Bookmark this page (Alt+D)"','"收藏此页 (Alt+D)"'),
    ('"Remove bookmark (Alt+D)"',   '"移除收藏 (Alt+D)"'),
    ("'Auto-scroll on'",            "'自动滚动已开'"),
    ("'Auto-scroll off'",           "'自动滚动已关'"),
    ("'Unmute tab'",                "'取消静音'"),
    ("'Mute tab'",                  "'静音标签页'"),
    ('"Add Bookmark"',              '"添加书签"'),
    ('"Add favorite"',              '"添加收藏"'),
    ('"Maximum 5 favorites"',       '"最多 5 个收藏"'),

    # ═══════════════════════════════════════════════════════════
    #  JS - 日志消息
    # ═══════════════════════════════════════════════════════════
    ("'WISP connection lost, reconnecting...'", "'WISP 连接断开，正在重连…'"),
    ("'WISP reconnect failed after 3 attempts: '", "'WISP 重连 3 次失败: '"),
    ("'WISP reconnect attempt '",   "'WISP 第 '"),
    ("' failed, retrying...'",      "' 次重连失败，重试中…'"),
    ("'Reconnected to WISP (attempt '", "'已重连 WISP（第 '"),
    ('WISP switched to <span',      'WISP 已切换到 <span'),
    ("'WISP switched to '",         "'WISP 已切换到 '"),
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
    ("'Offline'",                   "'离线'"),
    ("'Network offline detected'",  "'检测到网络离线'"),
    ("'Network online'",            "'网络已连接'"),

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
    ('"No recent history"',         '"无最近历史"'),

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
    ("' domains ('",                "' 个域名 ('"),
    ("' cookies)'",                 "' 个 Cookie)'"),

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
    ('>Try these steps<',           '>请尝试以下步骤<'),
    ('> Reload Page <',             '> 重新加载 <'),
    ('> Open Logs <',               '> 打开日志 <'),
    ('> Reload Page</button>',      '> 重新加载</button>'),
    ('> Go Back</button>',          '> 返回</button>'),
    ('> Open Logs</button>',        '> 打开日志</button>'),
    ('>Uh oh!<',                    '>哎呀！<'),
    ('libcurl failed to initialize: ', 'libcurl 初始化失败: '),
    ('Waiting for user to choose how to proceed...', '等待用户选择如何继续…'),
    ('Continuing in limited mode (falling back to native fetch)',
                                    '继续以受限模式运行（回退到原生 fetch）'),
    ('>Continue anyways<',          '>仍然继续<'),
    ('>Continue anyways</button>',  '>仍然继续</button>'),

    # ═══════════════════════════════════════════════════════════
    #  设置页标签标题
    # ═══════════════════════════════════════════════════════════
    ('Settings - ${',               '设置 - ${'),
    ('`Settings - ',                '`设置 - '),
    ('Settings - Connection',       '设置 - 连接'),
    ('Settings - Search',           '设置 - 搜索'),
    ('Settings - Privacy',          '设置 - 隐私'),
    ('Settings - Cache',            '设置 - 缓存'),
    ('Settings - Appearance',       '设置 - 外观'),
    ('Settings - Skins',            '设置 - 皮肤'),
    ('Settings - Homescreen',       '设置 - 主页'),
    ('Settings - Shortcuts',        '设置 - 快捷键'),
    ('Settings - Language',         '设置 - 语言'),
    ('Settings - Fallback',         '设置 - 回退'),
    ('Settings - Tutorial',         '设置 - 教程'),
    ('Settings - About',            '设置 - 关于'),
    ('Settings - Filesandmedia',    '设置 - 文件与媒体'),
    ('Settings - Aiassistant',      '设置 - AI 助手'),

    # ═══════════════════════════════════════════════════════════
    #  皮肤菜单（Chrome / Brave / Firefox / Opera GX / Zen）
    # ═══════════════════════════════════════════════════════════
    ("'New tab'",                   "'新建标签页'"),
    ("'New window'",                "'新建窗口'"),
    ("'New Incognito window'",      "'新建无痕窗口'"),
    ("'New private window'",        "'新建隐私窗口'"),
    ("'Your Chrome'",               "'你的 Chrome'"),
    ("'Not signed in'",             "'未登录'"),
    ("'Sign in to Chrome'",         "'登录 Chrome'"),
    ("'Sign in to Firefox'",        "'登录 Firefox'"),
    ("'Passwords and autofill'",    "'密码和自动填充'"),
    ("'Google Password Manager'",   "'Google 密码管理器'"),
    ("'Payment methods'",           "'付款方式'"),
    ("'Addresses and more'",        "'地址和更多'"),
    ("'History'",                   "'历史记录'"),
    ("'Recent'",                    "'最近'"),
    ("'Downloads'",                 "'下载'"),
    ("'Bookmarks and lists'",       "'书签和列表'"),
    ("'Bookmark this tab'",         "'收藏此标签页'"),
    ("'Show bookmarks bar'",        "'显示书签栏'"),
    ("'Tab groups'",                "'标签页分组'"),
    ("'No open tab groups'",        "'没有打开的标签页分组'"),
    ("'Extensions'",                "'扩展'"),
    ("'Manage extensions'",         "'管理扩展'"),
    ("'Visit Chrome Web Store'",    "'访问 Chrome 应用商店'"),
    ("'Delete browsing data...'",   "'删除浏览数据...'"),
    ("'Print...'",                  "'打印...'"),
    ("'Search this tab with Google Lens'", "'使用 Google Lens 搜索此标签页'"),
    ("'Translate...'",              "'翻译...'"),
    ("'Find and edit'",             "'查找和编辑'"),
    ("'Find...'",                   "'查找...'"),
    ("'Copy URL'",                  "'复制网址'"),
    ("'Cast, save, and share'",     "'投射、保存和分享'"),
    ("'Cast...'",                   "'投射...'"),
    ("'Save page as...'",           "'页面另存为...'"),
    ("'Copy link'",                 "'复制链接'"),
    ("'Share...'",                  "'分享...'"),
    ("'More tools'",                "'更多工具'"),
    ("'GUST Assistant'",            "'GUST 助手'"),
    ("'Name window...'",            "'重命名窗口...'"),
    ("'Task manager'",              "'任务管理器'"),
    ("'Developer tools'",           "'开发者工具'"),
    ("'Help'",                      "'帮助'"),
    ("'About Google Chrome'",       "'关于 Google Chrome'"),
    ("\"What's new\"",              "'新功能'"),
    ("'Report an issue'",           "'报告问题'"),
    ("'Settings'",                  "'设置'"),
    ("'Exit'",                      "'退出'"),
    ("'Quit'",                      "'退出'"),
    ("'Brave Shields'",             "'Brave 防护'"),
    ("'Brave Wallet'",              "'Brave 钱包'"),
    ("'Brave Rewards'",             "'Brave 奖励'"),
    ("'Customize profile'",         "'自定义个人资料'"),
    ("'Add profile'",               "'添加个人资料'"),
    ("'Add Chrome profile'",        "'添加 Chrome 个人资料'"),
    ("'Open Guest profile'",        "'打开访客个人资料'"),
    ("'Manage Chrome profiles'",    "'管理 Chrome 个人资料'"),
    ("'Manage add-ons'",            "'管理附加组件'"),
    ("'Visit addons.mozilla.org'",  "'访问 addons.mozilla.org'"),
    ("'Add-ons and themes'",        "'附加组件和主题'"),
    ("'Customize toolbar...'",      "'自定义工具栏...'"),
    ("'About Firefox'",             "'关于 Firefox'"),
    ("'Report broken site...'",     "'报告损坏的网站...'"),
    ("'GX Corner'",                 "'GX 角落'"),
    ("'GX Control'",                "'GX 控制'"),
    ("'Easy setup'",                "'简易设置'"),
    ("'GX Player'",                 "'GX 播放器'"),
    ("'About Opera GX'",            "'关于 Opera GX'"),
    ("'About GUST'",                "'关于 GUST'"),
    ("'Skins'",                     "'皮肤'"),
    ("'Customize Chrome'",          "'自定义 Chrome'"),
    ("'Google apps'",               "'Google 应用'"),
    ("'Search by voice'",           "'语音搜索'"),
    ("'Search by image'",           "'以图搜图'"),
    ("'Gmail'",                     "'Gmail'"),
    ("'Images'",                    "'图片'"),
    ("'Add shortcut'",              "'添加快捷方式'"),
    ("'Add site'",                  "'添加网站'"),
    ("'Add to GUST'",               "'添加到 GUST'"),
    ("'Remove from GUST'",          "'从 GUST 移除'"),
    ("'Remove'",                    "'移除'"),
    ("'Adding to GUST…'",           "'正在添加到 GUST…'"),
    ("'Added to GUST'",             "'已添加到 GUST'"),
    ("'Removing…'",                 "'正在移除…'"),
    ("'New Space'",                 "'新建空间'"),
    ("'Space'",                     "'空间'"),
    ("'Done'",                      "'完成'"),
    ("'Rename'",                    "'重命名'"),
    ("'Delete'",                    "'删除'"),
    ("'Toggle compact mode'",       "'切换紧凑模式'"),
    ("'Enable compact mode'",       "'启用紧凑模式'"),
    ("'New Tab Below'",             "'在下方新建标签页'"),
    ("'Add split view...'",         "'添加分屏视图...'"),
    ("'Reload Tab'",                "'刷新标签页'"),
    ("'Add to Essentials'",         "'添加到 Essentials'"),
    ("'Duplicate Tab'",             "'复制标签页'"),
    ("'Bookmark Tab...'",           "'收藏标签页...'"),
    ("'Move to Space'",             "'移动到空间'"),
    ("'Close Tab'",                 "'关闭标签页'"),
    ("'Reload Selected Tab'",       "'刷新选中的标签页'"),
    ("'Bookmark Selected Tab...'",  "'收藏选中的标签页...'"),
    ("'Tabs on the right'",         "'标签页靠右'"),
    ("'Edit Theme...'",             "'编辑主题...'"),
    ("'Sync and save data'",        "'同步并保存数据'"),
    ("'Sign In'",                   "'登录'"),
    ("'New blank window'",          "'新建空白窗口'"),
    ("'Passwords'",                 "'密码'"),
    ("'Extensions and Themes'",     "'扩展和主题'"),
    ("'Translate Page...'",         "'翻译页面...'"),
    ("'Customize Zen...'",          "'自定义 Zen...'"),
    ("'Web Developer Tools'",       "'Web 开发者工具'"),
    ("'About Zen'",                 "'关于 Zen'"),
    ("'New Window'",                "'新建窗口'"),
    ("'New Private Window'",        "'新建隐私窗口'"),
    ("'Search Google or type a URL'", "'使用 Google 搜索或输入网址'"),
    ("'Search Brave or type a URL'", "'使用 Brave 搜索或输入网址'"),
    ("'Search or enter address'",   "'搜索或输入网址'"),
    ("'Search...'",                 "'搜索...'"),
    ("'Ask anything, find anything...'", "'搜索或输入网址...'"),
    ("'Search the web'",            "'搜索网页'"),
    ("'Ask something…'",            "'问点什么…'"),
    ("'Please wait for a response.'", "'请等待响应。'"),
    ("'Please choose a response.'", "'请选择响应。'"),
    ("'Capturing page content…'",   "'正在捕获页面内容…'"),
    ("'Allow GUST Assistant to access this page?'", "'允许 GUST 助手访问此页面？'"),
    ("'I need permission to access the content of this page.'",
                                    "'我需要访问此页面内容的权限。'"),
    ("'GUST Assistant was cut off. Continue?'", "'GUST 助手被截断。是否继续？'"),
    ("'Continue'",                  "'继续'"),
    ("'No extensions installed.'",  "'未安装任何扩展。'"),
    ("'Load a .crx or .zip to get started.'",
                                    "'加载 .crx 或 .zip 文件以开始。'"),
    ("'Load extension (.crx / .zip)'", "'加载扩展 (.crx / .zip)'"),
    ("'Browse the Chrome Web Store'", "'浏览 Chrome 应用商店'"),
    ("'Open store page'",           "'打开商店页面'"),
    ("'Installed'",                 "'已安装'"),
    ("'Remove theme'",              "'移除主题'"),
    ("'Theme ·'",                   "'主题 ·'"),
    ("'active'",                    "'已激活'"),
    ("'No results parsed for'",     "'未解析到结果'"),
    ("'Searching the Chrome Web Store…'", "'正在搜索 Chrome 应用商店…'"),
    ("'Popular extensions'",        "'热门扩展'"),
    ("'Results for'",               "'搜索结果：'"),
    ("'Search the Chrome Web Store'", "'搜索 Chrome 应用商店'"),
    ("'Search extensions and themes'", "'搜索扩展和主题'"),
    ("'GUST Extensions'",           "'GUST 扩展'"),
    ("'Install real Chrome extensions — powered by the Chrome Web Store'",
                                    "'安装真正的 Chrome 扩展 — 由 Chrome 应用商店提供支持'"),
    ("'Install by URL / ID'",       "'通过网址 / ID 安装'"),
    ("'Load file'",                 "'加载文件'"),
    ("'Open the original store page anyway'",
                                    "'仍要打开原始商店页面'"),

    # ═══════════════════════════════════════════════════════════
    #  Extensions 面板 - HTML 内嵌文案
    # ═══════════════════════════════════════════════════════════
    ('>Load extension (.crx / .zip)<',  '>加载扩展 (.crx / .zip)<'),
    ('>Browse the Chrome Web Store<',   '>浏览 Chrome 应用商店<'),
    ('>No extensions installed.<br>Load a .crx or .zip to get started.',
     '>未安装任何扩展。<br>加载 .crx 或 .zip 文件以开始。'),
    ('>Open store page<',               '>打开商店页面<'),
    ('>Remove theme<',                  '>移除主题<'),

    # ═══════════════════════════════════════════════════════════
    #  Benchmarking relays（WISP 池启动基准测试）
    # ═══════════════════════════════════════════════════════════
    ('>Benchmarking relays…<',      '>正在基准测试中继…<'),
    ("'Benchmarking relays…'",      "'正在基准测试中继…'"),
    ("`Benchmarking relays… ${done}/${total}`",
     "`正在基准测试中继… ${done}/${total}`"),
    ("Benchmarking relays… ${done}/${total}",
     "正在基准测试中继… ${done}/${total}"),

    # ═══════════════════════════════════════════════════════════
    #  GUST+ 核心调色板名称
    # ═══════════════════════════════════════════════════════════
    ("['--bg0', 'Base']",           "['--bg0', '基础']"),
    ("['--bg1', 'Panel']",          "['--bg1', '面板']"),
    ("['--bg2', 'Card']",           "['--bg2', '卡片']"),
    ("['--bg3', 'Raised']",         "['--bg3', '凸起']"),
    ("['--bg-elevated', 'Elevated']","['--bg-elevated', '浮层']"),
    ("['--tx', 'Text']",            "['--tx', '文本']"),
    ("['--tx2', 'Muted']",          "['--tx2', '次要文本']"),
    ("['--tx3', 'Faint']",          "['--tx3', '弱化文本']"),
    ("['--ac', 'Accent']",          "['--ac', '强调色']"),
    ("['--ac2', 'Accent alt']",     "['--ac2', '强调色替代']"),
    ("['--bd', 'Border']",          "['--bd', '边框']"),
    ("['--bd2', 'Border hi']",      "['--bd2', '边框高亮']"),
    ("['--ok', 'OK']",              "['--ok', '成功']"),
    ("['--warn', 'Warn']",          "['--warn', '警告']"),
    ("['--err', 'Error']",          "['--err', '错误']"),

    # ═══════════════════════════════════════════════════════════
    #  启动 Splash / 初始化阶段
    # ═══════════════════════════════════════════════════════════
    ('>Initializing...<',           '>正在初始化...<'),
    ("'Initializing...'",           "'正在初始化...'"),
    ('"Initializing..."',           '"正在初始化..."'),
    ('Initializing...',             '正在初始化...'),
    ('"Starting..."',               '"正在启动…"'),
    ('"Cache initialized"',         '"缓存已初始化"'),
    ('libcurl initialized successfully', 'libcurl 初始化成功'),
    ("Ready! (${MAX_CONCURRENT} connections, 1h cache)",
     "就绪！(${MAX_CONCURRENT} 个连接，1 小时缓存)"),
    ('Ready! (',                    '就绪！('),
    ('connections, 1h cache)',      '个连接，1 小时缓存)'),
    ('>Loading...<',                '>加载中...<'),
    ("showOverlay(\"Loading...\")", "showOverlay(\"加载中...\")"),

    # ═══════════════════════════════════════════════════════════
    #  Discord Anywhere 内嵌页面（gust://discord）
    # ═══════════════════════════════════════════════════════════
    ('<title>Discord Anywhere</title>',  '<title>Discord 随行版</title>'),
    ('>Discord Anywhere<',               '>Discord 随行版<'),
    ('Full Discord client that runs from a local file. Every request and the realtime gateway are tunneled through a public Wisp relay (WASM TLS-over-WebSocket), so it works from <code>file://</code> even where discord.com is blocked.',
     '完整的 Discord 客户端，从本地文件运行。所有请求和实时网关都通过公共 Wisp 中继（WASM TLS-over-WebSocket）隧道传输，因此即使 discord.com 被屏蔽，也能从 <code>file://</code> 运行。'),
    ('Scripting Discord with a user token ("selfbotting") violates Discord\'s Terms and can get your account terminated. <b>Voice/video/screen-share is the one unsupported feature</b> — browsers forbid raw UDP, so the only in-browser voice path is WebRTC, and WebRTC media bypasses this tunnel to reach Discord\'s (blocked) voice servers directly. Every text/data feature works.',
     '使用用户令牌脚本化 Discord（“selfbotting”）违反 Discord 服务条款，可能导致账号被封禁。<b>语音/视频/屏幕共享是唯一不支持的功能</b> — 浏览器禁止原始 UDP，因此浏览器内唯一的语音路径是 WebRTC，而 WebRTC 媒体会绕过此隧道直接连接 Discord（被屏蔽）的语音服务器。所有文本/数据功能均正常工作。'),
    ('placeholder="paste token (or bake into BAKED_TOKEN)"',
     'placeholder="粘贴 token（或烘焙到 BAKED_TOKEN）"'),
    ('>Connect</button>',                '>连接</button>'),
    ('<summary>How to get your token</summary>',
     '<summary>如何获取你的 token</summary>'),
    ('At <code>discord.com/app</code>, DevTools → Network tab → filter <code>messages</code> → click a channel → open any <code>/api</code> request → Request Headers → copy the <code>authorization</code> value.',
     '在 <code>discord.com/app</code>，打开开发者工具 → Network（网络）标签 → 筛选 <code>messages</code> → 点击任意频道 → 打开任意 <code>/api</code> 请求 → Request Headers（请求头）→ 复制 <code>authorization</code> 的值。'),
    ("'Discord Anywhere'",               "'Discord 随行版'"),
    ('"Discord Anywhere"',               '"Discord 随行版"'),

    # ═══════════════════════════════════════════════════════════
    #  GitHub 仓库地址替换
    # ═══════════════════════════════════════════════════════════
    ('window.open("https://github.com/nautilus-os/GUST"',
     'window.open("https://github.com/cjhdevact/GUST-Chinese"'),

])


# ═══════════════════════════════════════════════════════════════════
#  JS 专用补充替换表
# ═══════════════════════════════════════════════════════════════════
JS_EXTRA = OrderedDict([
    ("'Starting...'",                   "'正在启动...'"),
    ("'Cache initialized'",             "'缓存已初始化'"),
    ("'Page ready'",                    "'页面就绪'"),
    ("'Logs cleared'",                  "'日志已清空'"),
    ("'Logs copied to clipboard'",      "'日志已复制到剪贴板'"),
    ("'Failed to copy logs: '",         "'复制日志失败: '"),
    ("'Custom filters saved'",          "'自定义过滤器已保存'"),
    ("'Failed to save filters'",        "'保存过滤器失败'"),
    ("'Browser reset initiated...'",    "'浏览器重置已开始...'"),
    ("'URL copied to clipboard'",       "'网址已复制到剪贴板'"),
    ("'Failed to copy URL'",            "'复制网址失败'"),
    ("'Stopped'",                       "'已停止'"),
    ("'Aborted'",                       "'已中止'"),
    ("'Invalid URL'",                   "'无效网址'"),
    ("'WISP connection lost, reconnecting...'",    "'WISP 连接断开，正在重连...'"),
    ("'Reconnected to WISP (attempt '",            "'已重连 WISP（第 '"),
    ("'WISP reconnect failed after 3 attempts: '", "'WISP 重连 3 次失败: '"),
    ("'WISP reconnect attempt '",                  "'WISP 第 '"),
    ("' failed, retrying...'",                     "' 次重连失败，重试中...'"),
    ("'WISP reconnect failed: '",                  "'WISP 重连失败: '"),
    ("'WISP switched to '",                        "'WISP 已切换到 '"),
    ("'Failed to save WISP URL'",                  "'保存 WISP 地址失败'"),
    ("'Failed to reset WISP URL'",                 "'重置 WISP 地址失败'"),
    ("'Saved — applying...'",                      "'已保存 — 正在应用...'"),
    ("'Saved & connected!'",                       "'已保存并连接！'"),
    ("'Reset — applying...'",                      "'已重置 — 正在应用...'"),
    ("'Reset & connected!'",                       "'已重置并连接！'"),
    ("'Must start with wss:// or ws://'",          "'必须以 wss:// 或 ws:// 开头'"),
    ("'Saved - idle: '",                "'已保存 - 空闲: '"),
    ("', active: '",                    "'，活跃: '"),
    ("'Failed to save'",                "'保存失败'"),
    ("'Reset to defaults (idle: 3, active: 6)'", "'已重置为默认值（空闲: 3，活跃: 6）'"),
    ("'Allowlist saved.'",              "'白名单已保存。'"),
    ("'Waiting for input...'",          "'等待输入...'"),
    ("'Cannot bookmark error pages'",   "'无法收藏错误页面'"),
    ("'Cannot bookmark internal pages'","'无法收藏内部页面'"),
    ("'Remove bookmark (Alt+D)'",       "'移除书签 (Alt+D)'"),
    ("'Bookmark this page (Alt+D)'",    "'收藏此页 (Alt+D)'"),
    ("'New tab (Ctrl+T)'",              "'新建标签页 (Ctrl+T)'"),
    
        # ═══════════════════════════════════════════════════════════
    #  关于页正文（SVG 多行精确匹配）
    # ═══════════════════════════════════════════════════════════

    # 品牌行
    ('GUST Browser\n                                            </div>',
     'GUST 浏览器\n                                            </div>'),

    # How it works 标题（跨行）
    ('> How it\n                                                    works\n                                                </div>',
     '> 工作原理\n                                                </div>'),
    ('How it\n                                                    works',
     '工作原理'),

    # How it works 正文
    ("Gust is a <strong style=\"color:var(--tx);\">static</strong> web proxy\n                                                    browser that runs entirely inside a single HTML file.",
     'Gust 是一个完全运行在单个 HTML 文件内的<strong style="color:var(--tx);">静态</strong> Web 代理浏览器。'),
    ("When you navigate to a URL, Gust fetches the target site's HTML,\n                                                CSS, scripts, and assets through <em>Wisp</em>, then rewrites\n                                                all resource URLs and injects them into a sandboxed iframe.",
     '当你导航到一个网址时，Gust 会通过 <em>Wisp</em> 获取目标站点的 HTML、CSS、脚本和资源，然后重写所有资源 URL 并将其注入到沙盒 iframe 中。'),
    ("Gust can be run inside any HTML editor, <code style=\"background:var(--bg3); padding:2px 6px; border-radius:4px; font-size:12px;\">iframe</code>, file, or blob. It's ultra lightweight, packed with features, and is near impossible to block for admins.",
     'Gust 可运行在任何 HTML 编辑器、<code style="background:var(--bg3); padding:2px 6px; border-radius:4px; font-size:12px;">iframe</code>、文件或 blob 中。它极其轻量，功能丰富，管理员几乎无法屏蔽。'),

    # WISP + libcurl.js 正文
    ('All network requests are tunnelled through a <strong style="color:var(--tx);">WISP WebSocket server</strong>. Your\n                                                browser opens a WebSocket to the WISP endpoint, which forwards\n                                                TCP/TLS connections on your behalf.',
     '所有网络请求都通过 <strong style="color:var(--tx);">WISP WebSocket 服务器</strong>隧道传输。你的浏览器会向 WISP 端点打开一个 WebSocket，由其代为转发 TCP/TLS 连接。'),
    ("The actual HTTP fetching is\n                                                handled by <strong style=\"color:var(--tx);\">libcurl.js</strong>\n                                                &amp;mdash; a port of the curl HTTP library compiled to WebAssembly\n                                                &amp;mdash; giving full HTTPS, redirect, and cookie support inside the\n                                                browser context.",
     '实际的 HTTP 请求由 <strong style="color:var(--tx);">libcurl.js</strong> 处理 &amp;mdash; 它是 curl HTTP 库编译为 WebAssembly 的移植版 &amp;mdash; 在浏览器上下文中提供完整的 HTTPS、重定向和 Cookie 支持。'),

    # Page rendering 标题
    ('> Page\n                                                    rendering\n                                                </div>',
     '> 页面渲染\n                                                </div>'),
    ('Page\n                                                    rendering',
     '页面渲染'),

    # Page rendering 正文
    ('Fetched HTML is parsed and rewritten in JavaScript. CSS stylesheets\n                                                and scripts are loaded through the proxy and injected inline or as\n                                                Blob URLs.',
     '获取的 HTML 由 JavaScript 解析并重写。CSS 样式表和脚本通过代理加载，并以内联或 Blob URL 的形式注入。'),
    ('Images, fonts, and other assets have their URLs rewritten\n                                                to route through the same proxy pipeline.',
     '图片、字体和其他资源的 URL 被重写，以通过同一代理管道路由。'),
    ('The final document is\n                                                rendered inside a sandboxed <code style="background:var(--bg3); padding:2px 6px; border-radius:4px; font-size:12px;">iframe</code>\n                                                using a generated Blob URL.',
     '最终文档使用生成的 Blob URL 在沙盒 <code style="background:var(--bg3); padding:2px 6px; border-radius:4px; font-size:12px;">iframe</code> 中渲染。'),

    # Privacy & limitations 标题
    ('> Privacy &amp; limitations\n                                                </div>',
     '> 隐私与限制\n                                                </div>'),
    ('Privacy &amp; limitations',
     '隐私与限制'),
    ('Privacy & limitations',
     '隐私与限制'),

    # Privacy & limitations 正文
    ('Because requests flow through the WISP server, your real IP is not\n                                                exposed to the sites you visit.',
     '由于请求流经 WISP 服务器，你的真实 IP 不会暴露给你访问的站点。'),
    ('However, the WISP server operator\n                                                may be able to see your traffic.',
     '但 WISP 服务器运营者可能看到你的流量。'),
    ('Some complex web features (native WebSockets from within pages,\n                                                WebRTC, service workers) cannot be fully proxied and may not work.',
     '一些复杂的 Web 特性（页面内的原生 WebSocket、WebRTC、Service Worker）无法完全代理，可能无法工作。'),
    ('JavaScript inside the iframe is fully sandboxed from the parent\n                                                page.',
     'iframe 内的 JavaScript 与父页面完全隔离。'),
     
    # ═══════════════════════════════════════════════════════════
    #  关于页面正文（逐段匹配 SVG 内换行）
    # ═══════════════════════════════════════════════════════════
    ("WebSocket proxy tunnelling",  "WebSocket 代理隧道"),
    ("curl compiled to WebAssembly","curl 编译为 WebAssembly"),
    ("v4.2.67 · PDF rendering engine","v4.2.67 · PDF 渲染引擎"),
    ("v6.5.1 · Icon library",       "v6.5.1 · 图标库"),
    ("v2.1.11 · ISO language codes","v2.1.11 · ISO 语言代码"),
    ("Monospace font (code viewer)","等宽字体（代码查看器）"),
    ("UI font via Google Fonts",    "通过 Google Fonts 加载的界面字体"),
    ("Proxy cache, storage, sessions","代理缓存、存储、会话"),
    ("The team behind GUST",        "GUST 背后的团队"),
    ("Original Gust Framework &amp; JS", "原始 Gust 框架与 JS"),
    ("Original Gust Framework & JS",     "原始 Gust 框架与 JS"),
    
    ('https://github.com/nautilus-os/GUST/', 'https://github.com/cjhdevact/GUST-Chinese/'),
    ('https://github.com/nautilus-os/GUST',  'https://github.com/cjhdevact/GUST-Chinese'),
    
])

REPLACEMENTS.update(JS_EXTRA)


# ═══════════════════════════════════════════════════════════════════
#  根据开关追加的替换规则
# ═══════════════════════════════════════════════════════════════════

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
        ("const engineNames = { brave: 'Brave', ddg: 'DuckDuckGo', bing: 'Bing', custom: getCustomEngineName() };",
         "const engineNames = { brave: 'Brave', ddg: 'DuckDuckGo', bing: 'Bing', baidu: '百度', custom: getCustomEngineName() };"),
    ]))

if USE_BING_AS_DEFAULT:
    REPLACEMENTS.update(OrderedDict([

        # ═══════════════════════════════════════════════════════════
        #  SVG 静态占位文本（site.svg 首屏渲染用）
        # ═══════════════════════════════════════════════════════════
        ('<span id="ntEngineLabel">Brave</span>',
         '<span id="ntEngineLabel">Bing</span>'),
        ('<span id="ntEngineLabel">DuckDuckGo</span>',
         '<span id="ntEngineLabel">Bing</span>'),
        ('<span id="ntEngineLabel">brave</span>',
         '<span id="ntEngineLabel">Bing</span>'),
        ('<span id="ntEngineLabel">ddg</span>',
         '<span id="ntEngineLabel">Bing</span>'),

        # ═══════════════════════════════════════════════════════════
        #  JS 默认引擎初始化（selectedEngine）
        # ═══════════════════════════════════════════════════════════

        # ── 单引号：'brave' / 'ddg' / 'google' ──
        ("ls.getItem('gust:engine:v1') || 'brave'; } catch { return 'brave'; }",
         "ls.getItem('gust:engine:v1') || 'bing'; } catch { return 'bing'; }"),
        ("ls.getItem('gust:engine:v1') || 'ddg'; } catch { return 'ddg'; }",
         "ls.getItem('gust:engine:v1') || 'bing'; } catch { return 'bing'; }"),
        ("ls.getItem('gust:engine:v1') || 'google'; } catch { return 'google'; }",
         "ls.getItem('gust:engine:v1') || 'bing'; } catch { return 'bing'; }"),

        # ── 双引号变体 ──
        ('ls.getItem("gust:engine:v1") || "brave"; } catch { return "brave"; }',
         'ls.getItem("gust:engine:v1") || "bing"; } catch { return "bing"; }'),
        ('ls.getItem("gust:engine:v1") || "ddg"; } catch { return "ddg"; }',
         'ls.getItem("gust:engine:v1") || "bing"; } catch { return "bing"; }'),

        # ── 直接赋值：selectedEngine = 'xxx' ──
        ("selectedEngine = 'brave';",   "selectedEngine = 'bing';"),
        ("selectedEngine = 'ddg';",     "selectedEngine = 'bing';"),
        ("selectedEngine = 'google';",  "selectedEngine = 'bing';"),
        ('selectedEngine = "brave";',   'selectedEngine = "bing";'),
        ('selectedEngine = "ddg";',     'selectedEngine = "bing";'),
        ('selectedEngine = "google";',  'selectedEngine = "bing";'),

        # ═══════════════════════════════════════════════════════════
        #  localStorage 存储值
        # ═══════════════════════════════════════════════════════════
        ("ls.setItem('gust:engine:v1', 'brave');",  "ls.setItem('gust:engine:v1', 'bing');"),
        ("ls.setItem('gust:engine:v1', 'ddg');",    "ls.setItem('gust:engine:v1', 'bing');"),
        ("ls.setItem('gust:engine:v1', 'google');", "ls.setItem('gust:engine:v1', 'bing');"),
        ('ls.setItem("gust:engine:v1", "brave");',  'ls.setItem("gust:engine:v1", "bing");'),
        ('ls.setItem("gust:engine:v1", "ddg");',    'ls.setItem("gust:engine:v1", "bing");'),
        ('ls.setItem("gust:engine:v1", "google");', 'ls.setItem("gust:engine:v1", "bing");'),

        # ═══════════════════════════════════════════════════════════
        #  engineNames 回退名（标签显示用）
        # ═══════════════════════════════════════════════════════════
        ("engineNames[selectedEngine] || 'Brave'",
         "engineNames[selectedEngine] || 'Bing'"),
        ("engineNames[selectedEngine] || 'DuckDuckGo'",
         "engineNames[selectedEngine] || 'Bing'"),
        ('engineNames[selectedEngine] || "Brave"',
         'engineNames[selectedEngine] || "Bing"'),
        ('engineNames[selectedEngine] || "DuckDuckGo"',
         'engineNames[selectedEngine] || "Bing"'),

        # ═══════════════════════════════════════════════════════════
        #  初始化时重置无效引擎（新版 GUST 的隐藏逻辑）
        # ═══════════════════════════════════════════════════════════
        # 原来是把 google/brave 重置为 ddg，现在把三者都重置为 bing
        # 多行缩进版本（key_to_pattern 会把空白转 \s+，所以能跨行匹配）
        ("if (selectedEngine === 'google' || selectedEngine === 'brave') {\n                            selectedEngine = 'ddg';\n                            try { ls.setItem('gust:engine:v1', 'ddg'); } catch { }",
         "if (selectedEngine === 'google' || selectedEngine === 'brave' || selectedEngine === 'ddg') {\n                            selectedEngine = 'bing';\n                            try { ls.setItem('gust:engine:v1', 'bing'); } catch { }"),

        # 单行版本（压缩代码）
        ("if (selectedEngine === 'google' || selectedEngine === 'brave') { selectedEngine = 'ddg'; try { ls.setItem('gust:engine:v1', 'ddg'); } catch { }",
         "if (selectedEngine === 'google' || selectedEngine === 'brave' || selectedEngine === 'ddg') { selectedEngine = 'bing'; try { ls.setItem('gust:engine:v1', 'bing'); } catch { }"),

        # 宽松版本：只要遇到这个 if 条件就把 brave/ddg 也纳入
        ("if (selectedEngine === 'google' || selectedEngine === 'brave') {",
         "if (selectedEngine === 'google' || selectedEngine === 'brave' || selectedEngine === 'ddg') {"),
        ("selectedEngine = 'ddg';",  "selectedEngine = 'bing';"),
        ("ls.setItem('gust:engine:v1', 'ddg');",  "ls.setItem('gust:engine:v1', 'bing');"),

        # ═══════════════════════════════════════════════════════════
        #  SEARCH_ENGINES 常量（可选：把默认值指向 Bing）
        # ═══════════════════════════════════════════════════════════
        # 如果源码里有这种写法：
        # const defaultEngine = 'brave';
        # 则需要改
        ("const defaultEngine = 'brave';",  "const defaultEngine = 'bing';"),
        ("const defaultEngine = 'ddg';",    "const defaultEngine = 'bing';"),
        ("const defaultEngine = 'google';", "const defaultEngine = 'bing';"),

        # ═══════════════════════════════════════════════════════════
        #  NTP 初始化逻辑（部分版本会显式设置一次）
        # ═══════════════════════════════════════════════════════════
        # 如果源码里有：
        # ntEngineLabel.textContent = 'Brave';
        # 则改为
        ("ntEngineLabel.textContent = 'Brave';",      "ntEngineLabel.textContent = 'Bing';"),
        ("ntEngineLabel.textContent = 'DuckDuckGo';", "ntEngineLabel.textContent = 'Bing';"),
        ("ntEngineLabel.textContent = 'brave';",      "ntEngineLabel.textContent = 'Bing';"),
        ("ntEngineLabel.textContent = 'ddg';",        "ntEngineLabel.textContent = 'Bing';"),

    ]))

# 清理永远不能命中的冗余规则
for _dead_key in [
    '>Cache<',
    'Blocklist & Filter',
    'Privacy & limitations',
    'Save Rules',
    '>Done<',
    "'Ready'",
    '"Loading…"',
]:
    REPLACEMENTS.pop(_dead_key, None)


# ═══════════════════════════════════════════════════════════════════
#  水印 / Emoji 清理规则
# ═══════════════════════════════════════════════════════════════════
WATERMARK_PATTERNS = [
    re.compile(r'<div\s+id="gustCredit"[^>]*>.*?</div>', re.DOTALL | re.IGNORECASE),
]

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
    """
    把 key 里的空白转成 \\s+，允许内部换行/多空格。
    首尾只有当 key 本身带空白时，才允许匹配空白 —— 避免吞掉标签间必要空格。
    """
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
    body = ''.join(parts)

    # 仅当 key 首尾本来就有空白时，才允许匹配任意空白
    prefix = r'\s*' if key[:1].isspace() else ''
    suffix = r'\s*' if key[-1:].isspace() else ''
    return prefix + body + suffix
    """
    把 key 里的空白转成 \\s+，同时允许首尾出现任意空白/换行/缩进。
    这对 SVG 场景很关键：源码里文本节点常被换行缩进拆开。
    """
    # 先按原样把内部空白转 \s+
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
    body = ''.join(parts)

    # 首尾加 \s* —— 允许标签前后有换行/缩进
    # 但如果 key 本身以 < 或 > 开头/结尾，就不加（避免误伤相邻标签）
    prefix = '' if key[:1] in ('<', '>') else r'\s*'
    suffix = '' if key[-1:] in ('<', '>') else r'\s*'
    return prefix + body + suffix


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
    在关于页面「How it works」标题上方注入两行署名。
    锚点：<i class="fas fa-globe" ...></i> How it works
    """
    translator_name = TRANSLATOR_NAME
    translator_url  = GITHUB_REPO_URL
    commit_hash     = COMMIT_HASH

    if translator_name in html and '提交翻译' in html:
        return html

    line1 = (
        f'由 <a href="{translator_url}" target="_blank" rel="noopener noreferrer" '
        f'style="color:var(--ac);text-decoration:none;">{translator_name}</a> 实现翻译'
    )
    line2 = f'基于 {commit_hash} 提交翻译'

    # 锚点：含 fa-globe 图标 + How it works（兼容 SVG 换行）
    pattern = re.compile(
        r'(<div[^>]*>\s*<i class="fas fa-globe"[^>]*></i>\s*(?:How\s+it\s+works|工作原理))',
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
#  文件类型识别
# ═══════════════════════════════════════════════════════════════════

def detect_file_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == '.svg':
        return 'svg'
    if suffix == '.js':
        return 'js'
    if suffix == '.css':
        return 'css'
    if suffix in ('.html', '.htm'):
        return 'html'
    try:
        head = path.read_text(encoding='utf-8', errors='ignore')[:500]
        if '<svg' in head:
            return 'svg'
    except Exception:
        pass
    return 'unknown'


# ═══════════════════════════════════════════════════════════════════
#  单文件处理
# ═══════════════════════════════════════════════════════════════════

def process_file(path: Path, args, verbose=True):
    ftype = detect_file_type(path)

    if ftype == 'css':
        if verbose:
            print(f"\n  [{path.name}] CSS 文件无需汉化，跳过。")
        return None

    text = path.read_text(encoding='utf-8')
    original_len = len(text)

    pattern = build_pattern(REPLACEMENTS)
    counts = {}
    result = localize(text, REPLACEMENTS, pattern, counts)

    if ftype in ('html', 'svg') and not args.keep_watermark:
        result = strip_watermark(result, counts)

    if not args.keep_emoji:
        result = strip_emoji(result, counts)

    if ftype in ('html', 'svg') and not args.no_credit:
        result = inject_translator_credit(result, counts)

    if verbose:
        print()
        print("=" * 78)
        print(f"  [{ftype.upper()}] {path.name}")
        print("=" * 78)
        total = 0
        hit, miss = 0, 0
        for old, new in REPLACEMENTS.items():
            key = normalize_ws(old)
            n = counts.get(key, 0)
            if n > 0:
                hit += 1
                total += n
                o = old if len(old) <= 44 else old[:41] + "..."
                n_ = new if len(new) <= 44 else new[:41] + "..."
                print(f"  [OK] {n:>3}x {o:<46} -> {n_}")
            else:
                miss += 1
        for k, label in [
            ('__watermark__', '水印已移除'),
            ('__emoji__',     'Emoji 已清除'),
            ('__translator__','翻译者信息已注入'),
        ]:
            if counts.get(k):
                total += counts[k]
                print(f"  [OK] {counts[k]:>3}x {label}")
        print("-" * 78)
        print(f"  命中 {hit} 条 / 共替换 {total} 处；未命中 {miss} 条")
        print(f"  大小: {original_len:,} -> {len(result):,} 字节")
        print("=" * 78)

    if args.dry_run:
        return result

    if args.output and len(args.files) == 1:
        out = Path(args.output)
    else:
        backup = path.with_suffix(path.suffix + '.bak')
        if not backup.exists():
            backup.write_text(text, encoding='utf-8')
            if verbose:
                print(f"  [备份] {backup.name}")
        out = path

    out.write_text(result, encoding='utf-8')
    if verbose:
        print(f"  [完成] -> {out.name}\n")
    return result


# ═══════════════════════════════════════════════════════════════════
#  自动扫描
# ═══════════════════════════════════════════════════════════════════

def auto_scan():
    files = []
    cwd = Path.cwd()
    for p in cwd.rglob('site.svg'):
        files.append(p)
        static = p.parent / 'static'
        for name in ('js.js', 'css.css'):
            f = static / name
            if f.is_file():
                files.append(f)
    return files


# ═══════════════════════════════════════════════════════════════════
#  主流程
# ═══════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(
        description="GUST 浏览器 SVG 版本汉化工具（完整修正版）"
    )
    ap.add_argument("files", nargs="*", help="输入文件（site.svg static/js.js ...）")
    ap.add_argument("--auto", action="store_true",
                    help="自动扫描当前目录及子目录中的 site.svg + static/js.js")
    ap.add_argument("-o", "--output", help="输出文件（仅单文件有效）")
    ap.add_argument("--dry-run", action="store_true", help="仅预览，不写文件")
    ap.add_argument("--keep-emoji", action="store_true", help="保留 emoji")
    ap.add_argument("--keep-watermark", action="store_true", help="保留主页水印")
    ap.add_argument("--no-credit", action="store_true", help="不注入翻译者信息")
    args = ap.parse_args()

    if args.auto:
        args.files = [str(p) for p in auto_scan()]
        if not args.files:
            print("[ERROR] 未在当前目录找到 site.svg")
            sys.exit(1)
        print(f"[扫描] 找到 {len(args.files)} 个文件")

    if not args.files:
        ap.print_help()
        sys.exit(1)

    paths = [Path(f) for f in args.files]
    missing = [p for p in paths if not p.is_file()]
    if missing:
        for m in missing:
            print(f"[ERROR] 找不到文件: {m}")
        sys.exit(1)

    success = 0
    for p in paths:
        try:
            process_file(p, args)
            success += 1
        except Exception as e:
            print(f"[ERROR] 处理 {p} 失败: {e}")

    print(f"\n  共处理 {success}/{len(paths)} 个文件。\n")
    if args.dry_run:
        print("  [dry-run] 未写入任何文件。\n")


if __name__ == "__main__":
    main()