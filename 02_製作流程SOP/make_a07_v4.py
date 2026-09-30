# -*- coding: utf-8 -*-
"""A-07 蒙古：整片天空拴在一根金樁上｜大畫布 v4.6

輸出：L1銀河 L2星點 L3經緯線 L4星座連線 L5連線-指極線 L6連線-Stellarium三雄鹿
      L7主角星白點 L8主角星白圈（v4.6 新增：疊在連線上，美宣不必再手點白點）
      L9…標籤：英文／繁中／蒙古原文／蒙古拼音／生肖-循環版／生肖-折返版／
      本命星君／Stellarium錯置／跨文化原文／跨文化中譯
      ＋ 南北盤圖層組（同結構）/ 預覽黑底 / SB-分鏡 / SB-鏡頭牆 / 鏡頭清單
      ＋ {EP}_標籤資料.json（給 gen_canva_pages.py 出 Canva 逐頁製作表用）
執行：python3 make_a07_v4.py

參數（見 星圖呈現規格_v4_大畫布.md 肆）
  lst = 322 → 北走廊（x=0）＝RA 322，從金樁沿銀河（仙王—天鵝交界）往下，
              天津四 x=+11.6：T「沿著天空的縫線往下」一鏡到底
              獵戶腰帶在 x −122（S 往東平移＝時間往後）；畫布左右接縫落在
              RA 142（長蛇座頭，本集不用）
              ★ 為什麼不是 305：鏡頭 14 要從 0° 轉到「10/2 20:00 面向北方」，
                lst=305 需逆時針 187.6°（>180°，Canva M&M 可能走最短路徑反轉＝時間倒流）；
                lst=322 只要 −170.6°，單一 M&M 方向明確
  D_s = 45 → 帶內容夏季大三角（Altair +8.9…Deneb +45.3）與獵戶腰帶（−1.9…−0.3）
  D_r = 49 → 北斗最南 Alkaid +49.31 剛好整把勺在盤上；仙后 W（+56…+63）在盤上
  D_fill=0 → k=1.397、R_fill=125.771；盤寬 ÷ 畫布寬 ＝ 0.698728（同 A-02/05/06）
  x_tN = 0 → 走廊置中，Canva 盤對位可「水平置中＋對齊上緣」

⚠ 資料來源修正（本集論點之一，逐字稿 11–12 鏡）：
  Stellarium mongolian 把 Gurvan Maral Od（三頭鹿）畫在夏季大三角；
  蒙古語辭典與傳說（奧伊拉特口傳）＝獵戶座腰帶。本檔兩者都畫：
  正確的畫在 L4（琥珀），Stellarium 的畫在獨立的 L6（紅），可單獨開關。
"""
import os, sys, json, math, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, R_RIM

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-07"
OUT = os.path.join(BASE, "05_素材/A-07_蒙古/_v4大畫布")
PHI, LST0 = 47.9, 322.0            # PHI＝烏蘭巴托緯度（僅 L_horizon 用，預設不出）
LST_TPE_2000 = 312.6               # 2026/10/02 20:00 台北的地方恆星時（自算，見逐字稿考據）

# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
DUB, MER, PHE, MEG, ALI, MIZ, ALK = 54061, 53910, 58001, 59774, 62956, 65378, 67301
ALC, POL = 65477, 11767
DIPPER = [DUB, MER, PHE, MEG, ALI, MIZ, ALK]
CAPH, SCHEDAR, NAVI, RUCHBAH, SEGIN = 746, 3179, 4427, 6686, 8886
DENEB, SADR, ALBIREO, GIENAH = 102098, 100453, 95947, 102488
VEGA, ALTAIR = 91262, 97649
MINTAKA, ALNILAM, ALNITAK = 25930, 26311, 26727
BETELGEUSE, RIGEL, ALCYONE = 27989, 24436, 17702
BELT = [MINTAKA, ALNILAM, ALNITAK]

MAINS = DIPPER + [ALC, POL, VEGA, ALTAIR, DENEB, SCHEDAR, CAPH] + BELT

# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium mongolian index.json 原樣＋本集修正）
# ══════════════════════════════════════════════════════════════════
def mongolian_lines():
    p = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master/"
                           "mongolian/index.json")
    d = json.load(open(p, encoding="utf-8"))
    return {c["id"].split()[-1]: c["lines"] for c in d["constellations"]}


ML = mongolian_lines()
SEG_BUDDHAS = ML["003"]               # Долоон бурхан 七佛（北斗）
SEG_BOW = ML["001"]                   # Нум сум 弓與箭（Stellarium：天鵝座）
SEG_WOMAN = ML["002"]                 # Хүн таван од 五顆星的人（仙后 W）
SEG_STAGS_STELLARIUM = ML["004"]      # Stellarium：三雄鹿＝夏季大三角（錯置）
SEG_DEER = [BELT]                     # 蒙古傳統：Гурван марал＝獵戶腰帶（本集修正）
SEG_POINTER = [[MER, DUB, POL]]       # 指極線：勺口兩星延長 5.3 倍到金樁

LG_MAIN = [(SEG_BUDDHAS, "amber", 1.0), (SEG_BOW, "green", 1.0),
           (SEG_WOMAN, "purple", 1.0), (SEG_DEER, "amber", 1.0)]
LG_POINTER = [(SEG_POINTER, "blue", 1.0)]
LG_STELLARIUM = [(SEG_STAGS_STELLARIUM, "red", 1.0)]


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


def uniq(seglists):
    return sorted({h for segs in seglists for seg in segs for h in seg})


# ══════════════════════════════════════════════════════════════════
# 三、名詞總表（＝標籤對照表的來源；給不會中文的組員直接複製貼上）
#   key: (錨點 HIP 或 HIP 群, 原文, 拼音, 英文翻譯, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = {
    "北斗-佛": (DIPPER, "Долоон бурхан", "Doloon Burkhan", "Seven Buddhas / Seven Gods",
               "七尊佛", "amber", "Stellarium mongolian CON 003；бурхан＝佛、神"),
    "北斗-老人": (DIPPER, "Долоон өвгөн", "Doloon Övgön", "Seven Old Men",
                "七位老人", "amber", "蒙古語別名（Wiktionary: Big Dipper）"),
    "金樁": ([POL], "Алтан гадас", "Altan Gadas", "Golden Stake (tethering peg)",
           "金樁", "blue", "蒙古通行寫法 Алтан гадас；Stellarium 拼作 Altan Hadaas（хадаас＝釘子），其 zh_TW 譯「黃金賭注」是誤譯"),
    "弓箭": (uniq([SEG_BOW]), "Нум сум", "Num Sum", "Bow and Arrow",
           "弓與箭", "green", "Stellarium mongolian CON 001（天鵝座）；僅此一來源"),
    "五星人": (uniq([SEG_WOMAN]), "Хүн таван од", "Khün Tavan Od", "Five-Star Person",
            "五顆星的人", "purple", "Stellarium 譯 Five Stars Woman；хүн＝人"),
    "三頭鹿": (BELT, "Гурван марал", "Gurvan Maral", "Three (Red) Deer, female",
            "三頭鹿", "amber", "＝獵戶座腰帶（蒙古語辭典、Хөхдэй мэргэн 傳說）；марал＝母鹿；Stellarium 錯置在夏季大三角且譯作雄鹿"),
    "銀河": (None, "Тэнгэрийн заадас", "Tengeriin Zaadas", "Seam of the Sky",
           "天空的縫線", "white", "蒙古語銀河；заадас＝縫線"),
    "昴": ([ALCYONE], "Мичид", "Michid", "the Pleiades", "昴", "white",
          "蒙古語昴星團（牧民季節曆）；只上標籤不唸"),
}
MW_ANCHOR = (324.0, 47.0)            # 銀河標籤錨點（天鵝—仙王之間，北走廊正中）

