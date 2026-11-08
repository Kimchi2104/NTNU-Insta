# A-33｜毛利 Matariki：星星升起就是新年（萬國星空 EP46）・v0（初稿・待查核）

> ⚠️ **排程已改（2026-10-31）**：本集改到 **2027/6/25（Matariki 國定假日）** 播出（原 6/4），配合 A-33 Matariki 對上 6/25 國定假日、現代星座上下集相鄰。本稿的「星空對時」、觀星段與「今晚」的天象仍是舊日期，**v1 時依新日期用 PyEphem 重算**。

| 項目 | 內容 |
|---|---|
| 發布 | **2027/06/25（五）20:00**＝紐西蘭 Matariki 國定假日（10/31 排程調整，原 6/4；天象 v1 重算） |
| 時長 | **215 秒**（14 鏡頭；節目表原訂 180 秒） |
| 格式 | Reels 9:16；**長圖帶狀**（昴宿特寫＋九星標籤層、獵戶參宿七、天蠍心宿二）＋概念圖 6 組（假日、挑日子、兩個季節、黎明重現、hautapu、北島示意）＋9:16 圖卡 2 張；不用盤（昴宿 dec +24°，在長圖帶內） |
| 來源 | Stellarium **maori**（新版 `stellarium-master/skycultures`；Dan Smale；CC BY-SA 4.0；引 Best 1955、1959、Leather & Hall 2004、Orbell 1996 等）；Rangi Mātāmua《Matariki: The Star of the Year》（2017；據 Te Kōkau Himiona Te Pikikōtuku 與 Rāwiri Te Kōkau 1933 年完成的手稿）；紐西蘭政府 MBIE／employment.govt.nz（Matariki 假日）、Matariki Advisory Group《Matariki dates 2022 to 2052》；Te Papa（Puanga 與 Matariki；假日日期與 Tangaroa 期）；Te Ara（Matariki 預測年景、各地以 Puanga 為新年）；RNZ 2025（Che Wilson 談 Puanga）；天象全部 PyEphem 4.2.1 自算 |
| 配音 | 逐字稿 **794 字**（中文字＋外文音節；毛利語按母音計音節），平均 **3.69 字/秒**；最快一格 08 鏡 **4.07**（上限 4.5） |
| 統一開頭 | 「同一片星空，毛利人看見——新的一年。」 |
| 承接 | EP45（A-36）現代星座（下）（結尾「下週五，紐西蘭放 Matariki 假：昴宿在黎明升起，就是新年。」）→ **EP46 毛利 Matariki：星星升起就是新年**（6/25＝紐西蘭 Matariki 國定假日）→ EP47（X-07）銀河環球：一條河、一條路、一道縫（7/2） |

> ⚠️ **節目表的鉤子要改**：原「紐西蘭唯一的原住民國定假日，由星星決定日期」。①「唯一的原住民國定假日」講不清楚——政府的說法是「**第一個**承認毛利世界觀（Te Ao Māori）的國定假日」（employment.govt.nz；2022 年阿爾登總理）；②日期不是只看星星：Matariki Advisory Group 是在毛利月曆 Pipiri 這個月裡，取月相 **Tangaroa** 那幾晚（下弦前後）**最近的星期五**，2022–2052 的日期已寫進《Te Kāhui o Matariki Public Holiday Act 2022》。建議改成：「**紐西蘭第一個為毛利世界觀放的假：日期看星星，也看月亮**」。
> ⚠️ **節目表的備註要補日期**：「對齊當年 Matariki 公告週（6 月中下旬晨空）」——2027 年的假日是 **6/25（五）**，Te Papa 列的 Tangaroa 期是 6/27–30；昴宿在紐西蘭黎明重現約 **6/11–13**（PyEphem，見星空對時）。本集 6/4 播出，比假日早三週，片中當「預告」寫。**可選**：若想在假日當週播，可跟 A-35（6/25）對調，但 A-32 的結尾句與 A-34 的開場要跟著改。
> ⚠️ **節目表的星圖需求要改**：原「北盤＋Matariki(昴宿)/Te Waka 大舟連線層」。①昴宿 dec +24°，在長圖帶內，不需要北盤；紐西蘭的黎明地平線用概念圖畫比較清楚。②**Te Waka-o-Tamarereti 的指認各家不一**：Stellarium maori 把它連在天蠍尾巴；Martinborough Star（Phoenix Astronomical Society 系統）說是貼著地平線的整條銀河，船尾是獵戶腰帶 Tautoru、船頭是天蠍 Te Matau-a-Māui；Museums Wellington 說「Tamarereti 的船頭」是天蠍的名字之一。這條留給 X-07 處理（X-07 v0 已改用毛利的銀河名 Te Ikaroa／Te ika o te rangi，並註明 Te Waka 在 Stellarium 是天蠍尾巴），本集不畫。
> ⚠️ **節目表的素材來源要注意**：`_整理CSV/Maori in Oceania.csv` 的繁中欄被 po 檔表頭（「Project-Id-Version: 1.0…」）污染；九顆星的名字沒有長音符號（Waiti、Waita、Tupuarangi、Tupuanuku、Pohutukawa、Waipunarangi）；Stellarium 舊版 references 還寫著「stars in Matariki also randomly labelled」——但新版 index.json 的 HIP 對應跟 Mātāmua／Te Papa 的對法一致（見星名表），片中照後者、加上長音符號。

