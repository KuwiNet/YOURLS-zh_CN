#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增量翻译 zh_CN.po 中「未翻译 / fuzzy」词条，使用 DeepL API Free。

设计要点：
1. 只处理新增或源字符串变更的词条，保护已有人工翻译；
2. 翻译前将 PHP 占位符（%s、%1$s、%2$d…）临时替换为 [[PHn]]，翻译后还原，防止被改写；
3. 对 HTML 标签用 DeepL 的 tag_handling=html 保护；失败时降级为不带 tag 处理再试；
4. 中文不区分单复数（nplurals=1），plural 条目只翻译并写入 msgstr[0]；
5. 单个词条翻译失败时保持待翻译状态并以非 0 退出，不写入英文原文。

用法：需环境变量 DEEPL_API_KEY。  python translate_new.py
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import polib

DEEPL_URL = "https://api-free.deepl.com/v2/translate"
API_KEY = os.environ.get("DEEPL_API_KEY", "")
PO_FILE = "zh_CN.po"

# 匹配 PHP gettext 占位符：%s、%1$s、%2$d 等
PH_RE = re.compile(r"%\d*\$?[sd]")


def _call_deepl(text, use_tag_handling):
    """调用 DeepL 翻译，返回译文文本。"""
    params = {
        "auth_key": API_KEY,
        "text": text,
        "source_lang": "EN",
        "target_lang": "ZH",
        "split_sentences": "0",
        "preserve_formatting": "1",
    }
    if use_tag_handling:
        params["tag_handling"] = "html"
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(DEEPL_URL, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result["translations"][0]["text"]


def _has_translation(entry):
    """判断词条是否已有译文。plural 条目需查 msgstr_plural[0]（polib 键为整数 0）。"""
    if entry.msgid_plural:
        return bool(entry.msgstr_plural.get(0))
    return bool(entry.msgstr)


def deepl_translate(text, retries=3):
    """翻译单条文本：先替换占位符，再调用 DeepL，失败时降级/重试。"""
    # 1) 占位符保护
    placeholders = {}
    counter = [0]

    def _repl(m):
        key = "[[PH%d]]" % counter[0]
        counter[0] += 1
        placeholders[key] = m.group(0)
        return key

    safe_text = PH_RE.sub(_repl, text)

    # 2) 调用，异常时先降级（去掉 tag_handling），再按指数退避重试
    last_err = None
    attempts = [True, False] if "<" in safe_text else [False]
    for use_tag in attempts:
        for attempt in range(retries):
            try:
                translated = _call_deepl(safe_text, use_tag)
                # 3) 还原占位符
                for key, orig in placeholders.items():
                    translated = translated.replace(key, orig)
                return translated
            except Exception as e:  # noqa: BLE001
                last_err = e
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
    print("DeepL 失败: %s\n原文: %s" % (last_err, text[:80]), file=sys.stderr)
    return None


def main():
    if not API_KEY:
        print("错误：缺少 DEEPL_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)

    po = polib.pofile(PO_FILE)

    # 需要翻译：无译文（新增）或 fuzzy（源字符串可能变更）。plural 条目以 msgstr_plural[0] 为准。
    to_translate = [
        e for e in po
        if e.msgid and not e.obsolete and (not _has_translation(e) or e.fuzzy)
    ]

    print("待处理词条数: %d" % len(to_translate))
    if not to_translate:
        print("官方模板无新增/变更词条，zh_CN.po 保持不变。")
        po.save(PO_FILE)
        return

    failures = 0
    for i, entry in enumerate(to_translate, 1):
        # 翻译源：plural 条目用复数形式（通常含 %s 占位符），其余用单数 msgid
        source = entry.msgid_plural if entry.msgid_plural else entry.msgid
        # 源字符串未变（仅位置/格式变化导致 fuzzy）→ 保留已有翻译，仅去掉 fuzzy
        if entry.fuzzy and _has_translation(entry) and entry.previous_msgid == source:
            entry.fuzzy = False
            print("[%d/%d] fuzzy 未变，保留已有翻译: %s"
                  % (i, len(to_translate), source[:60]))
            continue

        translated = deepl_translate(source)
        if translated is None:
            failures += 1
            print("[%d/%d] 翻译失败，保持待翻译状态（不写入英文原文）: %s"
                  % (i, len(to_translate), source[:60]))
            continue
        if entry.msgid_plural:
            # 中文 nplurals=1，仅 msgstr[0]
            entry.msgstr_plural[0] = translated
        else:
            entry.msgstr = translated
        entry.fuzzy = False
        print("[%d/%d] -> %s" % (i, len(to_translate), translated[:60]))
        time.sleep(0.1)  # 简单限速，避免触发 DeepL 限流

    po.save(PO_FILE)
    if failures:
        # 失败时以非 0 退出，让 workflow 中止，避免把英文/空词条错误推送
        print("有 %d 个词条翻译失败，已保持待翻译状态，未写入英文。", file=sys.stderr)
        print("请检查 DEEPL_API_KEY 后重新触发。", file=sys.stderr)
        sys.exit(1)
    print("翻译完成，已保存 %s" % PO_FILE)


if __name__ == "__main__":
    main()
