# 修复Git中文乱码问题

## 问题说明

在Windows PowerShell中，Git提交信息中的中文可能显示为乱码。这是因为PowerShell默认使用GBK编码，而Git使用UTF-8编码。

## 解决方案

### 方法1：配置Git使用UTF-8（推荐）

已执行的配置命令：

```bash
git config --global core.quotepath false
git config --global i18n.commitencoding utf-8
git config --global i18n.logoutputencoding utf-8
```

### 方法2：设置PowerShell编码

在PowerShell中执行：

```powershell
# 设置控制台输出编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001

# 然后查看Git日志
git log --oneline -5
```

### 方法3：使用Git Bash

使用Git Bash（而不是PowerShell）可以避免编码问题：

1. 右键项目文件夹
2. 选择 "Git Bash Here"
3. 执行 `git log --oneline -5`

### 方法4：使用Python脚本查看

已创建 `view_commits.py` 脚本，可以正确显示中文提交信息：

```bash
python view_commits.py
```

## 验证配置

检查Git配置：

```bash
git config --global --list | findstr encoding
```

应该看到：
```
i18n.commitencoding=utf-8
i18n.logoutputencoding=utf-8
core.quotepath=false
```

## 后续提交

配置完成后，新的提交信息应该能正确显示。如果仍有问题，可以使用英文提交信息：

```bash
git commit -m "Add new feature"
```

## 查看已存在的提交

即使提交信息显示为乱码，实际的提交信息在Git中是正确的。可以通过以下方式查看：

1. 使用 `view_commits.py` 脚本
2. 使用Git Bash
3. 在GitHub网页上查看（推送到GitHub后）