# ══════════════════════════════════════════════════════════════════
# 四、跨文化（北斗）——逐字稿第 09 鏡唸到的七個＋蒙古自己
# ══════════════════════════════════════════════════════════════════
CROSS = [
    ("Долоон бурхан", "七尊佛（蒙古）", "amber"),
    ("Лось", "駝鹿（西伯利亞）", "white"),
    ("Tukturjuit", "馴鹿（因紐特）", "white"),
    ("بنات نعش", "抬棺架的女兒們（阿拉伯）", "white"),
    ("Karlvagn", "男人的車（北歐）", "white"),
    ("Seven Brothers and Their Sister", "七兄弟和妹妹（黑腳族）", "white"),
    ("Sos Sette Frades", "七兄弟（薩丁尼亞）", "white"),
]

# ══════════════════════════════════════════════════════════════════
# 五、生肖本命星（兩個版本）＋ 台灣本命星君
# ══════════════════════════════════════════════════════════════════
ZOD_LOOP = {DUB: "鼠・羊", MER: "牛・猴", PHE: "虎・雞", MEG: "兔・狗",
            ALI: "龍・豬", MIZ: "蛇", ALK: "馬"}            # Stellarium（從頭再數）
ZOD_SWING = {DUB: "鼠", MER: "牛・豬", PHE: "虎・狗", MEG: "兔・雞",
             ALI: "龍・猴", MIZ: "蛇・羊", ALK: "馬"}         # 北斗經（折返）
XINGJUN = {DUB: "貪狼", MER: "巨門", PHE: "祿存", MEG: "文曲",
           ALI: "廉貞", MIZ: "武曲", ALK: "破軍"}
ZH_STAR = {DUB: "天樞", MER: "天璇", PHE: "天璣", MEG: "天權", ALI: "玉衡",
           MIZ: "開陽", ALK: "搖光", ALC: "輔", POL: "北極星（勾陳一）",
           VEGA: "織女", ALTAIR: "牛郎（河鼓二）", DENEB: "天津四",
           BETELGEUSE: "參宿四", RIGEL: "參宿七"}
EN_STAR = {DUB: "Dubhe", MER: "Merak", PHE: "Phecda", MEG: "Megrez", ALI: "Alioth",
           MIZ: "Mizar", ALK: "Alkaid", ALC: "Alcor", POL: "Polaris",
           VEGA: "Vega", ALTAIR: "Altair", DENEB: "Deneb",
           BETELGEUSE: "Betelgeuse", RIGEL: "Rigel"}
STAR_COLOR = {h: "amber" for h in DIPPER}
STAR_COLOR.update({ALC: "white", POL: "blue", VEGA: "white", ALTAIR: "white",
                   DENEB: "white", SCHEDAR: "purple", CAPH: "purple",
                   ALNITAK: "amber", ALNILAM: "amber", MINTAKA: "amber",
                   BETELGEUSE: "white", RIGEL: "white"})

# 標籤偏移（畫布單位；北斗在北盤右上、斗口朝金樁）。預覽＝SVG，看到重疊就是真重疊。
SIDE_OUT = {MER: "上", PHE: "上", DUB: "左", MEG: "右", ALI: "左下", MIZ: "左下",
            ALK: "下"}                                  # 生肖／星名：勺子外側
SIDE_IN = {MER: "左", PHE: "右", DUB: "下", MEG: "左上", ALI: "右上", MIZ: "上",
           ALK: "上"}                                   # 本命星君：另一側
OFF_STAR = {DUB: (0.0, 2.2), MER: (2.8, -1.8), PHE: (3.0, -1.6), MEG: (0.0, 2.2),
            ALI: (0.0, 2.2), MIZ: (-2.6, 1.8), ALK: (0.0, 2.2), ALC: (2.2, 1.6),
            POL: (0.0, -2.4), VEGA: (0.0, 2.4), ALTAIR: (0.0, -2.4),
            DENEB: (0.0, 2.4), ALNITAK: (0.0, -2.4), ALNILAM: (0.0, 2.4),
            MINTAKA: (0.0, -2.4), BETELGEUSE: (0.0, 2.4), RIGEL: (0.0, -2.4),
            SCHEDAR: (0.0, -2.2), CAPH: (0.0, 2.2)}
OFF_TERM = {"北斗-佛": (14.0, 11.2), "北斗-老人": (14.0, 5.6), "金樁": (0.0, 5.6),
            "弓箭": (-22.0, -4.0), "五星人": (-4.0, -7.0), "三頭鹿": (0.0, 6.4),
            "銀河": (0.0, 0.0), "昴": (0.0, 3.6)}
