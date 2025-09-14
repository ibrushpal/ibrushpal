# Git拉取失败手动解决方案

## 问题原因
`error: RPC failed; curl 16 Error in the HTTP2 framing layer` 是Git的HTTP2协议问题，通常由于网络环境或服务器配置导致。

## 解决方案

### 方法一：禁用HTTP2（推荐）
```bash
# 禁用HTTP2协议
git config --global http.version HTTP/1.1

# 重新拉取
git pull origin main
```

### 方法二：手动下载ZIP
```bash
# 1. 下载最新代码ZIP包
wget https://github.com/ibrushpal/ibrushpal/archive/refs/heads/main.zip

# 2. 解压
unzip main.zip

# 3. 复制文件（保留.git目录）
cp -r ibrushpal-main/* .
cp -r ibrushpal-main/.* . 2>/dev/null || true

# 4. 清理
rm -rf main.zip ibrushpal-main
```

### 方法三：使用浅层克隆
```bash
# 创建临时目录下载
git clone --depth 1 https://github.com/ibrushpal/ibrushpal.git temp_dir

# 复制文件
cp -r temp_dir/* .
cp -r temp_dir/.* . 2>/dev/null || true

# 清理
rm -rf temp_dir
```

### 方法四：Git配置优化
```bash
# 增加缓冲区大小
git config --global http.postBuffer 1048576000

# 禁用压缩
git config --global core.compression 0

# 设置低速度限制
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999
```

## 验证修复
```bash
# 测试Git连接
git ls-remote origin

# 尝试拉取
git fetch --depth 1
```

## 预防措施
```bash
# 永久禁用HTTP2
echo 'export GIT_HTTP_VERSION=HTTP/1.1' >> ~/.bashrc
source ~/.bashrc
```

如果所有方法都失败，考虑网络环境问题或联系服务器提供商。