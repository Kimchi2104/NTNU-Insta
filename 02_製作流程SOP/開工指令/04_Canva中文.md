# 卡 04｜Canva 中文版排頁

- 模型：**Sonnet 5.5／effort medium**（純照表的頁 low 也行）　預估：**一個對話一口氣做完整集**（A-16 五十多頁：Sonnet 1M 視窗做到第 27 頁用掉 54 萬 token，上下文滿了會自動壓縮接著做，不拆對話、不分段開 PR）
- 前提：素材已 push；你已在學校帳號複製好設計並分享

## 你先做
- [ ] 學校帳號：上一集中文設計 → Make a copy → 改名「{集} {集名}」（例 `A-16 納瓦荷`）→ 分享給 kimjoo2104（可編輯）
- [ ] 不用為了頁數刪頁：現有頁數＋要新增的頁數由 Claude 自己算，相加到 100 以上會自動走「工作稿模式」（見下面「100 頁上限」）
- [ ] 看剩餘用量夠不夠做完一個 transaction

## 貼給 Claude（整段複製；保留一種存檔方式）

```text
【卡 04 Canva 中文】
集號：　　　　Canva 設計名：　　　（補頁時在這行後面加「模式：補頁」）
存檔方式：直接存檔（縮圖檢查過就 commit transaction，不用等我）／先預覽（等我說「存檔」）

如果上面寫了「模式：補頁」：這份設計已經排完，只是逐字稿加回了內容。不要重排整集、不要移走既有頁。只讀 05_素材/{集}_…/_v4大畫布/{EP}_補頁清單.md 與新的逐頁製作表，照清單新增頁（add_page 後 reorder 到指定位置）、放素材與字、改清單列出的既有頁文字與備註；做完用 design_content 讀回頁序比對，縮圖看新頁與前後兩頁接得上。媒體ID.json 補新素材的 ID；節目表「狀態」欄拿掉【Canva 待補頁】，寫「Canva 完成（v2 補頁，待手工收尾）」。下面「要做」的清單只取用得到的部分（上傳素材、ops 順序、連接器脾氣、存檔）。回報列出新增的頁號，讓我只對那幾頁做手工收尾。

這個對話只做一件事：把上面那一集排進那個 Canva 設計。先讀：
1. 02_製作流程SOP/開工指令/README.md 第三節「共同規則」
2. 02_製作流程SOP/每集製作SOP.md 第二、三、五節
3. 05_素材/{集}_…/_v4大畫布/ 的逐頁製作表、Canva頁面參數.json、鏡頭清單；跑 /usr/bin/python3 02_製作流程SOP/canva_ops.py {EP} --list
4. 上一集的 {EP}_Canva媒體ID.json（格式）；02_製作流程SOP/Canva逐頁文字放置規格.md（字卡、字幕怎麼放）

要做：
- read-design 開 transaction，讀 page_metadata＋presenter_notes；範本頁全部保留（封面、下集見、追蹤我們，以及片尾的參考文獻／製作團隊／鳴謝；封面與下集見照下一條改），只有上一集留下來的內容頁才集中移到最後。成品頁序＝封面 → 本集內容頁 → 下集見 → 追蹤我們 → 片尾
- **100 頁上限（先算再動手）**：連接器打不開「存檔後 ≥ 100 頁」的設計。A-23 就是 32 頁的設計加了 104 頁新頁、commit 之後再也開不了 transaction。開工先算：現有頁數（search-designs 的 page_count）＋要新增的頁數（逐頁製作表的資料列數）。
  - 相加 ≤ 99 → 直接在原設計 add_page，照下面做。
  - 相加 ≥ 100 → **工作稿模式**，原設計在最後一步之前不加任何頁：① 原設計只開一次 transaction，把封面、下集見改好就 commit；② copy-design（原設計，page_numbers＝[1]）做出工作稿，新頁全部 add_page 在工作稿裡。每份工作稿連底頁最多 95 頁，新頁超過 94 就再做第二份。工作稿永遠在 99 頁以內，可以照常分次 commit；③ 全部排完、format_text 完、縮圖檢查完，才用 merge-designs（type＝modify_existing_design，design_id＝原設計）insert_pages：source 是工作稿、page_numbers 不含底頁，after_page_number＝封面那一頁，兩份工作稿依序接上；④ 併完用 search-designs 看原設計頁數對不對。併完之後原設計超過 99 頁、不能再開 transaction，所以所有編輯都要在併之前做完。
  - merge-designs 併不進原設計 → 改用 create_new_design 組一份「{設計名}（合併）」（封面 → 新頁 → 下集見、追蹤我們 → 片尾），回報設計 ID，請 Kim 在學校帳號另存。
  - 工作稿的 design_id 寫進 媒體ID.json 的 work_designs，不要刪，回報請 Kim 確認成品後自己刪。merge-designs 的 delete_pages 不要用，除非 Kim 在這個對話裡明寫要刪哪幾頁
- 封面與「下集見」不用問，直接改：開場字卡（封面）＝本集統一開頭句（逐字稿第一鏡「同一片星空，…」）＋全年節目表該列的「標題（工作名）」；「下集見」＝全年節目表**發布日的下一列**的標題＋鉤子（例 A-16 的下集見寫 A-17「黑腳族：留在天上的六個孩子」），北天星盤三層照 每集製作SOP 第二節 5 最後一條；追蹤我們、參考文獻原樣保留。改了什麼寫進回報就好
- 素材 upload-asset-from-url：commit SHA 的 raw 連結（中文路徑要 percent-encode），媒體 ID 寫進 05_素材/{集}_…/_v4大畫布/{EP}_Canva媒體ID.json
- 每頁 ops 照 canva_ops.py：背景 → 天空層 → 山 → 標籤 → 概念圖框 → 概念圖 → 備註；字卡與字幕照放置規格用 add_text＋format_text 放素字（位置照版型 A／B，不做美編）
- 連接器脾氣：山 insert_fill 後 crop_media 回 0/0/1939.08×300.56；update_fill 後 crop_media 寬高都給；add_text 後用回傳的 locator 送 format_text
- 一口氣做完整張卡（README 第三節規則 9）：中途不停下來回報、不分段開 PR、不把對話名改成「待續」。Canva transaction 每 15–20 頁 commit 一次保住進度就好（存檔後總頁數要 ≤ 99；會超過就是工作稿模式，原設計不加頁）；git 可以隨時 commit、push 到工作分支，PR 只在全部做完時開一次。只有工具真的回傳用量上限才停：commit、push 做到哪，回報做到第幾頁，等 Kim 在同一個對話說「繼續」
- reorder 完用 design_content 讀回頁序比對（presenter_notes 在 transaction 裡可能是舊的）
- 縮圖檢查：換組前後兩頁一模一樣、概念圖不疊字、每頁都有山且位置一致
- 節目表「狀態」欄加「＋Canva 完成（待手工收尾）」

結束：Canva 照上面的存檔方式；repo commit（媒體ID.json）、PR、合併。回報列出我要做的手工收尾：字型全部變更、山顏色、每頁轉場（換組頁＝無）、刪最後面的舊頁、改舊頁名；還有下一步（卡 05 或 07）。
```

## 做完之後（你）
- 手工收尾照 `每集製作SOP.md` 第六節（約 5 分鐘）。
- 下一步：英文稿還沒寫 → 卡 05；已有 EN v0／v1 → 複製同一集設計，開卡 07。
