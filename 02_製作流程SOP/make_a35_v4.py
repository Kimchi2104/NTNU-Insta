# -*- coding: utf-8 -*-
"""A-35 現代星座（上）：88 個星座誰說了算｜大畫布 v4.6（長圖帶狀為主＋南盤三段）

論點：今天的 88 個星座是四百年疊出來的——托勒密 48（今算 50）＋大航海南天 12＋Plancius 3＋南十字＋后髮
＋Hevelius 7＋Lacaille 14＝88；1922 年 IAU 定名單，1928／1930 年 Delporte 把邊界畫成赤經赤緯直線，
星座從「圖」變成「一塊地」。它只是切天空的其中一種方法（陳卓 283 官），好處是全世界約好一起用。

來源：Stellarium 新版 skycultures/modern_iau（88 星座連線）、modern（Robur Carolinum、Quadrans Muralis 星群）、
  chinese（312 星官）；stellarium-master/data/constellations_spans.dat（Delporte 1930 邊界、B1875.0 帶狀表，
  357 段）——本腳本用它建「誰擁有哪一格天」的格網：面積、填色、邊界線、標籤位置都從同一份格網出，
  面積核對：全天 41,252.96、長蛇 1,302.84、南十字 68.45（＝逐字稿考據備忘，✓）。
  B1875 → J2000 用 PyEphem 4.2.1 的歲差（三個基向量求旋轉矩陣，純旋轉＝精確）。
逐字稿：04_腳本庫/A-35-現代星座上88個星座誰說了算-逐字稿-v1.md。天象 PyEphem 4.2.1 自算（台北）。

參數（依本集逐字稿重新評估，不照抄範例）
  lst = 180 → 走廊 x=0 落在 RA 12h：大熊（天樞 x+14、玉衡 −14）、南十字（x −6）、查理的橡樹（x +5…+30）
              三個「高赤緯」的主角都在走廊裡，沿走廊可以連續拍到盤上；長蛇（x +50…−55）橫跨走廊兩側；
              長圖切口 x=±180 在 RA 0h（雙魚—鯨魚一帶，本集不上畫面）。
  D_s = 56、D_r = 60 → 決定因素是 05 鏡的天貓座（Lynx 走廊外 x +40…+85，最北 2 Lyn +59.0）：走廊外長圖帶只到 D_r，
              D_r 56 時 2 Lyn、15 Lyn 兩顆會落到帶外（不畫），60 才收得進來（構圖上緣 ≤ 59.7）。
              07 鏡牆象限儀（走廊外 x −40…−75，最北 +55.6）也要 D_r ≥ 56。
  D_fill = −4 → k＝1.9099、R_fill＝179.53（|x_t|＋R_fill ≤ 180 ✓；D_fill −5 會到 181.4）。
              盤寬 ÷ 畫布寬＝0.99739 ⚠ 只差 0.3%（比 A-04 更像同寬！Canva 一定要照盤寬比例縮，不能設同寬）。
              南盤收到 dec +4：南天 12 座（最北 −45）、Lacaille 14 座（最北 羅盤 γ −27.7）全在盤上。
  x_tN = x_tS = 0。
  南盤 R：Canva 正角＝順時針＝時間前進（南盤）；鏡頭牆／逐頁表用 lst→lst＋rot 重畫，與 Canva 旋轉逐點相同。

和逐字稿分鏡表不同的地方（理由寫在回報與 note）
  ・13 鏡（中國星官）原寫北盤 R：改在長圖（走廊上的太微垣＋北斗＋軫翼角亢），Z 慢慢拉遠。
    原因：12 鏡在南盤，南盤→北盤只能硬切，而且 gen_canva_pages 的換組狀態只記一個盤，南→北→長圖的回程頁
    會用錯盤（歸位頁跑到南盤）；長圖上就能直接接 14、15，不用多 3–4 頁換組頁。
  ・14 鏡（今晚 9 點）原寫北盤：北盤「面北」看不到東南方、南盤「面南」時東南方的地平線斜 15°，蛇夫、盾牌
    又在盤緣外（要 D_fill ≤ −50，D_r 只能 ≤ 45，天貓座就收不進長圖）。改在長圖上（東在左、西在右，方向
    與面南看天一致）：蛇頭、蛇夫、蛇尾、盾牌同框，標高度／方位；上弦月在畫面右外 90°，用「西邊 →」標籤；
    地平線與山的實景交給 9:16 圖卡 C-A35-05（照片式的找星圖）。
  ・10 鏡「南盤小窗：南十字」：改成同一張長圖沿走廊往下滑到南十字（長蛇→南十字），再疊 C-A35-02 同比例方塊。
  ・05、08、09、12 拆成子鏡（旁白照原文切開，秒數照字數分，總長 230 不變）。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import great_circle, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-35"
OUT = os.path.join(BASE, "05_素材/A-35_現代星座上/_v4大畫布")
LST0 = 180.0
D_S, D_R, D_FILL = 56.0, 60.0, -4.0
TPE = (25.0330, 121.5654)
SC = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")
SPANS = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/data/constellations_spans.dat")
TEAL = "#3D8B7D"
GREY = "#DDE6F5"

WARN_OK = """
  03／04／06／12／12b（南盤 R）的「切點」⚠：起訖格都在盤心附近（fov ≤ 50 換組格）或全新構圖；
  換組頁由 gen_canva_pages 補（長圖轉南盤＝盤心 fov ≤ 50 那一格，盤緣圈內逐點相同）。
