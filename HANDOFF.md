# CRUX セッション引き継ぎ資料
最終更新: 2026-06-07

---

## プロジェクト概要

**クラックス合同会社（CRUX G.K.）** のWebサイト＋営業資料整備プロジェクト。

- 製品：プロトケア XOP（石材向け）／ プロトケア FC（木材向け）／ **鉄・金属向け製品（名称未定・情報待ち）**
- 製造元：株式会社キーストン／販売：クラックス合同会社
- サイトリポジトリ：`/Users/gon/Documents/AIMemory/crux/website/`
- Next.js (App Router, static) + TypeScript + Tailwind CSS v4
- デプロイ：`vercel --prod --yes`

---

## ブランドカラー

| 用途 | カラー |
|---|---|
| 背景（黒） | `#0A0A0A` |
| ゴールド | `#C9A84C` |
| オフホワイト | `#F5F3EF` |
| グレー | `#8C8C8C` |

---

## 完了済み作業

### Webサイト

- `/technology` ページ（XOP）
  - 断面図SVG → AI画像（`diagram-old-stone.png` / `diagram-new-stone.png`）に置き換え済み
  - UV chart SVG → AI画像（`diagram-uv-spectrum.png`）に置き換え済み
  - 見出し：「太陽光では、XOPを分解できない。」

- `/technology2` ページ（FC）新規作成済み（現在ナビ未リンク・非公開）
  - Hero→Problem→Regret（喪失対比）→Principle→Proof→Science(RadarChart)→Applications→Comparison→Cases→CTA
  - 断面図：`diagram-old-wood.png` / `diagram-new-wood.png`
  - 喪失対比セクション：`fc-regret.png` / `fc-protected.png`
  - レーダーチャートSVG（6軸：耐久性・素材感維持・紫外線防止・メンテナンス・汚染防止・抗菌防カビ）

### 生成済み画像（`/website/public/images/`）

```
fc-hero.png, fc-proof.png, fc-shrine.png, fc-loghouse.png,
fc-deck.png, fc-facade.png, fc-cases.png, fc-regret.png, fc-protected.png,
diagram-old-stone.png, diagram-new-stone.png,
diagram-old-wood.png, diagram-new-wood.png, diagram-uv-spectrum.png
```

### 営業資料

- `/Users/gon/Documents/AIMemory/crux/sales/XOP_セールストーク_QA集.md` + `.pdf`
- `/Users/gon/Documents/AIMemory/crux/sales/FC_セールストーク_QA集.md` + `.pdf`

両ファイルとも：
- 表現ルール表（過剰表現の禁止事項を明記）
- 30秒ピッチ・差別化トーク・科学トーク・クロージング・Q&A
- 「施工は誰が？」→ **クラックス合同会社、またはクラックスの技術研修を修了した施工業者** に修正済み

---

## 表現ルール（重要）

| 項目 | 使ってよい表現 | NG・保留中 |
|---|---|---|
| XOP メンテ費削減 | 「**70%以上**削減」（キーストン公式） | 「75%削減」は断言不可 |
| XOP 耐久性 | 「**実績15年以上**」 | 「15年保証」は断言不可 |
| XOP 試験 | 「(一財)建材試験センター」JIS A 1404・A 6909・A 1454 | ~~JIS A 1454は汚染性試験~~ →正しくは滑り性試験 |
| XOP 実績 | GINZA SIX・六本木ヒルズ（公式カタログ記載済み・使用可） | — |
| FC 耐久性 | 「壁面で**10年以上**」 | — |
| FC LCC削減 | 「塗り替え回数が大幅に減る」 | 具体%は未確定、断言不可 |

---

## ⏳ 保留中タスク

### 1. キーストン確認待ち（最優先）
- 75%削減 → 公式は「70%以上」。キーストンに確認中、回答次第で資料を修正
- 15年保証 → 公式はQ&A「要相談」。同上

### 2. ~~FC競合調査~~ ✅ 完了（2026-06-07）
- `FC_競合分析.md` / `FC_競合分析.pdf` 作成済み
- 最重要競合：tatara撥水セラミック（屋外半年〜1年でメンテ必要 vs FC 10年以上）
- 他：オスモカラー・リボス（有機系）、キシラデコール・ガードラック（薬剤型）