> **資料來源挖掘重點（第〇節檢查表）**
> 1. **本文化的鄰居**：Stellarium maori 只有 6 個星座、24 個具名天體，主題是**航海與季節**：Te Ra-o-Tainui「Tainui 號的帆」（腰帶＝龍骨、畢宿＝蟹爪帆、昴宿＝船頭）、Tau-toro（腰帶）、Matakarehu（畢宿）、南十字 Taki-o-Autahi、南門二與馬腹一 Te Taura（船的繩）、天蠍尾巴 Te Waka-o-Tama-rereti。昴宿周圍 ±45°：Puanga（參宿七）、Taumata-kuku（畢宿五）、Takarua（天狼）、Whakaahu（北河二）——**冬天的星全是「季節鐘」**：Matariki 與 Puanga 在冬天黎明重現＝新年。論點＝「天上的時鐘決定一個國家的假期」；X-01 只講了名字家族（mata-liki）和「2022 年起放假」，本集往下挖：日期怎麼算、九顆星各管什麼、為什麼西岸看 Puanga、台灣什麼時候看得到。
> 2. **跨文化同星群**：昴宿在 X-01 已做足（約 40 個文化）。本集只用兩條：①**黎明重現＝新年**：毛利（6 月中，南半球冬至）、阿拉伯半島（6/7 昴宿晨升開夏季，A-13）、Hesiod「昴升起就收割」（X-01）——同一天前後，南半球在冬天、北半球在夏天；②**九顆 vs 七顆**：希臘七姊妹＋父母 Atlas、Pleione＝九顆有名字的星，Mātāmua 的九星恰好也是九顆，對到同樣九顆（Matariki＝Alcyone、Tupuārangi＝Atlas、Tupuānuku＝Pleione……）。
> 3. **恆星物理／天象**：九顆星的 V 星等（`03_星點座標表.csv`）：Matariki 2.87、Tupuārangi 3.63、Waipuna-ā-rangi 3.70、Waitī 3.87、Ururangi 4.18、Waitā 4.30、Tupuānuku 5.09、Hiwa-i-te-rangi 5.46、Pōhutukawa 5.76——**Mātāmua 加進來的兩顆（Pōhutukawa、Hiwa）正好是最暗的兩顆**；2027/5/21 太陽離昴宿最近（4.1°）；黎明重現（太陽在地平下 12° 時昴宿六高 ≥3°）：台北 6/7、利雅德 6/7、奧克蘭 6/11、新普利茅斯 6/12、威靈頓 6/13；Puanga（參宿七）在紐西蘭 6/5–7 就重現，比昴宿早一週；南半球冬至 6/22 02:11（紐西蘭時間），威靈頓白天 9.2 小時、台北 13.7 小時。
> 4. **文獻**：Mātāmua 2017（九星與各自照看的領域；手稿 1933 年完成）；MBIE／employment.govt.nz（2022/6/24 第一次放假、「first public holiday to recognise Te Ao Māori」）；Matariki Advisory Group 日期表（2022–2052，2027＝6/25）；Te Papa（2027 Tangaroa 期 6/27–30；Puanga 與 Matariki 的差別，引 Che Wilson）；Te Ara（星清楚＝暖和豐收、朦朧＝冷冬；Taranaki、Whanganui、Rangitīkei 等以 Puanga 為新年）；RNZ 2025（Che Wilson：看 Puanga 是因為它更能預告西岸天氣）。
> 5. **原始出處看到底**：①Stellarium maori 舊註記說九星標籤「random」，新版的 HIP 對應已跟 Mātāmua 一致——但 Atlas／Pleione 對 Tupuārangi／Tupuānuku 在部分網路海報是反過來的，要核 Mātāmua 原書；②Stellarium 的名字都沒有長音符號，也把 Waipuna-ā-rangi 寫成 Waipunarangi；③Stellarium 把 Te Waka-o-Tama-rereti 放在天蠍尾巴，跟其他毛利天文資料不一致（見⚠）；④「Matariki＝天神之眼（mata ariki）」是 X-01 講過的一說，另一說是「小小的眼睛」（mata riki），本集不再講；⑤Tāwhirimātea 挖出眼睛丟上天的故事，這次搜尋沒找到一手出處，片中不講；⑥九星裡誰是男、誰是女，各來源說法不一，片中不講性別（只說 Matariki 是母親）；⑦CSV 的繁中欄被 po 表頭污染（見⚠）。
> 6. **去處**：主線＝承接 → 假日（2022 起、2027＝6/25）→ 日期看星星＋月亮 → 南半球的冬至 → 台灣比紐西蘭早看到 → 看清楚＝看年冬 → 九顆星與手稿 → 六顆管自然 → 母親、願望、離開的人＋最暗的兩顆 → hautapu → 西岸看 Puanga → 今晚台灣看不到、六月中清晨 → 下集；字卡＝假日日期、星星＋月亮、南半球冬至、台灣 6/7、看年冬、九顆星、六個領域、最暗的兩顆、hautapu、Puanga、六月中清晨；圖卡＝九星小辭典、這週抬頭看；首留言＝日期規則、九星表、手稿、Puanga、重現日期表。

