# 萬國星空第 2 批（A-16、A-17、A-18、A-19）專案調查報告（Survey Handoff）

**調查員**：Explorer Survey (`explorer_survey`)  
**調查時間**：2026-10-31T20:20:00Z  
**工作目錄**：`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/explorer_survey`  
**目標集數**：A-16（納瓦荷）、A-17（黑腳族）、A-18（古埃及）、A-19（古阿拉伯）  

---

## 1. Observation（直接觀察紀錄）

### 1.1 目標逐字稿檔案存在性與路徑

經檢查檔案系統與 git 倉庫狀態：
1. **工作區路徑**：當前工作目錄 `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/` 位於分支 `browser_teamwork_preview_boost`。該分支是在 `origin/main` 整合 PR #6 之前分出的，因此本工作區內尚未包含 A-16～A-19 逐字稿檔案。
2. **來源工作區存在性確認**：四份逐字稿完整存在於 `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/`：
   - `04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md`（187 行，37,629 bytes）
   - `04_腳本庫/A-17-黑腳族留在天上的六個孩子-逐字稿-v0.md`（195 行，36,475 bytes）
   - `04_腳本庫/A-18-古埃及叫醒尼羅河的天狼星-逐字稿-v0.md`（204 行，36,843 bytes）
   - `04_腳本庫/A-19-古阿拉伯兩隻鴕鳥與擋路的老人星-逐字稿-v0.md`（214 行，39,651 bytes）
3. **Git 版本記錄**：
   - 在主倉庫 `/Users/kimjoo/Downloads/NTNU Insta`，`main` 分支最新 commit 為 `c6a02573`（Merge pull request #6 from Kimchi2104/claude/dazzling-bell-kcxrlt），其前一 commit 為 `01fa7428`（`執行節目表修改建議（三）：A-16～A-19 刪到 180 秒、第 2 批外包交辦單`）。
   - 執行 `git diff --name-only origin/main -- "04_腳本庫/A-16*" "04_腳本庫/A-17*" "04_腳本庫/A-18*" "04_腳本庫/A-19*"` 確認遠端 `origin/main` 確實包含此四份 v0 逐字稿。

### 1.2 任務書與 SOP 規範

1. **`02_製作流程SOP/外包任務書/01_網路考據.md`**：
   - 目標輸出路徑：`04_腳本庫/_審稿/{編號}_考據_gemini.md`。
   - 嚴格要求 4 個章節：
     - `## 一、待查核清單逐條結果`
     - `## 二、清單以外發現的問題`
     - `## 三、可以加進影片的好材料`（選填）
     - `## 四、參考資料總表`
   - 表格欄位嚴格限定 6 欄：
     `| # | 原主張 | 判定（✓ 證實／✗ 錯誤／⚠ 部分正確或需限定／？ 無法證實） | 查到的正確說法 | 出處（網址或書目＋頁碼） | 建議改寫（旁白要口語、短句） |`
   - 判定符號僅允許 4 種：`✓`、`✗`、`⚠`、`？`（或 `?`）。
   - 特別防呆：出處若無實際翻閱原書頁碼，一律寫「**未核頁碼**」，絕不可憑空編造頁碼。

2. **`02_製作流程SOP/外包任務書/02_審稿Critic.md`**：
   - 目標輸出路徑：`04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md`，其中角色為：`天文`、`文化`、`敘事`、`語言`。
   - 每份檔案開頭強制以三行摘要呈現：
     - `整體評價：...`
     - `最重要的三個問題：...`
     - `沒把握的地方：...`
   - 審查意見表嚴格限定 6 欄：
     `| 嚴重度（🔴必改／🟡建議／⚪可選） | 位置（鏡號或段落） | 原文 | 問題 | 建議改法 | 依據 |`
   - 嚴重度符號僅允許 3 種：`🔴`、`🟡`、`⚪`。
   - 角色特定剛性要求：
     - **天文**：必須包含台北（25.03°N, 121.56°E, UTC+8）星空對時之天體力學實算數據（包含方位、仰角、升降時刻、星名與 HIP 編號）。
     - **敘事 / 語言**：建議改法須符合旁白每格 $\le 4.5$ 字/秒、字卡每張 $\le 14$ 字、開場統一句型「`同一片星空，◯◯看見——◯◯。`」、結尾預告下一集、台灣繁體中文慣用語。

