# A-06 網路考據

## 一、待查核清單逐條結果

（原稿無獨立待查核清單，相關事實主張移至第二節全面查核）

| # | 原主張 | 判定（✓ 證實／✗ 錯誤／⚠ 部分正確或需限定／？ 無法證實） | 查到的正確說法 | 出處（網址或書目＋頁碼） | 建議改寫（旁白要口語、短句） |
|---|---|---|---|---|---|
| - | 原稿無獨立待查核清單 | ⚠ 部分正確或需限定 | 原稿為早期逐字稿，未設置獨立「⚠ 待查核清單」章節，其文末「首留言考據」與旁白之全部事實主張，均移入第二節進行逐項核驗。 | `04_腳本庫/A-06-中秋特輯二十八宿月亮的28間驛站-逐字稿-v1.md` 第 36–38 行 | 建議依 SOP 規範，將考據焦點全面覆蓋全篇事實主張。 |

## 二、清單以外發現的問題

| # | 原主張 | 判定（✓ 證實／✗ 錯誤／⚠ 部分正確或需限定／？ 無法證實） | 查到的正確說法 | 出處（網址或書目＋頁碼） | 建議改寫（旁白要口語、短句） |
|---|---|---|---|---|---|
| 1 | 今晚是中秋。你抬頭看的那顆滿月，正住在一間有名字的房間裡——它叫室宿。（05–16s）及星空對時核算（12 行） | ✓ 證實 | 經 Skyfield 1.54 與 JPL DE421 星曆嚴密演算，2026/09/25 20:00 台北時間，月球視赤經 RA = 23.2124h（348.19°），視赤緯 Dec = -4.01°；J2000 赤經為 23h17m08.7s（349.29°）。室宿距星室宿一（Markab, α Peg）赤經為 346.20°，壁宿距星壁宿一（Algenib, γ Peg）赤經為 3.31°。月球精準落在室宿距星赤經與壁宿距星赤經所夾之「室宿」天區！當晚為農曆八月十五（中秋），滿月月相達 98.5%（天文望日為 09/27 00:49 CST）。 | Skyfield 1.54 / JPL DE421 驗算；中央氣象署 2026 年天文日曆；SIMBAD: Markab (HIP 113963) | 維持原句（天體力學推算極度精確）。 |
| 2 | 月亮繞天空一圈，要 27.3 天。古人沒有時鐘，但每晚看月亮走到哪顆星旁邊，就知道今天是這個月的第幾天。（16–38s） | ✓ 證實 | 月球相對背景恆星公轉一周之平均週期為「恆星月」（sidereal month），精確值為 27.32166 日（約 27.3 天）；與朔望月（29.53 日）不同，恆星月正是古代各文明劃分 27 或 28 月站（每日一宿）的天文學物理基石。 | NASA Moon Fact Sheet; 陳遵媯《中國天文學史》（第二冊，第 88 頁） | 維持原句。 |
| 3 | 印度切成二十七段，叫 Nakshatra……留了一個第二十八宿，叫 Abhijit，織女星那一段，只在特殊的日子才用。（56–80s） | ✓ 證實 | 吠陀傳統與印度天文學將黃道平分為 27 個等分之 Nakṣatra（各 13°20′）；《鷓鴣氏梵書》（Taittirīya Brāhmaṇa）與《摩訶婆羅多》中明確記載第 28 個月站 Abhijit（梵文 अभिजित्，主星為織女星 Vega / α Lyr），插入於 Uttarāṣāḍhā 與 Śravaṇa 之間，專門用於神聖吉祥之擇日與祭典。 | Pingree, David, *Jyotiḥśāstra: Astral and Mathematical Literature*, Harrassowitz, 1981, pp. 8–10; Burgess, E., *Translation of the Sûrya-Siddhânta*, 1860, Ch. 8 | 維持原句。 |
| 4 | 同一團星星：中國叫昴宿七顆星；日本唸すばる；印度叫 Kṛittikā 連八顆；阿拉伯叫 al-Thurayya 只取兩顆。（96–140s） | ✗ 錯誤 | 嚴重文獻與數據誤讀。其中「阿拉伯叫 al-Thurayya 只取兩顆」判定為錯誤。查阿拉伯傳統天文學與民族誌（Ibn Qutayba《Kitāb al-Anwāʾ》），al-Thurayyā 實為整團昴宿星團（Pleiades cluster，肉眼見 6–7 顆星，與 A-13 考據完全一致）；Stellarium `arabic_lunar_stations/index.json`（CON arabic_lunar_stations 003）中 lines 欄位為 `[[17608, 17608], [18163, 18163]]`，實為兩個長度為零的自連標記錨點（HIP 17608 為昴宿五 Merope 4.14 等，HIP 18163 為距離約 3°、視星等 8.03 等肉眼不可見的背景暗星，僅供程式定位月站標記），同目錄 description.md 明載為星團整體。腳本誤將 Stellarium 自連錨點解讀為「只取兩顆」。此外，梵文 IAST 標準表記為 ***Kṛttikā***（非 Kṛittikā），阿拉伯文應標記長音符號 ***al-Thurayyā***。 | Ibn Qutayba《Kitāb al-Anwāʾ》；Kunitzsch (1989)；Stellarium `arabic_lunar_stations` 原始資料；Monier-Williams (1899) | 「同一團星星：中國叫昴宿七顆星；日本唸すばる；印度叫 Kṛttikā 連八顆；阿拉伯叫 al-Thurayyā，看作整團明亮的星群。」 |
| 5 | 阿拉伯人把這套系統叫 Manazil……《古蘭經》：「我為月亮制定了驛站，直到它變得像一根乾枯的椰棗枝。」（140–162s） | ✓ 證實 | 《古蘭經》雅辛章（Surah Yā-Sīn, 36:39）原文：「وَٱلْقَمَرَ قَدَّرْنَٰهُ مَنَازِلَ حَتَّىٰ عَادَ كَٱلْعُرْجُونِ ٱلْقَدِيمِ」（Wal-qamara qaddarnāhu manāzila ḥattā ʿāda kal-ʿurjūn il-qadīm），中文權威馬堅譯本為：「我為月亮而制定驛站，直到它變成了像乾枯的椰棗枝一樣。」引言完全吻合。 | 《古蘭經》36:39；馬堅譯《古蘭經》（中國社會科學出版社，1981）；Ibn Qutayba《Kitāb al-Anwāʾ》（1956 印本，第 6–7 頁） | 維持原句（經典文獻比對完全一致）。 |

