import re
import os

docs_path = "/Users/liyuebing/Projects/wuying-agentbay-sdk/docs"
readme_path = os.path.join(docs_path, "README.md")

with open(readme_path, 'r') as f:
    content = f.read()

link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
links = re.findall(link_pattern, content)

missing = []
existing = []
http_links = []

for title, path in links:
    if path.startswith('http'):
        http_links.append((title, path))
        continue
    if path.startswith('#'):
        continue
    
    if path.startswith('../'):
        full_path = os.path.join(docs_path, '..', path.replace('../', ''))
    else:
        full_path = os.path.join(docs_path, path)
    
    full_path = os.path.normpath(full_path)
    
    if os.path.exists(full_path):
        existing.append((title, path))
    else:
        missing.append((title, path))

print("=== MISSING FILES ===")
if missing:
    for title, path in missing:
        print(f"❌ [{title}]({path})")
else:
    print("✅ No missing files!")

print(f"\n=== SUMMARY ===")
print(f"Total local links: {len(links) - len(http_links)}")
print(f"Existing: {len(existing)}")
print(f"Missing: {len(missing)}")
print(f"HTTP links: {len(http_links)}")

if missing:
    print("\n=== MISSING FILES DETAILS ===")
    for title, path in missing:
        print(f"  - {path}")
