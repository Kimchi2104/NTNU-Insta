# -*- coding: utf-8 -*-
"""萬國星空｜Canva 逐頁製作表＋逐頁對位參考圖（v1）

把 make_{ep}_v4.py 的鏡頭清單，展開成「Canva 裡一頁一頁要做什麼」：

  {EP}_Canva逐頁製作表.csv   一列＝Canva 一頁（依頁序），欄位直接對應 Canva
                            「位置」面板：寬 W／高 H／X／Y（左上角，px）／旋轉；
                            頁名沿用團隊習慣：鏡頭01開始、鏡頭01結束、長圖轉北盤1…
                            並列出該頁要留哪幾層連線／標籤、旁白、字卡、概念圖、地平線高度
  {EP}_Canva逐頁製作表.md    同上，給人看的版本
  {EP}_逐頁標籤座標.csv       每頁每條標籤：原文／拼音／英文／中文、中心 X/Y px、字級 px、色碼
                            → 不必再用 SVG 標籤層（Canva 解析度不夠），直接原生打字對位
  {EP}_標籤對照表.csv         全集名詞：原文／拼音／英文翻譯／中文／來源（給不會中文的組員複製貼上）
  {EP}_對位參考/P##_頁名.png  每頁 1080×1920：畫面長相＋標籤虛影＋主角星白圈＋Reels 安全區
                            ＋地平線；放在該頁最上層當描圖紙，對好就刪

座標系（與 gen_master_canvas 一致）：
  長圖頁：元素寬 W＝360/fov×1080；盤頁：W＝H＝2·R_fill/fov×1080
  X/Y＝元素「未旋轉時」的左上角（Canva 位置面板）；旋轉以元素中心為軸，
  盤心置中時旋轉不影響 X/Y。北盤負角＝逆時針＝時間往前（1 小時＝15.041°）。

用法：
  python3 gen_canva_pages.py A-07              # 讀 05_素材/*/_v4大畫布/A-07_*
  python3 gen_canva_pages.py A-07 --seg 2.5    # 每段移動拆成 ≤2.5 秒的中間頁
  python3 gen_canva_pages.py A-07 --no-png     # 只出表格
"""
import os, sys, csv, json, math, glob, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, R_RIM
from gen_projection import great_circle, COLORS, horizon_points

PW, PH = 1080, 1920          # Reels 頁面
SAFE = 250                   # Reels 上下安全區
HEX = dict(COLORS)


def find_folder(base, ep):
    hits = glob.glob(os.path.join(base, "05_素材", "*", "_v4大畫布", f"{ep}_畫布資訊.json"))
    if not hits:
        sys.exit(f"找不到 {ep}_畫布資訊.json（先跑 make_{ep.lower().replace('-', '')}_v4.py）")
    return os.path.dirname(hits[0])


