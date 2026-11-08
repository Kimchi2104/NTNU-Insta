# A-16 & A-17 考據與審稿修訂分析與精確整改方案（Explorer 1 分析報告）

**檔案路徑**：`.agents/teamwork/explorer_a16_a17/analysis.md`  
**分析日期**：2026-10-31  
**分析目標**：`04_腳本庫/_審稿/` 下 A-16 與 A-17 共 10 份考據與審稿檔案之全面清查與整改規劃。

---

## 壹、核心規範與全域整改原則

依據統籌交辦（`ORIGINAL_REQUEST.md` 2026-10-31T21:03:02Z、`SCOPE.md`）及 `01_網路考據.md`、`02_審稿Critic.md`，本次整改嚴格落實以下四大底線原則：

### 一、文獻引用與防幻覺（Anti-Hallucination & Provenance）
1. **嚴禁捏造書名與頁碼**：
   - 徹底移除 `A-16_考據_gemini.md` 與 `A-16_審稿-文化_antigravity.md` 中捏造之書名與頁碼 `Barre Toelken, The Anguish of Arrival (1987), pp. 129–130`。
   - 正確替換為：Barre Toelken 真實著作 *The Anguish of Snails: Native American Folklore in the West* (2003)（未核頁碼）或 Toelken & Scott (1969)〈Poetic Retranslation and the "Pretty Languages" of Yellowman〉（未核頁碼）。
2. **本地 `07_資料來源/` 實際可查核之原書頁碼**：
   - **A-16**：`07_資料來源/Navojo in America/Star Trails Navajo (Don Childrey) (z-library.sk, 1lib.sk, z-lib.sk).pdf`
     - 經實測檢視 PDF 與書頁，真實頁碼包含：pp. 16, 18, 29–39, 42–73, 99–103。
     - **特別勘誤筆誤**：原書 p. 54 記載納瓦荷兩季時寫道 `"summer, Haz, and winter, Shi"`，實為夏冬對調之筆誤（納瓦荷語 Hai 為冬、Shį́ 為夏），考據報告中應保留該頁真實頁碼並指出此筆誤。
   - **A-17**：
     - `07_資料來源/Blackfoot in America/Mythology of the Blackfoot Indians.txt`（Wissler & Duvall 1908）：
       - 真實頁碼：pp. 5–7, 40–44, 58–65, 68–72。
       - **特別指出**：雙胞胎傳說中之神聖「四尾帳篷」（Four-Tail Lodge）彩繪及其象徵野牛尾標記明確記載於 **第 42 頁**（及 p. 41 footnote 1）。逐字稿待查核清單第 11 條稱「pp. 40–44 裡沒找到帳篷畫法」係漏看了第 42 頁，考據與審稿中必須明確指明 p. 42！
     - `07_資料來源/Blackfoot in America/The old north trail, or, Life, legends and religion of the Blackfeet Indians.txt`（McClintock 1910）：
       - 真實頁碼：pp. 26–35, 217–218, 488–501, 521–524。
3. **其餘所有非本地原書之外部專書與文獻**：
   - 包括 A-16 之 Haile 1947、Griffin-Pierce 1992、Kluckhohn & Leighton 1946、Young & Morgan 1987、Jayne 1906、Newcomb 1940、Witherspoon 1977、Matthews 1897、Chamberlain 1989、Schaafsma 1992、IEI 2010；A-17 之 Frantz & Russell 2017、Frantz 2009、Wissler 1911/1912/1918、Miller 1997、Dorsey 1894、Ibn Qutaybah 1956 等。
   - **一律移除推測或編造之具體頁碼數字（如 `pp. 45–48`、`p. 138`、`pp. 156, 172` 等），直接標記為「（未核頁碼）」**！
   - 絕不允許出現「既寫出猜測頁碼又在後方括注未核頁碼」之矛盾寫法。

### 二、考據第二節格式規範（`## 二、清單以外發現的問題`）
1. `01_網路考據.md` 第 30 行明文要求：`## 二、清單以外發現的問題（同上表格式，只列 ✗、⚠、？）`。
2. **第二節絕不可出現 `✓ 證實` 列**！
   - `A-16_考據_gemini.md` 第二節中原有的 5 列 `✓ 證實` 必須全部移除（或若屬清單延伸則併入第一節），確保第二節僅保留 `✗`、`⚠`、`？`。
   - 不得將表頭 changelog 中已標示刪除之鏡頭當作腳本問題。

### 三、A-16 專屬修正要求
1. **16 鏡老人星（Canopus）顏色與天體物理性質**：
   - 在 `A-16_考據_gemini.md` 與 `A-16_審稿-天文_antigravity.md` 中明確澄清：老人星物理光色為黃白色超巨星/亮巨星（光譜型 F0 Ib / A9 II，色指數 $B-V = +0.16$），絕非本質為紅色的恆星。
   - 在納瓦荷族地 Window Rock（35.68°N），老人星南中天幾何仰角僅 1.62°（含折射約 1.86°），因極度貼近地平線，受到強烈大氣消光（消光超過 3 星等）與瑞立散射影響，在低空肉眼觀察才呈現偏紅或橘紅；此外，民族誌記錄（Haile 1947，未核頁碼）指出部分傳統歌會中另有一說將郊狼之星指認為心宿二（Antares，紅超巨星 M1.5 Iab）。