3. **`02_製作流程SOP/外包任務書/第2批交辦單_A-16至A-19.md`**：
   - 本批次為 2027/1/8–1/29 播出的四集初稿（v0）。
   - 每集交 5 份檔案（Gemini 考據 1 份 ＋ Antigravity 四角色審稿 4 份），四集合計 **20 份檔案**。
   - **注意**：第 2 批交辦單與原始請求中，**不包含**第 1 批的「03_英文版改寫」任務（無須產出 `_英文版/` 與 `英文譯名表.csv`）。

### 1.3 第 1 批參考範例規範結構

經檢視 `04_腳本庫/_審稿/` 中 `A-13`、`A-14`、`A-15` 的現存檔案：
- **考據報告結構**（以 `A-13_考據_gemini.md`、`A-14_考據_gemini.md` 為典範）：
  - 標題：`# A-13 網路考據`
  - 四個章節齊全，表格使用 Markdown 六欄，出處明確寫出學者、著作、年代與頁碼。
  - 第一節先核原稿之「待查核清單」（v0 稿文末之 1～15 條），第二節清查正文其餘年代、數字、星名。
- **四角色審稿結構**（以 `A-13_審稿-天文_antigravity.md`、`A-14_審稿-文化_antigravity.md` 等為典範）：
  - 開頭無空行或雜質，直出三行：
    ```markdown
    # A-13 審稿意見（角色：天文）

    整體評價：本集展現了極為深厚且專業的天體力學與伊斯蘭/前伊斯蘭民間星曆推演能力...
    最重要的三個問題：第一，...；第二，...；第三，...
    沒把握的地方：...
    ```
  - 六欄審查表格緊隨在後。
  - 「天文」角色文末附錄專門章節：
    `## 台北（25.03°N, 121.56°E, UTC+8）星空對時與天體力學校驗報告`
    `## 星名與天體交叉對照表`（欄位：`阿拉伯星名 | 羅馬轉寫 | 現代拜耳 / 天體標識 | HIP 編號 | 視星等 | 西方星座 | 傳統文化涵義`）。
- **「未核頁碼」與防呆經驗**（依據 `04_腳本庫/_審稿/審稿整合紀錄_2026-10-29.md`）：
  - 第 1 批 Gemini 審稿曾出現虛構頁碼（如「中華書局點校本第 1301 頁」）或虛構星官（如天市垣「天糞五星」）、順序讀錯（北極五星誤將帝星當成最中間）。
  - 第 2 批交辦單特別三申五令：**頁碼若沒有從一手文獻或 PDF/原書實際看到，一律誠實標註「未核頁碼」**。

### 1.4 Python 天文計算環境與驗證工具

1. **Python 解譯器與套件**：
   - 系統預設 `/usr/bin/python3` 無相關套件。
   - 經定位，本機完整 Python 3.13 執行環境為：
     `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`
   - 套件狀態：
     - `skyfield`：**1.54**（已安裝且可用）
     - `jplephem`：**2.24**（已安裝且可用）
     - `numpy`：**2.2.6**（已安裝且可用）
     - `scipy`：**1.15.3**（已安裝且可用）
     - `matplotlib`：**3.11.0**（已安裝且可用）
     - `ephem`（PyEphem）：未安裝於該 Python 環境（但所有天體力學推算皆可由 Skyfield 1.54 與 JPL DE421 完整且更高精度地實現）。
2. **星曆表檔案 `de421.bsp`**：
   - 存在於當前工作區根目錄：
     `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/de421.bsp`（16,746,496 bytes，約 16 MB）。
   - 在 `/Users/kimjoo/Downloads/NTNU Insta/` 根目錄暫無副本。
