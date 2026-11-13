# A-33｜毛利 Matariki：星星升起就是新年（萬國星空 EP46）・v1（已查核＋外部審稿 2026-11-13）

| 項目 | 內容 |
|---|---|
| 發布 | **2027/06/25（五）20:00**＝紐西蘭 Matariki 國定假日（10/31 排程調整，原 6/4；v1 天象已依 6/25 重算） |
| 時長 | **226 秒**（14 鏡頭） |
| 格式 | Reels 9:16；**長圖帶狀**（昴宿特寫＋九星標籤層、獵戶參宿七、天蠍心宿二）＋概念圖 6 組（假日、挑日子、兩個季節、黎明重現、hautapu、北島示意）＋9:16 圖卡 2 張；不用盤（昴宿 dec +24°，在長圖帶內） |
| 來源 | Stellarium **maori**（`stellarium-master/skycultures` 與 `stellarium-skycultures-master` 兩版；Dan Smale；CC BY-SA 4.0；引 Best 1955、1959〔重印本；初版 1922、1924〕、Leather & Hall 2004、Orbell 1996 等）；Rangi Mātāmua（原書署名 Rangi Matamua）《Matariki: The Star of the Year》（2017；據 Te Kōkau Himiona Te Pikikōtuku 與 Rāwiri Te Kōkau 1933 年完成的手稿）；紐西蘭政府 MBIE／employment.govt.nz（Matariki 假日）、Matariki Advisory Group《Matariki dates 2022 to 2052》；Te Papa（九星與各自的領域、逐星預兆；假日日期與 Tangaroa 期）；Te Ara（Matariki 預測年景、各地以 Puanga 為新年）；RNZ 2025（Che Wilson 談 Puanga）；天象全部 PyEphem 4.2.1 自算（恆星 `_epoch=J2000`） |
| 配音 | 逐字稿 **835 字**（中文字＋外文音節；毛利語每個母音算一音節，長音符號不另計），平均 **3.69 字/秒**；最快一格 13 鏡 **4.11**（上限 4.5） |
| 統一開頭 | 「同一片星空，毛利人看見——新的一年。」 |
| 承接 | EP45（A-36）現代星座（下）（結尾「下週五，紐西蘭放 Matariki 假：昴宿在黎明升起，就是新年。」）→ **EP46 毛利 Matariki：星星升起就是新年**（6/25＝紐西蘭 Matariki 國定假日）→ EP47（X-07）銀河環球：一條河、一條路、一道縫（7/2） |

> ⚠️ **播出日就是假日當天**：6/25 晚上八點（台北）時，紐西蘭已是 6/26 凌晨；昴宿在台北、紐西蘭的黎明都已重現兩週左右。所以 06 鏡講「台灣比紐西蘭早」用回顧的口氣，13 鏡的觀星指引是「今晚八點看心宿二、明天（6/26）清晨看昴宿」。
> ⚠️ **節目表的星圖需求已改**（v1 同步改節目表）：原「北盤＋Matariki(昴宿)/Te Waka 大舟連線層」。①昴宿 dec +24°，在長圖帶內，不需要北盤；紐西蘭的黎明地平線用概念圖畫比較清楚。②**Te Waka-o-Tamarereti 的指認各家不一**：Stellarium maori 把它連在天蠍尾巴；Martinborough Star（Phoenix Astronomical Society 系統）說是貼著地平線的整條銀河，船尾是獵戶腰帶 Tautoru、船頭是天蠍 Te Matau-a-Māui；Museums Wellington 說「Tamarereti 的船頭」是天蠍的名字之一。這條留給 X-07 處理（X-07 v0 已改用毛利的銀河名 Te Ikaroa／Te ika o te rangi，並註明 Te Waka 在 Stellarium 是天蠍尾巴），本集不畫。
> ⚠️ **Stellarium 資料的狀態**：`_整理CSV/Maori in Oceania.csv` 在 10/31（commit 317eab65）已清掉 po 檔表頭、補上長音符號，現在九顆星的名字都有長音（Waitī、Waitā、Tupuārangi、Tupuānuku、Pōhutukawa、Waipuna-ā-rangi）。但 Stellarium 本身（兩版 `index.json`）仍沒有長音、把 Waipuna-ā-rangi 寫成 Waipunarangi；兩版的 `references.txt`（新版在資料夾根目錄、舊版在 `doc/`）都還寫著「stars in Matariki also randomly labelled, just to get the names in」；新版 `description.md` 也沒有列九顆星的名字。九顆星的 HIP 對應兩版相同，跟 Wikipedia「Matariki」表一致；片中照這套對應，名字照 Mātāmua／Te Papa 加長音（Te Papa 寫 Tipuānuku／Tipuārangi，本集照 Stellarium 與 CSV 寫 Tupu-，見待查核 1）。

