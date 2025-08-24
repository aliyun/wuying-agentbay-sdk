# 故障排除指南

本指南帮助你快速诊断和解决使用AgentBay SDK时遇到的常见问题。

## 🚨 紧急问题快速诊断

### 第一步：基础检查
运行以下诊断代码来快速识别问题：

```python
import os
from agentbay import AgentBay

def quick_diagnosis():
    print("=== AgentBay 快速诊断 ===")
    
    # 1. 检查API密钥
    api_key = os.getenv('AGENTBAY_API_KEY')
    if not api_key:
        print("❌ 未设置AGENTBAY_API_KEY环境变量")
        return False
    else:
        print(f"✅ API密钥已设置 (长度: {len(api_key)})")
    
    # 2. 测试连接
    try:
        agent_bay = AgentBay()
        print("✅ AgentBay客户端初始化成功")
    except Exception as e:
        print(f"❌ 客户端初始化失败: {e}")
        return False
    
    # 3. 测试会话创建
    try:
        result = agent_bay.create()
        if result.is_error:
            print(f"❌ 会话创建失败: {result.error}")
            return False
        else:
            print("✅ 会话创建成功")
            session = result.session
    except Exception as e:
        print(f"❌ 会话创建异常: {e}")
        return False
    
    # 4. 测试基本命令
    try:
        cmd_result = session.command.execute("echo 'Hello AgentBay'")
        if cmd_result.is_error:
            print(f"❌ 命令执行失败: {cmd_result.error}")
            return False
        else:
            print("✅ 命令执行成功")
    except Exception as e:
        print(f"❌ 命令执行异常: {e}")
        return False
    
    print("🎉 所有基础功能正常！")
    return True

# 运行诊断
quick_diagnosis()
```

## 🔧 安装和配置问题

### 问题：包安装失败

#### Python包安装问题
```bash
# 症状
pip install wuying-agentbay-sdk
# ERROR: Could not find a version that satisfies the requirement

# 解决方案
# 1. 更新pip
pip install --upgrade pip

# 2. 检查Python版本（需要3.7+）
python --version

# 3. 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple wuying-agentbay-sdk

# 4. 如果仍然失败，尝试从源码安装
pip install git+https://github.com/aliyun/wuying-agentbay-sdk.git#subdirectory=python
```

#### TypeScript/Node.js包安装问题
```bash
# 症状
npm install wuying-agentbay-sdk
# npm ERR! 404 Not Found

# 解决方案
# 1. 检查Node.js版本（需要14+）
node --version

# 2. 清理npm缓存
npm cache clean --force

# 3. 使用yarn替代
yarn add wuying-agentbay-sdk

# 4. 检查npm registry
npm config get registry
npm config set registry https://registry.npmjs.org/
```

#### Golang包安装问题
```bash
# 症状
go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay
# go: module github.com/aliyun/wuying-agentbay-sdk not found

# 解决方案
# 1. 检查Go版本（需要1.18+）
go version

# 2. 设置GOPROXY
go env -w GOPROXY=https://goproxy.cn,direct

# 3. 清理模块缓存
go clean -modcache

# 4. 重新获取
go mod tidy
go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay
```

### 问题：API密钥配置

#### 环境变量设置问题
```bash
# 症状：获取不到API密钥
print(os.getenv('AGENTBAY_API_KEY'))  # None

# 解决方案
# 1. 检查环境变量设置
echo $AGENTBAY_API_KEY

# 2. 临时设置（当前会话）
export AGENTBAY_API_KEY=your-api-key-here

# 3. 永久设置（添加到.bashrc或.zshrc）
echo 'export AGENTBAY_API_KEY=your-api-key-here' >> ~/.bashrc
source ~/.bashrc

# 4. Windows设置
set AGENTBAY_API_KEY=your-api-key-here

# 5. Python中动态设置
import os
os.environ['AGENTBAY_API_KEY'] = 'your-api-key-here'
```