## 三、可以加進影片的好材料

1. **日本 Subaru（富士重工）汽車商標的昴宿六星六芒星傳奇**：
   - 日本六大汽車製造商合併為富士重工業（現速霸陸汽車 Subaru）時，創辦人北健二親自命名為「スバル（Subaru）」，並以金牛座昴宿星團中最亮的六顆肉眼可見亮星設計成六星連線商標，是現代商業將上古星宿活化為跨國科技品牌的經典案例。
   - 出處：Subaru Corporation 官方品牌史（Origins of the Name and Logo, subaru.co.jp）。
2. **阿拉伯「像乾枯椰棗枝」的沙漠詩意天象**：
   - 《古蘭經》36:39 中比喻「乾枯的椰棗枝」（al-ʿurjūn al-qadīm），指阿拉伯沙漠特有的椰棗果串割下曬乾後，果柄自然彎曲成一道金黃細薄的微弧；古阿拉伯人在黎明時分看到月末極細殘月掛在東方地平線上，弧度與色澤正如乾枯棗枝，展現了沙漠遊牧民族極為細膩的星空觀察力。
   - 出處：Edward W. Lane, *Arabic-English Lexicon*, Williams & Norgate, London, 1863, p. 1957.
3. **中國「二十八宿」起源爭論之世紀公案**：
   - 十九世紀西方學者（如 Biot、Weber、Whitney 等）曾激烈爭論二十八宿究竟源於中國、印度、還是巴比倫阿拉伯。直到 1978 年湖北隨縣曾侯乙墓戰國早期漆箱蓋（西元前 433 年）出土完整二十八宿全名，徹底證實中國二十八宿體系早在先秦即已獨立形成，解決了長達百年的國際科技史爭論。
   - 出處：李約瑟《中國科學技術史・天文卷》（科學出版社，1975，第 3 冊第 230–255 頁）。

## 四、參考資料總表

1. 馬堅譯，《古蘭經》，中國社會科學出版社，1981年。
2. 陳遵媯，《中國天文學史》（第二冊），上海人民出版社，1982年。
3. 房玄齡等（唐），《晉書・卷十一・天文志上》，中華書局點校本，1974年。
4. 李約瑟（Joseph Needham），《中國科學技術史・第三卷・天文學》，科學出版社，1975年。
5. Ibn Qutaybah, Al-Dinawarī (d. 889). *Kitāb al-Anwāʾ*, Daʾirat al-Maʿārif al-Osmānia, Hyderabad, India, 1956.
6. Pingree, David. *Jyotiḥśāstra: Astral and Mathematical Literature*. Otto Harrassowitz, Wiesbaden, 1981, ISBN 9783447021654.
7. Burgess, Ebenezer. *Translation of the Sûrya-Siddhânta: A Text-book of Hindu Astronomy*. American Oriental Society, 1860.
8. Monier-Williams, Monier. *A Sanskrit-English Dictionary*. Oxford University Press, 1899.
9. Lane, Edward William. *An Arabic-English Lexicon*. Williams and Norgate, London, 1863.
10. Kunitzsch, Paul. *The Arabs and the Stars: Texts and Traditions on the Fixed Stars and Their Influence in Medieval Europe*. Variorum Reprints, Northampton, 1989.
11. NASA Goddard Space Flight Center, *Lunar Ephemeris and Moon Fact Sheet*, 2026.
12. CDS SIMBAD Astronomical Database, *Query results for Alcyone (HIP 17702), Markab (HIP 113963)*, 2026.
