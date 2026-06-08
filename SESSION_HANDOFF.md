# セッション引き継ぎプロンプト集

新しいセッションを開いたら、該当するプロンプトをそのままコピペしてください。

---

## #1 音声入力ワークフロー（日報の種）

```
以下の仕様書を読んでから作業を始めてください。

仕様書:
- /Users/gon/Documents/AIMemory/crux/20260517_CRUXタスク管理システム仕様書V2_1 .md
- /Users/gon/Documents/AIMemory/crux/XOP_QA_Bot/SPEC.md（GAS・n8n参考）

既存コード:
- /Users/gon/Documents/AIMemory/crux/XOP_QA_Bot/gas_wiki_api.js（GAS読み取り版・参考）

【現状】
- XopGp_bot（日報用）は稼働中
- GAS は XOP_Wiki の読み取りエンドポイントのみ（書き込みは未実装）

【今回のタスク】
音声入力 → 文字起こし → 整形 → Drive保存 → 本人返信 の n8n ワークフロー構築

【フロー】
音声メモ(XopGp_bot) → Gemini文字起こし → Gemini整形（フィラー除去・箇条書き）
→ GAS経由でDriveに保存 → Telegramで本人に返信

【整形ルール】
- フィラー除去（えー、あのー、まあ、えっと等）
- 内容を変えず箇条書きに整理
- 人名・会社名・数字は正確に保持
- 用語正規化: GAS経由で XOP_Wiki/辞書/XOP_用語辞書.md を参照
  （XOP_Wiki/辞書/ ID: 1BWQiPSAIHtYxpLG4fPZjXes6x1r0MYhR）

【Drive保存先】
- 業務メモ/ ID: 1m3Pc21a8dGwuB2faWLO4qoaPzW6Mgc6-
- INBOX/ ID: 174PXmcgyIvVJaeZnbCk9O_F9NfG3a5l7
- 保存パス: INBOX/YYYY-MM-DD/{username}_{HHMM}.md

【まず着手すること】
GAS に doPost（書き込みエンドポイント）を追加する
```

---

## #2 日報まとめワークフロー

```
以下の仕様書を読んでから作業を始めてください。

仕様書:
- /Users/gon/Documents/AIMemory/crux/20260517_CRUXタスク管理システム仕様書V2_1 .md（5.11章）

【前提】
- #1（音声入力ワークフロー）が完成済み
- INBOX/YYYY-MM-DD/ に {username}_{HHMM}.md が蓄積されている

【今回のタスク】
INBOX の種ファイルを集計 → 日報生成 → 各人に返信 → 宮脇に全員分送信

【フロー】
Schedule(19:00) or /まとめコマンド
→ GAS経由でINBOX/今日/ を読む
→ username ごとにグループ化
→ Gemini で日報Markdown生成
→ GAS経由で Wiki/日報/{名前}/YYYY-MM-DD.md に保存
  （2回目以降は _2.md, _3.md と連番）
→ 各メンバーに自分の日報を返信
→ 宮脇(miyawakiMM)に全員分まとめて送信

【Drive フォルダID】
- INBOX/ ID: 174PXmcgyIvVJaeZnbCk9O_F9NfG3a5l7
- Wiki/ ID: 1ozwGMWhMQaQ8MBIVdXVTm4TMHBXcJhN0
- Wiki/日報/ ID: 1nYzOQsIlJYobdFl2QyJPQ_T3_EKbLTqQ

【メンバーマッピング（Telegram username → 名前）】
miyawakiMM → 宮脇（管理者・全員分受信）
yoshioka*  → 吉岡
kobayashi* → 小林
takada*    → 高田
kitashoji* → 北庄司

【NocoDB】
- VoiceMemos テーブル ID: mfkc7q3k9fbfaeg
- 処理済みは processed フラグを True に更新
```

---

## #3 朝タスクレポート（改善・修正時）

```
以下の仕様書を読んでから作業を始めてください。

仕様書:
- /Users/gon/Documents/AIMemory/crux/20260517_CRUXタスク管理システム仕様書V2_1 .md（5.4章）

【現状】
- n8n ワークフロー稼働中（月〜土 7:30）
- NocoDB Deals/Tasks を取得して Telegram 送信
- 直前のエラー: 並列ノードの Merge 問題を修正済み

【NocoDB】
- Deals テーブル ID: m4dt4qlrw9ag6k0
- Tasks テーブル ID: m83uxghrdtij7gc
- API Token: nc_pat_iMb1Gt3rNkvtQk-clGRjtVMVfT2KdOLc2ovQjpxM

【今回の修正内容】
（ここに具体的な問題を記載してから送る）
```

---