2. **01 鏡固定開場不可刪改**：
   - 在 `A-16_審稿-敘事_antigravity.md` 中，**嚴禁建議刪改 01 鏡固定開場句型「同一片星空，納瓦荷人看見——」**，不可建議刪去「人」字或顛倒句序。
3. **05 鏡 hooghan 定義必須保留**：
   - 在 `A-16_審稿-語言_antigravity.md` 中，**嚴禁建議刪除 05 鏡之 `hooghan` 定義**（因為 09 鏡旁白「就像一家人住在圓圓的 hooghan 裡」再次出現 `hooghan`，05 鏡若刪除將造成 09 鏡無預先定義）。

### 四、A-17 專屬修正要求
1. **18 鏡不可建議刪除木星（Poïa）**：
   - 在 `A-17_審稿-天文_antigravity.md` 與 `A-17_審稿-敘事_antigravity.md` 中，**嚴禁建議在 18 鏡刪除木星（Poïa）**！
   - 理由：逐字稿 12 鏡專門鋪陳了疤臉 Poïa 成為晨星之子木星，18 鏡保留金星（晨星）與木星（Poïa）是為了前後呼應；且 2027/01/15 及 2027/01/22 台北 19:30 木星於東偏北仰角約 7°、20:00 仰角約 14°（視星等 -2.5 等），完全肉眼可見。審稿建議應引導受眾同時辨識晨星與其子木星，將繁複的仰角方位數字交由圖卡承載，而非砍除 Poïa。
2. **雙胞胎四尾帳篷出處精確定位**：
   - 在 `A-17_考據_gemini.md`、`A-17_審稿-文化_antigravity.md`、`A-17_審稿-天文_antigravity.md` 中，明確指認 Wissler & Duvall (1908) 原書第 42 頁（及 p. 41 腳註 1）之 Four-Tail Lodge（四尾彩繪帳篷），糾正腳本待查核清單第 11 條稱未載帳篷之疏漏。

---

## 貳、A-16 五份檔案逐檔問題剖析與精確修改內容

---

### 檔案 1：`04_腳本庫/_審稿/A-16_考據_gemini.md`

#### 【當前問題】
1. **第 7 行（第一節第 1 列）**：出現虛假書名與捏造頁碼 `Barre Toelken, The Anguish of Arrival (1987), pp. 129–130`；外部專書 `IEI (2010/2017), p. 8` 出現猜測頁碼。
2. **第 8 行（第一節第 2 列）**：外部專書出現猜測頁碼 `Griffin-Pierce (1992), pp. 45–48; Clyde Kluckhohn & Dorothea Leighton (1946), p. 138; IEI (2010), p. 12`。
3. **第 9 行（第一節第 3 列）**：外部文獻出現猜測頁碼 `Haile (1947), pp. 14–16; Griffin-Pierce (1992), pp. 140–142`；且未明確說明老人星本質為黃白色超巨星、因地平消光泛紅或 Haile 心宿二另說之天體物理機制。
4. **第 10 行（第一節第 4 列）**：外部字典出現猜測頁碼 `Young & Morgan (1987), pp. 581, 624`。
5. **第 11 行（第一節第 5 列）**：外部文獻出現猜測頁碼 `Haile (1947), pp. 7–9`。
6. **第 12 行（第一節第 6 列）**：外部文獻出現猜測頁碼 `Haile (1947), pp. 7–9`；未備註 Childrey p. 54 夏冬對調筆誤。
7. **第 13 行（第一節第 7 列）**：外部文獻出現猜測頁碼 `Griffin-Pierce (1992), pp. 132–135`。
8. **第 16 行（第一節第 10 列）**：外部文獻出現猜測頁碼 `Kluckhohn & Leighton (1946), pp. 60–62; Griffin-Pierce (1992), p. 50`。
9. **第 17 行（第一節第 11 列）**：外部文獻出現猜測頁碼 `Haile (1947), pp. 20–22; Griffin-Pierce (1992), pp. 120–125`。
10. **第 18 行（第一節第 12 列）**：外部文獻出現猜測頁碼 `Caroline F. Jayne (1906), pp. 10–15; Franc J. Newcomb (1940), p. 42`。
11. **第 19 行（第一節第 13 列）**：外部文獻出現猜測頁碼 `Young & Morgan (1987), p. 386`。
12. **第 20 行（第一節第 14 列）**：外部論文出現猜測頁碼 `Von Del Chamberlain (1989), pp. 18–25; Polly Schaafsma (1992), p. 118`。
13. **第 25–35 行（第二節）**：第二節列出 6 列，其中第 1 至 5 列判定全部為 `✓ 證實`！嚴重違反「第二節只列 ✗、⚠、？」之規則。
14. **第 41–50 行（第三節）**：出現猜測頁碼 `Jayne (1906), pp. 10–15; IEI (2010), p. 14`；`Chamberlain (1989), pp. 18–25`；`Witherspoon (1977), pp. 24–30`。
15. **第 62 行（第四節第 7 項）**：出現猜測頁碼 `Chamberlain (1989), pp. 18–25`。

