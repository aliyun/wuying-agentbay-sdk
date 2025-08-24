# 文件操作完整指南

本指南提供AgentBay SDK文件操作的完整介绍，包括基本文件操作、目录管理、批量操作、权限管理和性能优化。

## 📋 目录

- [基本概念](#基本概念)
- [API速查表](#api速查表)
- [基本文件操作](#基本文件操作)
- [目录管理](#目录管理)
- [批量操作](#批量操作)
- [文件权限和属性](#文件权限和属性)
- [大文件处理](#大文件处理)
- [性能优化](#性能优化)
- [错误处理](#错误处理)
- [最佳实践](#最佳实践)

## 🎯 基本概念

### 文件系统结构

AgentBay会话提供完整的文件系统访问，支持不同操作系统：

#### Linux环境（默认）
```
/
├── tmp/          # 临时文件（推荐用于测试）
├── home/         # 用户目录
├── mnt/          # 挂载点（用于上下文同步）
├── etc/          # 系统配置
├── var/          # 可变数据
└── usr/          # 用户程序
```

#### Windows环境
```
C:\
├── temp\         # 临时文件
├── Users\        # 用户目录
├── Program Files\ # 程序文件
└── Windows\      # 系统文件
```

### 路径规范

- **Linux/Android**: 使用正斜杠 `/tmp/file.txt`
- **Windows**: 使用反斜杠 `C:\temp\file.txt` 或正斜杠 `C:/temp/file.txt`
- **推荐**: 优先使用绝对路径避免歧义

## 🚀 API速查表

### 基本操作

<details>
<summary><strong>Python</strong></summary>

```python
# 写入文件
result = session.file_system.write_file("/tmp/test.txt", "Hello World")

# 读取文件
result = session.file_system.read_file("/tmp/test.txt")
content = result.data

# 删除文件
result = session.file_system.delete_file("/tmp/test.txt")

# 列出目录
result = session.file_system.list_directory("/tmp")
files = result.data

# 检查文件是否存在
exists = session.file_system.file_exists("/tmp/test.txt")

# 获取文件信息
info = session.file_system.get_file_info("/tmp/test.txt")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// 写入文件
const result = await session.fileSystem.writeFile("/tmp/test.txt", "Hello World");

// 读取文件
const result = await session.fileSystem.readFile("/tmp/test.txt");
const content = result.data;

// 删除文件
const result = await session.fileSystem.deleteFile("/tmp/test.txt");

// 列出目录
const result = await session.fileSystem.listDirectory("/tmp");
const files = result.data;

// 检查文件是否存在
const exists = await session.fileSystem.fileExists("/tmp/test.txt");

// 获取文件信息
const info = await session.fileSystem.getFileInfo("/tmp/test.txt");
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// 写入文件
result, err := session.FileSystem.WriteFile("/tmp/test.txt", "Hello World")

// 读取文件
result, err := session.FileSystem.ReadFile("/tmp/test.txt")
content := result.Data

// 删除文件
result, err := session.FileSystem.DeleteFile("/tmp/test.txt")

// 列出目录
result, err := session.FileSystem.ListDirectory("/tmp")
files := result.Data

// 检查文件是否存在
exists, err := session.FileSystem.FileExists("/tmp/test.txt")

// 获取文件信息
info, err := session.FileSystem.GetFileInfo("/tmp/test.txt")
```
</details>

## 📁 基本文件操作

### 文件写入

#### 创建新文件

<details>
<summary><strong>Python</strong></summary>

```python
# 基本写入
result = session.file_system.write_file("/tmp/hello.txt", "Hello, AgentBay!")
if result.is_error:
    print(f"写入失败: {result.error}")
else:
    print("文件写入成功")

# 写入二进制数据
binary_data = b'\x89PNG\r\n\x1a\n'  # PNG文件头
result = session.file_system.write_file("/tmp/image.png", binary_data, mode="binary")

# 追加内容
result = session.file_system.write_file("/tmp/log.txt", "新日志条目\n", mode="append")

# 确保目录存在
import os
file_path = "/tmp/subdir/file.txt"
dir_path = os.path.dirname(file_path)
session.command.execute(f"mkdir -p {dir_path}")
result = session.file_system.write_file(file_path, "内容")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// 基本写入
const result = await session.fileSystem.writeFile("/tmp/hello.txt", "Hello, AgentBay!");
if (result.isError) {
    console.log(`写入失败: ${result.error}`);
} else {
    console.log("文件写入成功");
}

// 写入二进制数据
const binaryData = new Uint8Array([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]);
const result = await session.fileSystem.writeFile("/tmp/image.png", binaryData, { mode: "binary" });

// 追加内容
const result = await session.fileSystem.writeFile("/tmp/log.txt", "新日志条目\n", { mode: "append" });

// 确保目录存在
const filePath = "/tmp/subdir/file.txt";
const dirPath = filePath.substring(0, filePath.lastIndexOf('/'));
await session.command.execute(`mkdir -p ${dirPath}`);
const result = await session.fileSystem.writeFile(filePath, "内容");
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// 基本写入
result, err := session.FileSystem.WriteFile("/tmp/hello.txt", "Hello, AgentBay!")
if err != nil || result.IsError {
    fmt.Printf("写入失败: %v\n", err)
} else {
    fmt.Println("文件写入成功")
}

// 写入二进制数据
binaryData := []byte{0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A}
result, err := session.FileSystem.WriteFileBytes("/tmp/image.png", binaryData)

// 追加内容
result, err := session.FileSystem.WriteFileAppend("/tmp/log.txt", "新日志条目\n")

// 确保目录存在
filePath := "/tmp/subdir/file.txt"
dirPath := filepath.Dir(filePath)
session.Command.ExecuteCommand(fmt.Sprintf("mkdir -p %s", dirPath))
result, err := session.FileSystem.WriteFile(filePath, "内容")
```
</details>

### 文件读取

#### 读取文本文件

<details>
<summary><strong>Python</strong></summary>

```python
# 基本读取
result = session.file_system.read_file("/tmp/hello.txt")
if result.is_error:
    print(f"读取失败: {result.error}")
else:
    content = result.data
    print(f"文件内容: {content}")

# 读取二进制文件
result = session.file_system.read_file("/tmp/image.png", mode="binary")
if not result.is_error:
    binary_data = result.data
    print(f"文件大小: {len(binary_data)} 字节")

# 按行读取
result = session.file_system.read_file("/tmp/multiline.txt")
if not result.is_error:
    lines = result.data.splitlines()
    for i, line in enumerate(lines, 1):
        print(f"第{i}行: {line}")

# 读取大文件（分块）
def read_large_file(session, file_path, chunk_size=1024):
    """分块读取大文件"""
    chunks = []
    offset = 0
    
    while True:
        result = session.file_system.read_file_chunk(file_path, offset, chunk_size)
        if result.is_error or not result.data:
            break
        chunks.append(result.data)
        offset += len(result.data)
    
    return ''.join(chunks)
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// 基本读取
const result = await session.fileSystem.readFile("/tmp/hello.txt");
if (result.isError) {
    console.log(`读取失败: ${result.error}`);
} else {
    const content = result.data;
    console.log(`文件内容: ${content}`);
}

// 读取二进制文件
const result = await session.fileSystem.readFile("/tmp/image.png", { mode: "binary" });
if (!result.isError) {
    const binaryData = result.data;
    console.log(`文件大小: ${binaryData.length} 字节`);
}

// 按行读取
const result = await session.fileSystem.readFile("/tmp/multiline.txt");
if (!result.isError) {
    const lines = result.data.split('\n');
    lines.forEach((line, index) => {
        console.log(`第${index + 1}行: ${line}`);
    });
}

// 读取大文件（分块）
async function readLargeFile(session: Session, filePath: string, chunkSize: number = 1024): Promise<string> {
    const chunks: string[] = [];
    let offset = 0;
    
    while (true) {
        const result = await session.fileSystem.readFileChunk(filePath, offset, chunkSize);
        if (result.isError || !result.data) {
            break;
        }
        chunks.push(result.data);
        offset += result.data.length;
    }
    
    return chunks.join('');
}
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// 基本读取
result, err := session.FileSystem.ReadFile("/tmp/hello.txt")
if err != nil || result.IsError {
    fmt.Printf("读取失败: %v\n", err)
} else {
    content := result.Data
    fmt.Printf("文件内容: %s\n", content)
}

// 读取二进制文件
result, err := session.FileSystem.ReadFileBytes("/tmp/image.png")
if err == nil && !result.IsError {
    binaryData := result.Data
    fmt.Printf("文件大小: %d 字节\n", len(binaryData))
}

// 按行读取
result, err := session.FileSystem.ReadFile("/tmp/multiline.txt")
if err == nil && !result.IsError {
    lines := strings.Split(result.Data, "\n")
    for i, line := range lines {
        fmt.Printf("第%d行: %s\n", i+1, line)
    }
}

// 读取大文件（分块）
func readLargeFile(session *agentbay.Session, filePath string, chunkSize int) (string, error) {
    var chunks []string
    offset := 0
    
    for {
        result, err := session.FileSystem.ReadFileChunk(filePath, offset, chunkSize)
        if err != nil || result.IsError || result.Data == "" {
            break
        }
        chunks = append(chunks, result.Data)
        offset += len(result.Data)
    }
    
    return strings.Join(chunks, ""), nil
}
```
</details>

### 文件删除

<details>
<summary><strong>Python</strong></summary>

```python
# 删除单个文件
result = session.file_system.delete_file("/tmp/test.txt")
if result.is_error:
    print(f"删除失败: {result.error}")
else:
    print("文件删除成功")

# 安全删除（检查是否存在）
def safe_delete_file(session, file_path):
    if session.file_system.file_exists(file_path):
        result = session.file_system.delete_file(file_path)
        return not result.is_error
    return True  # 文件不存在，视为删除成功

# 批量删除
files_to_delete = ["/tmp/file1.txt", "/tmp/file2.txt", "/tmp/file3.txt"]
for file_path in files_to_delete:
    result = session.file_system.delete_file(file_path)
    if result.is_error:
        print(f"删除 {file_path} 失败: {result.error}")
    else:
        print(f"删除 {file_path} 成功")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// 删除单个文件
const result = await session.fileSystem.deleteFile("/tmp/test.txt");
if (result.isError) {
    console.log(`删除失败: ${result.error}`);
} else {
    console.log("文件删除成功");
}

// 安全删除（检查是否存在）
async function safeDeleteFile(session: Session, filePath: string): Promise<boolean> {
    const exists = await session.fileSystem.fileExists(filePath);
    if (exists) {
        const result = await session.fileSystem.deleteFile(filePath);
        return !result.isError;
    }
    return true; // 文件不存在，视为删除成功
}

// 批量删除
const filesToDelete = ["/tmp/file1.txt", "/tmp/file2.txt", "/tmp/file3.txt"];
for (const filePath of filesToDelete) {
    const result = await session.fileSystem.deleteFile(filePath);
    if (result.isError) {
        console.log(`删除 ${filePath} 失败: ${result.error}`);
    } else {
        console.log(`删除 ${filePath} 成功`);
    }
}
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// 删除单个文件
result, err := session.FileSystem.DeleteFile("/tmp/test.txt")
if err != nil || result.IsError {
    fmt.Printf("删除失败: %v\n", err)
} else {
    fmt.Println("文件删除成功")
}

// 安全删除（检查是否存在）
func safeDeleteFile(session *agentbay.Session, filePath string) bool {
    exists, err := session.FileSystem.FileExists(filePath)
    if err != nil {
        return false
    }
    
    if exists {
        result, err := session.FileSystem.DeleteFile(filePath)
        return err == nil && !result.IsError
    }
    return true // 文件不存在，视为删除成功
}

// 批量删除
filesToDelete := []string{"/tmp/file1.txt", "/tmp/file2.txt", "/tmp/file3.txt"}
for _, filePath := range filesToDelete {
    result, err := session.FileSystem.DeleteFile(filePath)
    if err != nil || result.IsError {
        fmt.Printf("删除 %s 失败: %v\n", filePath, err)
    } else {
        fmt.Printf("删除 %s 成功\n", filePath)
    }
}
```
</details>

## 📂 目录管理

### 创建目录

<details>
<summary><strong>Python</strong></summary>

```python
# 创建单个目录
result = session.file_system.create_directory("/tmp/new_dir")
if result.is_error:
    print(f"创建目录失败: {result.error}")

# 创建多级目录
result = session.file_system.create_directory("/tmp/path/to/deep/dir", recursive=True)

# 使用命令创建目录（推荐）
session.command.execute("mkdir -p /tmp/path/to/deep/dir")

# 创建带权限的目录
session.command.execute("mkdir -m 755 /tmp/secure_dir")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// 创建单个目录
const result = await session.fileSystem.createDirectory("/tmp/new_dir");
if (result.isError) {
    console.log(`创建目录失败: ${result.error}`);
}

// 创建多级目录
const result = await session.fileSystem.createDirectory("/tmp/path/to/deep/dir", { recursive: true });

// 使用命令创建目录（推荐）
await session.command.execute("mkdir -p /tmp/path/to/deep/dir");

// 创建带权限的目录
await session.command.execute("mkdir -m 755 /tmp/secure_dir");
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// 创建单个目录
result, err := session.FileSystem.CreateDirectory("/tmp/new_dir")
if err != nil || result.IsError {
    fmt.Printf("创建目录失败: %v\n", err)
}

// 创建多级目录
result, err := session.FileSystem.CreateDirectoryRecursive("/tmp/path/to/deep/dir")

// 使用命令创建目录（推荐）
session.Command.ExecuteCommand("mkdir -p /tmp/path/to/deep/dir")

// 创建带权限的目录
session.Command.ExecuteCommand("mkdir -m 755 /tmp/secure_dir")
```
</details>

### 列出目录内容

<details>
<summary><strong>Python</strong></summary>

```python
# 基本目录列表
result = session.file_system.list_directory("/tmp")
if not result.is_error:
    for item in result.data:
        file_type = "目录" if item.is_directory else "文件"
        print(f"{item.name} ({file_type}) - 大小: {item.size} 字节")

# 递归列出所有文件
def list_directory_recursive(session, path, max_depth=3, current_depth=0):
    if current_depth >= max_depth:
        return
    
    result = session.file_system.list_directory(path)
    if result.is_error:
        return
    
    for item in result.data:
        indent = "  " * current_depth
        file_type = "📁" if item.is_directory else "📄"
        print(f"{indent}{file_type} {item.name}")
        
        if item.is_directory:
            full_path = f"{path}/{item.name}".replace("//", "/")
            list_directory_recursive(session, full_path, max_depth, current_depth + 1)

# 过滤特定类型文件
result = session.file_system.list_directory("/tmp")
if not result.is_error:
    # 只显示.txt文件
    txt_files = [item for item in result.data if item.name.endswith('.txt')]
    print(f"找到 {len(txt_files)} 个txt文件:")
    for file in txt_files:
        print(f"  {file.name}")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// 基本目录列表
const result = await session.fileSystem.listDirectory("/tmp");
if (!result.isError) {
    result.data.forEach(item => {
        const fileType = item.isDirectory ? "目录" : "文件";
        console.log(`${item.name} (${fileType}) - 大小: ${item.size} 字节`);
    });
}

// 递归列出所有文件
async function listDirectoryRecursive(
    session: Session, 
    path: string, 
    maxDepth: number = 3, 
    currentDepth: number = 0
): Promise<void> {
    if (currentDepth >= maxDepth) {
        return;
    }
    
    const result = await session.fileSystem.listDirectory(path);
    if (result.isError) {
        return;
    }
    
    for (const item of result.data) {
        const indent = "  ".repeat(currentDepth);
        const fileType = item.isDirectory ? "📁" : "📄";
        console.log(`${indent}${fileType} ${item.name}`);
        
        if (item.isDirectory) {
            const fullPath = `${path}/${item.name}`.replace("//", "/");
            await listDirectoryRecursive(session, fullPath, maxDepth, currentDepth + 1);
        }
    }
}

// 过滤特定类型文件
const result = await session.fileSystem.listDirectory("/tmp");
if (!result.isError) {
    // 只显示.txt文件
    const txtFiles = result.data.filter(item => item.name.endsWith('.txt'));
    console.log(`找到 ${txtFiles.length} 个txt文件:`);
    txtFiles.forEach(file => {
        console.log(`  ${file.name}`);
    });
}
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// 基本目录列表
result, err := session.FileSystem.ListDirectory("/tmp")
if err == nil && !result.IsError {
    for _, item := range result.Data {
        fileType := "文件"
        if item.IsDirectory {
            fileType = "目录"
        }
        fmt.Printf("%s (%s) - 大小: %d 字节\n", item.Name, fileType, item.Size)
    }
}

// 递归列出所有文件
func listDirectoryRecursive(session *agentbay.Session, path string, maxDepth, currentDepth int) {
    if currentDepth >= maxDepth {
        return
    }
    
    result, err := session.FileSystem.ListDirectory(path)
    if err != nil || result.IsError {
        return
    }
    
    for _, item := range result.Data {
        indent := strings.Repeat("  ", currentDepth)
        fileType := "📄"
        if item.IsDirectory {
            fileType = "📁"
        }
        fmt.Printf("%s%s %s\n", indent, fileType, item.Name)
        
        if item.IsDirectory {
            fullPath := strings.Replace(fmt.Sprintf("%s/%s", path, item.Name), "//", "/", -1)
            listDirectoryRecursive(session, fullPath, maxDepth, currentDepth+1)
        }
    }
}

// 过滤特定类型文件
result, err := session.FileSystem.ListDirectory("/tmp")
if err == nil && !result.IsError {
    // 只显示.txt文件
    var txtFiles []agentbay.FileInfo
    for _, item := range result.Data {
        if strings.HasSuffix(item.Name, ".txt") {
            txtFiles = append(txtFiles, item)
        }
    }
    fmt.Printf("找到 %d 个txt文件:\n", len(txtFiles))
    for _, file := range txtFiles {
        fmt.Printf("  %s\n", file.Name)
    }
}
```
</details>

### 删除目录

<details>
<summary><strong>Python</strong></summary>

```python
# 删除空目录
result = session.file_system.delete_directory("/tmp/empty_dir")
if result.is_error:
    print(f"删除目录失败: {result.error}")

# 递归删除目录及其内容
result = session.file_system.delete_directory("/tmp/dir_with_content", recursive=True)

# 使用命令删除（更可靠）
session.command.execute("rm -rf /tmp/dir_to_delete")

# 安全删除（先检查是否存在）
def safe_delete_directory(session, dir_path):
    # 检查目录是否存在
    check_result = session.command.execute(f"test -d {dir_path}")
    if check_result.data.exit_code == 0:  # 目录存在
        result = session.command.execute(f"rm -rf {dir_path}")
        return result.data.exit_code == 0
    return True  # 目录不存在，视为删除成功
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// 删除空目录
const result = await session.fileSystem.deleteDirectory("/tmp/empty_dir");
if (result.isError) {
    console.log(`删除目录失败: ${result.error}`);
}

// 递归删除目录及其内容
const result = await session.fileSystem.deleteDirectory("/tmp/dir_with_content", { recursive: true });

// 使用命令删除（更可靠）
await session.command.execute("rm -rf /tmp/dir_to_delete");

// 安全删除（先检查是否存在）
async function safeDeleteDirectory(session: Session, dirPath: string): Promise<boolean> {
    // 检查目录是否存在
    const checkResult = await session.command.execute(`test -d ${dirPath}`);
    if (checkResult.data.exitCode === 0) { // 目录存在
        const result = await session.command.execute(`rm -rf ${dirPath}`);
        return result.data.exitCode === 0;
    }
    return true; // 目录不存在，视为删除成功
}
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// 删除空目录
result, err := session.FileSystem.DeleteDirectory("/tmp/empty_dir")
if err != nil || result.IsError {
    fmt.Printf("删除目录失败: %v\n", err)
}

// 递归删除目录及其内容
result, err := session.FileSystem.DeleteDirectoryRecursive("/tmp/dir_with_content")

// 使用命令删除（更可靠）
session.Command.ExecuteCommand("rm -rf /tmp/dir_to_delete")

// 安全删除（先检查是否存在）
func safeDeleteDirectory(session *agentbay.Session, dirPath string) bool {
    // 检查目录是否存在
    checkResult, err := session.Command.ExecuteCommand(fmt.Sprintf("test -d %s", dirPath))
    if err != nil {
        return false
    }
    
    if checkResult.ExitCode == 0 { // 目录存在
        result, err := session.Command.ExecuteCommand(fmt.Sprintf("rm -rf %s", dirPath))
        return err == nil && result.ExitCode == 0
    }
    return true // 目录不存在，视为删除成功
}
```
</details>

## 🔄 批量操作

### 批量文件处理

<details>
<summary><strong>Python</strong></summary>

```python
import concurrent.futures
from typing import List, Tuple

def batch_file_operations(session, operations: List[dict]):
    """批量执行文件操作"""
    results = []
    
    for operation in operations:
        op_type = operation['type']
        file_path = operation['path']
        
        try:
            if op_type == 'read':
                result = session.file_system.read_file(file_path)
                results.append({
                    'operation': operation,
                    'success': not result.is_error,
                    'data': result.data if not result.is_error else None,
                    'error': result.error if result.is_error else None
                })
            
            elif op_type == 'write':
                content = operation['content']
                result = session.file_system.write_file(file_path, content)
                results.append({
                    'operation': operation,
                    'success': not result.is_error,
                    'error': result.error if result.is_error else None
                })
            
            elif op_type == 'delete':
                result = session.file_system.delete_file(file_path)
                results.append({
                    'operation': operation,
                    'success': not result.is_error,
                    'error': result.error if result.is_error else None
                })
                
        except Exception as e:
            results.append({
                'operation': operation,
                'success': False,
                'error': str(e)
            })
    
    return results

# 使用示例
operations = [
    {'type': 'write', 'path': '/tmp/file1.txt', 'content': 'Content 1'},
    {'type': 'write', 'path': '/tmp/file2.txt', 'content': 'Content 2'},
    {'type': 'read', 'path': '/tmp/file1.txt'},
    {'type': 'delete', 'path': '/tmp/file2.txt'},
]

results = batch_file_operations(session, operations)
for result in results:
    if result['success']:
        print(f"✅ {result['operation']['type']} {result['operation']['path']} 成功")
    else:
        print(f"❌ {result['operation']['type']} {result['operation']['path']} 失败: {result['error']}")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
interface FileOperation {
    type: 'read' | 'write' | 'delete';
    path: string;
    content?: string;
}

interface OperationResult {
    operation: FileOperation;
    success: boolean;
    data?: string;
    error?: string;
}

async function batchFileOperations(session: Session, operations: FileOperation[]): Promise<OperationResult[]> {
    const results: OperationResult[] = [];
    
    for (const operation of operations) {
        try {
            let result: any;
            
            switch (operation.type) {
                case 'read':
                    result = await session.fileSystem.readFile(operation.path);
                    results.push({
                        operation,
                        success: !result.isError,
                        data: result.isError ? undefined : result.data,
                        error: result.isError ? result.error : undefined
                    });
                    break;
                
                case 'write':
                    result = await session.fileSystem.writeFile(operation.path, operation.content!);
                    results.push({
                        operation,
                        success: !result.isError,
                        error: result.isError ? result.error : undefined
                    });
                    break;
                
                case 'delete':
                    result = await session.fileSystem.deleteFile(operation.path);
                    results.push({
                        operation,
                        success: !result.isError,
                        error: result.isError ? result.error : undefined
                    });
                    break;
            }
        } catch (error) {
            results.push({
                operation,
                success: false,
                error: error.toString()
            });
        }
    }
    
    return results;
}

// 使用示例
const operations: FileOperation[] = [
    { type: 'write', path: '/tmp/file1.txt', content: 'Content 1' },
    { type: 'write', path: '/tmp/file2.txt', content: 'Content 2' },
    { type: 'read', path: '/tmp/file1.txt' },
    { type: 'delete', path: '/tmp/file2.txt' },
];

const results = await batchFileOperations(session, operations);
results.forEach(result => {
    if (result.success) {
        console.log(`✅ ${result.operation.type} ${result.operation.path} 成功`);
    } else {
        console.log(`❌ ${result.operation.type} ${result.operation.path} 失败: ${result.error}`);
    }
});
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
type FileOperation struct {
    Type    string // "read", "write", "delete"
    Path    string
    Content string
}

type OperationResult struct {
    Operation FileOperation
    Success   bool
    Data      string
    Error     string
}

func batchFileOperations(session *agentbay.Session, operations []FileOperation) []OperationResult {
    var results []OperationResult
    
    for _, operation := range operations {
        var result OperationResult
        result.Operation = operation
        
        switch operation.Type {
        case "read":
            readResult, err := session.FileSystem.ReadFile(operation.Path)
            if err != nil {
                result.Success = false
                result.Error = err.Error()
            } else if readResult.IsError {
                result.Success = false
                result.Error = readResult.Error
            } else {
                result.Success = true
                result.Data = readResult.Data
            }
            
        case "write":
            writeResult, err := session.FileSystem.WriteFile(operation.Path, operation.Content)
            if err != nil {
                result.Success = false
                result.Error = err.Error()
            } else if writeResult.IsError {
                result.Success = false
                result.Error = writeResult.Error
            } else {
                result.Success = true
            }
            
        case "delete":
            deleteResult, err := session.FileSystem.DeleteFile(operation.Path)
            if err != nil {
                result.Success = false
                result.Error = err.Error()
            } else if deleteResult.IsError {
                result.Success = false
                result.Error = deleteResult.Error
            } else {
                result.Success = true
            }
        }
        
        results = append(results, result)
    }
    
    return results
}

// 使用示例
operations := []FileOperation{
    {Type: "write", Path: "/tmp/file1.txt", Content: "Content 1"},
    {Type: "write", Path: "/tmp/file2.txt", Content: "Content 2"},
    {Type: "read", Path: "/tmp/file1.txt"},
    {Type: "delete", Path: "/tmp/file2.txt"},
}

results := batchFileOperations(session, operations)
for _, result := range results {
    if result.Success {
        fmt.Printf("✅ %s %s 成功\n", result.Operation.Type, result.Operation.Path)
    } else {
        fmt.Printf("❌ %s %s 失败: %s\n", result.Operation.Type, result.Operation.Path, result.Error)
    }
}
```
</details>

## 🔐 文件权限和属性

### 查看文件信息

<details>
<summary><strong>Python</strong></summary>

```python
# 获取文件详细信息
result = session.file_system.get_file_info("/tmp/test.txt")
if not result.is_error:
    info = result.data
    print(f"文件名: {info.name}")
    print(f"大小: {info.size} 字节")
    print(f"类型: {'目录' if info.is_directory else '文件'}")
    print(f"修改时间: {info.modified_time}")
    print(f"权限: {info.permissions}")

# 使用命令获取详细信息
result = session.command.execute("ls -la /tmp/test.txt")
if not result.is_error:
    print("详细信息:")
    print(result.data.stdout)

# 获取文件大小
result = session.command.execute("du -h /tmp/test.txt")
if not result.is_error:
    size_info = result.data.stdout.strip()
    print(f"文件大小: {size_info}")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// 获取文件详细信息
const result = await session.fileSystem.getFileInfo("/tmp/test.txt");
if (!result.isError) {
    const info = result.data;
    console.log(`文件名: ${info.name}`);
    console.log(`大小: ${info.size} 字节`);
    console.log(`类型: ${info.isDirectory ? '目录' : '文件'}`);
    console.log(`修改时间: ${info.modifiedTime}`);
    console.log(`权限: ${info.permissions}`);
}

// 使用命令获取详细信息
const result = await session.command.execute("ls -la /tmp/test.txt");
if (!result.isError) {
    console.log("详细信息:");
    console.log(result.data.stdout);
}

// 获取文件大小
const result = await session.command.execute("du -h /tmp/test.txt");
if (!result.isError) {
    const sizeInfo = result.data.stdout.trim();
    console.log(`文件大小: ${sizeInfo}`);
}
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// 获取文件详细信息
result, err := session.FileSystem.GetFileInfo("/tmp/test.txt")
if err == nil && !result.IsError {
    info := result.Data
    fmt.Printf("文件名: %s\n", info.Name)
    fmt.Printf("大小: %d 字节\n", info.Size)
    fileType := "文件"
    if info.IsDirectory {
        fileType = "目录"
    }
    fmt.Printf("类型: %s\n", fileType)
    fmt.Printf("修改时间: %s\n", info.ModifiedTime)
    fmt.Printf("权限: %s\n", info.Permissions)
}

// 使用命令获取详细信息
result, err := session.Command.ExecuteCommand("ls -la /tmp/test.txt")
if err == nil && !result.IsError {
    fmt.Println("详细信息:")
    fmt.Println(result.Output)
}

// 获取文件大小
result, err := session.Command.ExecuteCommand("du -h /tmp/test.txt")
if err == nil && !result.IsError {
    sizeInfo := strings.TrimSpace(result.Output)
    fmt.Printf("文件大小: %s\n", sizeInfo)
}
```
</details>

### 修改文件权限

<details>
<summary><strong>Python</strong></summary>

```python
# 修改文件权限
def change_file_permissions(session, file_path, permissions):
    """修改文件权限"""
    result = session.command.execute(f"chmod {permissions} {file_path}")
    if result.is_error or result.data.exit_code != 0:
        print(f"修改权限失败: {result.data.stderr}")
        return False
    print(f"成功修改 {file_path} 权限为 {permissions}")
    return True

# 常用权限设置
change_file_permissions(session, "/tmp/script.sh", "755")  # 可执行脚本
change_file_permissions(session, "/tmp/config.txt", "644")  # 只读配置文件
change_file_permissions(session, "/tmp/secret.txt", "600")  # 私有文件

# 批量修改权限
files_and_permissions = [
    ("/tmp/script1.sh", "755"),
    ("/tmp/script2.sh", "755"),
    ("/tmp/config.conf", "644"),
]

for file_path, permissions in files_and_permissions:
    change_file_permissions(session, file_path, permissions)
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// 修改文件权限
async function changeFilePermissions(session: Session, filePath: string, permissions: string): Promise<boolean> {
    const result = await session.command.execute(`chmod ${permissions} ${filePath}`);
    if (result.isError || result.data.exitCode !== 0) {
        console.log(`修改权限失败: ${result.data.stderr}`);
        return false;
    }
    console.log(`成功修改 ${filePath} 权限为 ${permissions}`);
    return true;
}

// 常用权限设置
await changeFilePermissions(session, "/tmp/script.sh", "755");  // 可执行脚本
await changeFilePermissions(session, "/tmp/config.txt", "644");  // 只读配置文件
await changeFilePermissions(session, "/tmp/secret.txt", "600");  // 私有文件

// 批量修改权限
const filesAndPermissions = [
    ["/tmp/script1.sh", "755"],
    ["/tmp/script2.sh", "755"],
    ["/tmp/config.conf", "644"],
];

for (const [filePath, permissions] of filesAndPermissions) {
    await changeFilePermissions(session, filePath, permissions);
}
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// 修改文件权限
func changeFilePermissions(session *agentbay.Session, filePath, permissions string) bool {
    result, err := session.Command.ExecuteCommand(fmt.Sprintf("chmod %s %s", permissions, filePath))
    if err != nil || result.ExitCode != 0 {
        fmt.Printf("修改权限失败: %s\n", result.Stderr)
        return false
    }
    fmt.Printf("成功修改 %s 权限为 %s\n", filePath, permissions)
    return true
}

// 常用权限设置
changeFilePermissions(session, "/tmp/script.sh", "755")  // 可执行脚本
changeFilePermissions(session, "/tmp/config.txt", "644")  // 只读配置文件
changeFilePermissions(session, "/tmp/secret.txt", "600")  // 私有文件

// 批量修改权限
filesAndPermissions := map[string]string{
    "/tmp/script1.sh": "755",
    "/tmp/script2.sh": "755",
    "/tmp/config.conf": "644",
}

for filePath, permissions := range filesAndPermissions {
    changeFilePermissions(session, filePath, permissions)
}
```
</details>

## 📈 大文件处理

### 分块上传

<details>
<summary><strong>Python</strong></summary>

```python
def upload_large_file(session, local_file_path, remote_file_path, chunk_size=1024*1024):
    """分块上传大文件"""
    try:
        with open(local_file_path, 'rb') as f:
            chunk_number = 0
            
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                # 第一个块创建文件，后续块追加
                mode = "write" if chunk_number == 0 else "append"
                
                result = session.file_system.write_file(
                    remote_file_path, 
                    chunk, 
                    mode=mode
                )
                
                if result.is_error:
                    print(f"上传第 {chunk_number + 1} 块失败: {result.error}")
                    return False
                
                chunk_number += 1
                print(f"已上传第 {chunk_number} 块")
        
        print(f"文件 {local_file_path} 上传完成")
        return True
        
    except Exception as e:
        print(f"上传失败: {e}")
        return False

# 使用示例
success = upload_large_file(session, "large_file.zip", "/tmp/large_file.zip")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
import * as fs from 'fs';

async function uploadLargeFile(
    session: Session, 
    localFilePath: string, 
    remoteFilePath: string, 
    chunkSize: number = 1024 * 1024
): Promise<boolean> {
    try {
        const fileHandle = await fs.promises.open(localFilePath, 'r');
        let chunkNumber = 0;
        
        while (true) {
            const buffer = Buffer.alloc(chunkSize);
            const { bytesRead } = await fileHandle.read(buffer, 0, chunkSize, chunkNumber * chunkSize);
            
            if (bytesRead === 0) {
                break;
            }
            
            const chunk = buffer.slice(0, bytesRead);
            
            // 第一个块创建文件，后续块追加
            const mode = chunkNumber === 0 ? "write" : "append";
            
            const result = await session.fileSystem.writeFile(
                remoteFilePath, 
                chunk, 
                { mode }
            );
            
            if (result.isError) {
                console.log(`上传第 ${chunkNumber + 1} 块失败: ${result.error}`);
                await fileHandle.close();
                return false;
            }
            
            chunkNumber++;
            console.log(`已上传第 ${chunkNumber} 块`);
        }
        
        await fileHandle.close();
        console.log(`文件 ${localFilePath} 上传完成`);
        return true;
        
    } catch (error) {
        console.log(`上传失败: ${error}`);
        return false;
    }
}

// 使用示例
const success = await uploadLargeFile(session, "large_file.zip", "/tmp/large_file.zip");
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
import (
    "io"
    "os"
)

func uploadLargeFile(session *agentbay.Session, localFilePath, remoteFilePath string, chunkSize int) bool {
    file, err := os.Open(localFilePath)
    if err != nil {
        fmt.Printf("打开文件失败: %v\n", err)
        return false
    }
    defer file.Close()
    
    buffer := make([]byte, chunkSize)
    chunkNumber := 0
    
    for {
        bytesRead, err := file.Read(buffer)
        if err == io.EOF {
            break
        }
        if err != nil {
            fmt.Printf("读取文件失败: %v\n", err)
            return false
        }
        
        chunk := buffer[:bytesRead]
        
        // 第一个块创建文件，后续块追加
        var result *agentbay.FileResult
        if chunkNumber == 0 {
            result, err = session.FileSystem.WriteFileBytes(remoteFilePath, chunk)
        } else {
            result, err = session.FileSystem.AppendFileBytes(remoteFilePath, chunk)
        }
        
        if err != nil || result.IsError {
            fmt.Printf("上传第 %d 块失败: %v\n", chunkNumber+1, err)
            return false
        }
        
        chunkNumber++
        fmt.Printf("已上传第 %d 块\n", chunkNumber)
    }
    
    fmt.Printf("文件 %s 上传完成\n", localFilePath)
    return true
}

// 使用示例
success := uploadLargeFile(session, "large_file.zip", "/tmp/large_file.zip", 1024*1024)
```
</details>

### 分块下载

<details>
<summary><strong>Python</strong></summary>

```python
def download_large_file(session, remote_file_path, local_file_path, chunk_size=1024*1024):
    """分块下载大文件"""
    try:
        # 先获取文件大小
        info_result = session.file_system.get_file_info(remote_file_path)
        if info_result.is_error:
            print(f"获取文件信息失败: {info_result.error}")
            return False
        
        file_size = info_result.data.size
        total_chunks = (file_size + chunk_size - 1) // chunk_size
        
        with open(local_file_path, 'wb') as f:
            for chunk_number in range(total_chunks):
                offset = chunk_number * chunk_size
                
                # 读取文件块
                result = session.file_system.read_file_chunk(
                    remote_file_path, 
                    offset, 
                    chunk_size
                )
                
                if result.is_error:
                    print(f"下载第 {chunk_number + 1} 块失败: {result.error}")
                    return False
                
                f.write(result.data)
                print(f"已下载第 {chunk_number + 1}/{total_chunks} 块")
        
        print(f"文件 {remote_file_path} 下载完成")
        return True
        
    except Exception as e:
        print(f"下载失败: {e}")
        return False

# 使用示例
success = download_large_file(session, "/tmp/large_file.zip", "downloaded_file.zip")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
import * as fs from 'fs';

async function downloadLargeFile(
    session: Session, 
    remoteFilePath: string, 
    localFilePath: string, 
    chunkSize: number = 1024 * 1024
): Promise<boolean> {
    try {
        // 先获取文件大小
        const infoResult = await session.fileSystem.getFileInfo(remoteFilePath);
        if (infoResult.isError) {
            console.log(`获取文件信息失败: ${infoResult.error}`);
            return false;
        }
        
        const fileSize = infoResult.data.size;
        const totalChunks = Math.ceil(fileSize / chunkSize);
        
        const writeStream = fs.createWriteStream(localFilePath);
        
        for (let chunkNumber = 0; chunkNumber < totalChunks; chunkNumber++) {
            const offset = chunkNumber * chunkSize;
            
            // 读取文件块
            const result = await session.fileSystem.readFileChunk(
                remoteFilePath, 
                offset, 
                chunkSize
            );
            
            if (result.isError) {
                console.log(`下载第 ${chunkNumber + 1} 块失败: ${result.error}`);
                writeStream.close();
                return false;
            }
            
            writeStream.write(result.data);
            console.log(`已下载第 ${chunkNumber + 1}/${totalChunks} 块`);
        }
        
        writeStream.close();
        console.log(`文件 ${remoteFilePath} 下载完成`);
        return true;
        
    } catch (error) {
        console.log(`下载失败: ${error}`);
        return false;
    }
}

// 使用示例
const success = await downloadLargeFile(session, "/tmp/large_file.zip", "downloaded_file.zip");
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
import (
    "os"
)

func downloadLargeFile(session *agentbay.Session, remoteFilePath, localFilePath string, chunkSize int) bool {
    // 先获取文件大小
    infoResult, err := session.FileSystem.GetFileInfo(remoteFilePath)
    if err != nil || infoResult.IsError {
        fmt.Printf("获取文件信息失败: %v\n", err)
        return false
    }
    
    fileSize := infoResult.Data.Size
    totalChunks := (fileSize + int64(chunkSize) - 1) / int64(chunkSize)
    
    file, err := os.Create(localFilePath)
    if err != nil {
        fmt.Printf("创建本地文件失败: %v\n", err)
        return false
    }
    defer file.Close()
    
    for chunkNumber := int64(0); chunkNumber < totalChunks; chunkNumber++ {
        offset := chunkNumber * int64(chunkSize)
        
        // 读取文件块
        result, err := session.FileSystem.ReadFileChunk(remoteFilePath, offset, chunkSize)
        if err != nil || result.IsError {
            fmt.Printf("下载第 %d 块失败: %v\n", chunkNumber+1, err)
            return false
        }
        
        _, err = file.Write(result.Data)
        if err != nil {
            fmt.Printf("写入本地文件失败: %v\n", err)
            return false
        }
        
        fmt.Printf("已下载第 %d/%d 块\n", chunkNumber+1, totalChunks)
    }
    
    fmt.Printf("文件 %s 下载完成\n", remoteFilePath)
    return true
}

// 使用示例
success := downloadLargeFile(session, "/tmp/large_file.zip", "downloaded_file.zip", 1024*1024)
```
</details>

## ⚡ 性能优化

### 缓存策略

<details>
<summary><strong>Python</strong></summary>

```python
import time
from functools import lru_cache

class FileCache:
    def __init__(self, max_size=100, ttl=300):  # 5分钟TTL
        self.cache = {}
        self.timestamps = {}
        self.max_size = max_size
        self.ttl = ttl
    
    def get(self, key):
        if key in self.cache:
            # 检查是否过期
            if time.time() - self.timestamps[key] < self.ttl:
                return self.cache[key]
            else:
                # 过期，删除
                del self.cache[key]
                del self.timestamps[key]
        return None
    
    def set(self, key, value):
        # 如果缓存满了，删除最旧的条目
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.timestamps.keys(), key=lambda k: self.timestamps[k])
            del self.cache[oldest_key]
            del self.timestamps[oldest_key]
        
        self.cache[key] = value
        self.timestamps[key] = time.time()

# 全局文件缓存
file_cache = FileCache()

def cached_read_file(session, file_path):
    """带缓存的文件读取"""
    cached_content = file_cache.get(file_path)
    if cached_content is not None:
        print(f"从缓存读取: {file_path}")
        return cached_content
    
    # 缓存未命中，从远程读取
    result = session.file_system.read_file(file_path)
    if not result.is_error:
        file_cache.set(file_path, result.data)
        print(f"从远程读取并缓存: {file_path}")
        return result.data
    
    return None

# 使用示例
content1 = cached_read_file(session, "/tmp/config.txt")  # 从远程读取
content2 = cached_read_file(session, "/tmp/config.txt")  # 从缓存读取
```
</details>

### 并发操作

<details>
<summary><strong>Python</strong></summary>

```python
import asyncio
import concurrent.futures
from typing import List

async def concurrent_file_operations(session, file_paths: List[str], operation='read'):
    """并发执行文件操作"""
    
    async def process_file(file_path):
        try:
            if operation == 'read':
                result = session.file_system.read_file(file_path)
                return {
                    'path': file_path,
                    'success': not result.is_error,
                    'data': result.data if not result.is_error else None,
                    'error': result.error if result.is_error else None
                }
            elif operation == 'delete':
                result = session.file_system.delete_file(file_path)
                return {
                    'path': file_path,
                    'success': not result.is_error,
                    'error': result.error if result.is_error else None
                }
        except Exception as e:
            return {
                'path': file_path,
                'success': False,
                'error': str(e)
            }
    
    # 并发执行
    tasks = [process_file(path) for path in file_paths]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return results

# 使用示例（需要在异步环境中运行）
file_paths = ["/tmp/file1.txt", "/tmp/file2.txt", "/tmp/file3.txt"]
# results = await concurrent_file_operations(session, file_paths, 'read')
```
</details>

## 🚨 错误处理

### 常见错误类型

<details>
<summary><strong>Python</strong></summary>

```python
def robust_file_operation(session, operation, file_path, content=None, max_retries=3):
    """健壮的文件操作，包含重试机制"""
    
    for attempt in range(max_retries):
        try:
            if operation == 'read':
                result = session.file_system.read_file(file_path)
            elif operation == 'write':
                result = session.file_system.write_file(file_path, content)
            elif operation == 'delete':
                result = session.file_system.delete_file(file_path)
            else:
                raise ValueError(f"不支持的操作: {operation}")
            
            if not result.is_error:
                return result
            
            # 分析错误类型
            error_msg = result.error.lower()
            
            if 'permission denied' in error_msg:
                print(f"权限错误: {result.error}")
                # 尝试修改权限
                if operation in ['write', 'delete']:
                    session.command.execute(f"chmod 666 {file_path}")
                    continue
                else:
                    break  # 读取权限错误通常无法自动修复
            
            elif 'no such file or directory' in error_msg:
                if operation == 'write':
                    # 创建目录
                    import os
                    dir_path = os.path.dirname(file_path)
                    session.command.execute(f"mkdir -p {dir_path}")
                    continue
                else:
                    print(f"文件不存在: {file_path}")
                    break
            
            elif 'disk full' in error_msg or 'no space left' in error_msg:
                print("磁盘空间不足")
                break  # 磁盘满了，重试无意义
            
            else:
                print(f"尝试 {attempt + 1} 失败: {result.error}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
        
        except Exception as e:
            print(f"操作异常: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    
    print(f"操作 {operation} {file_path} 在 {max_retries} 次尝试后失败")
    return None

# 使用示例
result = robust_file_operation(session, 'write', '/tmp/test.txt', 'Hello World')
if result:
    print("操作成功")
else:
    print("操作失败")
```
</details>

## 💡 最佳实践

### 1. 路径管理
- 优先使用绝对路径
- 在操作前验证路径格式
- 使用适合操作系统的路径分隔符

### 2. 错误处理
- 始终检查操作结果
- 实现重试机制
- 记录详细的错误信息

### 3. 性能优化
- 对频繁读取的文件使用缓存
- 批量操作优于单次操作
- 大文件使用分块处理

### 4. 安全考虑
- 验证文件路径，防止路径遍历攻击
- 设置适当的文件权限
- 及时清理临时文件

### 5. 资源管理
- 合理使用临时目录
- 定期清理不需要的文件
- 监控磁盘使用情况

## 📚 相关资源

- [会话管理](session-management.md) - 了解会话生命周期
- [数据持久化](data-persistence.md) - 实现数据持久化
- [API速查表](../api-reference.md) - 快速查找API
- [故障排除](../quickstart/troubleshooting.md) - 解决常见问题

---

💡 **提示**: 文件操作是AgentBay的核心功能之一。掌握这些技巧将大大提高你的开发效率！ 