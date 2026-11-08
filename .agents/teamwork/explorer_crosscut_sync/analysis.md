# 萬國星空科普短影音系列：第 2 批（A-16 至 A-19）跨組規範、查核腳本與同步狀態調查報告

**報告路徑**：`.agents/teamwork/explorer_crosscut_sync/analysis.md`  
**調查代理人**：Explorer 3 (Sync & Verification Explorer)  
**日期**：2026-10-31  
**工作目標**：定位既有驗算與查核腳本、釐清執行環境與通過條件、確認 `A-16` v0 檔案狀態與複製指令、盤點 `04_腳本庫/_審稿/` 20 份交付檔案的 SHA-256 同步現狀，以及清查 `07_資料來源/` 本地原書與外部文獻標註規範。

---

## 一、驗證腳本、執行環境與判定條件

### 1. Python 執行環境定位
在當前 macOS 環境中，系統預設 `/usr/bin/python3` 以及專案目錄下的虛擬環境 `/Users/kimjoo/Downloads/NTNU Insta/.venv/bin/python` 均未安裝天文計算函式庫 `skyfield`。
- **有效 Python 直譯器絕對路徑**：
  ```bash
  /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
  ```
- **已安裝套件與相依性**：Python 3.13、Skyfield 1.54、NumPy、SciPy、zoneinfo、JPL 曆表 `de421.bsp`（位於工作樹根目錄 `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/de421.bsp`）。

---

### 2. 既有驗證腳本盤點與執行指令

| 腳本路徑 | 功能說明 | 執行指令 | 通過條件與判定依據 |
|---|---|---|---|
| `02_製作流程SOP/verification_harness/verify_batch2_ephemeris.py` | 第 2 批 4 集（A-16～A-19）天體力學物理數據驗證 | `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 02_製作流程SOP/verification_harness/verify_batch2_ephemeris.py` | **Exit Code 0**：<br>1. **A-16**：台北 2027/01/08 老人星中天 23:07 CST（折射仰角 12.33°，方位 180.0°）；搖光升起 22:16 CST（方位 32.88°，23:00 仰角 5.43°）；北極星仰角 25.48°。<br>2. **A-17**：台北 2027/01/15 昴宿六天頂 20:00 CST（仰角 88.76°）；北斗天樞 13.03°、天璇 10.62°、搖光升起 21:48 CST；Browning MT 全天恆顯性與 54 天昴星團偕日隱沒期。<br>3. **A-18**：台北 2027/01/22 天狼星中天 22:33 CST（仰角 48.23°）；望月時刻 20:17:23 CST；歲差位移 38 天（前 2500 至 2027 年）。<br>4. **A-19**：台北 2027/01/29 老人星中天 21:44 CST（仰角 12.33°）；銀道座標分割；光度比 661x、距離比 36x。<br>*(實測結果：目前 100% CONFIRMED 通過)* |
| `02_製作流程SOP/verification_harness/verify_schemas.py` | 單檔 Markdown Schema 與量化約束檢核 | `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 02_製作流程SOP/verification_harness/verify_schemas.py --file <檔案路徑> [--type <research\|critic>]` | **Exit Code 0**：<br>1. 考據檔：具備四個標準章節、六欄表格、判定欄含 ✓/✗/⚠/？、出處非空。<br>2. 審稿檔：開頭具備三行摘要、六欄表格、嚴重度含 🔴/🟡/⚪、字卡 ≤14 字、旁白語速 ≤4.5 字/秒、天文角色具備台北座標與對時數據。 |
| `02_製作流程SOP/verification_harness/verify_sync.py` | 原稿不可篡改性檢核（Git Status） | `python3 02_製作流程SOP/verification_harness/verify_sync.py --check-immutability-only` | **Exit Code 0**：`04_腳本庫/*.md` 原有追蹤逐字稿檔案在 `git status --porcelain` 中無任何 M（修改）、D（刪除）、R（重新命名）紀錄。 |
| `.agents/teamwork/explorer_crosscut_sync/verify_batch2_r2_rules.py` | **第 2 批 R2 專項防呆與雙區同步整合驗證器**（新建立） | `python3 .agents/teamwork/explorer_crosscut_sync/verify_batch2_r2_rules.py` | **Exit Code 0**：<br>1. `A-16` v0 檔案存在且 SHA-256 與 Downloads 一致。<br>2. 原稿 0 修改。<br>3. 4 份考據第二節 0 個 ✓ 證實。<br>4. 0 處捏造書名 `Anguish of Arrival`。<br>5. 07 外部文獻一律標註 `（未核頁碼）`。<br>6. A-16～A-19 各集特定規則落實。<br>7. 20 份審稿檔案雙工作區 SHA-256 100% 一致。 |

