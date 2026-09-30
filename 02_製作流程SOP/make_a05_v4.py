# -*- coding: utf-8 -*-
"""A-05 日本：一整座天空的農具｜大畫布 v4.5

輸出：L1銀河 L2星點 L3經緯線 L4星座連線
　　　L5標籤-英文 L6標籤-繁中宿名 L7標籤-和名 L8標籤-和名語意
　　　L9標籤-跨文化原文 L10標籤-跨文化中譯
　　　＋ 南北盤圖層組 / 預覽黑底 / SB-分鏡 / SB-鏡頭牆 / 鏡頭清單 / 盤對位
執行：python3 make_a05_v4.py

參數（見 星圖呈現規格_v4_大畫布.md 肆）
  lst  = 56  → 昴（RA 56.2）落在 x≈0；西方白虎七宿 奎(+38)→参(−33) 一次掃完
  D_s  = 45  → 二十八宿全體 dec −44.3（斗）…+41.1（奎）都在長圖帶內
  D_r  = 49  → 北斗最南 Alkaid +49.3 落在盤上；紫微垣整個在盤上
  D_fill=0   → k=1.397、R_fill=125.8 ≤180；北盤＝完整北半球＝キトラ式圓形星圖
  x_tN = 0   → 北走廊＝RA 56，由昴經英仙、仙后直通北極（T 抬頭用）

資料注意（見逐字稿「考據備忘・七」）：
  Stellarium japanese_moon_stations 的 21 宿 pronounce 誤植為 KagasukiBoshi，
  正確為 からすきぼし（唐鋤星）；ja.po 另把房/室對調。本檔一律以自備表為準。
"""
import os, sys, json, math, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, R_RIM

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP   = "A-05"
OUT  = os.path.join(BASE, "05_素材/A-05_日本/_v4大畫布")
PHI, LST0 = 25.0, 56.0

jsegs, jmeta = G.culture_lines(BASE, "japanese_moon_stations")
csegs, cmeta = G.culture_lines(BASE, "chinese")

# ══════════════════════════════════════════════════════════════════
# 一、二十八宿：english key → (序, 漢字宿名, 和名かな, 和名語意)
#     和名採辭書主形（大辞泉／精選版日国），非 Stellarium 羅馬字
# ══════════════════════════════════════════════════════════════════
SHUKU = [
    ("Horn",                "角", "すぼし",       ""),
    ("Neck",                "亢", "あみぼし",     "網？（野尻：意味不明）"),
    ("Root",                "氐", "ともぼし",     ""),
    ("Chamber",             "房", "そいぼし",     "添星・依著心宿"),
    ("Heart",               "心", "なかごぼし",   "中子・正中的那顆"),
    ("Tail",                "尾", "あしたれぼし", "足垂れ・垂下的腳"),
    ("Basket",              "箕", "みぼし",       "箕・簸箕"),
    ("Dipper",              "斗", "ひつきぼし",   ""),
    ("Cow",                 "牛", "いなみぼし",   "稲見・看得見稻子的時節"),
    ("Woman",               "女", "うるきぼし",   ""),
    ("Emptiness",           "虛", "とみてぼし",   ""),
    ("Roof Top",            "危", "うみやめぼし", ""),
    ("Room",                "室", "はついぼし",   ""),
    ("Wall",                "壁", "なまめぼし",   ""),
    ("Stride",              "奎", "とかきぼし",   "斗掻き・刮平米斗的棒"),
    ("Hill",                "婁", "たたらぼし",   "蹈鞴・腳踏的煉鐵風箱"),
    ("Stomach",             "胃", "えきえぼし",   ""),
    ("Stopping Place",      "昴", "すばるぼし",   "統ばる・束成一把"),
    ("Net",                 "畢", "あめふりぼし", "雨降り・下雨（漢籍移植）"),
    ("Turtle Snout",        "觜", "とろきぼし",   ""),
    ("Investigator",        "參", "からすきぼし", "唐鋤・一把犁"),
    ("Well",                "井", "ちちりぼし",   ""),
    ("Ogre",                "鬼", "たまおのぼし", "魂緒の星・繫住魂的繩"),
    ("Willow",              "柳", "ぬりこぼし",   "塗籠？・內室"),
    ("Stars",               "星", "ほとおりぼし", "熱り・熱（推測）"),
    ("Stretched Net",       "張", "ちりこぼし",   ""),
    ("Wings",               "翼", "たすきぼし",   "襷・綁袖子的帶"),
    ("Chariot Cross-Board", "軫", "みつかけぼし", ""),
]
# 四象分組（顏色）：白虎＝本集主秀
XIANG = {
    "amber":  ["Stride", "Hill", "Stomach", "Stopping Place", "Net",
               "Turtle Snout", "Investigator"],                       # 西方白虎
    "red":    ["Well", "Ogre", "Willow", "Stars", "Stretched Net",
               "Wings", "Chariot Cross-Board"],                       # 南方朱雀
    "green":  ["Horn", "Neck", "Root", "Chamber", "Heart", "Tail",
               "Basket"],                                             # 東方蒼龍
    "blue":   ["Dipper", "Cow", "Woman", "Emptiness", "Roof Top",
               "Room", "Wall"],                                       # 北方玄武
}
# 北盤用：中國紫微垣與北斗（妙見信仰的源頭）
CN_POLAR = ["紫微左垣", "紫微右垣", "北极", "勾陈", "天皇大帝", "四辅",
            "华盖", "杠 (附华盖)", "北斗", "辅 (附北斗)", "文昌", "五帝内座"]
