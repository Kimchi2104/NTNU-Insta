# -*- coding: utf-8 -*-
"""A-09 夏威夷：四條回家的路（星線）｜大畫布 v4.6

輸出：L1銀河 L2星點 L3經緯線 L4星座連線（四條星線全開）
      L5連線-舀水杓 L6連線-脊椎骨 L7連線-釣線 L8連線-風箏 L9連線-指針
      L10主角星白點 L11主角星白圈
      L12…標籤：夏威夷星名／繁中星名／星線原文／星線中譯／星線-盤／西伯利亞／毛利／四島
      ＋ 南北盤圖層組 / 預覽黑底 / SB-分鏡 / SB-鏡頭牆 / 鏡頭清單 / 標籤資料
執行：python3 make_a09_v4.py

參數
  lst = 205 → 北走廊（x=0）＝RA 205：脊椎骨（Ka Iwikuamoʻo）整條就在走廊上——
             北極星 → 北斗 → 大角（x −8.9）→ 角宿一（x +3.7）→ 烏鴉 → 南十字（x +13～+15），
             一個 T 鏡頭從南極拉到北極。往東（左）依序是釣線（天蠍 x −35～−58、引航三角 x −74～−105）、
             風箏（飛馬大四邊形 x −141～−158、北落師門 −139）；舀水杓在右邊（x +88～+126，昴宿 +148）。
             四條線照季節由右往左排＝時間往前。畫布左右接縫在 RA 25（仙后在北盤、水委一在南盤，都不在帶上）。
  D_s = 48、D_r = 52 → 帶內 |dec|<48 收得下五車二 +46.0、天津四 +45.3、水委一以外的整條星線中段；
             老人星 −52.7、南十字、半人馬 α/β 都在南盤本體。（A-09 舊版 45/49 會把五車二、天津四切進縫合帶）
  D_fill = −25 → k=1.508、R_fill=173.4（|x_t|+R_fill ≤ 180）；北盤收到 dec −25：
             舀水杓到天狼、脊椎骨到烏鴉、風箏到土司空，一張盤就看得到四條線的北半段
  x_tN = x_tS = 0（Canva 可水平置中）

資料：Stellarium hawaiian_starlines（Kamehameha Schools 2017，S. M. Hoffmann 重整）。
      index.json 原樣取線；夏威夷文寫法補上 ʻokina 與 kahakō（Stellarium 檔內大多省略），
      以 Polynesian Voyaging Society 的拼法為準。指針（meridian pointers）依 description.md
      與 PVS「Hawaiian Star Lines」：北指針 θ–β Aur／Sadr–Deneb／Alpheratz–Caph，
      南指針 Mirzam–Canopus／Gacrux–Acrux／Dschubba–π Sco／Markab–Fomalhaut；
      本檔另畫延長線到北極星與南極（σ Oct），示意「連線指向天極」。
"""
import os, sys, json, math, csv, re, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-09"
OUT = os.path.join(BASE, "05_素材/A-09_夏威夷星線/_v4大畫布")
LST0 = 205.0
PHI_TPE = 25.03
LST_TPE_2000 = 347.29              # 2026/11/06 20:00 台北的地方恆星時（PyEphem 自算，見逐字稿考據）

# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
POL, SIG_OCT = 11767, 104382
DUB, MER, PHE, MEG, ALI, MIZ, ALK = 54061, 53910, 58001, 59774, 62956, 65378, 67301
ARC, SPI = 69673, 65474
ALGORAB = 60965
GACRUX, ACRUX = 61084, 60718
CAPELLA, CASTOR, POLLUX, PROCYON, SIRIUS = 24608, 36850, 37826, 37279, 32349
MIRZAM, CANOPUS = 30324, 30438
MENKALINAN, THETA_AUR = 28360, 28380
MINTAKA, ALNILAM, ALNITAK = 25930, 26311, 26727
BETELGEUSE, RIGEL = 27989, 24436
ALCYONE = 17702
DENEB, SADR, VEGA, ALTAIR = 102098, 100453, 91262, 97649
ANTARES, DSCHUBBA, PI_SCO, SHAULA = 80763, 78401, 78265, 85927
ALPHERATZ, SCHEAT, MARKAB, ALGENIB = 677, 113881, 113963, 1067
FOMALHAUT, DIPHDA, CAPH, SCHEDAR = 113368, 3419, 746, 3179