---

## 二、`A-16` 初稿逐字稿（v0）狀態與同步指令

### 1. 存在狀態確認
- **Downloads 目錄**：`/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md`  
  - 狀態：**存在**
  - 檔案大小：`37,629` 位元組
  - SHA-256：`9240e0bedcf174c989457cfc0a0266874fe4d55801817071aaa460e3eb3ee740`
- **當前工作樹（Worktree）**：`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md`  
  - 狀態：**不存在（MISSING）**

### 2. Worker 執行複製之確切指令
為落實 0 修改且精確複製，Worker 請執行以下命令：
```bash
cp -p "/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md" "04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md"
```
複製完成後，請檢驗其 SHA-256：
```bash
shasum -a 256 "04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md"
# 預期值：9240e0bedcf174c989457cfc0a0266874fe4d55801817071aaa460e3eb3ee740
```

---

## 三、`04_腳本庫/_審稿/` 20 份交付檔案現況盤點

經以專案稽核程式比對，工作樹與 Downloads 鏡像目前均存在這 20 份檔案，且在修訂前的 SHA-256 完全一致。但各檔案內部均存在待修訂的 R2 問題（詳見下表）：

| # | 檔名 | 工作樹 | Downloads | 現況 SHA-256 | R2 待修訂項目摘要 |
|---|---|:---:|:---:|---|---|
| 1 | `A-16_考據_gemini.md` | ✓ | ✓ | `8252e43b37aa9fbb41f2b38663e0aef7215b4bc6e0b427bcd36843638231d984` | 1. 刪除捏造書名 `Anguish of Arrival` 改為 `Anguish of Snails (2003)（未核頁碼）`<br>2. 第二節移除 5 列 `✓ 證實`（移入第一節或刪除）<br>3. Haile, Griffin-Pierce 等外部專書頁碼改標 `（未核頁碼）`<br>4. 補充 16 鏡老人星黃白光色與消光泛紅說明 |
| 2 | `A-16_審稿-天文_antigravity.md` | ✓ | ✓ | `4357b890b275353d6710eab1ed82bb1eb0188341c80c7f48c82fb33cadbb5b74` | 補充 16 鏡老人星物理光色為黃白（F0 Ib），因超低空（仰角<2°）大氣消光泛紅之說明 |
| 3 | `A-16_審稿-文化_antigravity.md` | ✓ | ✓ | `e73908179cb24da8a6cd537e5b05090ea64921d22d275c75d44037d9faf556be` | 移除 `Toelken (1987) pp. 129` 等假頁碼，改為 `（未核頁碼）` |
| 4 | `A-16_審稿-敘事_antigravity.md` | ✓ | ✓ | `c9ca114751b46db0c25524a47c8f054a0308b79b5c855960418014ac2e70bbd1` | 確保絕不建議修改 01 鏡「同一片星空，納瓦荷人看見——」固定句型 |
| 5 | `A-16_審稿-語言_antigravity.md` | ✓ | ✓ | `e29bea74078d3d35460112ff9fe46a0f6cdc15732711b68b633d22f7cb7bf7bb` | 確保絕不建議刪除 05 鏡之 `hooghan` 定義（因 09 鏡會再次出現） |
| 6 | `A-17_考據_gemini.md` | ✓ | ✓ | `ccc7082976e5a8aac613460c0df5f63901e5b1e36091be059f698de09018ad8c` | 1. 外部語言學書 Frantz 2017/2009 移除頁碼改標 `（未核頁碼）`<br>2. 指出待查核清單引 Wissler & Duvall 漏了 p. 42（Four-Tail Lodge 在 p. 42）<br>3. 保留本地原書 Wissler 1908 與 McClintock 1910 真實頁碼 |
| 7 | `A-17_審稿-天文_antigravity.md` | ✓ | ✓ | `862e489c2a8811d1e65127c64400677060b96e7741de7933d901b7d255b4f761` | 確保絕不建議在 18 鏡刪除木星（Poïa），因與 12 鏡晨星三口呼應 |
| 8 | `A-17_審稿-文化_antigravity.md` | ✓ | ✓ | `a79db42b533874f76a3f8797a28d4c9f38899714141a8f63f0fc92a615f83fd8` | 指出 Four-Tail Lodge 帳篷彩繪在 Wissler & Duvall (1908) p. 42 |
| 9 | `A-17_審稿-敘事_antigravity.md` | ✓ | ✓ | `1cc9f45f72c6851010d38566852a2d0c46ed5cc6bc4075c7893fe7a6096cc440` | 確保絕不建議在 18 鏡刪除木星（Poïa） |
| 10 | `A-17_審稿-語言_antigravity.md` | ✓ | ✓ | `65c1f1b94700d39434cc87b1e541edbed4fde4fbacd4eccd15fd20bc00f68ff2` | 外部文獻改標 `（未核頁碼）` |
| 11 | `A-18_考據_gemini.md` | ✓ | ✓ | `529c95021b3ec91e12b55d832d9e02778ac18f9556a8927494fc8ea869b49840` | 1. 第二節增補 ⚠：逐字稿對時 2027/01/25 天狼星時刻與真值差 8 分鐘（真實為 16:52 升、21:00 仰角 43.7°、22:21 中天、03:51 落）<br>2. 外部專書（Parker, Neugebauer, Hurst, Ball, Petrie 等）全部改標 `（未核頁碼）` |
| 12 | `A-18_審稿-天文_antigravity.md` | ✓ | ✓ | `04d798c283aeae69220b31eeef0f003e5e5ac637933dcf6dfba7a2bff253554c` | 增列 2027/01/25 天狼星 16:52 升起、22:21 中天之精確數值審查意見 |
| 13 | `A-18_審稿-文化_antigravity.md` | ✓ | ✓ | `5233606e95229a65526db30807f1940ec45d071a216b909228372ff9a2b2b16f` | 外部埃及專書（Parker 1969, 1950 等）頁碼全部改標 `（未核頁碼）` |
| 14 | `A-18_審稿-敘事_antigravity.md` | ✓ | ✓ | `0d3cf2090b3162fb7864c55b2aa7bbfe4d2dcd18eb1ab08447a619feb84d75ee` | 確保絕不建議在 01 鏡「同一片星空，古埃及人看見——」前插入引言 |
| 15 | `A-18_審稿-語言_antigravity.md` | ✓ | ✓ | `9ca08cb7f9911b6b3fa08375007e3f9a6c15e9c328dd3e4aa79a8c4e0825e543` | 外部文獻改標 `（未核頁碼）` |
| 16 | `A-19_考據_gemini.md` | ✓ | ✓ | `0f511e0f37fab3d8aa68af18b57e10d47dc84cf8fe6e6d6e5531a77b9ed7fe33` | 1. 外部阿拉伯專書（Ibn Durayd, Ibn al-Jawzī, Kunitzsch, Lane 等）頁碼改標 `（未核頁碼）`<br>2. 不可建議刪除開場句中之「人」字 |
| 17 | `A-19_審稿-天文_antigravity.md` | ✓ | ✓ | `521cb47db25d09fbaf0e920875e8fce943af32bbd9ccbe461431ea386f2b17df` | 修改第 13 行老人星升落批評：含大氣折射之真值為 18:11 升、21:44 中天、01:17 落，逐字稿 18:10/01:17 正確，改為 `⚪可選` 建議附註折射 |
| 18 | `A-19_審稿-文化_antigravity.md` | ✓ | ✓ | `67d4cc63c978893b193e68426f0c4a967f767bced59175f6441035ffc145b248` | 外部阿拉伯文獻（Kunitzsch 1961, Smart 2006）頁碼改標 `（未核頁碼）` |
| 19 | `A-19_審稿-敘事_antigravity.md` | ✓ | ✓ | `77bdd969e1ecea0734c72b7343a916712c18f3d58b1dbba3c070d801507d81a1` | 不可建議刪除開場句之「人」字；建議將固定句移為第一句 |
| 20 | `A-19_審稿-語言_antigravity.md` | ✓ | ✓ | `c2cda88978e02def5bd406cf730efbd5e52ad095ae5e038d5be810a40bea0e8e` | 外部文獻改標 `（未核頁碼）` |