#### 【精確整改方案（建議實作者直接套用）】

- **第 7 行（出處欄）替換為**：
  `Indigenous Education Institute (IEI), Navajo Skies: Education and Activity Guide (2010/2017)（未核頁碼）; Barre Toelken, The Anguish of Snails: Native American Folklore in the West (2003)（未核頁碼）; Don Childrey (2004) pp. 16, 99–103`
- **第 8 行（出處欄）替換為**：
  `Trudy Griffin-Pierce, Earth Is My Mother, Sky Is My Father (1992)（未核頁碼）; Clyde Kluckhohn & Dorothea Leighton, The Navaho (1946)（未核頁碼）; IEI, Navajo Skies (2010)（未核頁碼）`
- **第 9 行（查到的正確說法與出處欄）替換為**：
  查到的正確說法欄增補老人星光色說明：「……然而 Berard Haile（1947）民族誌記錄指出，部分歌會傳承中亦有將天狼星或極低天體視為郊狼之星，另有一說視為心宿二（Antares，紅超巨星）。天體物理上，老人星（Canopus）本質為黃白色超巨星（F0 Ib / A9 II，B-V = +0.16），僅因在納瓦荷族地 Window Rock（35.68°N）仰角最高不到 2°，強烈大氣消光與瑞立散射使其在低空肉眼呈現紅色。片中審慎使用『很多人認為，就是老人星』，符合民俗多義性與天象觀測真實。」
  出處欄改為：`Don Childrey, Star Trails: Navajo (2004), p. 72; Father Berard Haile, Starlore among the Navaho (1947)（未核頁碼）; Trudy Griffin-Pierce (1992)（未核頁碼）`
- **第 10 行（出處欄）替換為**：
  `Robert W. Young & William Morgan, The Navajo Language (1987)（未核頁碼）; Diné College Navajo Studies Department materials (未核頁碼)`
- **第 11 行（出處欄）替換為**：
  `Don Childrey, Star Trails: Navajo (2004), pp. 18, 32–39; Father Berard Haile, Starlore among the Navaho (1947)（未核頁碼）`
- **第 12 行（查到的正確說法與出處欄）替換為**：
  查到的正確說法備註：`（注：Childrey 原書 p. 54 提及夏冬 Hai/Shi 存在印製對調筆誤，納瓦荷語 Hai 實為冬、Shį́ 為夏）。`
  出處欄改為：`Don Childrey (2004), pp. 38, 54; Father Berard Haile (1947)（未核頁碼）`
- **第 13 行（出處欄）替換為**：
  `Don Childrey (2004), p. 62; Stellarium navajo/index.json (CON navajo 006); Trudy Griffin-Pierce (1992)（未核頁碼）`
- **第 16 行（查到的正確說法與出處欄）替換為**：
  查到的正確說法中引文改為：`（Kluckhohn & Leighton, 1946; Griffin-Pierce, 1992; Childrey, 2004, p. 50）`
  出處欄改為：`Clyde Kluckhohn & Dorothea Leighton, The Navaho (1946)（未核頁碼）; Trudy Griffin-Pierce (1992)（未核頁碼）; Don Childrey (2004), p. 50`
- **第 17 行（出處欄）替換為**：
  `Father Berard Haile, Starlore among the Navaho (1947)（未核頁碼）; Trudy Griffin-Pierce (1992)（未核頁碼）; Don Childrey (2004), p. 66`
- **第 18 行（出處欄）替換為**：
  `Caroline F. Jayne, String Figures and How to Make Them (1906)（未核頁碼）; Franc J. Newcomb, Navaho Omens and Taboos (1940)（未核頁碼）; Gary Witherspoon (1977)（未核頁碼）`
- **第 19 行（出處欄）替換為**：
  `Robert W. Young & William Morgan (1987)（未核頁碼）; Navajo Nation Department of Diné Education, Diné Culture & Language Curriculum Guide (2015)（未核頁碼）`
- **第 20 行（出處欄）替換為**：
  `Von Del Chamberlain, "Navajo Constellations in Canyon de Chelly", Earth & Sky (1989)（未核頁碼）; Polly Schaafsma, Rock Art in New Mexico (1992)（未核頁碼）`
