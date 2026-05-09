# ==================== Git-Linux 命令与上传指南 ====================
# 作者：学习中
# 日期：2026年
# 用途：记录 Git、Linux 命令及 VS Code 上传方法，方便复习

# ==================== 第一章：VS Code 连接 GitHub/Gitee 上传指南 ====================
# 【知识点总结】
# 通过 VS Code 的源代码管理功能，可以方便地将本地代码同步到 GitHub 和 Gitee
# 核心流程：下载 Git → 注册账号 → 配置 Git → 创建远程仓库 → 本地初始化 → 上传代码

## 1.1 准备工作

### 1.1.1 下载并安装 Git
1. 访问 Git 官方网站：https://git-scm.com/downloads
2. 根据操作系统选择对应版本下载（Windows/macOS/Linux）
3. 安装时保持默认选项即可，安装完成后打开命令行验证：
   ```bash
   git --version    # 显示 Git 版本号表示安装成功
   ```

### 1.1.2 注册 GitHub 和 Gitee 账号
1. **注册 GitHub**：访问 https://github.com/，使用邮箱注册账号
2. **注册 Gitee**：访问 https://gitee.com/，使用**与 GitHub 相同的用户名和邮箱**注册
3. 注意：两个平台使用相同的用户名和邮箱，便于统一管理

## 1.2 配置 Git 用户名和邮箱

打开命令行（Windows 用 Git Bash 或 CMD），配置全局用户名和邮箱：

```bash
git config --global user.name "你的用户名"    # 例如：git config --global user.name "zhangsan"
git config --global user.email "你的邮箱"     # 例如：git config --global user.email "zhangsan@example.com"
```

验证配置是否成功：
```bash
git config --list    # 查看所有配置项，确认 user.name 和 user.email 已设置
```

## 1.3 GitHub 网络配置（针对国内用户）

由于 GitHub 在国内访问较慢，可配置端口加速：

```bash
# 配置 GitHub 使用 443 端口
git config --global http.https://github.com.proxy socks5://127.0.0.1:10808
git config --global https.https://github.com.proxy socks5://127.0.0.1:10808

# 如需取消代理
# git config --global --unset http.https://github.com.proxy
# git config --global --unset https.https://github.com.proxy
```

> **注意**：Gitee 在国内访问通常无需特殊配置，保持默认即可

## 1.4 在远程平台创建仓库

### 1.4.1 在 GitHub 创建仓库
1. 登录 GitHub，点击右上角 "+" → "New repository"
2. 填写仓库信息：
   - Repository name：仓库名称（如：my-project）
   - Description：仓库描述（可选）
   - 选择 Public 或 Private
   - 勾选 "Add a README file"（可选，建议勾选）
3. 点击 "Create repository" 完成创建

### 1.4.2 在 Gitee 创建仓库
1. 登录 Gitee，点击右上角 "+" → "新建仓库"
2. 填写仓库信息：
   - 仓库名称：建议与 GitHub 仓库名**不同**（方便区分），如：my-project-gitee
   - 仓库描述（可选）
   - 选择开源或私有
   - 勾选 "初始化 README 文件"（可选）
3. 点击 "创建" 完成创建

## 1.5 使用 VS Code 上传代码到远程仓库

### 1.5.1 打开本地项目
1. 打开 VS Code
2. 点击左侧 "资源管理器" → "打开文件夹"，选择你的项目目录

### 1.5.2 初始化本地仓库
1. 点击左侧 "源代码管理" 图标（Ctrl+Shift+G）
2. 点击 "初始化仓库" → 选择当前项目目录
3. 此时 VS Code 会在项目目录创建 `.git` 文件夹

### 1.5.3 添加远程仓库