> **⚠️ 注意**：一旦 Worker 在工作樹完成上述 20 份檔案的修改，其 SHA-256 將會變動。Worker 必須在交付前將這 20 份檔案同步複製至 `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/`，並重新執行 SHA-256 比對確認 100% 一致。

---

## 四、`07_資料來源/` 本地參考文獻與真實頁碼目錄結構

經完整清查本地 `07_資料來源/`：

### 1. 納瓦荷專題目錄（注意目錄拼寫為 `Navojo`）
- **實體目錄**：`07_資料來源/Navojo in America/`
- **原書檔案**：
  - `Star Trails Navajo (Don Childrey) (z-library.sk, 1lib.sk, z-lib.sk).pdf`（4,901,021 位元組）
- **合法可引真實頁碼**：
  - pp. 18, 29–39, 42–73, 99–103。
  - **特別勘誤備註**：p. 54 原書將夏季與冬季（Hai / Shį́）寫反，可在考據中點出。
- **外部專書標註規定**：
  - 舉凡 Haile (1947)、Griffin-Pierce (1992)、Kluckhohn & Leighton (1946)、Young & Morgan (1987)、Jayne (1906)、Newcomb (1940)、Witherspoon (1977)、Matthews (1897)、Chamberlain (1989)、Schaafsma (1992)、IEI (2010) 等，本地目錄均**無原書內頁**，一律**禁止編造頁碼**，出處欄統一標註「**（未核頁碼）**」。