> **資料來源挖掘重點（第〇節檢查表）**
> 1. **本文化的鄰居**：Stellarium maori 只有 6 個星座、24 顆具名恆星（另有 M45 與 7 個太陽系天體），主題是**航海與季節**：Te Rā o Tainui「Tainui 號的帆」（腰帶＝龍骨、畢宿＝蟹爪帆、昴宿＝船頭）、Tau-toro（腰帶）、Matakarehu（畢宿）、南十字 Taki-o-Autahi、南門二與馬腹一 Te Taura（船的繩）、天蠍尾巴 Te Waka-o-Tama-rereti。昴宿周圍 ±45°：Puanga（參宿七）、Taumata-kuku（畢宿五）、Takarua（天狼；一般拼作 Takurua）、Whakaahu（北河二）——**冬天的星全是「季節鐘」**：Matariki 與 Puanga 在冬天黎明重現＝新年。論點＝「天上的時鐘決定一個國家的假期」；X-01 只講了名字家族（mata-liki）和「2022 年起放假」，本集往下挖：日期怎麼算、九顆星各管什麼、為什麼西岸看 Puanga、台灣什麼時候看得到。
> 2. **跨文化同星群**：昴宿在 X-01 已做足（約 40 個文化）。本集只用兩條：①**黎明重現＝新年**：毛利（6 月中，南半球冬至前後）、阿拉伯半島（昴宿晨升開夏季，A-13）、Hesiod「昴升起就收割」（X-01）——今天的日期，南半球在冬天、北半球在夏天；**跨時代比較要算歲差**：Hesiod 時代波奧提亞的昴宿晨出約在儒略曆 5 月中，毛利先民約 1300 年抵達紐西蘭時當地重現約在 5 月下旬（天文角色推算，片中不用）；②**九顆 vs 七顆**：希臘七姊妹＋父母 Atlas、Pleione＝九顆有名字的星，Mātāmua 的九星恰好也是九顆，對到同樣九顆（Matariki＝Alcyone、Tupuārangi＝Atlas、Tupuānuku＝Pleione……）。
> 3. **恆星物理／天象**：九顆星的 V 星等（`03_星點座標表.csv`）：Matariki 2.87、Tupuārangi 3.63、Waipuna-ā-rangi 3.70、Waitī 3.87、Ururangi 4.18、Waitā 4.30、Tupuānuku 5.09、Hiwa-i-te-rangi 5.46、Pōhutukawa 5.76——**Mātāmua 加進來的兩顆（Pōhutukawa、Hiwa）正好是最暗的兩顆**；2027/5/22 太陽離昴宿最近（4.1°）；黎明重現（太陽在地平下 12° 時昴宿六高 ≥3°）：利雅德 6/7、台北 6/8、奧克蘭 6/12、新普利茅斯 6/12、威靈頓 6/13；Puanga（參宿七）在紐西蘭 6/5–7 就重現，比昴宿早一週；南半球冬至 6/22 02:10（紐西蘭時間），威靈頓白天 9.2 小時、台北 13.7 小時。
> 4. **文獻**：Mātāmua 2017（九星與各自照看的領域；手稿 1933 年完成）；MBIE／employment.govt.nz（2022/6/24 第一次放假、「first public holiday to recognise Te Ao Māori」）；Matariki Advisory Group 日期表（2022–2052，2027＝6/25）；Te Papa（九星的領域、逐星預兆、「widely known as the mother」；2027 Tangaroa 期 6/27–30）；Te Ara（星清楚明亮＝好年、朦朧擠在一起＝冷冬；Taranaki、Whanganui、Rangitīkei 等以 Puanga 為新年）；RNZ 2025（Che Wilson：Puanga 是西岸的天氣星）。
> 5. **原始出處看到底**：①Stellarium 的「randomly labelled」註記兩版都在，HIP 對應要核 Mātāmua 原書（Atlas／Pleione 對 Tupuārangi／Tupuānuku 在部分網路海報是反過來的）；②Stellarium 的名字都沒有長音符號；③Stellarium 把 Te Waka-o-Tama-rereti 放在天蠍尾巴，跟其他毛利天文資料不一致（見⚠）；④「Matariki＝天神之眼（mata ariki）」是 X-01 講過的一說，另一說是「小小的眼睛」（mata riki），本集不再講；⑤Tāwhirimātea 挖出眼睛丟上天的故事（Ngā Mata o te Ariki Tāwhirimātea），文化角色說 Mātāmua 與 Te Papa 都採用，本環境沒有原書、沒核到，X-01 已提「天神的眼睛」，本集不重複；⑥九星裡誰是男、誰是女，各來源說法不一，片中不講性別（只說 Matariki 是母親，Te Papa：widely known as the mother）。
> 6. **去處**：主線＝承接 → 假日（2022 起、2027＝6/25）→ 日期看星星＋月亮 → 南半球的冬至 → 台灣比紐西蘭早看到 → 看清楚＝看年冬 → 七顆與九顆、手稿 → 六顆管自然 → 母親、願望、離開的人＋最暗的兩顆 → hautapu → 西岸看 Puanga → 今晚心宿二、明晨昴宿 → 下集；字卡＝見表；圖卡＝九星小辭典（10 鏡後）、這週抬頭看（13 鏡）；首留言＝日期規則、九星表、手稿、Puanga、重現日期表。

---

## 逐字稿＋分鏡