class Pages:
    def __init__(self, ep, seg=0.0):
        self.base = G.find_base(os.path.dirname(os.path.abspath(__file__)))
        self.ep = ep
        self.dir = find_folder(self.base, ep)
        self.info = json.load(open(os.path.join(self.dir, f"{ep}_畫布資訊.json"),
                                   encoding="utf-8"))
        self.shots = json.load(open(os.path.join(self.dir, f"{ep}_鏡頭清單.json"),
                                    encoding="utf-8"))
        lp = os.path.join(self.dir, f"{ep}_標籤資料.json")
        self.lab = json.load(open(lp, encoding="utf-8")) if os.path.exists(lp) else {}
        P = self.info["params"]
        self.S = G.load_stars(self.base)
        self.m = Master(ep, self.S, os.path.join(self.dir, "_tmp_pages"),
                        lst=P["lst"], D_s=P["D_s"], D_r=P["D_r"], D_fill=P["D_fill"],
                        w_c=P["w_c"], feather=P["feather"], x_tN=P["x_tN"],
                        x_tS=P["x_tS"], maglim=P["maglim"])
        try:
            os.rmdir(os.path.join(self.dir, "_tmp_pages"))
        except OSError:
            pass
        self.seg = seg
        self.layer_files = [l["file"] for l in self.info.get("layers", [])]

    # ───────── 頁序 ─────────
    def build_pages(self):
        pages, n_in, n_out = [], 0, 0
        for sh in self.shots:
            grp = "長圖"
            if sh["kind"] == "R":
                grp = "北盤" if sh.get("north", True) else "南盤"
            frs = [tuple(f) for f in sh["frames"]]
            keys = self._split(frs, sh["sec"]) if self.seg > 0 else \
                [(i / (len(frs) - 1) if len(frs) > 1 else 0.0, f) for i, f in enumerate(frs)]
            for j, (t, fr) in enumerate(keys):
                last = j == len(keys) - 1
                nm = (f"鏡頭{sh['code']}開始" if j == 0 else
                      f"鏡頭{sh['code']}結束" if last else f"鏡頭{sh['code']}-中{j}")
                pg = dict(name=nm, shot=sh, group=grp, frame=fr, t=t,
                          sec=sh["sec"] * (t - keys[j - 1][0]) if j else 0.0)
                if j == 0 and pages:
                    prev = pages[-1]
                    same = all(abs(a - b) < 1e-6 for a, b in zip(prev["frame"], fr))
                    if same and prev["group"] == grp:          # 同框同組：一頁兩用
                        prev["name"] += f"＝{nm}"
                        prev["shot_next"] = sh
                        continue
                    if same:                                  # 同框換組：轉場頁
                        if grp != "長圖":
                            n_in += 1
                            pg["name"] = f"長圖轉{grp}{n_in}＝{nm}"
                        else:
                            n_out += 1
                            pg["name"] = f"{prev['group']}轉長圖{n_out}＝{nm}"
                        pg["trans"] = "無（同框硬切：前一頁複製後只換圖層組）"
                    else:
                        pg["trans"] = "無（硬切，新構圖）"
                        if prev["group"] != grp and grp == "長圖":
                            pg["trans"] += (f"；{prev['group']}→長圖不同框，"
                                            "若要同框接回＝複製前頁、倒序轉回 0°")
                elif j == 0:
                    pg["trans"] = "（第一頁）"
                else:
                    pg["trans"] = f"Match & Move（{pg['sec']:.1f} 秒）"
                pages.append(pg)
        for i, pg in enumerate(pages, 1):
            pg["no"] = i
        self.pages = pages
        return pages

    def _split(self, frs, sec):
        """每段 ≤ seg 秒：在關鍵格之間插中間頁（Canva 元素空間線性內插＝M&M 本身的內插）"""
        out = [(0.0, frs[0])]
        nseg = len(frs) - 1
        for k in range(nseg):
            dur = sec / nseg
            n = max(1, math.ceil(dur / self.seg - 1e-9))
            a, b = frs[k], frs[k + 1]
            wa, wb = 1.0 / a[2], 1.0 / b[2]              # 元素寬 ∝ 1/fov → 線性內插寬
            for i in range(1, n + 1):
                s = i / n
                w = wa + (wb - wa) * s
                fov = 1.0 / w
                # 畫面中心在元素座標裡線性移動：cx/fov 內插
                cx = (a[0] * wa + (b[0] * wb - a[0] * wa) * s) / w
                cy = (a[1] * wa + (b[1] * wb - a[1] * wa) * s) / w
                rot = a[3] + (b[3] - a[3]) * s
                out.append(((k + s) / nseg, (cx, cy, fov, rot)))
        return out

    # ───────── Canva 位置面板數字 ─────────
    def placement(self, pg):
        cx, cy, fov, rot = pg["frame"]
        u = PW / fov
        m = self.m
        x0, y0, x1, y1 = m.extent
        if pg["group"] == "長圖":
            W = (x1 - x0) * u; H = (y1 - y0) * u
            X = PW / 2 - (cx - x0) * u; Y = PH / 2 - (y1 - cy) * u
            return dict(W=W, H=H, X=X, Y=Y, rot=0.0)
        north = pg["group"] == "北盤"
        xt, yc = m.disc_center(north)
        W = H = 2 * m.R_fill * u
        ccx = PW / 2 + (xt - cx) * u; ccy = PH / 2 - (yc - cy) * u
        return dict(W=W, H=H, X=ccx - W / 2, Y=ccy - H / 2, rot=rot)

    def to_screen(self, pg, x, y, local=False):
        """畫布座標（長圖）或盤內局部座標（盤，未旋轉）→ 頁面 px"""
        cx, cy, fov, rot = pg["frame"]
        u = PW / fov
        if pg["group"] != "長圖":
            north = pg["group"] == "北盤"
            xt, yc = self.m.disc_center(north)
            a = math.radians(-rot)                     # Canva 正角＝順時針
            if not local:
                x, y = x - xt, y - yc
            x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
            x, y = x + xt, y + yc
        return PW / 2 + (x - cx) * u, PH / 2 - (y - cy) * u

    # ───────── 標籤 ─────────
    def label_sets(self):
        return {ls["name"]: ls["items"] for ls in self.lab.get("label_sets", [])}

    @staticmethod
    def label_names(pg):
        """本頁要開的標籤層：一頁兩用時取下一鏡；鏡頭最後一格可用 labels_end 換層"""
        sh = pg.get("shot_next") or pg["shot"]
        if pg.get("shot_next"):
            return sh.get("labels", [])
        if pg["t"] >= 1.0 and "labels_end" in sh:
            return sh["labels_end"]
        return sh.get("labels", [])

    def page_labels(self, pg):
        names = self.label_names(pg)
        sets = self.label_sets()
        m, S = self.m, self.S
        cx, cy, fov, rot = pg["frame"]
        out = []
        for nm in names:
            for it in sets.get(nm, []):
                if "hip" in it:
                    if it["hip"] not in S:
                        continue
                    ra, dec = S[it["hip"]][:2]
                else:
                    ra, dec = it["ra"], it["dec"]
                dx, dy = it.get("dx", 0.0), it.get("dy", 1.3)
                if pg["group"] == "長圖":
                    p = m.pos_primary(ra, dec)
                    X, Y = self.to_screen(pg, p[0] + dx, p[1] + dy)
                    sX, sY = self.to_screen(pg, *p)
                else:
                    north = pg["group"] == "北盤"
                    if (dec if north else -dec) < m.Dr:        # 同 D_labels：帶內標籤不進盤
                        continue
                    q = m.to_disc_local(m.p_disc(m.xw(ra), dec, north), north)
                    sX, sY = self.to_screen(pg, *q, local=True)
                    X, Y = sX + dx * PW / fov, sY - dy * PW / fov   # 原生文字不跟著轉
                fpx = it.get("size", 1.0) * m.fu * PW / fov
                if -40 <= X <= PW + 40 and -20 <= Y <= PH + 20:
                    out.append(dict(layer=nm, text=it["text"], key=it.get("key", ""),
                                    color=HEX.get(it.get("color", "white"),
                                                  it.get("color", "#FFFFFF")),
                                    X=X, Y=Y, starX=sX, starY=sY, font_px=fpx))
        return out

    def horizon_rows(self, pg):
        sh = pg["shot"]
        hz = sh.get("horizon") or []
        if not hz or pg["group"] == "長圖":
            return []
        cx, cy, fov, rot = pg["frame"]
        out = []
        yc = self.m.disc_center(pg["group"] == "北盤")[1]
        for phi in hz:                        # 地平線固定在畫面上（不隨盤轉）：
            Y = PH / 2 - (yc - self.m.k * phi - cy) * PW / fov   # 北點＝盤心正下方 kφ
            out.append((phi, Y))
        return out

    def horizon_curve(self, pg, phi):
        """地平線在頁面上的整條曲線（固定不動；天空在它後面轉）"""
        m = self.m
        cx, cy, fov, rot = pg["frame"]
        lst_view = m.lst - rot                  # 盤轉 rot ≡ lst 平移（sb_grid 同理）
        lst_obs = (lst_view - 180.0) % 360.0    # 盤心正下方＝北方地平線（下中天）
        pts = []
        save = m.lst
        m.lst = lst_view
        for ra, dec in horizon_points(phi, lst_obs, n=361):
            if dec < m.Dfill:
                pts.append(None); continue
            p = m.p_disc(m.xw(ra), dec, True)
            xt, yc = m.disc_center(True)
            X, Y = PW / 2 + (p[0] - cx) * PW / fov, PH / 2 - (p[1] - cy) * PW / fov
            pts.append((X, Y))
        m.lst = save
        return pts

    # ───────── 輸出 ─────────
    def layers_for(self, pg):
        sh = pg["shot"]
        key = "北盤" if pg["group"] == "北盤" else "南盤" if pg["group"] == "南盤" else ""
        want = ["銀河", "星點", "經緯線"]
        lines_map = self.lab.get("lines", {"L4": "星座連線"})
        want += [lines_map.get(k, k) for k in sh.get("layers", ["L4"])]
        want += ["主角星白點"]
        want += [f"標籤-{n}" for n in self.label_names(pg)]
        import re
        pat = re.compile(rf"^{re.escape(self.ep)}_(北盤|南盤)?L\d+-(.+)\.svg$")
        got = []
        for w in want:
            for f in self.layer_files:
                mm = pat.match(f)
                if not mm or (mm.group(1) or "") != key or mm.group(2) != w:
                    continue
                got.append(f.replace(f"{self.ep}_", "").replace(".svg", ""))
        return got

    def write(self, png=True):
        pages = self.build_pages()
        rows, lab_rows = [], []
        for pg in pages:
            sh = pg["shot"]
            pl = self.placement(pg)
            hz = self.horizon_rows(pg)
            is_start = pg["name"].startswith(f"鏡頭{sh['code']}開始") or "＝鏡頭" in pg["name"]
            shv = pg.get("shot_next") or sh
            rows.append({
                "頁": pg["no"], "頁名": pg["name"], "鏡頭": sh["code"], "原型": sh["kind"],
                "圖層組": pg["group"], "寬W px": round(pl["W"], 1), "高H px": round(pl["H"], 1),
                "X px": round(pl["X"], 1), "Y px": round(pl["Y"], 1),
                "旋轉°": round(pl["rot"], 1),
                "與上一頁": pg.get("trans", ""),
                "本段秒數": round(pg["sec"], 1) if pg["sec"] else "",
                "鏡頭總秒數": sh["sec"],
                "留下的圖層": "、".join(self.layers_for(pg)),
                "概念圖": sh.get("overlay", ""), "字卡": sh.get("card", ""),
                "地平線北點Y px": "；".join(f"緯度{p:g}°→{y:.0f}" for p, y in hz),
                "旁白（本頁起播）": shv.get("vo", "") if (is_start or pg.get("shot_next")) else "",
                "備註": shv.get("note", "") if (is_start or pg.get("shot_next")) else "",
            })
            for lb in self.page_labels(pg):
                lab_rows.append({"頁": pg["no"], "頁名": pg["name"], "標籤層": lb["layer"],
                                 "文字": lb["text"], "中心X px": round(lb["X"]),
                                 "中心Y px": round(lb["Y"]), "字級px": round(lb["font_px"]),
                                 "顏色": lb["color"], "對應星X": round(lb["starX"]),
                                 "對應星Y": round(lb["starY"]), "key": lb["key"]})
        self._csv(f"{self.ep}_Canva逐頁製作表.csv", rows)
        self._csv(f"{self.ep}_逐頁標籤座標.csv", lab_rows)
        self._terms_csv()
        self._md(rows)
        if png:
            d = os.path.join(self.dir, f"{self.ep}_對位參考")
            os.makedirs(d, exist_ok=True)
            for f in glob.glob(os.path.join(d, "*.png")):
                os.remove(f)
            for pg in pages:
                self.render(pg, d)
            print(f"  ✓ {self.ep}_對位參考/（{len(pages)} 張 1080×1920）")
        print(f"  ✓ 共 {len(pages)} 頁；標籤座標 {len(lab_rows)} 筆")

    def _csv(self, name, rows):
        if not rows:
            return
        with open(os.path.join(self.dir, name), "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
        print(f"  ✓ {name}")

    def _terms_csv(self):
        rows = []
        for k, t in self.lab.get("terms", {}).items():
            rows.append({"項目": k, "原文": t["原文"], "拼音": t["拼音"],
                         "英文翻譯": t["英文翻譯"], "中文": t["中文"],
                         "顏色": HEX.get(t["顏色"], t["顏色"]), "來源／備註": t["來源備註"]})
        for c in self.lab.get("cross", []):
            rows.append({"項目": "跨文化", "原文": c["原文"], "拼音": "",
                         "英文翻譯": "", "中文": c["中譯"],
                         "顏色": HEX.get(c["顏色"], c["顏色"]), "來源／備註": "Stellarium"})
        seen = set()
        for ls in self.lab.get("label_sets", []):
            for it in ls["items"]:
                if it.get("key", "").startswith("HIP") and (ls["name"], it["key"]) not in seen:
                    seen.add((ls["name"], it["key"]))
                    rows.append({"項目": f"{ls['name']}｜{it['key']}", "原文": it["text"],
                                 "拼音": "", "英文翻譯": "", "中文": "",
                                 "顏色": HEX.get(it.get("color", "white"), "#FFFFFF"),
                                 "來源／備註": ""})
        self._csv(f"{self.ep}_標籤對照表.csv", rows)

    def _md(self, rows):
        L = [f"# {self.ep}｜Canva 逐頁製作表（自動產生，勿手改；改鏡頭請改 make 腳本後重跑）", "",
             "- **X／Y＝Canva「位置」面板的左上角**（未旋轉時）；寬高直接填。",
             "- 頁名＝團隊慣例；「＝」表示同一頁兩用（上一鏡迄格＝下一鏡起格）。",
             "- 「長圖轉北盤」＝前一頁複製一份、只把長圖圖層組換成北盤圖層組（同框硬切）。",
             "- 標籤請看 `逐頁標籤座標.csv`＋`對位參考/`：原生打字，把文字中心放到虛影上。", "",
             "| 頁 | 頁名 | 組 | W | H | X | Y | 旋轉 | 與上一頁 | 留下的圖層 | 旁白 |",
             "|---:|---|---|---:|---:|---:|---:|---:|---|---|---|"]
        for r in rows:
            L.append(f"| {r['頁']} | {r['頁名']} | {r['圖層組']} | {r['寬W px']} | "
                     f"{r['高H px']} | {r['X px']} | {r['Y px']} | {r['旋轉°']} | "
                     f"{r['與上一頁']} | {r['留下的圖層']} | {r['旁白（本頁起播）']} |")
        open(os.path.join(self.dir, f"{self.ep}_Canva逐頁製作表.md"), "w",
             encoding="utf-8").write("\n".join(L) + "\n")
        print(f"  ✓ {self.ep}_Canva逐頁製作表.md")

    # ───────── 對位參考圖 ─────────
    def render(self, pg, outdir):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        m, S = self.m, self.S
        FP, FS = G.find_font(), MC.find_serif()
        f = plt.figure(figsize=(PW / 100, PH / 100), dpi=100)
        ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(0, PW); ax.set_ylim(PH, 0); ax.axis("off")
        f.patch.set_facecolor(COLORS["bg"])
        cx, cy, fov, rot = pg["frame"]
        u = PW / fov
        disc = pg["group"] != "長圖"
        north = pg["group"] != "南盤"

        def put(x, y, local=False):
            return self.to_screen(pg, x, y, local=local)

        def inside(X, Y, pad=30):
            return -pad <= X <= PW + pad and -pad <= Y <= PH + pad
        # 銀河（與 L1 同一組取樣）
        xs, ys, ss = [], [], []
        for ra, dec, sz in m._mw_samples()[::2]:
            pts = m.pos_disc(ra, dec, north) if disc else m.pos_all(ra, dec)
            for p in pts:
                X, Y = put(*p, local=disc)
                if inside(X, Y):
                    xs.append(X); ys.append(Y); ss.append((sz * u * 0.9) ** 2)
        ax.scatter(xs, ys, s=ss, c=COLORS["mw"], alpha=.25, lw=0, zorder=1)
        # 星點
        xs, ys, ss = [], [], []
        for h, (ra, dec, v) in S.items():
            if v > m.maglim:
                continue
            pts = m.pos_disc(ra, dec, north) if disc else m.pos_all(ra, dec)
            for p in pts:
                X, Y = put(*p, local=disc)
                if inside(X, Y):
                    xs.append(X); ys.append(Y)
                    ss.append(max(1.2, m.sz_star(v) * u * 1.1) ** 2)
        ax.scatter(xs, ys, s=ss, c="#FFFFFF", lw=0, zorder=2)
        # 連線（本頁留下的）
        lg = self.lab.get("line_groups", {})
        sh = pg["shot"]
        for key in sh.get("layers", ["L4"]):
            for segs, col, _ in lg.get(key, []):
                for seg in segs:
                    hs = [h for h in seg if h in S]
                    for a, b in zip(hs, hs[1:]):
                        gc = great_circle(*S[a][:2], *S[b][:2])
                        runs = m._runs_disc(gc, north) if disc else m.runs_all(gc)
                        for r in runs:
                            P = [put(*p, local=disc) for p in r]
                            ax.plot([p[0] for p in P], [p[1] for p in P],
                                    c=HEX.get(col, col), lw=max(1.0, m.lw * u * 0.9),
                                    alpha=.85, zorder=4, solid_capstyle="round")
        # 主角星白圈（指認用）
        for h in self.lab.get("mains", []):
            if h not in S:
                continue
            ra, dec, v = S[h]
            pts = m.pos_disc(ra, dec, north) if disc else m.pos_all(ra, dec)
            for p in pts:
                X, Y = put(*p, local=disc)
                if inside(X, Y, 0):
                    ax.add_patch(plt.Circle((X, Y), max(10, m.sz_star(v) * 6 * u),
                                            fill=False, ec="#FFFFFF", lw=1.2,
                                            alpha=.8, zorder=6))
        # 地平線
        for phi in sh.get("horizon") or []:
            if not disc:
                continue
            pts = self.horizon_curve(pg, phi)
            run = []
            for p in pts + [None]:
                if p is None or not inside(*p, 200):
                    if len(run) > 1:
                        ax.plot([q[0] for q in run], [q[1] for q in run], c="#48E39B",
                                lw=2.2, alpha=.9, zorder=7)
                    run = []
                else:
                    run.append(p)
            for ph, Y in self.horizon_rows(pg):
                if abs(ph - phi) < 1e-9:
                    ax.text(PW - 24, Y + 12, f"地平線（緯度 {phi:g}°）北點 Y={Y:.0f}",
                            fontproperties=FP, fontsize=15, color="#48E39B",
                            ha="right", va="top", zorder=9)
        # 標籤虛影＋中心十字
        for lb in self.page_labels(pg):
            ax.text(lb["X"], lb["Y"], G.rtl(lb["text"]), fontproperties=FS,
                    fontsize=lb["font_px"] * 0.72, color=lb["color"], alpha=.75,
                    ha="center", va="center", zorder=8)
            ax.plot([lb["X"] - 7, lb["X"] + 7], [lb["Y"], lb["Y"]], c="#FF6B6B", lw=1, zorder=9)
            ax.plot([lb["X"], lb["X"]], [lb["Y"] - 7, lb["Y"] + 7], c="#FF6B6B", lw=1, zorder=9)
        # 安全區與頁頭
        for y0, y1 in ((0, SAFE), (PH - SAFE, PH)):
            ax.add_patch(plt.Rectangle((0, y0), PW, y1 - y0, fc="#000000", ec="none",
                                       alpha=.35, zorder=10))
        pl = self.placement(pg)
        ax.text(20, 22, f"P{pg['no']:02d}　{pg['name']}　［{pg['group']}］",
                fontproperties=FP, fontsize=26, color="#FFC94A", ha="left", va="top",
                weight="bold", zorder=11)
        ax.text(20, 72, f"W {pl['W']:.0f}　H {pl['H']:.0f}　X {pl['X']:.0f}　Y {pl['Y']:.0f}"
                        f"　旋轉 {pl['rot']:+.1f}°　｜　{pg.get('trans', '')}",
                fontproperties=FP, fontsize=15, color="#9FB3D9", ha="left", va="top",
                zorder=11)
        vo = (pg.get("shot_next") or sh).get("vo", "")
        if vo and (pg["t"] == 0.0 or pg.get("shot_next")):
            import textwrap
            ax.text(20, PH - SAFE + 18, "\n".join(textwrap.wrap(vo, 34)[:5]),
                    fontproperties=FP, fontsize=17, color="#FFFFFF", alpha=.9,
                    ha="left", va="top", zorder=11, linespacing=1.4)
        safe_nm = pg["name"].replace("／", "_").replace("/", "_")
        f.savefig(os.path.join(outdir, f"P{pg['no']:02d}_{safe_nm}.png"),
                  facecolor=COLORS["bg"])
        plt.close(f)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ep")
    ap.add_argument("--seg", type=float, default=0.0,
                    help="每段移動最長秒數；>0 時自動插中間頁（Canva 轉場時間不夠長時用）")
    ap.add_argument("--no-png", action="store_true")
    a = ap.parse_args()
    Pages(a.ep, seg=a.seg).write(png=not a.no_png)