DIPPER = [DUB, MER, PHE, MEG, ALI, MIZ, ALK]
SQUARE = [ALPHERATZ, SCHEAT, MARKAB, ALGENIB]
MAINS = ([POL, ARC, SPI, GACRUX, ACRUX, CAPELLA, CASTOR, POLLUX, PROCYON, SIRIUS, MINTAKA,
          ALCYONE, DENEB, VEGA, ALTAIR, ANTARES, FOMALHAUT, CANOPUS] + SQUARE + DIPPER)


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium hawaiian_starlines index.json）
# ══════════════════════════════════════════════════════════════════
def sc_lines(culture):
    p = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master/"
                           f"{culture}/index.json")
    d = json.load(open(p, encoding="utf-8"))
    return {c["id"].split()[-1]: c["lines"] for c in d["constellations"]}


SL = sc_lines("hawaiian_starlines")
LG_KOM = [(SL["KOM"], "amber", 1.0), (SL["KHK"], "amber", 0.55), (SL["MAK"], "amber", 0.55)]
LG_IWI = [(SL["IWI"], "green", 1.0), (SL["NAH"], "green", 0.8), (SL["MEE"], "green", 0.8),
          (SL["HAN"], "green", 0.8)]
LG_MAN = [(SL["MAN"], "blue", 1.0), (SL["NAV"], "blue", 0.8)]
LG_LUP = [(SL["LUP"], "purple", 1.0), (SL["IWA"], "purple", 0.8)]
LG_ALL = LG_KOM + LG_IWI + LG_MAN + LG_LUP
# 指針：兩顆星赤經幾乎相同（ΔRA 0.05°～1.8°；Sadr–Deneb 4.8°）→ 同時過中天、上下排成一直線
PTR_N = [[THETA_AUR, MENKALINAN], [SADR, DENEB], [ALPHERATZ, CAPH]]
PTR_S = [[MIRZAM, CANOPUS], [GACRUX, ACRUX], [DSCHUBBA, PI_SCO], [MARKAB, FOMALHAUT]]
EXT_N = [[b, POL] for a, b in PTR_N]
EXT_S = [[b, SIG_OCT] for a, b in PTR_S]
LG_PTR = [(PTR_N + PTR_S, "red", 1.35), (EXT_N + EXT_S, "red", 0.45)]


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


def uniq(seglists):
    return sorted({h for segs in seglists for seg in segs for h in seg})


# ══════════════════════════════════════════════════════════════════
# 三、名詞總表（＝標籤對照表）
#   夏威夷文依 PVS 寫法（補 ʻokina、kahakō）；中文用台灣通行星名
# ══════════════════════════════════════════════════════════════════
HAW = {POL: "Hōkūpaʻa", ARC: "Hōkūleʻa", SPI: "Hikianalia",
       CAPELLA: "Hōkūlei", CASTOR: "Nānāmua", POLLUX: "Nānāhope", PROCYON: "Puana",
       SIRIUS: "ʻAʻā", MINTAKA: "Mintaka",
       DENEB: "Hawaiki", VEGA: "Keoe", ALTAIR: "Humu", ANTARES: "Lehua Kona",
       ALPHERATZ: "Manōkalanipō", SCHEAT: "Kākuhihewa", MARKAB: "Keawe", ALGENIB: "Piʻilani",
       FOMALHAUT: "Kūkaniloko"}
ZH = {POL: "北極星", ARC: "大角星", SPI: "角宿一", CAPELLA: "五車二", CASTOR: "北河二",
      POLLUX: "北河三", PROCYON: "南河三", SIRIUS: "天狼星", MINTAKA: "參宿三",
      DENEB: "天津四", VEGA: "織女一", ALTAIR: "牛郎（河鼓二）", ANTARES: "心宿二",
      ALPHERATZ: "壁宿二", SCHEAT: "室宿二", MARKAB: "室宿一", ALGENIB: "壁宿一",
      FOMALHAUT: "北落師門"}
COLOR = {}
for h in (CAPELLA, CASTOR, POLLUX, PROCYON, SIRIUS, MINTAKA):
    COLOR[h] = "amber"
for h in (POL, ARC, SPI):
    COLOR[h] = "green"
for h in (DENEB, VEGA, ALTAIR, ANTARES):
    COLOR[h] = "blue"
