# -*- coding: utf-8 -*-
"""A-17 黑腳族：留在天上的六個孩子｜大畫布 v4.6

論點：黑腳族的天上，收留了被欺負、被拋下的孩子——北斗是逃上天的七兄弟和小妹 Sinopa（輔星），
昴宿是六個沒有小牛皮袍、被笑的窮孩子（走失的孩子），疤臉 Poïa 成了晨星（木星）；
地上的帳篷頂畫著天（北斗、昴宿、晨星的十字），北極星是天上的一個洞。
最後一個弟弟（搖光）繞著北極星＝半夜的時鐘。

來源：McClintock《The Old North Trail》1910；Wissler & Duvall 1908；
Stellarium blackfoot（舊版 stellarium-skycultures-master：Bucur 據 Miller 1997；新版主程式已不收）；
跨文化（19 鏡下集）：Stellarium egyptian「Bull's Foreleg」；天象 PyEphem 自算。
逐字稿：04_腳本庫/A-17-黑腳族留在天上的六個孩子-逐字稿-v1.md。

連線：北斗（七兄弟和小妹，琥珀）照 Stellarium blackfoot 001；輔星（Sinopa）Stellarium 只寫了一個
[65477, 65477] 的空線段 → 改用「主角星細圈」標出。北河二—北河三（灰燼酋長與卡在後面的）、
北冕（蜘蛛人的帳篷）、武仙（蜘蛛人的手指）只在 L4 總層（11 鏡已刪）。牛的前腿＝古埃及（下集預告）。

鏡頭路線：01 長圖昴宿推近（開場）→ 02–04 定格 C-A17-01 三層的帳篷 →【換北盤】05–07 Browning 面北
（20:00）：七兄弟和小妹、C-A17-02 逃上天、推近北斗 → 08 盤從 18:00 轉到 06:00（最後一個弟弟）
→ 09 推近北極星（天上的洞）→【換長圖】10 羽毛女（C-A17-03）→ 12 木星＝疤臉 → 14 昴宿
→ 15 春天看不見（C-A17-04）→ 17 拉遠到銀河（狼的路）→ 18 圖卡 → 19【換北盤】北斗＝牛的前腿。

參數
  lst = 7 → 由 08 鏡決定（v4.6 第四節）：Browning 1/15 的地方恆星時 18:00 17.2°、20:00 47.3°、
             00:00 107.5°、06:00 197.7°；rot＝(lst−LST)%360−180 → 18:00 +169.8°、20:00 +139.7°、
             00:00 +79.5°、06:00 −10.7°：18:00→06:00 一路逆時針、整段在 (−180,180] 內，
             分 18→00、00→06 兩段（各 90°，< 180°）。lst 再大 18:00 就超過 +180°。
             代價：長圖的內容都在東側——昴宿 x −50、銀河（英仙—御夫）−43…−90、北河 −107、
             木星（1/15 RA 147.5、Dec +14.1，獅子座）−140.5；長圖鏡頭用 S／Z 平移，不走走廊。
  D_s = 45、D_r = 49 → 北斗最南的搖光 +49.31 在北盤本體；輔星 +55.0；昴宿 +24、北河、木星在帶內。
  D_fill = 0 → k=1.3975、R_fill=125.77（盤寬 ÷ 畫布寬＝0.698728，同 A-02／A-05／A-09）。
             Browning 面北 fov 116：地平線北點 kφ＝67.9 → 畫面中心在北極星下方 0.9（北點 Y≈1600），
             角落距盤心 119.1 < 125.3；頭頂（r＝57.9）也在畫面內（06:00 搖光 84°）。
  x_tN = x_tS = 0

秒數：02 鏡 6→7 秒、17 鏡 6→5 秒（Niitsitapi、tipi 依外文音節計 6 字，6 秒會破 4.5 字/秒；總長仍 179 秒）。

check_shots 的 ⚠（判斷後接受）
  R 鏡頭「畫面含長圖側扇區」：長圖⇄北盤只在 gen_canva_pages 插的換組頁（盤心置中、0°）互切。
"""
import os, sys, json, math, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from make_a16_v4 import vo_units, centroid, lst_at

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-17"
OUT = os.path.join(BASE, "05_素材/A-17_黑腳族/_v4大畫布")
LST0 = 7.0
BRW = (48.556, -113.013)        # Browning, Montana（MST＝UTC−7）
PHI = 48.56
JUPITER = (147.55, 14.14)       # 2027/1/15 J2000（PyEphem）