---

## 逐字稿＋分鏡

| 鏡 | 秒數 | 旁白（逐字） | 字卡（畫面大字，可空） | 畫面構想 | 字/秒 |
|---|---|---|---|---|---|
| **01** Z | 0–13s（13） | 上週，我們數了課本沒教的星群。今天，紐西蘭放 Matariki 假：同一片星空，毛利人看見——新的一年。 | 同一片星空，／毛利人看見——新的一年。 | 長圖 fov 40→12：從獵戶—金牛推近昴宿；Matariki 標籤；開場字卡 | 36 字／2.73 |
| **02** — | 13–31s（18） | 二〇二二年起，紐西蘭多了一個國定假日，叫 Matariki。政府說，這是第一個承認毛利世界觀的國定假日。它每年日期都不一樣：二〇二七年，是六月二十五號，星期五。 | 2027 Matariki 假日：6/25 | 定格疊概念圖 C-A33-01「Matariki 假日」：2022/6/24 第一次 → 2026/7/10 → 2027/6/25（五）；「第一個承認 Te Ao Māori 的國定假日」中譯；慶典照片美宣另尋授權圖 | 66 字／3.67 |
| **03** Z | 31–44s（13） | 日期由天上決定。Matariki 就是昴宿：每年五月，它在黃昏沉進西方，躲進太陽的光裡；六月，再從冬天的黎明裡冒出來。 | Matariki＝昴宿 | 長圖 昴宿＋太陽位置標記：5/21 太陽離昴宿最近（約 4°）→ 6 月太陽往東移開；兩格 Match & Move | 47 字／3.62 |
| **04** — | 44–61s（17） | 假日還要對上毛利的月曆：在 Pipiri 這個月，月亮走到叫 Tangaroa 的那幾晚，大約下弦月前後，再挑最近的星期五。今年的 Tangaroa，是六月二十七到三十號。 | 星星＋月亮＝放假日 | 定格疊概念圖 C-A33-02「怎麼挑日子」：Pipiri 月曆條（6/5 新月 → 6/27 下弦）、Tangaroa 6/27–30 標色、最近的星期五 6/25 圈起 | 63 字／3.71 |
| **05** — | 61–76s（15） | 為什麼在六月？南半球的六月是冬天：冬至那天，威靈頓的白天只有九個多小時。最冷、最暗的時候，昴宿回來了——舊的一年結束，新的一年開始。 | 南半球的冬至 | 定格疊概念圖 C-A33-03「同一天、兩個季節」：6/21 台北白天 13.7 小時 vs 威靈頓 9.2 小時（日出日落時刻） | 56 字／3.73 |
| **06** — | 76–92s（16） | 台灣其實更早看到：這週昴宿還躲在太陽旁邊，大約六月七號起，清晨四點，東北東的地平線上就會冒出來；紐西蘭要再晚幾天，六月中才看得清楚。 | 台灣 6/7 前後清晨 | 定格疊概念圖 C-A33-04「黎明重現」：東方地平線示意（太陽在地平下 12° 那一刻）：台北 6/7 昴宿高 3°（方位 65°）、奧克蘭 6/11 3°（57°）、威靈頓 6/13 3°（54°） | 59 字／3.69 |
| **07** Z | 92–105s（13） | 看到還不夠，還要看清楚。長老在天亮前仔細看這群星：清楚又明亮，來年溫暖豐收；朦朧不清，就要準備過一個冷冬。 | 看清楚＝看年冬 | 長圖推近 fov 3：昴宿特寫，九顆主角星白點＋光暈 | 46 字／3.54 |
| **08** Z | 105–120s（15） | 近年最受注目的，是九顆星的說法。毛利天文學者 Rangi Mātāmua，整理祖先在一九三三年完成的手稿，替 Matariki 的九顆星，各自配上它們照看的東西。 | Matariki 的九顆星 | 長圖 fov 2.6：九星標籤層（毛利原名，長音符號照原文）逐一淡入；不放 Mātāmua 書封（版權） | 61 字／4.07 |
| **09** Z | 120–135s（15） | Tupuānuku 管土裡長的食物，Tupuārangi 管樹上和天上來的食物；Waitī 管淡水，Waitā 管大海；Waipuna-ā-rangi 管雨，Ururangi 管風。 | 土・樹・淡水・海・雨・風 | 同框；六顆依序高亮＋小圖示（土、樹、水滴、浪、雨、風）；結束疊 9:16 圖卡 C-A33-05「Matariki 九星小辭典」（可存圖） | 51 字／3.40 |
| **10** Z | 135–153s（18） | Matariki 是母親，照看人們的健康；Hiwa-i-te-rangi 收下新年的願望；Pōhutukawa 代表過去一年離開的人。有趣的是，這兩顆是九顆裡最暗的，要在很黑的地方才看得到。 | 最暗的兩顆 | 同框；Matariki（2.9 等）高亮 → Hiwa-i-te-rangi（5.5 等）、Pōhutukawa（5.8 等）圈出 | 66 字／3.67 |
| **11** — | 153–167s（14） | 所以 Matariki 的儀式，有點像我們的除夕：天亮前生火煮食物，讓熱氣升上天，獻給這群星；念出離開的人的名字，也說出新年的願望。 | 天亮前的 hautapu | 定格疊概念圖 C-A33-06「hautapu」：地爐的熱氣升向昴宿的示意（不畫人物、不仿任何既有插畫）；若要用儀式照片，美宣另尋授權並確認可公開 | 53 字／3.79 |
| **12** S | 167–185s（18） | 但不是每個部族都看昴宿。北島西岸的 Taranaki、Whanganui 等部族，新年看的是 Puanga——參宿七。有的地方被山擋住看不清昴宿；也有長老說，Puanga 更能預告西岸的天氣。 | 西岸看 Puanga | 長圖往左下（東南）捲到獵戶：參宿七 Puanga 標籤；右下小框：北島示意地圖（自繪，標 Taranaki、Whanganui、Rangitīkei） | 68 字／3.78 |
| **13** Z | 185–203s（18） | 今晚八點，台灣看不到這兩位主角，它們都躲在太陽附近。往東南方低空看，紅色的心宿二已經升起，毛利人叫它 Rehua。想看 Matariki，就等六月中的清晨，跟紐西蘭一起迎新年。 | 6 月中・清晨・東北東 | 【硬切】長圖 天蠍：心宿二 Rehua 標籤；結束疊 9:16 圖卡 C-A33-07「這週抬頭看」（台北 6/4 20:00；6/7、6/14、6/25 清晨昴宿高度，可存圖） | 71 字／3.94 |
| **14** — | 203–215s（12） | 下週五，我們沿著銀河繞地球一圈：有人看見一條河，有人看見一條路，也有人看見一道縫。 | 下集｜銀河環球 | 端卡（背景：長圖夏季銀河）＋「下集見｜銀河環球：一條河、一條路、一道縫」＋追蹤 CTA | 36 字／3.00 |