for h in (ALPHERATZ, SCHEAT, MARKAB, ALGENIB, FOMALHAUT):
    COLOR[h] = "purple"
# 星名偏移（畫布單位；東在左）。中文放在夏威夷名正下方
OFF = {POL: (0.0, 2.6), ARC: (-6.6, 0.6), SPI: (6.0, 0.6),
       CAPELLA: (5.2, -1.4), CASTOR: (-5.4, 1.0), POLLUX: (5.6, -1.2), PROCYON: (5.4, 0.4),
       SIRIUS: (-4.6, 0.4), MINTAKA: (4.8, 1.2),
       DENEB: (-1.0, -5.0), VEGA: (-5.0, 1.0), ALTAIR: (-4.0, -2.2), ANTARES: (-5.6, 0.6),
       ALPHERATZ: (-6.2, 1.8), SCHEAT: (0.0, 2.6), MARKAB: (5.0, -1.6), ALGENIB: (-5.0, -1.6),
       FOMALHAUT: (6.0, 0.6)}
DY_ZH = -2.3

# 星群（不是單星）：(錨點 HIP 群, 夏威夷文, 中文, 顏色, dx, dy)
GROUPS = {
    "七星": (DIPPER, "Nā Hiku", "北斗七星", "green", 0.0, 6.0),
    "烏鴉": (uniq([SL["MEE"]]), "Meʻe", "烏鴉座", "green", 7.0, 2.4),
    "南十字": ([GACRUX, ACRUX, 62434, 59747], "Hānaiakamalama", "南十字", "green", -9.5, 0.0),
    "昴宿": ([ALCYONE, 17499, 17489], "Makaliʻi", "昴宿星團", "amber", 0.0, 3.4),
    "獵戶": (uniq([SL["KHK"]]), "Ka Heihei o Nā Keiki", "獵戶座", "amber", 0.0, -12.5),
    "魚鉤": (uniq([SL["MAN"]]), "Ka Makau Nui o Māui", "天蠍座", "blue", -3.0, 28.0),
}
LINES = {   # 星線名：(錨點 ra,dec, 原文, 中譯, 顏色)
    "舀水杓": ((102.0, -30.0), "Ke Kā o Makaliʻi", "Makaliʻi 的舀水杓", "amber"),
    "脊椎骨": ((222.0, -4.0), "Ka Iwikuamoʻo", "脊椎骨", "green"),
    "釣線": ((262.0, -18.0), "Manaiakalani", "酋長的釣線", "blue"),
    "引航三角": ((293.0, 30.0), "引航三角", "Navigator's Triangle", "blue"),
    "風箏": ((355.0, -2.0), "Ka Lupe o Kawelo", "Kawelo 的風箏", "purple"),
}
LINES_DISC = {  # 北盤上的星線名（dec ≥ D_r 才進盤）：沿各線的赤經放在盤心附近
    "舀水杓": ((96.0, 56.0), "amber"), "脊椎骨": ((226.0, 66.0), "green"),
    "釣線": ((300.0, 57.0), "blue"), "風箏": ((338.0, 58.0), "purple"),
}
TERM_DY2 = -2.6


# ══════════════════════════════════════════════════════════════════
# 四、旁白字數（中文字＋外文音節；夏威夷文一個母音群＝一音節）
# ══════════════════════════════════════════════════════════════════
VOW = set("aeiouāēīōūAEIOUĀĒĪŌŪ")
DIPH = {"ai", "ae", "ao", "au", "ei", "eu", "oi", "ou"}
_BASE = str.maketrans("āēīōūĀĒĪŌŪ", "aeiouAEIOU")


def vo_units(t):
    """中文字＋外文音節：一個母音一音節，夏威夷文常見雙母音（ai、au、ei、ou…）算一個"""
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏʻ'’]+|\d+|[\u3400-\u9fff]", t):
        if re.match(r"[\u3400-\u9fff]", w):
            n += 1
        elif w.isdigit():
            n += len(w)
        elif w.isupper() and len(w) <= 4:
            n += len(w)                          # GPS → 三個字母
        else:
            c = w.translate(_BASE).lower()
            i = k = 0
            while i < len(c):
                if c[i] in "aeiou":
                    k += 1
                    if i + 1 < len(c) and c[i:i + 2] in DIPH:
                        i += 1
                i += 1
            n += max(1, k)
    return n