def rot_at(when):
    L = lst_at(*BRW, -7, when)
    return round((LST0 - L - 180.0 + 180.0) % 360.0 - 180.0, 2)


T_BRW = {"18:00": "2027/1/15 18:00", "20:00": "2027/1/15 20:00", "00:00": "2027/1/16 00:00",
         "06:00": "2027/1/16 06:00"}
ROT = {k: rot_at(v) for k, v in T_BRW.items()}

POLARIS, ALCOR = 11767, 65477
DUB, MER, PHE, MEG, ALI, MIZ, ALK = 54061, 53910, 58001, 59774, 62956, 65378, 67301
CASTOR, POLLUX = 36850, 37826
PLEIADES = [17702, 17847, 17851, 17608, 17499, 17531]
DIPPER = [DUB, MER, PHE, MEG, ALI, MIZ, ALK]
MAINS = [POLARIS] + DIPPER + [ALCOR] + PLEIADES[:1]


def x_of(ra):
    return -(((ra - LST0) + 180.0) % 360.0 - 180.0)


SC_OLD = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")


def load(path, cul):
    d = json.load(open(os.path.join(path, cul, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
        out[c["common_name"]["english"]] = [s for s in segs if len(set(s)) >= 2]
    return out


BF = load(SC_OLD, "blackfoot")
EG = load(SC_NEW, "egyptian")
SEG_SEVEN = BF["Seven Brothers and Their Sister"]        # 北斗一筆（輔星的空線段已濾掉）
SEG_TWINS = BF["Ashes-Chief and Stuck-Behind"]
SEG_FING = BF["Spider Man's Fingers"]
SEG_LODGE = BF["Lodge of the Spider Man"]
SEG_LEG = EG["Bull's Foreleg"]

LG_SEVEN = [(SEG_SEVEN, "amber", 1.0)]
LG_LEG = [(SEG_LEG, "red", 1.0)]
LG_ALL = LG_SEVEN + [(SEG_TWINS, "green", 0.9), (SEG_LODGE, "purple", 0.9), (SEG_FING, "blue", 0.8)]
LINE_SETS = [(LG_SEVEN, "連線-七兄弟和小妹"), (LG_LEG, "連線-牛的前腿")]
LINES_KEY = {"L4": "星座連線", "七": "連線-七兄弟和小妹", "埃": "連線-牛的前腿"}
LINE_GROUPS = {"L4": LG_ALL, "七": LG_SEVEN, "埃": LG_LEG}

# (錨點, 原文／紀錄名, 英文, 中文, 顏色, 來源)
TERMS = [
    (DIPPER, "Seven Brothers", "Seven Brothers and Their Sister", "七兄弟和小妹（北斗）", "amber",
     "McClintock 1910 pp.488–489；Stellarium blackfoot 001。黑腳語 Ihkitsikammiksi（「七個人」，Rothney Observatory 引 Glenbow；拼法待查，畫面不放）"),
    ([ALCOR], "Sinopa", "Kit-Fox (Little Sister)", "小妹「小狐狸」（輔星）", "amber", "McClintock p.488"),
    ([ALK], "Last Brother", "Last Brother", "最後一個弟弟（搖光）", "amber", "McClintock p.488、附錄 p.521"),
    ([POLARIS], "Star that Stands Still", "Star that Stands Still", "站著不動的星（北極星）", "white",
     "McClintock pp.499–500：天上的一個洞，太陽家裡的光從洞裡透出來"),
    (JUPITER, "Poïa", "Scarface", "疤臉＝木星", "amber",
     "McClintock pp.491–499；年輕的晨星。位置＝2027/1/15 木星（PyEphem），星點層沒有行星，標籤附「●」"),
    (PLEIADES, "Lost Children", "Lost Children／Bunched Stars", "走失的孩子（昴宿）", "amber",
     "McClintock p.490；Wissler & Duvall pp.71–72。黑腳語 Miohpoisiks 等拼法不一，畫面不放"),
    ((85.0, 28.0), "Wolf Trail", "Wolf Trail", "狼的路（銀河）", "blue",
     "McClintock p.498；錨點＝御夫座一帶的銀河（示意位置）"),
    (DIPPER, "Bull's Foreleg", "Bull's Foreleg (Meskhetyu)", "牛的前腿（古埃及）", "red",
     "Stellarium egyptian 001；下集 A-18 預告"),
]


def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=45, D_r=49, D_fill=0,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None, maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")

    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        if len(a) == 1:
            return {"hip": a[0]}
        ra, dec = centroid(a, S)
        return {"ra": ra, "dec": dec}

    def item(a, text, color, size, dx, dy, key):
        return dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2), dy=round(dy, 2), key=key)

    T = {t[1]: t for t in TERMS}

    def term(name, dx, dy, s1=1.6, s2=1.2, gap=2.4, bullet=False):
        a, orig, _, zh, col, _ = T[name]
        out = [item(a, orig, col, s1, dx, dy + gap / 2, name),
               item(a, zh, "white", s2, dx, dy - gap / 2, name + "-zh")]
        if bullet:
            out.insert(0, item(a, "●", col, 1.2, 0.0, 0.0, name + "-點"))
        return out

    RS = dict(s1=3.4, s2=2.8, gap=3.8)              # 北盤 fov 116
    RC = dict(s1=1.7, s2=1.35, gap=2.5)             # 北盤推近 fov 46–50
    LB_SEVEN = term("Seven Brothers", 0.0, 22.0, **RS)
    LB_SEVEN_C = term("Seven Brothers", 10.0, -8.0, **RC) + term("Sinopa", 15.0, -12.0, **RC)
    RL = dict(s1=2.8, s2=2.4, gap=3.2)
    LB_LAST18 = term("Last Brother", -4.0, 17.0, **RL)    # 18:00：搖光在左端、貼著地平線 → 字放上方
    LB_LAST00 = term("Last Brother", -20.0, -9.0, **RL)   # 00:00：搖光在右下 → 字放左下（右邊會出畫）
    LB_POLE = term("Star that Stands Still", 0.0, -4.0, **RC)
    LB_POIA = term("Poïa", 0.0, -3.4, bullet=True)
    LB_LOST = term("Lost Children", 0.0, -4.2)
    LB_WOLF = term("Wolf Trail", 0.0, 0.0, s1=2.0, s2=1.5, gap=2.9)
    LB_LEG = term("Bull's Foreleg", 0.0, -12.0, s1=2.4, s2=2.0, gap=3.0)

    label_sets = [(LB_SEVEN, "七兄弟和小妹"), (LB_SEVEN_C, "七兄弟和小妹-近"), (LB_LAST18, "最後一個弟弟-18點"), (LB_LAST00, "最後一個弟弟-0點"),
                  (LB_POLE, "站著不動的星"), (LB_POIA, "疤臉"), (LB_LOST, "走失的孩子"),
                  (LB_WOLF, "狼的路"), (LB_LEG, "牛的前腿")]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_ALL)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    m.L_marks(MAINS, "主角星白點", "dot")
    m.L_marks([ALCOR], "輔星細圈", "ring")
    for items, name in label_sets:
        m.L_labels(items, name)
    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS,
                  marks=[(MAINS, "主角星白點", "dot"), ([ALCOR], "輔星細圈", "ring")])

    # ════════════════════ 鏡頭 ════════════════════
    yp = m.y_pole

    def disc_on(hips, rot, fov, dy=0.0):
        ra, dec = centroid(hips, S) if len(hips) > 1 else S[hips[0]][:2]
        q = m.to_disc_local(m.p_disc(m.xw(ra), dec, True), True)
        a = math.radians(-rot)
        x, y = q[0] * math.cos(a) - q[1] * math.sin(a), q[0] * math.sin(a) + q[1] * math.cos(a)
        return (round(x, 2), round(yp + y + dy, 2), fov, rot)

    def FB(t):                                   # Browning 面北：地平線北點 Y≈1600
        return (0.0, round(yp - 0.9, 2), 116.0, ROT[t])

    HAND = (0.0, round(yp, 2), 48.0, 0.0)
    xp = x_of(S[17702][0])
    PLE0 = (round(xp + 4, 2), 16.0, 48.0, 0.0)          # 昴宿＋畢宿＋御夫腳下
    PLE1 = (round(xp, 2), 22.0, 26.0, 0.0)
    DIP = disc_on(DIPPER, ROT["20:00"], 50.0)
    POLE = (0.0, round(yp, 2), 40.0, ROT["06:00"])
    xj = x_of(JUPITER[0])
    JUP0 = (round(xj + 12, 2), 2.0, 48.0, 0.0)          # 木星＋北河（雙子）
    JUP1 = (round(xj, 2), 10.0, 30.0, 0.0)
    PLE2 = (round(xp, 2), 18.0, 30.0, 0.0)
    PLE3 = (round(xp - 6, 2), 18.0, 30.0, 0.0)           # 畫面中心往東（左）移＝昴宿往西（右）沉
    MWV = (-72.0, 0.0, 50.0, 0.0)                         # 英仙—御夫—雙子的銀河
    LEG = disc_on(DIPPER, 0.0, 60.0)
    HZ = [PHI]

    def ls(*n):
        return list(n)

    shots = [
        dict(code="01", kind="Z", sec=12, north=True, frames=[PLE0, PLE1], layers=[], labels=[],
             labels_end=ls("走失的孩子"),
             vo="上週在納瓦荷，北斗是一個繞著爐火轉的男人。今天往北，到洛磯山東邊的大平原：同一片星空，"
                "黑腳族看見——一群走失的孩子。",
             card="同一片星空，黑腳族看見——一群走失的孩子。",
             note="開場字卡；長圖推近昴宿（北斗在北盤，長圖上滑不過去：開場直接從昴宿起）"),
        dict(code="02", kind="Z", sec=7, north=True, frames=[PLE1], layers=[], labels=ls("走失的孩子"),
             overlay="C-A17-01_三層的帳篷", overlay_layers=["帳篷層", "夜空層", "大地層"],
             vo="黑腳族自稱 Niitsitapi，「真正的人」，以前住在大平原的圓錐帳篷 tipi 裡。",
             card="自稱：真正的人",
             note="畫面不動；定格疊 C-A17-01：帳篷層對 02、夜空層對 03、大地層對 04（03、04 同一格，不另疊）；"
                  "不重現任何真實帳篷的圖案、不用照片"),
        dict(code="03", kind="Z", sec=14, north=True, frames=[PLE1], layers=[], labels=ls("走失的孩子"),
             vo="一百多年前，一位美國作者數過：他們夏季的大營地裡，十頂帳篷就有一頂畫了圖。最上面那一圈塗黑，"
                "是夜空：畫著北斗、昴宿，還有一個十字——晨星。",
             card="帳篷頂上是夜空", note="同 02 的畫面；C-A17-01 夜空層在 02 的概念圖頁"),
        dict(code="04", kind="Z", sec=7, north=True, frames=[PLE1], layers=[], labels=ls("走失的孩子"),
             vo="最下面一圈是大地，畫著一排圓點，叫「塵土星」：據說是掉下來的流星。",
             card="塵土星＝落下的流星", note="同 02 的畫面；C-A17-01 大地層在 02 的概念圖頁"),
        dict(code="05", kind="R", sec=13, north=True, horizon=HZ, frames=[HAND, FB("20:00")], layers=["七"],
             labels=ls("七兄弟和小妹"), labels_start=[],
             overlay="C-A17-02_逃上天", overlay_layers=["熊層", "箭層", "樹叢層", "湖層", "大樹層"],
             vo="北斗是七兄弟和小妹。家裡的大姊嫁給了一頭灰熊；族人殺了灰熊，她披上熊皮、變成大熊，"
                "把營地裡的人都殺了，只留下最小的弟弟和小妹。",
             card="七兄弟和小妹",
             note=f"【換北盤】Browning 1/15 20:00 面北（{ROT['20:00']:+.1f}°；山＝北方地平線）；"
                  "北斗（琥珀）＋輔星細圈；角落小字「連線：Miller 1997 依文獻所畫」；迄格定格疊 C-A17-02 "
                  "（熊層對 05；箭、樹叢、湖、大樹四層對 06——06 同一格，不另疊）"),
        dict(code="06", kind="R", sec=15, north=True, horizon=HZ, frames=[FB("20:00")], layers=["七"],
             labels=ls("七兄弟和小妹"),
             vo="六個哥哥回來，帶著弟妹逃。最小的弟弟有法力：射出一支箭，大家就飛到箭落的地方；揮一下羽毛，"
                "長出樹叢、變出湖。最後他們爬上一棵大樹，熊撞下了四個——",
             card="箭、羽毛、湖、大樹", note="同 05 迄格；C-A17-02 後四層在 05 的概念圖頁"),
        dict(code="07", kind="R", sec=15, north=True, horizon=HZ, frames=[FB("20:00"), DIP], layers=["七"],
             labels=ls("七兄弟和小妹-近"), labels_start=ls("七兄弟和小妹"),
             vo="他唱：「除了天上，沒有地方可以得救。」一箭一箭射向天，妹妹、哥哥們，最後是他自己。"
                "斗口四顆，是被熊撞下樹的四個哥哥；斗柄旁小小的輔星，是小妹 Sinopa，「小狐狸」。",
             card="斗柄旁的小妹", note="推近北斗（fov 50）；輔星（HIP 65477）細圈＋Sinopa 標籤"),
        dict(code="08", kind="R", sec=9, north=True, horizon=HZ,
             frames=[DIP, FB("18:00"), FB("00:00")], layers=["七"], labels=ls("最後一個弟弟-18點"),
             labels_start=ls("七兄弟和小妹-近"),
             vo="沒有時鐘的年代，北斗就是時鐘。半夜想知道幾點，就問一句：「最後一個弟弟，現在指向哪裡？」",
             card="最後一個弟弟指向哪？",
             note=f"拉回 fov 116、回到 18:00（{ROT['18:00']:+.1f}°），再逆時針轉到 00:00（{ROT['00:00']:+.1f}°；每段 < 180°）；"
                  "00:00→06:00 併入 09 鏡（「最後一個弟弟」標籤 18:00、00:00 各放一版）"),
        dict(code="09", kind="R", sec=10, north=True, horizon=HZ, frames=[FB("00:00"), FB("06:00"), POLE], layers=["七"],
             labels=ls("站著不動的星"), labels_start=ls("最後一個弟弟-0點"), overlay="C-A17-天上的洞",
             vo="北斗繞著的北極星，叫「站著不動的星」。他們說，那其實是天上的一個洞，太陽家裡的光從洞裡透出來。",
             card="北極星＝天上的洞",
             note=f"繼續逆時針 00:00→06:00（{ROT['06:00']:+.1f}°；搖光轉到頭頂 84°），再推近北極星；迄格疊 C-A17-天上的洞_透明.png（1080×1920 滿版，暖光圈圓心＝畫面中心＝北極星）"),
        dict(code="10", kind="Z", sec=12, north=True, frames=[JUP0], layers=[], labels=[],
             overlay="C-A17-03_羽毛女與洞", overlay_layers=["天上層", "洞層"],
             vo="有個女孩叫羽毛女，嫁給了晨星，住到天上。天上的人警告她：別挖那棵大蕪菁。她還是挖了——"
                "從洞裡往下看，看見了地上的家。",
             card="不能挖的大蕪菁",
             note="【換長圖】盤轉回 0°、換回長圖、下到出發點 → 滑到獅子座（木星）；定格疊 C-A17-03（不畫人臉）"),
        dict(code="12", kind="Z", sec=11, north=True, frames=[JUP0, JUP1], layers=[], labels=ls("疤臉"),
             vo="她的兒子臉上有疤，被叫 Poïa，「疤臉」。他走到太陽的家，疤被除去，帶回了太陽舞；後來，"
                "他也成了一顆晨星——就是木星。",
             card="疤臉 Poïa＝木星", note="推近 2027/1/15 的木星位置（獅子座，軒轅十四西北）；不畫太陽舞"),
        dict(code="14", kind="S", sec=13, north=True, frames=[JUP1, PLE2], layers=[], labels=ls("走失的孩子"),
             vo="再來是昴宿：「走失的孩子」。春天獵到野牛，小牛皮是黃的，孩子們都披著黃色小牛皮玩；"
                "只有一家六個窮孩子沒有，被大家笑是「長癬的老公牛」。",
             card="走失的孩子", note="往西（右）滑過雙子、御夫到昴宿；Stellarium 沒有昴宿連線，只標名字"),
        dict(code="15", kind="S", sec=14, north=True, frames=[PLE2, PLE3], layers=[], labels=ls("走失的孩子"),
             overlay="C-A17-04_春天看不見", overlay_layers=["日曆層", "回來層"],
             vo="他們不好意思回家，在草原上走失，被帶上了天。所以每年春天，小牛還是黃的時候，天上看不到他們；"
                "等到秋天小牛轉成褐色，他們才每晚回來。",
             card="春天看不見他們",
             note="畫面中心往東（左）移、昴宿相對往右（西）滑；迄格定格疊 C-A17-04（Browning：5/1 最後一次黃昏可見 → 6/24 清晨回來）"),
        dict(code="17", kind="Z", sec=5, north=True, frames=[PLE3, MWV], layers=[], labels=ls("狼的路"),
             vo="銀河呢？叫「狼的路」，是天上和人間之間最近的一條路。",
             card="銀河＝狼的路", note="拉遠到英仙—御夫—雙子一段的銀河"),
        dict(code="18", kind="Z", sec=13, north=True, frames=[MWV], layers=[], labels=ls("狼的路"),
             overlay="C-A17-05_今晚與明晨",
             vo="今晚八點，昴宿就在頭頂。明天清晨五點半往東南看，最亮的那顆就是晨星，金星；"
                "而晚上七點半從東方升起的木星，是他的兒子 Poïa。",
             card="今晚與明晨", note="定格疊 9:16 圖卡 C-A17-05（台北 1/15 20:00、1/16 05:30；可存圖）"),
        dict(code="19", kind="R", sec=9, north=True, frames=[HAND, LEG], layers=["埃"], labels=ls("牛的前腿"),
             labels_start=[],
             vo="下週五，我們去古埃及：北斗在那裡，是一條牛的前腿；而天狼星一回來，尼羅河就要漲水。",
             card="下集見｜古埃及：叫醒尼羅河的天狼星",
             note="【換北盤】推到北斗，古埃及「牛的前腿」連線（紅）淡入；端卡＋追蹤 CTA"),
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
            if sh["kind"] == "R":
                yc = m.y_pole if sh["north"] else -m.y_pole
                which = ("北盤" if sh["north"] else "南盤") + "圖層組（置中）"
                ew = 2 * m.R_fill / fov * 1080
                off = (round(-cx / fov * 1080), round((cy - yc) / fov * 1080))
            else:
                which = "大畫布圖層組"
                ew = 360.0 / fov * 1080
                off = (round(-cx / fov * 1080), round(cy / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"], "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": which, "元素寬px": round(ew), "位移X px": off[0], "位移Y px": off[1],
                         "旋轉度": round(rot, 1), "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[dict(s) for s in shots])
    print("  北盤旋轉角（Browning 1/15–16，面向北方）：" + "、".join(f"{k} {v:+.1f}°" for k, v in ROT.items()))
    print(f"  x：昴宿 {xp:+.1f}、木星 {xj:+.1f}、北河二 {x_of(S[CASTOR][0]):+.1f}；DIP {DIP}；LEG {LEG}")

    terms = {}
    for hips, orig, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=hips if not isinstance(hips, tuple) else [], 原文=orig, 拼音="", 英文翻譯=en,
                           中文=zh, 顏色=col, 來源備註=note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "rot_browning": ROT, "lst0": LST0, "phi": PHI},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=LG_ALL + LG_LEG,
                  labels=[dict(it, pt=6) for it in items], title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_ALL)
    m.sb_grid(os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), shots, line_groups=LG_ALL,
              labels=[dict(it, pt=5) for items, _ in label_sets for it in items],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