> **全片在大畫布（長圖）上**，01–11 都在金牛—獵戶一帶（昴宿特寫 fov 2.6–3），12 往東南捲到參宿七，13 硬切到天蠍；02、04、05、06、11 是定格疊概念圖。
> **九星標籤層**：毛利原名（含長音符號）＋中文領域兩行；特寫時九顆星的白點照 V 星等畫大小，讓「最暗的兩顆」看得出來。
> **字卡**：每張 ≤14 字；「／」表示分兩張。

---

## 星空對時（PyEphem 4.2.1 自算；含大氣折射；「黎明重現」＝太陽在地平下 12° 那一刻，昴宿六 Alcyone 高度 ≥3° 的第一天）

**2027/6/4（五）台北（25.033°N、121.565°E、UTC+8）——13 鏡「今晚八點」**

| 時刻 | 事件 |
|---|---|
| 17:42 | 昴宿六落下（在日落前，整晚看不到） |
| 18:05 | 參宿七落下（同上） |
| 18:24 | 心宿二升起 |
| 18:41 | 日落；20:09 天文昏影結束 |
| **20:00** | **心宿二 17°（方位 131°，東南）**；尾宿八 0.4°；角宿一 53°（168°）；大角 71°（104°）；織女 19°（55°）；南十字 γ 星 7.7°、十字架一 1.9°（正南，貼地）；火星 55°（250°）、木星 42°（269°）；月亮在地平下 |
| 21:00 | 心宿二 27°（142°）；尾宿八 10° |
| 22:00 | 心宿二 34°（155°）；尾宿八 18° |
| 6/5（六）03:40 | 新月（Pipiri 月從這天算起；毛利月曆的新月期叫 Whiro） |
| 6/5（六）03:59 | 昴宿六升起（日出 05:03）——太陽在地平下 12°（04:07）時昴宿只高 1.5°，還看不到 |
| 行星星等（Mallama & Hilton 2018） | 木星 −1.91、火星 +0.80（片中不提） |

**昴宿的黎明重現（太陽在地平下 12° 時昴宿六的高度；台北時間 UTC+8、紐西蘭 NZST UTC+12）——03、06 鏡**

| 地點 | 首次 ≥3° | 6/25（假日）同一時刻 | 方位 |
|---|---|---|---|
| **台北** | **6/7（04:07，3.0°）** | 04:09，18.0° | 東北東 65°→71° |
| 利雅德（A-13 對照） | 6/7（04:07，3.2°） | — | 65° |
| 奧克蘭 36.85°S | 6/11（06:28，3.1°） | — | 東北 57° |
| 新普利茅斯（Taranaki）39.06°S | 6/12 | — | 55° |
| **威靈頓 41.29°S** | **6/13（06:37，3.3°）** | **06:41，10.3°（方位 45°，東北）** | 54°→45° |
| Puanga（參宿七）威靈頓 | **6/5**（3.7°，正東 98°） | 06:41，19.7°（84°） | — |
| Puanga 新普利茅斯／Whanganui | 6/6／6/5 | — | 98° |