| 鏡 | 秒數 | 旁白（逐字） | 字卡（畫面大字，可空） | 畫面構想 | 字/秒 |
|---|---|---|---|---|---|
| **01** Z | 0–13s（13） | 上週，我們數了課本沒教的星群。今天，紐西蘭放 Matariki 假：同一片星空，毛利人看見——新的一年。 | 同一片星空，／毛利人看見——新的一年。 | 長圖 fov 40→12：從獵戶—金牛推近昴宿；Matariki 標籤；開場字卡 | 38 字／2.92 |
| **02** — | 13–31s（18） | 二〇二二年起，紐西蘭多了一個國定假日，叫 Matariki。政府說，這是第一個承認毛利世界觀的國定假日。它每年日期都不一樣：二〇二七年，是六月二十五號，星期五。 | 今年假日：6/25 | 定格疊概念圖 C-A33-01「Matariki 假日」：2022/6/24 第一次 → 2026/7/10 → 2027/6/25（五）；「第一個承認 Te Ao Māori 的國定假日」中譯；慶典照片美宣另尋授權圖 | 66 字／3.67 |
| **03** Z | 31–44s（13） | 日期由天上決定。Matariki 就是昴宿：每年四、五月，它在黃昏沉進西方，躲進太陽的光裡；六月，再從冬天的黎明裡冒出來。 | Matariki＝昴宿 | 長圖 昴宿＋太陽位置標記：5/22 太陽離昴宿最近（約 4°）→ 6 月太陽往東移開；兩格 Match & Move | 48 字／3.69 |
| **04** — | 44–62s（18） | 假日還要對上官方採用的毛利月曆：在昴宿重現的 Pipiri 月，月亮走到叫 Tangaroa 的那幾晚，大約下弦月前後，再挑最近的星期五。今年的 Tangaroa，是六月二十七到三十號。 | 星星＋月亮＝放假日 | 定格疊概念圖 C-A33-02「怎麼挑日子」：Pipiri 月曆條（6/5 新月 → 6/27 下弦）、Tangaroa 6/27–30 標色、6/25（五）圈起並標「6/27 是星期日」 | 70 字／3.89 |
| **05** — | 62–77s（15） | 為什麼新年在六月？南半球的六月是冬天：冬至那天，威靈頓的白天只有九個多小時。最冷、最暗的時候，昴宿回來了——舊的一年結束，新的一年開始。 | 南半球的冬至 | 定格疊概念圖 C-A33-03「同一天、兩個季節」：6/21 台北白天 13.7 小時 vs 威靈頓 9.2 小時（日出日落時刻） | 58 字／3.87 |
| **06** — | 77–93s（16） | 台灣其實比紐西蘭早：同樣在天亮前，昴宿六月八號前後就在台灣東北東的地平線露臉，紐西蘭要再晚四五天；到了六月下旬，兩邊都好找了。 | 台灣早四五天 | 定格疊概念圖 C-A33-04「黎明重現」：東方地平線示意（太陽在地平下 12° 那一刻）：台北 6/8 昴宿高 3.6°（方位 65°）、奧克蘭 6/12 3.6°（56°）、威靈頓 6/13 3.1°（54°）；小字「高度 10° 以上才好找：台北 6/16、奧克蘭 6/22、威靈頓 6/25」 | 57 字／3.56 |
| **07** Z | 93–106s（13） | 看到還不夠，還要看清楚。天亮前，懂星的人仔細看這群星：清楚又明亮，來年溫暖豐收；朦朧、擠成一團，就要準備過一個冷冬。 | 看清楚＝看年冬 | 長圖推近 fov 3：昴宿特寫，九顆主角星白點＋光暈 | 49 字／3.77 |
| **08** Z | 106–123s（17） | 很多說法只數七顆；近年最受注目的，是九顆星的說法。毛利天文學者 Rangi Mātāmua 整理祖先在一九三三年完成的手稿，介紹這九顆星和它們各自照看的領域。 | 七顆之外：九顆星 | 長圖 fov 2.6：先亮七顆（Matariki＋六顆），再淡入 Pōhutukawa、Hiwa-i-te-rangi；九星標籤層（毛利原名，長音符號照原文）；不放 Mātāmua 書封（版權） | 65 字／3.82 |
| **09** Z | 123–141s（18） | Tupuānuku 管土裡長的食物，Tupuārangi 管樹上的果實和鳥；Waitī 管淡水和河裡的食物，Waitā 管大海和海裡的食物；Waipuna-ā-rangi 管雨，Ururangi 管風。 | 土・樹・淡水・海・雨・風 | 同框；六顆依序高亮＋小圖示（土、樹、水滴、浪、雨、風）；星名與中文領域上下兩行對齊，不排成一整段橫字 | 64 字／3.56 |
| **10** Z | 141–159s（18） | Matariki 是母親，照看人們的健康；Hiwa-i-te-rangi 收下新年的願望；Pōhutukawa 代表過去一年離開的人。而後面這兩顆，正好是九顆裡最暗的，要在很黑的地方才看得到。 | 健康・願望・思念／最暗的兩顆 | 同框；Matariki（2.9 等）高亮 → Hiwa-i-te-rangi（5.5 等）、Pōhutukawa（5.8 等）圈出時換第二張字卡；結束疊 9:16 圖卡 C-A33-05「Matariki 九星小辭典」（可存圖） | 68 字／3.78 |
| **11** — | 159–177s（18） | 天亮前的這場儀式叫 hautapu：生火煮食物，讓熱氣升上天，獻給這群星；念出離開的人的名字，也說出新年的願望。有點像我們過年：送走舊的一年，想念親人，許下新願。 | 天亮前的 hautapu | 定格疊概念圖 C-A33-06「hautapu」：地爐的熱氣升向昴宿的示意（不畫人物、不仿任何既有插畫）；若要用儀式照片，美宣另尋授權並確認可公開 | 67 字／3.72 |
| **12** S | 177–195s（18） | 但不是每個部族都看昴宿。北島西岸的 Taranaki、Whanganui 等部族，新年看的是 Puanga——參宿七。有的地方被山擋住，看不清昴宿；也有部族的專家說，Puanga 更能預告西岸的天氣。 | 西岸看 Puanga | 長圖往左下（東南）捲到獵戶：參宿七 Puanga 標籤；右下小框：北島示意地圖（自繪，標 Taranaki、Whanganui、Rangitīkei；角落小字「南島 Kāi Tahu 叫它 Puaka」） | 71 字／3.94 |
| **13** Z | 195–214s（19） | 今晚八點，這兩位主角下午就已經西沉，台灣看不到。往南偏東看，紅色的心宿二已經升到半空，毛利人叫它 Rehua。想看 Matariki，明天清晨三點半到四點，往東北東低空找，跟紐西蘭一起迎新年。 | 今晚：心宿二 Rehua／明晨 3:30・東北東 | 【硬切】長圖 天蠍：心宿二 Rehua 標籤（第一張字卡）；後半換第二張字卡；結束疊 9:16 圖卡 C-A33-07「這週抬頭看」（見星空對時：台北 6/25 20:00 心宿二；6/26 清晨 03:30–04:09 昴宿高度、月亮位置；可存圖） | 78 字／4.11 |
| **14** — | 214–226s（12） | 下週五，我們沿著銀河繞地球一圈：有人看見一條河，有人看見一條路，也有人看見一道縫。 | 下集｜銀河環球 | 端卡（背景：長圖夏季銀河）＋「下集見｜銀河環球：一條河、一條路、一道縫」＋追蹤 CTA | 36 字／3.00 |