#### API密钥验证问题
```python
# 症状：API密钥无效
# AgentBayError: Invalid API key

# 解决方案
def validate_api_key():
    api_key = os.getenv('AGENTBAY_API_KEY')
    
    # 1. 检查密钥格式
    if not api_key:
        print("❌ API密钥未设置")
        return False
    
    if len(api_key) < 20:
        print("❌ API密钥长度异常，可能不完整")
        return False
    
    # 2. 检查密钥字符
    if not api_key.replace('-', '').replace('_', '').isalnum():
        print("❌ API密钥包含异常字符")
        return False
    
    # 3. 测试密钥有效性
    try:
        agent_bay = AgentBay(api_key=api_key)
        result = agent_bay.create()
        if result.is_error:
            print(f"❌ API密钥无效: {result.error}")
            return False
        print("✅ API密钥有效")
        return True
    except Exception as e:
        print(f"❌ API密钥验证失败: {e}")
        return False

validate_api_key()
```

## 🌐 网络连接问题

### 问题：连接超时

```python
# 症状
# requests.exceptions.ConnectTimeout: HTTPSConnectionPool

# 解决方案
import requests
from agentbay import AgentBay

def test_network_connectivity():
    print("=== 网络连接诊断 ===")
    
    # 1. 测试基础网络
    try:
        response = requests.get('https://www.baidu.com', timeout=5)
        print("✅ 基础网络连接正常")
    except Exception as e:
        print(f"❌ 基础网络连接失败: {e}")
        return False
    
    # 2. 测试AgentBay服务端点
    try:
        # 这里需要替换为实际的AgentBay API端点
        response = requests.get('https://agentbay-api.aliyun.com/health', timeout=10)
        print("✅ AgentBay服务可达")
    except Exception as e:
        print(f"❌ AgentBay服务不可达: {e}")
        print("可能的解决方案：")
        print("- 检查防火墙设置")
        print("- 检查代理配置")
        print("- 尝试使用VPN")
        return False
    
    return True

# 配置代理（如果需要）
def configure_proxy():
    proxies = {
        'http': 'http://proxy.company.com:8080',
        'https': 'https://proxy.company.com:8080'
    }
    
    # 设置环境变量
    os.environ['HTTP_PROXY'] = proxies['http']
    os.environ['HTTPS_PROXY'] = proxies['https']
    
    # 或者在AgentBay初始化时传入
    agent_bay = AgentBay(proxies=proxies)
```

### 问题：SSL证书错误

```python
# 症状
# ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]

# 临时解决方案（不推荐生产环境）
import ssl
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 永久解决方案
def fix_ssl_issues():
    # 1. 更新证书
    # macOS
    # /Applications/Python\ 3.x/Install\ Certificates.command
    
    # Ubuntu/Debian
    # sudo apt-get update && sudo apt-get install ca-certificates
    
    # CentOS/RHEL
    # sudo yum update ca-certificates
    
    # 2. 设置证书路径
    import certifi
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
```

## 💻 会话和执行问题

### 问题：会话创建失败

```python
# 症状
result = agent_bay.create()
if result.is_error:
    print(result.error)  # Session creation failed

# 诊断和解决
def diagnose_session_creation():
    agent_bay = AgentBay()
    
    # 1. 检查账户状态
    try:
        # 假设有账户信息API
        account_info = agent_bay.get_account_info()
        print(f"账户状态: {account_info.status}")
        print(f"剩余配额: {account_info.quota}")
    except Exception as e:
        print(f"无法获取账户信息: {e}")
    
    # 2. 尝试不同的会话参数
    try:
        # 最小配置
        result = agent_bay.create()
        if result.is_error:
            print(f"默认配置失败: {result.error}")
            
            # 尝试指定镜像
            from agentbay import CreateSessionParams
            params = CreateSessionParams(image="ubuntu:20.04")
            result = agent_bay.create(params)
            if result.is_error:
                print(f"指定镜像失败: {result.error}")
            else:
                print("✅ 指定镜像成功")
        else:
            print("✅ 默认配置成功")
    except Exception as e:
        print(f"会话创建异常: {e}")

diagnose_session_creation()
```

### 问题：命令执行失败

