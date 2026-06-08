# XOP Q&A Bot セットアップガイド

## アーキテクチャ

```
[Telegram XopGp_bot]
  ↓ 質問メッセージ
[n8n Webhook Trigger]
  ↓
[GAS エンドポイント]  ← XOP_Wiki フォルダの.mdファイルを全取得
  ↓ 全Wikiコンテンツ
[Claude API]  ← Wikiをコンテキストに回答生成
  ↓ 回答テキスト
[Telegram 返信]
```

**なぜGASを経由するか？**
- n8n から Google Drive に直接 OAuth でアクセスするのは設定が複雑
- GAS なら Drive ファイルを1回のHTTP GETで全取得できる
- Wikiが更新されても n8n 側の変更は不要

---

## Step 1: Google Apps Script のデプロイ

### 1-1. 新しいGASプロジェクトを作成
1. https://script.google.com にアクセス
2. 「新しいプロジェクト」をクリック
3. プロジェクト名: `XOP_Wiki_API`

### 1-2. コードを貼り付け
`gas_wiki_api.js` の中身を GAS エディタに貼り付ける（既存の `function myFunction(){}` は削除）

### 1-3. 動作確認
1. `testWikiApi` 関数を選択して「実行」
2. コンソールに取得ファイル一覧が表示されることを確認

### 1-4. Web App としてデプロイ
1. 右上「デプロイ」→「新しいデプロイ」
2. 種類: **ウェブアプリ**
3. 実行するユーザー: **自分 (miyawaki.toshio@gmail.com)**
4. アクセスできるユーザー: **全員**
5. 「デプロイ」をクリック
6. 表示されたURLをメモ → `GAS_ENDPOINT_URL`
   ```
   https://script.google.com/macros/s/AKfycbx1JGu8Qdtinn2ISQGegBLP95E1R48S4_eMEnytR_kxDT-xwCLFkoCqXPvFHfCiwfC5Ug/exec
   ```

### 1-5. 動作テスト
```bash
curl "https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'取得ファイル数: {data[\"fileCount\"]}')
print('ファイル一覧:')
for f in data['fileList']:
    print(f'  - {f}')
"
```

---

## Step 2: n8n のクレデンシャル設定

### 2-1. Telegram Bot クレデンシャル
すでに設定済みの `XopGp_bot` クレデンシャルのIDを確認する

### 2-2. Anthropic API Key クレデンシャル
1. n8n の「Settings」→「Credentials」→「Add Credential」
2. タイプ: **Header Auth**
3. 名前: `Anthropic API Key`
4. Name: `x-api-key`
5. Value: `sk-ant-...` (Anthropic APIキー)
6. 保存してIDをメモ → `ANTHROPIC_CRED_ID`

> APIキーは Google Drive の `.env` ファイル (ID: `1yB1HyhRCOfiQG0H1KNeLo1BcGkpXKsLc`) に保存済み

---

## Step 3: n8n ワークフローのインポート

### 3-1. JSONをインポート
1. n8n の「Workflows」→「Import from File」
2. `n8n_xop_qa_bot.json` を選択

### 3-2. `FILL_ME` を置き換える

| ノード | 修正箇所 | 置き換え内容 |
|--------|---------|------------|
| 📨 Telegram受信 | credentials.id | Telegram クレデンシャルID |
| 📚 Wiki全文取得 | url | Step1でメモした `GAS_ENDPOINT_URL` |
| 🤖 Claude API呼び出し | credentials.id | `ANTHROPIC_CRED_ID` |
| 📤 Telegram送信 | credentials.id | Telegram クレデンシャルID |
| ⚠️ エラー通知 | credentials.id | Telegram クレデンシャルID |

### 3-3. テスト実行
1. ワークフローを保存
2. 「Test Workflow」をクリック
3. Telegram から `XopGp_bot` に質問を送る
4. 動作確認

---

## 動作確認のテスト質問

```
XOPとウォーターセラミックの違いは？
施工単価はいくら？
海外展開で最優先の市場はどこですか？
代理店になるのに初期費用はいくら？
六本木ヒルズでの実績を教えて
ビルオーナーへの営業フローを教えて
```

---

## Wiki更新時の運用

1. XOP_Wiki フォルダの .md ファイルを更新/追加
2. n8n ワークフローの変更は**不要**（GASが毎回最新を取得するため）
3. GAS 自体の変更が必要な場合のみ再デプロイ

---

## トラブルシューティング

| 症状 | 原因 | 対処 |
|------|------|------|
| Wikiが取得できない | GASデプロイ設定誤り | 「実行するユーザー: 自分」を確認 |
| Claude APIエラー | APIキー誤り/上限 | クレデンシャルを確認 |
| Telegramに返信なし | bot設定 | bot tokenとwebhookを確認 |
| 文字化け | エンコーディング | GASの `getDataAsString('UTF-8')` を確認 |

---

## ファイル一覧

```
XOP_QA_Bot/
├── SETUP.md                    ← このファイル
├── gas_wiki_api.js             ← GASに貼り付けるコード
├── normalize.js                ← n8n 正規化ノード（音声入力対応）
├── CLAUDE_XOP.md               ← Claude行動規範（XOPプロジェクト用）
├── n8n_xop_qa_bot.json         ← v1: Wiki のみ
├── n8n_xop_qa_bot_v2.json      ← v2: Wiki + NocoDB Deals/Tasks
└── n8n_xop_qa_bot_v3.json      ← v3: Wiki + NocoDB + 正規化 ★推奨
```

Google Drive:
- XOP_Wiki/辞書/XOP_用語辞書.md  ← 顧客名・会社名・製品名辞書

## v2 追加クレデンシャル（NocoDB）

### NocoDB API Token の取得
1. https://app.nocodb.com にログイン
2. 右上アバター → 「Team & Settings」
3. 「API Tokens」→「Add New Token」
4. 名前: `n8n_xop_bot`、作成してトークンをコピー

### n8n に登録
1. n8n「Credentials」→「Add」→ **Header Auth**
2. 名前: `NocoDB API Token`
3. Name: `xc-token`
4. Value: `<コピーしたトークン>`

## v2 の FILL_ME 箇所

| ノード | 修正箇所 | 内容 |
|--------|---------|------|
| 📨 Telegram受信 | credentials.id | Telegram cred ID |
| 📚 Wiki取得 (GAS) | url | GAS endpoint URL |
| 💼 Deals取得 | credentials.id | NocoDB cred ID |
| ✅ Tasks取得 | credentials.id | NocoDB cred ID |
| 🤖 Claude API | credentials.id | Anthropic cred ID |
| 📤 Telegram返信 | credentials.id | Telegram cred ID |

## 参照

- XOP_Wiki フォルダID: `1mzZnlFGEwy8fGceH3lA2t-RsXa2ZYRp3`
- .env ファイル ID: `1yB1HyhRCOfiQG0H1KNeLo1BcGkpXKsLc`
- Claude API: https://console.anthropic.com