（2027/5/21 太陽離昴宿六最近，角距 4.1°。台北 6/14 同一時刻 8.5°、6/25 18.0°——「六月中以後」就好找。紐西蘭 6/25 清晨月亮 73%、在西北高 46°，不會擋到東北方的昴宿。）

**南半球的冬至——05 鏡**

| 地點 | 6/21 日出 | 日落 | 白天長 |
|---|---|---|---|
| 威靈頓 | 07:47 | 16:59 | **9.2 小時** |
| 台北 | 05:04 | 18:47 | 13.7 小時 |

（2027 年 6 月至日：UTC 6/21 14:11＝台北 6/21 22:11＝紐西蘭 6/22 02:11。）

**假日與月相（紐西蘭時間）——04 鏡**

| 項目 | 日期 |
|---|---|
| 新月（Pipiri 月開始的依據之一） | 6/5 07:40 NZST（台北 6/5 03:40） |
| 下弦 | 6/27 16:54 NZST |
| Tangaroa 期（Te Papa 表） | 6/27–30 |
| **Matariki 假日** | **6/25（五）**（Tangaroa 期最近的星期五） |

---

## 星名表（毛利語照 Mātāmua／Te Papa 的寫法，長音符號照原文）

| 毛利名 | Stellarium 拼法 | 意思／照看的領域（Mātāmua） | 西方星名 | HIP | V | 片中 |
|---|---|---|---|---|---|---|
| Matariki | Matariki | 母親；人們的健康與福祉（也是整個星團的名字） | Alcyone（η Tau，昴宿六） | 17702 | 2.87 | 01–03、10、13 |
| Tupuārangi | Tupuarangi | 樹上與天上來的食物（果實、鳥） | Atlas（27 Tau） | 17847 | 3.63 | 09 |
| Tupuānuku | Tupuanuku | 土裡長的食物 | Pleione（28 Tau） | 17851 | 5.09 | 09 |
| Waitī | Waiti | 淡水，與淡水裡的食物 | Maia（20 Tau） | 17573 | 3.87 | 09 |
| Waitā | Waita | 大海，與海裡的食物 | Taygeta（19 Tau） | 17531 | 4.30 | 09 |
| Waipuna-ā-rangi | Waipunarangi | 雨 | Electra（17 Tau） | 17499 | 3.70 | 09 |
| Ururangi | Ururangi | 風 | Merope（23 Tau） | 17608 | 4.18 | 09 |
| Hiwa-i-te-rangi | Hiwa-i-te-rangi | 新年的願望與志向 | Celaeno（16 Tau） | 17489 | 5.46 | 10 |
| Pōhutukawa | Pohutukawa | 過去一年離開的人 | Asterope（21 Tau） | 17579 | 5.76 | 10 |
| Puanga | Puanga | 西岸部族的新年星 | Rigel（β Ori，參宿七） | 24436 | 0.13 | 12 |
| Rehua | Rehua | （夏天的星；本集只用名字） | Antares（α Sco，心宿二） | 80763 | 0.91 | 13 |
| Te Ra-o-Tainui | Te-Ra-o-Tainui | Tainui 號的帆 | 腰帶＋畢宿＋昴宿 | — | — | 首留言 |
| Tau-toro（Tautoru） | Tau-toro | 腰帶三星 | 獵戶腰帶 | 25930、26311、26727 | — | — |
| Te Waka-o-Tamarereti | Te-Waka-o-Tama-Rereti | Tamarereti 的船 | Stellarium：天蠍尾巴（他說不一，見⚠） | — | — | X-07 |

**其他片中用詞**

| 毛利語 | 意思 | 片中 |
|---|---|---|
| Pipiri | 毛利月曆的月名（約 6–7 月；Matariki 重現的那個月） | 04 |
| Tangaroa | 月相名（下弦前後的幾晚；也是海神的名字） | 04 |
| hautapu | Matariki 儀式中獻給星群的食物（whāngai i te hautapu＝餵養星群） | 11 |
| Te Ao Māori | 毛利世界（觀） | 02（中譯） |
| Te Kāhui o Matariki | Matariki 星群（法案名稱） | 首留言 |
| Aotearoa | 紐西蘭的毛利名 | 首留言 |
| Whiro | 新月期（月曆的第一晚） | 星空對時 |

---

## 考據備忘