```python
# 症状
result = session.command.execute("ls -la")
if result.is_error:
    print(result.error)

# 诊断和解决
def diagnose_command_execution(session):
    print("=== 命令执行诊断 ===")
    
    # 1. 测试基础命令
    basic_commands = ["pwd", "whoami", "echo 'test'", "ls"]
    
    for cmd in basic_commands:
        try:
            result = session.command.execute(cmd)
            if result.is_error:
                print(f"❌ {cmd}: {result.error}")
            else:
                print(f"✅ {cmd}: {result.data.stdout.strip()}")
        except Exception as e:
            print(f"❌ {cmd} 异常: {e}")
    
    # 2. 检查环境
    env_commands = [
        "echo $PATH",
        "which python",
        "python --version",
        "which pip",
        "df -h",
        "free -h"
    ]
    
    print("\n=== 环境信息 ===")
    for cmd in env_commands:
        try:
            result = session.command.execute(cmd)
            if not result.is_error:
                print(f"{cmd}: {result.data.stdout.strip()}")
        except:
            pass

# 使用示例
session = agent_bay.create().session
diagnose_command_execution(session)
```

### 问题：文件操作失败

```python
# 症状
result = session.file_system.write_file("/path/file.txt", "content")
if result.is_error:
    print(result.error)  # Permission denied 或 No such file or directory

# 解决方案
def safe_file_operations(session):
    # 1. 检查目录权限
    def check_directory_permissions(path):
        dir_path = path.rsplit('/', 1)[0] if '/' in path else '.'
        result = session.command.execute(f"ls -ld {dir_path}")
        if not result.is_error:
            print(f"目录权限: {result.data.stdout.strip()}")
        
        # 确保目录存在
        session.command.execute(f"mkdir -p {dir_path}")
    
    # 2. 安全写入文件
    def safe_write_file(file_path, content):
        try:
            # 检查目录
            check_directory_permissions(file_path)
            
            # 尝试写入
            result = session.file_system.write_file(file_path, content)
            if result.is_error:
                # 尝试使用临时目录
                temp_path = f"/tmp/{file_path.split('/')[-1]}"
                result = session.file_system.write_file(temp_path, content)
                if not result.is_error:
                    print(f"文件已写入临时目录: {temp_path}")
                    return temp_path
            return file_path if not result.is_error else None
        except Exception as e:
            print(f"文件写入异常: {e}")
            return None
    
    # 3. 测试文件操作
    test_content = "Hello AgentBay Test"
    test_paths = [
        "/tmp/test.txt",
        "/home/test.txt",
        "./test.txt"
    ]
    
    for path in test_paths:
        result_path = safe_write_file(path, test_content)
        if result_path:
            # 验证读取
            read_result = session.file_system.read_file(result_path)
            if not read_result.is_error and read_result.data == test_content:
                print(f"✅ 文件操作成功: {result_path}")
                break
            else:
                print(f"❌ 文件读取失败: {path}")
        else:
            print(f"❌ 文件写入失败: {path}")

# 使用示例
safe_file_operations(session)
```

## 🔄 上下文和持久化问题

### 问题：上下文创建失败

```python
# 症状
context_result = agent_bay.context.get("my-context", create=True)
if context_result.is_error:
    print(context_result.error)

# 解决方案
def diagnose_context_issues(agent_bay):
    print("=== 上下文诊断 ===")
    
    # 1. 列出现有上下文
    try:
        contexts = agent_bay.context.list()
        if not contexts.is_error:
            print(f"现有上下文数量: {len(contexts.data)}")
            for ctx in contexts.data[:5]:  # 显示前5个
                print(f"- {ctx.name} ({ctx.id})")
        else:
            print(f"❌ 无法列出上下文: {contexts.error}")
    except Exception as e:
        print(f"❌ 上下文列表异常: {e}")
    
    # 2. 测试上下文创建
    test_name = f"test-context-{int(time.time())}"
    try:
        result = agent_bay.context.get(test_name, create=True)
        if result.is_error:
            print(f"❌ 上下文创建失败: {result.error}")
        else:
            print(f"✅ 上下文创建成功: {result.context.id}")
            
            # 清理测试上下文
            delete_result = agent_bay.context.delete(result.context.id)
            if not delete_result.is_error:
                print("✅ 测试上下文已清理")
    except Exception as e:
        print(f"❌ 上下文创建异常: {e}")

diagnose_context_issues(agent_bay)
```

### 问题：数据同步失败