> **全片在大畫布（長圖）上**，01–11 都在金牛—獵戶一帶（昴宿特寫 fov 2.6–3），12 往東南捲到參宿七，13 硬切到天蠍；02、04、05、06、11 是定格疊概念圖。
> **九星標籤層**：毛利原名（含長音符號）＋中文領域兩行；特寫時九顆星的白點照 V 星等畫大小，讓「最暗的兩顆」看得出來。`gen_master_canvas.py` 預設 `maglim=5.6` 會把 Pōhutukawa（5.76）濾掉，跑長圖時 `maglim` 設 ≥5.8，九顆用同一套星點畫法（不要靠標記層補畫）。
> **字卡**：每張 ≤14 字；「／」表示分兩張。
> **刪減紀錄**：無（14 鏡全留、不重排）。

---

## 星空對時（PyEphem 4.2.1 自算；恆星 `03_星點座標表.csv`、`_epoch=J2000`；1010 hPa、20°C，含大氣折射；「黎明重現」＝太陽在地平下 12° 那一刻，昴宿六 Alcyone 高度 ≥3° 的第一天）

**2027/6/25（五）台北（25.033°N、121.565°E、UTC+8）——13 鏡「今晚八點」**

| 時刻 | 事件 |
|---|---|
| 16:20 | 昴宿六落下（太陽與昴宿角距 33.6°） |
| 16:43 | 參宿七落下（角距 34.8°） |
| 17:02 | 心宿二升起 |
| 18:47 | 日落；19:43 航海昏影結束；20:16 天文昏影結束 |
| **20:00** | **心宿二 29.6°（方位 146°，南偏東）**；尾宿八 12.7°（142°）；角宿一 51.4°（201°）；大角 84.0°（187°，近天頂）；織女 34.7°（59°）；南十字 γ 星 4.8°、十字架一 −0.4°（已落）；火星 42.8°（252°，+1.0 等，在獅子座）、木星 25.6°（275°，在獅子座）；月亮在地平下 |
| 21:00 | 心宿二 35.7°（160°） |
| 22:10 | 心宿二中天（約 38.5°，正南） |
| 22:48 | 月出（虧凸月，亮面約 66%） |
| 6/26（六）02:30 | 心宿二低於 10°（03:18 落下）——今晚可看心宿二的時段：天黑到半夜兩點 |
| 6/26（六）02:36 | 昴宿六升起 |
| 6/26 03:30 | 昴宿六 10.5°（方位 68°） |
| 6/26 03:36 | 天文曙光開始（太陽 −18°）；昴宿六 11.7° |
| 6/26 04:00 | 昴宿六 16.8°（71°） |
| 6/26 04:09 | 太陽 −12°；昴宿六 18.8°（71°）；畢宿五 5.5°；參宿七在地平下 −13.7°（台北要到 7/13 才黎明重現） |
| 6/26 05:05 | 日出 |
| 月光 | 6/26 清晨月亮亮面 64%，在南偏東高 56°–61°，離昴宿約 72°：不擋昴宿主星，但不利看最暗的兩顆（5.5、5.8 等） |

**昴宿的黎明重現（太陽在地平下 12° 時昴宿六的高度；台北 UTC+8、利雅德 UTC+3、紐西蘭 NZST UTC+12）——03、06 鏡**

| 地點 | 首次 ≥3°（前一天） | 首次 ≥10° | 6/25（假日）同一時刻 | 方位 |
|---|---|---|---|---|
| **台北** | **6/8（04:06，3.6°；6/7 2.8°）** | 6/16 | 04:08，17.9° | 東北東 65°→71° |
| 利雅德（A-13 對照） | 6/7（04:07，3.0°） | 6/16 | 04:09，18.1° | 65° |
| 奧克蘭 36.85°S | 6/12（06:29，3.6°；6/11 2.9°） | 6/22 | 06:32，12.1° | 東北 56°→47° |
| 新普利茅斯（Taranaki）39.06°S | 6/12（3.0°） | 6/24 | 06:39，11.1° | 55° |
| Whanganui 39.93°S | 6/13（3.5°） | 6/24 | 06:37，10.8° | 54° |
| **威靈頓 41.29°S** | **6/13（06:37，3.1°；6/12 2.5°）** | 6/25 | **06:41，10.2°（方位 45°，東北）** | 54°→45° |
| Puanga（參宿七）威靈頓 | **6/5**（3.6°，正東 98°） | 6/13 | 06:41，19.6°（84°） | — |
| Puanga 新普利茅斯／Whanganui | 6/6（3.3°）／6/6（3.7°；6/5 2.9°） | 6/14 | 19.0°／19.2° | 98° |
| Puanga 台北 | 7/13 | 7/20 | 6/25 在地平下 −14.7° | 100° |

（2027/5/22 太陽離昴宿六最近，角距 4.1°。台北太陽 −15° 時昴宿 ≥10° 要到 6/20。紐西蘭 6/25 清晨月亮 73%、在西北高 46°，離昴宿 85°，不擋東北方的昴宿。昴宿在紐西蘭的**黃昏消失**：威靈頓太陽 −6° 時 4/26 已低於 3°、奧克蘭 4/30；台北 5/13——03 鏡寫「四、五月」。）

**南半球的冬至——05 鏡**

| 地點 | 6/21 日出 | 日落 | 白天長 |
|---|---|---|---|
| 威靈頓 | 07:46 | 16:58 | **9.2 小時** |
| 台北 | 05:04 | 18:46 | 13.7 小時 |

（2027 年 6 月至日：UTC 6/21 14:10＝台北 6/21 22:10＝紐西蘭 6/22 02:10。）

**假日與月相（紐西蘭時間）——04 鏡**

| 項目 | 日期 |
|---|---|
| 新月（Pipiri 月開始的依據之一） | 6/5 07:40 NZST（台北 6/5 03:40） |
| 滿月 | 6/19 12:44 NZST |
| 下弦 | 6/27 16:54 NZST |
| Tangaroa 期（Te Papa 表） | 6/27–30 |
| **Matariki 假日** | **6/25（五）**（Tangaroa 期最近的星期五；6/27 是星期日。7/2 與 6/30 也相隔兩天，官方怎麼取捨見待查核 3） |

---

## 星名表（毛利語照 Mātāmua／Te Papa 的寫法，長音符號照原文）

