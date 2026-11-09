# 卡 07｜Canva 英文版（換字、換概念圖、移頁）

- 模型：**Sonnet 5.5／effort medium**（EN01 實測：24 頁縮圖都要看、要判斷窄框，low 不夠）　預估：半到 1 個對話
- 前提：EN v1（或先用 v0）＋每頁文字表；英文概念圖已 push；你已複製好設計

## 你先做
- [ ] 該集**中文 Canva 已做完、手工收尾也做完**（副本不會同步；中文版沒做完就複製的副本只有上一集或韓國集的內容，要刪掉重複製）
- [ ] 學校帳號：打開**同一集**的中文設計 → Make a copy → 名字＝中文原名前加 `EN{nn} `（例 `EN01 A-11 阿努塔`）→ 放「萬國星空 EN」資料夾 → 分享給 kimjoo2104（可編輯）
- [ ] 看剩餘用量夠不夠做完一個 transaction

## 貼給 Claude（整段複製；保留一種存檔方式）

```text
【卡 07 Canva 英文】
英文集號：　　　　Canva 設計名：　　　
存檔方式：直接存檔（縮圖檢查過就 commit transaction，不用等我）／先預覽（等我說「存檔」）

這個對話只做一件事：把英文稿放進上面那個 Canva 副本。先讀：
1. 02_製作流程SOP/開工指令/README.md 第三節「共同規則」
2. 02_製作流程SOP/英文版製作流程.md 第二節 4–5；02_製作流程SOP/Canva逐頁文字放置規格.md 第四節（字級與 EN01 實際座標）；01_視覺與品牌/字幕字卡版型.md 第四節（英文封面）
3. 04_腳本庫/_英文版/EN{nn}-…-v1.md（沒有 v1 就用 v0）的 Page sequence 表；05_素材/{集}_…/_英文版/EN{nn}_Canva逐頁文字.csv
4. 05_素材/{集}_…/_v4大畫布/{EP}_Canva媒體ID.json；EN01 的做法見 04_腳本庫/_英文版/EN01-A-11-Anuta-v1.md 表頭的 Canva 列

要做：
- read-design 開 transaction（大型輸出會存成檔案，用 python 解析）；對照 Page sequence 表決定每頁去留
- 英文概念圖 upload-asset-from-url（commit SHA 的 raw 連結）→ 該頁 update_fill＋crop_media 0/0/1032/1032
- 封面照版型第四節，文字＝英文節目表該列的「英文標題」＋「英文鉤子」；內容頁 add_text＋format_text（字卡 72 px 粗體、字幕 44 px、窄框 38–40 px，座標照放置規格第四節）；中譯標籤 replace_text 成英文（＋resize_element、position_element 對回星點）；「下集見」＝英文節目表**下一列**（EN{nn+1}）的英文標題＋鉤子，追蹤我們改英文，參考文獻保留——這三頁不用問，直接改，改了什麼寫進回報；每頁備註改英文（EN{nn} p{原頁號} 頁名 — 到下一頁幾秒 — 這頁的文字）
- 不用的頁全部 reorder_page 到最後一張保留頁之後；再用 design_content 讀回頁序（presenter_notes 在 transaction 裡可能是舊的，不能拿來比）
- 每頁縮圖看一次：字沒出框、沒壓到標籤與主角星；會壓到就改窄框或移位置，不改字
- 媒體ID.json 加 en 區塊（design_id、design_title、commit、concept 的媒體 ID）；英文稿 Page sequence 表加 Now 欄（移頁後的頁號）並重跑 gen_en_pages.py
- 英文節目表「英文 Canva」欄改「完成（待人工收尾）」

結束：存檔照上面；repo commit、PR、合併。回報：哪幾頁用了窄框、哪些頁的 Pos 跟稿不同（我會回填稿子）、我要做的收尾（刪第 N 頁以後、每頁秒數、哪裡硬切、音樂、美編）。
```

## 做完之後（你）
- 格狀檢視刪掉最後面不用的頁；每頁秒數照 Page sequence 表；換組頁轉場「無」；配樂（YouTube 音樂庫或 CC0）。
- 圖傳同學依 `01_視覺與品牌/字幕字卡版型.md` 版型 EN-A／B／C 做字的美編、品牌字全部變更。
- 發布後用卡 08 填四平台日期。