- **第 25–35 行（第二節整改）**：
  將原有判定為 `✓ 證實` 的第 1 至 5 列全部移除！僅保留符合規範之 `⚠ 部分正確或需限定` 項目。重構第二節表格如下：
  ```markdown
  ## 二、清單以外發現的問題

  | # | 原主張 | 判定（✓ 證實／✗ 錯誤／⚠ 部分正確或需限定／？ 無法證實） | 查到的正確說法 | 出處（網址或書目＋頁碼） | 建議改寫（旁白要口語、短句） |
  |---|---|---|---|---|---|
  | 1 | 08 鏡稱仙后座為「五顆星」，Stellarium navajo CON 002 卻包含多達 13 顆星。 | ⚠ 部分正確或需限定 | 仙后座傳統肉眼辨識特徵為顯著的「W」形五顆亮星（王良四、王良一、策、閣道三、閣道二），Childrey 書中亦稱黑神擺放了五顆星；但 Stellarium 現代模組 CON 002 卻擴充納入了周邊多顆暗星（總數達 13 顆）。逐字稿旁白忠於民族誌口傳「對面再擺五顆，一個女人」，符合肉眼可見特徵，畫面連線需提示美宣避免開啟暗星雜線。 | Don Childrey (2004), pp. 35, 50; Stellarium `navajo/index.json` | 旁白維持「對面再擺五顆，一個女人」；畫面製作提示建議僅勾勒 W 形五顆肉眼亮星。 |
  | 2 | 16 鏡稱郊狼的星（老人星）為紅色，或畫面示意將其標為紅星。 | ⚠ 部分正確或需限定 | 老人星（Canopus, HIP 30438）本質為黃白色超巨星/亮巨星（光譜型 F0 Ib / A9 II，色指數 B-V = +0.16），物理光色非紅色。其在納瓦荷族地 Window Rock（35.68°N）南中天仰角最高僅 1.62°（含大氣折射約 1.86°），係因極低地平線強烈大氣消光與瑞立散射而呈現泛紅視感；另依 Haile (1947) 記錄，部分納瓦荷傳統歌會另有一說將郊狼星視為心宿二（Antares，紅超巨星 M1.5 Iab）。解說時需釐清天體本質與地平大氣光學效應。 | CDS SIMBAD Astrometric Database; Don Childrey (2004), p. 72; Father Berard Haile (1947)（未核頁碼） | 旁白維持「很多人認為，就是老人星」；畫面與備忘提示老人星物理本質為黃白星，因地平大氣消光而泛紅，或另說對應心宿二。 |
  ```
- **第 41–50 行（第三節好材料）**：
  移除所有外部書頁碼，改為 `（未核頁碼）`：
  - 第 1 條出處改為：`Caroline F. Jayne, String Figures and How to Make Them (1906)（未核頁碼）; IEI Navajo Skies (2010)（未核頁碼）.`
  - 第 2 條出處改為：`Von Del Chamberlain, "Navajo Constellations in Canyon de Chelly", Earth & Sky (1989)（未核頁碼）.`
  - 第 3 條出處改為：`Gary Witherspoon, Language and Art in the Navajo Universe (Univ. of Michigan Press, 1977)（未核頁碼）.`
- **第 62 行（第四節第 7 項）**：
  改為：`7. Chamberlain, Von Del. "Navajo Constellations in Canyon de Chelly", Earth & Sky: Visions of the Cosmos in Native American Folklore, 1989（未核頁碼）.`

---

### 檔案 2：`04_腳本庫/_審稿/A-16_審稿-天文_antigravity.md`

#### 【當前問題】
1. **第 13 行（審查意見表第 1 列，16 鏡）**：問題與建議改法中未明確指出老人星本質光譜型為 F0 Ib / A9 II 黃白色超巨星，以及其在 Window Rock 因低空大氣消光散射而泛紅、或 Haile 1947 另指心宿二之關鍵事實。
2. **第 92 行（星名對照表）**：現代天體性質欄原寫 `F0II 白色亮巨星`，需補充為 `F0 Ib / A9 II 黃白色超巨星（低空受大氣消光顯紅色）`。

#### 【精確整改方案】
- **第 13 行「問題」欄增補**：
  在「畫面規格與天球赤緯防裁切限制……」之後，增補：「……此外，需釐清老人星天體物理光色：老人星（Canopus）為 F0 Ib / A9 II 黃白色超巨星（B-V = +0.16），本質非紅星；納瓦荷族地 Window Rock（35.68°N）其南中天仰角僅 1.6°–1.9°，強烈大氣消光散射方顯泛紅視感（或民族誌 Haile 1947 另說對應紅超巨星心宿二）。美宣若渲染老人星色彩，需注意真實物理本色與地平大氣消光效果之科學嚴謹性。」
- **第 92 行「西方天體性質」欄修改為**：
  `F0 Ib / A9 II 黃白色超巨星（Window Rock 地平仰角 <2° 大氣消光顯紅色）`

---

### 檔案 3：`04_腳本庫/_審稿/A-16_審稿-文化_antigravity.md`

#### 【當前問題】
1. **第 15 行（02–03 鏡 依據欄）**：出現虛假書名與捏造頁碼 `Indigenous Education Institute (2010); Barre Toelken (1987) pp. 129–130`。
2. **第 13、14、16、17 行（各意見之依據欄）**：外部文獻出現未核對頁碼（如 `Haile (1947) pp. 7–9`、`Griffin-Pierce (1992) pp. 88–92`、`Witherspoon (1977) pp. 24–30`、`Griffin-Pierce (1992) pp. 110–114`）。

#### 【精確整改方案】
- **第 13 行（依據欄）改為**：
  `聯合國《原住民族權利宣言》（UNDRIP）；Navajo Nation Historic Preservation Department 儀式影像倫理指引；Griffin-Pierce (1992)（未核頁碼）`
- **第 14 行（依據欄）改為**：
  `Father Berard Haile (1947)（未核頁碼）; Trudy Griffin-Pierce (1992)（未核頁碼）; 原住民文化主權倫理規範`
