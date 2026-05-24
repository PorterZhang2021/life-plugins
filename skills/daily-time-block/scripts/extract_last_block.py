#!/usr/bin/env python3
"""
提取日记文件中最后一段时间块的结构化信息。
用法: python extract_last_block.py <日记文件路径>

输出 JSON:
{
  "found": true,
  "start_time": "8 点 41",
  "main_goal": {
    "task": "进行一小时计算机概念学习",
    "duration": "1 小时"
  },
  "actual_goal": "进行了一小时左右的计算机概念内容学习",
  "end_time": "09点 49",
  "is_closed": true
}
"""

import json
import re
import sys


def parse_duration(line):
    """从行文本中提取时长和备注。"""
    match = re.match(r"-\s*(.+?)\s+-\s*(.+?)$", line.strip())
    if not match:
        return None, None

    text = match.group(1).strip()
    rest = match.group(2).strip()

    note_match = re.match(r"(.+?)\s*（(.+?)）", rest)
    if note_match:
        duration = note_match.group(1).strip()
    else:
        duration = rest

    return text, duration


def extract_last_block(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 按空行分割成段落块
    blocks = re.split(r"\n\n+", content)

    # 找到包含"开始"的最后一段
    last_block_text = ""
    for block in reversed(blocks):
        if "开始" in block:
            last_block_text = block
            break

    if not last_block_text:
        return {"found": False}

    lines = last_block_text.strip().split("\n")
    result = {
        "found": True,
        "start_time": "",
        "main_goal": {"task": "", "duration": ""},
        "actual_goal": "",
        "end_time": "",
        "is_closed": False,
    }

    section = None  # 'main_goal' | 'actual_goal'

    for line in lines:
        line_stripped = line.strip()

        # 开始时间
        if "开始" in line_stripped and not line_stripped.startswith("-"):
            result["start_time"] = line_stripped.replace("开始", "").strip()
            continue

        # 主要目标
        if line_stripped == "主要目标：":
            section = "main_goal"
            continue

        # 实际目标
        if line_stripped == "实际目标：":
            section = "actual_goal"
            continue

        # 结束时间
        if "结束" in line_stripped and not line_stripped.startswith("-"):
            result["end_time"] = line_stripped.replace("结束", "").strip()
            result["is_closed"] = True
            continue

        # 处理列表项
        if line_stripped.startswith("-"):
            if section == "main_goal":
                text, duration = parse_duration(line_stripped)
                if text:
                    result["main_goal"] = {"task": text, "duration": duration or ""}
            elif section == "actual_goal":
                result["actual_goal"] = line_stripped.lstrip("-").strip()

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python extract_last_block.py <日记文件路径>", file=sys.stderr)
        sys.exit(1)

    result = extract_last_block(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
