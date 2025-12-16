# 将当前工作目录递归地压缩为 zip 文件
# 同时忽略指定的文件夹

import os
import zipfile

IGNORED_DIRS: list[str] = ['.venv', '__pycache__', '.vscode', 'dist']
OUT_FILE: str = 'dist/code.zip'

def should_ignore(path: str) -> bool:
    """判断路径是否应该被忽略"""
    for ignored_dir in IGNORED_DIRS:
        if ignored_dir in path.split(os.sep):
            return True
    return False

def zip_directory(directory: str, output_file: str) -> None:
    """递归压缩目录为 zip 文件"""
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            # 过滤掉需要忽略的文件夹
            dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d))]
            for file in files:
                file_path = os.path.join(root, file)
                if not should_ignore(file_path):
                    # 将文件写入 zip 文件，保持相对路径
                    arcname = os.path.relpath(file_path, directory)
                    zipf.write(file_path, arcname)

if __name__ == '__main__':
    # 确保输出目录存在
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    # 压缩当前工作目录
    zip_directory('.', OUT_FILE)
    print(f"目录已成功压缩为 {OUT_FILE}")