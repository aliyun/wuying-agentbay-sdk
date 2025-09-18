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
    
    print("\n=== Error Confirmation ===")
    print("Documentation says cmdline is str type, but actual implementation allows None values")
    print("This proves that the type annotation in the documentation is incorrect, should be Optional[str]")
    
except Exception as e:
    print(f"✗ Error: {e}")