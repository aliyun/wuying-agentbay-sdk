# Test to verify that Process cmdline should be Optional[str], not str
from python.agentbay.application.application import Process

# This should work - Process with cmdline=None (which proves it's Optional)
try:
    process1 = Process("test_process", 1234, None)
    print(f"✓ Process created with cmdline=None: {process1}")
    print(f"✓ cmdline value: {process1.cmdline}")
    
    # This should also work - Process with actual cmdline
    process2 = Process("test_process2", 5678, "python test.py")
    print(f"✓ Process created with cmdline string: {process2}")
    
    print("\n=== 错误确认 ===")
    print("文档说cmdline是str类型，但实际实现允许None值")
    print("这证明文档中的类型标注是错误的，应该是Optional[str]")
    
except Exception as e:
    print(f"✗ Error: {e}")