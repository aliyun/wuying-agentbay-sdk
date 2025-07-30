import { describe, beforeEach, afterEach, test, expect } from '@jest/globals';
import { AgentBay } from '../../src/agent-bay';
import { Session } from '../../src/session';
import { FileSystem } from '../../src/filesystem';
import { log } from 'console';

describe('FileSystem Comprehensive Tests', () => {
  let agentBay: AgentBay;
  let session: Session;
  let fileSystem: FileSystem;

  beforeEach(async () => {
    agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY || 'test-api-key' });
    const sessionResult = await agentBay.create();
    expect(sessionResult.success).toBe(true);

    session = sessionResult.session!;
    fileSystem = session.fileSystem;
    await fileSystem.createDirectory('/tmp');
  });

  afterEach(async () => {
    if (session) {
      await agentBay.delete(session);
    }
  });

  // 1. 文件基础操作测试
  describe('1. File Basic Operations', () => {
    const testFilePath = '/tmp/test_files.txt';
    const multiLineFilePath = '/tmp/test_multiline.txt';

    beforeEach(async () => {
      // 创建30KB测试文件，内容为重复的"hello world!!!"
      const testContent = 'hello world!!!\n'.repeat(2000);
      await fileSystem.writeFile(testFilePath, testContent, 'overwrite');
    });

    describe('1.1 File Reading Tests', () => {
      test('should successfully read file content', async () => {
        const result = await fileSystem.readFile(testFilePath);

        expect(result.success).toBe(true);
        expect(result.requestId).toBeDefined();
        expect(result.requestId).not.toBe('');
        expect(result.content).toBeDefined();
        expect(result.content).toContain('hello world!!!');
        expect(result.errorMessage).toBeUndefined();
        expect(result.content.length).toEqual(30000);
      });

      test('should return correct file content pattern', async () => {
        const result = await fileSystem.readFile(testFilePath);

        expect(result.success).toBe(true);
        const lines = result.content.split('\n').filter(line => line.trim() !== '');
        lines.forEach(line => {
          if (line.trim() !== '') {
            expect(line).toBe('hello world!!!');
          }
        });
      });
    });

    describe('1.2 Parameterized File Reading Tests', () => {
      beforeEach(async () => {
        // 创建多行测试文件
        const multiLineContent = Array.from({ length: 10 }, (_, i) => `Line ${i + 1}: This is test content`).join('\n');
        await fileSystem.writeFile(multiLineFilePath, multiLineContent, 'overwrite');
      });

      test('should read specific bytes with offset and length parameters', async () => {
        // 从第3个字节开始读取3个字节 (offset=2, length=3)
        const result = await fileSystem.readFile(multiLineFilePath, 2, 3);

        expect(result.success).toBe(true);
        expect(result.requestId).toBeDefined();
        expect(result.content).toBeDefined();
        expect(result.content.length).toBeLessThanOrEqual(3); // 应该最多读取3个字节

        // 验证读取的内容是从第3个字节开始的
        const fullContent = await fileSystem.readFile(multiLineFilePath);
        const expectedContent = fullContent.content.substring(2, 5); // 字节2-4 (3个字节)
        expect(result.content).toBe(expectedContent);
      });

      test('should read from offset to end of file', async () => {
        // 从第6个字节开始读取到文件末尾 (offset=5, length=0)
        const result = await fileSystem.readFile(multiLineFilePath, 5, 0);

        expect(result.success).toBe(true);
        expect(result.requestId).toBeDefined();
        expect(result.content).toBeDefined();

        // 验证从第6个字节开始读取到文件末尾
        const fullContent = await fileSystem.readFile(multiLineFilePath);
        const expectedContent = fullContent.content.substring(5); // 从第6个字节到末尾
        expect(result.content).toBe(expectedContent);
      });

      test('should handle large offset values correctly', async () => {
        // 测试大于文件大小的offset值
        const result = await fileSystem.readFile(multiLineFilePath, 1000);

        expect(result.success).toBe(true);
        expect(result.content).toBeDefined();
        // 应该返回空内容，因为offset超过了文件大小
      });

      test('should handle zero length parameter correctly', async () => {
        // 测试length=0应该读取从offset到文件末尾
        const result = await fileSystem.readFile(multiLineFilePath, 0, 0);

        expect(result.success).toBe(true);
        expect(result.content).toBeDefined();

        // length=0应该读取整个文件
        const fullContent = await fileSystem.readFile(multiLineFilePath);
        expect(result.content).toBe(fullContent.content);
      });
    });

    describe('1.3 File Writing Tests', () => {
      const writeTestFilePath = '/tmp/test_write.txt';

      test('should write file with different modes', async () => {
        const testContent = 'Hello, World!';

        // 测试overwrite模式
        const writeResult = await fileSystem.writeFile(writeTestFilePath, testContent, 'overwrite');
        expect(writeResult.success).toBe(true);
        expect(writeResult.requestId).toBeDefined();
        expect(writeResult.data).toBe(true);

        // 验证内容
        const readResult = await fileSystem.readFile(writeTestFilePath);
        expect(readResult.success).toBe(true);
        expect(readResult.content).toBe(testContent);

        // 测试append模式
        const appendResult = await fileSystem.writeFile(writeTestFilePath, '\nAppended content', 'append');
        expect(appendResult.success).toBe(true);

        const readResult2 = await fileSystem.readFile(writeTestFilePath);
        expect(readResult2.content).toContain(testContent);
        expect(readResult2.content).toContain('Appended content');
      });

      test('should validate write mode parameter', async () => {
        const result = await fileSystem.writeFile(writeTestFilePath, 'content', 'invalid_mode' as any);
        log(`Write result: ${JSON.stringify(result)}`);
        expect(result.success).toBe(false);
        expect(result.errorMessage).toContain('Invalid mode');
      });
    });

    describe('1.4 Large File Tests', () => {
      test('should handle large file operations', async () => {
        const largeContent = 'Large content line. '.repeat(3000);
        const largeFilePath = '/tmp/large_test.txt';

        // 写入大文件
        const writeResult = await fileSystem.writeLargeFile(largeFilePath, largeContent);
        expect(writeResult.success).toBe(true);

        // 读取大文件
        const readResult = await fileSystem.readLargeFile(largeFilePath);
        expect(readResult.success).toBe(true);
        expect(readResult.content).toBe(largeContent);
      });
    });
  });

  // 2. 文件信息管理测试
  describe('2. File Information Management', () => {
    test('should get file info correctly', async () => {
      await fileSystem.writeFile('/tmp/info_test.txt', '', 'overwrite');

      const result = await fileSystem.getFileInfo('/tmp/info_test.txt');
      expect(result.success).toBe(true);
      expect(result.fileInfo!.name).toBeDefined();
      expect(result.fileInfo!.size).toBe(0);
      expect(result.fileInfo!.isDirectory).toBe(false);
    });

    test('should list directory contents', async () => {
      await fileSystem.createDirectory('/tmp/list_test');
      await fileSystem.writeFile('/tmp/list_test/file1.txt', 'content1', 'overwrite');
      await fileSystem.createDirectory('/tmp/list_test/subdir1');

      const result = await fileSystem.listDirectory('/tmp/list_test');
      expect(result.success).toBe(true);
      expect(result.entries.length).toBeGreaterThan(0);
    });
  });

  // 3. 批量文件操作测试
  describe('3. Batch File Operations', () => {
    test('should read multiple files correctly', async () => {
      const files = ['/tmp/batch1.txt', '/tmp/batch2.txt', '/tmp/batch3.txt'];
      await fileSystem.writeFile(files[0], 'Content 1', 'overwrite');
      await fileSystem.writeFile(files[1], '', 'overwrite');
      await fileSystem.writeFile(files[2], 'Content 3', 'overwrite');

      const result = await fileSystem.readMultipleFiles(files);
      expect(result.success).toBe(true);
      expect(result.contents[files[0]]).toBe('Content 1');
      expect(result.contents[files[1]]).toBe('');
      expect(result.contents[files[2]]).toBe('Content 3');
    });

    test('should search files correctly', async () => {
      await fileSystem.createDirectory('/tmp/search_test');
      await fileSystem.writeFile('/tmp/search_test/test1.txt', 'content', 'overwrite');
      await fileSystem.writeFile('/tmp/search_test/test2.log', 'log', 'overwrite');

      const result1 = await fileSystem.searchFiles('/tmp/search_test', 'test1.txt');
      expect(result1.success).toBe(true);
      expect(result1.matches).toBeDefined();
      const result2 = await fileSystem.searchFiles('/tmp/search_test', "", ['test2.log']);
      expect(result2.success).toBe(true);
      expect(result2.matches).toBeDefined();
    });
  });

  // 4. 文件编辑和移动测试
  describe('4. File Edit and Move Operations', () => {
    test('should edit file with find-replace', async () => {
      const editPath = '/tmp/edit_test.txt';
      await fileSystem.writeFile(editPath, 'This is old1 text with old2 content.', 'overwrite');

      const edits = [
        { oldText: 'old1', newText: 'new1' },
        { oldText: 'old2', newText: 'new2' }
      ];

      const result = await fileSystem.editFile(editPath, edits, false);
      expect(result.success).toBe(true);

      const readResult = await fileSystem.readFile(editPath);
      expect(readResult.content).toContain('new1');
      expect(readResult.content).toContain('new2');
    });

    test('should move file correctly', async () => {
      const sourcePath = '/tmp/move_source.txt';
      const destPath = '/tmp/move_dest.txt';

      await fileSystem.writeFile(sourcePath, 'Content to move', 'overwrite');

      const result = await fileSystem.moveFile(sourcePath, destPath);
      expect(result.success).toBe(true);

      const readResult = await fileSystem.readFile(destPath);
      expect(readResult.success).toBe(true);
      expect(readResult.content).toBe('Content to move');
    });
  });

  // 5. 目录管理测试
  describe('5. Directory Management', () => {
    test('should create directory successfully', async () => {
      const dirPath = '/tmp/new_directory';

      const result = await fileSystem.createDirectory(dirPath);
      expect(result.success).toBe(true);

      const infoResult = await fileSystem.getFileInfo(dirPath);
      expect(infoResult.success).toBe(true);
      expect(infoResult.fileInfo!.isDirectory).toBe(true);
    });

    test('should create nested directories', async () => {
      const nestedPath = '/tmp/level1/level2/level3';

      await fileSystem.createDirectory('/tmp/level1');
      await fileSystem.createDirectory('/tmp/level1/level2');
      const result = await fileSystem.createDirectory(nestedPath);

      expect(result.success).toBe(true);
    });
  });

  // 6. 异常处理测试
  describe('6. Error Handling', () => {
    test('should handle non-existent file operations', async () => {
      const nonExistentPath = '/tmp/non_existent.txt';

      const readResult = await fileSystem.readFile(nonExistentPath);
      log(`Read result: ${JSON.stringify(readResult)}`);
      expect(readResult.success).toBe(false);
      expect(readResult.errorMessage).toBeDefined();

      const infoResult = await fileSystem.getFileInfo(nonExistentPath);
      log(`Info result: ${JSON.stringify(infoResult)}`);
      expect(infoResult.success).toBe(false);
      expect(infoResult.errorMessage).toBeDefined();
    });

    test('should handle invalid parameters', async () => {
      const emptyPathResult = await fileSystem.readFile('');
      log(`Empty path read result: ${JSON.stringify(emptyPathResult)}`);
      expect(emptyPathResult.success).toBe(false);
      expect(emptyPathResult.errorMessage).toBeDefined();
    });
  });

  // 7. 性能和边界测试
  describe('7. Performance and Boundary Tests', () => {
    test('should handle 1MB file efficiently', async () => {
      const largePath = '/tmp/1mb_test.txt';
      const largeContent = 'Performance test content line. '.repeat(35000); // ~1MB

      const writeStart = Date.now();
      const writeResult = await fileSystem.writeLargeFile(largePath, largeContent);
      const writeTime = Date.now() - writeStart;

      expect(writeResult.success).toBe(true);
      expect(writeTime).toBeLessThan(30000); // Should complete within 30 seconds

      const readStart = Date.now();
      const readResult = await fileSystem.readLargeFile(largePath);
      const readTime = Date.now() - readStart;

      expect(readResult.success).toBe(true);
      expect(readResult.content).toBe(largeContent);
      expect(readTime).toBeLessThan(30000);
    });

    test('should handle concurrent operations', async () => {
      const promises: Promise<any>[] = [];

      for (let i = 0; i < 5; i++) {
        const filePath = `/tmp/concurrent_${i}.txt`;
        const content = `Concurrent content ${i}`;

        promises.push(fileSystem.writeFile(filePath, content, 'overwrite'));
      }

      const results = await Promise.all(promises);
      results.forEach(result => {
        expect(result.success).toBe(true);
        expect(result.requestId).toBeDefined();
      });
    });
  });

  // 8. 路径长度边界测试
  describe('8. Path Length Boundary Tests', () => {
    test('should handle normal path lengths', async () => {
      const normalPath = '/tmp/normal_path_test.txt';

      const writeResult = await fileSystem.writeFile(normalPath, 'content', 'overwrite');
      expect(writeResult.success).toBe(true);

      const readResult = await fileSystem.readFile(normalPath);
      expect(readResult.success).toBe(true);
      expect(readResult.content).toBe('content');
    });

    test('should handle long paths within limits', async () => {
      const longDirName = 'long_directory_name_' + 'x'.repeat(50);
      const longFileName = 'long_file_name_' + 'y'.repeat(50) + '.txt';
      const longPath = `/tmp/${longDirName}/${longFileName}`;

      await fileSystem.createDirectory(`/tmp/${longDirName}`);

      const writeResult = await fileSystem.writeFile(longPath, 'long path content', 'overwrite');
      if (writeResult.success) {
        const readResult = await fileSystem.readFile(longPath);
        expect(readResult.success).toBe(true);
        expect(readResult.content).toBe('long path content');
      }
    });

    test('should handle paths with special characters', async () => {
      const spacePath = '/tmp/file with spaces.txt';

      const writeResult = await fileSystem.writeFile(spacePath, 'space content', 'overwrite');
      if (writeResult.success) {
        const readResult = await fileSystem.readFile(spacePath);
        expect(readResult.success).toBe(true);
        expect(readResult.content).toBe('space content');
      }
    });
  });

  // 9. 文件内容极限边界测试
  describe('9. File Content Boundary Tests', () => {
    test('should handle empty file content', async () => {
      const emptyPath = '/tmp/empty_test.txt';

      const writeResult = await fileSystem.writeFile(emptyPath, '', 'overwrite');
      expect(writeResult.success).toBe(true);

      const readResult = await fileSystem.readFile(emptyPath);
      expect(readResult.success).toBe(true);
      expect(readResult.content).toBe('');

      const infoResult = await fileSystem.getFileInfo(emptyPath);
      expect(infoResult.success).toBe(true);
      expect(infoResult.fileInfo!.size).toBe(0);
    });

    test('should handle single long line content', async () => {
      const longLinePath = '/tmp/long_line_test.txt';
      const longLine = 'x'.repeat(10000); // 10KB single line

      const writeResult = await fileSystem.writeFile(longLinePath, longLine, 'overwrite');
      expect(writeResult.success).toBe(true);

      const readResult = await fileSystem.readFile(longLinePath);
      expect(readResult.success).toBe(true);
      expect(readResult.content).toBe(longLine);
      expect(readResult.content.length).toBe(10000);
    });

    test('should handle multiline content with special characters', async () => {
      const specialPath = '/tmp/special_chars_test.txt';
      const specialContent = `Line 1: Normal text
Line 2: Special chars !@#$%^&*()
Line 3: Unicode: 你好世界 🌍
Line 4: Quotes: "double" 'single'
Line 5: Newlines and tabs:\n\t\r\n`;

      const writeResult = await fileSystem.writeFile(specialPath, specialContent, 'overwrite');
      expect(writeResult.success).toBe(true);

      const readResult = await fileSystem.readFile(specialPath);
      expect(readResult.success).toBe(true);
      expect(readResult.content).toBe(specialContent);
      expect(readResult.content).toContain('你好世界');
      expect(readResult.content).toContain('🌍');
    });
  });

  // 10. 极端场景边界测试
  describe('10. Extreme Scenario Tests', () => {
    test('should handle multiple files in directory', async () => {
      const manyFilesDir = '/tmp/many_files_test';
      await fileSystem.createDirectory(manyFilesDir);

      const filePromises = Array.from({ length: 20 }, (_, i) =>
        fileSystem.writeFile(`${manyFilesDir}/file_${i}.txt`, `Content ${i}`, 'overwrite')
      );

      const results = await Promise.all(filePromises);
      results.forEach(result => {
        expect(result.success).toBe(true);
      });

      const listResult = await fileSystem.listDirectory(manyFilesDir);
      expect(listResult.success).toBe(true);
      expect(listResult.entries.length).toBe(20);
    });

    test('should handle deep directory nesting', async () => {
      let currentPath = '/tmp';
      for (let i = 1; i <= 10; i++) {
        currentPath += `/level${i}`;
        const result = await fileSystem.createDirectory(currentPath);
        expect(result.success).toBe(true);
      }

      const deepFilePath = `${currentPath}/deep_file.txt`;
      const writeResult = await fileSystem.writeFile(deepFilePath, 'Deep content', 'overwrite');
      expect(writeResult.success).toBe(true);

      const readResult = await fileSystem.readFile(deepFilePath);
      expect(readResult.success).toBe(true);
      expect(readResult.content).toBe('Deep content');
    });
  });

  // 数据完整性测试
  describe('11. Data Integrity Tests', () => {
    test('should maintain data integrity across operations', async () => {
      const integrityPath = '/tmp/integrity_test.txt';
      const originalContent = 'Original integrity test content with special chars: äöüß';

      // 写入 -> 读取 -> 编辑 -> 读取 -> 移动 -> 读取
      await fileSystem.writeFile(integrityPath, originalContent, 'overwrite');

      let readResult = await fileSystem.readFile(integrityPath);
      expect(readResult.content).toBe(originalContent);

      const edits = [{ oldText: 'Original', newText: 'Modified' }];
      await fileSystem.editFile(integrityPath, edits, false);

      readResult = await fileSystem.readFile(integrityPath);
      expect(readResult.content).toContain('Modified');
      expect(readResult.content).toContain('äöüß');

      const movedPath = '/tmp/integrity_moved.txt';
      await fileSystem.moveFile(integrityPath, movedPath);

      const finalResult = await fileSystem.readFile(movedPath);
      expect(finalResult.success).toBe(true);
      expect(finalResult.content).toContain('Modified');
      expect(finalResult.content).toContain('äöüß');
    });
  });
});