#### 添加 GitHub 远程仓库（命名为 origin）
1. 复制 GitHub 仓库的 HTTPS 地址（如：https://github.com/用户名/my-project.git）
2. 打开 VS Code 终端（Ctrl+`），执行：
   ```bash
   git remote add origin https://github.com/用户名/my-project.git
   ```

#### 添加 Gitee 远程仓库（命名为 gitee）
1. 复制 Gitee 仓库的 HTTPS 地址（如：https://gitee.com/用户名/my-project-gitee.git）
2. 在终端执行：
   ```bash
   git remote add gitee https://gitee.com/用户名/my-project-gitee.git
   ```

#### 查看远程仓库配置
```bash
git remote -v    # 会显示两个远程仓库：origin 和 gitee
```

### 1.5.4 提交并推送代码

#### 第一次推送步骤
1. 在 VS Code 源代码管理界面，输入提交信息（如："Initial commit"）
2. 点击 "√" 按钮提交到本地仓库
3. 点击 "..." → "推送"，选择要推送的分支（通常是 main 或 master）
4. 首次推送可能需要输入 GitHub/Gitee 的账号密码或使用 Token

#### 推送到两个远程仓库
```bash
# 推送到 GitHub（origin）
git push -u origin main

# 推送到 Gitee（gitee）
git push -u gitee main
```

> **注意**：`-u` 参数表示建立本地分支与远程分支的关联，后续推送可直接使用 `git push`

### 1.5.5 日常开发流程
1. **修改代码**：在 VS Code 中编辑文件
2. **查看状态**：源代码管理界面会显示修改的文件
3. **暂存修改**：点击文件旁的 "+" 号，或使用 `git add .`
4. **提交到本地**：输入提交信息，点击 "√" 提交
5. **推送到远程**：点击 "..." → "推送"，或使用命令：
   ```bash
   git push origin main    # 推送到 GitHub
   git push gitee main     # 推送到 Gitee
   ```

## 1.6 常见问题与注意事项

### 注意事项
1. **仓库命名**：两个远程仓库名称必须不同（如 origin 和 gitee），否则会覆盖
2. **同步更新**：本地修改后必须执行推送操作，代码才会同步到云端
3. **Token 认证**：GitHub 已不再支持密码认证，需使用 Personal Access Token
4. **分支名称**：不同平台默认分支可能不同（main 或 master），需注意对应

### 获取 GitHub Personal Access Token
1. 登录 GitHub → 点击头像 → Settings → Developer settings
2. 点击 Personal access tokens → Generate new token
3. 设置 token 名称、有效期，勾选必要权限（如 repo）
4. 复制生成的 token（只显示一次，务必保存）
5. 推送时代码时，用户名输入 GitHub 用户名，密码输入此 token

### 获取 Gitee 私人令牌
1. 登录 Gitee → 点击头像 → 设置 → 私人令牌
2. 点击 "生成新令牌"，设置描述和有效期
3. 复制令牌并保存
4. 推送时代码时使用此令牌作为密码

# ==================== 第二章：Linux 常见命令 ====================
# 【知识点总结】
# Linux 命令是操作服务器和开发环境的必备技能
# 命令格式：命令名 [选项] [参数]

## 2.1 文件与目录操作

### 目录导航
ls              # 列出当前目录内容
ls -l           # 显示详细信息（权限、所有者、大小、时间）
ls -a           # 显示隐藏文件和目录（以 . 开头）
ls -la          # 组合选项：显示所有文件的详细信息
ls -h           # 人性化显示文件大小（KB、MB 等）
ls -t           # 按修改时间排序
ls -r           # 反向排序

cd 目录名        # 切换到指定目录
cd ..           # 返回上一级目录
cd ~            # 回到用户主目录
cd /            # 回到根目录
pwd             # 显示当前所在路径

### 文件操作
cat 文件名       # 查看文件内容（适合小文件）
more 文件名      # 分页查看文件（空格翻页，q 退出）
less 文件名      # 分页查看文件（支持上下键，更灵活）
head 文件名      # 查看文件前几行（默认前10行）
head -n 20 文件名 # 查看前20行
tail 文件名      # 查看文件末尾几行
tail -f 文件名   # 实时监控文件更新（日志文件常用）

cp 源文件 目标文件  # 复制文件
cp -r 源目录 目标目录 # 复制目录（递归）
mv 源文件 目标文件  # 移动文件或重命名
rm 文件名        # 删除文件（需确认）
rm -f 文件名     # 强制删除文件（不提示）
rm -r 目录名     # 删除目录及其内容
rm -rf 目录名    # 强制删除目录（危险操作！谨慎使用）

touch 文件名     # 创建空文件
mkdir 目录名     # 创建目录
mkdir -p 路径/目录 # 创建多级目录（如不存在则创建父目录）

### 文件权限
chmod +x 文件名  # 添加执行权限
chmod -x 文件名  # 取消执行权限
chmod 755 文件名 # 设置权限为 rwxr-xr-x
chmod 644 文件名 # 设置权限为 rw-r--r--
chown 用户:组 文件名 # 修改文件所有者

### 链接文件
ln -s 源文件 链接名  # 创建软链接（快捷方式）
ln 源文件 链接名     # 创建硬链接

## 2.2 系统信息与进程

whoami          # 显示当前用户名
uname -a        # 显示系统信息
df -h           # 查看磁盘空间使用情况
free -h         # 查看内存使用情况
top             # 实时查看系统进程（q 退出）
ps aux          # 查看当前进程列表
kill 进程ID     # 终止指定进程
kill -9 进程ID  # 强制终止进程

## 2.3 网络操作

ping 域名/IP    # 测试网络连通性
ifconfig        # 查看网络接口信息
ip addr         # 查看IP地址（新版命令）
curl 网址       # 发送 HTTP 请求
wget 下载链接   # 下载文件

## 2.4 搜索与查找

find 目录 -name "文件名"  # 按名称查找文件
grep "关键词" 文件名     # 在文件中搜索关键词
grep -r "关键词" 目录    # 递归搜索目录下所有文件
which 命令名    # 查找命令所在位置

## 2.5 压缩与解压

tar -czvf 压缩包名.tar.gz 目录 # 压缩目录为 gz 格式
tar -xzvf 压缩包名.tar.gz      # 解压 gz 格式压缩包
unzip 压缩包名.zip             # 解压 zip 格式
zip 压缩包名.zip 文件/目录     # 压缩为 zip 格式


# ==================== 第三章：Git 常见命令 ====================
# 【知识点总结】
# Git 是分布式版本控制系统，用于管理代码版本
# 核心概念：工作区、暂存区、本地仓库、远程仓库

## 3.1 仓库初始化

git init              # 在当前目录初始化 Git 仓库
git clone 仓库地址     # 克隆远程仓库到本地

## 3.2 基础操作

git status            # 查看工作区状态（哪些文件被修改/新增）
git add 文件名        # 将指定文件添加到暂存区
git add .             # 将所有修改添加到暂存区
git add -u            # 只添加已跟踪文件的修改

git commit -m "提交信息"  # 将暂存区内容提交到本地仓库
git commit -a -m "提交信息" # 跳过暂存区，直接提交已跟踪文件的修改

git log               # 查看提交历史（按时间倒序）
git log --oneline     # 简洁显示提交历史
git log --graph       # 显示分支合并图

## 3.3 分支操作

git branch            # 查看所有分支
git branch 分支名      # 创建新分支
git checkout 分支名    # 切换到指定分支
git checkout -b 分支名 # 创建并切换到新分支（常用）
git merge 分支名       # 将指定分支合并到当前分支
git branch -d 分支名   # 删除分支（需先合并）
git branch -D 分支名   # 强制删除分支

## 3.4 远程仓库操作

git remote           # 查看远程仓库列表
git remote -v        # 查看远程仓库详细信息
git remote add origin 仓库地址 # 添加远程仓库
git remote rm origin # 删除远程仓库

git push 远程仓库名 分支名 # 推送到远程仓库
git push -u origin main   # 首次推送并关联分支
git pull 远程仓库名 分支名 # 从远程仓库拉取更新

git fetch            # 获取远程仓库最新信息（不合并）
git merge origin/main # 将远程分支合并到本地

## 3.5 撤销与回退

git checkout -- 文件名 # 撤销工作区的修改（未暂存）
git reset HEAD 文件名  # 将暂存区的修改撤回到工作区
git reset --hard 提交ID # 强制回退到指定版本（慎用！会丢失本地修改）
git revert 提交ID      # 创建新提交来撤销指定提交（推荐方式）

## 3.6 标签操作

git tag              # 查看所有标签
git tag 标签名        # 创建轻量标签
git tag -a 标签名 -m "标签说明" # 创建带说明的标签
git push origin 标签名 # 推送标签到远程仓库

## 3.7 实用技巧

git stash            # 临时保存工作区（未提交的修改）
git stash pop        # 恢复最近一次保存的内容
git diff             # 查看工作区与暂存区的差异
git diff --cached    # 查看暂存区与本地仓库的差异
git config --list    # 查看 Git 配置信息