```python
# 症状：数据没有在会话间保持

# 解决方案
def test_data_persistence(agent_bay):
    from agentbay import ContextSync, SyncPolicy, CreateSessionParams
    
    print("=== 数据持久化测试 ===")
    
    # 1. 创建上下文
    context_name = f"persistence-test-{int(time.time())}"
    context_result = agent_bay.context.get(context_name, create=True)
    
    if context_result.is_error:
        print(f"❌ 上下文创建失败: {context_result.error}")
        return
    
    context = context_result.context
    print(f"✅ 上下文创建成功: {context.id}")
    
    # 2. 创建同步配置
    sync_policy = SyncPolicy.default()
    context_sync = ContextSync.new(context.id, "/mnt/data", sync_policy)
    
    # 3. 第一个会话 - 写入数据
    params = CreateSessionParams(context_syncs=[context_sync])
    session1_result = agent_bay.create(params)
    
    if session1_result.is_error:
        print(f"❌ 会话1创建失败: {session1_result.error}")
        return
    
    session1 = session1_result.session
    test_data = f"Test data at {time.time()}"
    
    write_result = session1.file_system.write_file("/mnt/data/test.txt", test_data)
    if write_result.is_error:
        print(f"❌ 数据写入失败: {write_result.error}")
        return
    
    print("✅ 数据写入成功")
    
    # 4. 第二个会话 - 读取数据
    session2_result = agent_bay.create(params)
    if session2_result.is_error:
        print(f"❌ 会话2创建失败: {session2_result.error}")
        return
    
    session2 = session2_result.session
    
    # 等待同步
    time.sleep(2)
    
    read_result = session2.file_system.read_file("/mnt/data/test.txt")
    if read_result.is_error:
        print(f"❌ 数据读取失败: {read_result.error}")
    elif read_result.data == test_data:
        print("✅ 数据持久化成功")
    else:
        print(f"❌ 数据不一致: 期望 '{test_data}', 实际 '{read_result.data}'")
    
    # 5. 清理
    agent_bay.context.delete(context.id)
    print("✅ 测试上下文已清理")

test_data_persistence(agent_bay)
```

## 🐛 代码执行问题

### 问题：Python代码执行失败

```python
# 症状
code = "import numpy as np\nprint(np.array([1,2,3]))"
result = session.code.run_code(code, "python")
if result.is_error:
    print(result.error)  # ModuleNotFoundError: No module named 'numpy'

# 解决方案
def fix_python_environment(session):
    print("=== Python环境修复 ===")
    
    # 1. 检查Python版本
    result = session.command.execute("python --version")
    if not result.is_error:
        print(f"Python版本: {result.data.stdout.strip()}")
    
    # 2. 检查pip
    result = session.command.execute("pip --version")
    if result.is_error:
        print("❌ pip未安装，尝试安装...")
        session.command.execute("apt-get update && apt-get install -y python3-pip")
    
    # 3. 安装常用包
    common_packages = ["numpy", "pandas", "requests", "matplotlib"]
    for package in common_packages:
        print(f"安装 {package}...")
        result = session.command.execute(f"pip install {package}")
        if result.is_error:
            print(f"❌ {package} 安装失败: {result.error}")
        else:
            print(f"✅ {package} 安装成功")
    
    # 4. 测试导入
    test_code = """
import sys
print("Python路径:", sys.path)
try:
    import numpy
    print("✅ numpy可用")
except ImportError:
    print("❌ numpy不可用")
"""
    
    result = session.code.run_code(test_code, "python")
    if not result.is_error:
        print("测试结果:")
        print(result.data.stdout)

fix_python_environment(session)
```

### 问题：JavaScript代码执行失败