| 毛利名 | Stellarium 拼法 | 意思／照看的領域（Mātāmua；Te Papa） | 西方星名 | HIP | V | 片中 |
|---|---|---|---|---|---|---|
| Matariki | Matariki | 母親；人們的健康與福祉（也是整個星團的名字） | Alcyone（η Tau，昴宿六） | 17702 | 2.87 | 01–03、10、13 |
| Tupuārangi | Tupuarangi | 樹上與天上來的食物（果實、鳥；Te Papa 寫 Tipuārangi） | Atlas（27 Tau） | 17847 | 3.63 | 09 |
| Tupuānuku | Tupuanuku | 土裡長的食物（kūmara 等；Te Papa 寫 Tipuānuku） | Pleione（28 Tau；Be 變星約 4.8–5.5 等，離 Atlas 5′） | 17851 | 5.09 | 09 |
| Waitī | Waiti | 淡水，與淡水裡的食物 | Maia（20 Tau） | 17573 | 3.87 | 09 |
| Waitā | Waita | 大海，與海裡的生物 | Taygeta（19 Tau） | 17531 | 4.30 | 09 |
| Waipuna-ā-rangi | Waipunarangi | 雨 | Electra（17 Tau） | 17499 | 3.70 | 09 |
| Ururangi | Ururangi | 風 | Merope（23 Tau） | 17608 | 4.18 | 09 |
| Hiwa-i-te-rangi | Hiwa-i-te-rangi | 新年的願望與志向 | Celaeno（16 Tau） | 17489 | 5.46 | 10 |
| Pōhutukawa | Pohutukawa | 過去一年離開的人 | Asterope（21 Tau；旁邊 2.5′ 有 22 Tau 6.43 等，肉眼合併約 5.3 等） | 17579 | 5.76 | 10 |
| Puanga | Puanga | 西岸部族的新年星（南島 Kāi Tahu 作 Puaka） | Rigel（β Ori，參宿七） | 24436 | 0.13 | 12 |
| Rehua | Rehua | （夏天的星；本集只用名字） | Antares（α Sco，心宿二） | 80763 | 0.91 | 13 |
| Te Rā o Tainui | Te-Ra-o-Tainui | Tainui 號的帆 | 腰帶＋畢宿＋昴宿 | — | — | （片中、首留言都不用；挖掘重點 1） |
| Tau-toro（Tautoru） | Tau-toro | 腰帶三星 | 獵戶腰帶 | 25930、26311、26727 | — | — |
| Te Waka-o-Tamarereti | Te-Waka-o-Tama-Rereti | Tamarereti 的船 | Stellarium：天蠍尾巴（他說不一，見⚠） | — | — | X-07 |

**其他片中用詞**

| 毛利語 | 意思 | 片中 |
|---|---|---|
| Pipiri | 毛利月曆的月名（約 6–7 月；Matariki 重現的那個月） | 04 |
| Tangaroa | 月相名（下弦前後的幾晚；也是海神的名字） | 04 |
| hautapu | Matariki 儀式中獻給星群的食物與儀式（whāngai i te hautapu＝餵養星群） | 11 |
| Te Ao Māori | 毛利世界（觀） | 02（中譯） |
| Te Kāhui o Matariki | Matariki 星群（法案名稱） | 首留言 |
| Aotearoa | 紐西蘭的毛利名 | 首留言 |
| Whiro | 新月期（月曆的第一晚） | 星空對時 |

---

## 考據備忘