### 3. ~~XOP競合調査~~ ✅ 完了（2026-06-07）
- `XOP_競合分析.md` / `XOP_競合分析.pdf` 作成済み
- 最重要競合：ウォーターセラミック（アクアテック・シリカ系・防水特化・姫路城実績）
- 他：アリストン（フッ素+シリコーン混合）、AD-COAT、シーカ（Sika）
- 確認宿題：XOPフッ素がPFAS非該当か → キーストンに確認できれば強い差別化になる

### 4. /technology2 公開タイミング
- FCページはナビ未リンクの状態を維持
- 公開するときはナビゲーションに追加するだけでOK

### 5. PDFの再生成
- キーストン確認後、75%/15年の表現が確定したらPDFを再生成

### 7. 塩害Q&Aの追記
- XOP塩害対応のQ&Aをセールストーク集に追加（宮脇さんOK次第）
- キーストンへ確認：塩害環境での施工実績・塩化物イオン浸透抑制試験の有無

### 8. 鉄・金属向け製品（情報待ち）
- キーストンにFC・XOPに続く**鉄・金属向けプロテケア製品**があるとのこと
- 製品名・成分・特徴の情報が入り次第：競合分析＋セールストークを作成予定
- XOPとの組み合わせ提案（石材+鉄骨建築）でセールス幅が広がる可能性あり

### 9. 問い合わせBotの実装（次フェーズ検討中）
- 問い合わせフォームは心理的ハードルが高く使われにくいという課題
- 方向性：GAS Web App + Claude API でチャットBot
  - Q&A集・競合分析を知識ベースに使用
  - 会話ログ → Google Sheets自動記録
  - 「連絡希望」→ Gmail通知 → クラックスからフォローアップ
- NotebookLM は**社内スタッフ向け**（顧客向けBotには不向き：埋め込み不可・連絡先取得不可）

---

## ディレクトリ構成（主要ファイル）

```
/Users/gon/Documents/AIMemory/crux/
├── website/
│   ├── app/
│   │   ├── technology/page.tsx      ← XOP技術ページ
│   │   └── technology2/page.tsx     ← FC技術ページ（非公開）
│   └── public/images/               ← 生成画像すべてここ
├── sales/
│   ├── XOP_セールストーク_QA集.md/pdf
│   ├── FC_セールストーク_QA集.md/pdf
│   ├── XOP_競合分析.md/pdf          ← 2026-06-07 新規
│   ├── FC_競合分析.md/pdf           ← 2026-06-07 新規
│   └── generate_competition_pdf.py  ← Chrome headless PDF生成スクリプト
└── Branding Contents/               ← 参考画像・元素材置き場
```

---

## PDF生成コマンド（覚書）

```bash
cd /Users/gon/Documents/AIMemory/crux/sales
# 競合分析PDF生成（Chrome headless使用）
python3.12 generate_competition_pdf.py

# セールストークPDF生成（同スクリプトに追加可能）
# generate_competition_pdf.py の FILES リストに追加すればOK
```
※ `python3`ではなく`python3.12`を使うこと（markdown-itが3.12にインストール済み）  
※ Chrome headless + markdown_it → HTML → PDF の流れ

---

## 直近の会話の流れ（コンテキスト保持用）

### セッション1（〜2026-06-07前半）
1. キーストン実績カタログPDFを確認 → GINZA SIX・六本木ヒルズ使用可を確認
2. FC製品のPDFを読み込み、/technology2ページを新規作成
3. 断面図SVG → GPT Image 2による電子顕微鏡風断面画像に置き換え
4. UV chart SVG → GPT Image 2による太陽光スペクトル画像に置き換え
5. 喪失対比セクション（fc-regret/fc-protected）追加
6. XOP・FC両方のセールストーク&Q&A集をMD+PDFで作成
7. 「施工は誰が？」の回答をクラックスに修正

### セッション2（2026-06-07）
8. FC競合分析 作成（tatara撥水セラミック・オスモ・リボス・キシラデコール等）
9. XOP競合分析 作成（ウォーターセラミック・アリストン・AD-COAT・Sika等）
10. 両競合分析をPDF化（Chrome headless + generate_competition_pdf.py）
11. 問い合わせページのUX改善を議論 → Bot化の方向性を検討
12. **GAS + Claude API構成で問い合わせBotを実装検討中** ← 次回はここから
