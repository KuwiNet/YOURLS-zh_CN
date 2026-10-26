#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
msgmerge 之后调用：把插件专属词条从 obsolete 恢复为 active。

官方 YOURLS.pot 排除了 user/ 目录，所以插件的词条（如 sample-toolbar 用
yourls_n() 的 'day'/'days'、'view'/'views'）不在官方 pot 中。msgmerge 默认会把
po 里不在 pot 中的词条标为 obsolete（#~），编译进 .mo 时会丢失、翻译失效。
本脚本在 merge 之后、DeepL 翻译之前运行，把这些词条恢复为 active。
"""
import polib

PO_FILE = "zh_CN.po"

# 需要保护的插件专属词条（msgid 值）
PLUGIN_MSGS = {"day", "view"}


def main():
    po = polib.pofile(PO_FILE)
    restored = []

    # 逐个检查 obsolete 词条（polib 中 obsolete_entries 是过滤视图方法；
    # 只需把 e.obsolete 置 False，保存时即恢复为 active 并保留已有译文）
    for e in list(po.obsolete_entries()):
        if e.msgid in PLUGIN_MSGS:
            e.obsolete = False
            e.fuzzy = False
            restored.append(e.msgid)

    po.save(PO_FILE)

    if restored:
        print("已恢复插件词条为 active: %s" % ", ".join(restored))
    else:
        print("无需恢复（插件词条已在 po 中或本次无变更）")


if __name__ == "__main__":
    main()
