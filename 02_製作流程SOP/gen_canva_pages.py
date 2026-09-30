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
  {EP}_Canva頁面參數.json    同一份數字的機器版（Claude 用 Canva 連接器逐頁排版時讀這個）
  {EP}_對位參考/P##_頁名.png  每頁 1080×1920：畫面長相＋標籤虛影＋主角星白圈＋Reels 安全區
                            ＋地平線；放在該頁最上層當描圖紙，對好就刪

座標系（與 gen_master_canvas 一致）：
  長圖頁：元素寬 W＝360/fov×1080；盤頁：W＝H＝2·R_fill/fov×1080
  X/Y＝元素「未旋轉時」的左上角（Canva 位置面板）；旋轉以元素中心為軸，
  盤心置中時旋轉不影響 X/Y。北盤負角＝逆時針＝時間往前（1 小時＝15.041°）。
  長圖 H 用 Canva 取整後的比例（360×466），Y 由內容中心反推（見 placement）。

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
            first = None                         # 這一鏡的起格頁（可能是與上一鏡共用的那頁）
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
                        first = len(pages) - 1
                        continue
                    pg["trans"] = "無（硬切，新構圖）"      # 換圖層組的頁由 _bridges 補轉場
                elif j == 0:
                    pg["trans"] = "（第一頁）"
                else:
                    pg["trans"] = f"Match & Move（{pg['sec']:.1f} 秒）"
                pages.append(pg)
                if first is None:
                    first = len(pages) - 1
            files = self.overlay_files(sh)
            if files:
                if sh.get("overlay_at", "end") == "start":
                    pages[first + 1:first + 1] = self._holds(sh, pages[first], files, clear=False)
                else:
                    pages += self._holds(sh, pages[-1], files, clear=True)
        pages = self._bridges(pages)
        for i, pg in enumerate(pages, 1):
            pg["no"] = i
        self.pages = pages
        return pages

    # ───────── 長圖⇄盤 轉場（團隊做法：同框換組＋倒放回來） ─────────
    TRANS_MM = "Match & Move（轉場，≤2.5 秒）"

    # ───────── 概念圖定格頁（同一鏡多頁、畫面不動） ─────────
    PANEL = dict(left=24, top=0, width=1032, height=0, color="#000000",
                 opacity=0.75, radius=48)            # 團隊半透明黑底圓角框（韓國集同款）

    def overlay_files(self, sh):
        """_概念圖/ 裡這一鏡要疊的檔案（依序＝一頁多一層）"""
        ov = sh.get("overlay")
        if not ov:
            return []
        d = os.path.join(os.path.dirname(self.dir), "_概念圖")
        if sh.get("overlay_layers"):
            files = [f"{ov}_{L}_透明.png" for L in sh["overlay_layers"]]
        else:
            files = next(([c] for c in (f"{ov}_透明.png", f"{ov}_圖卡.png", f"{ov}.png")
                          if os.path.exists(os.path.join(d, c))), [f"{ov}_透明.png"])
        miss = [f for f in files if not os.path.exists(os.path.join(d, f))]
        if miss:
            print(f"  ⚠ 鏡頭{sh['code']} 概念圖找不到：{miss}（先跑 make_*_diagrams.py）")
        return files

    def overlay_box(self, fn, group):
        """概念圖在頁面上的位置。
        9:16 圖卡＝滿版；方形分層圖＝寬 1032 置中，整組（group＝這一鏡全部層）內容的
        聯集框垂直置中在畫面中心，後面墊團隊的半透明黑底圓角框（只包住內容＋留白）"""
        from PIL import Image
        d = os.path.join(os.path.dirname(self.dir), "_概念圖")
        path = os.path.join(d, fn)
        if not os.path.exists(path):
            return dict(left=0, top=0, width=PW, height=PH), None
        w, h = Image.open(path).size
        if abs(h / w - PH / PW) < 0.05:
            return dict(left=0, top=0, width=PW, height=PH), None
        P = dict(self.PANEL)
        sc = P["width"] / w
        boxes = [Image.open(os.path.join(d, f)).getchannel("A").getbbox()
                 for f in group if os.path.exists(os.path.join(d, f))]
        boxes = [b for b in boxes if b] or [(0, 0, w, h)]
        x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
        x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
        top = PH / 2 - (y0 + y1) / 2 * sc
        pad = 40
        pt, pb = max(SAFE / 2, top + y0 * sc - pad), min(PH - SAFE / 2, top + y1 * sc + pad)
        P.update(top=pt, height=pb - pt)
        return dict(left=P["left"], top=top, width=w * sc, height=h * sc), P

    def _holds(self, sh, base, files, clear):
        n, out = len(files), []
        for i in range(1, n + 1):
            nm = f"鏡頭{sh['code']}-概念圖" + (f"{i}" if n > 1 else "")
            tr = ("Match & Move（畫面不動；概念圖" + (f"第 {i} 層" if n > 1 else "") + "淡入）")
            out.append(dict(name=nm, shot=sh, group=base["group"], frame=base["frame"],
                            t=base["t"], sec=0.0, trans=tr, hold=True, labels_from=base,
                            overlay_files=files[:i]))
        if clear:                                 # 收：畫面不動、概念圖淡出，後面接換組／下一鏡都乾淨
            out.append(dict(name=f"鏡頭{sh['code']}-概念圖收", shot=sh, group=base["group"],
                            frame=base["frame"], t=base["t"], sec=0.0, hold=True,
                            labels_from=base, overlay_files=[],
                            trans="Match & Move（畫面不動；概念圖淡出）"))
        return out

    def _bridge_page(self, name, group, frame, shot, trans):
        sh = {k: v for k, v in shot.items()
              if k not in ("labels", "labels_end", "vo", "note", "overlay", "card")}
        return dict(name=name, shot=sh, group=group, frame=tuple(frame), t=0.5, sec=0.0,
                    trans=trans, transition=True)

    def _bridges(self, pages):
        """長圖→盤：先回長圖中心（走廊 x_t），沿走廊往上到盤心，同框硬切換成盤組。
        盤→長圖：盤轉回 0° 回到換組那一格，同框硬切換回長圖，再往下回到出發點（＝前面的倒放）。
        換組那兩頁畫面逐點相同（check_disc_align 驗證），觀眾看不出換了檔。"""
        same = lambda a, b: all(abs(x - y) < 1e-6 for x, y in zip(a, b))
        out, state, n_in, n_out = [], None, 0, 0
        for pg in pages:
            prev = out[-1] if out else None
            if prev and prev["group"] == "長圖" and pg["group"] != "長圖":
                grp, north = pg["group"], pg["group"] == "北盤"
                xt, yc = self.m.disc_center(north)
                pf, sh_prev = prev["frame"], prev.get("shot_next") or prev["shot"]
                n_in += 1
                if abs(pf[0] - xt) < 1e-6 and abs(pf[1] - yc) < 1e-6:
                    f_sw = pf[2]
                    t0 = sh_prev["frames"][0]            # 往上的起點＝這一鏡（T）的起格
                    origin = tuple(t0) if sh_prev["kind"] == "T" else (xt, 0.0, f_sw, 0.0)
                else:
                    f_sw = min(pf[2], pg["frame"][2], 50.0)
                    origin = (xt, 0.0, f_sw, 0.0)
                    if not same(pf, origin):
                        out.append(self._bridge_page(f"長圖轉{grp}{n_in}-回中心", "長圖", origin,
                                                     sh_prev, self.TRANS_MM))
                    out.append(self._bridge_page(f"長圖轉{grp}{n_in}-上移", "長圖",
                                                 (xt, yc, f_sw, 0.0), sh_prev, self.TRANS_MM))
                sw = (xt, yc, f_sw, 0.0)
                hard = f"無（同框硬切：畫面完全相同，只把長圖換成{grp}）"
                if same(pg["frame"], sw):
                    pg["name"] = f"長圖轉{grp}{n_in}＝{pg['name']}"
                    pg["trans"] = hard
                else:
                    out.append(self._bridge_page(f"長圖轉{grp}{n_in}", grp, sw, pg["shot"], hard))
                    pg["trans"] = self.TRANS_MM
                state = (grp, sw, origin)
            elif prev and prev["group"] != "長圖" and pg["group"] == "長圖" and state:
                grp, sw, origin = state
                n_out += 1
                sh_prev = prev["shot"]
                if not same(prev["frame"], sw):
                    out.append(self._bridge_page(f"{grp}轉長圖{n_out}-歸位", grp, sw, sh_prev,
                                                 self.TRANS_MM + "；盤轉回 0°"))
                out.append(self._bridge_page(f"{grp}轉長圖{n_out}", "長圖", sw, sh_prev,
                                             f"無（同框硬切：畫面完全相同，只把{grp}換回長圖）"))
                down = self.TRANS_MM + f"；＝長圖轉{grp}的倒放"
                if same(pg["frame"], origin):
                    pg["name"] = f"{grp}轉長圖{n_out}-下移＝{pg['name']}"
                    pg["trans"] = down
                else:
                    out.append(self._bridge_page(f"{grp}轉長圖{n_out}-下移", "長圖", origin,
                                                 sh_prev, down))
                    pg["trans"] = self.TRANS_MM
                state = None
            out.append(pg)
        return out

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
            # Canva 匯入 SVG 時把寬高取整數（360×465.72 → 360×466），內容等比置中；
            # 所以 H 用 Canva 的比例，Y 由「內容中心」反推，填進去才不會上下差 10–20 px
            W = (x1 - x0) * u
            H = W * round(y1 - y0) / round(x1 - x0)
            X = PW / 2 - (cx - x0) * u
            Y = PH / 2 - (y1 - cy) * u + ((y1 - y0) * u - H) / 2
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
        if pg.get("transition"):
            return []
        if pg.get("labels_from") and not pg.get("shot_next"):
            return Pages.label_names(pg["labels_from"])
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
                "概念圖": "＋".join(pg.get("overlay_files", [])), "字卡": sh.get("card", ""),
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
        # 給 Claude 直接操作 Canva 用（Canva MCP edit-design：left/top/width/height/rotation）
        api = [{"page": r["頁"], "title": r["頁名"], "group": r["圖層組"],
                "left": round(pl["X"], 2), "top": round(pl["Y"], 2),
                "width": round(pl["W"], 2), "height": round(pl["H"], 2),
                "rotation": round(pl["rot"], 2), "layers": r["留下的圖層"].split("、"),
                "notes": r["旁白（本頁起播）"], "trans": r["與上一頁"],
                **self._overlay_api(pg)}
               for r, pl, pg in zip(rows, (self.placement(pg) for pg in pages), pages)]
        json.dump(api, open(os.path.join(self.dir, f"{self.ep}_Canva頁面參數.json"), "w",
                            encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"  ✓ {self.ep}_Canva頁面參數.json")
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

    def _overlay_api(self, pg):
        if not pg.get("hold"):
            return {}
        ov, panel = [], None
        grp = self.overlay_files(pg["shot"])
        for fn in pg.get("overlay_files", []):
            box, panel = self.overlay_box(fn, grp)
            ov.append(dict(file=fn, **{k: round(v, 2) for k, v in box.items()}))
        return {"hold": True, "overlay": ov, "panel": panel if ov else None}

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
                         "英文翻譯": c.get("英文", ""), "中文": c["中譯"],
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
             "- 長圖→北盤：長圖先回中心、沿走廊往上到北盤心；「長圖轉北盤」＝前一頁複製一份、"
             "只把長圖圖層組換成北盤圖層組（畫面完全重疊，觀眾看不出換檔）。",
             "- 北盤→長圖＝倒放：「-歸位」盤轉回 0° 回到換組那一格 →「北盤轉長圖」同框換回長圖 →"
             "「-下移」往下回到出發點，再繼續長圖上的鏡頭。",
             "- 概念圖＝「定格頁」：同一鏡可以不只開始／結束兩頁，中間插畫面完全不動的頁，"
             "一頁多疊一層概念圖（半透明黑底圓角框＋透明 PNG）；最後「-概念圖收」把概念圖淡出。",
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
        # 概念圖（定格頁）
        for fn in pg.get("overlay_files", []):
            box, panel = self.overlay_box(fn, self.overlay_files(pg["shot"]))
            if panel:
                from matplotlib.patches import FancyBboxPatch
                ax.add_patch(FancyBboxPatch((panel["left"], panel["top"]), panel["width"],
                                            panel["height"],
                                            boxstyle=f"round,pad=0,rounding_size={panel['radius']}",
                                            fc=panel["color"], ec="none", alpha=panel["opacity"],
                                            zorder=9.2))
            path = os.path.join(os.path.dirname(self.dir), "_概念圖", fn)
            if os.path.exists(path):
                ax.imshow(plt.imread(path), extent=(box["left"], box["left"] + box["width"],
                                                    box["top"] + box["height"], box["top"]),
                          zorder=9.5, interpolation="antialiased")
        ax.set_xlim(0, PW); ax.set_ylim(PH, 0)
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
        if vo and ((pg["t"] == 0.0 and not pg.get("hold")) or pg.get("shot_next")):
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