- **第 15 行（依據欄）改為**：
  `Indigenous Education Institute (2010)（未核頁碼）; Barre Toelken, The Anguish of Snails (2003)（未核頁碼）`
- **第 16 行（依據欄）改為**：
  `Gary Witherspoon (1977)（未核頁碼）; Paul Radin, The Trickster (1956)（未核頁碼）; Childrey (2004) pp. 37–39`
- **第 17 行（依據欄）改為**：
  `Griffin-Pierce (1992)（未核頁碼）; Childrey (2004) pp. 44–46`

---

### 檔案 4：`04_腳本庫/_審稿/A-16_審稿-敘事_antigravity.md`

#### 【當前問題】
1. **第 4 行（最重要的三個問題第 1 點）**：批評 01 鏡開場鋪墊，建議調整開場句型。
2. **第 13 行（01 鏡審查意見）**：建議改法寫為「同一片星空，納瓦荷看見——郊狼撒了一地的星星。接續上週獵戶腰帶……」，**擅自刪去了「人」字，並顛倒了原稿固定句式**，違反交辦規範「不可建議刪改 01 鏡固定開場句型『同一片星空，納瓦荷人看見——』」。

#### 【精確整改方案】
- **第 4 行「最重要的三個問題」第 1 點改為**：
  `第一，01 鏡開場需嚴格遵守系列統一定式「同一片星空，納瓦荷人看見——郊狼撒了一地的星星」，文字不可刪改，但前 3 秒畫面構想宜將大字字卡「郊狼撒了一地的星星」第一時間破題淡入，迅速抓住隨機滑動受眾；`
- **第 13 行「問題」與「建議改法」欄修正為**：
  - **問題欄**：`短影音前 3 秒注意力捕獲與統一定式保護：本系列各集均有嚴格固定之開場定式（02_審稿Critic.md 第 57 行），01 鏡「同一片星空，納瓦荷人看見——郊狼撒了一地的星星」文字必須一字不差完整保留，絕不可擅改句型或刪去「人」字！審稿重點應在於視聽節奏：原稿前 6 秒鋪陳上週獵戶座，畫面可提早於前 3 秒同步浮現醒目字卡「郊狼撒了一地的星星」，在定式旁白念出時達成視聽雙重破題。`
  - **建議改法欄**：`嚴格維持原稿固定開場白，一字不改：「上週，我們跟著獵戶腰帶繞了地球一圈。今天到美國西南，納瓦荷人的家：同一片星空，納瓦荷人看見——郊狼撒了一地的星星。」（50字，12秒，語速4.17字/秒）。畫面製作強化：開場第 1 秒字卡「郊狼撒了一地的星星」（9字）直接亮起破題，長圖自獵戶迅速推展至全天星點。`

---

### 檔案 5：`04_腳本庫/_審稿/A-16_審稿-語言_antigravity.md`

#### 【當前問題】
1. **第 4 行（最重要的三個問題第 2 點）**：建議將 05 鏡「泥土屋 hooghan」直接改為「傳統霍甘屋」，導致原語名詞缺失。
2. **第 14 行（05 鏡審查意見）**：建議改法寫為「很久以前，神聖的人們在第一座傳統霍甘屋裡造世界……」，**徹底刪除了 `hooghan` 原語定義**，導致 09 鏡再次出現「就像一家人住在圓圓的 hooghan 裡」時失去語意根基，違反交辦規範「不可建議刪除 05 鏡的 hooghan（因為 09 鏡會再次出現 hooghan，05 鏡必須保留定義）」。

#### 【精確整改方案】
- **第 4 行「最重要的三個問題」第 2 點改為**：
  `第二，05 鏡首次引入納瓦荷傳統居所泥土屋 hooghan，此處定義不可刪除（09 鏡將再次出現 hooghan 圍繞中央爐火之家庭象徵），但口播需注意外語音節與漢語輔助詞之搭配，避免聽覺認知模糊；`
- **第 14 行「問題」與「建議改法」欄修正為**：
  - **問題欄**：`外來文化核心名詞之首次定義與前後呼應：納瓦荷傳統泥土屋 hooghan（音近霍-甘）為本集核心文化符號。05 鏡作為 hooghan 首次登場之鏡頭，必須明確保留其名稱與「泥土屋」之定義，萬不可將 hooghan 刪除；否則 09 鏡旁白「就像一家人住在圓圓的 hooghan 裡」再次出現時，觀眾將毫無先驗認知而產生嚴重聽覺中斷。審稿建議應在保留「泥土屋 hooghan」之基礎上，優化配音提示與字卡同音輔助。`
  - **建議改法欄**：`旁白維持原稿嚴謹定義：「其中一個版本說：很久以前，神聖的人們在第一座泥土屋 hooghan 裡造世界，用彩色的沙畫出大地母親、天空父親。」（51字，13秒，語速3.92字/秒）。字卡增補音義標記：「第一座泥土屋 hooghan」（10字）。配音提示叮嚀：「hooghan 念『霍-甘』，泥土屋三字需咬字清晰，建立 09 鏡名詞基礎。」`

---

## 參、A-17 五份檔案逐檔問題剖析與精確修改內容

---