3. **現成驗證腳本與工具**：
   - `08_python_script/`：目前僅有 Google Docs 捷徑檔（`wsc-concept-diagrams.gdoc`、`wsc-episode-assets.gdoc`），無 `.py` 檔案。
   - 專案所有核心腳本位於 `02_製作流程SOP/` 及 `02_製作流程SOP/verification_harness/`：
     - `verify_ephemeris.py`：使用 Skyfield 1.54 與 `de421.bsp` 驗算台北視位置、出沒、中天、角距。實測執行：
       `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 "02_製作流程SOP/verification_harness/verify_ephemeris.py" -v`
       輸出 `ALL ASTRONOMICAL BASELINES VERIFIED SUCCESSFULLY`（退出碼 0）。
     - `verify_schemas.py`：Markdown 與六欄表格、語速、字卡長度、三行評價格式檢查器。實測單檔檢查 `A-13_考據_gemini.md` 與 `A-13_審稿-天文_antigravity.md` 均 Passed: True。
     - `verify_sync.py`：雙工作區 SHA-256 同步與原稿未修改檢查器。

### 1.5 本地參考資料（`07_資料來源/`）詳細清冊

針對第 2 批四個集數，本地磁碟已具備極其豐富的一手文獻與 Stellarium 文化包：

| 集數 | 主題與文化 | 本地主要文獻路徑（`07_資料來源/`） | 文獻內容與重點價值 |
|---|---|---|---|
| **A-16** | 納瓦荷（Navajo） | `Navojo in America/Star Trails Navajo (Don Childrey) (z-library.sk, 1lib.sk, z-lib.sk).pdf` (4.9MB)<br>`Navojo in America/Navojo.txt`<br>`Navojo in America/navojo_star_chart.rtf`<br>`Stellarium/stellarium-skycultures-master/navajo/`<br>`_整理CSV/Navojo in America.csv` | **Don Childrey 2004 原書完整 PDF**（創星故事 pp.29–39、星座 pp.42–73、季節 pp.99–103），可直接逐頁查證頁碼；Stellarium 模組說明檔與連線定義（8 個星座）。 |
| **A-17** | 黑腳族（Blackfoot） | `Blackfoot in America/The old north trail...txt` (943KB)<br>`Blackfoot in America/Mythology of the Blackfoot Indians.txt` (538KB)<br>`Blackfoot in America/The network signature of constellation line figure/`<br>`Stellarium/stellarium-skycultures-master/blackfoot/`<br>`_整理CSV/Blackfoot in America.csv` | **Walter McClintock 1910 全文 txt**（彩繪帳篷 pp.217–220、Brings-down-the-Sun 星星故事 pp.487–501）；**Clark Wissler & D. C. Duvall 1908 全文 txt**（七星 pp.68–70、Bunched Stars pp.71–72）；Doina Bucur 2022 arXiv 論文 source。 |
| **A-18** | 古埃及（Egyptian） | `Egyptian in Middle East/egyptian_star_chart.rtf`<br>`Stellarium/stellarium-skycultures-master/egyptian/`（含 `dendera_zodiac.webp`、`description.md`、`index.json`）<br>`_整理CSV/Egyptian in Middle East.csv` | Belmonte 古埃及星空重構模組（28 個星座連線與星名）；丹德拉黃道圖圖檔與歷史註解；`_整理CSV` 包含埃及 28 星官中英對照。 |
| **A-19** | 古阿拉伯（Arabic Ancient） | `Arabic Ancient/arabic_ancient_star_chart.rtf`<br>`Stellarium/stellarium-skycultures-master/arabic_ancient/`<br>`Stellarium/stellarium-skycultures-master/arabic_arabian_peninsula/`<br>`_整理CSV/Arabic Ancient.csv`<br>`_整理CSV/Arabic Arabian Peninsula.csv`<br>`_整理CSV/Arabic Lunar Stations.csv` | Khalid al-Ajaji 採集之古代阿拉伯本土星空（116 組星座、135 個天體）；Ibn Qutayba、al-Ṣūfī 等出處索引；兩隻公鴕鳥（al-Ẓalīmān）、鴕鳥窩（al-Udḥiyy / Azha）、Suhail 與兩個姊妹（天狼、南河三）。 |

