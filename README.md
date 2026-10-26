# YOURLS 简体中文 翻译包

YOURLS（Your Own URL Shortener）的简体中文翻译包，基于官方最新英文模板，由 GitHub Actions 自动拉取并增量翻译。

## 翻译包内容

| 文件 | 说明 |
|------|------|
| `YOURLS.pot` | 官方最新英文翻译模板（源自 [YOURLS/YOURLS.pot](https://github.com/YOURLS/YOURLS.pot)） |
| `zh_CN.po` | 简体中文翻译（gettext 源码，可读可编辑） |
| `zh_CN.mo` | 编译后的翻译文件（YOURLS 实际加载） |
| `user/plugins/` | 6 个官方示例插件的中文汉化（解压即部署） |

## 安装

将 `zh_CN.po` 与 `zh_CN.mo` 放入 YOURLS 根目录的 `user/languages/` 目录，并在 `user/config.php` 中设置语言：

```php
define( 'YOURLS_LANG', 'zh_CN' );
```

> **推荐**：直接从 Release 下载 `yourls-zh_CN-<版本>.zip`，解压后把整个 `user/` 目录复制到 YOURLS 根目录即可（同时包含简体翻译与插件汉化）。

## 自动同步（GitHub Actions）

本仓库通过 GitHub Actions 每周自动更新翻译：

1. 从官方仓库拉取最新英文模板 `YOURLS.pot`
2. 使用 DeepL API **增量翻译**新增/变更词条
3. 重新编译 `zh_CN.mo`，自动提交并推送
4. 按官方 YOURLS 版本号发布/更新 Release（含翻译 + 插件汉化）

- **运行时间**：每周定时（北京时间周一 05:00），也可在 Actions 页手动触发
- **增量翻译**：只处理新增或变更的词条，已有人工翻译保持不变
- **前提**：需在仓库 Secrets 配置 `DEEPL_API_KEY`（DeepL API Free，每月 50 万字符免费额度）
- **官方源**：[YOURLS/YOURLS.pot](https://github.com/YOURLS/YOURLS.pot)，官方用 xgettext 从源码自动生成

## 插件汉化（user/plugins/）

本仓库自带 6 个官方示例插件的中文汉化（硬编码中文，不走 po），随 Release 一同发布：

| 插件 | 说明 |
|------|------|
| `hyphens-in-urls` | 允许短链接中使用连字符 |
| `random-bg` | 随机漂亮的背景图案 |
| `random-shorturls` | 为短链接分配随机关键字 |
| `sample-page` | 示例后台页面 |
| `sample-plugin` | 示例插件 |
| `sample-toolbar` | YOURLS 工具栏 |

安装时把 `user/plugins/` 整个复制到 YOURLS 根目录即可（或直接用 Release 完整包）。

## 上游模板源

- [YOURLS/YOURLS.pot](https://github.com/YOURLS/YOURLS.pot)：官方英文翻译模板仓库
