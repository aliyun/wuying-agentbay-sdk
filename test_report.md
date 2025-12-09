# 批量文档验证报告

**总结**: 10 文件 | ✅ 7 成功 | ❌ 3 失败

## 🚨 验证失败的文件

### 📄 python/docs/examples/_async/common-features/basics/list_sessions/README.md

**错误输出**:
```

  File "/Users/liyuebing/Projects/wuying-agentbay-sdk/tmp/doc_verification_batch/batch_2135/batch_verify.py", line 1
    SKIP_ALL: 提供的代码片段仅为函数定义，没有具体的实现或调用示例。
                           ^
SyntaxError: invalid character '，' (U+FF0C)

```

### 📄 python/docs/examples/_async/computer-use/computer/README.md

**错误输出**:
```
ameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 725, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/liyuebing/Projects/wuying-agentbay-sdk/tmp/doc_verification_batch/batch_8183/batch_verify.py", line 71, in main
    raise RuntimeError(f"Failed to create session: {session_result.error_message}")
RuntimeError: Failed to create session: Failed to create session: Error: Image.NotExist code: 400, code: 400, The image does not exist. request id: 64864826-01D1-50C8-BAEB-C7BFF0A983D6 request id: CD536CD8-593D-5784-A1AA-F0EDD3D8EA15 Response: {'RequestId': 'CD536CD8-593D-5784-A1AA-F0EDD3D8EA15', 'HostId': 'wuyingai.cn-shanghai.aliyuncs.com', 'Code': 'Image.NotExist', 'Message': 'code: 400, The image does not exist. request id: 64864826-01D1-50C8-BAEB-C7BFF0A983D6', 'Recommend': 'https://api.aliyun.com/troubleshoot?q=Image.NotExist&product=WuyingAI&requestId=CD536CD8-593D-5784-A1AA-F0EDD3D8EA15', 'statusCode': 400}

```

### 📄 python/docs/examples/_sync/common-features/basics/list_sessions/README.md

**错误输出**:
```

  File "/Users/liyuebing/Projects/wuying-agentbay-sdk/tmp/doc_verification_batch/batch_6465/batch_verify.py", line 1
    SKIP_ALL: 提供的代码片段仅为方法签名，没有具体的逻辑或函数调用。
                           ^
SyntaxError: invalid character '，' (U+FF0C)

```

## 📊 详细结果

- `python/docs/guides/async-programming/migration-guide.md`: ✅ 成功
- `python/docs/guides/async-programming/sync-vs-async.md`: ✅ 成功
- `python/docs/examples/README.md`: ✅ 成功
- `python/docs/examples/_async/common-features/basics/data_persistence/context_sync_demo.md`: ✅ 成功
- `python/docs/examples/_async/common-features/basics/list_sessions/README.md`: ❌ 失败
- `python/docs/examples/_async/common-features/basics/get/README.md`: ✅ 成功
- `python/docs/examples/_async/common-features/basics/archive-upload-mode-example/README.md`: ✅ 成功
- `python/docs/examples/_async/computer-use/computer/README.md`: ❌ 失败
- `python/docs/examples/_sync/common-features/basics/data_persistence/context_sync_demo.md`: ✅ 成功
- `python/docs/examples/_sync/common-features/basics/list_sessions/README.md`: ❌ 失败
