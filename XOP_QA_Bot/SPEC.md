# XOP Q&A Bot — システム仕様書

**バージョン**: 1.0  
**作成日**: 2026-05-19  
**対象プロジェクト**: プロテケアXOP / 株式会社クラックス

---

## 目次

1. [システム概要](#1-システム概要)
2. [アーキテクチャ](#2-アーキテクチャ)
3. [コンポーネント詳細](#3-コンポーネント詳細)
4. [データソース](#4-データソース)
5. [音声入力対応](#5-音声入力対応)
6. [ファイル一覧](#6-ファイル一覧)
7. [セットアップ手順](#7-セットアップ手順)
8. [運用ガイド](#8-運用ガイド)
9. [トラブルシューティング](#9-トラブルシューティング)

---

## 1. システム概要

### 目的
Telegram グループ（XopGp_bot）に質問を送ると、XOP の社内知識・リアルタイム案件情報・タスク状況をもとに Claude が自動回答するシステム。テキスト入力・音声入力の両方に対応。

### 主な機能

| 機能 | 内容 |
|------|------|
| Q&A 自動回答 | Telegram → Claude API → Telegram |
| Wiki 参照 | Google Drive の .md ファイルをリアルタイム取得 |
| 案件情報参照 | NocoDB Deals テーブル（リアルタイム） |
| タスク情報参照 | NocoDB Tasks テーブル（リアルタイム） |
| 音声入力補正 | Whisper 誤認識を正規化してから処理 |

---

## 2. アーキテクチャ

### 全体フロー（v3）

```
[Telegram: XopGp_bot]
  ↓ テキスト or 音声入力（Whisper文字起こし済み）
[n8n: Webhook Trigger]
  ↓
[🔤 テキスト正規化]  ← Whisper誤認識パターンを修正
  ↓　　↓　　↓（3並列リクエスト）
  ↓　　↓　　↓
[GAS]  [NocoDB Deals]  [NocoDB Tasks]
 ↓（全Wikiコンテンツ）  ↓（未完了案件）   ↓（未完了タスク）
  └─────────────────┬──────────────────────┘
                    ↓
          [🧩 プロンプト構築]  ← 3つの情報源を結合
                    ↓
          [Claude API]  ← claude-3-5-haiku-20241022
                    ↓
          [✂️ 回答整形]
                    ↓
          [Telegram返信]
```

### 設計方針

- **GAS 経由の理由**: n8n から Google Drive への直接 OAuth は設定が複雑。GAS なら1回の HTTP GET で全 Wiki を取得できる。Wiki が更新されても n8n 側の変更は不要。
- **NocoDB 並列取得**: Wiki・Deals・Tasks を同時取得してレイテンシを最小化。
- **2層正規化**: Layer1（n8n 正規化ノード）で機械的に置換 → Layer2（Claude system prompt）で意味的に補完。

---

## 3. コンポーネント詳細

### 3-1. n8n ワークフロー（v3）

**ファイル**: `n8n_xop_qa_bot_v3.json`

| ノード | 種類 | 役割 |
|--------|------|------|
| 📨 Telegram受信 | TelegramTrigger | メッセージ受信 |
| 🔍 テキストのみ通過 | Filter | テキストメッセージのみ通過（コマンド除外） |
| 📝 変数抽出 | Set | question / chatId / username を抽出 |
| 🔤 テキスト正規化 | Code | Whisper誤認識パターンを正規化 |
| 📚 Wiki取得 (GAS) | HTTP Request | GAS エンドポイントから全Wikiを取得 |
| 💼 Deals取得 (NocoDB) | HTTP Request | アクティブ案件一覧取得 |
| ✅ Tasks取得 (NocoDB) | HTTP Request | 未完了タスク一覧取得 |
| 🧩 プロンプト構築 | Code | 3つの情報源を結合して system prompt 生成 |
| 🤖 Gemini API | HTTP Request | Google Gemini API 呼び出し（`gemini-2.5-flash`）|
| ✂️ 回答整形 | Code | 回答テキストに参照情報フッターを付与 |
| 📤 Telegram返信 | Telegram | 質問者のチャットに返信 |

**バージョン履歴**:
- v1: Wiki のみ（`n8n_xop_qa_bot.json`）
- v2: Wiki + NocoDB Deals/Tasks（`n8n_xop_qa_bot_v2.json`）
- v3: v2 + テキスト正規化ノード追加（`n8n_xop_qa_bot_v3.json`）★現在推奨

---

### 3-2. Google Apps Script（Wiki API）

**ファイル**: `gas_wiki_api.js`  
**GAS プロジェクト名**: `XOP_Wiki_API`

**動作**:
1. `XOP_Wiki` フォルダ（Drive ID: `1mzZnlFGEwy8fGceH3lA2t-RsXa2ZYRp3`）を再帰的にスキャン
2. `.md` ファイルをすべて読み込み、`index.md` を先頭に並び替え
3. 全ファイルを結合して JSON で返す

**レスポンス形式**:
```json
{
  "success": true,
  "fileCount": 14,
  "fileList": ["index.md", "事業戦略/事業概要.md", "..."],
  "content": "# 📄 index.md\n\n...\n\n---\n\n# 📄 事業戦略/事業概要.md\n\n..."
}
```

**デプロイ設定**:
- 実行するユーザー: **自分（miyawaki.toshio@gmail.com）**
- アクセスできるユーザー: **全員**

---

### 3-3. 正規化コード（normalize.js）

**ファイル**: `normalize.js`（n8n Code ノードに貼り付け）

対応する誤認識パターン:

| カテゴリ | 誤認識 → 正式表記 |
|---------|-----------------|
| 製品名 | ゾップ/ゾッポ → XOP |
| 製品名 | プロテカ/プロテア → プロテケア |
| 製品名 | 水セラミック → ウォーターセラミック |
| 会社名 | クラック/クラクス → クラックス |
| 人名 | 湯沢 → 湯澤 |
| 人名 | 稲沢 → 稲澤 |
| 人名 | 中沢 → 中澤 |
| 人名 | 笹木 → 佐々木 |
| 会社名 | パナホーム → Panaホームリフォーム |
| 会社名 | アルティス → Artis |

---

### 3-4. Claude 行動規範（CLAUDE_XOP.md）

**ファイル**: `CLAUDE_XOP.md`

Claude の応答ルール:
- **情報源の優先順位**: Wiki > NocoDB Deals > NocoDB Tasks > 用語辞書
- **数字は正確に引用**（価格・スペック・日付）
- **情報なし**: 「記録にありません。詳細は宮脇さんへご確認ください」
- **推測禁止**: 情報源にないことは答えない
- **回答は最大500文字、箇条書き**
- **社外秘データも回答可**（社内文書のため）
- **日報フォーマット対応**: 「日報」「活動報告」キーワードで専用フォーマット出力

---

## 4. データソース

### 4-1. XOP_Wiki（Google Drive）

**フォルダ ID**: `1mzZnlFGEwy8fGceH3lA2t-RsXa2ZYRp3`

```
XOP_Wiki/
├── index.md                              ← 全体目次
├── 事業戦略/
│   ├── 事業概要.md
│   ├── ビジネスモデル.md
│   ├── 収益予測.md
│   └── 実行スケジュール.md
├── 製品/
│   └── XOP概要.md
├── 競合比較/
│   ├── XOP_vs_ウォーターセラミック.md
│   └── 競合分析レポート.md
├── 営業フロー/
│   ├── Aトラック_ビルオーナー.md
│   └── Bトラック_代理店認定フロー.md
├── 海外戦略/
│   └── 海外展開戦略.md
├── ターゲット顧客/
│   └── ターゲット顧客ペルソナ.md
├── 顧客情報/
│   └── 顧客・案件管理概要.md
└── 辞書/
    └── XOP_用語辞書.md                   ← 顧客名・会社名・製品名辞書
```

**更新方法**: ファイルを Google Drive で直接編集するだけで OK（n8n・GAS の変更不要）

---

### 4-2. NocoDB（リアルタイムデータ）

**ベース URL**: `https://app.nocodb.com`

| テーブル | ID | 用途 | フィルター |
|---------|-----|------|-----------|
| Deals | `m4dt4qlrw9ag6k0` | 案件パイプライン | ステータス ≠ 完了 |
| Tasks | `m83uxghrdtij7gc` | タスク管理 | ステータス ≠ Done |

**認証**: Header Auth（`xc-token`）→ n8n クレデンシャル `NocoDB API Token`

---

### 4-3. XOP 用語辞書

**Drive パス**: `XOP_Wiki/辞書/XOP_用語辞書.md`  
**Drive ID**: `1nTaON6xnnWHvzrbFPmtPk6wgZKrQAK27`

収録データ:
- 製品・技術用語（XOP, プロテケア 等）
- 顧客名（50名）と読み仮名
- 会社名（47社）と読み仮名・略称
- 音声補正方法（n8n Layer1 / Claude Layer2）

---

## 5. 音声入力対応

### 2層正規化アーキテクチャ

```
音声 → Whisper文字起こし
  ↓
Layer 1: n8n 正規化ノード（機械的置換・高速）
  ↓
Layer 2: Claude system prompt（意味的補完・柔軟）
  ↓
最終的な正確な回答
```

**Layer 1（n8n）**: 確実にわかっている誤認識パターンを `String.replace()` で機械的に修正。誤検知リスクが低いものだけを登録。

**Layer 2（Claude）**: system prompt に「ゾップ→XOP」等の補正ヒントを含め、Layer1 で拾えなかった揺らぎをモデルが文脈から解釈。

### 日報入力での活用

音声日報フロー（別ワークフロー）でも同じ正規化辞書が有効:
```
音声メモ → Whisper → normalize.js → Claude日報整形 → Wiki保存・NocoDB更新 → Telegram通知
```

---

## 6. ファイル一覧

### ローカル（`/Users/gon/Documents/AIMemory/crux/XOP_QA_Bot/`）

| ファイル | 内容 |
|---------|------|
| `SPEC.md` | このファイル（システム仕様書）|
| `SETUP.md` | セットアップ手順書 |
| `gas_wiki_api.js` | GAS ウェブアプリ コード |
| `normalize.js` | n8n 正規化ノード コード |
| `CLAUDE_XOP.md` | Claude 行動規範 |
| `n8n_xop_qa_bot.json` | n8n ワークフロー v1（Wiki のみ）|
| `n8n_xop_qa_bot_v2.json` | n8n ワークフロー v2（Wiki + NocoDB）|
| `n8n_xop_qa_bot_v3.json` | n8n ワークフロー v3（+ 正規化）★推奨 |

### Google Drive（`XOP_Wiki/`）

| パス | Drive ID |
|------|---------|
| XOP_Wiki/ (フォルダ) | `1mzZnlFGEwy8fGceH3lA2t-RsXa2ZYRp3` |
| 辞書/ (フォルダ) | `1BWQiPSAIHtYxpLG4fPZjXes6x1r0MYhR` |
| 辞書/XOP_用語辞書.md | `1nTaON6xnnWHvzrbFPmtPk6wgZKrQAK27` |
| index.md | `1MvhBa9W6QITi0BhdCBjNzdhetBY0ifGC` |
| 顧客情報/顧客・案件管理概要.md | `1O6QcxgeaXpX2lr6iT7xJ1TRyIMwrdtUu` |
| .env（APIキー保管） | `1yB1HyhRCOfiQG0H1KNeLo1BcGkpXKsLc` |

---

## 7. セットアップ手順

### Step 1: Google Apps Script デプロイ

1. https://script.google.com → 「新しいプロジェクト」
2. プロジェクト名: `XOP_Wiki_API`
3. `gas_wiki_api.js` の内容を貼り付け（既存の `myFunction()` を削除）
4. `testWikiApi` 関数で動作確認（コンソールにファイル一覧が出ること）
5. 「デプロイ」→「新しいデプロイ」→ 種類: **ウェブアプリ**
   - 実行するユーザー: **自分（miyawaki.toshio@gmail.com）**
   - アクセスできるユーザー: **全員**
6. 発行された URL をメモ → `GAS_ENDPOINT_URL`
   ```
   https://script.google.com/macros/s/AKfycbx1JGu8Qdtinn2ISQGegBLP95E1R48S4_eMEnytR_kxDT-xwCLFkoCqXPvFHfCiwfC5Ug/exec
   ```

### Step 2: n8n クレデンシャル登録

| クレデンシャル名 | タイプ | Name | Value |
|---------------|------|------|-------|
| XopGp_bot（日報用・既存） | Telegram API | — | （既存トークン）|
| XopQA_bot（Q&A用・新規） | Telegram API | — | `8868759206:AAEyJ1YgPCuQLO7-eeQFV4_jehDO7mmn2vc` |
| Gemini API Key | Header Auth | `x-goog-api-key` | `AIzaSyDr6P-eaEBsRH2Tp4W01pO2HBvCKM7aThU` |
| NocoDB API Token | Header Auth | `xc-token` | `nc_pat_iMb1Gt3rNkvtQk-clGRjtVMVfT2KdOLc2ovQjpxM` |

> Gemini・NocoDB のAPIキーは Google Drive の .env ファイル（ID: `1yB1HyhRCOfiQG0H1KNeLo1BcGkpXKsLc`）に保存してください。

### Step 3: n8n ワークフローインポート

1. n8n「Workflows」→「Import from File」
2. `n8n_xop_qa_bot_v3.json` を選択
3. 以下の `FILL_ME` を置き換え:

| ノード | 項目 | 値 |
|--------|------|----|
| 📨 Telegram受信 | credentials.id | Telegram クレデンシャル ID |
| 📤 Telegram返信 | credentials.id | Telegram クレデンシャル ID |
| 📚 Wiki取得 (GAS) | url | Step1 の GAS_ENDPOINT_URL |
| 💼 Deals取得 | credentials.id | NocoDB クレデンシャル ID |
| ✅ Tasks取得 | credentials.id | NocoDB クレデンシャル ID |
| 🤖 Gemini API | credentials.id | Gemini クレデンシャル ID |

4. 保存 → 「Activate」

### Step 4: 動作確認

Telegram の XopGp_bot に以下を送信して確認:

```
XOPとウォーターセラミックの違いは？
施工単価はいくら？
海外展開で最優先の市場はどこですか？
代理店になるのに初期費用はいくら？
六本木ヒルズでの実績を教えて
現在の案件パイプラインを教えて
```

---

## 8. 運用ガイド

### Wiki 更新時

1. Google Drive の `XOP_Wiki/` 以下の `.md` ファイルを直接編集
2. n8n・GAS の変更は**不要**（GAS が毎回最新を取得するため）
3. 新しいフォルダを追加した場合も自動的に取得される

### 辞書更新時（新規顧客・会社追加）

1. `XOP_Wiki/辞書/XOP_用語辞書.md` を Google Drive で更新（Claude の参照に反映）
2. 頻出の誤認識パターンは `normalize.js` にも追記して n8n ワークフローを保存し直す

### NocoDB スキーマ変更時

- カラム名変更時: `🧩 プロンプト構築` ノードのコードは汎用フォーマットのため変更不要
- テーブル ID 変更時: `💼 Deals取得` / `✅ Tasks取得` ノードの URL を更新

---

## 9. トラブルシューティング

| 症状 | 原因 | 対処 |
|------|------|------|
| Wiki が取得できない | GAS デプロイ設定誤り | 「実行するユーザー: 自分」を確認 |
| GAS へのアクセス権エラー | 「全員」設定になっていない | デプロイ設定を確認・再デプロイ |
| Claude API エラー | APIキー誤り / 利用上限 | クレデンシャルと残高を確認 |
| Telegram に返信なし | Bot Token / Webhook 設定 | Bot token と Webhook URL を確認 |
| NocoDB 401 エラー | xc-token 期限切れ | NocoDB でトークンを再発行 |
| NocoDB 404 エラー | テーブル ID 誤り | URL の tableId を確認 |
| 文字化け | エンコーディング | GAS の `getDataAsString('UTF-8')` を確認 |
| 正規化されていない | normalize.js が古い | n8n ワークフローの Code ノードを更新 |

---

## 参考リンク

- Google Drive XOP_Wiki フォルダ: https://drive.google.com/drive/folders/1mzZnlFGEwy8fGceH3lA2t-RsXa2ZYRp3
- GAS エンドポイント: https://script.google.com/macros/s/AKfycbx1JGu8Qdtinn2ISQGegBLP95E1R48S4_eMEnytR_kxDT-xwCLFkoCqXPvFHfCiwfC5Ug/exec
- Google Apps Script: https://script.google.com
- NocoDB: https://app.nocodb.com
- Anthropic Console: https://console.anthropic.com
- n8n（セルフホスト）: 社内 URL
