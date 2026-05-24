#!/usr/bin/env python3
"""
从历史同类型日记中提取未完成的 Todo（从文件开头的全局 Todo 清单）。
用法: python carry_over_todos.py <日记根目录> <标记类型 workday|weekend>

输出 JSON:
{
  "found": 3,
  "todos": [
    {"text": "Agent 编排", "duration": "6 小时", "note": "", "source": "5.23.md"},
    {"text": "深度对话练习", "duration": "2 小时", "note": "", "source": "5.23.md"}
  ]
}
"""

import json
import os
import re
import sys


def extract_global_todos(content):
    """从日记内容中提取文件开头的全局 Todo 列表。"""
    lines = content.strip().split("\n")
    todos = []
    in_todo = False

    for line in lines:
        line_stripped = line.strip()

        # 找到 "## 可能的 Todo" 标题
        if line_stripped == "## 可能的 Todo":
            in_todo = True
            continue

        # 遇到下一个 ## 标题，结束 Todo 提取
        if in_todo and line_stripped.startswith("## "):
            break

        # 遇到空行，也结束 Todo 提取（防止跨段落）
        if in_todo and line_stripped == "":
            break

        if in_todo and line_stripped.startswith("-"):
            # 解析 "- 任务内容 - 时长（备注）"
            match = re.match(r"-\s*(.+?)\s+-\s*(.+?)$", line_stripped)
            if match:
                text = match.group(1).strip()
                rest = match.group(2).strip()
                note_match = re.match(r"(.+?)\s*（(.+?)）", rest)
                if note_match:
                    duration = note_match.group(1).strip()
                    note = note_match.group(2).strip()
                else:
                    duration = rest
                    note = ""
                todos.append({"text": text, "duration": duration, "note": note})
            else:
                # 没有 "- 时长" 格式的，如 "- 修复 push gateway 问题"
                text = line_stripped.lstrip("-").strip()
                todos.append({"text": text, "duration": "", "note": ""})

    return todos


def main():
    if len(sys.argv) < 3:
        print("用法: python carry_over_todos.py <日记根目录> <workday|weekend>", file=sys.stderr)
        sys.exit(1)

    root = sys.argv[1]
    tag = sys.argv[2]  # workday 或 weekend

    all_todos = []
    seen_texts = set()

    # 遍历所有 .md 文件
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if not fname.endswith(".md"):
                continue

            fpath = os.path.join(dirpath, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue

            # 检查第一行是否是目标标记
            first_line = content.split("\n")[0].strip() if content.strip() else ""
            if first_line != f"#{tag}":
                continue

            # 提取文件开头的全局 Todo
            todos = extract_global_todos(content)
            for todo in todos:
                # 去重：同类型日记中同一个 Todo 只保留一次（取最新文件的）
                if todo["text"] not in seen_texts:
                    seen_texts.add(todo["text"])
                    todo["source"] = fname
                    all_todos.append(todo)

    print(json.dumps({"found": len(all_todos), "todos": all_todos}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
