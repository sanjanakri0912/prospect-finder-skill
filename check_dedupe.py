import os

with open("existing_lookup.txt", "r", encoding="utf-8") as f:
    text = f.read()

lines = [l.strip().lower() for l in text.split("\n") if l.strip()]

def check_candidate(name, website):
    name_clean = name.lower()
    website_clean = website.lower().replace("https://", "").replace("http://", "").replace("www.", "").strip("/")
    
    found_name = [l for l in lines if name_clean in l or l in name_clean]
    found_web = [l for l in lines if website_clean in l or l in website_clean] if website_clean else []
    
    print(f"Checking '{name}' ({website}):")
    if found_name:
        print(f"  -> Name match found: {found_name[:3]}")
    else:
        print("  -> Name: CLEAN")
    if found_web:
        print(f"  -> Website match found: {found_web[:3]}")
    else:
        print("  -> Website: CLEAN")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        name = sys.argv[1]
        web = sys.argv[2] if len(sys.argv) > 2 else ""
        check_candidate(name, web)