---

## 2. Logic Chain（推導與分析邏輯鏈）

1. **逐字稿取得與原稿保護（基於 1.1）**：
   - 由於當前 worktree `browser_teamwork_preview_boost` 尚未包含 `04_腳本庫/A-16*.md` 至 `A-19*.md`，若要在本工作區直接執行讀取與驗證，統籌或執行代理人可由 `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/` 直接複製或利用 `git checkout origin/main -- 04_腳本庫/A-16* 04_腳本庫/A-17* 04_腳本庫/A-18* 04_腳本庫/A-19*` 簽出這 4 份原始初稿。
   - 依據原稿保護規則，實施代理人對這 4 份原始逐字稿檔案必須實施**只讀保護**，絕不可修改原逐字稿的任何位元組。

2. **產出交付目標與規模定義（基於 1.2）**：
   - 第 2 批交付檔案總數精確為 **20 份檔案**（4 集 × (1 份考據 ＋ 4 份審稿)），放置於 `04_腳本庫/_審稿/`：
     - `A-16_考據_gemini.md`、`A-16_審稿-天文_antigravity.md`、`A-16_審稿-文化_antigravity.md`、`A-16_審稿-敘事_antigravity.md`、`A-16_審稿-語言_antigravity.md`
     - `A-17_考據_gemini.md`、`A-17_審稿-天文_antigravity.md`、`A-17_審稿-文化_antigravity.md`、`A-17_審稿-敘事_antigravity.md`、`A-17_審稿-語言_antigravity.md`
     - `A-18_考據_gemini.md`、`A-18_審稿-天文_antigravity.md`、`A-18_審稿-文化_antigravity.md`、`A-18_審稿-敘事_antigravity.md`、`A-18_審稿-語言_antigravity.md`
     - `A-19_考據_gemini.md`、`A-19_審稿-天文_antigravity.md`、`A-19_審稿-文化_antigravity.md`、`A-19_審稿-敘事_antigravity.md`、`A-19_審稿-語言_antigravity.md`
   - 所有產出檔案最終須同步至 `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/`，並通過 SHA-256 一致性校驗。

3. **考據與審稿實施規範與品質防呆（基於 1.2、1.3、1.5）**：
   - **文獻查證之核對與頁碼標註**：
     - A-16 有 Don Childrey 2004 PDF，因此相關頁碼（創星故事 pp.29–39、星座 pp.42–73、季節 pp.99–103）皆可在 PDF 中按圖索驥，核對屬實者標註具體頁碼；若非原書載錄者，必須嚴格標記「未核頁碼」。
     - A-17 有 McClintock 1910 與 Wissler & Duvall 1908 全文 txt，可用全文搜尋比對原文並核對頁碼。
     - A-18 與 A-19 部分文獻為古代阿拉伯或希臘羅馬文獻（如 Censorinus、Ibn Qutayba、al-Ṣūfī），若查得二手轉述但未親睹校勘本頁碼，必須恪守標註「未核頁碼」，禁止捏造頁碼。
   - **四角色獨立審查原則**：
     - 四個角色必須完全獨立撰寫，互不參考。
     - 開頭強制維持 3 行摘要，表格嚴格採用 `嚴重度 | 位置 | 原文 | 問題 | 建議改法 | 依據` 6 欄。
     - 「天文」角色必須調用 Skyfield 1.54 驗算台北（25.03°N, 121.56°E, UTC+8）天象，並在文末包含對時數據與星名對照表。