- **假日**：《Te Kāhui o Matariki Public Holiday Act 2022》（2022 年 4 月三讀）；第一次放假 2022/6/24（五）；2026 年 7/10（X-01 已用）、**2027 年 6/25（五）**。政府說法：「the first public holiday to recognise Te Ao Māori」（employment.govt.nz、阿爾登總理）。片中「第一個承認毛利世界觀的國定假日」。
- **日期規則**：Matariki Advisory Group（主席 Rangi Mātāmua）：在 Pipiri 月（Matariki 黎明重現的那個陰曆月）取 Tangaroa 月相期最近的星期五；2022–2052 年都已排定（MBIE 公布的 PDF）。Te Papa 表：2027 年 Tangaroa 期 6/27–30、假日 6/25。片中「大約下弦月前後」——Tangaroa 那幾晚在下弦附近（2027 下弦 6/27 16:54 NZST），屬推算，Te Papa 的表沒有直接寫「下弦」（待查核 3）。
- **為什麼是冬天**：南半球冬至 6/22（紐西蘭時間）；威靈頓白天 9.2 小時。Te Ara 有一說：Matariki 和她的女兒們出來，是去陪伴冬天走得疲累的太陽 Te Rā——片中沒用。
- **台灣比紐西蘭早看到**：同一個「太陽在地平下 12°、昴宿六高 3°」的條件，台北 6/7、威靈頓 6/13（PyEphem 逐日算）。原因：南半球的冬天清晨，太陽與昴宿都在東北方升起、升起的角度斜，要多等幾天昴宿才離開曙光（推論，片中只說「晚幾天」）。
- **看清楚＝看年冬**：Te Ara：星清楚明亮，來年溫暖豐收；朦朧、擠在一起，就是冷冬（另有 Tūhoe 的說法：星看起來靠得近＝冷、分得開＝暖，跟前者講法不同）。片中「清楚又明亮，來年溫暖豐收；朦朧不清，就要準備過一個冷冬」。
- **九顆星與手稿**：Rangi Mātāmua（Tūhoe；毛利天文學者，2019 年獲紐西蘭總理科學傳播獎）根據家族手稿——Ruatāhuna 的 Te Kōkau Himiona Te Pikikōtuku 與兒子 Rāwiri Te Kōkau 編寫、1933 年由 Rāwiri 完成、約 400 頁——在《Matariki: The Star of the Year》（2017）整理出九顆星：在常見的七顆之外加上 Pōhutukawa 與 Hiwa-i-te-rangi；Matariki 是母親，其餘八顆是她的孩子。很多較早的毛利資料只列七顆（Wikipedia 轉述；待核原書）。片中「近年最受注目的，是九顆星的說法」——不說「真正有九顆」。
- **各星的領域**：Matariki 健康福祉；Tupuānuku 土裡的食物；Tupuārangi 樹上、天上的食物（果實、鳥）；Waitī 淡水；Waitā 海；Waipuna-ā-rangi 雨；Ururangi 風；Hiwa-i-te-rangi 願望；Pōhutukawa 過去一年離開的人（Mātāmua；Te Papa、Science Learning Hub 一致）。
- **西方星名對應**：照 Stellarium 新版 index.json（HIP）＝Wikipedia「Matariki」表（引 Mātāmua）：Matariki＝Alcyone、Tupuārangi＝Atlas、Tupuānuku＝Pleione、Waitī＝Maia、Waitā＝Taygeta、Waipuna-ā-rangi＝Electra、Ururangi＝Merope、Pōhutukawa＝Asterope、Hiwa-i-te-rangi＝Celaeno。有海報把 Atlas／Pleione 對調（Playcentre），也有學生作業把 Maia／Taygeta 對調——片中照 Stellarium＝Wikipedia，但要核原書（待查核 1）。
- **最暗的兩顆**：Pōhutukawa（Asterope，21 Tau，V 5.76；旁邊的 22 Tau 6.4 等）、Hiwa-i-te-rangi（Celaeno，16 Tau，5.46）是九顆裡最暗的；肉眼極限約 6 等，城市裡看不到。片中「要在很黑的地方才看得到」。
- **hautapu**：Mātāmua 描述的儀式：天亮前在地爐（umu）煮食物，讓熱氣升上天「餵」星群（whāngai i te hautapu）；同時哀悼、念出過去一年離開的人（向 Pōhutukawa），也對 Hiwa-i-te-rangi 許下新年的願望。「有點像我們的除夕」是本社的比喻（片中說「有點像」）。2025 年國家轉播的 hautapu 在 Ruapehu 山腳由 Ngāti Rangi 主持（RNZ）。
- **Puanga**：Te Ara：Taranaki、Whanganui、Rangitīkei 等北島西岸部族以 Puanga（參宿七）為新年星；Te Papa 引 Che Wilson（Whanganui）：有些地方看不清楚 Matariki，所以看旁邊重要的 Puanga；RNZ 2025 同一人又說：「我們看 Puanga 不是因為看不到 Matariki……而是 Puanga 更能預告西岸的天氣」（北島的山脈把東西兩邊的天氣分開）。片中兩個理由並列。PyEphem：Puanga 在紐西蘭比 Matariki 早約一週重現（威靈頓 6/5 vs 6/13）。
- **Rehua**：Stellarium maori 的 HIP 80763＝Rehua（引 Best 1955）。毛利傳統裡 Rehua 是夏天的星（也是一位神祇的名字），片中只說「毛利人叫它 Rehua」（待查核 6）。
- **今晚台灣**：6/4 昴宿 17:42、參宿七 18:05 就落下，都在日落前——「這兩位主角都躲在太陽附近」。心宿二 18:24 升起，20:00 高 17°、方位 131°。