TERM_DY2 = -2.4        # 中譯／拼音放在原文正下方（可與原文同時開）


def build():
    S = G.load_stars(BASE)
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=45, D_r=49, D_fill=0,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=PHI,
               maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")

    def anchor(key):
        hips = TERMS[key][0]
        if hips is None:
            return {"ra": MW_ANCHOR[0], "dec": MW_ANCHOR[1]}
        if len(hips) == 1:
            return {"hip": hips[0]}
        ra, dec = centroid(hips, S)
        return {"ra": ra, "dec": dec}

    def term_items(field, size=1.35):
        idx = {"mn": 1, "rom": 2, "en": 3, "zh": 4}[field]
        out = []
        for k, t in TERMS.items():
            dx, dy = OFF_TERM[k]
            if field != "mn":
                dy += TERM_DY2
            out.append(dict(anchor(k), text=t[idx], color=t[5], size=size,
                            dx=dx, dy=dy, key=k))
        return out

    def star_items(table, off, size=1.05, color=None, side=None):
        out = []
        for h in table:
            if h not in S:
                continue
            dx, dy = off.get(h, (0.0, 2.2)) if off else (0.0, 2.2)
            if side and h in side:
                w, hh = MC.label_box(table[h], size, m.fu)
                sd = side[h]
                dx = {"左": -(w / 2 + 1.1), "右": w / 2 + 1.1}.get(sd[0], 0.0)
                dy = {"上": hh / 2 + 0.9, "下": -(hh / 2 + 0.9)}.get(sd[-1], 0.0)
                if len(sd) == 2:                                   # 斜角：各退一點
                    dx = {"左": -(w / 2 + 0.6), "右": w / 2 + 0.6}[sd[0]]
                    dy = {"上": hh / 2 + 0.5, "下": -(hh / 2 + 0.5)}[sd[1]]
            out.append({"hip": h, "text": table[h],
                        "color": color or STAR_COLOR.get(h, "white"),
                        "size": size, "dx": round(dx, 2), "dy": round(dy, 2),
                        "key": f"HIP {h}"})
        return out

    eng = star_items(EN_STAR, OFF_STAR, side=SIDE_OUT)
    zh = star_items(ZH_STAR, OFF_STAR, side=SIDE_OUT) + term_items("zh", 1.25)
    mn = term_items("mn")
    rom = term_items("rom", 1.2)
    # 生肖（兩版同位置、逐格切換）放勺子外側；本命星君放另一側，可與折返版同開
    zloop = star_items(ZOD_LOOP, None, 1.2, "white", side=SIDE_OUT)
    zswing = star_items(ZOD_SWING, None, 1.2, "white", side=SIDE_OUT)
    xj = star_items(XINGJUN, None, 1.1, "amber", side=SIDE_IN)
    wrong = [dict(zip(("ra", "dec"), centroid(uniq([SEG_STAGS_STELLARIUM]), S)),
                  text="Stellarium：三頭雄鹿？", color="red",
                  size=1.3, dx=-18.0, dy=-20.0, key="Stellarium錯置")]
    dra, ddec = centroid(DIPPER, S)
    cross_o, cross_z = [], []
    for i, (nat, zhn, col) in enumerate(CROSS):
        base = dict(ra=dra, dec=ddec, color=col, dx=-36.0, key=f"跨文化{i+1}")
        cross_o.append(dict(base, text=nat, size=1.2, dy=24.0 - 5.6 * i))   # 原文在上
        cross_z.append(dict(base, text=zhn, size=0.95, dy=21.8 - 5.6 * i))  # 中譯在下

    label_sets = [(eng, "英文"), (zh, "繁中"), (mn, "蒙古原文"), (rom, "蒙古拼音"),
                  (zloop, "生肖-循環版"), (zswing, "生肖-折返版"), (xj, "本命星君"),
                  (wrong, "Stellarium錯置"), (cross_o, "跨文化原文"),
                  (cross_z, "跨文化中譯")]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_MAIN)
    m.L_lines(LG_POINTER, name="連線-指極線")
    m.L_lines(LG_STELLARIUM, name="連線-Stellarium三雄鹿")
    m.L_marks(MAINS, "主角星白點", "dot")
    m.L_marks(MAINS, "主角星白圈", "ring")
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_MAIN, label_sets, mains=MAINS,
                  line_sets=[(LG_POINTER, "連線-指極線"),
                             (LG_STELLARIUM, "連線-Stellarium三雄鹿")],
                  marks=[(MAINS, "主角星白點", "dot"), (MAINS, "主角星白圈", "ring")])

    # ════════════════════ 鏡頭 ════════════════════
    yp = m.y_pole

    def P(h):
        return m.pos_primary(*S[h][:2])

    def mid(a, b, t=0.5):
        return (a[0] * (1 - t) + b[0] * t, a[1] * (1 - t) + b[1] * t)

    pole = (0.0, yp)
    dips = [P(h) for h in DIPPER]
    dipc = (sum(p[0] for p in dips) / 7, sum(p[1] for p in dips) / 7)
    dpc = mid(pole, dipc, 0.62)
    ptr = mid(P(MER), pole, 0.45)
    belt = P(ALNILAM)
    tp = [P(h) for h in (DENEB, VEGA, ALTAIR)]
    tri = (sum(p[0] for p in tp) / 3, sum(p[1] for p in tp) / 3 + 4.0)
    ROT_20 = -((LST_TPE_2000 + 180.0 - LST0) % 360.0)   # 盤轉到「10/2 20:00 面向北方」
    ROT_2030 = ROT_20 - 7.52                           # 再過 30 分鐘（15.041°/h）

    shots = [
        dict(code="01", kind="Z", sec=12, north=True,
             frames=[(dpc[0], dpc[1], 78.0, 0.0), (dpc[0], dpc[1], 66.0, 0.0)],
             layers=["L4"], labels=[],
             vo="上週五，我們跟著月亮走過二十八間房。今晚往北，走上草原。"
                "同一片星空，蒙古人看見——七位老人。",
             card="同一片星空，蒙古人看見——七位老人",
             note="統一開頭：北斗＋金樁同框，七佛連線亮起"),
        dict(code="02", kind="Z", sec=16, north=True,
             frames=[(dipc[0], dipc[1], 60.0, 0.0), (dipc[0], dipc[1], 52.0, 0.0)],
             layers=["L4"], labels=["蒙古原文", "繁中"],
             vo="北斗七星，蒙古人叫它 Долоон өвгөн，七位老人；更常叫的名字是 "
                "Долоон бурхан——七尊佛。直到今天，還有人早晚灑一點奶敬它。",
             note="兩個名字依序疊字（L 蒙古原文＋繁中）"),
        dict(code="03", kind="Z", sec=22, north=True,
             frames=[(dpc[0], dpc[1], 64.0, 0.0), (dpc[0], dpc[1], 56.0, 0.0)],
             layers=["L4"], labels=["繁中"],
             vo="傳說有八個孤兒兄弟，從怪物手裡救回了王后。國王把一支金箭拋上天："
                "誰接到，就歸誰。最小的弟弟接住了，變成北極星；七個哥哥變成北斗，"
                "每天晚上都來看他。",
             note="八兄弟傳說：金樁（北極星）亮起＝最小的弟弟"),
        dict(code="04", kind="Z", sec=16, north=True,
             frames=[(ptr[0], ptr[1], 54.0, 0.0), (ptr[0], ptr[1], 48.0, 0.0)],
             layers=["L4", "指極線"], labels=["蒙古原文", "繁中"],
             vo="北極星的蒙古名字叫 Алтан гадас，金樁——гадас 是打進草原土裡、"
                "拴牲口的木樁。找它很簡單：勺口這兩顆星的距離拉長五倍多，就撞到金樁。",
             note="指極線（藍）由天璇→天樞畫向金樁：28.7° ÷ 5.37° ＝ 5.3 倍"),
        dict(code="05", kind="Z", sec=24, north=True,
             frames=[(dipc[0], dipc[1], 58.0, 0.0), (dipc[0], dipc[1], 52.0, 0.0)],
             layers=["L4"], labels=["生肖-循環版"],
             vo="蒙古人還把十二生肖，掛上了這七顆星。從勺口的天樞開始：鼠、牛、虎、兔、"
                "龍、蛇，一路數到斗柄尾端的搖光——馬。今年二〇二六是馬年，"
                "今年出生的孩子，本命星就是搖光。",
             note="七顆星逐一亮起（天樞→搖光），只露前七個生肖；搖光＋「2026 馬年」字卡"),
        dict(code="06", kind="Z", sec=20, north=True,
             frames=[(dipc[0], dipc[1], 52.0, 0.0), (dipc[0], dipc[1], 52.0, 0.0)],
             layers=["L4"], labels=["生肖-循環版"], labels_end=["生肖-折返版"],
             overlay="C-A07-01_生肖本命星兩個版本",
             vo="明年羊年，版本就分家了。Stellarium 記的是從頭再數：羊回到天樞。"
                "蒙古文的《北斗七星經》，還有今天蒙古人拜星的說法，卻是折返：羊在開陽、"
                "猴在玉衡，一路退回去，豬落在天璇。",
             note="起格＝循環版（Stellarium），唸到「北斗經」時換成迄格＝折返版；"
                  "同時疊概念圖 C-A07-01 左右對照"),
        dict(code="07", kind="Z", sec=20, north=True,
             frames=[(dipc[0], dipc[1], 56.0, 0.0), (dipc[0], dipc[1], 52.0, 0.0)],
             layers=["L4"], labels=["生肖-折返版", "本命星君"],
             vo="這個折返版，你可能在台灣廟裡見過。禮斗、點本命星燈，查的就是同一張表："
                "屬鼠拜貪狼，屬馬拜破軍。同一張表也寫在佛教的《北斗七星延命經》裡；"
                "唐代以後它傳到日本、韓國，也譯成了藏文和蒙古文。",
             note="本命星君（貪狼…破軍）疊在折返版生肖旁"),
        dict(code="08", kind="Z", sec=22, north=True,
             frames=[(dipc[0], dipc[1], 58.0, 0.0), (dipc[0], dipc[1], 50.0, 0.0)],
             layers=["L4"], labels=["繁中"],
             overlay="C-A07-02_七兄弟不是一家人",
             vo="但這七兄弟，其實不是一家人。量過距離：中間五顆都在八十光年上下，"
                "一起誕生、朝同一個方向走；天樞一百二十三光年、搖光一百零四光年，"
                "只是剛好路過。大約五萬年後，這把勺子就認不出來了。",
             note="疊概念圖 C-A07-02（距離＋運動方向）"),
        dict(code="09", kind="Z", sec=18, north=True,
             frames=[(dipc[0] - 14.0, dipc[1] - 8.0, 80.0, 0.0),
                     (dipc[0] - 14.0, dipc[1] - 8.0, 74.0, 0.0)],
             layers=["L4"], labels=["跨文化原文", "跨文化中譯"],
             vo="同一把勺子，換片土地就換了故事。西伯利亞看見駝鹿，因紐特看見馴鹿，"
                "阿拉伯看見抬著棺架的女兒們，北歐看見一輛車。黑腳族和薩丁尼亞，"
                "看見的也是七兄弟。",
             note="跨文化堆疊（原文／中譯兩層同位置，交替或同開）"),
        dict(code="10", kind="T", sec=14, north=True,
             frames=[(0.0, yp, 48.0, 0.0), (0.0, 34.0, 48.0, 0.0)],
             layers=["L4"], labels=["蒙古原文"],
             vo="Stellarium 收的蒙古星座不多。沿著金樁往下，是銀河——蒙古人叫它 "
                "Тэнгэрийн заадас，天空的縫線。",
             note="【硬切】到金樁置中，沿北走廊（RA 305＝銀河）往下到天鵝座"),
        dict(code="11", kind="Z", sec=20, north=True,
             frames=[(tri[0] - 4.0, tri[1], 64.0, 0.0), (20.0, 6.0, 40.0, 0.0)],
             layers=["L4", "Stellarium三雄鹿"], labels=["繁中", "Stellarium錯置"],
             vo="Stellarium 的蒙古資料，在縫線上畫了一把弓、一支箭，Нум сум；"
                "旁邊這三顆亮星——七夕那集的織女、牛郎、天津四——它說是三頭雄鹿。",
             note="弓箭（綠）＋紅色三角（Stellarium 錯置）＋紅字問號；迄格收到 S 安全框"),
        dict(code="12", kind="S", sec=24, north=True,
             frames=[(20.0, 6.0, 40.0, 0.0), (belt[0], 2.0, 40.0, 0.0)],
             layers=["L4"], labels=["蒙古原文", "繁中"],
             vo="但我們翻了蒙古自己的辭典和傳說：三頭鹿不在這裡。Гурван марал，"
                "是獵戶座的腰帶。蒙古的傳說裡，有個神射手追著三頭鹿，一路追上了天。",
             note="紅三角刪除（本頁起不放 L6）→ 往東（左）平移到獵戶腰帶；"
                  "途經昴星團（Мичид 標籤）"),
        dict(code="13", kind="T", sec=10, north=True,
             frames=[(0.0, 20.0, 48.0, 0.0), (0.0, yp, 48.0, 0.0)],
             layers=["L4"], labels=[],
             vo="最後，回到北方，回到那根樁。",
             note="【硬切】回北走廊，沿銀河抬頭到金樁；迄格＝14 起格（長圖轉北盤）"),
        dict(code="14", kind="R", sec=26, north=True,
             frames=[(0.0, yp, 48.0, 0.0), (-8.0, yp, 116.0, ROT_20)],
             layers=["L4"], labels=[],
             vo="整片天空繞著金樁轉。七個哥哥也繞著它，像被拴住的馬，繞著樁子走了一整夜。"
                "現在停下來的，是十月二日晚上八點、面向北方的天空。",
             note=f"從「長圖轉北盤1」（與 13 迄格同框換組）→ 逆時針 {ROT_20:+.1f}°"
                  f"（{-ROT_20/15.041:.1f} 小時）＋拉遠到 fov 116（盤心略偏右，斗柄不出框）。"
                  "【驗證器 ⚠ 已判斷可接受】迄格含填滿環，之後全留在盤圖層組、不切回大畫布"),
        dict(code="15", kind="R", sec=20, north=True,
             frames=[(-8.0, yp, 116.0, ROT_20), (-8.0, yp, 116.0, ROT_20)],
             layers=["L4"], labels=["蒙古原文"], horizon=[47.9, 25.03],
             vo="在烏蘭巴托，金樁掛在四十八度高，北斗整夜不落，七兄弟天天到齊。"
                "在台北，金樁只有二十五度；十月初晚上七點，斗口已經貼著西北地平線，"
                "八點多就沉下去了。",
             note="盤不動；山的剪影從烏蘭巴托高度升到台北高度（Match & Move），"
                  "位置見逐頁製作表「地平線」欄"),
        dict(code="16", kind="R", sec=16, north=True,
             frames=[(-8.0, yp, 116.0, ROT_20), (-8.0, yp, 116.0, ROT_2030)],
             layers=["L4"], labels=[], horizon=[25.03],
             vo="在一個會搬家的世界裡，他們把整片天空，拴在一根不動的樁上。"
                "下週五再往北：同一條腰帶，西伯利亞人看見的不是鹿，是打穀的人。",
             card="EP8 西伯利亞：駝鹿、鴨巢與打穀者",
             note="盤再轉 30 分鐘；端卡＋追蹤 CTA"),
    ]
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
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {sum(s['sec'] for s in shots)} 秒）")
    m.save_manifest(shots=[{k: v for k, v in s.items()} for s in shots])

    # 給逐頁製作表用：每一層標籤的每一條（含錨點、偏移、顏色、字級）＋名詞總表
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": {k: dict(zip(("hips", "原文", "拼音", "英文翻譯", "中文",
                                      "顏色", "來源備註"), v)) for k, v in TERMS.items()},
               "cross": [dict(zip(("原文", "中譯", "顏色"), c)) for c in CROSS],
               "mains": MAINS,
               "lines": {"L4": "星座連線", "指極線": "連線-指極線",
                         "Stellarium三雄鹿": "連線-Stellarium三雄鹿"},
               "line_groups": {"L4": LG_MAIN, "指極線": LG_POINTER,
                               "Stellarium三雄鹿": LG_STELLARIUM},
               "lst_tpe_2000": LST_TPE_2000},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    lg_all = LG_MAIN + LG_POINTER + LG_STELLARIUM
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=lg_all,
                  labels=[dict(it, pt=6) for it in items],
                  title=f"{EP}　大畫布 v4.6（{name}標籤）")
    storyboard(m, shots, lg_all)
    m.sb_grid(os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), shots, line_groups=LG_MAIN,
              labels=[dict(it, pt=5) for it in zh],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）"
                    f"　總長 {sum(s['sec'] for s in shots)} 秒")
    print("\n完成 →", OUT)