- **假日**：《Te Kāhui o Matariki Public Holiday Act 2022》（2022 年 4 月三讀）；第一次放假 2022/6/24（五）；2026 年 7/10（X-01 已用）、**2027 年 6/25（五）**。政府說法：「the first public holiday to recognise Te Ao Māori」（employment.govt.nz、阿爾登總理）。片中「第一個承認毛利世界觀的國定假日」（「承認」對 recognise，維持；首留言統一寫「毛利世界觀」）。Waitangi Day 紀念 1840 年條約簽署，不是以毛利曆法定日的節日，所以「第一個」比「唯一」穩。
- **日期規則**：Matariki Advisory Group（主席 Rangi Mātāmua）：在 Pipiri 月（Matariki 黎明重現的那個陰曆月）取 Tangaroa 月相期最近的星期五；2022–2052 年都已排定（MBIE 公布的 PDF；本環境下載被擋，規則「closest Friday to the Tangaroa lunar calendar period」以搜尋摘要為據）。這是 2021 年為國定假日協調出的官方做法，各部族的 maramataka 不盡相同——片中「官方採用的毛利月曆」。Te Papa 表：2027 年 Tangaroa 期 6/27–30、假日 6/25。片中「大約下弦月前後」——2027 下弦 6/27 16:54 NZST，Tangaroa 那幾晚就在下弦附近（Gemini 說 Tangaroa 是第 23–26 晚，沒有親核出處；從 6/5 新月起算，第 23 晚正好是 6/27，數字一致）。
- **為什麼是冬天**：南半球冬至 6/22（紐西蘭時間）；威靈頓白天 9.2 小時。Te Ara 有一說：Matariki 和她的女兒們出來，是去陪伴冬天走得疲累的太陽 Te Rā——片中沒用。
- **台灣比紐西蘭早看到**：同一個「太陽在地平下 12°、昴宿六高 3°」的條件，台北 6/8、威靈頓 6/13（PyEphem 逐日算，`_epoch=J2000`；v0 的 6/7 是 `_epoch=2016` 少算 16 年歲差的結果）。3° 只是幾何條件，貼地平、在曙光裡，實際要高 10° 以上才好找：台北 6/16、奧克蘭 6/22、威靈頓 6/25——片中「到了六月下旬，兩邊都好找了」。原因主要是緯度：威靈頓 41°S 比台北 25°N 高，星升起的路徑更斜，要多等幾天才離開曙光（推論，片中只說「晚四五天」）。反過來，在赤道以南的參宿七（−8°），紐西蘭 6/5 就重現、台北要到 7/13。
- **黃昏消失**：昴宿在紐西蘭的黃昏 4 月下旬就看不到（威靈頓 4/26、奧克蘭 4/30，太陽 −6°、高度 <3°），台北要到 5 月中——03 鏡「每年四、五月」。
- **看清楚＝看年冬**：Te Ara：星清楚明亮，來年溫暖豐收；朦朧、擠在一起（hazy and closely bunched），就是冷冬、延後種植——v0 說 Te Ara 與 Tūhoe 的「靠得近＝冷」是兩種說法，其實 Te Ara 同一句就有「擠在一起」（文化角色指出；搜尋摘要 ✓），07 鏡改「朦朧、擠成一團」。Te Papa 另外有逐星的預兆：Tupuārangi 暗＝天上來的食物少、Waitī 暗＝淡水食物少、Waipuna-ā-rangi 不清楚＝多雨、Ururangi 難見＝多風（首留言用）。看星的人是誰：文化角色說是受訓的 tohunga kōkōrangi（沒親核），片中寫中性的「懂星的人」。
- **九顆星與手稿**：Rangi Mātāmua（Tūhoe；毛利天文學者，2019 年獲紐西蘭總理科學傳播獎；2017 年原書與 Te Papa 署名 Rangi Matamua，不加長音）根據家族手稿——Ruatāhuna 的 Te Kōkau Himiona Te Pikikōtuku 與兒子 Rāwiri Te Kōkau 編寫、1933 年由 Rāwiri 完成、約 400 頁——在《Matariki: The Star of the Year》（2017）介紹九顆星：在常見的七顆之外還有 Pōhutukawa 與 Hiwa-i-te-rangi；Matariki 是母親，其餘八顆是她的孩子（Te Papa：「widely known as the mother of the eight stars」）。手稿開始編寫的年份（1898）與 1995 年傳到 Mātāmua 手上，文化角色與 Gemini 都給了，出處沒親核，不寫進片中。很多較早的資料只列七顆（Wikipedia 轉述；Gemini 引 Best 1922 Pio 的「Matariki, and her six children」，本環境打不開 Best 全文，待查核 2）。08 鏡「很多說法只數七顆；近年最受注目的，是九顆星的說法」——不說「真正有九顆」；「介紹」而不是「配上」，領域是手稿原本就記的。
- **各星的領域**：Matariki 健康福祉；Tupuānuku 土裡的食物；Tupuārangi 樹上、天上的食物（果實、鳥）；Waitī 淡水與淡水裡的食物；Waitā 海與海裡的生物；Waipuna-ā-rangi 雨；Ururangi 風；Hiwa-i-te-rangi 願望；Pōhutukawa 過去一年離開的人（Te Papa 頁面 ✓；Mātāmua、Science Learning Hub 一致）。
- **西方星名對應**：照 Stellarium 兩版 index.json（HIP）＝Wikipedia「Matariki」表（引 Mātāmua）：Matariki＝Alcyone、Tupuārangi＝Atlas、Tupuānuku＝Pleione、Waitī＝Maia、Waitā＝Taygeta、Waipuna-ā-rangi＝Electra、Ururangi＝Merope、Pōhutukawa＝Asterope、Hiwa-i-te-rangi＝Celaeno。Te Papa 的九星頁沒有列西方星名。有海報把 Atlas／Pleione 對調（Playcentre），也有學生作業把 Maia／Taygeta 對調——片中照 Stellarium＝Wikipedia，原書未核（待查核 1）。
- **最暗的兩顆**：Pōhutukawa（Asterope，21 Tau，V 5.76；2.5′ 外的 22 Tau 6.43 等，肉眼分不開，合併約 5.3 等）、Hiwa-i-te-rangi（Celaeno，16 Tau，5.46）是九顆裡目錄星等最暗的；Tupuānuku（Pleione，5.09）離 3.6 等的 Atlas 只有 5′，實際也很難單獨認出。肉眼極限約 6 等，城市裡看不到。片中「要在很黑的地方才看得到」。
- **hautapu**：Mātāmua 描述的儀式：天亮前在地爐（umu）煮食物，讓熱氣升上天「餵」星群（whāngai i te hautapu）；同時哀悼、念出過去一年離開的人（向 Pōhutukawa），也對 Hiwa-i-te-rangi 許下新年的願望。文化角色補：地爐叫 umu kohukohu whetū、四個領域的食物、tapu 的規範與 tohunga 主持（沒親核，首留言只寫「是莊重的儀式」）。「有點像我們過年」是本社的比喻，v1 把相像的地方說出來（送舊、想念親人、許願），不說儀式本身一樣。2025 年國家轉播的 hautapu 在 Ruapehu 山腳由 Ngāti Rangi 主持（RNZ）。
- **Puanga**：Te Ara：Taranaki、Whanganui、Rangitīkei 等北島西岸部族以 Puanga（參宿七）為新年星，在這些地方 Matariki 不容易看清楚；RNZ 2025：「主要是西岸的部族」以 Puanga 為新年，是西岸的「天氣星」，可以讀出新年的西風（引 Ngāti Rangi 發言人、Puanga 專家 Che Wilson，以及 Tapiata）。南島 Kāi Tahu 叫這顆星 Puaka，與天氣、季節、食物有關，也同時慶祝 Matariki（1News 搜尋摘要）。文化角色說北島極北 Te Tai Tokerau 也以 Puanga 為新年——沒有找到出處，不寫。12 鏡維持「北島西岸……等部族」，Puaka 寫進畫面小字與首留言。PyEphem：Puanga 在紐西蘭比 Matariki 早約一週重現（威靈頓 6/5 vs 6/13）。
- **Rehua**：Stellarium maori 的 HIP 80763＝Rehua（references.txt「Antares Rehua」，引 Best 1955）。毛利傳統裡 Rehua 是夏天的星（也是一位神祇的名字），片中只說「毛利人叫它 Rehua」。文化角色說「在 Mātāmua 的傳承裡 Rehua 是 Matariki 的丈夫」、Best 記有別的指認——兩條都沒親核，不寫進片中（待查核 6）。
- **今晚台灣**：6/25 昴宿 16:20、參宿七 16:43 就落下，都在日落前——「這兩位主角下午就已經西沉」。心宿二 17:02 升起，20:00 高 29.6°、方位 146°；看得到的時段天黑到半夜兩點。明晨昴宿 02:36 升起，03:30 過 10°，04:09 曙光變亮時 18.8°。

