import os
import hashlib

episodes = ["A-16", "A-17", "A-18", "A-19"]
roles = ["天文", "文化", "敘事", "語言"]

files = []
for ep in episodes:
    files.append(f"{ep}_考據_gemini.md")
    for r in roles:
        files.append(f"{ep}_審稿-{r}_antigravity.md")

worktree_base = "/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/04_腳本庫/_審稿"
downloads_base = "/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿"

def get_sha256(p):
    if not os.path.exists(p):
        return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

print(f"{'#':<3} | {'Filename':<35} | {'Worktree':<8} | {'Downloads':<9} | {'Match?':<6} | {'Worktree SHA256'} | {'Downloads SHA256'}")
print("-" * 120)

for idx, fname in enumerate(files, 1):
    wp = os.path.join(worktree_base, fname)
    dp = os.path.join(downloads_base, fname)
    w_exists = os.path.exists(wp)
    d_exists = os.path.exists(dp)
    w_hash = get_sha256(wp)
    d_hash = get_sha256(dp)
    match = (w_hash == d_hash) and (w_hash is not None)
    w_h_str = w_hash if w_hash else "MISSING"
    d_h_str = d_hash if d_hash else "MISSING"
    print(f"{idx:<3} | {fname:<35} | {str(w_exists):<8} | {str(d_exists):<9} | {str(match):<6} | {w_h_str} | {d_h_str}")