CN_ZH = {"紫微左垣": "紫微左垣", "紫微右垣": "紫微右垣", "北极": "北極五星",
         "勾陈": "勾陳", "天皇大帝": "天皇大帝", "四辅": "四輔",
         "华盖": "華蓋", "杠 (附华盖)": "杠", "北斗": "北斗七星",
         "辅 (附北斗)": "輔", "文昌": "文昌", "五帝内座": "五帝內座"}

# 主角星
ALCYONE, ALDEBARAN = 17702, 21421
MINTAKA, ALNILAM, ALNITAK = 25930, 26311, 26727
BETELGEUSE, RIGEL, ALPHARD = 27989, 24436, 46390
POLARIS, DUBHE, ALKAID = 11767, 54061, 67301
HAMAL, MIRFAK, CAPELLA = 9884, 15863, 24608
BELT = [MINTAKA, ALNILAM, ALNITAK]
PLEIADES = [17499, 17531, 17702, 17608]
HYADES = [20889, 20455, 20205, 20894, 21421]
BEEHIVE = [42911, 41822, 41909, 42806]

MAINS = [ALCYONE, ALDEBARAN, MINTAKA, ALNILAM, ALNITAK, BETELGEUSE, RIGEL,
         ALPHARD, POLARIS, DUBHE, ALKAID, HAMAL, MIRFAK, CAPELLA]


def _load_iau(base):
    p = os.path.join(base, "07_資料來源/_整理CSV/03_星點座標表.csv")
    out = {}
    for r in csv.DictReader(open(p, encoding="utf-8-sig")):
        if r["代號"].startswith("HIP") and r.get("國際星名/說明"):
            nm = r["國際星名/說明"].split("（")[0].split("(")[0].strip()
            if nm:
                out[int(r["代號"].split()[1])] = nm
    return out


ENG = _load_iau(BASE)


def hips_of(name, src):
    return sorted({h for seg in src.get(name, []) for h in seg})


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    if not hs:
        return None
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