### ⚠ 待查核清單（給下一輪審稿）

1. **九星的西方星名對應**：核 Mātāmua《Matariki: The Star of the Year》（2017）原書，特別是 Tupuārangi／Tupuānuku 對 Atlas／Pleione、Waitī／Waitā 對 Maia／Taygeta（網路上有對調的版本）。10 鏡「最暗的兩顆」依賴 Pōhutukawa＝Asterope、Hiwa＝Celaeno。也請確認原書拼法是 Tupu- 還是 Tipu-（Te Papa 寫 Tipuānuku、Tipuārangi）。
2. **「很多說法只數七顆」**：Gemini 引 Best 1922 p.43 Pio 的「Matariki, and her six children」，本環境打不開 Best 全文（NZETC、Knowledge Basket 都失敗）；請親核那一段。08 鏡只說「很多說法只數七顆」。
3. **6/25 還是 7/2**：Tangaroa 期 6/27–30，6/25（五）與 7/2（五）都相隔兩天。MBIE 日期表的 PDF 本環境下載被擋，請核報告裡 Tangaroa 期的定義（陰曆第幾晚）與等距時怎麼取。片中只說「挑最近的星期五」，不解釋為什麼不是 7/2。
4. **手稿細節**：1933 年完成、約 400 頁、編者 Te Kōkau Himiona Te Pikikōtuku 與 Rāwiri Te Kōkau（NZ Geographic、Prime Minister's Science Prizes）；1898 年開始編寫、1995 年傳給 Mātāmua（文化、Gemini，未親核）；親屬關係片中只說「祖先」。
5. **逐星預兆**：Te Papa 的逐星預兆已核；文化角色說 tohunga kōkōrangi 負責解讀——請找出處。
6. **Rehua＝心宿二**：Best 1955 的指認，請核；Rehua 是不是 Matariki 的丈夫、有沒有其他指認，請找原書。若有爭議，13 鏡改成只說「紅色的心宿二已經升到半空」（−7 字）。
7. **Puanga 的部族名單**：Te Ara、RNZ 列 Taranaki、Whanganui、Rangitīkei（「主要是西岸」）；南島 Kāi Tahu 作 Puaka（1News）；極北 Te Tai Tokerau 待找出處。
8. **hautapu 的程序**：請核 Mātāmua 書中的儀式步驟（天亮前、地爐、念名、許願、四種食物）；11 鏡「有點像我們過年：送走舊的一年，想念親人，許下新願」請再審得不得體。
9. **Te Waka-o-Tamarereti**：X-07 處理；本集不畫，星名表照 Stellarium 列出並標「他說不一」。
10. **毛利語讀音**：請熟悉毛利語的人聽配音（長音、wh、r 輕彈舌、ng 不拆開、重音）。

---

## Caption 建議

> 紐西蘭今天放一個國定假日，日期是星星和月亮一起決定的：Matariki。✨
> Matariki 就是昴宿。每年四、五月它躲進太陽的光裡，六月在冬天的黎明重新出現——舊的一年結束，新的一年開始。2027 年的假日是 6/25（五）。
> 毛利學者 Rangi Mātāmua 從 1933 年的家族手稿裡，介紹九顆星各自照看的領域：土裡的食物、樹上的食物、淡水、大海、雨、風、健康、願望，還有過去一年離開的人。
> 台灣也看得到：明天（6/26）清晨 3:30–4:00，往東北東低空找，它已經升到 10–17 度。
> 📌 圖卡「Matariki 九星小辭典」、「這週抬頭看」可以存起來。
> 👇 日期怎麼算、九顆星的對照表，在首留言
> EP47 下週五｜銀河環球：一條河、一條路、一道縫
> #萬國星空 #師大天文社 #Matariki #毛利 #紐西蘭 #昴宿 #新年 #天文 #星空

## 首留言（考據長文）

📚 **Matariki 假日**：紐西蘭《Te Kāhui o Matariki Public Holiday Act 2022》，2022/6/24 第一次放假；政府稱它是「第一個承認 Te Ao Māori（毛利世界觀）的國定假日」。日期由 Matariki Advisory Group 排定（2022–2052）：在毛利月曆的 Pipiri 月（Matariki 黎明重現的那個月）裡，取月相 Tangaroa 期最近的星期五。這是為國定假日協調出的官方做法，各部族的月曆（maramataka）不盡相同。2027 年：Tangaroa 期 6/27–30，假日 6/25（五；據 Te Papa）。

📚 **九顆星**（Rangi Mātāmua《Matariki: The Star of the Year》2017，原書署名 Rangi Matamua；據 Ruatāhuna 的 Te Kōkau Himiona Te Pikikōtuku 與 Rāwiri Te Kōkau 1933 年完成的手稿）：Matariki（母親；健康福祉；Alcyone）、Tupuānuku（土裡的食物；Pleione）、Tupuārangi（樹上與天上的食物；Atlas）、Waitī（淡水與淡水裡的食物；Maia）、Waitā（大海與海裡的生物；Taygeta）、Waipuna-ā-rangi（雨；Electra）、Ururangi（風；Merope）、Hiwa-i-te-rangi（願望；Celaeno）、Pōhutukawa（過去一年離開的人；Asterope）。很多較早的資料只列七顆。西方星名的對應照 Stellarium 與 Wikipedia 的表，網路上也有把 Tupuānuku／Tupuārangi 或 Waitī／Waitā 對調的版本。九顆裡最暗的是 Pōhutukawa（5.8 等）和 Hiwa-i-te-rangi（5.5 等）。