### 檔案 6：`04_腳本庫/_審稿/A-17_考據_gemini.md`

#### 【當前問題】
1. **第 7 行（第一節第 1 列）**：外部辭典出現猜測頁碼 `Donald G. Frantz & Norma Jean Russell (2017, pp. 156, 172, 388)`。
2. **第 8 行（第一節第 2 列）**：外部著作出現猜測頁碼 `Clark Wissler, The Social Life of the Blackfoot Indians (1911, pp. 3–5)`。（注：同列之 Wissler & Duvall 1908 p. 5 為本地已核原書，應保留）。
3. **第 9 行（第一節第 3 列）**：McClintock 1910 本地原書中，Ch. I pp. 1–25 與 Ch. II pp. 26–35 中，核實頁碼為 pp. 26–35。
4. **第 12 行（第一節第 6 列）**：外部專書出現猜測頁碼 `Dorcas S. Miller (1997, p. 243)`。
5. **第 17 行（第一節第 11 列）**：雙胞胎傳說與帳篷畫法中，未明確強調 **Four-Tail Lodge 即在 Wissler & Duvall 1908 原書第 42 頁**，且未指出腳本待查核清單第 11 條稱「pp. 40–44 沒找到帳篷畫法」係漏看了第 42 頁。
6. **第 18 行（第一節第 12 列）**：外部文獻出現猜測頁碼 `J. O. Dorsey (1894); Ibn Qutaybah (1956)`。
7. **第 25 行（第二節第 2 列）**：外部文獻出現猜測頁碼 `Clark Wissler (1911, p. 38)`。
8. **第 27 行（第二節第 4 列）**：外部文法書出現猜測頁碼 `Donald G. Frantz, Blackfoot Grammar (2009, pp. 3–7)`。
9. **第 47 行（第四節第 5 項）**：出現猜測頁碼 `Dorcas S. Miller... 1997, pp. 243–250`。

#### 【精確整改方案】
- **第 7 行（出處欄）改為**：
  `Donald G. Frantz & Norma Jean Russell, Blackfoot Dictionary of Stems, Roots, and Affixes (3rd ed., Univ. of Toronto Press, 2017)（未核頁碼）; Galt Museum Blackfoot Protocols`
- **第 8 行（出處欄）改為**：
  `Clark Wissler & D. C. Duvall, Mythology of the Blackfoot Indians (AMNH Anthropological Papers, Vol. II, Part I, 1908, p. 5); Clark Wissler, The Social Life of the Blackfoot Indians (1911)（未核頁碼）`
- **第 9 行（出處欄）改為**：
  `Walter McClintock, The Old North Trail (Macmillan, 1910, pp. 26–35, 217–218, 488–501, 521–524)`
- **第 12 行（出處欄）改為**：
  `McClintock (1910, p. 500); Dorcas S. Miller (1997)（未核頁碼）; Stellarium blackfoot index.json`
- **第 17 行（查到的正確說法與出處欄）增補修訂**：
  查到的正確說法改為：`經重新詳查 Wissler & Duvall (1908) 原典全文：雙胞胎傳說收錄於 pp. 40–44，其中【第 42 頁明文記載】神祕男子傳授給雙胞胎父親 Smart-Crow 的神聖帳篷稱為「四尾帳篷」（Four-Tail Lodge），帳篷外懸掛四根野牛尾巴（兩母兩公）作為召喚野牛群之標誌，第 41 頁腳註 1 更明確註解「此為彩繪帳篷之旗幟標記（flag for a painted lodge）」。腳本待查核清單第 11 條稱『pp. 40–44 裡沒找到帳篷畫法』係漏看了第 42 頁。Miller 與 Stellarium 之轉述確有所本。`
  出處欄改為：`Wissler & Duvall, Mythology of the Blackfoot Indians (1908, pp. 41–42 含 p. 41 Footnote 1 與 p. 42 Four-Tail Lodge 正文)`
- **第 18 行（出處欄）改為**：
  `McClintock (1910, Appendix p. 522); J. O. Dorsey, A Study of Siouan Cults (1894)（未核頁碼）; Ibn Qutaybah, Kitāb al-Anwāʾ (1956)（未核頁碼）`
- **第 25 行（出處欄）改為**：
  `McClintock (1910, p. 219); Clark Wissler (1911)（未核頁碼）`
- **第 27 行（出處欄）改為**：
  `Donald G. Frantz, Blackfoot Grammar (2nd ed., Univ. of Toronto Press, 2009)（未核頁碼）`
- **第 47 行（第四節第 5 項）改為**：
  `5. Dorcas S. Miller, Stars of the First People: Native American Star Myths and Constellations, Pruett Publishing / Westwinds Press, 1997（未核頁碼）.`

---

### 檔案 7：`04_腳本庫/_審稿/A-17_審稿-天文_antigravity.md`

#### 【當前問題】
1. **第 13 行（審查意見表第 1 列，18 鏡）**：建議改法將旁白改為「今晚八點，昴宿就在頭頂。想看北斗，等到十點過後整組升起；明天清晨五點半往東南看，最亮的就是晨星金星。」**擅自將木星（Poïa）完全刪除**！違反交辦要求「不可建議在 18 鏡刪除木星（Poïa），因為 12 鏡保留晨星三口之家正是為了與 18 鏡的金星＋木星前後呼應」。
2. **第 79 行（星名對照表）**：雙胞胎行記載 Four-Tail Lodge，宜明確備註原典出處為 Wissler & Duvall (1908) p. 42。

