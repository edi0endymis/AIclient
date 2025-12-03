# check_old_memory_blocks.py
import re

with open("app.py", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()

# 旧插入块识别关键字
patterns = [
    r"START 插入",
    r"SummaryMemory",
    r"mem\.add\(.*meta=",
    r"summary\.add_message",
    r"summary\.update"
]

print("开始扫描 app.py 中的旧 memory/summary 冗余代码块:\n")

for i, line in enumerate(lines, start=1):
    for p in patterns:
        if re.search(p, line):
            print(f"疑似旧逻辑行: {i} → {line.strip()}")
            break

print("\n扫描完毕。")
print("这些行不会被自动删除，请把输出复制给我，我会告诉你哪一些需要删。")
