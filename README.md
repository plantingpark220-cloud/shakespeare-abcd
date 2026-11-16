# Bard's Lexicon · 莎士比亞詞彙 A–Z

純靜態網站（HTML/CSS/JS），不需建置。每個字母一個文學詞彙 + 劇中金句 + 中文釋義 + 印象派風格配圖 + 單字/金句發音。

## 檔案結構
- `index.html` 網站本體　`data.js` 26 筆內容資料（要改詞彙/句子改這裡）
- `images/` 26 張 jpg（`a_argosy.jpg` …）　`gen_images.py` 重新產生圖片
- `audio/` mp3（命名 `a_argosy_word.mp3` / `a_argosy_quote.mp3`）　`gen_audio.py` 產生音檔

## 步驟
1. `pip install edge-tts` → `python gen_audio.py`（產生 52 個 mp3，約 1–2 分鐘）
2. 推上 GitHub → Settings → Pages → Branch: main / root
3. 本機預覽：`python -m http.server` 後開 http://localhost:8000

沒有 `audio/` 時，按鈕會自動改用瀏覽器內建語音朗讀。
