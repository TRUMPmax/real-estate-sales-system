"""
查看Git提交历史（解决中文乱码问题）
"""
import subprocess
import sys

# 设置UTF-8编码
if sys.platform == 'win32':
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'

try:
    # 获取提交历史
    result = subprocess.run(
        ['git', 'log', '--oneline', '--all', '-10'],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    print("=" * 80)
    print("Git Commit History (Last 10 commits)")
    print("=" * 80)
    print()
    
    if result.returncode == 0:
        commits = result.stdout.strip().split('\n')
        for i, commit in enumerate(commits, 1):
            if commit:
                parts = commit.split(' ', 1)
                if len(parts) == 2:
                    hash_id = parts[0]
                    message = parts[1]
                    print(f"{i}. [{hash_id[:7]}] {message}")
                else:
                    print(f"{i}. {commit}")
    else:
        print("Error:", result.stderr)
    
    print()
    print("=" * 80)
    
    # 获取详细提交信息
    print("\n详细提交信息:")
    print("=" * 80)
    result = subprocess.run(
        ['git', 'log', '--format=%H|%an|%ae|%ad|%s', '--date=short', '-5'],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    if result.returncode == 0:
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) >= 5:
                    print(f"Hash: {parts[0][:7]}")
                    print(f"Author: {parts[1]} <{parts[2]}>")
                    print(f"Date: {parts[3]}")
                    print(f"Message: {parts[4]}")
                    print("-" * 80)

except Exception as e:
    print(f"Error: {e}")