# ══════════════════════════════════════════════════════════════════
# 二、跨文化：同一排星，每個靠天吃飯的地方都看成自己手裡那件工具
#     （全部出自 07_資料來源/_整理CSV，見逐字稿「考據備忘・五」）
# ══════════════════════════════════════════════════════════════════
CROSS = [
    # 参宿腰帶——工具的大合唱（本集最強跨文化段）
    ("からすきぼし 唐鋤星",        "犁（日本）",              BELT, "amber", -15.0,  11.0),
    ("Bintoéng Rakkalaé",         "犁（布吉・蘇拉威西）",    BELT, "amber", -15.0,   7.4),
    ("Rarița",                    "小犁（羅馬尼亞）",        BELT, "amber", -15.0,   3.8),
    ("Sfredelul mare",            "大螺旋鑽（羅馬尼亞）",    BELT, "amber", -15.0,   0.2),
    ("Касцы Kastsy",              "割草的人（白俄羅斯）",    BELT, "amber", -15.0,  -3.4),
    ("Kichigi",                   "打穀的人（西伯利亞）",    BELT, "amber", -15.0,  -7.0),
    ("Sioyahpu",                  "錛子的柄（圖卡諾）",      BELT, "amber", -15.0, -10.6),
    ("Sos Bacheddos",             "手杖（薩丁尼亞）",        BELT, "amber", -15.0, -14.2),
    ("النظم al-Naẓm",             "一串珠（阿拉伯）",        BELT, "amber", -15.0, -17.8),
    ("Ullaktut",                  "奔跑的人（因紐特）",      BELT, "amber", -15.0, -21.4),
    # 昴——「束起來」的意象在兩個沒接觸的文化撞在一起
    ("すばる 統ばる",             "束成一把（日本）",        PLEIADES, "blue", 13.0,  9.5),
    ("S'Udrone",                  "一束（薩丁尼亞）",        PLEIADES, "blue", 13.0,  5.9),
    ("الثريا al-Thurayyā",        "圖拉亞（阿拉伯）",        PLEIADES, "blue", 13.0,  2.3),
    ("Куркі Kurki",               "母雞（白俄羅斯）",        PLEIADES, "blue", 13.0, -1.3),
    ("Cloșca cu pui",             "孵蛋的母雞與小雞（羅馬尼亞）", PLEIADES, "blue", 13.0, -4.9),
    ("Sakiattiak",                "胸骨（因紐特）",          PLEIADES, "blue", 13.0, -8.5),
    ("Eixu",                      "大黃蜂（圖皮）",          PLEIADES, "blue", 13.0, -12.1),
    ("Makaliʻi",                  "酋長之眼（夏威夷）",      PLEIADES, "blue", 13.0, -15.7),
    ("Kṛittikā",                  "基栗底柯（印度）",        PLEIADES, "blue", 13.0, -19.3),
    # 畢——三個文化都看見嘴或顎；日本的「雨」是從漢籍搬來的
    ("あめふりぼし 雨降り星",     "下雨（日本・借自漢籍）",  HYADES, "red", 0.0, 26.0),
    ("Wolf's Mouth",              "狼嘴（北歐）",            HYADES, "red", 0.0, 22.4),
    ("Jaw",                       "下巴（埃及）",            HYADES, "red", 0.0, 18.8),
    ("Tapi'i rainhyka",           "貘的下顎（圖皮）",        HYADES, "red", 0.0, 15.2),
    ("Qimmiitt",                  "狗群（因紐特）",          HYADES, "red", 0.0, 11.6),
    ("釣鐘星 つりがねぼし",       "吊鐘（日本・真正的民間名）", HYADES, "red", 0.0,  8.0),
    # 鬼——積屍氣／魂緒
    ("たまおのぼし 魂緒の星",     "繫住魂的繩（日本）",      BEEHIVE, "purple", 0.0,  6.6),
    ("النثرة al-Nathrah",         "獅子的鼻孔（阿拉伯）",    BEEHIVE, "purple", 0.0,  3.0),
    ("Puṣyā",                     "滋養者（印度）",          BEEHIVE, "purple", 0.0, -0.6),
    ("Racul",                     "小龍蝦（羅馬尼亞）",      BEEHIVE, "purple", 0.0, -4.2),
]


