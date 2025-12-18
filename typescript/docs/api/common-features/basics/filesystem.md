# Class: FileSystem

## 📁 Related Tutorial

- [File Operations Guide](../../../../../docs/guides/common-features/basics/file-operations.md) - Complete guide to file system operations

Handles file operations in the AgentBay cloud environment.

## Table of contents


### Methods

- [createDirectory](#createdirectory)
- [deleteFile](#deletefile)
- [downloadFile](#downloadfile)
- [editFile](#editfile)
- [listDirectory](#listdirectory)
- [moveFile](#movefile)
- [readFile](#readfile)
- [readMultipleFiles](#readmultiplefiles)
- [searchFiles](#searchfiles)
- [uploadFile](#uploadfile)
- [watchDirectory](#watchdirectory)
- [writeFile](#writefile)

## Methods

### createDirectory

▸ **createDirectory**(`path`): `Promise`\<`BoolResult`\>

Creates a new directory at the specified path.
Corresponds to Python's create_directory() method

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | Path to the directory to create. |

#### Returns

`Promise`\<`BoolResult`\>

BoolResult with creation result and requestId

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create();
if (result.success) {
  const createResult = await result.session.fileSystem.createDirectory('/tmp/mydir');
  console.log('Directory created:', createResult.success);
  await result.session.delete();
}
```

___

### deleteFile

▸ **deleteFile**(`path`): `Promise`\<`BoolResult`\>

Deletes a file at the specified path.
Corresponds to Python's delete_file() method

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | Path to the file to delete. |

#### Returns

`Promise`\<`BoolResult`\>

BoolResult with deletion result and requestId

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create();
if (result.success) {
  const session = result.session;
  await session.fileSystem.writeFile('/tmp/to_delete.txt', 'hello');
  const deleteResult = await session.fileSystem.deleteFile('/tmp/to_delete.txt');
  console.log('File deleted:', deleteResult.success);
  await session.delete();
}
```

___

### downloadFile

▸ **downloadFile**(`remotePath`, `localPath`, `options?`): `Promise`\<`any`\>

Download a file from remote path to local path using pre-signed URLs.
This is a synchronous wrapper around the FileTransfer.download method.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `remotePath` | `string` | Remote file path to download from |
| `localPath` | `string` | Local file path to download to |
| `options?` | `Object` | Optional parameters |
| `options.overwrite?` | `boolean` | - |
| `options.pollInterval?` | `number` | - |
| `options.progressCb?` | (`bytesReceived`: `number`) => `void` | - |
| `options.wait?` | `boolean` | - |
| `options.waitTimeout?` | `number` | - |

#### Returns

`Promise`\<`any`\>

DownloadResult with download result and requestId

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create({ imageId: 'code_latest' });
if (result.success) {
  await result.session.fileSystem.writeFile('/workspace/remote.txt', 'Content to download');
  const downloadResult = await result.session.fileSystem.downloadFile('/workspace/remote.txt', '/tmp/local.txt');
  console.log('Download success:', downloadResult.success);
  await result.session.delete();
}
```

___

### editFile

▸ **editFile**(`path`, `edits`, `dryRun?`): `Promise`\<`BoolResult`\>

Edits a file by replacing occurrences of oldText with newText.
Corresponds to Python's edit_file() method

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `path` | `string` | `undefined` | Path to the file to edit. |
| `edits` | \{ `newText`: `string` ; `oldText`: `string`  }[] | `undefined` | Array of edit operations, each containing oldText and newText. |
| `dryRun` | `boolean` | `false` | Optional: If true, preview changes without applying them. |

#### Returns

`Promise`\<`BoolResult`\>

BoolResult with edit result and requestId

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create();
if (result.success) {
  await result.session.fileSystem.writeFile('/tmp/config.txt', 'DEBUG=false');
  const edits = [{ oldText: 'DEBUG=false', newText: 'DEBUG=true' }];
  const editResult = await result.session.fileSystem.editFile('/tmp/config.txt', edits);
  console.log('File edited:', editResult.success);
  await result.session.delete();
}
```

### listDirectory

▸ **listDirectory**(`path`): `Promise`\<`DirectoryListResult`\>

Lists the contents of a directory.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | Absolute path to the directory to list. |

#### Returns

`Promise`\<`DirectoryListResult`\>

Promise resolving to DirectoryListResult containing array of entries.

**`Example`**

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create();

if (result.success) {
  const session = result.session;

  // List directory contents
  const listResult = await session.fileSystem.listDirectory('/tmp');
  if (listResult.success) {
    console.log(`Found ${listResult.entries.length} entries`);
    for (const entry of listResult.entries) {
      console.log(`${entry.name} (${entry.isDirectory ? 'dir' : 'file'})`);
    }
  }

  await session.delete();
}
```

**`See`**

[readFile](#readfile), [writeFile](#writefile)

___

### moveFile

▸ **moveFile**(`source`, `destination`): `Promise`\<`BoolResult`\>

Moves a file or directory from source to destination.
Corresponds to Python's move_file() method

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `source` | `string` | Path to the source file or directory. |
| `destination` | `string` | Path to the destination file or directory. |

#### Returns

`Promise`\<`BoolResult`\>

BoolResult with move result and requestId

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create();
if (result.success) {
  await result.session.fileSystem.writeFile('/tmp/original.txt', 'Test content');
  const moveResult = await result.session.fileSystem.moveFile('/tmp/original.txt', '/tmp/moved.txt');
  console.log('File moved:', moveResult.success);
  await result.session.delete();
}
```

___

### readFile

▸ **readFile**(`path`): `Promise`\<`FileContentResult`\>

Reads the entire content of a file.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | Absolute path to the file to read. |

#### Returns

`Promise`\<`FileContentResult`\>

Promise resolving to FileContentResult containing:
         - success: Whether the read operation succeeded
         - content: String content of the file
         - requestId: Unique identifier for this API request
         - errorMessage: Error description if read failed

**`Throws`**

Error if the API call fails.

**`Example`**

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create();

if (result.success) {
  const session = result.session;

  // Read a text file
  const fileResult = await session.fileSystem.readFile('/etc/hostname');
  if (fileResult.success) {
    console.log(`Content: ${fileResult.content}`);
    // Output: Content: agentbay-session-xyz
  }

  await session.delete();
}
```

**`Remarks`**

**Behavior:**
- Automatically handles large files by reading in 60KB chunks
- Returns empty string for empty files
- Fails if path is a directory or doesn't exist
- Content is returned as UTF-8 string

**`See`**

[writeFile](#writefile), [listDirectory](#listdirectory)

___

### readMultipleFiles

▸ **readMultipleFiles**(`paths`): `Promise`\<`MultipleFileContentResult`\>

Reads the content of multiple files.
Corresponds to Python's read_multiple_files() method

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `paths` | `string`[] | Array of file paths to read. |

#### Returns

`Promise`\<`MultipleFileContentResult`\>

MultipleFileContentResult with file contents and requestId

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create();
if (result.success) {
  await result.session.fileSystem.writeFile('/tmp/file1.txt', 'Content 1');
  await result.session.fileSystem.writeFile('/tmp/file2.txt', 'Content 2');
  const readResult = await result.session.fileSystem.readMultipleFiles(['/tmp/file1.txt', '/tmp/file2.txt']);
  console.log(`Read ${Object.keys(readResult.contents).length} files`);
  await result.session.delete();
}
```

___

### searchFiles

▸ **searchFiles**(`path`, `pattern`, `excludePatterns?`): `Promise`\<`FileSearchResult`\>

Searches for files in a directory that match a wildcard pattern.
Corresponds to Python's search_files() method

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `path` | `string` | `undefined` | Path to the directory to search in. |
| `pattern` | `string` | `undefined` | Wildcard pattern to match against file names. Supports * (any characters) and ? (single character). Examples: "*.py", "test_*", "*config*". |
| `excludePatterns` | `string`[] | `[]` | Optional: Array of wildcard patterns to exclude. |

#### Returns

`Promise`\<`FileSearchResult`\>

FileSearchResult with search results and requestId

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create();
if (result.success) {
  await result.session.fileSystem.createDirectory('/tmp/test');
  await result.session.fileSystem.writeFile('/tmp/test/file1.py', "print('hello')");
  const searchResult = await result.session.fileSystem.searchFiles('/tmp/test', '*.py');
  console.log(`Found ${searchResult.matches.length} Python files`);
  await result.session.delete();
}
```

___

### uploadFile

▸ **uploadFile**(`localPath`, `remotePath`, `options?`): `Promise`\<`any`\>

Upload a file from local to remote path using pre-signed URLs.
This is a synchronous wrapper around the FileTransfer.upload method.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `localPath` | `string` | Local file path to upload |
| `remotePath` | `string` | Remote file path to upload to |
| `options?` | `Object` | Optional parameters |
| `options.contentType?` | `string` | - |
| `options.pollInterval?` | `number` | - |
| `options.progressCb?` | (`bytesTransferred`: `number`) => `void` | - |
| `options.wait?` | `boolean` | - |
| `options.waitTimeout?` | `number` | - |

#### Returns

`Promise`\<`any`\>

UploadResult with upload result and requestId

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create({ imageId: 'code_latest' });
if (result.success) {
  const uploadResult = await result.session.fileSystem.uploadFile('/tmp/local.txt', '/workspace/remote.txt');
  console.log('Upload success:', uploadResult.success);
  await result.session.delete();
}
```

___

### watchDirectory

▸ **watchDirectory**(`path`, `callback`, `interval?`, `signal?`): `Promise`\<`void`\>

Watch a directory for file changes and call the callback function when changes occur

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `path` | `string` | `undefined` | Directory path to monitor |
| `callback` | (`events`: ``FileChangeEvent``[]) => `void` | `undefined` | Function called when changes are detected |
| `interval` | `number` | `500` | Polling interval in milliseconds (default: 500, minimum: 100) |
| `signal?` | `AbortSignal` | `undefined` | Signal to abort the monitoring |

#### Returns

`Promise`\<`void`\>

Promise that resolves when monitoring stops

**`Example`**

```typescript
const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create();
if (result.success) {
  const testDir = '/tmp/watch_test';
  await result.session.fileSystem.createDirectory(testDir);
  const controller = new AbortController();
  const callback = (events) => console.log(`Detected ${events.length} changes`);
  await result.session.fileSystem.watchDirectory(testDir, callback, 1000, controller.signal);
  await result.session.delete();
}
```

___

### writeFile

▸ **writeFile**(`path`, `content`, `mode?`): `Promise`\<`BoolResult`\>

Writes content to a file.

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `path` | `string` | `undefined` | Absolute path to the file to write. |
| `content` | `string` | `undefined` | String content to write to the file. |
| `mode` | `string` | `"overwrite"` | Write mode: "overwrite" (default) or "append". |

#### Returns

`Promise`\<`BoolResult`\>

Promise resolving to BoolResult with success status.

**`Example`**

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

const agentBay = new AgentBay({ apiKey: 'your_api_key' });
const result = await agentBay.create();

if (result.success) {
  const session = result.session;

  // Write to a file (overwrite mode)
  const writeResult = await session.fileSystem.writeFile(
    '/tmp/test.txt',
    'Hello, AgentBay!'
  );
  if (writeResult.success) {
    console.log('File written successfully');
  }

  // Append to a file
  const appendResult = await session.fileSystem.writeFile(
    '/tmp/test.txt',
    '\nNew line',
    'append'
  );

  await session.delete();
}
```

**`Remarks`**

**Behavior:**
- Automatically handles large files by writing in 60KB chunks
- Creates parent directories if they don't exist
- "overwrite" mode replaces existing file content
- "append" mode adds content to the end of the file

**`See`**

[readFile](#readfile), [listDirectory](#listdirectory)

## Related Resources

- [Session API Reference](session.md)
- [Command API Reference](command.md)

