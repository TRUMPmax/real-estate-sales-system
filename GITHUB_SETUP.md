# GitHub 仓库设置指南

## 第一步：在GitHub上创建仓库

1. 登录 GitHub
2. 点击右上角的 "+" 号，选择 "New repository"
3. 填写仓库信息：
   - Repository name: `real-estate-sales-system` (或你喜欢的名称)
   - Description: `房地产销售管理系统 - Django Web应用`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"（因为我们已经有了代码）
4. 点击 "Create repository"

## 第二步：连接本地仓库到GitHub

在项目目录下执行以下命令（将 `YOUR_USERNAME` 和 `YOUR_REPO_NAME` 替换为你的实际信息）：

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 或者使用SSH（如果你配置了SSH密钥）
# git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git

# 推送代码到GitHub
git branch -M main
git push -u origin main
```

## 第三步：验证

访问你的GitHub仓库页面，应该能看到所有代码文件。

## 后续更新代码

```bash
git add .
git commit -m "描述你的更改"
git push
```

## 恢复代码

如果需要恢复到当前版本：

```bash
git log  # 查看提交历史
git checkout <commit-hash>  # 恢复到指定版本
```

或者直接：
```bash
git reset --hard HEAD  # 恢复到最新提交
```