#### 【精確整改方案】
- **第 13 行「問題」與「建議改法」欄修正為**：
  - **問題欄**：`台北觀星實務地平遮蔽引導與行星呼應完整性：經 Skyfield 1.54 演算 2027/1/15 20:00 CST 台北，北斗七星僅天樞（13.0°）與天璇（10.6°）勉強出地平，末端搖光遲至 21:48 升起，台北盆地東北低空易受遮擋，字卡宜加註「北斗十點後全升起」。更關鍵的是：【絕對不可建議刪除木星 Poïa】！逐字稿 12 鏡已專門鋪陳 Poïa 成為晨星之子木星，18 鏡「明晨五點半東南方的晨星金星」與「晚上七點半東方升起的木星 Poïa」係前後呼應之晨星三口之家結構。2027/1/15（及 1/22）台北 19:30 木星仰角約 7°、20:00 仰角約 14°（視星等 -2.5 等），完全肉眼可見。審稿意見必須完整保留金星與木星 Poïa！`
  - **建議改法欄**：`旁白維持晨星父子前後呼應，微調地平提醒：「今晚八點，昴宿就在頭頂。明天清晨五點半往東南看是晨星金星；而晚上七點半升起的木星，就是他的兒子 Poïa。（想看北斗，十點後整組高懸）。」（62字/15秒＝4.13字/秒）。字卡維持「今晚與明晨」（5字）。圖卡加註「北斗斗口 20:00 出地平，22:00 全組高懸；木星 19:37 東升 14°」。`
- **第 79 行「傳統文化涵義」欄修改為**：
  `神奇雙胞胎，傳授四尾彩繪帳篷（Four-Tail Lodge，Wissler & Duvall 1908 p. 42）`

---

### 檔案 8：`04_腳本庫/_審稿/A-17_審稿-文化_antigravity.md`

#### 【當前問題】
1. **第 4 行（最重要的三個問題第 3 點）與第 16 行（審查意見第 4 列）**：指出雙胞胎四尾帳篷時寫 `原書 pp. 41–42 明載`，需更明確指證 **Four-Tail Lodge 專有名詞與彩繪傳授正文即在原書第 42 頁**，並直指腳本待查核清單第 11 條稱未載帳篷畫法係漏看了第 42 頁。
2. 檢查各依據欄，確保無未核對外部專書頁碼。

#### 【精確整改方案】
- **第 4 行第 3 點修訂為**：
  `第三，原稿備忘誤以為 Wissler & Duvall 沒載明雙胞胎的帳篷畫法，經查原書第 42 頁明文記載即為神聖的「四尾帳篷」（Four-Tail Lodge，p. 41 腳註 1 亦註明為彩繪帳篷標記），腳本待查核清單稱未找到係漏看 p. 42，首留言應予明確補充。`
- **第 16 行「問題」與「建議改法」欄修訂為**：
  - **問題欄**：`原典出處考據勘誤：原稿備忘誤以為 Wissler & Duvall 沒載明帳篷畫法，實則原書【第 42 頁明文記載】神祕人傳授給雙胞胎之父 Smart-Crow 的神聖帳篷即為著名的「四尾帳篷」（Four-Tail Lodge），四角懸掛四根野牛尾巴以召喚野牛，第 41 頁腳註 1 更直接指明「此為彩繪帳篷之旗幟標記（flag for a painted lodge）」。腳本待查核清單第 11 條稱沒找到帳篷畫法，係漏看了第 42 頁。首留言宜補齊此段出處。`
  - **建議改法欄**：`首留言補充：「雙子座雙胞胎傳說解釋了著名的『四尾彩繪帳篷』（Four-Tail Lodge）之起源，四角懸掛野牛尾象徵召喚牛群（Wissler & Duvall 1908 p. 42，p. 41 腳註 1）。」`

---

### 檔案 9：`04_腳本庫/_審稿/A-17_審稿-敘事_antigravity.md`

#### 【當前問題】
1. **第 4 行（最重要的三個問題第 3 點）**：批評 18 鏡塞入三個時刻，建議將木星 Poïa 等資訊完全砍掉移交圖卡。
2. **第 15 行（審查意見第 3 列，18 鏡）**：建議改法將旁白改為「今晚八點，昴宿就在頭頂。想看北斗，等到十點過後整組升起；明天清晨五點半往東南看，最亮的就是晨星金星。」**直接將木星（Poïa）刪除**！違反交辦要求「不可建議在 18 鏡刪除木星（Poïa），因為 12 鏡保留晨星三口之家正是為了與 18 鏡金星＋木星前後呼應」。

#### 【精確整改方案】
- **第 4 行第 3 點修訂為**：
  `第三，18 鏡在 13 秒內串聯今晚昴宿、明晨金星與晚間木星 Poïa，其中木星 Poïa 是 12 鏡晨星之子鋪陳的關鍵回收，不可刪除；但口播時宜精簡方位度數，將細部仰角交由圖卡「今晚與明晨」承載，以平衡敘事流暢度。`
