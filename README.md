# YOURLS 简体中文 翻译包

YOURLS（Your Own URL Shortener）的简体中文翻译包，基于官方最新英文模板，由 GitHub Actions 自动拉取并增量翻译。

## 翻译包内容

| 文件 | 说明 |
|------|------|
| `YOURLS.pot` | 官方最新英文翻译模板（源自 [YOURLS/YOURLS.pot](https://github.com/YOURLS/YOURLS.pot)） |
| `zh_CN.po` | 简体中文翻译（gettext 源码，可读可编辑） |
| `zh_CN.mo` | 编译后的翻译文件（YOURLS 实际加载） |

## 安装

将 `zh_CN.po` 与 `zh_CN.mo` 放入 YOURLS 根目录的 `user/languages/` 目录，并在 `user/config.php` 中设置语言：

```php
define( 'YOURLS_LANG', 'zh_CN' );
```

## 自动同步（GitHub Actions）

本仓库通过 GitHub Actions 每周自动更新翻译：

1. 从官方仓库拉取最新英文模板 `YOURLS.pot`
2. 使用 DeepL API **增量翻译**新增/变更词条
3. 重新编译 `zh_CN.mo`，自动提交并推送

- **运行时间**：每周定时（北京时间周一 05:00），也可在 Actions 页手动触发
- **增量翻译**：只处理新增或变更的词条，已有人工翻译保持不变
- **前提**：需在仓库 Secrets 配置 `DEEPL_API_KEY`（DeepL API Free，每月 50 万字符免费额度）
- **官方源**：[YOURLS/YOURLS.pot](https://github.com/YOURLS/YOURLS.pot)，官方用 xgettext 从源码自动生成

## 插件汉化

插件列表中的名称与简介取自各插件 `plugin.php` 头注释（`Plugin Name:` / `Description:`），属于插件自身的元数据，**不通过本翻译包翻译**。如需汉化插件，请直接修改对应插件的 `plugin.php` 头注释。

## 关联仓库

- 上游英文模板源：[YOURLS/YOURLS.pot](https://github.com/YOURLS/YOURLS.pot)
- 更新调整：[KuwiNet/YOURLS.pot-zh_CN](https://github.com/KuwiNet/YOURLS.pot-zh_CN)