### ⚠ 待查核清單（給下一輪審稿）

1. **九星的西方星名對應**：核 Mātāmua《Matariki: The Star of the Year》（2017）原書，特別是 Tupuārangi／Tupuānuku 對 Atlas／Pleione、Waitī／Waitā 對 Maia／Taygeta（網路上有對調的版本）。10 鏡「最暗的兩顆」依賴 Pōhutukawa＝Asterope、Hiwa＝Celaeno。
2. **「很多較早的資料只列七顆」**：出處是 Wikipedia 轉述；請找 Best（1955）或 Mātāmua 書中的說法。片中只說「近年最受注目的，是九顆星的說法」。
3. **Tangaroa 期與「下弦前後」**：Te Papa 的表寫 2027 Tangaroa 期 6/27–30；片中「大約下弦月前後」是本社用月相推的（下弦 6/27 16:54 NZST），請找 Matariki Advisory Group 報告裡 Tangaroa 期的定義（陰曆第幾晚）。
4. **手稿細節**：1933 年完成、約 400 頁、編者 Te Kōkau Himiona Te Pikikōtuku 與 Rāwiri Te Kōkau（NZ Geographic、Prime Minister's Science Prizes）；他跟 Mātāmua 的親屬關係各來源說法不一（片中只說「祖先」）。
5. **預測年景的兩種說法**：Te Ara（清楚＝暖）vs Tūhoe（星靠得近＝冷、分開＝暖）；片中用前者，請確認不會跟 Mātāmua 的說法衝突。
6. **Rehua＝心宿二**：Best 1955 的指認，請核；若有爭議，13 鏡改成只說「紅色的心宿二剛升起」（−7 字）。
7. **「第一個承認毛利世界觀的國定假日」**：employment.govt.nz 原文是「the first public holiday to recognise Te Ao Māori」；請審「承認」這個譯法（也可用「認可」「以毛利世界觀為本」）。
8. **Puanga 的部族名單**：Te Ara 列 Taranaki、Whanganui、Rangitīkei；片中只唸前兩個＋「等部族」。也請確認 Puanga 在這些部族的拼法（有的寫 Puaka，南島 Kāi Tahu 用 Puaka）。
9. **hautapu 的程序**：請核 Mātāmua 書中的儀式步驟（天亮前、地爐、念名、許願）；片中說「有點像我們的除夕」，請審這個比喻是否得體。
10. **台灣 6/7 重現**：用「太陽 −12°、星高 3°」的簡化條件；肉眼實際要看大氣與光害，請審片中「大約六月七號起……就會冒出來」是否要改成「六月上旬末」。
11. **Te Waka-o-Tamarereti**：X-07 v0 已處理（片名改「一條河、一條路、一道縫」）；本集不畫，星名表照 Stellarium 列出並標「他說不一」。
12. **節目表「唯一的原住民國定假日」**：若節目表要保留「唯一」，需要查 Waitangi Day 是否被視為原住民相關的國定假日（多數說法把 Matariki 稱為「第一個」）。
13. **毛利語讀音**：請熟悉毛利語的人聽配音（長音、wh＝f、r 是輕彈舌）。

---

## Caption 建議

> 紐西蘭有一個國定假日，日期是星星和月亮一起決定的：Matariki。✨
> Matariki 就是昴宿。每年五月它躲進太陽的光裡，六月在冬天的黎明重新出現——舊的一年結束，新的一年開始。2027 年的假日是 6/25（五）。
> 毛利學者 Rangi Mātāmua 從 1933 年的家族手稿裡整理出九顆星：土裡的食物、樹上的食物、淡水、大海、雨、風、健康、願望，還有過去一年離開的人。
> 台灣其實更早看到：6 月上旬起，清晨四點往東北東低空找，6 月中以後更好找。
> 📌 圖卡「Matariki 九星小辭典」「這週抬頭看」可以存起來
> EP47 下週五｜銀河環球：一條河、一條路、一道縫
> #萬國星空 #師大天文社 #Matariki #毛利 #紐西蘭 #昴宿 #新年 #天文 #星空

## 首留言（考據長文）

📚 **Matariki 假日**：紐西蘭《Te Kāhui o Matariki Public Holiday Act 2022》，2022/6/24 第一次放假；政府稱它是「第一個承認 Te Ao Māori（毛利世界）的國定假日」。日期由 Matariki Advisory Group 排定（2022–2052）：在毛利月曆的 Pipiri 月（Matariki 黎明重現的那個月）裡，取月相 Tangaroa 期最近的星期五。2027 年：Tangaroa 期 6/27–30，假日 6/25（五）（Te Papa）。

