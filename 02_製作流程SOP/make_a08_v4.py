# -*- coding: utf-8 -*-
"""A-08 西伯利亞：一場永不結束的狩獵｜大畫布 v4.6

輸出：L1銀河 L2星點 L3經緯線 L4星座連線 L5連線-小駝鹿 L6連線-獵人
      L7主角星白點 L8主角星白圈
      L9…標籤：英文／繁中／俄文原文／俄文拼音／埃文基原文／埃文基中譯／追獵角色／
      金樁原文／金樁中譯／銀河-鵝之路／銀河-馬麥之路／昴-別名／歐俄
      ＋ 南北盤圖層組 / 預覽黑底 / SB-分鏡 / SB-鏡頭牆 / 鏡頭清單 / 標籤資料
執行：python3 make_a08_v4.py

參數
  lst = 50 → 北走廊（x=0）＝RA 50：金樁沿英仙座銀河（鵝之路）往下，
             一路到昴宿（鴨巢 x −6.9）；獵戶腰帶（打穀者）在 x −34，往東（左）平移就到。
             北斗（駝鹿）在盤的左上方、斗柄朝上。畫布左右接縫落在 RA 230（牧夫座南，本集不用）。
             鏡頭 16 轉到「10/9 20:00 台北面向北方」只要逆時針 −89.7°（< 180°，方向明確）。
  D_s = 45、D_r = 49、D_fill = 0 → 同 A-07：k=1.397、R_fill=125.771、盤寬 ÷ 畫布寬 ＝ 0.698728
  x_tN = 0

資料：Stellarium siberian（index.json 原樣：Elk、Duck Nest；Threshers 只畫腰帶三顆——
      description 說「西伯利亞人通常只用腰帶三顆星」，index.json 的線多連了寶劍 ι Ori、HIP 26268）
"""
import os, sys, json, math, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-08"
OUT = os.path.join(BASE, "05_素材/A-08_西伯利亞/_v4大畫布")
PHI, LST0 = 64.27, 50.0            # PHI＝圖拉（埃文基自治區首府）緯度（鏡頭 16–17 地平線）
LST_TPE_2000 = 319.69              # 2026/10/09 20:00 台北的地方恆星時（自算，見逐字稿考據）
PHI_TPE = 25.03

# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
DUB, MER, PHE, MEG, ALI, MIZ, ALK = 54061, 53910, 58001, 59774, 62956, 65378, 67301
ALC, POL = 65477, 11767
DIPPER = [DUB, MER, PHE, MEG, ALI, MIZ, ALK]
BOWL, HANDLE = [DUB, MER, PHE, MEG], [ALI, MIZ, ALK]
KOCHAB, PHERKAD = 72607, 75097
MINTAKA, ALNILAM, ALNITAK = 25930, 26311, 26727
BELT = [MINTAKA, ALNILAM, ALNITAK]
BETELGEUSE, RIGEL = 27989, 24436
ALCYONE, ELECTRA, MAIA, MEROPE, ATLAS, TAYGETA = 17702, 17499, 17573, 17608, 17847, 17531
MIRFAK, ALGOL, CAPELLA = 15863, 14576, 24608
SCHEDAR, CAPH = 3179, 746

MAINS = DIPPER + [ALC, POL, KOCHAB, PHERKAD, ALCYONE, BETELGEUSE, RIGEL, MIRFAK,
                  CAPELLA, SCHEDAR] + BELT


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium siberian index.json＋小熊座 western）
# ══════════════════════════════════════════════════════════════════
def sc_lines(culture):
    p = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master/"
                           f"{culture}/index.json")
    d = json.load(open(p, encoding="utf-8"))
    return {c["id"].split()[-1]: c["lines"] for c in d["constellations"]}


SL = sc_lines("siberian")
SEG_ELK = SL["Elk"]                   # Лось 駝鹿（北斗；Stellarium 多連一段回天權）
SEG_NEST = SL["DNe"]                  # Утиное гнездо 鴨巢（昴宿一圈）
SEG_THRESH = [BELT]                   # Кичиги 打穀者：腰帶三顆（見檔頭說明）
SEG_CALF = sc_lines("western")["UMi"]  # 小熊座＝小駝鹿（埃文基母駝鹿與小駝鹿的版本）
SEG_HUNTERS = [HANDLE]                # 斗柄三顆＝獵人

