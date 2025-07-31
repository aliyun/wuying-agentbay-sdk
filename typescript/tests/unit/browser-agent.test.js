// Simple browser agent unit tests
const { Browser, BrowserAgent } = require('../../dist/index.cjs');

class TestSchema {
  constructor() {
    this.title = "";
    this.content = "";
  }
}

describe('Browser Unit Tests', () => {
  let mockSession;
  let browser;

  beforeEach(() => {
    mockSession = {
      getAPIKey: jest.fn().mockReturnValue('test-api-key'),
      getSessionId: jest.fn().mockReturnValue('test-session-id'),
      getClient: jest.fn().mockReturnValue({
        initBrowser: jest.fn().mockResolvedValue({
          body: {
            data: {
              port: 9222,
              endpoint: 'ws://localhost:9222'
            }
          }
        })
      }),
      callMcpTool: jest.fn().mockResolvedValue({
        success: true,
        data: '{"success": true, "message": "test"}',
        errorMessage: '',
        requestId: 'test-request-id'
      }),
      getLink: jest.fn().mockResolvedValue({
        success: true,
        data: 'ws://localhost:9222',
        requestId: 'test-request-id'
      })
    };
    browser = new Browser(mockSession);
  });

  test('should create browser instance', () => {
    expect(browser).toBeDefined();
    expect(browser.agent).toBeInstanceOf(BrowserAgent);
  });

  test('should initialize browser', async () => {
    const option = { persistentPath: '/tmp/browser' };
    const result = await browser.initializeAsync(option);
    
    expect(result).toBe(true);
    expect(browser.isInitialized()).toBe(true);
    expect(browser.getOption()).toEqual(option);
  });

  test('should get endpoint URL when initialized', async () => {
    const option = { persistentPath: '/tmp/browser' };
    await browser.initializeAsync(option);
    
    const endpointUrl = await browser.getEndpointUrl();
    expect(endpointUrl).toBe('ws://localhost:9222');
    expect(mockSession.getLink).toHaveBeenCalled();
  });

  test('should throw error when getting endpoint URL without initialization', async () => {
    await expect(browser.getEndpointUrl()).rejects.toThrow('Browser is not initialized');
  });

  test('should perform act operation', async () => {
    await browser.initializeAsync({});
    
    const mockPage = { url: () => 'http://example.com' };
    const options = { action: 'Click search button' };
    
    const result = await browser.agent.act(mockPage, options);
    
    expect(result.success).toBe(true);
    expect(mockSession.callMcpTool).toHaveBeenCalledWith('page_use_act', expect.any(Object));
  });

  test('should perform observe operation', async () => {
    await browser.initializeAsync({});
    
    mockSession.callMcpTool.mockResolvedValue({
      success: true,
      data: '{"success": true, "observe_result": "[]"}',
      errorMessage: '',
      requestId: 'test-request-id'
    });
    
    const mockPage = { url: () => 'http://example.com' };
    const options = { instruction: 'Find the search button' };
    
    const [success, results] = await browser.agent.observe(mockPage, options);
    
    expect(success).toBe(true);
    expect(Array.isArray(results)).toBe(true);
    expect(mockSession.callMcpTool).toHaveBeenCalledWith('page_use_observe', expect.any(Object));
  });

  test('should perform extract operation', async () => {
    await browser.initializeAsync({});
    
    mockSession.callMcpTool.mockResolvedValue({
      success: true,
      data: '{"success": true, "extract_result": "[{\\"title\\": \\"Test Title\\"}]"}',
      errorMessage: '',
      requestId: 'test-request-id'
    });
    
    const mockPage = { url: () => 'http://example.com' };
    const options = { 
      instruction: 'Extract the title', 
      schema: TestSchema 
    };
    
    const [success, objects] = await browser.agent.extract(mockPage, options);
    
    expect(success).toBe(true);
    expect(Array.isArray(objects)).toBe(true);
    expect(mockSession.callMcpTool).toHaveBeenCalledWith('page_use_extract', expect.any(Object));
  });

  test('should handle act operation failure', async () => {
    await browser.initializeAsync({});
    
    mockSession.callMcpTool.mockResolvedValue({
      success: false,
      data: '',
      errorMessage: 'Test error',
      requestId: 'test-request-id'
    });
    
    const mockPage = { url: () => 'http://example.com' };
    const options = { action: 'Click search button' };
    
    const result = await browser.agent.act(mockPage, options);
    
    expect(result.success).toBe(false);
    expect(result.message).toBe('Test error');
  });

  test('should throw error when browser not initialized for operations', async () => {
    const mockPage = { url: () => 'http://example.com' };
    
    await expect(browser.agent.act(mockPage, { action: 'test' })).rejects.toThrow('Browser must be initialized');
    await expect(browser.agent.observe(mockPage, { instruction: 'test' })).rejects.toThrow('Browser must be initialized');
    await expect(browser.agent.extract(mockPage, { instruction: 'test', schema: TestSchema })).rejects.toThrow('Browser must be initialized');
  });
}); 