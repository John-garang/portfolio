"""
SEO Asset Renaming Script for John Ngor Deng Garang's Graphic Design Portfolio.
Renames files in-place and outputs a JSON manifest grouped by brand.
"""

import os, re, json
from collections import defaultdict

FOLDER = r"C:\Portfolio\templates\static\Pictures\Graphic Design Portfolio"
PREFIX = "John_Ngor_Deng_Garang"

# Priority brand groups (order matters — first match wins)
BRAND_GROUPS = [
    ("Nalafem",                  ["nalafem"]),
    ("Africa_Inventor_Alliance", ["africa inventor alliance", "aia alliance", " aia", "aia.", "aia "]),
    ("nFIX",                     ["nfix", "nfixx", "nfx"]),
    ("Education_Bridge",         ["education bridge"]),
    ("Uganics",                  ["uganics"]),
    ("Creative_Connect",         ["creative connect"]),
    ("Little_Bet_Innovations",   ["little bet"]),
    ("UNLEASH",                  ["unleash"]),
    ("Accra_Fusion",             ["accra fusion"]),
    ("ALU",                      ["alu global", "alu "]),
    ("Indaba",                   ["indaba"]),
    ("BK",                       ["bk1", "bk2", "bk3", "bk4"]),
]

MEDIA_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4"}

def classify(name_lower):
    for group, keywords in BRAND_GROUPS:
        for kw in keywords:
            if kw in name_lower:
                return group
    return None

def main():
    files = [f for f in os.listdir(FOLDER)
             if os.path.splitext(f)[1].lower() in MEDIA_EXTS]

    # First pass: classify every file
    buckets = defaultdict(list)
    for f in files:
        name_lower = f.lower()
        group = classify(name_lower)
        if group:
            buckets[group].append(f)
        else:
            buckets["__unclassified__"].append(f)

    # Dynamic grouping: unclassified files sharing a common token (4+ files)
    unclassified = buckets.pop("__unclassified__", [])
    token_map = defaultdict(list)
    for f in unclassified:
        stem = os.path.splitext(f)[0]
        # Use first meaningful word sequence as token
        token = re.sub(r'[^a-z0-9 ]', '', stem.lower()).strip()
        # Try to find a shared prefix of 2+ words
        words = token.split()
        key = "_".join(w.capitalize() for w in words[:2]) if len(words) >= 2 else words[0].capitalize() if words else "Misc"
        token_map[key].append(f)

    for token, tfiles in token_map.items():
        if len(tfiles) >= 4:
            safe_token = re.sub(r'[^A-Za-z0-9]', '_', token).strip('_')
            buckets[safe_token].extend(tfiles)
        else:
            buckets["General_Graphic_Design"].extend(tfiles)

    # Second pass: rename files and build manifest
    manifest = {}
    for group, group_files in buckets.items():
        group_files.sort()
        manifest[group] = []
        for idx, old_name in enumerate(group_files, start=1):
            ext = os.path.splitext(old_name)[1].lower()
            new_name = f"{PREFIX}_{group}_{idx:02d}{ext}"
            old_path = os.path.join(FOLDER, old_name)
            new_path = os.path.join(FOLDER, new_name)
            if old_path != new_path and not os.path.exists(new_path):
                os.rename(old_path, new_path)
            manifest[group].append(new_name)

    manifest_path = os.path.join(FOLDER, "_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Done. {sum(len(v) for v in manifest.values())} files renamed.")
    print(f"Manifest saved to: {manifest_path}")
    for group, files in manifest.items():
        print(f"  {group}: {len(files)} files")

if __name__ == "__main__":
    main()