- **第 15 行「問題」與「建議改法」欄修正為**：
  - **問題欄**：`晨星父子結構呼應與資訊降載平衡：18 鏡連續提及昴宿、晨星金星與木星 Poïa。需特別注意：【絕對不可建議刪除木星 Poïa】！逐字稿 12 鏡刻意保留了疤臉 Poïa 成為晨星（木星）的情節，18 鏡在片尾點出木星 Poïa，正是為了與 12 鏡形成強烈的敘事回收（回扣晨星三口之家）。若刪去木星，12 鏡的鋪陳將淪為無效伏筆。敘事降載的正確做法是保留金星與木星 Poïa 的角色關係，而將繁複的方位角與度數交由定格圖卡承載。`
  - **建議改法欄**：`旁白精煉並完整保留晨星父子：「今晚八點，昴宿就在頭頂。明天清晨五點半往東南看，最亮的是晨星金星；而晚上七點半升起的木星，就是他的兒子 Poïa。」（53字/13秒＝4.08字/秒）。字卡維持「今晚與明晨」（5字）。畫面提示「截圖存下觀星圖卡」，詳細方位度數由圖卡呈現。`

---

### 檔案 10：`04_腳本庫/_審稿/A-17_審稿-語言_antigravity.md`

#### 【當前審查確認】
1. 表格欄位、六欄格式、三行摘要完整合規。
2. 嚴重度標記僅使用 `🔴`、`🟡`、`⚪`。
3. 旁白字速（≤ 4.5 字/秒）與字卡長度（≤ 14 字）均已達標。
4. 經逐條文獻依據清查，本檔依據欄無未核頁碼之幻覺引用。維持當前高水準版本。

---

## 肆、實作者執行清單（Actionable Implementation Checklist）

實作代理人（Implementer）可依序執行下列步驟完成修改：

1. [ ] **同步 A-16 v0 逐字稿**：
   - 將 `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md` 複製至工作樹 `04_腳本庫/` 下，確保內容 100% 保持 0 修改。
2. [ ] **修訂 A-16 五份檔案**：
   - `04_腳本庫/_審稿/A-16_考據_gemini.md`：
     - 替換第 1 條 fake citation（Toelken 2003 未核頁碼）。
     - 清除外部專書未核頁碼，Childrey 保留 p. 18, 29–39, 42–73, 99–103 並備註 p. 54 筆誤。
     - 第二節徹底刪除 5 列 `✓ 證實`，確保第二節僅含 `⚠`（仙后座暗星、老人星黃白光色與消光）。
     - 第三、四節清除外部頁碼。
   - `04_腳本庫/_審稿/A-16_審稿-天文_antigravity.md`：
     - 16 鏡補述老人星 F0 Ib / A9 II 黃白色超巨星、低空大氣消光散射顯紅及 Haile 1947 心宿二另說。
   - `04_腳本庫/_審稿/A-16_審稿-文化_antigravity.md`：
     - 移除第 15 行 Toelken (1987) 假書名，換為 Toelken (2003)（未核頁碼）；清理外部頁碼。
   - `04_腳本庫/_審稿/A-16_審稿-敘事_antigravity.md`：
     - 01 鏡嚴禁刪改「同一片星空，納瓦荷人看見——」固定定式。
   - `04_腳本庫/_審稿/A-16_審稿-語言_antigravity.md`：
     - 05 鏡嚴禁刪除 `hooghan` 定義。
3. [ ] **修訂 A-17 五份檔案**：
   - `04_腳本庫/_審稿/A-17_考據_gemini.md`：
     - 清理外部書目頁碼（Frantz & Russell 2017、Wissler 1911、Miller 1997 等）。
     - 第一節第 11 列指出 Wissler & Duvall 1908 原書 p. 42 明載 Four-Tail Lodge，指正待查核清單漏看 p. 42。
     - 確認第二節僅含 4 列 `⚠`，無 `✓ 證實` 列。
   - `04_腳本庫/_審稿/A-17_審稿-天文_antigravity.md`：
     - 18 鏡嚴禁建議刪除木星（Poïa），保持晨星三口之家呼應；指出 Four-Tail Lodge 在 p. 42。
   - `04_腳本庫/_審稿/A-17_審稿-文化_antigravity.md`：
     - 明確指證 Four-Tail Lodge 在 Wissler & Duvall 1908 原書第 42 頁。
   - `04_腳本庫/_審稿/A-17_審稿-敘事_antigravity.md`：
     - 18 鏡嚴禁建議刪除木星（Poïa），確保 12 鏡伏筆完整回收。
   - `04_腳本庫/_審稿/A-17_審稿-語言_antigravity.md`：
     - 確認格式合規無誤。
4. [ ] **雙工作區同步與校驗**：
   - 將修訂後之 10 份檔案同步複製至 `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/`。
   - 執行 SHA-256 對比確保完全一致。
   - 運行 `uv run --with skyfield python 02_製作流程SOP/verification_harness/verify_batch2_ephemeris.py` 與 schema 驗證工具。