📚 **九顆星**（Rangi Mātāmua《Matariki: The Star of the Year》2017，據 Ruatāhuna 的 Te Kōkau Himiona Te Pikikōtuku 與 Rāwiri Te Kōkau 1933 年完成的手稿）：Matariki（母親；健康福祉；Alcyone）、Tupuānuku（土裡的食物；Pleione）、Tupuārangi（樹上與天上的食物；Atlas）、Waitī（淡水；Maia）、Waitā（大海；Taygeta）、Waipuna-ā-rangi（雨；Electra）、Ururangi（風；Merope）、Hiwa-i-te-rangi（願望；Celaeno）、Pōhutukawa（過去一年離開的人；Asterope）。西方星名對應依 Stellarium 與 Wikipedia 表〔待核原書〕。九顆裡最暗的是 Pōhutukawa（5.8 等）和 Hiwa-i-te-rangi（5.5 等）。

📚 **看年冬**：傳統上在黎明仔細觀察 Matariki：星清楚明亮，來年溫暖豐收；朦朧、擠成一團，就是冷冬（Te Ara）。

📚 **Puanga**：北島西岸的 Taranaki、Whanganui、Rangitīkei 等部族以 Puanga（參宿七）為新年星（Te Ara）。Whanganui 的 Che Wilson：有些地方看不清楚 Matariki；更重要的是 Puanga 更能預告西岸的天氣（Te Papa、RNZ 2025）。Puanga 在紐西蘭的黎明比 Matariki 早約一週重現（PyEphem：威靈頓 6/5 vs 6/13）。

📚 **黎明重現**（太陽在地平下 12° 時昴宿六高 ≥3° 的第一天，PyEphem）：台北 6/7、利雅德 6/7、奧克蘭 6/11、新普利茅斯 6/12、威靈頓 6/13。台灣 6/25 清晨四點，昴宿已在東北東高 18°。

📚 **資料來源**：Stellarium maori（Dan Smale；Best 1955、1959 等）；Mātāmua 2017；MBIE／employment.govt.nz；Te Papa；Te Ara；RNZ；天象 PyEphem 4.2.1。

## 聯盟版文案（臺灣業餘天文聯盟）

> 昴宿這兩週躲在太陽旁邊（5/21 合日），6 月上旬末會在台灣的清晨重新出現；而在紐西蘭，它的黎明重現就是毛利新年 Matariki——2027 年的國定假日是 6/25（五）。
> 假日的日期由星星和月亮一起決定：在 Matariki 重現的 Pipiri 月裡，取月相 Tangaroa 期（2027 年 6/27–30）最近的星期五。毛利學者 Rangi Mātāmua 依 1933 年的家族手稿，替昴宿九顆星各配上照看的領域：土、樹、淡水、海、雨、風、健康、願望、離開的人——其中最暗的 Pōhutukawa（Asterope，5.8 等）和 Hiwa-i-te-rangi（Celaeno，5.5 等），要很暗的天空才看得到。
> 北島西岸的部族則以 Puanga（參宿七）為新年星，它在紐西蘭比昴宿早約一週重現。
> **這幾天晚上抬頭看得到嗎**：看不到——6/4 昴宿 17:42、參宿七 18:05 就落下（都在日落前）。晚上八點東南方低空（高 17°）有心宿二，毛利名 Rehua；6/5 是新月，整晚很暗。想看昴宿重現：台北 6/7 前後清晨 04:07 只高 3°（東北東），6/14 約 8.5°、6/25 約 18°。
> 資料來源：Stellarium 星空文化 maori（Dan Smale）；Mātāmua《Matariki: The Star of the Year》；Te Papa、Te Ara；天象以 PyEphem 計算。
> #萬國星空 #師大天文社

## 配音提示

- 毛利語唸法（近似；r 是輕輕彈一下舌頭，wh 接近 f，長音符號的母音拉長）：Matariki（瑪-搭-**里**-基）、Pipiri（**皮**-皮-里）、Tangaroa（當-阿-**羅**-阿）、Rangi Mātāmua（**朗**-伊、**瑪**-**搭**-姆-阿）、Tupuānuku（圖-普-**阿**-努-庫）、Tupuārangi（圖-普-**阿**-朗-伊）、Waitī（外-**替**）、Waitā（外-**搭**）、Waipuna-ā-rangi（外-普-納-**阿**-朗-伊）、Ururangi（烏-魯-朗-伊）、Hiwa-i-te-rangi（希-瓦-伊-帖-朗-伊）、Pōhutukawa（**坡**-呼-圖-卡-瓦）、Puanga（普-**安**-阿）、Taranaki（搭-拉-**納**-基）、Whanganui（**方**-阿-努-伊）、Rehua（雷-**胡**-阿）、hautapu（浩-搭-普）。
- 09 鏡六個名字一個一個唸清楚，每個名字後面小停，「管」字不要吞掉。
- 08 鏡（4.07）是全片最快的一格：「一九三三年」唸清楚，「各自配上它們照看的東西」放慢。
- 10 鏡「Pōhutukawa 代表過去一年離開的人」語氣放輕；「有趣的是」之後換回輕快。
- 11 鏡「有點像我們的除夕」帶一點溫度，不要誇張。
