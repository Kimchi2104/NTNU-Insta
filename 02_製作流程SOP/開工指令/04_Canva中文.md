# 卡 04｜Canva 中文版排頁

- 模型：**Sonnet 5.5／effort medium**（純照表的頁 low 也行）　預估：40 頁以內 1 個對話；超過就拆前半、後半兩個
- 前提：素材已 push；你已在學校帳號複製好設計並分享

## 你先做
- [ ] 學校帳號：上一集中文設計 → Make a copy → 改名「{集} {集名}」（例 `A-16 納瓦荷`）→ 分享給 kimjoo2104（可編輯）
- [ ] 複製來的設計如果已經 80 多頁，先刪掉上一集不會再用的頁（連接器一份設計最多 100 頁）
- [ ] 看剩餘用量夠不夠做完一個 transaction

## 貼給 Claude（整段複製；保留一種存檔方式）

```text
【卡 04 Canva 中文】
集號：　　　　Canva 設計名：　　　
存檔方式：直接存檔（縮圖檢查過就 commit transaction，不用等我）／先預覽（等我說「存檔」）

這個對話只做一件事：把上面那一集排進那個 Canva 設計。先讀：
1. 02_製作流程SOP/開工指令/README.md 第三節「共同規則」
2. 02_製作流程SOP/每集製作SOP.md 第二、三、五節
3. 05_素材/{集}_…/_v4大畫布/ 的逐頁製作表、Canva頁面參數.json、鏡頭清單；跑 /usr/bin/python3 02_製作流程SOP/canva_ops.py {EP} --list
4. 上一集的 {EP}_Canva媒體ID.json（格式）；02_製作流程SOP/Canva逐頁文字放置規格.md（字卡、字幕怎麼放）

要做：
- read-design 開 transaction，讀 page_metadata＋presenter_notes；保留「下集見」「追蹤我們」「參考文獻」，其餘舊頁最後集中移到最後
- 素材 upload-asset-from-url：commit SHA 的 raw 連結（中文路徑要 percent-encode），媒體 ID 寫進 05_素材/{集}_…/_v4大畫布/{EP}_Canva媒體ID.json
- 每頁 ops 照 canva_ops.py：背景 → 天空層 → 山 → 標籤 → 概念圖框 → 概念圖 → 備註；字卡與字幕照放置規格用 add_text＋format_text 放素字（位置照版型 A／B，不做美編）
- 連接器脾氣：山 insert_fill 後 crop_media 回 0/0/1939.08×300.56；update_fill 後 crop_media 寬高都給；add_text 後用回傳的 locator 送 format_text
- 用量不夠做完就先做到一個鏡頭結束處 commit transaction，回報做到第幾頁，下一個對話接著做
- reorder 完用 design_content 讀回頁序比對（presenter_notes 在 transaction 裡可能是舊的）
- 縮圖檢查：換組前後兩頁一模一樣、概念圖不疊字、每頁都有山且位置一致
- 節目表「狀態」欄加「＋Canva 完成（待手工收尾）」

結束：Canva 照上面的存檔方式；repo commit（媒體ID.json）、PR、合併。回報列出我要做的手工收尾：字型全部變更、山顏色、每頁轉場（換組頁＝無）、刪最後面的舊頁、改舊頁名；還有下一步（卡 05 或 07）。
```

## 做完之後（你）
- 手工收尾照 `每集製作SOP.md` 第六節（約 5 分鐘）。
- 下一步：英文稿還沒寫 → 卡 05；已有 EN v0／v1 → 複製同一集設計，開卡 07。
