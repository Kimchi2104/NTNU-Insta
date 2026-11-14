# -*- coding: utf-8 -*-
"""A-33 毛利 Matariki：星星升起就是新年｜大畫布 v4.6（全片長圖帶狀；不用盤，盤組照規定生成）

論點：天上的時鐘決定一個國家的假期——昴宿（Matariki）在南半球冬天的黎明重現＝新年；
  2022 起紐西蘭放 Matariki 國定假日，日期看星星＋月亮（Pipiri 月的 Tangaroa 期）；
  九顆星（Mātāmua 據 1933 年手稿）各管一個領域，最暗的兩顆＝願望與思念；西岸部族看 Puanga（參宿七）。
來源：Stellarium maori（新舊兩版 index.json；九星 HIP 對應兩版相同）；western（定位連線）；
  逐字稿 04_腳本庫/A-33-毛利Matariki星星升起就是新年-逐字稿-v1.md（星名表、星空對時）。
  太陽位置 PyEphem 4.2.1 自算（地心、轉 J2000）。

參數（依本集逐字稿重新評估，不照抄範例）
  lst = 40 → 長圖切口 x＝±180 在 RA 220（牧夫南方／豺狼一帶，本集完全不用）。
             x：昴宿 −16.2…−17.3（Alcyone −16.87）、畢宿五 −29、參宿七 Puanga −38.6、參宿四 −48.8、
             太陽 5/22 −19.7、6/8 −37、6/25 −54；心宿二 Rehua +152.6、天蠍尾 +135…+137、人馬銀河 +115…+135。
             X-01 用 lst 57 讓昴宿在 x≈0，但切口會落在 RA 237（天蠍頭 δ Sco 240.1）：13 鏡的天蠍會被切斷，所以不能照抄。
  D_s = 60、D_r = 64 → 決定因素是 13–14 鏡：心宿二 dec −26.4、天蠍尾 −43、14 鏡夏季銀河大框 fov 44（cy −22）
             |cy|+fov·8/9 ＝ 59.1 ≤ 60。北邊沒有東西超過 +45（01 鏡 fov 40 上緣 +43.6）。
  D_fill = 15 → k＝2.2037、R_fill＝165.276（盤寬 ÷ 畫布寬＝0.918200，與 H-七夕、A-03、A-32 相同）；
             |x_t|＋R_fill ≤ 180 ✓。x_tN = x_tS = 0（Canva 可水平置中）。本集沒有 T／R 鏡頭，盤組只是照規定備著。
  maglim = 5.8 → 逐字稿規定：預設 5.5–5.6 會把 Pōhutukawa（Asterope 5.76）濾掉；九顆用同一套星點畫法
             （mains ×1.5＋光暈），不用標記層補畫，最暗的兩顆自然看得出來比較小。
  特寫 fov：07 鏡 3.0（無標籤、只看九顆白點）；08–11 鏡 4.2（逐字稿寫 2.6，改 4.2：毛利星名最長
             「Waipuna-ā-rangi」「Hiwa-i-te-rangi」15 個字元，40 px 時寬約 330 px；fov 2.6 時星團本身就佔 460 px，
             兩側放不下名字。4.2 時星團 283 px、四周留得出名字＋引線）。

自訂圖層
  深空天體（M45 反射星雲淡光＋5.8–8.5 等暗星；X-01 同款）、太陽（5/22、6/8、6/25 三個位置＋6 月的路徑，03–06 鏡）、
  引線-七顆／九顆／六顆／三顆（特寫時星名離星有段距離，用 1.5–3 px 細線連回去）、
  圈-六顆、圈-最暗兩顆（特寫用細圈；引擎的 ring 半徑下限 1.1 單位，fov 4 會整團圈住，不能用）。

鏡頭路線（14 鏡、226 秒；與逐字稿 v1 相同）
  01 Z 獵戶—金牛 fov 40 → 昴宿 fov 12（Matariki 標籤＋開場字卡）→ 02 定格疊 C-A33-01 假日
  → 03 Z 昴宿＋太陽 5/22（fov 14）→ 拉遠 fov 48 看太陽 6/8、6/25 往東移開 → 04、05、06 定格疊 C-A33-02／03／04
  → 07 Z 推近 fov 3 → 08 Z fov 4.2 七顆 → 九顆 → 09 六顆領域 → 10 三顆＋最暗兩顆＋圖卡 C-A33-05
  → 11 定格疊 C-A33-06 hautapu → 12 S 拉遠往東南到 獵戶（Matariki 與 Puanga 同框）＋C-A33-08 北島示意
  →【硬切】13 Z 天蠍 心宿二 Rehua＋圖卡 C-A33-07 → 14 S 滑到夏季銀河＋端卡。

check_shots 判斷：全部 Z／S，無 ⚠。12 鏡 fov 4.2 → 34 一次拉遠（Canva 單段 2.5 秒）是刻意的「從星團退回整片冬季星空」。
執行：/usr/bin/python3 make_a33_v4.py
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-33"
OUT = os.path.join(BASE, "05_素材/A-33_毛利Matariki/_v4大畫布")
LST0 = 40.0
D_S, D_R, D_FILL = 60.0, 64.0, 15.0
MAGLIM = 5.8


# ══════════════════════════════════════════════════════════════════
# 〇、太陽位置（地心、J2000）
# ══════════════════════════════════════════════════════════════════
def sun_j2000(when):
    import ephem
    s = ephem.Sun(); s.compute(ephem.Date(when))
    q = ephem.Equatorial(ephem.Equatorial(s.g_ra, s.g_dec, epoch=ephem.Date(when)), epoch=ephem.J2000)
    return math.degrees(q.ra), math.degrees(q.dec)


SUN_DAYS = [("5/22", "2027/5/22 00:00"), ("6/8", "2027/6/8 00:00"), ("6/25", "2027/6/25 00:00")]   # UT 0h≈台北 8:00
SUN = {k: sun_j2000(w) for k, w in SUN_DAYS}
SUN_PATH = [sun_j2000(f"2027/5/{d} 00:00") for d in range(18, 32)] + \
           [sun_j2000(f"2027/6/{d} 00:00") for d in range(1, 29)]


def sep(a, b):
    r1, d1, r2, d2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
ALCYONE, ATLAS, PLEIONE, MAIA, TAYGETA = 17702, 17847, 17851, 17573, 17531
ELECTRA, MEROPE, CELAENO, ASTEROPE = 17499, 17608, 17489, 17579
RIGEL, BETELGEUSE, ALDEBARAN, ANTARES = 24436, 27989, 21421, 80763
MINTAKA, ALNILAM, ALNITAK = 25930, 26311, 26727
NINE = [ALCYONE, ATLAS, PLEIONE, MAIA, TAYGETA, ELECTRA, MEROPE, CELAENO, ASTEROPE]
SEVEN = [ALCYONE, ATLAS, PLEIONE, MAIA, TAYGETA, ELECTRA, MEROPE]
SIX = [PLEIONE, ATLAS, MAIA, TAYGETA, ELECTRA, MEROPE]
THREE = [ALCYONE, CELAENO, ASTEROPE]
DIM2 = [CELAENO, ASTEROPE]
MAINS = NINE + [RIGEL, ALDEBARAN, ANTARES]
M45 = (56.75, 24.12)

# 毛利名（Mātāmua／Te Papa 的長音）、中文領域、星圖上的顏色
MAO = {
    ALCYONE: ("Matariki", "母親・健康", "amber"),
    PLEIONE: ("Tupuānuku", "土裡的食物", "green"),
    ATLAS: ("Tupuārangi", "樹上的果實和鳥", "green"),
    MAIA: ("Waitī", "淡水", "blue"),
    TAYGETA: ("Waitā", "大海", "blue"),
    ELECTRA: ("Waipuna-ā-rangi", "雨", "blue"),
    MEROPE: ("Ururangi", "風", "white"),
    CELAENO: ("Hiwa-i-te-rangi", "新年的願望", "purple"),
    ASTEROPE: ("Pōhutukawa", "離開的人", "purple"),
}


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


def ra_of(x):
    return (LST0 - x) % 360.0


# ══════════════════════════════════════════════════════════════════
# 二、連線（western 定位；不畫毛利連線：本集講的都是單星與星團）
# ══════════════════════════════════════════════════════════════════
SC_OLD = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")


def sc_lines(culture):
    d = json.load(open(os.path.join(SC_OLD, culture, "index.json"), encoding="utf-8"))
    return {c["id"].split()[-1]: [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
            for c in d["constellations"]}


W = sc_lines("western")
_PLE = set(NINE)
LG_LOC = [([sg for sg in W["Ori"]], "white", 0.6),
          ([sg for sg in W["Tau"] if not (set(sg) & _PLE)], "white", 0.6)]
LG_SCO = [([sg for sg in W["Sco"]], "white", 0.6)]
LG_ALL = LG_LOC + LG_SCO
LINE_SETS = [(LG_LOC, "連線-定位（獵戶、金牛）"), (LG_SCO, "連線-天蠍")]


# ══════════════════════════════════════════════════════════════════
# 三、旁白字數（逐字稿 v1 的算法：中文字＋外文音節；毛利語每個母音算一音節，長音符號不另計）
# ══════════════════════════════════════════════════════════════════
def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏ]+|\d+|[㐀-鿿〇]", t):
        if re.match(r"[㐀-鿿〇]", w):
            n += 1
        elif w.isdigit():
            n += len(w)
        else:
            n += max(1, len(re.findall(r"[aeiouyāēīōū]", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 四、自訂圖層
# ══════════════════════════════════════════════════════════════════
def ellipse(ra0, dec0, a, b, pa, n=48):
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        u, v = a * math.cos(t), b * math.sin(t)
        th = math.radians(pa)
        x = u * math.sin(th) + v * math.cos(th)
        y = u * math.cos(th) - v * math.sin(th)
        pts.append(((ra0 + x / max(0.05, math.cos(math.radians(dec0)))) % 360, dec0 + y))
    return pts


def cluster_stars(S, ra0, dec0, rad, vmax):
    c = math.cos(math.radians(dec0))
    return [(ra, dec, v) for h, (ra, dec, v) in S.items()
            if v <= vmax and abs(dec - dec0) <= rad and math.hypot((ra - ra0) * c, dec - dec0) <= rad]


def custom_layers(m, S, leaders):
    mw, amb = COLORS["mw"], COLORS["amber"]

    def deep(s, pos, runs):
        for (dra, ddec, a, op) in ((0.0, 0.0, 1.1, 0.06), (0.0, 0.0, 0.7, 0.08),
                                   (-0.12, -0.12, 0.32, 0.10), (0.15, 0.25, 0.25, 0.08)):
            s.poly_fill(runs(ellipse(M45[0] + dra, M45[1] + ddec, a, a * 0.8, 20.0)), fill=mw, opacity=op)
        dots = []
        for ra, dec, v in cluster_stars(S, *M45, 1.3, 8.5):
            if v <= m.maglim:
                continue
            for p in pos(ra, dec):
                dots.append((p[0], p[1], 0.012 + 0.006 * (8.5 - v)))
        if dots:
            s.dots(dots, fill="#FFFFFF", opacity=0.8)

    def sun(s, pos, runs):
        s.polylines(runs(SUN_PATH), stroke=amb, w=0.10, opacity=0.55, dash="0.6 0.5")
        for k, (ra, dec) in SUN.items():
            for p in pos(ra, dec):
                s.circle(p[0], p[1], 2.2, fill=amb, opacity=0.12)
                s.circle(p[0], p[1], 1.3, fill=amb, opacity=0.22)
                s.circle(p[0], p[1], 0.75, fill=amb, opacity=0.95)

    def leader_fn(pairs):
        def f(s, pos, runs):
            for a, b in pairs:
                s.polylines(runs([a, b]), stroke="#FFFFFF", w=0.010, opacity=0.65)
        return f

    def ring_fn(hips):
        def f(s, pos, runs):
            for h in hips:
                r = m.sz_star(S[h][2]) * 1.5 + 0.05
                for p in pos(*S[h][:2]):
                    s.circle(p[0], p[1], r, stroke=COLORS["amber"], w=0.012, opacity=0.95)
        return f

    out = [("深空天體", deep), ("太陽", sun)]
    for name, pairs in leaders:
        out.append((f"引線-{name}", leader_fn(pairs)))
    out += [("圈-六顆", ring_fn(SIX)), ("圈-最暗兩顆", ring_fn(DIM2))]
    return out


def write_custom(m, layers, discs=False):
    for name, fn in layers:
        if not discs:
            s = m._new()
            fn(s, lambda ra, dec: m.pos_all(ra, dec), m.runs_all)
            m._write(s, name)
        else:
            for north in (True, False):
                s = m._new_disc()
                fn(s, lambda ra, dec, n=north: m.pos_disc(ra, dec, n),
                   lambda pts, n=north: m._runs_disc(pts, n))
                m._write_disc(s, north, name)


# ══════════════════════════════════════════════════════════════════
# 五、特寫標籤版面（fov 4.2；標籤中心 → 引線）
# ══════════════════════════════════════════════════════════════════
PXC = -16.75                     # 九顆的中心 x
PYC = 24.25
# 每顆星的名字往哪個方向放（從星團中心量的角度；東在左，0°＝右、90°＝上）。
# 依星在星團裡的方位角排序，引線才不會交叉；長名字（15 字元）放上下、右側，左側只放短名
ANG = {ATLAS: -168, ALCYONE: -128, MEROPE: -88, ELECTRA: -42, CELAENO: 2, TAYGETA: 30,
       ASTEROPE: 62, MAIA: 112, PLEIONE: 158}
FOV_8A, FOV_8B, FOV_9, FOV_10, FOV_11 = 4.8, 5.0, 5.2, 5.4, 7.0
SZ1, SZ2 = 0.106, 0.096          # 名字／領域字級（畫布單位）：fov 4.8–5.4 → Canva 40–36 px、37–33→夾到 36


def layout(m, S):
    """沿每顆星的方向射線往外找第一個不壓到任何星點、不壓到已放標籤的位置（名字＋領域兩行一起保留）。
    回傳 {hip: (名字中心 x, y, 領域在上(+1)/下(-1))}"""
    em1, em2 = SZ1 * m.fu, SZ2 * m.fu
    stars = [(x_of(S[h][0]), S[h][1], m.sz_star(S[h][2]) * (1.5 * 2.0 if h in MAINS else 1.0))      # 主角星連光暈一起避開
             for h in S if S[h][2] <= m.maglim and abs(x_of(S[h][0]) - PXC) < 4 and abs(S[h][1] - PYC) < 4]
    dom_w = {h: max(MC.label_box(MAO[h][1] + "・0.0 等", SZ2, m.fu)[0],
                    MC.label_box(MAO[h][1], SZ2, m.fu)[0]) for h in NINE}
    placed, out = [], {}

    def boxes_for(h, x, y, side):
        w1, h1 = MC.label_box(MAO[h][0], SZ1, m.fu)
        gap = (em1 + em2) * 0.62
        return [(x - w1 / 2, y - h1 / 2, x + w1 / 2, y + h1 / 2),
                (x - dom_w[h] / 2, y + side * gap - em2 * 0.62, x + dom_w[h] / 2, y + side * gap + em2 * 0.62)]

    def hit(bx, pad=0.05):
        for (x0, y0, x1, y1) in bx:
            for sx, sy, r in stars:
                if x0 - r - pad < sx < x1 + r + pad and y0 - r - pad < sy < y1 + r + pad:
                    return True
            for (a0, b0, a1, b1) in placed:
                if x0 < a1 + 0.05 and a0 < x1 + 0.05 and y0 < b1 + 0.03 and b0 < y1 + 0.03:
                    return True
        return False

    for h in sorted(NINE, key=lambda h: ANG[h]):
        ph = math.radians(ANG[h])
        ux, uy = math.cos(ph), math.sin(ph)
        side = 1 if uy > 0.35 else -1
        sx, sy = x_of(S[h][0]), S[h][1]
        t = 0.25
        while True:
            x, y = sx + ux * t, sy + uy * t
            bx = boxes_for(h, x, y, side)
            if not hit(bx):
                break
            t += 0.02
        placed += bx
        out[h] = (x, y, side, t)
    return out


def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=D_S, D_r=D_R, D_fill=D_FILL,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None, maglim=MAGLIM, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")

    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        return {"hip": a[0]}

    def item(a, text, color, size, dx, dy, key):
        return dict(anchor(a), text=text, color=color, size=round(size, 4), dx=round(dx, 3),
                    dy=round(dy, 3), key=key)

    def lab(a, orig, zh, col, fov, dx=0.0, dy=0.0, key=None, k1=0.030, k2=0.025):
        s1, s2, gap = fov * k1, fov * k2, fov * 0.048
        key = key or orig
        out = [item(a, orig, col, s1, dx, dy + gap / 2, key)]
        if zh:
            out.append(item(a, zh, "white", s2, dx, dy - gap / 2, key + "-zh"))
        return out

    # ── 特寫：名字層與領域層分開（領域一律放在名字「離星較遠」的那一側，引線只接名字，
    #    所以 08b→09→10 名字與引線都不動，只多疊一層領域）──
    LAY = layout(m, S)
    em1, em2 = SZ1 * m.fu, SZ2 * m.fu
    print("\n── 特寫標籤（射線距離）──")
    for h in NINE:
        x, y, side, t = LAY[h]
        print(f"  {MAO[h][0]:16s} 角 {ANG[h]:+4d}°  距星 {t:.2f}  名字中心 ({x:.2f}, {y:.2f})  領域在{'上' if side > 0 else '下'}")

    def nm(h):
        x, y, side, _ = LAY[h]
        return [item([h], MAO[h][0], MAO[h][2], SZ1, x - x_of(S[h][0]), y - S[h][1], f"mao-{h}")]

    def dom(h, extra=None):
        x, y, side, _ = LAY[h]
        z = MAO[h][1] if extra is None else f"{MAO[h][1]}・{extra}"
        return [item([h], z, "white", SZ2, x - x_of(S[h][0]), y + side * (em1 + em2) * 0.62 - S[h][1], f"dom-{h}")]

    def leader(h):
        """星點邊緣 → 名字框邊緣"""
        x, y, side, _ = LAY[h]
        sx, sy = x_of(S[h][0]), S[h][1]
        w, hh = MC.label_box(MAO[h][0], SZ1, m.fu)
        dx, dy = x - sx, y - sy
        d = math.hypot(dx, dy)
        ux, uy = dx / d, dy / d
        r0 = m.sz_star(S[h][2]) * 1.5 + 0.05
        tx = (w / 2 + 0.04) / abs(ux) if abs(ux) > 1e-6 else 1e9
        ty = (hh / 2 + 0.02) / abs(uy) if abs(uy) > 1e-6 else 1e9
        t1 = d - min(tx, ty)
        if t1 <= r0 + 0.03:
            return None
        a, b = (sx + ux * r0, sy + uy * r0), (sx + ux * t1, sy + uy * t1)
        return ((ra_of(a[0]), a[1]), (ra_of(b[0]), b[1]))

    VMAG = {h: f"{S[h][2]:.1f} 等" for h in NINE}
    L_SEVEN = [it for h in SEVEN for it in nm(h)]
    L_NINE = [it for h in NINE for it in nm(h)]
    L_SIX = [it for h in SIX for it in dom(h)]
    L_THREE = [it for h in THREE for it in dom(h, VMAG[h])]
    LEADERS = [("七顆", [p for h in SEVEN if (p := leader(h))]),
               ("九顆", [p for h in NINE if (p := leader(h))])]

    # ── 中景 ──
    L01 = lab(M45, "Matariki", "昴宿", "amber", 12.0, 0.0, 1.55, key="Matariki-01")
    F03 = 48.0
    L03 = (lab(M45, "Matariki", "昴宿", "amber", F03, 0.0, 4.2, key="Matariki-03")
           + [it for k in SUN for it in lab(SUN[k], f"{k} 太陽", "", "amber", F03, 0.0, -3.6, key=f"sun-{k}")])
    L03a = (lab(M45, "Matariki", "昴宿", "amber", 14.0, -0.6, 1.55, key="Matariki-03a")
            + lab(SUN["5/22"], "5/22 太陽", "", "amber", 14.0, 0.0, -1.5, key="sun-5/22-a"))
    F12 = 34.0
    L12 = (lab([RIGEL], "Puanga", "參宿七", "blue", F12, 0.0, -2.6, key="Puanga")
           + lab(M45, "Matariki", "昴宿", "amber", F12, 0.0, 2.6, key="Matariki-12"))
    F13 = 30.0
    L13 = lab([ANTARES], "Rehua", "心宿二", "red", F13, -4.6, 0.0, key="Rehua")

    label_sets = [(L01, "Matariki"), (L03a, "太陽近"), (L03, "太陽遠"), (L_SEVEN, "七顆"), (L_NINE, "九顆"),
                  (L_SIX, "六顆領域"), (L_THREE, "三顆領域"), (L12, "Puanga"), (L13, "Rehua")]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    custom = custom_layers(m, S, LEADERS)
    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_ALL)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    write_custom(m, custom)
    MARKS = [(MAINS, "主角星白點", "dot")]
    for hips, name, style in MARKS:
        m.L_marks(hips, name, style)
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS, marks=MARKS)
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, custom, discs=True)

    LINES_KEY = {"L4": "星座連線", "定位": "連線-定位（獵戶、金牛）", "天蠍": "連線-天蠍",
                 "深空": "深空天體", "太陽": "太陽", "圈六": "圈-六顆", "圈暗": "圈-最暗兩顆"}
    for n, _ in LEADERS:
        LINES_KEY[f"引{n}"] = f"引線-{n}"
    LINE_GROUPS = {"L4": LG_ALL, "定位": LG_LOC, "天蠍": LG_SCO}

    # ════════════════════ 構圖 ════════════════════
    def fr(x, y, fov):
        return (round(x, 2), round(y, 2), round(fov, 1), 0.0)

    F01a = fr(-30.0, 8.0, 40.0)                       # 獵戶—金牛
    F01b = fr(PXC, 23.2, 12.0)                        # 昴宿與四周
    F03a = fr(-18.4, 22.6, 14.0)                      # 昴宿＋5/22 的太陽
    F03b = fr(-35.0, 14.0, F03)                       # 拉遠：5/22 → 6/8 → 6/25 太陽往東移開
    F07 = fr(PXC, PYC, 3.0)                           # 特寫（無標籤）
    F08a = fr(PXC, PYC, FOV_8A)                       # 特寫＋標籤：每鏡迄格都略拉遠一點（4.8→5.4），
    F08b = fr(PXC, PYC, FOV_8B)                       # 讓每一鏡都有自己的頁（同框會被 gen_canva_pages 併成一頁，
    F09 = fr(PXC, PYC, FOV_9)                         # 標籤就換不了層）
    F10 = fr(PXC, PYC, FOV_10)
    F11 = fr(PXC, PYC - 0.4, FOV_11)
    F12 = fr(-30.0, 4.0, F12)                         # 獵戶＋金牛＋昴宿（Matariki 與 Puanga 同框）
    F13 = fr(150.0, -28.0, F13)                       # 天蠍
    F14 = fr(128.0, -20.0, 44.0)                      # 夏季銀河（天蠍—人馬）
    print("\n── 構圖 ──")
    for k, v in dict(F01a=F01a, F01b=F01b, F03a=F03a, F03b=F03b, F07=F07, F08a=F08a, F08b=F08b, F09=F09, F10=F10, F11=F11, F12=F12,
                     F13=F13, F14=F14).items():
        print(f"  {k} {v}")

    ls = lambda *n: list(n)
    PLE = ["深空"]
    shots = [
        dict(code="01", kind="Z", sec=13, north=True, frames=[F01a, F01b], layers=["定位"] + PLE,
             labels=ls("Matariki"), labels_start=[],
             vo="上週，我們數了課本沒教的星群。今天，紐西蘭放 Matariki 假：同一片星空，毛利人看見——新的一年。",
             card="同一片星空，／毛利人看見——新的一年。",
             note="長圖 fov 40→12：從獵戶—金牛推近昴宿；迄格開 Matariki／昴宿 標籤；開場字卡兩張（「／」處換）"),
        dict(code="02", kind="Z", sec=18, north=True, frames=[F01b], layers=["定位"] + PLE, labels=ls("Matariki"),
             overlay="C-A33-01_Matariki假日", overlay_layers=["年份層", "今年層"],
             vo="二〇二二年起，紐西蘭多了一個國定假日，叫 Matariki。政府說，這是第一個承認毛利世界觀的國定假日。"
                "它每年日期都不一樣：二〇二七年，是六月二十五號，星期五。",
             card="今年假日：6/25",
             note="畫面停在昴宿；定格疊 C-A33-01 兩層：年份層（2022/6/24 第一次、Te Ao Māori 中譯）→ 今年層"
                  "（2026/7/10 → 2027/6/25 五）；慶典照片美宣另尋授權圖"),
        dict(code="03", kind="Z", sec=13, north=True, frames=[F03a, F03b], layers=["定位", "太陽"] + PLE,
             labels=ls("太陽遠"), labels_start=ls("太陽近"),
             vo="日期由天上決定。Matariki 就是昴宿：每年四、五月，它在黃昏沉進西方，躲進太陽的光裡；"
                "六月，再從冬天的黎明裡冒出來。",
             card="Matariki＝昴宿",
             note=f"長圖 昴宿＋太陽（太陽圖示放大示意）：起格 fov 14 看 5/22 太陽離昴宿最近"
                  f"（{sep(SUN['5/22'], S[ALCYONE][:2]):.1f}°）→ 迄格拉遠 fov {F03:g}：6/8、6/25 太陽往東（左）移開，"
                  "昴宿留在右上；太陽層的虛線＝5/18–6/28 太陽走的路"),
        dict(code="04", kind="Z", sec=18, north=True, frames=[F03b], layers=["定位", "太陽"] + PLE, labels=ls("太陽遠"),
             overlay="C-A33-02_怎麼挑日子", overlay_layers=["月曆層", "放假層"],
             vo="假日還要對上官方採用的毛利月曆：在昴宿重現的 Pipiri 月，月亮走到叫 Tangaroa 的那幾晚，"
                "大約下弦月前後，再挑最近的星期五。今年的 Tangaroa，是六月二十七到三十號。",
             card="星星＋月亮＝放假日",
             note="畫面不動；疊 C-A33-02 兩層：月曆層（Pipiri 月 6/5 新月 → 6/19 滿月 → 6/27 下弦、Tangaroa 6/27–30）"
                  "→ 放假層（6/25 五圈起、「6/27 是星期日」）"),
        dict(code="05", kind="Z", sec=15, north=True, frames=[F03b], layers=["定位", "太陽"] + PLE, labels=ls("太陽遠"),
             overlay="C-A33-03_兩個季節",
             vo="為什麼新年在六月？南半球的六月是冬天：冬至那天，威靈頓的白天只有九個多小時。"
                "最冷、最暗的時候，昴宿回來了——舊的一年結束，新的一年開始。",
             card="南半球的冬至",
             note="畫面不動；疊 C-A33-03「同一天、兩個季節」：6/21 台北白天 13.7 小時 vs 威靈頓 9.2 小時"),
        dict(code="06", kind="Z", sec=16, north=True, frames=[F03b], layers=["定位", "太陽"] + PLE, labels=ls("太陽遠"),
             overlay="C-A33-04_黎明重現", overlay_layers=["地平線層", "三地層"],
             vo="台灣其實比紐西蘭早：同樣在天亮前，昴宿六月八號前後就在台灣東北東的地平線露臉，"
                "紐西蘭要再晚四五天；到了六月下旬，兩邊都好找了。",
             card="台灣早四五天",
             note="畫面不動；疊 C-A33-04 兩層：地平線層（東方地平線、太陽在地平下 12° 的那一刻）→ 三地層"
                  "（台北 6/8、奧克蘭 6/12、威靈頓 6/13 的昴宿高度與方位；10° 以上才好找的日期）"),
        dict(code="07", kind="Z", sec=13, north=True, frames=[F03b, F07], layers=["定位", "太陽"] + PLE,
             labels=[], labels_start=ls("太陽遠"),
             vo="看到還不夠，還要看清楚。天亮前，懂星的人仔細看這群星：清楚又明亮，來年溫暖豐收；"
                "朦朧、擠成一團，就要準備過一個冷冬。",
             card="看清楚＝看年冬",
             note="長圖從 fov 48 一路推近到 fov 3：昴宿特寫，九顆主角星白點＋光暈（照 V 星等畫大小）；迄格不開標籤"),
        dict(code="08", kind="Z", sec=3, north=True, frames=[F07, F08a], layers=PLE + ["引七顆"],
             labels=ls("七顆"), labels_start=[],
             vo="很多說法只數七顆；",
             card="七顆之外：九顆星",
             note=f"fov 3→{FOV_8A:g} 輕拉（讓出放名字的位置）：迄格開七顆（Matariki＋六顆）＋引線-七顆。"
                  "逐字稿 08 鏡在「；」拆成 08／08b（17 秒＝3＋14）：引線層整鏡固定，七顆→九顆要換引線層，只能分兩鏡"),
        dict(code="08b", kind="Z", sec=14, north=True, frames=[F08a, F08b], layers=PLE + ["引九顆"],
             labels=ls("九顆"), labels_start=ls("七顆"),
             vo="近年最受注目的，是九顆星的說法。毛利天文學者 Rangi Mātāmua 整理祖先在"
                "一九三三年完成的手稿，介紹這九顆星和它們各自照看的領域。",
             note=f"fov {FOV_8A:g}→{FOV_8B:g}：淡入 Pōhutukawa、Hiwa-i-te-rangi（九顆層＋引線-九顆）；"
                  "名字照 Mātāmua／Te Papa 的長音；不放 Mātāmua 書封（版權）"),
        dict(code="09", kind="Z", sec=18, north=True, frames=[F08b, F09], layers=PLE + ["引九顆", "圈六"],
             labels=ls("九顆", "六顆領域"), labels_start=ls("九顆"),
             vo="Tupuānuku 管土裡長的食物，Tupuārangi 管樹上的果實和鳥；Waitī 管淡水和河裡的食物，"
                "Waitā 管大海和海裡的食物；Waipuna-ā-rangi 管雨，Ururangi 管風。",
             card="土・樹・淡水・海・雨・風",
             note=f"fov {FOV_8B:g}→{FOV_9:g}；名字不動，多疊六顆的中文領域（在名字離星較遠的一側），細圈圈出這六顆；"
                  "名字顏色分組：綠＝土與樹、藍＝水與雨、白＝風。美宣可照唸的順序逐顆淡入領域字。"
                  "逐字稿原寫「小圖示」：不另畫（星團特寫裡塞不下、容易像貼圖），改用顏色分組"),
        dict(code="10", kind="Z", sec=18, north=True, frames=[F09, F10], layers=PLE + ["引九顆", "圈暗"],
             labels=ls("九顆", "三顆領域"), labels_start=ls("九顆", "六顆領域"),
             overlay="C-A33-05_Matariki九星小辭典",
             vo="Matariki 是母親，照看人們的健康；Hiwa-i-te-rangi 收下新年的願望；Pōhutukawa 代表過去一年離開的人。"
                "而後面這兩顆，正好是九顆裡最暗的，要在很黑的地方才看得到。",
             card="健康・願望・思念／最暗的兩顆",
             note=f"fov {FOV_9:g}→{FOV_10:g}；領域層換成三顆（Matariki、Hiwa-i-te-rangi、Pōhutukawa＋星等 2.9／5.5／5.8），"
                  "最暗兩顆細圈；唸到「最暗的」換第二張字卡；結束疊 9:16 圖卡 C-A33-05「Matariki 九星小辭典」（可存圖）"),
        dict(code="11", kind="Z", sec=18, north=True, frames=[F11], layers=PLE, labels=[],
             overlay="C-A33-06_hautapu", overlay_layers=["爐火層", "熱氣層", "名字層"],
             vo="天亮前的這場儀式叫 hautapu：生火煮食物，讓熱氣升上天，獻給這群星；念出離開的人的名字，"
                "也說出新年的願望。有點像我們過年：送走舊的一年，想念親人，許下新願。",
             card="天亮前的 hautapu",
             note=f"從 10 鏡輕拉到 fov {FOV_11:g}、星團略偏上（不開標籤）；疊 C-A33-06 三層：爐火層 → 熱氣層（熱氣升向昴宿）"
                  "→ 名字層（念名字、許願、和過年對照）；不畫人物、不仿既有插畫；儀式照片美宣另尋授權"),
        dict(code="12", kind="S", sec=18, north=True, frames=[F11, F12], layers=["定位"] + PLE,
             labels=ls("Puanga"), labels_start=[],
             overlay="C-A33-08_北島示意",
             vo="但不是每個部族都看昴宿。北島西岸的 Taranaki、Whanganui 等部族，新年看的是 Puanga——參宿七。"
                "有的地方被山擋住，看不清昴宿；也有部族的專家說，Puanga 更能預告西岸的天氣。",
             card="西岸看 Puanga",
             note=f"從星團拉遠、往左下（東南）滑到獵戶 fov {F12[2]:g}：參宿七 Puanga（藍）與昴宿 Matariki 同框；"
                  "結束疊 C-A33-08 北島示意（自繪：Taranaki、Whanganui、Rangitīkei；南島 Kāi Tahu 叫它 Puaka）"),
        dict(code="13", kind="Z", sec=19, north=True, cut=True, frames=[F13], layers=["天蠍"],
             labels=ls("Rehua"),
             overlay="C-A33-07_這週抬頭看",
             vo="今晚八點，這兩位主角下午就已經西沉，台灣看不到。往南偏東看，紅色的心宿二已經升到半空，"
                "毛利人叫它 Rehua。想看 Matariki，明天清晨三點半到四點，往東北東低空找，跟紐西蘭一起迎新年。",
             card="今晚：心宿二 Rehua／明晨 3:30・東北東",
             note="【硬切】長圖 天蠍 fov 30：心宿二 Rehua（紅）標籤（第一張字卡）；唸到「想看 Matariki」換第二張字卡；"
                  "結束疊 9:16 圖卡 C-A33-07「這週抬頭看」（台北 6/25 20:00 心宿二、6/26 清晨昴宿；可存圖）"),
        dict(code="14", kind="S", sec=12, north=True, frames=[F13, F14], layers=["天蠍"], labels=[],
             labels_start=ls("Rehua"),
             vo="下週五，我們沿著銀河繞地球一圈：有人看見一條河，有人看見一條路，也有人看見一道縫。",
             card="下集見｜銀河環球：一條河、一條路、一道縫",
             note="長圖從天蠍往左滑到 天蠍—人馬 的夏季銀河 fov 44；端卡「下集見｜銀河環球：一條河、一條路、一道縫」"
                  "＋追蹤 CTA（停 2 秒以上）"),
    ]
    print("\n── 旁白字數 ──")
    tot_u = 0
    for sh in shots:
        u = vo_units(sh["vo"]); tot_u += u
        r = u / sh["sec"]
        print(f"  {sh['code']}  {u:3d} 字 / {sh['sec']:2d} 秒 ＝ {r:.2f}{'  ✗ 超過 4.5' if r > 4.5 else ''}")
        sh["vo_units"] = u
    tot_s = sum(s["sec"] for s in shots)
    print(f"  合計 {tot_u} 字 / {tot_s} 秒 ＝ {tot_u/tot_s:.2f} 字/秒")
    m.check_shots(shots)

    rows = []
    for sh in shots:
        for i, (cx, cy, fov, rot) in enumerate(sh["frames"]):
            ew = 360.0 / fov * 1080
            off = (round(-cx / fov * 1080), round(cy / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"], "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": "大畫布圖層組", "元素寬px": round(ew), "位移X px": off[0], "位移Y px": off[1],
                         "旋轉度": round(rot, 1), "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[{k: v for k, v in s.items()} for s in shots])

    print("\n── 天象核對 ──")
    for k, (ra, dec) in SUN.items():
        print(f"  太陽 {k}: RA {ra:.2f} Dec {dec:+.2f}（x {x_of(ra):+.1f}）離昴宿六 {sep((ra, dec), S[ALCYONE][:2]):.1f}°")
    best = min(((sep(sun_j2000(f'2027/5/{d} 00:00'), S[ALCYONE][:2]), d) for d in range(10, 32)))
    print(f"  太陽離昴宿六最近：5/{best[1]}（{best[0]:.1f}°）")
    print("  九顆星等：" + "、".join(f"{MAO[h][0]} {S[h][2]:.2f}" for h in sorted(NINE, key=lambda h: S[h][2])))
    print(f"  k {m.k:.4f}、R_fill {m.R_fill:.3f}、盤寬比 {2 * m.R_fill / 360:.6f}")

    def T(hips, orig, en, zh, col, note):
        return dict(hips=hips, 原文=orig, 拼音="", 英文翻譯=en, 中文=zh, 顏色=col, 來源備註=note)

    western = {ALCYONE: "Alcyone（η Tau）", ATLAS: "Atlas（27 Tau）", PLEIONE: "Pleione（28 Tau）",
               MAIA: "Maia（20 Tau）", TAYGETA: "Taygeta（19 Tau）", ELECTRA: "Electra（17 Tau）",
               MEROPE: "Merope（23 Tau）", CELAENO: "Celaeno（16 Tau）", ASTEROPE: "Asterope（21 Tau）"}
    stl = {ALCYONE: "Matariki", ATLAS: "Tupuarangi", PLEIONE: "Tupuanuku", MAIA: "Waiti", TAYGETA: "Waita",
           ELECTRA: "Waipunarangi", MEROPE: "Ururangi", CELAENO: "Hiwa-i-te-rangi", ASTEROPE: "Pohutukawa"}
    terms = {}
    for h in NINE:
        t, zh, col = MAO[h]
        terms[t] = T([h], t, western[h], zh, col,
                     f"Stellarium maori HIP {h}（寫作 {stl[h]}，無長音）；名字與領域照 Mātāmua 2017／Te Papa；V {S[h][2]:.2f}")
    terms["Puanga"] = T([RIGEL], "Puanga", "Rigel", "參宿七（西岸部族的新年星）", "blue",
                        "Stellarium maori HIP 24436；南島 Kāi Tahu 作 Puaka")
    terms["Rehua"] = T([ANTARES], "Rehua", "Antares", "心宿二", "red", "Stellarium maori HIP 80763")
    for k, zh, note in [("Pipiri", "毛利月曆的月名（約 6–7 月）", "逐字稿星名表"),
                        ("Tangaroa", "月相名（下弦前後的幾晚）", "Te Papa 2027 Tangaroa 期 6/27–30"),
                        ("hautapu", "獻給星群的食物與儀式", "Mātāmua 2017"),
                        ("Te Ao Māori", "毛利世界（觀）", "MBIE／employment.govt.nz")]:
        terms[k] = T([], k, "", zh, "white", note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst0": LST0, "sun": {k: list(v) for k, v in SUN.items()}},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=LG_ALL,
                  labels=[dict(it, pt=6) for it in items], title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_ALL)
    from make_a21_v4 import sb_wall
    LS = {n: it for it, n in label_sets}
    walls = []
    for sh in shots:
        g = [x for k in sh.get("layers", []) for x in LINE_GROUPS.get(k, [])]
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", [])))
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]]))
    sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
            title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    closeup_qa(m, S, [("08 迄・七顆", F08a, L_SEVEN, LEADERS[0][1], []),
                      ("08b 迄・九顆", F08b, L_NINE, LEADERS[1][1], []),
                      ("09 起・六顆領域", F08b, L_NINE + L_SIX, LEADERS[1][1], SIX),
                      ("10 迄・三顆領域", F10, L_NINE + L_THREE, LEADERS[1][1], DIM2),
                      ("03 起・太陽近", F03a, L03a, [], []), ("03 迄・太陽遠", F03b, L03, [], []),
                      ("12 迄・Puanga", F12, L12, [], []), ("13・Rehua", F13, L13, [], [])])
    print("\n完成 →", OUT)


def closeup_qa(m, S, panels):
    """特寫 QA：照 Canva 實際比例畫（星點半徑、字級、Canva 36–96 px 夾限、上下 250 px 安全區）"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Rectangle
    FP = MC.find_serif()
    cw, ch = 2.7, 4.8
    f = plt.figure(figsize=(cw * len(panels), ch + 0.3), dpi=110)
    f.patch.set_facecolor("#0B0F1E")
    for j, (title, (cx, cy, fov, _), labs, leaders, rings) in enumerate(panels):
        ax = f.add_axes([j / len(panels) + 0.002, 0.0, 1 / len(panels) - 0.004, ch / (ch + 0.3)])
        ax.set_facecolor("#05070F")
        hw, hh = fov / 2, fov * 8 / 9
        ax.set_xlim(cx - hw, cx + hw); ax.set_ylim(cy - hh, cy + hh); ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        for h, (ra, dec, v) in S.items():
            if v > m.maglim:
                continue
            x = x_of(ra)
            if abs(x - cx) > hw + 1 or abs(dec - cy) > hh + 1:
                continue
            r = m.sz_star(v) * (1.5 if h in MAINS else 1.0)
            ax.add_patch(Circle((x, dec), r, color="white", lw=0, zorder=3))
            if h in MAINS:
                ax.add_patch(Circle((x, dec), r * 2.6, color="white", alpha=.18, lw=0, zorder=2))
        for a, b in leaders:
            ax.plot([x_of(a[0]), x_of(b[0])], [a[1], b[1]], c="white", lw=0.010 / fov * cw * 72 * 1.0,
                    alpha=.65, zorder=4)
        for h in rings:
            r = m.sz_star(S[h][2]) * 1.5 + 0.05
            ax.add_patch(Circle((x_of(S[h][0]), S[h][1]), r, fill=False, ec=COLORS["amber"],
                                lw=0.012 / fov * cw * 72, zorder=4))
        if title.startswith("03"):
            for (ra, dec) in SUN.values():
                ax.add_patch(Circle((x_of(ra), dec), 0.75, color=COLORS["amber"], zorder=3))
        for it in labs:
            ra, dec = S[it["hip"]][:2] if "hip" in it else (it["ra"], it["dec"])
            px = min(96, max(36, it["size"] * m.fu * 1080 / fov))        # Canva 夾限
            fs = px / 1080 * cw * 72
            ax.text(x_of(ra) + it["dx"], dec + it["dy"], it["text"], fontproperties=FP, fontsize=fs,
                    color=COLORS.get(it["color"], it["color"]), ha="center", va="center", zorder=6, clip_on=True)
        sz = 250 / 1920 * 2 * hh
        for y0 in (cy - hh, cy + hh - sz):
            ax.add_patch(Rectangle((cx - hw, y0), 2 * hw, sz, color="#FF6B6B", alpha=.10, lw=0, zorder=7))
        ax.set_title(f"{title}　fov {fov:g}", color="#FFC94A", fontproperties=MC.find_serif(), fontsize=9)
    p = os.path.join(OUT, f"{EP}_QA-特寫標籤.png")
    f.savefig(p, facecolor="#0B0F1E"); plt.close(f)
    print(f"  ✓ {os.path.basename(p)}")


if __name__ == "__main__":
    build()
