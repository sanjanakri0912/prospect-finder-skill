import pandas as pd
import glob
import re

files = glob.glob("*.csv")
records = []

for f in files:
    try:
        df = pd.read_csv(f)
        for _, row in df.iterrows():
            rec = {}
            for col in df.columns:
                c_low = col.lower()
                val = str(row[col]).strip() if pd.notna(row[col]) else ""
                if not val or val.lower() == 'nan':
                    continue
                if any(k in c_low for k in ['company', 'clinic', 'business', 'name']):
                    rec['name'] = val
                elif any(k in c_low for k in ['website', 'domain', 'url']):
                    rec['website'] = val
                elif any(k in c_low for k in ['phone', 'contact', 'whatsapp']):
                    rec['phone'] = val
                elif 'city' in c_low or 'location' in c_low:
                    rec['location'] = val
            if rec:
                records.append(rec)
    except Exception as e:
        print(f"Error {f}: {e}")

print(f"Total extracted records: {len(records)}")

# Write unique names and domains to a text file for fast lookup
names = set()
websites = set()

for r in records:
    if 'name' in r:
        names.add(r['name'].lower())
    if 'website' in r:
        websites.add(r['website'].lower())

with open("existing_lookup.txt", "w", encoding="utf-8") as out:
    out.write("NAMES:\n")
    for n in sorted(list(names)):
        out.write(n + "\n")
    out.write("\nWEBSITES:\n")
    for w in sorted(list(websites)):
        out.write(w + "\n")

print(f"Saved {len(names)} unique names and {len(websites)} unique websites.")