"""


# ══════════════════════════════════════════════════════════════════
# 〇、星曆與歲差
# ══════════════════════════════════════════════════════════════════
def _obs(when, lat=TPE[0], lon=TPE[1], tz=8):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.temp, o.pressure = 20.0, 1010.0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


def _prec_matrix(ep_from, ep_to):
    """把 ep_from 赤道座標轉到 ep_to 的旋轉矩陣（歲差＝純旋轉；用 ephem 轉三個基向量）"""
    import ephem
    cols = []
    for ra, dec in ((0.0, 0.0), (90.0, 0.0), (0.0, 90.0)):
        a = ephem.Equatorial(math.radians(ra), math.radians(dec), epoch=ep_from)
        b = ephem.Equatorial(a, epoch=ep_to)
        r, d = float(b.ra), float(b.dec)
        cols.append([math.cos(d) * math.cos(r), math.cos(d) * math.sin(r), math.sin(d)])
    return np.array(cols).T


def _ep():
    import ephem
    return dict(B1875=ephem.Date(2405889.258550475 - 2415020.0), J2000=ephem.J2000,
                E2027=ephem.Date("2027/1/1"))


EPOCH = _ep()
M_1875 = _prec_matrix(EPOCH["B1875"], EPOCH["J2000"])     # B1875 → J2000
M_2027 = _prec_matrix(EPOCH["E2027"], EPOCH["J2000"])     # 2027.0 → J2000


def rot_pts(M, pts):
    """pts：[(ra°, dec°)] → 套旋轉矩陣 → [(ra°, dec°)]"""
    a = np.radians(np.array(pts, dtype=float))
    v = np.stack([np.cos(a[:, 1]) * np.cos(a[:, 0]), np.cos(a[:, 1]) * np.sin(a[:, 0]), np.sin(a[:, 1])])
    w = M @ v
    ra = np.degrees(np.arctan2(w[1], w[0])) % 360.0
    dec = np.degrees(np.arcsin(np.clip(w[2], -1, 1)))
    return list(zip(ra.tolist(), dec.tolist()))


def sep(a, b):
    r1, d1, r2, d2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def altaz(ra, dec, when):
    import ephem
    o = _obs(when)
    b = ephem.FixedBody(); b._ra, b._dec = math.radians(ra), math.radians(dec); b._epoch = ephem.J2000
    b.compute(o)
    return math.degrees(b.alt), math.degrees(b.az)


def moon_at(when):
    import ephem
    o = _obs(when)
    mo = ephem.Moon(); mo.compute(o)
    q = ephem.Equatorial(ephem.Equatorial(mo.ra, mo.dec, epoch=o.date), epoch=ephem.J2000)
    return dict(ra=math.degrees(q.ra), dec=math.degrees(q.dec), alt=round(math.degrees(mo.alt), 1),
                az=round(math.degrees(mo.az), 1), phase=round(mo.phase, 0))


MOON = moon_at("2027/6/11 21:00")


# ══════════════════════════════════════════════════════════════════
# 一、IAU 邊界格網（constellations_spans.dat，B1875）
#   每行＝「RA1 RA2 Dec_low 星座」：由上往下掃，第一個 RA1≤α<RA2 且 δ≥Dec_low 的就是該點的星座
#   （Roman 1987 的查表法）。所有斷點切成格子 → 每格一個主人 → 面積、填色、邊界線、名牌位置
# ══════════════════════════════════════════════════════════════════
def _hms(s):
    h, m_, x = (float(t) for t in s.split(":"))
    return h + m_ / 60 + x / 3600


def _dm(s):
    sg = -1 if s.startswith("-") else 1
    d, m_ = (float(t) for t in s.lstrip("+-").split(":"))
    return sg * (d + m_ / 60)


class IAUGrid:
    def __init__(self, path):
        L = []
        for ln in open(path, encoding="utf-8"):
            p = ln.split()
            if len(p) >= 4:
                L.append((_hms(p[0]), _hms(p[1]), _dm(p[2]), p[3]))
        self.n_lines = len(L)
        self.R = sorted({0.0, 24.0} | {a for a, _, _, _ in L} | {b for _, b, _, _ in L})
        self.D = sorted({-90.0, 90.0} | {d for _, _, d, _ in L})
        self.NI, self.NJ = len(self.R) - 1, len(self.D) - 1
        own = {}
        for j in range(self.NJ):
            dm = (self.D[j] + self.D[j + 1]) / 2
            for i in range(self.NI):
                rm = (self.R[i] + self.R[i + 1]) / 2
                c = None
                for a, b, d, cc in L:
                    if d <= dm and a <= rm < b:
                        c = cc
                        break
                if c == "Ser":                       # 巨蛇：蛇頭（RA<17h）／蛇尾
                    c = "SerCaput" if rm < 17 else "SerCauda"
                elif c:
                    c = c.upper()
                own[(i, j)] = c
        self.own = own

    def area(self):
        A = {}
        for (i, j), c in self.own.items():
            a = ((self.R[i + 1] - self.R[i]) * 15 * (math.sin(math.radians(self.D[j + 1]))
                 - math.sin(math.radians(self.D[j]))) * 180 / math.pi)
            A[c] = A.get(c, 0.0) + a
        return A

    def _o(self, i, j):
        if j < 0 or j >= self.NJ:
            return "__out__"
        return self.own[(i % self.NI, j)]

    def _v(self, i, j):                               # 格點 → (RA°, Dec°)，B1875
        return (self.R[i % (self.NI + 1)] * 15.0 if i <= self.NI else self.R[i % self.NI] * 15.0,
                self.D[j])

    @staticmethod
    def _dense(a, b, step=0.5):
        n = max(1, int(math.ceil(max(abs(b[0] - a[0]), abs(b[1] - a[1])) / step)))
        return [(a[0] + (b[0] - a[0]) * t / n, a[1] + (b[1] - a[1]) * t / n) for t in range(n)]

    def loops(self, cons):
        """cons（集合）佔的區域外框 → 閉合迴圈（J2000 [(ra,dec)]）；evenodd 填色"""
        cons = set(cons)
        E = {}
        NI = self.NI
        for (i, j), c in self.own.items():
            if c not in cons:
                continue
            for (di, dj, a, b) in ((0, -1, (i, j), (i + 1, j)), (1, 0, (i + 1, j), (i + 1, j + 1)),
                                   (0, 1, (i + 1, j + 1), (i, j + 1)), (-1, 0, (i, j + 1), (i, j))):
                nb = self._o(i + di, j + dj)
                if nb in cons:
                    continue
                if dj == -1 and j == 0:              # 南天極那條退化邊不算
                    continue
                if dj == 1 and j == self.NJ - 1:
                    continue
                a2, b2 = (a[0] % NI, a[1]), (b[0] % NI, b[1])
                E.setdefault(a2, []).append(b2)
        out = []
        while E:
            st = next(iter(E))
            cur, loop = st, [st]
            while True:
                nx = E[cur].pop()
                if not E[cur]:
                    del E[cur]
                if nx == st:
                    break
                loop.append(nx)
                cur = nx
                if cur not in E:
                    break
            pts = []
            for a, b in zip(loop, loop[1:] + loop[:1]):
                pa, pb = self.vert(a), self.vert(b)
                if abs(pb[0] - pa[0]) > 180:                  # 跨 0h
                    pb = (pb[0] + 360 if pb[0] < pa[0] else pb[0] - 360, pb[1])
                pts += self._dense(pa, pb)
            out.append(rot_pts(M_1875, pts))
        return out

    def vert(self, v):
        i, j = v
        return (self.R[i] * 15.0, self.D[j])

    def edges(self, sel=lambda a, b: True):
        """不同主人之間的邊界（每條一次）→ 串成折線（J2000）。sel(主人A, 主人B, 邊的兩端赤緯)"""
        segs = []
        NI = self.NI
        for (i, j), c in self.own.items():
            for (di, dj, a, b) in ((1, 0, (i + 1, j), (i + 1, j + 1)), (0, 1, (i, j + 1), (i + 1, j + 1))):
                if j + dj >= self.NJ:
                    continue
                nb = self._o(i + di, j + dj)
                if nb == c:
                    continue
                pa, pb = self.vert((a[0] % (NI + 1), a[1])), self.vert((b[0] % (NI + 1), b[1]))
                if not sel(c, nb, min(pa[1], pb[1])):
                    continue
                segs.append(((a[0] % NI, a[1]), (b[0] % NI, b[1])))
        adj = {}
        for a, b in segs:
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
        used, lines = set(), []

        def walk(st):
            path, cur = [st], st
            while True:
                nxt = [n for n in adj[cur] if frozenset((cur, n)) not in used]
                if not nxt:
                    return path
                n = nxt[0]
                used.add(frozenset((cur, n)))
                path.append(n)
                cur = n
                if len(adj[cur]) != 2:
                    return path
        for v in [v for v in adj if len(adj[v]) != 2] + list(adj):
            while any(frozenset((v, n)) not in used for n in adj[v]):
                lines.append(walk(v))
        out = []
        for ln in lines:
            pts = []
            for a, b in zip(ln, ln[1:]):
                pa, pb = self.vert(a), self.vert(b)
                if abs(pb[0] - pa[0]) > 180:
                    pb = (pb[0] + 360 if pb[0] < pa[0] else pb[0] - 360, pb[1])
                pts += self._dense(pa, pb)
            pts.append(self.vert(ln[-1]))
            out.append(rot_pts(M_1875, pts))
        return out

    def centroid(self, c):
        """面積加權質心（J2000）——名牌放這裡"""
        v = np.zeros(3)
        for (i, j), cc in self.own.items():
            if cc != c:
                continue
            r0, r1 = self.R[i] * 15, self.R[i + 1] * 15
            d0, d1 = self.D[j], self.D[j + 1]
            a = math.radians(r1 - r0) * (math.sin(math.radians(d1)) - math.sin(math.radians(d0)))
            rm, dm = math.radians((r0 + r1) / 2), math.radians((d0 + d1) / 2)
            v += a * np.array([math.cos(dm) * math.cos(rm), math.cos(dm) * math.sin(rm), math.sin(dm)])
        ra, dec = math.degrees(math.atan2(v[1], v[0])) % 360, math.degrees(math.asin(v[2] / np.linalg.norm(v)))
        return rot_pts(M_1875, [(ra, dec)])[0]

    def north_edge(self, c):
        return max(self.D[j + 1] for (i, j), cc in self.own.items() if cc == c)

    def meridian_between(self, c1, c2):
        """c1、c2 之間最長的一段等赤經邊界（B1875）→ (RA°, dec_lo, dec_hi)"""
        best = None
        for (i, j), c in self.own.items():
            nb = self._o(i + 1, j)
            if {c, nb} == {c1, c2}:
                ra = self.R[(i + 1)] * 15
                cand = (ra, self.D[j], self.D[j + 1])
                # 合併同一條經線上相鄰的格
                if best and abs(best[0] - ra) < 1e-9 and abs(best[2] - self.D[j]) < 1e-9:
                    best = (ra, best[1], self.D[j + 1])
                elif not best or (self.D[j + 1] - self.D[j]) > (best[2] - best[1]):
                    best = cand
        return best


GRID = IAUGrid(SPANS)
AREA = GRID.area()

# ══════════════════════════════════════════════════════════════════
# 二、88 星座：出身分組、中文正式名、連線
# ══════════════════════════════════════════════════════════════════
ZH = dict(And="仙女", Ant="唧筒", Aps="天燕", Aqr="寶瓶", Aql="天鷹", Ara="天壇", Ari="白羊", Aur="御夫", Boo="牧夫",
          Cae="雕具", Cam="鹿豹", Cnc="巨蟹", CVn="獵犬", CMa="大犬", CMi="小犬", Cap="摩羯", Car="船底", Cas="仙后",
          Cen="半人馬", Cep="仙王", Cet="鯨魚", Cha="蝘蜓", Cir="圓規", Col="天鴿", Com="后髮", CrA="南冕", CrB="北冕",
          Crv="烏鴉", Crt="巨爵", Cru="南十字", Cyg="天鵝", Del="海豚", Dor="劍魚", Dra="天龍", Equ="小馬", Eri="波江",
          For="天爐", Gem="雙子", Gru="天鶴", Her="武仙", Hor="時鐘", Hya="長蛇", Hyi="水蛇", Ind="印第安", Lac="蝎虎",
          Leo="獅子", LMi="小獅", Lep="天兔", Lib="天秤", Lup="豺狼", Lyn="天貓", Lyr="天琴", Men="山案", Mic="顯微鏡",
          Mon="麒麟", Mus="蒼蠅", Nor="矩尺", Oct="南極", Oph="蛇夫", Ori="獵戶", Pav="孔雀", Peg="飛馬", Per="英仙",
          Phe="鳳凰", Pic="繪架", Psc="雙魚", PsA="南魚", Pup="船尾", Pyx="羅盤", Ret="網罟", Sge="天箭", Sgr="人馬",
          Sco="天蠍", Scl="玉夫", Sct="盾牌", Ser="巨蛇", Sex="六分儀", Tau="金牛", Tel="望遠鏡", Tri="三角",
          TrA="南三角", Tuc="杜鵑", UMa="大熊", UMi="小熊", Vel="船帆", Vir="室女", Vol="飛魚", Vul="狐狸")
assert len(ZH) == 88
PTOL = ("And Aqr Aql Ara Ari Aur Boo CMa CMi Cnc Cap Cas Cen Cep Cet CrA CrB Crv Crt Cyg Del Dra Equ Eri Gem Her "
        "Hya Leo Lep Lib Lup Lyr Oph Ori Peg Per Psc PsA Sge Sgr Sco Ser Tau Tri UMa UMi Vir Car Pup Vel").split()
KEYSER = "Aps Cha Dor Gru Hyi Ind Mus Pav Phe TrA Tuc Vol".split()
OTHER5 = "Col Mon Cam Cru Com".split()                 # Plancius 3＋南十字＋后髮
HEV = "CVn Lac LMi Lyn Sct Sex Vul".split()
LAC = "Ant Cae Cir For Hor Men Mic Nor Oct Pic Pyx Ret Scl Tel".split()
assert len(PTOL) == 50 and len(set(PTOL + KEYSER + OTHER5 + HEV + LAC)) == 88 == len(set(ZH) & set(
    PTOL + KEYSER + OTHER5 + HEV + LAC))
ORIGIN = {}
for grp, cs in (("托勒密 48（今 50）", PTOL), ("Keyser＆de Houtman・Plancius 12", KEYSER),
                ("Plancius 3・南十字・后髮", OTHER5), ("Hevelius 7", HEV), ("Lacaille 14", LAC)):
    for c in cs:
        ORIGIN[c] = grp
GRIDKEY = lambda c: c.upper() if c != "Ser" else None


def load_sc(cu):
    d = json.load(open(os.path.join(SC, cu, "index.json"), encoding="utf-8"))
    return {c["id"].split()[-1]: c for c in d["constellations"] + d.get("asterisms", [])}


def segs_of(c):
    """連線；遇到非 HIP（Gaia 編號字串）就斷開，不把前後兩顆硬接起來"""
    out = []
    for l in c.get("lines", []):
        run = []
        for h in l:
            if isinstance(h, int):
                run.append(h)
            else:
                if len(run) > 1:
                    out.append(run)
                run = []
        if len(run) > 1:
            out.append(run)
    return out


IAU = load_sc("modern_iau")
MOD = load_sc("modern")
CHN = load_sc("chinese")
assert len(IAU) == 88 and len(CHN) == 312
SEG = {c: segs_of(IAU[c]) for c in IAU}
segs = lambda cs: [s for c in cs for s in SEG[c]]
hips_of = lambda ss: sorted({h for s in ss for h in s})
SEG_ROBUR = segs_of(MOD["RoC"])
SEG_QUAD = segs_of(MOD["QuM"])
SEG_CHN = [s for c in CHN.values() for s in segs_of(c)]
DIPPER = [[54061, 53910, 58001, 59774, 54061], [59774, 62956, 65378, 67301]]

# 主角星
DUBHE, MERAK, ALKAID = 54061, 53910, 67301
BETELGEUSE, RIGEL, ALNILAM = 27989, 24436, 26311
ACRUX, GACRUX, ACHERNAR, RIGIL, HADAR, CANOPUS = 60718, 61084, 7588, 71683, 68702, 30438
UNUK, RASALHAGUE, ETA_SER, THETA_SER, ALPHA_SCT = 77070, 86032, 89962, 92946, 91117
ALPHARD = 46390
FELIS_STAR = 48615            # HIP 48615 的星名就叫 Felis（貓座被廢後留下的名字；Stellarium modern_iau）
FELIS_C = (147.0, -27.0)      # 貓座示意中心（Lalande 1799：長蛇與唧筒之間；示意，不是邊界）
LMC = (80.89, -69.76)         # 大麥哲倫雲
SMC = (13.19, -72.83)         # 小麥哲倫雲


def ellipse(c, a, b, n=72):
    """天球上的小橢圓（a＝赤經向、b＝赤緯向半軸，度）"""
    return [((c[0] + a * math.cos(2 * math.pi * k / n) / math.cos(math.radians(c[1]))) % 360,
             c[1] + b * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]
MAINS = [DUBHE, MERAK, ALKAID, BETELGEUSE, RIGEL, ACRUX, GACRUX, ACHERNAR, UNUK, RASALHAGUE, ETA_SER,
         ALPHA_SCT, ALPHARD]

# 亞歷山卓（31.2°N）西元 150 年看不到的天區：以當年南天極（J2000 RA 0h47m、Dec −79.7°）為圓心、半徑 31.2°
ALEX_POLE, ALEX_R = (11.75, -79.7), 31.2


def small_circle(c, r, n=240):
    ra0, d0 = map(math.radians, c)
    rr = math.radians(r)
    out = []
    for k in range(n + 1):
        b = 2 * math.pi * k / n
        d = math.asin(math.sin(d0) * math.cos(rr) + math.cos(d0) * math.sin(rr) * math.cos(b))
        a = ra0 + math.atan2(math.sin(b) * math.sin(rr) * math.cos(d0), math.cos(rr) - math.sin(d0) * math.sin(d))
        out.append((math.degrees(a) % 360, math.degrees(d)))
    return out


def dec_circle_2027(dec, n=360):
    return rot_pts(M_2027, [(360.0 * k / n, dec) for k in range(n + 1)])


# 台北／鵝鑾鼻：永不升起的界線（2027 赤緯；含 0.57° 地平折射）
LIM_TPE = -(90 - 25.033) - 0.57
LIM_ELB = -(90 - 21.90) - 0.57


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


# ══════════════════════════════════════════════════════════════════
# 三、自訂圖層（邊界、填色、圈、遮罩、2027 格線）：同一份幾何出 SVG（大畫布＋南北盤）與縮圖牆
# ══════════════════════════════════════════════════════════════════
def edges_sel(fn):
    return GRID.edges(fn)


SER_OPH = GRID.meridian_between("OPH", "SerCauda")


def grid2027_zoom():
    """蛇夫—蛇尾邊界附近的 2027 赤經赤緯線（每 1°），放大框用"""
    ra_b, d_lo, d_hi = SER_OPH
    c = rot_pts(M_1875, [(ra_b, (d_lo + d_hi) / 2)])[0]
    inv = np.linalg.inv(M_2027)
    c27 = rot_pts(inv, [c])[0]
    out = []
    for k in range(-8, 9):
        ra = round(c27[0]) + k
        out.append(rot_pts(M_2027, [(ra, c27[1] + t * 0.25) for t in range(-60, 61)]))
    for k in range(-14, 15):
        dec = round(c27[1]) + k
        out.append(rot_pts(M_2027, [(c27[0] + t * 0.25, dec) for t in range(-60, 61)]))
    return out, c


ZOOM_LINES, ZOOM_C = grid2027_zoom()


def bright_grid():
    out = []
    for ra in range(0, 360, 15):
        out.append([(ra, -88 + t) for t in range(0, 177)])
    for dec in range(-75, 90, 15):
        out.append([(t * 1.0, dec) for t in range(0, 361)])
    return out


# 每層：[(kind, geom, style)]；kind＝line（折線，style: color, w, op, dash）／fill（迴圈，style: color, op, mode）
#   fill 的 mode：band＝長圖帶＋盤本體（同 pos_primary）；disc＝只畫在盤上（大畫布版也照盤投影放在盤區）
def custom_defs():
    D = {}
    W = 0.10
    D["IAU邊界"] = [("line", edges_sel(lambda a, b, d: True), dict(color=GREY, w=W, op=0.70))]
    D["IAU邊界-北段"] = [("line", edges_sel(lambda a, b, d: d >= 30), dict(color=GREY, w=W, op=0.70))]
    D["IAU邊界-中段"] = [("line", edges_sel(lambda a, b, d: d >= -30), dict(color=GREY, w=W, op=0.70))]
    D["IAU邊界-大熊座"] = [("line", edges_sel(lambda a, b, d: "UMA" in (a, b)), dict(color=GREY, w=0.12, op=0.75,
                                                                                    dash="1.0 0.7"))]
    D["經緯線-加亮"] = [("line", bright_grid(), dict(color="#9FB3D9", w=0.08, op=0.38))]
    D["填色-長蛇座"] = [("fill", GRID.loops({"HYA"}), dict(color=COLORS["blue"], op=0.22, mode="band")),
                     ("line", GRID.loops({"HYA"}), dict(color=COLORS["blue"], w=0.16, op=0.9))]
    D["填色-南十字座"] = [("fill", GRID.loops({"CRU"}), dict(color=COLORS["amber"], op=0.30, mode="band")),
                      ("line", GRID.loops({"CRU"}), dict(color=COLORS["amber"], w=0.16, op=0.9))]
    D["填色-巨蛇與蛇夫"] = [("fill", GRID.loops({"SerCaput"}), dict(color=COLORS["green"], op=0.22, mode="band")),
                       ("fill", GRID.loops({"SerCauda"}), dict(color=COLORS["green"], op=0.22, mode="band")),
                       ("fill", GRID.loops({"OPH"}), dict(color=COLORS["amber"], op=0.16, mode="band")),
                       ("line", GRID.loops({"SerCaput"}) + GRID.loops({"SerCauda"}),
                        dict(color=COLORS["green"], w=0.16, op=0.9)),
                       ("line", GRID.loops({"OPH"}), dict(color=COLORS["amber"], w=0.14, op=0.8))]
    D["填色-台北看不到的4個"] = [("fill", GRID.loops({c}), dict(color=COLORS["red"], op=0.28, mode="disc"))
                          for c in ("CHA", "OCT", "MEN", "APS")] + \
                         [("line", GRID.loops({"CHA"}) + GRID.loops({"OCT"}) + GRID.loops({"MEN"}) +
                           GRID.loops({"APS"}), dict(color=COLORS["red"], w=0.16, op=0.9))]
    D["圈-台北永不升起"] = [("line", [dec_circle_2027(LIM_TPE)], dict(color="#48E39B", w=0.22, op=0.95))]
    D["圈-鵝鑾鼻永不升起"] = [("line", [dec_circle_2027(LIM_ELB)], dict(color="#48E39B", w=0.22, op=0.95, dash="1.2 0.8"))]
    D["遮罩-亞歷山卓150年"] = [("fill", [small_circle(ALEX_POLE, ALEX_R)], dict(color="#000000", op=0.62, mode="disc")),
                         ("line", [small_circle(ALEX_POLE, ALEX_R)], dict(color=COLORS["red"], w=0.16, op=0.85,
                                                                          dash="1.0 0.7"))]
    D["已淘汰星座"] = [("line", [great_circle(*S_[a][:2], *S_[b][:2]) for s in SEG_ROBUR + SEG_QUAD
                             for a, b in zip(s, s[1:]) if a in S_ and b in S_],
                      dict(color=COLORS["red"], w=0.26, op=0.95, dash="0.9 0.6")),
                     ("line", [small_circle(FELIS_C, 6.0)], dict(color=COLORS["red"], w=0.22, op=0.9, dash="0.9 0.6"))]
    D["麥哲倫雲"] = [("fill", [ellipse(LMC, 5.4, 4.6)], dict(color=COLORS["mw"], op=0.22, mode="disc")),
                    ("fill", [ellipse(SMC, 2.6, 1.8)], dict(color=COLORS["mw"], op=0.20, mode="disc"))]
    D["經緯線-2027（放大框）"] = [("line", ZOOM_LINES, dict(color=COLORS["blue"], w=0.04, op=0.75))]
    D["IAU邊界-放大框"] = [("line", edges_sel(lambda a, b, d: {a, b} & {"OPH", "SerCauda", "SerCaput", "SCT",
                                                                   "SGR", "AQL", "HER", "SCO"}),
                          dict(color="#FFFFFF", w=0.05, op=0.95))]
    return D


S_ = {}          # build() 裡填入星表（custom_defs 的已淘汰星座要用）


def _fmap_canvas(m, mode):
    def f(ra, dec):
        h = m.xw(ra)
        if mode == "disc":
            return m.p_disc(h, dec, dec > 0)
        if abs(dec) < m.Dr:
            return m.p_band(h, dec)
        return m.p_disc(h, dec, dec > 0)
    return f


def _fmap_disc(m, north):
    def f(ra, dec):
        p = m.pos_disc(ra, dec, north)
        return p[0] if p else None
    return f


def render_svg(s, prims, runs, fmap):
    for kind, geom, st in prims:
        if kind == "line":
            rr = []
            for pts in geom:
                rr += runs(pts)
            s.polylines(rr, stroke=st["color"], w=st["w"], opacity=st["op"], dash=st.get("dash"))
        else:
            mp = fmap(st.get("mode", "band"))
            d = []
            for loop in geom:
                P = [mp(ra, dec) for ra, dec in loop]
                if any(p is None for p in P) or len(P) < 3:
                    continue
                d.append("M " + " L ".join(f"{x:.2f} {-y:.2f}" for x, y in P) + " Z")
            if d:
                s.parts.append(f'<g fill="{st["color"]}" fill-opacity="{st["op"]:.3f}" fill-rule="evenodd" '
                               f'stroke="none"><path d="{" ".join(d)}"/></g>')


def write_custom(m, defs):
    files = {}
    for name, prims in defs.items():
        s = m._new()
        render_svg(s, prims, m.runs_all, lambda mode: _fmap_canvas(m, mode))
        files[name] = m._write(s, name)
    return files


def write_custom_discs(m, defs):
    for name, prims in defs.items():
        for north in (True, False):
            s = m._new_disc()
            render_svg(s, prims, lambda pts, n=north: m._runs_disc(pts, n), lambda mode, n=north: _fmap_disc(m, n))
            m._write_disc(s, north, name)


EXTRA = {"keys": [], "defs": {}}


def hook_draw(m):
    """縮圖牆／預覽：draw_mpl 畫完後再畫本鏡開著的自訂層（邊界、填色……）"""
    orig = m.draw_mpl

    def draw(ax, line_groups=(), maglim=None, mw_n=9000, labels=(), disc=None):
        orig(ax, line_groups, maglim=maglim, mw_n=mw_n, labels=labels, disc=disc)
        from matplotlib.patches import PathPatch
        from matplotlib.path import Path
        if disc is None:
            runs = m.runs_all
            fm = lambda mode: _fmap_canvas(m, mode)
            off = (0.0, 0.0)
        else:
            runs = lambda pts: m._runs_disc(pts, disc)
            fm = lambda mode: _fmap_disc(m, disc)
            off = m.disc_center(disc)
        for key in EXTRA["keys"]:
            for kind, geom, st in EXTRA["defs"][key]:
                if kind == "line":
                    for pts in geom:
                        for r in runs(pts):
                            ax.plot([p[0] + off[0] for p in r], [p[1] + off[1] for p in r], c=st["color"],
                                    lw=0.8 if st["w"] < 0.2 else 1.1, alpha=min(1, st["op"] + 0.1),
                                    ls="--" if st.get("dash") else "-", zorder=6)
                else:
                    mp = fm(st.get("mode", "band"))
                    verts, codes = [], []
                    for loop in geom:
                        P = [mp(ra, dec) for ra, dec in loop]
                        if any(p is None for p in P):
                            continue
                        verts += [(x + off[0], y + off[1]) for x, y in P] + [(0, 0)]
                        codes += [Path.MOVETO] + [Path.LINETO] * (len(P) - 1) + [Path.CLOSEPOLY]
                    if verts:
                        ax.add_patch(PathPatch(Path(verts, codes), fc=st["color"], ec="none",
                                               alpha=st["op"], zorder=3))
    m.draw_mpl = draw


# ══════════════════════════════════════════════════════════════════
# 四、連線分組
# ══════════════════════════════════════════════════════════════════
LG_ALL = [(segs(IAU), "white", 0.7)]
LG_PTOL = [(segs(PTOL), "amber", 0.9)]
LG_KEY = [(segs(KEYSER), "green", 1.1)]
LG_HEV = [(segs(HEV), "blue", 1.1)]
LG_LAC = [(segs(LAC), "purple", 1.1)]
LG_SER = [(segs(["Ser"]), "green", 1.1), (segs(["Oph"]), "amber", 1.0), (segs(["Sct"]), "blue", 1.1)]
LG_CHN = [(SEG_CHN, TEAL, 0.9)]
LG_DIP = [(DIPPER, "white", 1.3)]
LINE_SETS = [(LG_PTOL, "連線-托勒密48"), (LG_KEY, "連線-南天12（Keyser＆de Houtman）"),
             (LG_HEV, "連線-Hevelius7"), (LG_LAC, "連線-Lacaille14"), (LG_SER, "連線-巨蛇蛇夫盾牌"),
             (LG_CHN, "連線-中國星官312"), (LG_DIP, "連線-北斗七星")]
CUSTOM_KEYS = {"界": "IAU邊界", "界北": "IAU邊界-北段", "界中": "IAU邊界-中段", "界熊": "IAU邊界-大熊座",
               "格亮": "經緯線-加亮", "填蛇": "填色-長蛇座", "填十": "填色-南十字座", "填巨": "填色-巨蛇與蛇夫",
               "填四": "填色-台北看不到的4個", "圈北": "圈-台北永不升起", "圈鵝": "圈-鵝鑾鼻永不升起",
               "罩": "遮罩-亞歷山卓150年", "廢": "已淘汰星座", "格27": "經緯線-2027（放大框）",
               "界放": "IAU邊界-放大框", "雲": "麥哲倫雲"}
LINES_KEY = dict({"L4": "星座連線", "托": "連線-托勒密48", "南12": "連線-南天12（Keyser＆de Houtman）",
                  "赫": "連線-Hevelius7", "拉": "連線-Lacaille14", "蛇": "連線-巨蛇蛇夫盾牌",
                  "中": "連線-中國星官312", "斗": "連線-北斗七星"}, **CUSTOM_KEYS)
LINE_GROUPS = dict({"L4": LG_ALL, "托": LG_PTOL, "南12": LG_KEY, "赫": LG_HEV, "拉": LG_LAC, "蛇": LG_SER,
                    "中": LG_CHN, "斗": LG_DIP}, **{k: [] for k in CUSTOM_KEYS})


# ══════════════════════════════════════════════════════════════════
# 五、旁白字數（中文字＋外文音節；逐字稿 vo_units 的同一套例外）
# ══════════════════════════════════════════════════════════════════
VO_FIX = {"Keyser": 2, "Houtman": 2, "Plancius": 4, "Bayer": 2, "Hevelius": 4, "Lacaille": 3, "Delporte": 4,
          "UMa": 3, "Ori": 3, "IAU": 3, "de": 1}


def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏ]+|\d+|[㐀-鿿〇]", t):
        if re.match(r"[㐀-鿿〇]", w):
            n += 1
        elif w in VO_FIX:
            n += VO_FIX[w]
        elif w.isdigit():
            n += len(w)
        else:
            n += max(1, len(re.findall(r"[aeiouy]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 六、建置
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    S_.update(S)
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=D_S, D_r=D_R, D_fill=D_FILL,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None, maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    yp = m.y_pole
    DEFS = custom_defs()

    # ── 面積核對（＝逐字稿考據備忘） ──
    tot = sum(AREA.values())
    print(f"\n── IAU 格網：{GRID.n_lines} 段、{GRID.NI}×{GRID.NJ} 格、{len([c for c in AREA if c])} 塊 ──")
    print(f"  全天 {tot:.2f}（4π＝41252.96）；長蛇 {AREA['HYA']:.2f}、室女 {AREA['VIR']:.2f}、大熊 {AREA['UMA']:.2f}；"
          f"南十字 {AREA['CRU']:.2f}、小馬 {AREA['EQU']:.2f}；長蛇／南十字＝{AREA['HYA'] / AREA['CRU']:.2f}")
    assert abs(tot - 41252.96) < 0.05 and abs(AREA["HYA"] - 1302.84) < 0.01 and abs(AREA["CRU"] - 68.45) < 0.01
    print(f"  巨蛇：蛇頭 {AREA['SerCaput']:.2f}＋蛇尾 {AREA['SerCauda']:.2f}＝{AREA['SerCaput'] + AREA['SerCauda']:.2f}")
    for c in ("CHA", "OCT", "MEN", "APS"):
        print(f"  {c} 最北（B1875）{GRID.north_edge(c):+.2f}")

    # ── 構圖工具 ──
    def P(h):
        ra, dec = (S[h][:2] if isinstance(h, int) else h)
        return (x_of(ra), dec)

    def fr(pts, fov, dx=0.0, dy=0.0, corridor=False, cx=None, cy=None):
        """長圖構圖；走廊外的上下緣不出 D_r（再外面是填滿圓的重複天區）"""
        pts = [P(h) for h in pts]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        x = (max(xs) + min(xs)) / 2 + dx if cx is None else cx
        y = (max(ys) + min(ys)) / 2 + dy if cy is None else cy
        if not corridor:
            lim = m.Dr - fov * 8 / 9 - 0.3
            y = max(-lim, min(lim, y))
        return (round(x, 2), round(y, 2), float(fov), 0.0)

    def disc_xy(h, rot, north=False):
        ra, dec = (S[h][:2] if isinstance(h, int) else h)
        keep = m.lst
        m.lst = LST0 - rot if north else LST0 + rot
        p = m.pos_disc(ra, dec, north)
        m.lst = keep
        c = m.disc_center(north)
        return (p[0][0] + c[0], p[0][1] + c[1]) if p else None

    def far(cx, cy, f, north=False):
        c = m.disc_center(north)
        return max(math.hypot(cx + sx * f / 2 - c[0], cy + sy * f * 8 / 9 - c[1]) for sx in (-1, 1) for sy in (-1, 1))

    def dfit(hips, rot, pad=0.12, minfov=30.0, dx=0.0, dy=0.0, fov=None, north=False):
        pts = [p for p in (disc_xy(h, rot, north) for h in hips) if p]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        f = fov or max(minfov, (max(xs) - min(xs)) * (1 + 2 * pad), (max(ys) - min(ys)) * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        while far(cx, cy, f, north) > m.R_fill - 1.0:
            f *= 0.98
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    SP = (0.0, -yp)                                   # 南盤心（畫布座標）

    # ════════════════════ 構圖 ════════════════════
    LEO = hips_of(SEG["Leo"]); VIR = hips_of(SEG["Vir"]); HYA = hips_of(SEG["Hya"])
    F01a = fr(hips_of(SEG["UMa"] + SEG["Leo"]), 44.0, dy=-4.0)
    F01b = (0.0, 0.0, 66.5, 0.0)                      # 長圖帶內最大（上下緣 ±59.1）
    F02 = (8.0, 0.0, 66.5, 0.0)
    ROT03 = 0.0
    F03a = (0.0, round(-yp, 2), 50.0, ROT03)           # 換組格（盤心 fov 50）
    F03b = (0.0, round(-yp + 8.0, 2), 150.0, 0.0)      # 南盤總覽：南天極在下半、托勒密的南天在上
    F04a = (0.0, round(-yp, 2), 170.0, 0.0)
    F04b = (0.0, round(-yp, 2), 170.0, 40.0)           # 慢轉 40°（順時針＝時間前進）
    lyn = hips_of(SEG["Lyn"])
    F05 = fr(lyn, 30.0, dx=-3.0)
    F05b = fr(hips_of(SEG["Sct"]), 30.0, dy=2.0)
    F06a = (0.0, round(-yp, 2), 34.0, 0.0)            # ＝換組格（前一格 fov 34）
    F06b = (0.0, round(-yp, 2), 170.0, 0.0)
    F06c = (0.0, round(-yp, 2), 170.0, 90.0)
    men = hips_of(SEG["Men"])
    F06d = dfit(men + [LMC], 90.0, fov=40.0)
    F07a = fr(hips_of(SEG_ROBUR) + [FELIS_C], 60.0, corridor=True, dx=-2.0)
    F07b = fr(hips_of(SEG_QUAD), 26.0, dy=-3.0)
    uma = hips_of(SEG["UMa"])
    F08a = fr([h for s in DIPPER for h in s], 56.0, corridor=True, dy=-4.0)
    F08b = fr(hips_of(SEG["Ori"]), 50.0)
    F09a = (0.0, 0.0, 66.5, 0.0)
    F09b = (0.0, 0.0, 64.5, 0.0)
    F09c = (0.0, 0.0, 62.5, 0.0)
    F10a = fr(HYA, 66.5, cx=x_of(GRID.centroid("HYA")[0]) + 4.0, cy=-12.0)
    F10b = fr(hips_of(SEG["Cru"]), 30.0, corridor=True, dy=1.0)
    ser = hips_of(SEG["Ser"]); oph = hips_of(SEG["Oph"]); sct = hips_of(SEG["Sct"])
    F11a = fr(ser + oph + sct, 64.0)
    zc = P(ZOOM_C)
    F11b = (round(zc[0], 2), round(zc[1], 2), 8.0, 0.0)
    F11c = F11a                                       # 拉回總覽（換組前；不然換組要在 fov 8 沿走廊走 120°）
    F12a = (0.0, round(-yp, 2), 104.0, 0.0)           # 台北的圈（r＝k·24.4＝46.6）整圈入鏡
    F12b = (0.0, round(-yp, 2), 98.0, 0.0)
    F13a = fr(hips_of(SEG["Leo"] + SEG["Vir"] + SEG["Crv"]) + [DUBHE, ALKAID], 50.0, dx=-3.0)
    F13b = fr(hips_of(SEG["Leo"] + SEG["Vir"] + SEG["Crv"]) + [DUBHE, ALKAID], 62.0, dx=-3.0)
    F14 = fr(ser + oph + sct, 62.0, dx=-2.0)
    F15 = fr([h for s in DIPPER for h in s], 52.0, corridor=True, dy=-4.0)
    FR = dict(F01a=F01a, F01b=F01b, F02=F02, F03a=F03a, F03b=F03b, F04a=F04a, F04b=F04b, F05=F05, F05b=F05b,
              F06a=F06a, F06b=F06b, F06c=F06c, F06d=F06d, F07a=F07a, F07b=F07b, F08a=F08a, F08b=F08b,
              F09a=F09a, F09c=F09c, F10a=F10a, F10b=F10b, F11a=F11a, F11b=F11b, F12a=F12a, F12b=F12b,
              F13a=F13a, F13b=F13b, F14=F14, F15=F15)
    print("\n── 構圖（cx, cy, fov, rot） ──")
    for k, v in FR.items():
        extra = f"  角落距南盤心 {far(*v[:3]):.1f}" if v[1] < -yp + 60 and abs(v[1] + yp) < 90 else ""
        print(f"  {k} {v}{extra}")

    # ════════════════════ 標籤 ════════════════════
    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": round(a[0], 3), "dec": round(a[1], 3)}
        if isinstance(a, str):                         # 星座縮寫 → IAU 區域質心
            ra, dec = GRID.centroid(a)
            return {"ra": round(ra, 3), "dec": round(dec, 3)}
        if len(a) == 1:
            return {"hip": a[0]}
        v = [0.0, 0.0, 0.0]
        for h in a:
            r, d = math.radians(S[h][0]), math.radians(S[h][1])
            v[0] += math.cos(d) * math.cos(r); v[1] += math.cos(d) * math.sin(r); v[2] += math.sin(d)
        n = math.sqrt(sum(c * c for c in v))
        return {"ra": round(math.degrees(math.atan2(v[1], v[0])) % 360, 3),
                "dec": round(math.degrees(math.asin(v[2] / n)), 3)}

    def lab(a, text, col, fov, px=48, dx=0.0, dy=0.0, key=None, sub=None, px2=36, disc=False, sub_col="white"):
        """px＝Canva 字級（1080 寬）。sub＝第二行小字"""
        s1 = px * fov / (m.fu * 1080)
        out = []
        base = dict(anchor(a), disc=disc) if disc else anchor(a)
        if sub:
            s2 = px2 * fov / (m.fu * 1080)
            g = (s1 + s2) * m.fu * 0.62
            out.append(dict(base, text=text, color=col, size=round(s1, 3), dx=round(dx, 2),
                            dy=round(dy + g / 2, 2), key=key or text))
            out.append(dict(base, text=sub, color=sub_col, size=round(s2, 3), dx=round(dx, 2),
                            dy=round(dy - g / 2, 2), key=(key or text) + "-sub"))
        else:
            out.append(dict(base, text=text, color=col, size=round(s1, 3), dx=round(dx, 2), dy=round(dy, 2),
                            key=key or text))
        return out

    GK = lambda c: {"Ser": "SerCaput"}.get(c, c.upper())
    LB = {}
    f = F02[2]
    LB["托勒密"] = []
    for c, dx, dy in (("Leo", 0, -3), ("Vir", 0, -4), ("Hya", 10, 2), ("Crv", 0, -3), ("Crt", 0, -4),
                      ("Boo", 0, 0), ("UMa", 0, -6), ("Cnc", 0, 0), ("Cen", 0, 6), ("Lib", 0, 0)):
        LB["托勒密"] += lab(GK(c), ZH[c] + "座", "amber", f, px=40, dx=dx, dy=dy, key=f"托-{c}")
    f = F03b[2]
    LB["亞歷山卓看不到"] = (lab(ALEX_POLE, "亞歷山卓看不到的天", "red", f, px=46, dy=-18.0, disc=True,
                         sub="西元 150 年・北緯 31°", px2=36)
                     + lab([ACHERNAR], "水委一", "white", f, px=38, dx=0, dy=-5.0, disc=True, sub="當年看不到")
                     + lab([ACRUX], "南十字", "amber", f, px=38, dy=7.0, disc=True, sub="托勒密看得到")
                     + lab([CANOPUS], "老人星", "amber", f, px=38, dy=-5.0, disc=True))
    f = F04a[2]
    LB["南天12"] = []
    kdx = {"Cha": (0, -5), "Vol": (0, 4), "Aps": (0, -4), "Pav": (0, -5), "Tuc": (0, -5), "Mus": (0, 4),
           "Dor": (0, 4), "Hyi": (0, -5), "Ind": (0, -5), "Gru": (0, -5), "Phe": (0, -5), "TrA": (0, -5)}
    for c in KEYSER:
        dx, dy = kdx[c]
        LB["南天12"] += lab(c.upper(), ZH[c] + "座", "green", f, px=40, dx=dx, dy=dy, disc=True, key=f"南-{c}",
                           sub="變色龍" if c == "Cha" else None, px2=32)
    f = F05[2]
    LB["天貓"] = (lab("LYN", "天貓座", "blue", f, px=50, dx=-7.0, dy=0.0, sub="要有山貓的眼睛", px2=38)
                + lab("LMI", "小獅座", "blue", f, px=36, dx=0, dy=-3.0)
                + lab("UMA", "大熊座", "white", f, px=36, dx=-4, dy=-10.0)
                + lab("GEM", "雙子座", "white", f, px=36, dx=6, dy=-6.0))
    f = F05b[2]
    LB["盾牌"] = (lab("SCT", "盾牌座", "blue", f, px=50, dx=5.0, dy=-3.0, sub="獻給波蘭國王", px2=38)
                + lab([97649], "牛郎星", "white", f, px=36, dy=-2.4))
    f = F06b[2]
    LB["Lacaille14"] = []
    for c in LAC:
        LB["Lacaille14"] += lab(c.upper(), ZH[c] + "座", "purple", f, px=40, disc=True, key=f"拉-{c}",
                                sub="桌山" if c == "Men" else None, px2=32)
    f = F06d[2]
    LB["山案"] = (lab("MEN", "山案座", "purple", f, px=52, dx=0, dy=6.0, disc=True, sub="開普敦的桌山", px2=40)
                + lab(LMC, "大麥哲倫雲", "white", f, px=38, dx=-4.0, dy=-2.5, disc=True))
    f = F07a[2]
    LB["已淘汰"] = (lab(hips_of(SEG_ROBUR), "查理的橡樹", "red", f, px=46, dy=-6.0, sub="Robur Carolinum・1679", px2=34)
                 + lab(FELIS_C, "貓座（示意）", "red", f, px=44, dy=-8.0, sub="Felis・1799", px2=34))
    f = F07b[2]
    LB["牆象限儀"] = lab(hips_of(SEG_QUAD), "牆象限儀", "red", f, px=48, dy=-6.0, sub="Quadrans Muralis・1795", px2=36)
    LB["已淘汰"] += lab(hips_of(SEG_QUAD), "牆象限儀", "red", F07a[2], px=44, dy=-6.0, key="象限儀-遠")
    LB["IAU縮寫"] = []
    for c in sorted(ZH):
        ab = c if c != "Ser" else "Ser"
        if c == "Ser":
            for part, k in (("SerCaput", "Ser 蛇頭"), ("SerCauda", "Ser 蛇尾")):
                LB["IAU縮寫"] += lab(part, "Ser", "white", 56.0, px=36, key=f"縮-{part}")
            continue
        big = c in ("UMa", "Ori")
        LB["IAU縮寫"] += lab(c.upper(), ab, "amber" if big else "white", 56.0, px=64 if big else 36,
                           key=f"縮-{c}", sub=(ZH[c] + "座") if big else None, px2=44)
    f = F10a[2]
    LB["長蛇"] = lab("HYA", "長蛇座", "blue", f, px=52, dx=0, dy=-4.0, sub="1,303 平方度・最大", px2=38)
    f = F10b[2]
    LB["南十字"] = (lab("CRU", "南十字座", "amber", f, px=48, dx=0, dy=-6.5, sub="68 平方度・最小", px2=38)
                 + lab([RIGIL], "南門二", "white", f, px=34, dy=-2.4)
                 + lab("HYA", "長蛇座", "blue", f, px=40, dy=0.0, key="長蛇-遠"))
    f = F11a[2]
    LB["巨蛇"] = (lab("SerCaput", "蛇頭", "green", f, px=50, dx=-2.0, dy=2.0, sub="Serpens Caput", px2=34)
                + lab("SerCauda", "蛇尾", "green", f, px=50, dx=1.0, dy=-3.0, sub="Serpens Cauda", px2=34)
                + lab("OPH", "蛇夫座", "amber", f, px=46, dx=0, dy=-8.0))
    f = F11b[2]
    zx = ZOOM_C
    LB["放大框"] = (lab((zx[0] + 1.2, zx[1] + 2.6), "1875 年的邊界", "white", f, px=40, key="1875")
                 + lab((zx[0] - 1.6, zx[1] - 2.9), "2027 年的赤經線", "blue", f, px=40, key="2027")
                 + lab((zx[0], zx[1] - 5.2), "夾角約 0.85°", "amber", f, px=44, key="夾角"))
    f = F12a[2]
    LB["台北看不到"] = []
    for c, dx, dy in (("Cha", 0, 0), ("Oct", 0, 0), ("Men", 0, 0), ("Aps", 0, 0)):
        LB["台北看不到"] += lab(c.upper(), ZH[c] + "座", "red", f, px=44, dx=dx, dy=dy, disc=True, key=f"看-{c}")
    LB["台北看不到"] += lab((180.0, LIM_TPE + 0.8), "台北：這圈以南永不升起", "#48E39B", f, px=36, disc=True,
                         key="台北圈")
    f = F12b[2]
    LB["鵝鑾鼻"] = (lab((240.0, LIM_ELB + 0.8), "鵝鑾鼻：退到這圈", "#48E39B", f, px=36, disc=True, key="鵝圈")
                 + lab("APS", "天燕座", "red", f, px=44, disc=True, key="鵝-Aps", sub="邊界露出一角", px2=34))
    f = F13b[2]
    LB["中國星官"] = (lab([DUBHE, MERAK, 58001, 59774, 62956, 65378, ALKAID], "北斗", TEAL, f, px=44, dy=-5.5)
                   + lab((176.0, 14.0), "太微垣", TEAL, f, px=44, key="太微")
                   + lab((166.0, -18.0), "翼宿", TEAL, f, px=38, key="翼")
                   + lab((187.0, -19.5), "軫宿", TEAL, f, px=38, key="軫")
                   + lab((201.3, -14.0), "角宿", TEAL, f, px=38, key="角"))
    f = F14[2]
    a_u = altaz(*S[UNUK][:2], "2027/6/11 21:00"); a_r = altaz(*S[RASALHAGUE][:2], "2027/6/11 21:00")
    a_e = altaz(*S[ETA_SER][:2], "2027/6/11 21:00"); a_s = altaz(*S[ALPHA_SCT][:2], "2027/6/11 21:00")
    LB["今晚"] = (lab([UNUK], "蛇頭", "green", f, px=46, dx=-5.0, dy=4.2, sub=f"東南高處 {a_u[0]:.0f}°", px2=34)
                + lab([RASALHAGUE], "蛇夫", "amber", f, px=46, dy=3.4, sub=f"正東 {a_r[0]:.0f}°", px2=34)
                + lab([ETA_SER], "蛇尾", "green", f, px=46, dx=-1.0, dy=3.4, sub=f"東南 {a_e[0]:.0f}°", px2=34)
                + lab([ALPHA_SCT], "盾牌座", "blue", f, px=44, dx=1.0, dy=-7.0, sub="蛇尾下方・要暗處", px2=32)
                + lab(((LST0 - (F14[0] + F14[2] / 2 - 9.0)) % 360, F14[1] - 40.0), "西邊：上弦月 →",
                      "white", f, px=36, key="月", sub="午夜才下山", px2=30))
    f = F15[2]
    LB["下集"] = (lab([DUBHE, MERAK, 58001, 59774, 62956, 65378, ALKAID], "北斗七星", "white", f, px=48, dy=-6.0)
                + lab("UMA", "大熊座 UMa", "white", f, px=40, dx=0, dy=-12.0, key="UMa下集"))
    label_sets = [(v, k) for k, v in LB.items()]
    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    # ════════════════════ 圖層 ════════════════════
    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_ALL)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    write_custom(m, DEFS)
    MARKS = [(MAINS, "主角星白點", "dot")]
    for hips, name, style in MARKS:
        m.L_marks(hips, name, style)
    for items, name in label_sets:
        m.L_labels(items, name)
    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS, marks=MARKS)
    print("\n── 盤：自訂圖層 ──")
    write_custom_discs(m, DEFS)

    # ════════════════════ 鏡頭（vo＝逐字稿 v1 原文） ════════════════════
    ls = lambda *n: list(n)
    shots = [
        dict(code="01", kind="Z", sec=10, north=True, frames=[F01a, F01b], layers=["L4", "界"], labels=[],
             vo="上週，蘇菲把希臘星座畫進一本書；今天，回到課本上那一套。同一片星空，天文學家把它——切成八十八塊。",
             card="同一片星空，／天文學家把它——切成八十八塊。",
             note="長圖：春季大熊—獅子 fov 44 拉遠到長圖帶內最大 66.5（上下緣 ±59°，逐字稿寫「全天」：長圖帶 9:16 放不下全天，"
                  "這一格是帶內最大）；88 星座連線（白細）＋IAU 邊界（淡白）淡入，銀河層淡出（Canva 調 L1 透明度）；開場字卡"),
        dict(code="02", kind="Z", sec=15, north=True, frames=[F01b, F02], layers=["托"], labels=ls("托勒密"),
             overlay="C-A35-01_88個星座從哪來", overlay_layers=["到150年層"],
             vo="這套星座的老底子，是將近一千九百年前，亞歷山卓的托勒密，在《天文學大成》裡列的四十八個星座、一千多顆星。"
                "上週的蘇菲，用的也是這四十八個。",
             card="托勒密：48 座",
             note="只亮托勒密 48 座的連線（琥珀；modern_iau 的線，挑出托勒密的 50 個今名星座：南船＝船底＋船尾＋船帆）；"
                  "迄格疊 C-A35-01 第一層（約 150 年：48）"),
        dict(code="03", kind="R", sec=11, north=False, frames=[F03a, F03b], layers=["托", "罩"],
             labels=ls("亞歷山卓看不到"),
             vo="可是托勒密看不到南天最南的那一塊；在希臘這套星圖裡，星座和星座之間，也留著不少沒畫進圖形的暗星。",
             card="希臘星圖的空白",
             note="長圖沿走廊往下→換南盤（同框）→拉遠 fov 132：托勒密連線（琥珀）＋深色罩＝亞歷山卓（31.2°N）西元 150 年"
                  "看不到的天區（以當年南天極 J2000 RA 0h47m、Dec −79.7° 為圓心、半徑 31.2° 的偏心圓）；"
                  "南十字、南門二、馬腹一在罩外，水委一在罩內"),
        dict(code="04", kind="R", sec=18, north=False, frames=[F04a, F04b], layers=["南12", "罩"],
             labels=ls("南天12"),
             overlay="C-A35-01_88個星座從哪來", overlay_layers=["到1597年層"],
             vo="十六世紀末，荷蘭船隊開到南半球，領航員 Keyser 和 de Houtman 記下南天的星，Plancius 把它們做成十二個新星座："
                "孔雀、杜鵑、天燕、蝘蜓、飛魚……一六〇三年，Bayer 的星圖把它們印了出來。",
             card="南天的 12 個新星座",
             note="南盤 fov 112：12 個新星座（綠）在罩裡依序亮起（Canva 逐個顯示或整層淡入）；慢轉 0°→+40°；"
                  "蝘蜓座標籤加小字「變色龍」；迄格疊 C-A35-01 第二層（1597：+12）"),
        dict(code="05", kind="Z", sec=13, north=True, frames=[F05], layers=["L4", "赫"], labels=ls("天貓"),
             vo="北邊和赤道一帶的空地，由但澤的 Hevelius 補上，他的星圖一六九〇年出版，有七個留到今天。"
                "像天貓座：他說，要有山貓的眼睛才看得到；",
             card="要有山貓的眼睛",
             note="南盤→長圖（換組，沿走廊回到帶中央）→滑到大熊與雙子之間的天貓座（藍，暗星；Hevelius 7 座整層藍）；"
                  "天貓最北 2 Lyn +59.0° 在畫面上緣（D_r 60 才收得進長圖帶）"),
        dict(code="05b", kind="Z", sec=4, north=True, frames=[F05, F05b], layers=["L4", "赫"], labels=ls("盾牌"),
             labels_start=ls("天貓"),
             overlay="C-A35-01_88個星座從哪來", overlay_layers=["到1690年層"],
             vo="還有一面盾牌，是獻給波蘭國王的。",
             card="要有山貓的眼睛",
             note="S 往東（畫面往左）捲 140° 到天赤道南邊的盾牌座（藍）；迄格疊 C-A35-01 第三層（1690：+7，"
                  "連同 Plancius 3、南十字、后髮這 5 個一起補上）"),
        dict(code="06", kind="R", sec=16, north=False, frames=[F06a, F06b, F06c], layers=["拉", "雲"],
             labels=ls("Lacaille14"),
             vo="最後一批留到今天的，來自法國的 Lacaille。一七五〇年代，他在南非好望角量了將近一萬顆南天星，把空地填成十四個星座，"
                "幾乎全是儀器：望遠鏡、顯微鏡、時鐘、抽氣機……",
             card="14 個星座：儀器＋一座山",
             note="長圖→南盤（換組）→拉遠 fov 170：Lacaille 14 座（紫）依序亮起，慢轉 0°→90° 把盤側的唧筒、羅盤轉進畫面"),
        dict(code="06b", kind="R", sec=4, north=False, frames=[F06d], layers=["拉", "雲"], labels=ls("山案"),
             overlay="C-A35-01_88個星座從哪來", overlay_layers=["到1756年層"],
             vo="還有一座山：開普敦的桌山，就是山案座。",
             card="14 個星座：儀器＋一座山",
             note="推近山案座（大麥哲倫雲南端跨進山案座；雲＝淡色填色層）；迄格疊 C-A35-01 第四層（1756：+14＝88）；"
                  "桌山照片由美宣另尋授權圖（或公版版畫／自繪），腳本不提供"),
        dict(code="07", kind="Z", sec=15, north=True, frames=[F07a, F07b], layers=["廢"], labels=ls("牆象限儀"),
             labels_start=ls("已淘汰"),
             vo="從十七世紀到十九世紀初，各家星圖還加過不少：一棵橡樹、一具牆上的象限儀、一隻貓——後來都被淘汰了。"
                "同一顆星，換一張星圖，就換了一個星座。",
             card="被淘汰的：橡樹、貓",
             note="南盤→長圖（換組）：被淘汰的星座（紅虛線）：Robur Carolinum（船底—船帆—半人馬間，modern 星群 RoC）、"
                  "Felis（長蛇—唧筒間，示意圈；Stellarium 只剩 HIP 48615 的星名 Felis）→ 滑到 Quadrans Muralis"
                  "（牧夫—天龍間，modern 星群 QuM）"),
        dict(code="08", kind="Z", sec=14, north=True, frames=[F08a, F08b], layers=["L4"], labels=ls("IAU縮寫"),
             overlay="C-A35-04_88星座出身表",
             vo="一九二二年，剛成立三年的國際天文學聯合會在羅馬開大會，定下八十八個星座的名單，每個配三個字母的縮寫："
                "UMa 是大熊，Ori 是獵戶。",
             card="1922：88 個星座名",
             note="紅色虛線淡出；88 星座三字母縮寫標籤層淡入（UMa、Ori 放大＋中文）；角落小字「IAU 國際天文學聯合會」用原生文字；"
                  "推近大熊（走廊上，fov 56）→「Ori 是獵戶」滑到獵戶（fov 50）；迄格疊 9:16 圖卡 C-A35-04「88 星座出身表」"),
        dict(code="09", kind="Z", sec=7, north=True, frames=[F09a], layers=["格亮", "界北"], labels=[],
             vo="可是名單只有名字，沒有邊界。比利時天文學家 Delporte 接下這份工作：",
             card="1930：一點空隙都不留",
             note="長圖帶內最大 fov 66.5：經緯線層調亮（加亮層）；IAU 邊界先畫北段（dec ≥ +30）"),
        dict(code="09b", kind="Z", sec=6, north=True, frames=[F09b], layers=["格亮", "界中"], labels=[],
             vo="邊界全部沿著赤經、赤緯畫成直線，南天參考阿根廷的星圖。",
             card="1930：一點空隙都不留",
             note="同一片天微推（66.5→64.5）：邊界畫到 dec −30"),
        dict(code="09c", kind="Z", sec=6, north=True, frames=[F09c], layers=["格亮", "界"], labels=[],
             vo="一九二八年大會通過，一九三〇年出版——整片天空，一點空隙都不留。",
             card="1930：一點空隙都不留",
             note="64.5→62.5：全天邊界完成"),
        dict(code="10", kind="Z", sec=13, north=True, frames=[F10a, F10b], layers=["界", "填蛇", "填十"],
             labels=ls("南十字"), labels_start=ls("長蛇"),
             overlay="C-A35-02_邊界是一塊地", overlay_layers=["長蛇層", "南十字層"],
             vo="從此，星座不只是一幅圖，而是一塊地：天上每一點，都屬於、也只屬於一個星座。最大的長蛇座，面積是最小的南十字座的十九倍。",
             card="長蛇是南十字的 19 倍",
             note="長蛇座整塊填色（藍 22%；長蛇橫跨 105°，畫面只放得下中段，刻意讓它出畫面）→「最小的南十字座」沿走廊往下滑到"
                  "南十字（琥珀填色；逐字稿寫南盤小窗，改成同一張長圖滑過去，不換組）；迄格疊 C-A35-02（同比例方塊）"),
        dict(code="11", kind="Z", sec=9, north=True, frames=[F11a], layers=["蛇", "填巨", "界"],
             labels=ls("巨蛇"),
             overlay="C-A35-03_巨蛇被切成兩塊", overlay_layers=["三塊層", "89塊層"], overlay_at="start",
             vo="也有怪地方：巨蛇座被蛇夫座從中間切開，蛇頭蛇尾分在兩邊——八十八個星座，其實是八十九塊。",
             card="88 個星座，89 塊",
             note="滑到蛇夫—巨蛇：蛇頭、蛇尾兩塊填色（綠），蛇夫（琥珀）夾在中間；起格疊 C-A35-03"),
        dict(code="11b", kind="Z", sec=7, north=True, frames=[F11b], layers=["界放", "格27"],
             labels=ls("放大框"),
             vo="邊界照一八七五年的座標畫，地軸一直在晃，今天的線已經歪了一點。",
             card="88 個星座，89 塊",
             note="推近到蛇夫—蛇尾邊界（fov 8，逐字稿要的 5°–10° 放大框）：2027 年的赤經赤緯線（藍細）"
                  "與 1875 年的邊界（白）疊在一起，夾角約 0.85°（本腳本自算 −0.85°）"),
        dict(code="11c", kind="Z", sec=1, north=True, frames=[F11c], layers=["蛇", "填巨", "界"], labels=[],
             vo="",
             card="",
             note="（無旁白，1 秒）拉回蛇夫—巨蛇總覽，接下一鏡換南盤（不在 fov 8 沿走廊走 120°）"),
        dict(code="12", kind="R", sec=9, north=False, frames=[F12a], layers=["填四", "圈北"], labels=ls("台北看不到"),
             vo="這八十八個，台灣看得到幾個？在台北，有四個永遠不會升起：蝘蜓座、南極座、山案座、天燕座；",
             card="台北看不到的 4 個",
             note="長圖→南盤（換組）fov 64：台北永不升起的界線（2027 赤緯 −65.6°，含 0.57° 折射；綠圈），"
                  "圈內四個星座填色（紅）"),
        dict(code="12b", kind="R", sec=5, north=False, frames=[F12b], layers=["填四", "圈鵝"], labels=ls("鵝鑾鼻"),
             vo="跑到最南端的鵝鑾鼻，天燕座的邊界才露出一角。",
             card="台北看不到的 4 個",
             note="推近 fov 52：綠圈換成鵝鑾鼻（−68.7°，虛線），天燕座邊界一角跨出圈外（＝會升到地平線上；界內的星還是看不到）"),
        dict(code="13", kind="Z", sec=17, north=True, frames=[F13a, F13b], layers=["中", "界"], labels=ls("中國星官"),
             vo="其實，人類有好多種切天空的方法——像中國古代的星圖，就有二百八十三個星官。IAU 的八十八個，只是其中一種；"
                "它的好處是，全世界的天文學家約好了，一起用它。",
             card="283 星官 vs 88 星座",
             note="南盤→長圖（換組）：中國星官連線（青 #3D8B7D；Stellarium chinese 312 個，含後代增補）與 IAU 邊界交疊，"
                  "走廊上的太微垣＋北斗＋翼軫角，Z 慢慢拉遠 50→62（逐字稿寫北盤 R 慢轉；改長圖的理由見腳本開頭）"),
        dict(code="14", kind="Z", sec=23, north=True, frames=[F14], layers=["蛇"], labels=ls("今晚"),
             overlay="C-A35-05_今晚的巨蛇與盾牌",
             vo="今晚九點往東南看：高處那顆亮星，是巨蛇的頭；正東是蛇夫，東南方低一點是蛇尾——同一個星座，分在兩邊。"
                "蛇尾下方那面小盾牌，就是獻給波蘭國王的盾牌座；蛇尾和盾牌都暗，要到郊外才看得到。西邊的半個月亮，午夜才下山。",
             card="今晚 9 點：巨蛇、盾牌",
             note="長圖（東在左、西在右＝面南看天的方向）：巨蛇（綠）、蛇夫（琥珀）、盾牌（藍），標台北 6/11 21:00 的高度與方位；"
                  "上弦月在畫面右外（西南西 39°），用「西邊：上弦月 →」；迄格疊 9:16 圖卡 C-A35-05「今晚的巨蛇與盾牌」"
                  "（有地平線與方位，可存圖；標「市區大概只認得出蛇頭最亮那顆；蛇尾、盾牌用雙筒望遠鏡更好」）"),
        dict(code="15", kind="Z", sec=7, north=True, frames=[F15], layers=["斗", "界熊"], labels=ls("下集"),
             vo="下週五，下集：北斗七星其實不是星座？課本沒教的星群。",
             card="下集見｜現代星座（下）：課本沒教的星群",
             note="滑到北斗（走廊上）：北斗七星（白）亮起、大熊座邊界（細白）同框；端卡「下集見｜現代星座（下）：課本沒教的星群」"
                  "＋追蹤 CTA"),
    ]
    print("\n── 旁白字數 ──")
    tot_u = 0
    for sh in shots:
        u = vo_units(sh["vo"]); tot_u += u
        r = u / sh["sec"] if sh["sec"] else 0
        print(f"  {sh['code']:>3}  {u:3d} 字 / {sh['sec']:2d} 秒 ＝ {r:.2f}{'  ✗ 超過 4.5' if r > 4.5 else ''}")
        sh["vo_units"] = u
    tot_s = sum(s["sec"] for s in shots)
    print(f"  合計 {tot_u} 字 / {tot_s} 秒 ＝ {tot_u / tot_s:.2f} 字/秒")
    m.check_shots(shots)
    print("  判斷後接受的 ⚠：" + WARN_OK)
    for sh in shots:                                # 長圖：走廊外上下緣不出 D_r
        if sh["kind"] == "R":
            continue
        for (cx, cy, fov, rot) in sh["frames"]:
            hw, hh = fov / 2, fov * 8 / 9
            if abs(cy) + hh > m.Dr + 1e-6 and (abs(cx) + hw > m.wc - m.fe):
                print(f"  ⚠ {sh['code']}：畫面上下緣出 D_r 且碰到走廊外（cx {cx:+.0f}、fov {fov:.0f}）")

    rows = []
    for sh in shots:
        for i, (cx, cy, fov, rot) in enumerate(sh["frames"]):
            if sh["kind"] == "R":
                yc = m.disc_center(sh.get("north", True))[1]
                ew, use = 2 * m.R_fill / fov * 1080, f"{'北' if sh.get('north', True) else '南'}盤圖層組（置中）"
                off_ = (round(-cx / fov * 1080), round((cy - yc) / fov * 1080))
            else:
                ew, use = 360.0 / fov * 1080, "大畫布圖層組"
                off_ = (round(-cx / fov * 1080), round(cy / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"], "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": use, "元素寬px": round(ew), "位移X px": off_[0],
                         "位移Y px": off_[1], "旋轉度": round(rot, 1), "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[dict(s) for s in shots])

    # ── 數字核對（逐字稿星空對時表、考據備忘） ──
    print("\n── 數字核對 ──")
    print(f"  台北 −65.54 → 本腳本 {LIM_TPE:.2f}；鵝鑾鼻 {LIM_ELB:.2f}")
    for nm, h in (("蛇頭 Unukalhai", UNUK), ("蛇夫 α", RASALHAGUE), ("蛇尾 η", ETA_SER), ("θ¹ Ser", THETA_SER),
                  ("盾牌 α", ALPHA_SCT)):
        a, z = altaz(*S[h][:2], "2027/6/11 21:00")
        print(f"  6/11 21:00 {nm} 高 {a:5.1f}° 方位 {z:5.1f}°")
    print(f"  月 6/11 21:00 高 {MOON['alt']}° 方位 {MOON['az']}° 相 {MOON['phase']}%；RA {MOON['ra']:.1f} → x {x_of(MOON['ra']):+.1f}")
    print(f"  蛇夫—蛇尾邊界（B1875 RA {SER_OPH[0] / 15:.4f}h，dec {SER_OPH[1]:+.1f}…{SER_OPH[2]:+.1f}）放大框中心 "
          f"J2000 ({ZOOM_C[0]:.2f}, {ZOOM_C[1]:+.2f})")
    # 1875 邊界的經線 vs 2027 經線的夾角（放大框標「約 0.85°」）
    ra_b = SER_OPH[0]
    p1, p2 = rot_pts(M_1875, [(ra_b, SER_OPH[1]), (ra_b, SER_OPH[2])])
    inv = np.linalg.inv(M_2027)
    q1, q2 = rot_pts(inv, [p1, p2])
    ang = math.degrees(math.atan2((q2[0] - q1[0]) * math.cos(math.radians((q1[1] + q2[1]) / 2)), q2[1] - q1[1]))
    print(f"  1875 邊界經線在 2027 座標裡的傾角 {ang:+.2f}°（逐字稿：約 0.85°）")
    alex = [(nm, sep(S[h][:2], ALEX_POLE)) for nm, h in (("十字架二", ACRUX), ("南門二", RIGIL), ("馬腹一", HADAR),
                                                     ("水委一", ACHERNAR), ("老人星", CANOPUS))]
    print("  離 150 年南天極：" + "、".join(f"{n} {d:.1f}°（{'看不到' if d < ALEX_R else '看得到'}）" for n, d in alex))

    terms = {}
    for c in sorted(ZH):
        terms[c] = dict(hips=hips_of(SEG[c]), 原文=IAU[c]["common_name"]["native"], 拼音=c, 英文翻譯=IAU[c]["common_name"].get("english", ""),
                        中文=ZH[c] + "座", 顏色="white",
                        來源備註=f"{ORIGIN[c]}；IAU 面積 "
                                 + (f"{AREA['SerCaput'] + AREA['SerCauda']:.2f}（蛇頭 {AREA['SerCaput']:.2f}＋蛇尾 {AREA['SerCauda']:.2f}）"
                                    if c == "Ser" else f"{AREA[c.upper()]:.2f}") + " 平方度")
    for key, orig, en, zh, note in (("RoC", "Robur Carolinum", "Charles' Oak", "查理的橡樹（已廢）", "Halley 1679；modern 星群 RoC"),
                                    ("QuM", "Quadrans Muralis", "Mural Quadrant", "牆象限儀（已廢）", "Lalande 1795；modern 星群 QuM"),
                                    ("Fel", "Felis", "The Cat", "貓座（已廢）", "Lalande 1799；示意位置")):
        terms[key] = dict(hips=[], 原文=orig, 拼音="", 英文翻譯=en, 中文=zh, 顏色="red", 來源備註=note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst0": LST0, "area": {k: round(v, 2) for k, v in AREA.items() if k}, "moon_2100": MOON},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    hook_draw(m)
    EXTRA["defs"] = DEFS
    import make_a07_v4 as A7
    PREV = {"托勒密": (LG_PTOL, ["界"]), "亞歷山卓看不到": (LG_PTOL, ["罩"]), "南天12": (LG_KEY, []),
            "天貓": (LG_HEV, []), "盾牌": (LG_HEV, []), "Lacaille14": (LG_LAC, []), "山案": (LG_LAC, []),
            "已淘汰": ([], ["廢"]), "牆象限儀": ([], ["廢"]), "IAU縮寫": (LG_ALL, ["界"]), "長蛇": ([], ["填蛇"]),
            "南十字": ([], ["填十"]), "巨蛇": (LG_SER, ["填巨"]), "放大框": ([], ["格27", "界放"]),
            "台北看不到": ([], ["填四", "圈北"]), "鵝鑾鼻": ([], ["填四", "圈鵝"]), "中國星官": (LG_CHN, ["界"]),
            "今晚": (LG_SER, []), "下集": (LG_DIP, ["界熊"])}
    PREV["山案"] = (LG_LAC, ["雲"])
    for items, name in label_sets:
        lg, ex = PREV[name]
        EXTRA["keys"] = [CUSTOM_KEYS[k] for k in ex]
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=lg,
                  labels=[dict(it, pt=6) for it in items], title=f"{EP}　大畫布 v4.6（{name}標籤）")
    EXTRA["keys"] = []
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_PTOL)
    LS = {n: it for it, n in label_sets}
    walls = []
    for sh in shots:
        g = [x for k in sh.get("layers", []) for x in LINE_GROUPS[k]]
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", []) + sh.get("labels_start", [])))
        ex = [CUSTOM_KEYS[k] for k in sh.get("layers", []) if k in CUSTOM_KEYS]
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]], ex))
    sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
            title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


def sb_wall(m, path, walls, title=""):
    """make_a21_v4.sb_wall 加上每鏡的自訂層（邊界、填色、圈）"""
    from PIL import Image, ImageDraw, ImageFont
    tmp = []
    for i, (sh, g, labs, ex) in enumerate(walls):
        p = path.replace(".png", f"_tmp{i:02d}.png")
        EXTRA["keys"] = ex
        m.sb_grid(p, [sh], line_groups=g, labels=labs, cols=len(sh["frames"]), title="")
        tmp.append(p)
    EXTRA["keys"] = []
    ims = [Image.open(p).convert("RGB") for p in tmp]
    cols = 4
    rows = [ims[i:i + cols] for i in range(0, len(ims), cols)]
    ch = max(im.size[1] for im in ims)
    W = max(sum(im.size[0] for im in r) + 10 * cols for r in rows)
    out = Image.new("RGB", (W, len(rows) * (ch + 10) + 40), (11, 15, 30))
    d = ImageDraw.Draw(out)
    try:
        fnt = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 24)
    except Exception:
        fnt = None
    d.text((10, 6), title, fill=(255, 255, 255), font=fnt)
    y = 40
    for r in rows:
        x = 0
        for im in r:
            out.paste(im, (x, y)); x += im.size[0] + 10
        y += ch + 10
    out.save(path)
    for p in tmp:
        os.remove(p)
    print(f"  ✓ {os.path.basename(path)}（{len(walls)} 鏡）")


if __name__ == "__main__":
    build()
