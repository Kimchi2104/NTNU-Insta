# Handoff Report — Explorer 1 (A-16 & A-17 Remediation Analysis)

## 1. Observation
1. **文獻引用與幻覺檢查**：
   - 在 `04_腳本庫/_審稿/A-16_考據_gemini.md` 第 7 行與 `04_腳本庫/_審稿/A-16_審稿-文化_antigravity.md` 第 15 行，均直接引用了虛構的書名與頁碼：`Barre Toelken, The Anguish of Arrival (1987), pp. 129–130`。Barre Toelken 真實專書為 *The Anguish of Snails: Native American Folklore in the West* (2003) 或 Toelken & Scott (1969)。
   - 本地 `07_資料來源/` 實際可核對原書內頁者僅有：
     - A-16：`07_資料來源/Navojo in America/Star Trails Navajo (Don Childrey)...pdf`，核對頁碼為 pp. 16, 18, 29–39, 42–73, 99–103。在 p. 54 記載納瓦荷兩季時原文作 `"summer, Haz, and winter, Shi"`，確有夏冬 Hai/Shi 印製對調筆誤。
     - A-17：`07_資料來源/Blackfoot in America/Mythology of the Blackfoot Indians.txt`（Wissler & Duvall 1908，核對頁碼 pp. 5–7, 40–44, 58–65, 68–72；且在 p. 42 明載 Four-Tail Lodge）與 `The old north trail...txt`（McClintock 1910，核對頁碼 pp. 26–35, 217–218, 488–501, 521–524）。
   - 在 `A-16_考據_gemini.md`（第 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20 行）與 `A-17_考據_gemini.md`（第 7, 8, 12, 18, 25, 27 行）中，外部未在 `07_資料來源/` 的文獻（如 Haile 1947, Griffin-Pierce 1992, Kluckhohn 1946, Young & Morgan 1987, Jayne 1906, Newcomb 1940, Witherspoon 1977, Chamberlain 1989; Frantz & Russell 2017, Wissler 1911, Miller 1997 等）普遍帶有臆測的頁碼數字（如 `pp. 45–48`、`pp. 156, 172` 等）。
2. **考據第二節（`## 二、清單以外發現的問題`）格式違規**：
   - `04_腳本庫/_審稿/A-16_考據_gemini.md` 第 25–35 行，第二節共收錄 6 列，其中第 1 至 5 列判定全部為 `✓ 證實`（違規），僅第 6 列為 `⚠ 部分正確或需限定`。
   - `04_腳本庫/_審稿/A-17_考據_gemini.md` 第 20–28 行，第二節收錄 4 列皆為 `⚠ 部分正確或需限定`，無 `✓ 證實` 列。
3. **具體天文／文化／敘事／語言偏離**：
   - A-16 老人星顏色：`A-16_考據_gemini.md` 第 9 行與 `A-16_審稿-天文_antigravity.md` 第 13 行未說明老人星本質為 F0 Ib / A9 II 黃白色超巨星，僅因在 Window Rock 仰角 < 2° 承受強烈大氣消光散射而泛紅（或 Haile 1947 另說對應心宿二）。
   - A-16 01 鏡開場白：`A-16_審稿-敘事_antigravity.md` 第 13 行建議改為「同一片星空，納瓦荷看見——」，擅自刪去「人」字並顛倒結構，違反固定定式規範。
   - A-16 05 鏡 hooghan 定義：`A-16_審稿-語言_antigravity.md` 第 14 行建議將「泥土屋 hooghan」改為「傳統霍甘屋」並刪除 `hooghan`，導致 09 鏡再提 `hooghan` 時無定義。
   - A-17 18 鏡木星 Poïa：`A-17_審稿-天文_antigravity.md` 第 13 行與 `A-17_審稿-敘事_antigravity.md` 第 15 行，均在建議改法中徹底刪除了木星（Poïa），斬斷了與 12 鏡晨星之子木星之伏筆回收。
   - A-17 雙胞胎帳篷出處：`A-17_考據_gemini.md` 第 17 行、`A-17_審稿-文化_antigravity.md` 第 16 行指認出處為 Wissler & Duvall 1908 pp. 41–42，但需更明確強調 Four-Tail Lodge 專有名詞與彩繪就在 p. 42，並指正待查核清單稱未找到係漏看了 p. 42。
