# 音声メモワークフロー セットアップ手順

**対象**: ワークフロー #1「音声入力 → 文字起こし → Drive保存 → Telegram返信」

---

## Step 1: GAS (CRUX_Inbox_API) をデプロイ

1. https://script.google.com → 「新しいプロジェクト」
2. プロジェクト名: `CRUX_Inbox_API`（XOP_Wiki_API とは別プロジェクト）
3. `gas_inbox_api.js` の内容を貼り付け（既存の `myFunction()` を削除）
4. **動作確認**
   - `testDoPost` を実行 → `{"success":true,"path":"2026-..."}` が出ること
   - `testDoGet` を実行 → `{"success":true,"date":"...","files":[...]}` が出ること
5. 「デプロイ」→「新しいデプロイ」→ 種類: **ウェブアプリ**
   - 実行するユーザー: **自分（miyawaki.toshio@gmail.com）**
   - アクセスできるユーザー: **全員**
6. 発行された URL をメモ → `GAS_INBOX_ENDPOINT`

---

## Step 2: n8n ワークフローをインポート

1. n8n「Workflows」→「Import from File」
2. `n8n_voice_memo_workflow.json` を選択
3. 以下の `FILL_ME` を置き換える

| ノード | 項目 | 値 |
|--------|------|----|
| 📨 Telegram受信 | credentials.id | XopGp_bot の Telegram クレデンシャル ID |
| 🔗 getFile (Telegram) | credentials.id | 同上 |
| ⬇️ 音声ダウンロード | credentials.id | 同上 |
| 📤 Telegram返信 | credentials.id | 同上 |
| 🤖 Gemini 文字起こし+整形 | credentials.id | Gemini API Key クレデンシャル ID |
| 💾 Drive保存 (GAS) | url | Step1 の GAS_INBOX_ENDPOINT |

4. 保存 → 「Activate」

---

## Step 3: 動作確認

XopGp_bot に音声メモを送信する。

**期待する結果:**
```
✅ 音声メモを保存しました
📄 2026-05-24/yoshioka_1430.md

整形内容:
## 2026-05-24 業務メモ（yoshioka）

- 午前: 顧客 A 社（湯澤様）訪問、XOP の提案実施
- 午後: 見積書作成、金額 120万円で確認
```

**Drive で確認:**
- Google Drive → 業務メモ → INBOX → YYYY-MM-DD → `{username}_{HHMM}.md` が作成されていること

---

## ノード構成（フロー図）

```
📨 Telegram受信
  ↓
🎤 音声のみ通過（voice フィルタ）
  ↓
📝 変数抽出（chatId / username / fileId）
  ↓
🔗 getFile (Telegram API)
  ↓
⬇️ 音声ダウンロード（OGG バイナリ）
  ↓
🔧 音声データ準備（base64 変換）
  ↓
🤖 Gemini 文字起こし+整形（gemini-2.5-flash）
  ↓
🔤 テキスト整形+正規化（Layer1 正規化）
  ↓
💾 Drive保存 (GAS doPost)
  ↓
📋 返信テキスト生成
  ↓
📤 Telegram返信
```

---

## トラブルシューティング

| 症状 | 原因 | 対処 |
|------|------|------|
| `音声バイナリが見つかりません` | ダウンロードノードの responseFormat | `response.responseFormat: "file"` を確認 |
| GAS 保存エラー `invalid username format` | username に日本語が含まれる | Telegram username（英数字）が設定されているか確認 |
| Gemini タイムアウト | 音声が長すぎる | 60秒以内を推奨。長い場合は `timeout: 90000` を増やす |
| GAS `success: false` | INBOX フォルダ ID 誤り | `gas_inbox_api.js` の `INBOX_FOLDER_ID` を確認 |
| Drive に保存されるが文字化け | UTF-8 | GAS は `MimeType.PLAIN_TEXT` で保存（自動 UTF-8）|

---

## Drive フォルダ ID（参考）

| パス | ID |
|------|-----|
| 業務メモ/ | `1m3Pc21a8dGwuB2faWLO4qoaPzW6Mgc6-` |
| INBOX/ | `174PXmcgyIvVJaeZnbCk9O_F9NfG3a5l7` |
| XOP_Wiki/辞書/ | `1BWQiPSAIHtYxpLG4fPZjXes6x1r0MYhR` |