def storyboard(m, shots, lg):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, FancyArrowPatch, Arc
    FP = G.find_font()
    x0, y0, x1, y1 = m.extent
    W = 16.0
    f = plt.figure(figsize=(W, W * (y1 - y0) / (x1 - x0)), dpi=110)
    f.patch.set_facecolor(MC.COLORS["bg"])
    ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    ax.set_aspect("equal"); ax.axis("off")
    m.draw_mpl(ax, lg)
    AC, PA = "#FF6B6B", "#FFC94A"
    for sh in shots:
        frs = sh["frames"]
        if sh["kind"] == "R":
            yc = m.y_pole if sh["north"] else -m.y_pole
            xt = m.xtN if sh["north"] else m.xtS
            fov = frs[0][2]; hw, hh = fov / 2, fov * 8 / 9
            ax.add_patch(Rectangle((frs[0][0] - hw, frs[0][1] - hh), 2 * hw,
                                   2 * hh, fill=False, lw=1.8, ec=AC, zorder=10))
            r0, r1 = frs[0][3], frs[-1][3]
            rr = fov * .3
            if abs(r1 - r0) > 0.1:
                ax.add_patch(Arc((xt, yc), rr * 2, rr * 2,
                                 theta1=min(90 - r0, 90 - r1),
                                 theta2=max(90 - r0, 90 - r1), color=PA, lw=2.0,
                                 ls=(0, (6, 4)), zorder=11))
            ax.text(frs[0][0], frs[0][1] - hh - 3,
                    f"{sh['code']}　盤組旋轉 {r1-r0:+.0f}°", fontproperties=FP,
                    fontsize=10, color=PA, ha="center", va="top",
                    weight="bold", zorder=12)
            continue
        for i, (cx, cy, fov, rot) in enumerate(frs):
            hw, hh = fov / 2, fov * 8 / 9
            last = i == len(frs) - 1
            ax.add_patch(Rectangle((cx - hw, cy - hh), 2 * hw, 2 * hh, fill=False,
                                   lw=1.8 if not last else 1.4,
                                   ls="-" if not last else (0, (5, 4)),
                                   ec=AC, zorder=10))
            ax.text(cx, cy + hh - 3, f"{sh['code']}{'起' if i == 0 else '迄'}",
                    fontproperties=FP, fontsize=9, color=AC, ha="center",
                    va="top", weight="bold", zorder=12)
        a, b = (frs[0][0], frs[0][1]), (frs[-1][0], frs[-1][1])
        if math.hypot(b[0] - a[0], b[1] - a[1]) > 2:
            ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=16,
                                         lw=1.8, ls=(0, (6, 4)), color=PA, zorder=11,
                                         shrinkA=0, shrinkB=0))
    ax.text(x0 + 3, y1 - 3, f"{EP}　分鏡（v4.6 單一大畫布）", fontproperties=FP,
            fontsize=14, color="#FFFFFF", ha="left", va="top", weight="bold",
            zorder=13)
    fn = os.path.join(OUT, f"{EP}_SB-分鏡.png")
    f.savefig(fn, facecolor=MC.COLORS["bg"]); plt.close(f)
    print(f"  ✓ {os.path.basename(fn)}")


if __name__ == "__main__":
    build()