📚 **看年冬**：傳統上在黎明仔細觀察 Matariki：星清楚明亮，來年溫暖豐收；朦朧、擠成一團，就是冷冬（Te Ara）。每顆星也各有預兆：Tupuārangi 暗，天上來的食物少；Waitī 暗，淡水裡的食物少；Waipuna-ā-rangi 看不清楚，雨多；Ururangi 難找，風大（Te Papa）。

📚 **hautapu**：天亮前在地爐煮食物，讓熱氣升上天獻給星群，同時念出過去一年離開的人、對 Hiwa-i-te-rangi 許願。這是莊重的儀式；片中「有點像我們過年」只是比喻送舊、思念、許願這幾件事。

📚 **Puanga**：北島西岸的 Taranaki、Whanganui、Rangitīkei 等部族以 Puanga（參宿七）為新年星（Te Ara、RNZ）；南島 Kāi Tahu 叫它 Puaka。Ngāti Rangi 的 Che Wilson 等人說：有些地方看不清楚 Matariki；而且 Puanga 是西岸的天氣星，看得出新年的西風（Te Papa、RNZ 2025）。Puanga 在紐西蘭的黎明比 Matariki 早約一週重現（PyEphem：威靈頓 6/5 vs 6/13）。

📚 **黎明重現**（太陽在地平下 12° 時昴宿六高 ≥3° 的第一天，PyEphem）：利雅德 6/7、台北 6/8、奧克蘭 6/12、新普利茅斯 6/12、威靈頓 6/13；高 10° 以上比較好找：台北 6/16、奧克蘭 6/22、威靈頓 6/25。台灣 6/26 清晨 4:00，昴宿已在東北東高 17°。

📚 **資料來源**：Stellarium maori（Dan Smale；Best 1922〔1955 重印〕、1924〔1959 重印〕等）；Mātāmua 2017；MBIE／employment.govt.nz；Te Papa；Te Ara；RNZ；天象 PyEphem 4.2.1。

## 聯盟版文案（臺灣業餘天文聯盟）

> 今天（6/25）是紐西蘭的 Matariki 國定假日：昴宿在冬天的黎明重現，就是毛利新年。昴宿 5/22 合日，6 月上旬在台灣與紐西蘭的清晨先後回來，現在天亮前已經升得夠高。
> 假日的日期由星星和月亮一起決定：在 Matariki 重現的 Pipiri 月裡，取月相 Tangaroa 期（2027 年 6/27–30）最近的星期五。毛利學者 Rangi Mātāmua 依 1933 年的家族手稿，介紹昴宿九顆星各自照看的領域：土裡的食物、樹上與空中的食物、淡水、大海、雨、風、健康、願望、過去一年離開的人——其中最暗的 Pōhutukawa（Asterope，5.8 等；與 2.5′ 外的 22 Tau 合併約 5.3 等）和 Hiwa-i-te-rangi（Celaeno，5.5 等），要很暗的天空才看得到。
> 紐西蘭北島西岸的部族則以 Puanga（參宿七）為新年星（南島叫 Puaka），它在紐西蘭比昴宿早約一週重現。
> **這幾天抬頭看得到嗎**：昴宿與參宿七下午就落下（6/25 16:20、16:43），晚上看不到。20:00 南偏東高 30° 有心宿二，毛利名 Rehua，天黑到 02:00 都在 10° 以上；20:16 天文昏影結束，22:48 虧凸月（66%）升起。想看昴宿：6/26 清晨 03:30 昴宿在東北東高 10.5°、04:00 約 17°、04:09（太陽 −12°）約 19°；月亮（64%）在南偏東高約 60°、離昴宿 72°，最暗的兩顆不好看。黎明重現的日期（太陽 −12° 時高 ≥3°）：台北 6/8、奧克蘭 6/12、威靈頓 6/13；高 10° 以上：台北 6/16、奧克蘭 6/22、威靈頓 6/25。
> 資料來源：Stellarium 星空文化 maori（Dan Smale）；Mātāmua《Matariki: The Star of the Year》；Te Papa、Te Ara、RNZ；天象以 PyEphem 計算。
> #萬國星空 #師大天文社

## 配音提示

- 中文：昴 ㄇㄠˇ（不讀「昂」）；參宿七的參 ㄕㄣ；宿 ㄒㄧㄡˋ（昴宿、參宿七、心宿二）。
- 毛利語唸法（近似；r 是輕輕彈一下舌頭；wh 在標準語接近 f，但 Whanganui 當地方言唸得接近輕的 w／h；ng 是 singer 的 ng，直接接後面的母音、不要拆成兩個字；長音符號的母音拉長；重音大多在第一音節）：Matariki（**瑪**-搭-里-基）、Pipiri（**皮**-皮-里）、Tangaroa（**當**-阿-羅-阿，ng 連讀）、Rangi Mātāmua（**朗**-伊、**瑪**-**搭**-姆-阿）、Tupuānuku（圖-普-**阿**-努-庫）、Tupuārangi（圖-普-**阿**-朗-伊）、Waitī（外-**替**）、Waitā（外-**搭**）、Waipuna-ā-rangi（外-普-納-**阿**-朗-伊）、Ururangi（**烏**-魯-朗-伊）、Hiwa-i-te-rangi（**希**-瓦-伊-帖-朗-伊）、Pōhutukawa（**坡**-呼-圖-卡-瓦）、Puanga（**普**-阿-ng阿）、Taranaki（**搭**-拉-納-基）、Whanganui（**汪**-阿-努-伊，當地唸法）、Rehua（**雷**-胡-阿）、hautapu（**浩**-搭-普）。
- 09 鏡六個名字一個一個唸清楚，每個名字後面小停，「管」字不要吞掉。
- 13 鏡（4.11）是全片最快的一格：「今晚八點」「明天清晨三點半到四點」兩個時間唸清楚，中間換氣。
- 10 鏡「Pōhutukawa 代表過去一年離開的人」語氣放輕；「而後面這兩顆」之後換回輕快。
- 11 鏡「有點像我們過年」帶一點溫度，不要誇張。