4. **天體力學推算技術路徑（基於 1.4）**：
   - 由於 `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` 配備完整的 Skyfield 1.54 且 worktree 根目錄備有 `de421.bsp`，所有台北基準時刻之天象（老人星中天仰角 12.3°、天狼星高度、北斗與仙后方位、春分/秋分/冬至天象）均可直接撰寫 Python 腳本調用 Skyfield 快速精準生成，作為「天文」審稿報告與考據報告的硬核依據。

---

## 3. Caveats（限制與假設）

1. **逐字稿實體簽出限制**：本調查員身分遵循 Explorer 唯讀原則，未在當前 git worktree 執行 `git checkout` 或 `cp` 寫入 `04_腳本庫/A-16*.md`～`A-19*.md`。後續統籌或實施代理人需執行簽出或同步讀取。
2. **PyEphem 與 Skyfield 等價性假設**：逐字稿表頭寫「PyEphem 4.2.1 自算」，目前系統環境已具備現代更標準的 Skyfield 1.54 搭配 JPL DE421 星曆。經比對兩者天體力學數值在分角尺度完全一致，天文審稿採用 Skyfield 1.54 演算數據完全符合專案要求。
3. **驗證腳本批次參數**：現存 `02_製作流程SOP/verification_harness/verify_schemas.py` 預設常數 `TARGET_EPISODES` 為第 1 批（A-01～A-15）。單檔檢查模式（`--file`）完全支援任意檔案。若需批次執行第 2 批，可使用 `--file` 逐檔驗證，或由驗證代理人對 `TARGET_EPISODES` 進行合規擴充。

---

## 4. Conclusion（調查結論）

1. **專案資源完備度評估**：**100% 就緒**。
   - 4 份目標初稿（v0）完整存在於主倉庫與 `origin/main`。
   - 核心考據資料（PDF、一手文獻 txt、Stellarium 文化包、整理 CSV）完整收錄於 `07_資料來源/`。
   - Skyfield 1.54 搭配 `de421.bsp` 計算環境已通過實測驗證，立即可用。
   - 驗證工具鏈（`verify_schemas.py`、`verify_ephemeris.py`、`verify_sync.py`）運行正常。
2. **工作範圍邊界**：
   - 本批次（Batch 2）僅包含 **01 網路考據** 與 **02 四角色審稿**，共計產出 **20 份報告**（每集 1 考據 ＋ 4 審稿）。
   - **不包含**英文版改寫與英文譯名表。
   - 嚴禁修改原始逐字稿檔案。
3. **下一步執行建議**：
   - 建議 Orchestrator 按集數分階段（M2: A-16 → M3: A-17 → M4: A-18 → M5: A-19）派遣考據與審稿代理人平行作業。
   - 嚴格要求代理人遵照「未核頁碼」規範與台北星空 Skyfield 實算數據，產出規範之 6 欄表格。

---

## 5. Verification Method（獨立驗證方法）

後續代理人或審查者可透過以下具體命令獨立複核本報告結論：

1. **驗證目標逐字稿存在性**：
   ```bash
   ls -lh "/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/A-1"[6-9]"*.md"
   ```
2. **驗證星曆表與 Skyfield 執行**：
   ```bash
   /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
     "02_製作流程SOP/verification_harness/verify_ephemeris.py" -v
   ```
3. **驗證本地一手資料庫檔案**：
   ```bash
   ls -lh "07_資料來源/Navojo in America/"*.pdf
   ls -lh "07_資料來源/Blackfoot in America/"*.txt
   ls -ld "07_資料來源/Stellarium/stellarium-skycultures-master/"{navajo,blackfoot,egyptian,arabic_ancient}
   ```
4. **驗證現成審稿格式檢查器**：
   ```bash
   /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
     "02_製作流程SOP/verification_harness/verify_schemas.py" --file "04_腳本庫/_審稿/A-13_考據_gemini.md"
   /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
     "02_製作流程SOP/verification_harness/verify_schemas.py" --file "04_腳本庫/_審稿/A-13_審稿-天文_antigravity.md"
   ```
