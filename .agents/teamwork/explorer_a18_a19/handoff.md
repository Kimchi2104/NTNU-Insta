# Handoff Report — Explorer 2 (A-18 & A-19 Remediation)

## 1. Observation
1. **本地資料庫實勘**：
   - 經檢查 `07_資料來源/Egyptian in Middle East/` 僅包含 `egyptian_star_chart.rtf`；`07_資料來源/Arabic Ancient/` 等阿拉伯目錄僅包含 `.rtf` 檔案，本地並無 Censorinus、Parker 1950、Neugebauer & Parker、Hurst 1952、Ball 1939、Petrie 1883、Buchwald & Josefowicz 2010、Sethe 1908、Ibn Qutayba 1956、al-Ṣūfī、Ibn Durayd、Ibn Manẓūr、Ibn al-Jawzī、Ibn Ḥibbān、Kunitzsch 1961、Kunitzsch & Smart 2006、Lane 1863、ʿUmar ibn Abī Rabīʿa 等任何實體原書或 PDF。
2. **外部書籍頁碼標註與自相矛盾**：
   - 在 `A-18_考據_gemini.md`（第 9–19 行）與 `A-18_審稿-文化_antigravity.md`（第 15–17 行）中，外部專書多處出現推測頁碼（例如 Hurst 1952 `pp. 63–78`、Petrie 1883 `pp. 38–43`、Buchwald & Josefowicz `pp. 31–48` 等）。
   - 在 `A-19_考據_gemini.md`（第 7–16 行）中，出現了「既寫猜測頁碼又寫未核頁碼」之自相矛盾：例如 `vol. 1, p. 488；未核頁碼`、`vol. 1, p. 152；未核頁碼`、`vol. 1, p. 106；未核頁碼`、`pp. 97–98, 114–115；未核頁碼`。
3. **第二節格式與漏項**：
   - `A-18_考據_gemini.md` 與 `A-19_考據_gemini.md` 之第二節（`## 二、清單以外發現的問題`）均僅包含 `✗` 與 `⚠`，無任何 `✓ 證實` 列。
   - 但 `A-18_考據_gemini.md` 第二節漏列了逐字稿第 97 行天狼星 2027/01/25 台北升落時刻存在 8 分鐘誤差之重要事實（逐字稿寫「17:00 升起 → 22:29 中天 → 03:58 落下」實為 1/23 時刻；1/25 真實視運動為 16:52 升起 → 21:00 仰角 43.7° → 22:21 中天 → 03:51 落下）。
4. **開場白固定句型違規**：
   - `A-18_審稿-敘事_antigravity.md`（第 13 行）建議在固定句前插入自創句「在幾乎不下雨的埃及，天上的星就是生命訊號。」，違反《02_審稿Critic.md》第 13、57 行規範。
   - `A-19_審稿-敘事_antigravity.md`（第 14 行）建議改為「同一片星空，古阿拉伯看見——一座沙漠動物園」，擅自刪除了「古阿拉伯人」中的「人」字，違反固定句型一字不差之要求。
5. **A-19 老人星大氣折射校驗**：
   - 經 Skyfield 1.54 驗算台北 2027/01/29：幾何 0° 地平升落為 18:16 升 / 01:12 落；計入標準大氣折射（-34'）後真視時刻為 18:11 升 → 21:44 中天（仰角 12.34°）→ 01:17 落。逐字稿第 63、76 行寫「18:10 升起、01:17 落下」完全正確。`A-19_審稿-天文_antigravity.md` 第 30–33 行原校驗數據僅列純幾何出沒（18:15 升、01:12 落），需修正並在審查表格以 `⚪可選` 註記折射正確性。

## 2. Logic Chain
1. 依據《01_網路考據.md》第 6 條與《02_審稿Critic.md》第 59 行：「頁碼與書目只寫你真的看到的；沒有實際查到頁碼，就寫『未核頁碼』；不要憑印象補頁碼或書名」。基於 Observation 1 & 2，本地無原書且出現猜測頁碼及格式矛盾，必須全面移除所有猜測頁碼，統一明確標記為 `（未核頁碼）`。
2. 依據《01_網路考據.md》第 30 行與專題勘誤要求，第二節必須只列 `✗`、`⚠`、`？`。基於 Observation 3，現有檔案無 `✓ 證實`，但漏列天狼星 1/25 8 分鐘誤差，必須於 `A-18_考據_gemini.md` 第二節新增 `⚠` 條目，並同步更新 `A-18_審稿-天文_antigravity.md`。
3. 依據短影音開場白白皮書規範，第一鏡固定開場句型必須一字不差（「同一片星空，古埃及人看見——◯◯」、「同一片星空，古阿拉伯人看見——◯◯」）。基於 Observation 4，A-18 敘事不可前置插入其他句子、A-19 敘事不可刪除「人」字；兩者均應採將固定句移至全片第一句破題之方案，後接簡化轉場，維持語速 ≤ 4.5 字/秒。
4. 基於 Observation 5，大氣折射對近地平（如 12° 之老人星）天體視出沒影響達 5 分鐘以上，逐字稿 18:10/01:17 係採用折射後之標準數值，天文審稿應給予正面科學背書，避免將正確算式誤批為錯誤。

## 3. Caveats
1. 未直接修改 `04_腳本庫/_審稿/` 下任何檔案（嚴格遵守 Explorer Read-Only 調查約束）。
2. 所有精確修訂程式碼（TargetContent / ReplacementContent）與行號已完整記錄於 `analysis.md`，可供 Implementer 立即執行。
3. 外部文獻之出版年與版本資訊均已依權威學術書目校正，未更動其學術論點本質。

## 4. Conclusion
A-18 與 A-19 的 10 份審查檔案整體考據扎實、天體力學推步高深，但存在文獻頁碼標註不實與格式矛盾、天狼星 1/25 對時誤差漏列、開場白固定句型變更違規，以及老人星大氣折射出沒數據需精準背書等問題。所有修正方案均已擬定完畢，行號與替換區塊明確，可交由後續代理人實施修訂並同步雙工作區。

## 5. Verification Method
1. **定量規範校驗**：
   執行 `/Users/kimjoo/.local/bin/uv run --with skyfield python 02_製作流程SOP/verification_harness/verify_schemas.py --file "<檔案路徑>"`，檢查 10 份檔案全數通過（Passed: True，語速 ≤ 4.5 字/秒，字卡 ≤ 14 字）。
2. **天體力學校驗**：
   執行 `/Users/kimjoo/.local/bin/uv run --with skyfield python 02_製作流程SOP/verification_harness/verify_batch2_ephemeris.py`，確認 A-18（Sirius 22:33、Full Moon 20:17、歲差 38 天）與 A-19（Canopus 21:44、銀道座標、光度比 661x）全數通過。
3. **雙工作區 SHA-256 同步驗證**：
   修改完成後，以 `sha256sum` 比對工作區與 `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/` 下對應 10 份檔案，驗證雜湊值完全相同。