LG_MAIN = [(SEG_ELK, "amber", 1.0), (SEG_NEST, "amber", 1.0), (SEG_THRESH, "amber", 1.0)]
LG_CALF = [(SEG_CALF, "blue", 0.9)]
LG_HUNT = [(SEG_HUNTERS, "green", 1.0)]


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


def uniq(seglists):
    return sorted({h for segs in seglists for seg in segs for h in seg})


# ══════════════════════════════════════════════════════════════════
# 三、名詞總表（＝標籤對照表；給不會中文、不會西里爾字母的組員直接複製貼上）
#   key: (錨點 HIP 群 或 (ra,dec), 原文, 拼音, 英文翻譯, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
MW_ANCHOR = (36.0, 57.5)             # 銀河標籤錨點（英仙雙星團一帶，北走廊右側）
MW_SKI = (18.0, 62.0)                # 「雪橇痕」標籤（仙后—英仙之間的銀河）
TERMS = {
    "駝鹿": (DIPPER, "Лось", "Los'", "Elk (= moose, Alces alces)", "駝鹿", "amber",
           "Stellarium siberian CON Elk；中西伯利亞常用，東西伯利亞多稱「熊」"),
    "鴨巢": (uniq([SEG_NEST]), "Утиное гнездо", "Utinoe gnezdo", "Duck Nest", "鴨巢", "amber",
           "Stellarium siberian CON DNe／NAME Pleiades；西伯利亞昴宿的名字都可歸成「鳥巢」"),
    "打穀者": (BELT, "Кичиги", "Kichigi", "Threshers (flail sticks)", "打穀者", "amber",
            "Stellarium siberian CON Kic；кичига＝打穀用的彎木棍；歐俄的 Кичиги 常指北斗"),
    "金樁": ([POL], "Golden stake", "", "Golden Stake", "金樁", "blue",
           "Stellarium siberian HIP 11767 Golden stake（只給英文，不自造俄文）；阿爾泰 Алтын казык、哈薩克 Темірқазық 見金樁原文層"),
    "鵝之路": (MW_ANCHOR, "Гусиная дорога", "Gusinaya doroga", "Goose Road", "鵝之路", "white",
            "Stellarium siberian NAME Milky Way（較古老的名字）；俄羅斯民間：大雁沿著它飛"),
    "馬麥之路": (MW_ANCHOR, "Мамаева дорога", "Mamaeva doroga", "Mamai's Road", "馬麥之路", "white",
             "Stellarium siberian NAME Milky Way（較晚，受蒙古—韃靼入侵影響）；Мамай＝金帳汗國將領馬麥"),
}
EVENKI = {
    "宇宙駝鹿": (DIPPER, "Хэглэн", "Kheglen", "the cosmic elk", "宇宙駝鹿（埃文基）", "amber",
             "埃文基：天上森林的母駝鹿，傍晚把太陽頂在角上帶走（Анисимов 等；Berezkin 母題索引）"),
    "滑雪道": (MW_SKI, "Манги кинглэн", "Mangi kinglen", "Mangi's ski track", "Манги 的滑雪道（銀河）",
            "white", "埃文基：追鹿的獵人 Манги 滑雪留下的痕跡＝銀河"),
}
POLE_NAMES = [("Golden stake", "金樁（西伯利亞）", "blue"),
              ("Алтын казык", "金樁（阿爾泰）", "blue"),
              ("Темірқазық", "鐵樁（哈薩克；突厥語多這樣叫）", "blue")]
ROLES = [(BOWL, "駝鹿的腳", "amber"), (HANDLE, "三個獵人", "green"),
         ([POL, KOCHAB, PHERKAD], "小駝鹿", "blue")]
PLEIADES_ALT = [("Курица с цыплятами", "母雞帶小雞（俄羅斯）"), ("すばる", "昴（日本）")]