## #4 Q&A Bot（改善・修正時）

```
以下のファイルを読んでから作業を始めてください。

仕様書:
- /Users/gon/Documents/AIMemory/crux/XOP_QA_Bot/SPEC.md

既存コード:
- /Users/gon/Documents/AIMemory/crux/XOP_QA_Bot/n8n_xop_qa_bot_v4.json  ← 最新 JSON
- /Users/gon/Documents/AIMemory/crux/XOP_QA_Bot/normalize.js
- /Users/gon/Documents/AIMemory/crux/XOP_QA_Bot/gas_wiki_api.js

【現状】（2026-05-25 更新）

稼働状況:
- ワークフロー v4 稼働中（XopQA_bot をグループに追加済み）
- Gemini API（gemini-2.5-flash）で回答生成
- Google Cloud Project: gen-lang-client-0554785916 (CRUX) — 後払いプラン済み

v4 での主な変更点（初稼働セッション）:
- Merge ノード追加（Wiki + Deals + Tasks の3並列 → 1出力、3重返信バグ修正）
- 回答に質問文を表示（❓ 質問 → 回答 の形式）
- maxOutputTokens: 1024 → 8192（途中切れ対策）
- 正規化ルール追加: 起訴者 → キーストーン社

QA ログ記録機能（2026-05-25 追加・稼働中）:
- ✂️ 回答整形ノードに question / answer フィールドを追加出力
- 📊 QAログ記録ノード追加（Telegram返信の後に実行）
- GAS doPost で Google スプレッドシートに記録 ✅
- 列構成: タイムスタンプ / ユーザー名 / 質問 / 回答 / チャットID
- 質問の先頭 = + - @ を 🔤 テキスト正規化ノードで除去（#NAME? 対策）

【正規化アーキテクチャ】

Layer 1 — 機械的 regex（n8n 🔤テキスト正規化ノード / normalize.js）:
  製品名・人名・会社名の固定パターンを即時置換
  → normalize.js と n8n JSON の jsCode を常に同期すること

Layer 2 — 意味的補正（Gemini + GAS 経由の XOP_用語辞書.md）:
  XOP_Wiki/辞書/XOP_用語辞書.md（Drive）を Gemini がコンテキストとして参照
  → Drive ファイルを更新するだけで即反映（デプロイ不要）

【Drive フォルダ構造】

XOP_Wiki/          ID: 1mzZnlFGEwy8fGceH3lA2t-RsXa2ZYRp3
└── 辞書/          ID: 1BWQiPSAIHtYxpLG4fPZjXes6x1r0MYhR
    └── XOP_用語辞書.md  ← 用語・誤認識パターンを蓄積

【GAS doPost アクション一覧】

action: "log_qa"  → QA ログをスプレッドシートに記録
  受け取るフィールド: timestamp / username / question / answer / chatId

【クレデンシャル（n8n登録済み）】

- XopQA_bot Token : 8868759206:AAEyJ1YgPCuQLO7-eeQFV4_jehDO7mmn2vc
- Gemini API Key  : AIzaSyDr6P-eaEBsRH2Tp4W01pO2HBvCKM7aThU
- NocoDB Token    : nc_pat_iMb1Gt3rNkvtQk-clGRjtVMVfT2KdOLc2ovQjpxM
- GAS Endpoint    : https://script.google.com/macros/s/AKfycbx1JGu8Qdtinn2ISQGegBLP95E1R48S4_eMEnytR_kxDT-xwCLFkoCqXPvFHfCiwfC5Ug/exec

【次回セッションで取り組む場合】
（ここに具体的な問題を記載してから送る）
```

---

## 共通情報（どのセッションでも参照）

| 項目 | 値 |
|------|-----|
| 業務メモ/ | `1m3Pc21a8dGwuB2faWLO4qoaPzW6Mgc6-` |
| INBOX/ | `174PXmcgyIvVJaeZnbCk9O_F9NfG3a5l7` |
| Wiki/ | `1ozwGMWhMQaQ8MBIVdXVTm4TMHBXcJhN0` |
| Wiki/日報/ | `1nYzOQsIlJYobdFl2QyJPQ_T3_EKbLTqQ` |
| XOP_Wiki/ | `1mzZnlFGEwy8fGceH3lA2t-RsXa2ZYRp3` |
| XOP_Wiki/辞書/ | `1BWQiPSAIHtYxpLG4fPZjXes6x1r0MYhR` |
| NocoDB Deals | `m4dt4qlrw9ag6k0` |
| NocoDB Tasks | `m83uxghrdtij7gc` |
| NocoDB VoiceMemos | `mfkc7q3k9fbfaeg` |