4. **逐字稿同步狀態**：
   - `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md` 存在，但目前當前工作樹 `04_腳本庫/` 下缺少該檔，需複製同步。

## 2. Logic Chain
1. **防幻覺推理**：依據 `01_網路考據.md` 與 `02_審稿Critic.md` 嚴禁編造頁碼與書目之規定，未親自檢索原書實體頁碼者，標記具體頁數即屬幻覺（hallucination）。因此 Toelken (1987) 必須更正為真實出版物 Toelken (2003)（未核頁碼）；外部專書必須清除臆測頁碼標注「（未核頁碼）」；本地原書（Childrey 2004、Wissler & Duvall 1908、McClintock 1910）則保留真實核實之頁碼。
2. **結構規範推理**：`01_網路考據.md` 明定「## 二、清單以外發現的問題（同上表格式，只列 ✗、⚠、？）」。「✓ 證實」出現在第二節屬於格式違規，必須從第二節刪除，以維持報告之邏輯純粹性。
3. **科普精確性推理**：老人星為光譜型 F0 黃白色恆星，低空顯紅是物理大氣現象，必須在天文與考據檔中釐清；01 鏡「同一片星空，◯◯看見——」為全系列統一開場口號，不得擅自刪改；05 鏡與 09 鏡、12 鏡與 18 鏡分別構成語言與敘事之呼應鏈條，刪除 05 鏡 hooghan 或 18 鏡 Poïa 將破壞腳本內部結構完整性。

## 3. Caveats
- 本 Explorer 代理人為唯讀（Read-Only）探查角色，未直接修改 `04_腳本庫/_審稿/` 下任何交付檔案，所有具體文字修改方案均已詳盡編寫於 `analysis.md` 中。
- 外部書籍未標注頁碼（標記為未核頁碼）完全合乎 SOP 與批次要求，絕不影響審查評級。

## 4. Conclusion
A-16 與 A-17 的 10 份考據與審稿檔案整體考據深厚、天體力學實算極為精確，主要缺失集中在：(1) Barre Toelken 書名與未核外部書目之猜測頁碼；(2) A-16 考據第二節出現 `✓ 證實` 列；(3) A-16 敘事誤改開場定式、語言誤刪 hooghan；(4) A-17 天文與敘事誤刪 18 鏡木星 Poïa；(5) A-17 四尾帳篷出處定位需明確標記 p. 42。所有問題之修訂方案已在 `analysis.md` 中提供逐行精確替換內容，實作代理人可直接套用修訂並完成雙工作區同步。

## 5. Verification Method
1. **文獻與頁碼檢驗**：
   - 檢視修訂後之 `A-16_考據_gemini.md` 與 `A-16_審稿-文化_antigravity.md`，搜尋 `Anguish of Arrival` 應為 0 結果；搜尋 `Toelken` 應顯示 `(2003)（未核頁碼）`。
   - 檢視所有外部書籍引用，應無未核頁碼猜測，全部合規標記為 `（未核頁碼）`。
   - 檢視 `A-17_考據_gemini.md` 第 11 列與文化審稿，確認指出 Four-Tail Lodge 在 Wissler & Duvall 1908 第 42 頁。
2. **考據第二節檢驗**：
   - 檢查 `A-16_考據_gemini.md` 第二節，執行 `grep -n "✓ 證實" 04_腳本庫/_審稿/A-16_考據_gemini.md`，第二節內應為 0 結果（僅第一節有 `✓ 證實`）。
3. **特定修正檢驗**：
   - `A-16_審稿-敘事_antigravity.md`：確認 01 鏡建議保留「同一片星空，納瓦荷人看見——郊狼撒了一地的星星。」
   - `A-16_審稿-語言_antigravity.md`：確認 05 鏡建議保留 `hooghan`。
   - `A-17_審稿-天文_antigravity.md` 與 `A-17_審稿-敘事_antigravity.md`：確認 18 鏡建議保留木星（Poïa）。
4. **天體力學校驗**：
   - 運行 `/Users/kimjoo/.local/bin/uv run --with skyfield python 02_製作流程SOP/verification_harness/verify_batch2_ephemeris.py`，確認 100% 通過。