---

### 2. 黑腳族專題目錄
- **實體目錄**：`07_資料來源/Blackfoot in America/`
- **原書文字檔案**：
  - `Mythology of the Blackfoot Indians.txt`（Wissler & Duvall 1908，538,401 位元組）
    - 合法可引真實頁碼：pp. 5–7, 40–44, 58–65, 68–72。
    - **關鍵出處**：Four-Tail Lodge 帳篷彩繪真實頁碼在 **p. 42**（逐字稿待查核清單寫 pp. 40–41 漏了 p. 42）。
  - `The old north trail, or, Life, legends and religion of the Blackfeet Indians.txt`（McClintock 1910，943,101 位元組）
    - 合法可引真實頁碼：pp. 26–35, 217–218, 488–501, 521–524。
- **外部專書標註規定**：
  - Frantz & Russell (2017)、Frantz (2009)、Wissler (1911/1912) 等外部著作，一律移除猜測頁碼，標註「**（未核頁碼）**」。

---

### 3. 古埃及與阿拉伯專題目錄
- **實體目錄**：
  - `07_資料來源/Egyptian in Middle East/`（僅有 `egyptian_star_chart.rtf`）
  - `07_資料來源/Arabic Ancient/`（僅有 `arabic_ancient_star_chart.rtf`）
  - `07_資料來源/Arabic Arabian Peninsula/`（僅有 `arabic_arabian_peninsula_star_chart.rtf`）
- **原書狀況**：
  - 本地**完全沒有**古埃及與古阿拉伯的歷史專著或論文原書（如 Censorinus, Parker, Neugebauer, Hurst, Ball, Petrie, Buchwald & Josefowicz, Sethe, Allen, Otto；Ibn Qutayba, al-Ṣūfī, Ibn Durayd, Ibn Manẓūr, Ibn al-Jawzī, Ibn Ḥibbān, Kunitzsch, Smart, Lane 等）。
- **外部專書標註規定**：
  - **所有引用這類專書之處，一律強制移除推測頁碼數字，一律標註「（未核頁碼）」**！

---

## 五、Worker 交付與驗收自動化標準流程（Runbook）

在 Worker 完成四集修改後，請依序執行以下 4 步驗收指令，確保 100% 通過：

```bash
# 步驟 1：複製 A-16 初稿逐字稿至工作樹（若尚未複製）
cp -p "/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md" "04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md"

# 步驟 2：同步 20 份審稿檔案至 Downloads 鏡像
cp -p 04_腳本庫/_審稿/A-1[6789]_*.md "/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/"

# 步驟 3：執行天體力學物理數據檢驗（Skyfield 1.54）
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 02_製作流程SOP/verification_harness/verify_batch2_ephemeris.py

# 步驟 4：執行第 2 批 R2 專項防呆與雙區同步整合驗證
python3 .agents/teamwork/explorer_crosscut_sync/verify_batch2_r2_rules.py
```
只有在上述 4 項指令皆回傳 Exit Code 0 時，第 2 批交付才符合結案標準。