def build():
    S = G.load_stars(BASE)
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=45, D_r=49, D_fill=0,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=PHI,
               maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([c[0] for c in CROSS] + [c[1] for c in CROSS] +
                   [s[2] for s in SHUKU] + [s[3] for s in SHUKU if s[3]])

    # ── 連線分組 ──
    lg = []
    for color, keys in XIANG.items():
        ss = []
        for k in keys:
            if k not in jsegs:
                print(f"  ⚠ 找不到宿：{k}")
            ss += jsegs.get(k, [])
        lg.append((ss, color, 1.0))
    cn_ss = []
    for n in CN_POLAR:
        if n not in csegs:
            print(f"  ⚠ 找不到中國星官：{n}")
        cn_ss += csegs.get(n, [])
    lg.append((cn_ss, "purple", 0.9))

    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(lg)

    # ── L5 英文（IAU 星名）──
    eng_items = [{"hip": h, "text": ENG.get(h, ""), "color": c, "dy": 2.0}
                 for h, c in [(ALCYONE, "amber"), (ALDEBARAN, "amber"),
                              (ALNILAM, "amber"), (BETELGEUSE, "amber"),
                              (RIGEL, "amber"), (HAMAL, "amber"),
                              (MIRFAK, "amber"), (CAPELLA, "amber"),
                              (ALPHARD, "red"), (POLARIS, "purple"),
                              (DUBHE, "purple"), (ALKAID, "purple")]
                 if ENG.get(h)]
    m.L_labels(eng_items, "英文")

    # ── L6 繁中宿名 / L7 和名 / L8 和名語意 ──
    key2color = {k: c for c, ks in XIANG.items() for k in ks}
    zh_items, ja_items, mean_items = [], [], []
    for i, (key, zh, kana, mean) in enumerate(SHUKU):
        hs = hips_of(key, jsegs)
        cc = centroid(hs, S)
        if not cc:
            print(f"  ⚠ 宿無星：{key}")
            continue
        ra, dec = cc
        col = key2color.get(key, "white")
        base = dict(ra=ra, dec=dec, color=col, size=1.5, dx=0.0, dy=3.2)
        zh_items.append(dict(base, text=f"{i+1:02d} {zh}宿"))
        ja_items.append(dict(base, text=kana))
        if mean:
            mean_items.append(dict(base, text=mean, size=1.2, dy=-3.2))
    for n in CN_POLAR:
        cc = centroid(hips_of(n, csegs), S)
        if cc:
            zh_items.append({"ra": cc[0], "dec": cc[1], "text": CN_ZH[n],
                             "color": "purple", "size": 1.5, "dx": 0.0, "dy": 2.8})
    zh_items = MC.spread_labels(m, zh_items, pad=1.4, pull=0.05)
    ja_items = MC.spread_labels(m, ja_items, pad=1.4, pull=0.05)
    mean_items = MC.spread_labels(m, mean_items, pad=1.2, pull=0.05)
    m.L_labels(zh_items, "繁中宿名")
    m.L_labels(ja_items, "和名")
    m.L_labels(mean_items, "和名語意")

    def cross_items(which):
        out = []
        for nat, zh, grp, color, dx, dy in CROSS:
            cc = centroid(grp, S)
            out.append({"ra": cc[0], "dec": cc[1],
                        "text": nat if which == 0 else zh,
                        "color": color, "size": 1.2, "dx": dx, "dy": dy})
        return out

    m.L_labels(cross_items(0), "跨文化原文")
    m.L_labels(cross_items(1), "跨文化中譯")

    label_sets = [(eng_items, "英文"), (zh_items, "繁中宿名"),
                  (ja_items, "和名"), (mean_items, "和名語意"),
                  (cross_items(0), "跨文化原文"), (cross_items(1), "跨文化中譯")]
    m.build_discs(lg, label_sets, mains=MAINS)
    MC.disc_svg_registration_test(m)

    # ════════════════════ 鏡頭（對齊逐字稿 v2，17 鏡／300 秒）═════════
    yp = m.y_pole
    F_T = 48.0          # T 半寬 24 ≤ w_c−feather−1 = 25
    F_R = 50.0          # 極點置中：≤55 才可與大畫布同框互切
    shots = [
        dict(code="01", kind="Z", sec=16, north=True,
             frames=[(0.0, 24.0, 14.0, 0.0), (0.0, 24.0, 9.0, 0.0)],
             note="鉤子：昴特寫＋C-A05-01（六連星→車標）。"
                  "すばる＝日本現存最古老的星名，現在印在車頭上"),
        dict(code="02", kind="Z", sec=18, north=True,
             frames=[(0.0, 24.0, 9.0, 0.0), (0.0, 22.0, 46.0, 0.0)],
             note="拉開：從昴退到昴—畢—胃—婁一帶。"
                  "旁白轉到奈良明日香村キトラ古墳、1998 年的探測鏡"),
        dict(code="03", kind="T", sec=16, north=True,
             frames=[(0.0, 22.0, 46.0, 0.0), (0.0, yp, F_T, 0.0)],
             note="沿北走廊（RA 56：昴→英仙→仙后）抬頭到北極；"
                  "疊 C-A05-02 キトラ天文図復原：360+ 金箔星／74 星官／四個圈"),
        dict(code="04", kind="R", sec=18, north=True,
             frames=[(0.0, yp, F_R, 0.0), (0.0, yp, F_R, -16.0)],
             note="切北盤圖層組（置中，與 03 迄格同框硬切）→慢轉 −16°。"
                  "北盤＝完整北半球圓形星圖，正是キトラ那張圖的形狀"),
        dict(code="05", kind="R", sec=20, north=True,
             frames=[(0.0, yp, F_R, -16.0), (-6.0, yp + 16.0, 58.0, -38.0)],
             note="續轉至 −38°＋微退。緯度爭議三組數字上字卡："
                  "宮島 37–38°/平壤/前 65；相馬 33.9°/長安/300；奈文研：量不出來"),
        dict(code="06", kind="Z", sec=10, north=True,
             frames=[(38.0, 4.0, 48.0, 0.0), (38.0, 4.0, 40.0, 0.0)],
             note="【全新構圖硬切】切回大畫布、停在奎宿，準備往西掃。"
                  "「照抄了整套格子，卻沒有照抄名字」"),
        dict(code="07", kind="S", sec=25, north=True,
             frames=[(38.0, 4.0, 40.0, 0.0), (-33.0, 4.0, 40.0, 0.0)],
             note="★招牌：右→左掃過西方白虎七宿 奎→婁→胃→昴→畢→觜→参，"
                  "L7 和名與 L8 語意逐一淡入（斗掻き／蹈鞴／すばる／雨降り／唐鋤）"),
        dict(code="08", kind="Z", sec=16, north=True,
             frames=[(-33.0, 4.0, 40.0, 0.0), (-33.0, 4.0, 44.0, 0.0)],
             note="定格在昴—参段。左右對照字卡：韓國＝官職名冊／日本＝量米棒、"
                  "煉鐵風箱、下雨、一把犁"),
        dict(code="09", kind="S", sec=15, north=True,
             frames=[(-36.0, 4.0, 44.0, 0.0), (-105.0, 4.0, 44.0, 0.0)],
             note="續掃南方朱雀七宿 井→鬼→柳→星→張→翼（末格帶到軫）（ちちり／魂緒／"
                  "ぬりこ／ほとおり／ちりこ／たすき／みつかけ）"),
        dict(code="10", kind="Z", sec=18, north=True,
             frames=[(-105.0, 4.0, 44.0, 0.0), (-105.0, 4.0, 34.0, 0.0)],
             note="定格＋字卡「江戸の訳名／九個意味不明」：這是江戶中期學者配的"
                  "訓讀，不是自古的民間星名（野尻抱影）"),
        dict(code="11", kind="Z", sec=20, north=True,
             frames=[(-11.0, 20.0, 32.0, 0.0), (-11.0, 20.0, 26.0, 0.0)],
             note="【全新構圖硬切】畢宿特寫：真民間名是釣鐘星、稲叢星、扇星，"
                  "沒有雨；「雨降り星」是《詩經》「月離于畢，俾滂沱矣」整句搬來"),
        dict(code="12", kind="Z", sec=20, north=True,
             frames=[(0.0, 24.0, 20.0, 0.0), (0.0, 24.0, 11.0, 0.0)],
             note="昴特寫＋文獻字卡：《古事記》美須麻流之珠／《和名類聚抄》934"
                  "「和名須波流」／《枕草子》236 段「星は、昴」／語源 統ばる"),
        dict(code="13", kind="Z", sec=16, north=True,
             frames=[(0.0, 24.0, 11.0, 0.0), (0.0, 24.0, 8.0, 0.0)],
             note="疊 C-A05-01 第二張：1955 年北謙治定名すばる，六顆星＝六家公司"),
        dict(code="14", kind="Z", sec=25, north=True,
             frames=[(-33.0, 0.0, 30.0, 0.0), (-33.0, 0.0, 46.0, 0.0)],
             note="【全新構圖硬切】参宿特寫→退開，L9/L10 跨文化十條整疊淡入："
                  "犁／小犁／螺旋鑽／割草的人／打穀的人／錛柄／手杖／一串珠"),
        dict(code="15", kind="T", sec=14, north=True,
             frames=[(0.0, 20.0, F_T, 0.0), (0.0, yp, F_T, 0.0)],
             note="沿走廊抬頭。「沒有人互相抄——每一個靠天吃飯的地方，都把那排"
                  "星星看成自己手裡的那件工具」"),
        dict(code="16", kind="R", sec=18, north=True,
             frames=[(0.0, yp, F_R, 0.0), (-16.0, yp + 20.0, 58.0, -22.0)],
             note="切北盤圖層組（與 15 迄格同框硬切）→轉 −22°，把紫微垣與北斗"
                  "帶進畫面：妙見菩薩＝北極星與北斗；陰陽寮的天文密奏"),
        dict(code="17", kind="S", sec=15, north=True,
             frames=[(0.0, 8.0, 40.0, 0.0), (-33.0, 8.0, 40.0, 0.0)],
             note="【全新構圖硬切】回大畫布，昴→畢→参 依升起順序平移＋端卡"
                  "「EP6 中秋｜二十八宿：月亮的 28 間驛站」"),
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
                off = (round(-(cx - xt) / fov * 1080),
                       round((cy - yc) / fov * 1080))
            else:
                which = "大畫布圖層組"
                ew = 360.0 / fov * 1080
                off = (round(-cx / fov * 1080), round(cy / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"],
                         "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else "迄", "用檔": which,
                         "元素寬px": round(ew), "位移X px": off[0],
                         "位移Y px": off[1], "旋轉度": rot,
                         "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w",
              encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w",
                          encoding="utf-8"), ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {sum(s['sec'] for s in shots)} 秒）")
    m.save_manifest(shots=[{k: v for k, v in s.items()} for s in shots])

    print("\n── 預覽與分鏡 ──")
    m.preview(os.path.join(OUT, f"{EP}_預覽黑底.png"), line_groups=lg,
              labels=[dict(it, pt=6) for it in zh_items],
              title=f"{EP}　大畫布 v4.5（繁中宿名）")
    m.preview(os.path.join(OUT, f"{EP}_預覽黑底-和名.png"), line_groups=lg,
              labels=[dict(it, pt=6) for it in ja_items],
              title=f"{EP}　大畫布 v4.5（和名）")
    m.preview(os.path.join(OUT, f"{EP}_預覽黑底-跨文化.png"), line_groups=lg,
              labels=[dict(it, pt=6) for it in cross_items(0)],
              title=f"{EP}　大畫布 v4.5（跨文化原文）")
    storyboard(m, shots, lg)
    m.sb_grid(os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), shots, line_groups=lg,
              labels=[dict(it, pt=5) for it in zh_items],
              title=f"{EP} 逐鏡頭 9:16")
    print("\n完成：", OUT)



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
    ax.text(x0 + 3, y1 - 3, f"{EP}　分鏡（v4.5 單一大畫布）", fontproperties=FP,
            fontsize=14, color="#FFFFFF", ha="left", va="top", weight="bold",
            zorder=13)
    fn = os.path.join(OUT, f"{EP}_SB-分鏡.png")
    f.savefig(fn, facecolor=MC.COLORS["bg"]); plt.close(f)
    print(f"  ✓ {os.path.basename(fn)}")


if __name__ == "__main__":
    build()