```python
# 症状
code = "const fs = require('fs'); console.log('Hello');"
result = session.code.run_code(code, "javascript")
if result.is_error:
    print(result.error)

# 解决方案
def fix_nodejs_environment(session):
    print("=== Node.js环境修复 ===")
    
    # 1. 检查Node.js
    result = session.command.execute("node --version")
    if result.is_error:
        print("❌ Node.js未安装，尝试安装...")
        install_commands = [
            "curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -",
            "apt-get install -y nodejs"
        ]
        for cmd in install_commands:
            session.command.execute(cmd)
    else:
        print(f"✅ Node.js版本: {result.data.stdout.strip()}")
    
    # 2. 检查npm
    result = session.command.execute("npm --version")
    if not result.is_error:
        print(f"✅ npm版本: {result.data.stdout.strip()}")
    
    # 3. 测试基础功能
    test_code = """
console.log("Node.js版本:", process.version);
console.log("当前目录:", process.cwd());
console.log("✅ JavaScript执行正常");
"""
    
    result = session.code.run_code(test_code, "javascript")
    if not result.is_error:
        print("测试结果:")
        print(result.data.stdout)
    else:
        print(f"❌ JavaScript测试失败: {result.error}")

fix_nodejs_environment(session)
```

## 📊 性能问题

### 问题：操作响应慢

```python
# 诊断性能问题
import time

def performance_diagnosis(session):
    print("=== 性能诊断 ===")
    
    # 1. 测试命令执行速度
    commands = [
        "echo 'test'",
        "ls",
        "pwd",
        "date"
    ]
    
    for cmd in commands:
        start_time = time.time()
        result = session.command.execute(cmd)
        end_time = time.time()
        
        if not result.is_error:
            print(f"✅ {cmd}: {end_time - start_time:.2f}秒")
        else:
            print(f"❌ {cmd}: 失败")
    
    # 2. 测试文件操作速度
    test_content = "x" * 1024  # 1KB
    start_time = time.time()
    
    write_result = session.file_system.write_file("/tmp/perf_test.txt", test_content)
    write_time = time.time() - start_time
    
    if not write_result.is_error:
        start_time = time.time()
        read_result = session.file_system.read_file("/tmp/perf_test.txt")
        read_time = time.time() - start_time
        
        if not read_result.is_error:
            print(f"✅ 文件写入: {write_time:.2f}秒")
            print(f"✅ 文件读取: {read_time:.2f}秒")
    
    # 3. 测试代码执行速度
    python_code = "print('Hello from Python')"
    start_time = time.time()
    
    code_result = session.code.run_code(python_code, "python")
    code_time = time.time() - start_time
    
    if not code_result.is_error:
        print(f"✅ Python代码执行: {code_time:.2f}秒")

performance_diagnosis(session)
```

## 🆘 获取帮助

### 收集诊断信息

当你需要寻求帮助时，请运行以下脚本收集诊断信息：

```python
def collect_diagnostic_info():
    import sys
    import platform
    
    print("=== AgentBay 诊断信息 ===")
    print(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python版本: {sys.version}")
    print(f"操作系统: {platform.system()} {platform.release()}")
    
    # SDK版本
    try:
        import agentbay
        print(f"AgentBay SDK版本: {agentbay.__version__}")
    except:
        print("AgentBay SDK版本: 未知")
    
    # 环境变量
    api_key = os.getenv('AGENTBAY_API_KEY')
    print(f"API密钥设置: {'是' if api_key else '否'}")
    
    # 网络测试
    try:
        import requests
        response = requests.get('https://www.baidu.com', timeout=5)
        print(f"网络连接: 正常 ({response.status_code})")
    except:
        print("网络连接: 异常")
    
    # 基础功能测试
    try:
        agent_bay = AgentBay()
        result = agent_bay.create()
        if result.is_error:
            print(f"会话创建: 失败 - {result.error}")
        else:
            print("会话创建: 成功")
    except Exception as e:
        print(f"会话创建: 异常 - {e}")
    
    print("=== 诊断信息收集完成 ===")

collect_diagnostic_info()
```

### 提交问题

如果问题仍未解决，请：

1. **运行诊断脚本**并保存输出
2. **准备最小复现代码**
3. **访问** [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
4. **创建新Issue**，包含：
   - 问题描述
   - 预期行为
   - 实际行为
   - 诊断信息
   - 复现代码

### 社区资源

- [GitHub Discussions](https://github.com/aliyun/wuying-agentbay-sdk/discussions) - 社区讨论
- [常见问题FAQ](faq.md) - 常见问题解答
- [官方文档](https://agentbay.console.aliyun.com) - 完整文档

---

记住：大多数问题都有解决方案，不要放弃！如果遇到困难，社区随时准备帮助你。 