def build():
    S = G.load_stars(BASE)
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=48, D_r=52, D_fill=-25,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None,
               maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")

    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        if len(a) == 1:
            return {"hip": a[0]}
        ra, dec = centroid(a, S)
        return {"ra": ra, "dec": dec}

    def star_items(table, size, dy_extra=0.0):
        out = []
        for h, txt in table.items():
            if h not in S:
                continue
            dx, dy = OFF.get(h, (0.0, 2.4))
            w, _ = MC.label_box(txt, size, m.fu)
            if abs(dx) > 0.1:                                  # 左右：讓字邊貼著星
                dx = math.copysign(abs(dx) + w / 2 - 1.6, dx)
            out.append({"hip": h, "text": txt, "color": COLOR.get(h, "white"),
                        "size": size, "dx": round(dx, 2), "dy": round(dy + dy_extra, 2),
                        "key": f"HIP {h}"})
        return out

    def group_items(idx, size, dy_extra=0.0):
        out = []
        for k, (hips, haw, zh, col, dx, dy) in GROUPS.items():
            out.append(dict(anchor(hips), text=(haw, zh)[idx], color=col, size=size,
                            dx=dx, dy=dy + dy_extra, key=k))
        return out

    haw = star_items(HAW, 1.15) + group_items(0, 1.15)
    zh = star_items(ZH, 1.0, DY_ZH) + group_items(1, 1.0, DY_ZH)
    ln_o = [dict(ra=a[0], dec=a[1], text=o, color=c, size=1.45, dx=0.0, dy=0.0, key=k)
            for k, (a, o, z, c) in LINES.items()]
    ln_z = [dict(ra=a[0], dec=a[1], text=z, color=c, size=1.15, dx=0.0, dy=TERM_DY2, key=k)
            for k, (a, o, z, c) in LINES.items()]
    ln_disc = []
    for k, ((ra, dec), c) in LINES_DISC.items():
        o, z = LINES[k][1], LINES[k][2]
        ln_disc.append(dict(ra=ra, dec=dec, text=o, color=c, size=1.45, dx=0.0, dy=0.0,
                            key=k))
        ln_disc.append(dict(ra=ra, dec=dec, text=z, color=c, size=1.15, dx=0.0,
                            dy=-3.0, key=k))
    sib = [dict(hip=ALCYONE, text="西伯利亞：鴨巢", color="white", size=1.05, dx=0.0, dy=-6.4,
                key="鴨巢"),
           dict(hip=ALNILAM, text="西伯利亞：打穀者", color="white", size=1.05, dx=-11.5,
                dy=0.0, key="打穀者")]
    ra_s, de_s = centroid(uniq([SL["MAN"]]), S)
    maori = [dict(ra=ra_s, dec=de_s, text="Te Matau a Māui", color="white", size=1.15,
                  dx=-1.0, dy=32.0, key="毛利1"),
             dict(ra=ra_s, dec=de_s, text="毛利：Māui 的魚鉤", color="white", size=0.95,
                  dx=-1.0, dy=29.4, key="毛利1"),
             dict(ra=ra_s, dec=de_s, text="Manaia ki te Rangi", color="white", size=1.15,
                  dx=-1.0, dy=25.4, key="毛利2"),
             dict(ra=ra_s, dec=de_s, text="毛利：另一個季節的名字", color="white", size=0.95,
                  dx=-1.0, dy=22.8, key="毛利2")]
    isl = [dict(hip=ALPHERATZ, text="考艾 Kauaʻi", color="white", size=1.0, dx=-7.8,
                dy=-2.4, key="島-考艾"),
           dict(hip=SCHEAT, text="歐胡 Oʻahu", color="white", size=1.0, dx=6.5,
                dy=0.0, key="島-歐胡"),
           dict(hip=ALGENIB, text="茂宜 Maui", color="white", size=1.0, dx=-7.0,
                dy=-6.2, key="島-茂宜"),
           dict(hip=MARKAB, text="夏威夷島 Hawaiʻi", color="white", size=1.0, dx=0.0,
                dy=-6.6, key="島-夏威夷島")]

    label_sets = [(haw, "夏威夷星名"), (zh, "繁中星名"), (ln_o, "星線原文"),
                  (ln_z, "星線中譯"), (ln_disc, "星線-盤"), (sib, "西伯利亞"),
                  (maori, "毛利"), (isl, "四島")]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_ALL)
    line_sets = [(LG_KOM, "連線-舀水杓"), (LG_IWI, "連線-脊椎骨"), (LG_MAN, "連線-釣線"),
                 (LG_LUP, "連線-風箏"), (LG_PTR, "連線-指針")]
    for g, name in line_sets:
        m.L_lines(g, name=name)
    m.L_marks(MAINS, "主角星白點", "dot")
    m.L_marks(MAINS, "主角星白圈", "ring")
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=line_sets,
                  marks=[(MAINS, "主角星白點", "dot"), (MAINS, "主角星白圈", "ring")])

    # ════════════════════ 鏡頭 ════════════════════
    yp = m.y_pole

    def P(h):
        return m.pos_primary(*S[h][:2])

    arc = P(ARC)
    HOME = (0.0, 12.0, 44.0, 0.0)                 # 大角星一帶（走廊上）
    HOME2 = (0.0, 8.0, 50.0, 0.0)                 # 稍微拉遠（03 迄格＝04 定格＝05 起格）
    CRUX = (0.0, -62.0, 44.0, 0.0)                # 南十字（走廊下端；脊椎骨的起點）
    SW = (0.0, yp, 44.0, 0.0)                     # 長圖 ⇄ 北盤 換組格
    SCO_A = (-47.0, -21.0, 34.0, 0.0)              # 10 鏡中段：夏威夷名
    SCO = (-47.0, -21.0, 32.0, 0.0)                # 10 迄＝11 起：毛利名
    TRI = (-88.0, 12.9, 44.0, 0.0)               # 頂到 dec 52（走廊外縫合帶不變形），天津四才不會擠進上方安全區
    KITE = (-151.0, 0.0, 52.0, 0.0)
    KOM = (106.0, 0.0, 54.0, 0.0)
    BAIL = (131.0, -2.0, 46.0, 0.0)
    PLE = (146.0, 16.0, 30.0, 0.0)
    ROT_TPE = -((LST_TPE_2000 + 180.0 - LST0) % 360.0)   # −322.3 ≡ +37.7：盤轉到「11/6 20:00 面向北方」
    ROT_TPE_C = ROT_TPE + 360.0                          # Canva 旋轉只收 −180～180
    ROT_2020 = ROT_TPE_C - 5.01                          # 再過 20 分鐘（15.041°/h）
    TPE = (-6.0, yp + 40.0, 116.0, ROT_TPE_C)

    shots = [
        dict(code="01", kind="S", sec=12, north=True,
             frames=[(150.0, 0.0, 54.0, 0.0), (132.0, 0.0, 54.0, 0.0)],
             layers=[], labels=[],
             vo="上週，我們在古中國的天上，找一隻消失的神獸。今晚出海，到太平洋的正中間。"
                "同一片星空，夏威夷人看見——四條回家的路。",
             card="同一片星空，夏威夷人看見——四條回家的路",
             note="統一開頭：昴宿、畢宿、獵戶一帶（十一月東升的星）緩慢平移（畫面往左＝時間往前），先不開連線"),
        dict(code="02", kind="Z", sec=19, north=True,
             frames=[(132.0, 0.0, 54.0, 0.0), HOME],
             layers=[], labels=[], labels_end=["夏威夷星名", "繁中星名"],
             overlay="C-A09-03_航線與三角", overlay_layers=["島嶼層", "航線層"],
             vo="一九七六年，一艘雙體獨木舟從夏威夷出海：沒有羅盤、沒有六分儀、沒有地圖。"
                "三十四天後，它開進大溪地——四千多公里，全靠看天、看海。今年，剛好五十週年。"
                "船名 Hōkūleʻa，就是這顆大角星——「喜悅之星」。",
             note="從冬季星空滑到大角星（Hōkūleʻa）並推近；結束後疊概念圖 C-A09-03（島嶼→1976 航線）"),
        dict(code="03", kind="Z", sec=18, north=True,
             frames=[HOME, HOME2],
             layers=[], labels=["夏威夷星名", "繁中星名"],
             vo="帶路的，是密克羅尼西亞 Satawal 島的航海師 Mau Piailug——那時夏威夷人的"
                "遠洋導航，早已失傳。四年後，他的學生 Nainoa Thompson 親手把船帶到大溪地，"
                "被認為是六百多年來，第一位這麼做的夏威夷航海師。",
             note="大角星一帶，稍微拉遠"),
        dict(code="04", kind="Z", sec=25, north=True,
             frames=[HOME2],
             layers=[], labels=["夏威夷星名", "繁中星名"],
             overlay="C-A09-01_星羅盤", overlay_layers=["羅盤層", "參宿三層"],
             vo="Nainoa 把老師教的，整理成夏威夷的「星羅盤」：地平線一圈，切成三十二間房子。"
                "每顆星都從東邊固定的一間升起，再從西邊、同名的那一間落下。"
                "最好用的是獵戶腰帶上的 Mintaka，參宿三：它就在天赤道上，所以正東升起、正西落下。"
                "認得房子，就認得方向。",
             note="疊概念圖 C-A09-01（羅盤 32 間房子 → 參宿三：Hikina 升、Komohana 落）"),
        dict(code="05", kind="T", sec=17, north=True,
             frames=[HOME2, CRUX],
             layers=["L4"], labels=["星線原文", "星線中譯"],
             vo="可是天上的星有幾百顆，怎麼記？Nainoa 把整片天分成四條南北走向的「星線」，"
                "大多用傳統的夏威夷星名串起來。先說清楚：這不是古代傳下來的星圖，"
                "是現代航海家為了背天空，做的筆記。",
             note="四條星線（L4）亮起；沿走廊往下到南十字（脊椎骨的南端）"),
        dict(code="06", kind="T", sec=21, north=True,
             frames=[CRUX, SW],
             layers=["脊椎骨"], labels=["夏威夷星名", "繁中星名"],
             vo="先看最好認的一條：Ka Iwikuamoʻo，脊椎骨，從南天一路接到北天。"
                "最南端是南十字 Hānaiakamalama；往上是烏鴉座 Meʻe、角宿一 Hikianalia、"
                "大角星 Hōkūleʻa，再接北斗 Nā Hiku，最後是北極星 Hōkūpaʻa——「固定不動的星」。",
             note="只開脊椎骨（L6，綠）；沿走廊從南十字一路抬頭到北極星；迄格＝07 起格（長圖轉北盤）"),
        dict(code="07", kind="R", sec=13, north=True,
             frames=[SW, (0.0, yp, 160.0, -60.0)],
             layers=["L4"], labels=["夏威夷星名", "繁中星名"], labels_end=["星線-盤"],
             vo="退遠一點看：四條線像四根輻條，各管一個季節——冬天是 Makaliʻi 的舀水杓，"
                "春天是脊椎骨，夏天是酋長的釣線，秋天是 Kawelo 的風箏。",
             note="長圖轉北盤（同框換組；標籤與 06 迄格相同）→ 拉遠到 fov 160＋逆時針 −60°（4 小時），換成星線名"),
        dict(code="08", kind="R", sec=15, north=True,
             frames=[(0.0, yp, 160.0, -60.0), (0.0, yp, 160.0, -90.0)],
             layers=["L4", "指針"], labels=["星線-盤"],
             vo="每條星線還配一對「指針」：兩顆星幾乎同時爬到最高點，那一刻上下排成一直線，"
                "順著往下，就是正北或正南。北極星看不到的時候——比如過了赤道——就看指針。",
             note="指針（L9，紅）亮起：北指針延長線全部收向北極星。迄格不回大畫布（下一頁先歸位）"),
        dict(code="09", kind="Z", sec=26, north=True,
             frames=[CRUX],
             layers=["脊椎骨"], labels=["夏威夷星名", "繁中星名"],
             overlay="C-A09-02_緯度尺", overlay_layers=["天頂星層", "南十字層"],
             vo="方向有了，那到了沒？這就是 Hōkūleʻa 的用處：它會從夏威夷大島的正頭頂經過。"
                "船往北開，看它一晚比一晚高，等它正好掛在頭頂，就到了夏威夷的緯度。"
                "往南還有一把尺：南十字直立時，海面到十字底的高度，剛好等於十字本身的長度，"
                "大約六度——只有在夏威夷的緯度才會這樣。",
             note="北盤轉長圖→下移回南十字（＝06 倒放）；定格疊概念圖 C-A09-02（天頂星→南十字）"),
        dict(code="10", kind="Z", sec=21, north=True,
             frames=[CRUX, SCO_A, SCO],
             layers=["釣線"], labels=["夏威夷星名", "繁中星名"],
             vo="接著往東，夏天的 Manaiakalani，酋長的釣線。南半段就是天蠍座："
                "半神 Māui 的魚鉤，傳說他用它從海底釣起島嶼。七千公里外的紐西蘭，"
                "毛利人也叫它 Māui 的魚鉤，某些月份還叫它 Manaia ki te Rangi——lani 和 rangi 本是同一個字：天。",
             note="只開釣線（L7，藍）；往東（左）滑到天蠍（中段頁：夏威夷名）；迄格＝11 起格，唸到毛利時換成毛利標籤"),
        dict(code="11", kind="Z", sec=21, north=True,
             frames=[SCO, TRI],
             layers=["釣線"], labels=["毛利"], labels_end=["夏威夷星名", "繁中星名"],
             overlay="C-A09-03_航線與三角", overlay_layers=["島嶼層", "三角層"],
             vo="釣線往北，是三顆亮星組成的「引航三角」：天津四 Hawaiki、織女 Keoe、牛郎 Humu。"
                "航海協會把它看成玻里尼西亞三角——夏威夷、復活節島、紐西蘭，彼此相隔七千多公里。"
                "七夕那集的牛郎織女，在這裡撐起了一整片海。",
             note="起格（＝10 迄格）開毛利標籤；往北上移到引航三角；疊概念圖 C-A09-03（島嶼→玻里尼西亞三角）"),
        dict(code="12", kind="Z", sec=19, north=True,
             frames=[TRI, KITE],
             layers=["風箏"], labels=["夏威夷星名", "繁中星名"], labels_end=["四島"],
             vo="再往東，是秋天的 Ka Lupe o Kawelo，Kawelo 的風箏。風箏就是飛馬座大四邊形，"
                "四顆星各用一位大酋長命名：考艾的 Manōkalanipō、歐胡的 Kākuhihewa、"
                "茂宜的 Piʻilani、夏威夷島的 Keawe——一顆星，一座島。",
             note="只開風箏（L8，紫）；往東平移到飛馬大四邊形；迄格換成四島標籤"),
        dict(code="13", kind="Z", sec=25, north=True, cut=True,
             frames=[KOM, BAIL],
             layers=["舀水杓"], labels=["夏威夷星名", "繁中星名"],
             vo="最後一條，就是這個季節：Ke Kā o Makaliʻi，Makaliʻi 的舀水杓。"
                "從北端的五車二 Hōkūlei，經過雙子、南河三，彎到最亮的天狼星 ʻAʻā。"
                "勺子裡盛著獵戶座和昴宿星團——上個月的西伯利亞人說，那是打穀的人和鴨巢。"
                "舀水杓從東邊升起時盛滿星星，西沉時再倒回海裡。",
             note="【硬切】從風箏跳回右邊的舀水杓（只開 L5，琥珀）；推向獵戶與昴宿；迄格（＝14 起格）加西伯利亞標籤"),
        dict(code="14", kind="Z", sec=17, north=True,
             frames=[BAIL, PLE],
             layers=["舀水杓"], labels=["西伯利亞", "夏威夷星名", "繁中星名"],
             labels_end=["夏威夷星名", "繁中星名"],
             vo="昴宿還是夏威夷的新年鐘：每年十一月，Makaliʻi 在日落時從東方升起，"
                "Makahiki 季就開始了——四個月獻給豐收之神 Lono，停戰、競技、慶祝收成。"
                "今年在檀香山，大約就在十一月中。",
             note="推近昴宿（Makaliʻi）"),
        dict(code="15", kind="R", sec=18, north=True,
             frames=[(0.0, yp, 30.0, 0.0), (0.0, yp, 160.0, -179.9)],
             layers=["L4"], labels=["星線-盤"],
             vo="所以，說星線是玻里尼西亞人的 GPS，不太對。它不會告訴你「你在哪」，"
                "只教你兩件事：往哪走，還有到了沒。中間那一大段，靠航海家在腦子裡記著："
                "船開了多快、開了多久，一路算到島出現。",
             note="昴宿 → 回中心 → 上移 → 長圖轉北盤2 → 拉遠並逆時針轉到 −179.9°（約 12 小時）"),
        dict(code="16", kind="R", sec=13, north=True, cut=True,
             frames=[(0.0, yp, 160.0, 180.0), TPE],
             layers=["L4"], labels=[], horizon=[PHI_TPE],
             vo="今晚八點在台北抬頭：Kawelo 的風箏就掛在頭頂，西邊是引航三角，"
                "東方偏北，Makaliʻi 已經升起——舀水杓的季節，要開始了。",
             note=f"起格 180°＝15 迄格 −179.9°（同一個畫面；轉場設「無」，Canva 旋轉只收 ±180）→ "
                  f"繼續逆時針到 {ROT_TPE_C:+.1f}°（＝11/6 20:00 台北面向北方），"
                  f"拉近到 fov 116、山升到台北 25°N 地平線"),
        dict(code="17", kind="R", sec=9, north=True,
             frames=[TPE, (TPE[0], TPE[1], TPE[2], ROT_2020)],
             layers=["L4"], labels=[], horizon=[PHI_TPE],
             vo="下週五，往南到東加——南十字在那裡叫「南方的野鴨」。星星的名字，就是航線。",
             card="下集見｜東加：星星的名字就是航線",
             note="盤再轉 20 分鐘；端卡＋追蹤 CTA"),
    ]
    # 字數檢查：每格 ≤ 4.5 字/秒
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
            if sh["kind"] == "R":
                xt = m.xtN if sh["north"] else m.xtS
                yc = m.y_pole if sh["north"] else -m.y_pole
                which = ("北盤" if sh["north"] else "南盤") + "圖層組（置中）"
                ew = 2 * m.R_fill / fov * 1080
                off = (round(-(cx - xt) / fov * 1080), round((cy - yc) / fov * 1080))
            else:
                which = "大畫布圖層組"
                ew = 360.0 / fov * 1080
                off = (round(-cx / fov * 1080), round(cy / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"],
                         "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else "迄", "用檔": which,
                         "元素寬px": round(ew), "位移X px": off[0],
                         "位移Y px": off[1], "旋轉度": round(rot, 1),
                         "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w",
              encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w",
                          encoding="utf-8"), ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[{k: v for k, v in s.items()} for s in shots])

    terms = {}
    for h in HAW:
        terms[f"HIP {h}"] = dict(hips=[h], 原文=HAW[h], 拼音="", 英文翻譯=S[h][3] if len(S[h]) > 3 else "",
                                 中文=ZH.get(h, ""), 顏色=COLOR.get(h, "white"),
                                 來源備註="Stellarium hawaiian_starlines common_names（補 ʻokina／kahakō）")
    for k, (hips, hw, z, col, dx, dy) in GROUPS.items():
        terms[k] = dict(hips=hips, 原文=hw, 拼音="", 英文翻譯="", 中文=z, 顏色=col,
                        來源備註="Stellarium hawaiian_starlines（星群）")
    for k, (a, o, z, col) in LINES.items():
        terms["星線-" + k] = dict(hips=[], 原文=o, 拼音="", 英文翻譯="", 中文=z, 顏色=col,
                                 來源備註="Stellarium hawaiian_starlines description.md；PVS")
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms,
               "cross": [dict(原文="Te Matau a Māui", 中譯="Māui 的魚鉤（毛利，7–9 月）", 顏色="white"),
                         dict(原文="Manaia ki te Rangi", 中譯="天蠍座（毛利，4–6 月）", 顏色="white"),
                         dict(原文="Утиное гнездо", 中譯="鴨巢（西伯利亞，A-08）", 顏色="white"),
                         dict(原文="Кичиги", 中譯="打穀者（西伯利亞，A-08）", 顏色="white")],
               "mains": MAINS,
               "lines": {"L4": "星座連線", "舀水杓": "連線-舀水杓", "脊椎骨": "連線-脊椎骨",
                         "釣線": "連線-釣線", "風箏": "連線-風箏", "指針": "連線-指針"},
               "line_groups": {"L4": LG_ALL, "舀水杓": LG_KOM, "脊椎骨": LG_IWI,
                               "釣線": LG_MAN, "風箏": LG_LUP, "指針": LG_PTR},
               "lst_tpe_2000": LST_TPE_2000},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    lg_all = LG_ALL + LG_PTR
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=lg_all,
                  labels=[dict(it, pt=6) for it in items],
                  title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, lg_all)
    m.sb_grid(os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), shots, line_groups=LG_ALL,
              labels=[dict(it, pt=5) for it in haw + zh],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）"
                    f"　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