ZH_STAR = {DUB: "天樞", MER: "天璇", PHE: "天璣", MEG: "天權", ALI: "玉衡",
           MIZ: "開陽", ALK: "搖光", POL: "北極星（勾陳一）", ALCYONE: "昴宿六",
           BETELGEUSE: "參宿四", RIGEL: "參宿七", CAPELLA: "五車二", MIRFAK: "天船三"}
EN_STAR = {DUB: "Dubhe", MER: "Merak", PHE: "Phecda", MEG: "Megrez", ALI: "Alioth",
           MIZ: "Mizar", ALK: "Alkaid", POL: "Polaris", ALCYONE: "Alcyone",
           BETELGEUSE: "Betelgeuse", RIGEL: "Rigel", CAPELLA: "Capella", MIRFAK: "Mirfak"}
# 腰帶三顆不上星名：Canva 字級 ≥36px 時三個名字擠在 2° 內會疊在「打穀者」上
STAR_COLOR = {h: "amber" for h in DIPPER}
STAR_COLOR.update({POL: "blue", ALCYONE: "white", BETELGEUSE: "white", RIGEL: "white",
                   ALNITAK: "amber", ALNILAM: "amber", MINTAKA: "amber",
                   CAPELLA: "white", MIRFAK: "white"})

# 標籤偏移（畫布單位）。北斗在北盤左上方：斗口在下（天璇—天樞）、斗柄往右上翹。
OFF_STAR = {DUB: (3.4, -1.0), MER: (-3.4, -1.0), PHE: (-3.4, 0.6), MEG: (3.4, -0.6),
            ALI: (3.4, -0.8), MIZ: (3.4, -0.6), ALK: (0.0, 2.2), POL: (0.0, -2.6),
            ALCYONE: (0.0, -3.0), BETELGEUSE: (0.0, 2.4), RIGEL: (0.0, -2.4),
            ALNITAK: (0.0, -2.4), ALNILAM: (0.0, -2.4), MINTAKA: (0.0, -2.4),
            CAPELLA: (0.0, 2.4), MIRFAK: (3.6, 0.0)}
OFF_TERM = {"駝鹿": (-4.0, -21.0), "鴨巢": (0.0, 5.0), "打穀者": (0.0, 5.0),
            "金樁": (0.0, -5.4), "鵝之路": (0.0, 0.0), "馬麥之路": (0.0, 0.0)}
OFF_EVENKI = {"宇宙駝鹿": (-4.0, -21.0), "滑雪道": (0.0, 0.0)}
TERM_DY2 = -2.6        # 中譯／拼音放在原文正下方（可與原文同時開）


def build():
    S = G.load_stars(BASE)
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=45, D_r=49, D_fill=0,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=PHI,
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

    def term_items(table, offs, field, size=1.35, keys=None):
        idx = {"orig": 1, "rom": 2, "en": 3, "zh": 4}[field]
        out = []
        for k, t in table.items():
            if keys and k not in keys:
                continue
            dx, dy = offs[k]
            if field != "orig":
                dy += TERM_DY2
            out.append(dict(anchor(t[0]), text=t[idx], color=t[5], size=size,
                            dx=dx, dy=dy, key=k))
        return out

    def star_items(table, size=1.05):
        out = []
        for h in table:
            if h not in S:
                continue
            dx, dy = OFF_STAR.get(h, (0.0, 2.2))
            w, _ = MC.label_box(table[h], size, m.fu)
            if abs(dx) > 0.1:                                  # 左右：讓字邊貼著星
                dx = math.copysign(abs(dx) + w / 2 - 1.2, dx)
            out.append({"hip": h, "text": table[h], "color": STAR_COLOR.get(h, "white"),
                        "size": size, "dx": round(dx, 2), "dy": dy, "key": f"HIP {h}"})
        return out

    base_terms = ["駝鹿", "鴨巢", "打穀者"]      # 金樁只在 07–08 鏡用「金樁原文／中譯」層
    eng = star_items(EN_STAR)
    zh = star_items(ZH_STAR) + term_items(TERMS, OFF_TERM, "zh", 1.25, base_terms)
    ru = term_items(TERMS, OFF_TERM, "orig", keys=base_terms)
    rom = term_items(TERMS, OFF_TERM, "rom", 1.2, base_terms)
    goose = (term_items(TERMS, OFF_TERM, "orig", keys=["鵝之路"]) +
             term_items(TERMS, OFF_TERM, "zh", 1.25, ["鵝之路"]))
    mamai = (term_items(TERMS, OFF_TERM, "orig", keys=["馬麥之路"]) +
             term_items(TERMS, OFF_TERM, "zh", 1.25, ["馬麥之路"]))
    ev_o = term_items(EVENKI, OFF_EVENKI, "orig")
    ev_z = term_items(EVENKI, OFF_EVENKI, "zh", 1.15)
    roles = []
    for hips, txt, col in ROLES:
        ra, dec = centroid(hips, S)
        roles.append(dict(ra=ra, dec=dec, text=txt, color=col, size=1.2,
                          dx={"駝鹿的腳": -12.0, "三個獵人": 11.0, "小駝鹿": 9.0}[txt],
                          dy={"駝鹿的腳": -3.0, "三個獵人": 0.0, "小駝鹿": 3.0}[txt],
                          key=f"角色-{txt}"))
    roles.append(dict(ra=MW_SKI[0], dec=MW_SKI[1], text="雪橇痕＝銀河", color="white",
                      size=1.2, dx=0.0, dy=0.0, key="角色-雪橇痕"))
    pole_o, pole_z = [], []
    for i, (nat, zhn, col) in enumerate(POLE_NAMES):
        pole_o.append(dict(hip=POL, text=nat, color=col, size=1.25, dx=0.0,
                           dy=-6.0 - 6.8 * i, key=f"金樁{i+1}"))
        pole_z.append(dict(hip=POL, text=zhn, color=col, size=1.0, dx=0.0,
                           dy=-8.6 - 6.8 * i, key=f"金樁{i+1}"))
    ple = []
    for i, (nat, zhn) in enumerate(PLEIADES_ALT):
        ple.append(dict(hip=ALCYONE, text=nat, color="white", size=1.15, dx=0.0,
                        dy=-6.4 - 5.6 * i, key=f"昴別名{i+1}"))
        ple.append(dict(hip=ALCYONE, text=zhn, color="white", size=0.95, dx=0.0,
                        dy=-8.8 - 5.6 * i, key=f"昴別名{i+1}"))
    euro = [dict(hip=ALNILAM, text="歐俄：Кичиги＝北斗", color="red", size=1.2,
                 dx=0.0, dy=-16.0, key="歐俄")]

    label_sets = [(eng, "英文"), (zh, "繁中"), (ru, "俄文原文"), (rom, "俄文拼音"),
                  (ev_o, "埃文基原文"), (ev_z, "埃文基中譯"), (roles, "追獵角色"),
                  (pole_o, "金樁原文"), (pole_z, "金樁中譯"), (goose, "銀河-鵝之路"),
                  (mamai, "銀河-馬麥之路"), (ple, "昴-別名"), (euro, "歐俄")]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_MAIN)
    m.L_lines(LG_CALF, name="連線-小駝鹿")
    m.L_lines(LG_HUNT, name="連線-獵人")
    m.L_marks(MAINS, "主角星白點", "dot")
    m.L_marks(MAINS, "主角星白圈", "ring")
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_MAIN, label_sets, mains=MAINS,
                  line_sets=[(LG_CALF, "連線-小駝鹿"), (LG_HUNT, "連線-獵人")],
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
    wide = mid(pole, dipc, 0.30)                  # 北斗＋小北斗＋仙后段銀河同框
    ple = P(ALCYONE)
    belt = P(ALNILAM)
    ROT_20 = -((LST_TPE_2000 + 180.0 - LST0) % 360.0)   # 盤轉到「10/9 20:00 面向北方」
    ROT_2020 = ROT_20 - 5.01                           # 再過 20 分鐘（15.041°/h）

    shots = [
        dict(code="01", kind="Z", sec=12, north=True,
             frames=[(dipc[0], dipc[1], 78.0, 0.0), (dipc[0], dipc[1], 66.0, 0.0)],
             layers=["L4"], labels=[],
             vo="上週五在草原，我們找到一根拴住天空的樁。今晚再往北，走進針葉林。"
                "同一片星空，西伯利亞獵人看見——一場永不結束的狩獵。",
             card="同一片星空，西伯利亞獵人看見——一場永不結束的狩獵",
             note="統一開頭：北斗（駝鹿）＋金樁同框，駝鹿連線亮起"),
        dict(code="02", kind="Z", sec=18, north=True,
             frames=[(dipc[0], dipc[1], 60.0, 0.0), (dipc[0], dipc[1], 52.0, 0.0)],
             layers=["L4"], labels=["俄文原文", "繁中"],
             vo="先看北斗七星。西伯利亞的俄文名字叫 Лось——駝鹿，就是北美說的 moose，"
                "不是四不像的麋鹿。在西伯利亞中部，這個名字最常聽到；再往東，人們多半叫它熊。",
             note="Лось＋駝鹿疊字；首留言補「Stellarium 英文寫 Elk＝英式英語的 moose」"),
        dict(code="03", kind="Z", sec=18, north=True,
             frames=[(dipc[0], dipc[1], 56.0, 0.0), (dipc[0], dipc[1], 50.0, 0.0)],
             layers=["L4"], labels=["埃文基原文", "埃文基中譯"],
             vo="埃文基人的故事最完整。天空是上面那一層的森林，住著一頭宇宙駝鹿，Хэглэн。"
                "每天傍晚，牠把太陽頂在角上，拖進林子裡——天就黑了。",
             note="埃文基：宇宙駝鹿 Хэглэн（天上的母駝鹿）"),
        dict(code="04", kind="Z", sec=20, north=True,
             frames=[(dipc[0], dipc[1], 52.0, 0.0), (dipc[0], dipc[1], 48.0, 0.0)],
             layers=["L4", "獵人"], labels=["追獵角色"],
             vo="獵人 Манги 踩著雪橇追上去，一箭射中駝鹿，把太陽搶回來——天就亮了。"
                "斗口四顆，是駝鹿的腳；斗柄三顆，是追在後面的獵人。每天晚上，這場追獵都重演一次。",
             note="斗柄三顆改綠（L6 連線-獵人）；角色標籤：駝鹿的腳／三個獵人"),
        dict(code="05", kind="Z", sec=14, north=True,
             frames=[(dipc[0], dipc[1], 56.0, 0.0), (wide[0], wide[1], 100.0, 0.0)],
             layers=["L4", "獵人", "小駝鹿"], labels=["追獵角色", "埃文基原文"],
             vo="旁邊的小北斗，是跟在媽媽後面的小駝鹿。獵人滑過天空留下的雪橇痕，就是銀河——"
                "Манги кинглэн，Манги 的滑雪道。",
             note="拉遠：小北斗（藍，L5 連線-小駝鹿）＋仙后—英仙段銀河同框"),
        dict(code="06", kind="Z", sec=18, north=True,
             frames=[(wide[0], wide[1], 100.0, 0.0), (wide[0], wide[1], 100.0, 0.0)],
             layers=["L4", "獵人", "小駝鹿"], labels=["追獵角色"],
             overlay="C-A08-01_宇宙追獵", overlay_layers=["埃文基層", "米克馬克層"],
             vo="這個追獵的故事，不只西伯利亞有。有學者推測，它一萬多年前就跟著人走過白令陸橋——"
                "北美的米克馬克人也說：斗口是一頭熊，斗柄是追牠的獵人。",
             note="疊概念圖 C-A08-01（埃文基／米克馬克兩層，定格頁逐層疊上）"),
        dict(code="07", kind="Z", sec=16, north=True,
             frames=[(0.0, yp + 6.0, 54.0, 0.0), (0.0, yp + 4.0, 48.0, 0.0)],
             layers=["L4"], labels=["金樁原文", "金樁中譯", "繁中"],
             vo="而牠們繞著轉的那一點，西伯利亞也叫它金樁——跟上週的蒙古一樣。"
                "阿爾泰人說 Алтын казык，也是金樁；更多突厥民族說得更硬：鐵樁。",
             note="金樁置中；阿爾泰／哈薩克兩個名字依序疊字"),
        dict(code="08", kind="Z", sec=22, north=True,
             frames=[(0.0, yp + 4.0, 48.0, 0.0), (0.0, yp + 4.0, 48.0, 0.0)],
             layers=["L4"], labels=["金樁原文", "金樁中譯", "繁中"],
             overlay="C-A08-02_候鳥看轉軸", overlay_layers=["北極星層", "參宿四層"],
             vo="這根樁，連候鳥都在用。一九七〇年，鳥類學家 Emlen 在天象儀裡養大一群小鳥："
                "星空繞著北極星轉，牠們秋天就往南飛；把轉軸換成參宿四，牠們就背著參宿四飛。"
                "鳥記住的，是天空的轉軸。",
             note="疊概念圖 C-A08-02（北極星轉軸／參宿四轉軸兩層）"),
        dict(code="09", kind="T", sec=18, north=True,
             frames=[(0.0, yp, 48.0, 0.0), (0.0, 58.0, 48.0, 0.0)],
             layers=["L4"], labels=["銀河-鵝之路"],
             vo="候鳥飛的那條路，西伯利亞有個老名字：Гусиная дорога，鵝之路——"
                "傳說大雁秋天往南，就沿著這條光帶走。上週的蒙古人，叫它天空的縫線。",
             note="從金樁沿北走廊往下，穿進英仙座一段的銀河"),
        dict(code="10", kind="Z", sec=20, north=True,
             frames=[(0.0, 58.0, 48.0, 0.0), (6.0, 60.0, 64.0, 0.0)],
             layers=["L4"], labels=["銀河-鵝之路"], labels_end=["銀河-馬麥之路"],
             vo="後來，它多了一個新名字：Мамаева дорога，馬麥之路。馬麥是金帳汗國的大將；"
                "這個名字記住的，是蒙古—韃靼大軍打進俄羅斯的那段日子。一條銀河，兩個時代。",
             card="鵝之路 → 馬麥之路",
             note="起格＝鵝之路，唸到 Мамаева 時換成迄格＝馬麥之路；稍微拉遠讓銀河更長"),
        dict(code="11", kind="T", sec=18, north=True,
             frames=[(0.0, 58.0, 48.0, 0.0), (0.0, 30.0, 48.0, 0.0)],
             layers=["L4"], labels=["俄文原文", "繁中"],
             vo="順著銀河往下，是一小團星：Утиное гнездо，鴨巢。西伯利亞給它的名字，"
                "比給銀河的還多；但每一個，幾乎都能歸成同一個樣子——鳥窩。",
             note="沿北走廊往下到昴宿（鴨巢一圈連線）"),
        dict(code="12", kind="Z", sec=12, north=True,
             frames=[(ple[0], ple[1] - 4.0, 34.0, 0.0), (ple[0], ple[1] - 4.0, 30.0, 0.0)],
             layers=["L4"], labels=["昴-別名"],
             vo="同一團星，俄羅斯人也叫它 Курица с цыплятами，母雞帶小雞；在日本，它是 すばる。",
             note="昴宿特寫；兩個別名依序疊字"),
        dict(code="13", kind="Z", sec=20, north=True,
             frames=[(ple[0], ple[1] - 6.0, 40.0, 0.0), (belt[0], belt[1] + 4.0, 40.0, 0.0)],
             layers=["L4"], labels=["俄文原文", "繁中"],
             vo="再往東，是那條三顆星的腰帶。上週，蒙古的神射手追著三頭鹿；"
                "西伯利亞人看見的，是三個打穀的人，排成一排——Кичиги。кичига，就是打穀用的彎木棍。",
             note="往東（左）平移到獵戶腰帶；Кичиги 三顆連線"),
        dict(code="14", kind="Z", sec=14, north=True,
             frames=[(belt[0], belt[1] + 2.0, 36.0, 0.0), (belt[0], belt[1] + 2.0, 32.0, 0.0)],
             layers=["L4"], labels=["俄文原文", "繁中", "歐俄"],
             vo="有趣的是，同一個名字到了俄羅斯的歐洲那一邊，常常指的是北斗。"
                "同一件農具，換個地方，就掛到了另一群星上。",
             note="紅字「歐俄：Кичиги＝北斗」"),
        dict(code="15", kind="T", sec=10, north=True,
             frames=[(0.0, 24.0, 48.0, 0.0), (0.0, yp, 48.0, 0.0)],
             layers=["L4"], labels=[], cut=True,
             vo="最後，回到北方，回到那頭駝鹿。",
             note="【硬切】回北走廊，沿銀河抬頭到金樁；迄格＝16 起格（長圖轉北盤）"),
        dict(code="16", kind="R", sec=22, north=True,
             frames=[(0.0, yp, 48.0, 0.0), (-8.0, yp, 116.0, ROT_20)],
             layers=["L4", "獵人"], labels=[],
             vo="整片天空繞著金樁轉。看它怎麼轉：斗口在前、斗柄在後——三個獵人永遠追在駝鹿後面。"
                "在埃文基人的森林裡，駝鹿整夜不落，這場追獵從來不停。",
             note=f"從「長圖轉北盤1」（與 15 迄格同框換組）→ 逆時針 {ROT_20:+.1f}°"
                  f"（{-ROT_20/15.041:.1f} 小時）＋拉遠到 fov 116；斗口在前（逆時針方向）、斗柄在後。"
                  "起格＝換組頁，山留在模板位置（與 15 迄格一致）；迄格＝17 起格，山降到圖拉 64.3°N 的地平線"
                  "（Y≈1796，只露出山頂）"),
        dict(code="17", kind="R", sec=20, north=True,
             frames=[(-8.0, yp, 116.0, ROT_20), (-8.0, yp, 116.0, ROT_20)],
             layers=["L4", "獵人"], labels=[], horizon=[PHI, PHI_TPE],
             vo="在台北，今晚八點，斗口已經沉到西北方的地平線，只剩三個獵人還在上面追。"
                "轉過身，東北方的鴨巢剛升起；十點多，打穀的人也會從正東方排隊上來。",
             note="盤不動；山的剪影從圖拉高度升到台北高度（Match & Move）"),
        dict(code="18", kind="R", sec=10, north=True,
             frames=[(-8.0, yp, 116.0, ROT_20), (-8.0, yp, 116.0, ROT_2020)],
             layers=["L4", "獵人"], labels=[], horizon=[PHI_TPE],
             vo="下週五，換個問題：古人以為，天空到底長什麼樣？",
             card="下集見｜論天三家：古人以為天空長什麼樣？",
             note="盤再轉 20 分鐘；端卡＋追蹤 CTA"),
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

    terms_all = dict(TERMS, **EVENKI)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": {k: dict(zip(("hips", "原文", "拼音", "英文翻譯", "中文",
                                      "顏色", "來源備註"), v)) for k, v in terms_all.items()},
               "cross": [dict(原文=n, 中譯=z, 顏色=c) for n, z, c in POLE_NAMES] +
                        [dict(原文=n, 中譯=z, 顏色="white") for n, z in PLEIADES_ALT],
               "mains": MAINS,
               "lines": {"L4": "星座連線", "小駝鹿": "連線-小駝鹿", "獵人": "連線-獵人"},
               "line_groups": {"L4": LG_MAIN, "小駝鹿": LG_CALF, "獵人": LG_HUNT},
               "lst_tpe_2000": LST_TPE_2000},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    lg_all = LG_MAIN + LG_CALF + LG_HUNT
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=lg_all,
                  labels=[dict(it, pt=6) for it in items],
                  title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, lg_all)
    m.sb_grid(os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), shots, line_groups=LG_MAIN,
              labels=[dict(it, pt=5) for it in zh],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）"
                    f"　總長 {sum(s['sec'] for s in shots)} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
