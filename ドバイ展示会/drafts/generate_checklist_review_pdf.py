#!/usr/bin/env python3
"""
ドバイ展示会 チェックリスト 担当者・内容確認シート
各タスクに回答欄つき（手書き用）
出力: 20260606_チェックリスト確認シート_社長確認用.pdf
"""

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── フォント ──────────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont("NotoSansJP", "/tmp/NotoSansJP.ttf"))
F = "NotoSansJP"

# ── 出力先 ──────────────────────────────────────────────────────────────
OUTPUT = "/Users/gon/Documents/AIMemory/crux/ドバイ展示会/drafts/20260606_チェックリスト確認シート_社長確認用.pdf"

# ── カラー ──────────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#1B2A4A")
ORANGE = colors.HexColor("#C45000")
GRAY   = colors.HexColor("#555555")
LGRAY  = colors.HexColor("#F0F2F5")
LLGRAY = colors.HexColor("#FAFAFA")
WHITE  = colors.white
RED    = colors.HexColor("#CC0000")
GOLD   = colors.HexColor("#C9A84C")

# ── スタイル ──────────────────────────────────────────────────────────────
def sty(name, **kw):
    kw.setdefault("fontName", F)
    return ParagraphStyle(name, **kw)

ST_COVER_TITLE = sty("ct", fontSize=20, leading=28, textColor=NAVY, spaceAfter=3*mm)
ST_COVER_SUB   = sty("cs", fontSize=10, leading=15, textColor=GRAY, spaceAfter=2*mm)
ST_COVER_NOTE  = sty("cn", fontSize=8.5, leading=13, textColor=GRAY)
ST_CAT_HDR     = sty("ch", fontSize=13, leading=18, textColor=WHITE, spaceAfter=0)
ST_TASK_NO     = sty("tn", fontSize=10, leading=14, textColor=NAVY)
ST_TASK_BODY   = sty("tb", fontSize=8.5, leading=13, textColor=colors.HexColor("#222222"))
ST_TASK_ORIG   = sty("to", fontSize=7.5, leading=11, textColor=GRAY)
ST_Q_LABEL     = sty("ql", fontSize=10, leading=14, textColor=NAVY)
ST_ANS_LABEL   = sty("al", fontSize=7.5, leading=11, textColor=GRAY)
ST_MEMBER      = sty("mb", fontSize=8, leading=12)
ST_FOOTER      = sty("ft", fontSize=7, leading=10, textColor=GRAY)
ST_DEADLINE    = sty("dl", fontSize=8, leading=12, textColor=ORANGE)
ST_PAGE_BREAK_NOTE = sty("pbn", fontSize=7.5, leading=11, textColor=GRAY, spaceBefore=1*mm)

def P(text, st=None):
    return Paragraph(text, st or ST_TASK_BODY)

# ── ページ設定 ──────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN_L = 16*mm
MARGIN_R = 16*mm
MARGIN_T = 16*mm
MARGIN_B = 16*mm
W = PAGE_W - MARGIN_L - MARGIN_R  # ≈ 178mm

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=MARGIN_L, rightMargin=MARGIN_R,
    topMargin=MARGIN_T, bottomMargin=MARGIN_B,
    title="ドバイ展示会 チェックリスト確認シート",
    author="CRUX G.K.",
)

# ── メンバーチェックボックス行 ───────────────────────────────────────────
MEMBERS = ["吉岡", "宮脇", "北庄司", "高田", "山田（ドバイ）", "キーストン", "未定・外注"]
# 列幅：「山田（ドバイ）」が折り返さないよう広めに確保
MEMBER_WIDTHS = [20*mm, 20*mm, 23*mm, 20*mm, 34*mm, 28*mm, W - 145*mm]

def checkbox_row():
    """担当者チェックボックス行（□ 名前 × 7人）"""
    cells = []
    for m in MEMBERS:
        cells.append(Paragraph(f"□ {m}", ST_MEMBER))
    row_data = [cells]
    widths = MEMBER_WIDTHS
    tbl = Table(row_data, colWidths=widths)
    tbl.setStyle(TableStyle([
        ("FONTNAME",    (0,0), (-1,-1), F),
        ("FONTSIZE",    (0,0), (-1,-1), 8),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0), (-1,-1), 2),
        ("BOTTOMPADDING",(0,0),(-1,-1), 2),
        ("LEFTPADDING", (0,0), (-1,-1), 2),
        ("BACKGROUND",  (0,0), (-1,-1), LGRAY),
        ("BOX",         (0,0), (-1,-1), 0.4, colors.HexColor("#CCCCCC")),
        ("INNERGRID",   (0,0), (-1,-1), 0.3, colors.HexColor("#DDDDDD")),
    ]))
    return tbl

def write_box(label="", height=12*mm):
    """手書き記入欄"""
    inner = Table(
        [[Paragraph(label, ST_ANS_LABEL), ""]],
        colWidths=[30*mm, W - 30*mm],
        rowHeights=[height]
    )
    inner.setStyle(TableStyle([
        ("FONTNAME",    (0,0),(-1,-1), F),
        ("VALIGN",      (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",  (0,0),(-1,-1), 2),
        ("LEFTPADDING", (0,0),(-1,-1), 3),
        ("BACKGROUND",  (0,0),(0,0), LGRAY),
        ("BACKGROUND",  (1,0),(1,0), WHITE),
        ("BOX",         (0,0),(-1,-1), 0.5, colors.HexColor("#AAAAAA")),
        ("INNERGRID",   (0,0),(-1,-1), 0.3, colors.HexColor("#CCCCCC")),
    ]))
    return inner

def task_block(no, deadline, current_desc, hint_q, status="☐"):
    """1タスク分のブロックを生成"""
    # ヘッダー行（タスクNo・期限・現在の担当）
    header_data = [[
        Paragraph(f"<b>{no}</b>", ST_TASK_NO),
        Paragraph(f"期限：{deadline}", ST_DEADLINE),
        Paragraph(f"現状：{status}", ST_TASK_ORIG),
    ]]
    header_tbl = Table(header_data, colWidths=[20*mm, 50*mm, W-70*mm])
    header_tbl.setStyle(TableStyle([
        ("FONTNAME",    (0,0),(-1,-1), F),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
        ("LEFTPADDING", (0,0),(-1,-1), 4),
        ("BACKGROUND",  (0,0),(-1,-1), LGRAY),
        ("BOX",         (0,0),(-1,-1), 0.5, colors.HexColor("#CCCCCC")),
    ]))

    elems = [
        header_tbl,
        Spacer(1, 1*mm),
        # 現在の記述（参考）
        Table([[Paragraph("現在の記述：", ST_ANS_LABEL), Paragraph(current_desc, ST_TASK_ORIG)]],
              colWidths=[22*mm, W-22*mm],
              style=TableStyle([
                  ("FONTNAME", (0,0),(-1,-1), F),
                  ("VALIGN",   (0,0),(-1,-1), "TOP"),
                  ("TOPPADDING",(0,0),(-1,-1), 2),
                  ("BOTTOMPADDING",(0,0),(-1,-1), 2),
                  ("LEFTPADDING",(0,0),(-1,-1), 4),
                  ("BACKGROUND",(0,0),(-1,-1), colors.HexColor("#F8F8F8")),
                  ("BOX",(0,0),(-1,-1), 0.3, colors.HexColor("#DDDDDD")),
              ])),
        Spacer(1, 1.5*mm),
        # Q1: 担当者
        Paragraph("<b>Q1｜実際の担当者は誰ですか？　当てはまる人に ✓ または名前を記入</b>", ST_Q_LABEL),
        Spacer(1, 1*mm),
        checkbox_row(),
        Spacer(1, 1.5*mm),
        # Q2: ヒント質問（タスク固有）
        Paragraph(f"<b>Q2｜{hint_q}</b>", ST_Q_LABEL),
        Spacer(1, 1*mm),
        write_box("現状・補足：", height=14*mm),
        Spacer(1, 1.5*mm),
        # Q3: 次のアクション
        Paragraph("<b>Q3｜このタスクの「次にやるべき具体的なアクション」を教えてください</b>", ST_Q_LABEL),
        Spacer(1, 1*mm),
        write_box("次のアクション：", height=14*mm),
        Spacer(1, 3*mm),
        HRFlowable(width=W, thickness=0.4, color=colors.HexColor("#DDDDDD"), spaceAfter=3*mm),
    ]
    return KeepTogether(elems)

def cat_header(letter, title, color=NAVY):
    tbl = Table(
        [[Paragraph(f"カテゴリ {letter}　{title}", ST_CAT_HDR)]],
        colWidths=[W],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), color),
        ("TOPPADDING", (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",(0,0),(-1,-1), 6),
    ]))
    return tbl

# ══════════════════════════════════════════════════════════════════
# ストーリー組み立て
# ══════════════════════════════════════════════════════════════════
story = []

# ── 表紙ブロック ──────────────────────────────────────────────────
story.append(Spacer(1, 8*mm))
story.append(Paragraph("ドバイ展示会 チェックリスト", ST_COVER_TITLE))
story.append(Paragraph("担当者・タスク内容 確認シート", sty("ct2", fontSize=14, leading=20, textColor=ORANGE, spaceAfter=4*mm)))
story.append(HRFlowable(width=W, thickness=2, color=NAVY, spaceAfter=4*mm))
story.append(Paragraph("Middle East Coatings Show 2026　9月27〜30日 / Expo City Dubai", ST_COVER_SUB))
story.append(Paragraph("記入日：　　　　年　　月　　日　　　確認者：吉岡 正彦 代表", ST_COVER_SUB))
story.append(Spacer(1, 3*mm))

cover_note = """
<b>【このシートの使い方】</b><br/>
現在のチェックリストには「担当者が実態とズレている」「タスク内容が抽象的で次のアクションがわかりにくい」箇所が多数あります。<br/>
各タスクについて以下の3点をご確認・ご記入ください。<br/>
　<b>Q1</b>：実際に動く担当者（✓ を入れる、または名前を書き足す）<br/>
　<b>Q2</b>：現状・補足（どこまで進んでいるか、わかっていること）<br/>
　<b>Q3</b>：次にやるべき具体的なアクション（「〇〇に電話して▲▲を確認する」レベルで）<br/>
<br/>
記入後、宮脇さんに戻していただければチェックリストを更新します。
"""
story.append(Table(
    [[Paragraph(cover_note, sty("cn2", fontSize=8, leading=13, fontName=F))]],
    colWidths=[W],
    style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), LGRAY),
        ("BOX",(0,0),(-1,-1), 0.8, NAVY),
        ("TOPPADDING",(0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",(0,0),(-1,-1), 8),
    ])
))
story.append(Spacer(1, 6*mm))
story.append(HRFlowable(width=W, thickness=0.5, color=GRAY, spaceAfter=4*mm))

# ══ カテゴリ A ════════════════════════════════════════════════════
story.append(cat_header("A", "展示会申込関連（締切：2026年6月30日・最優先）", NAVY))
story.append(Spacer(1, 3*mm))

story.append(task_block("A-1", "6月30日",
    "展示会ブース申込書類の提出（Middle East Coatings Show 公式フォーム）",
    "申込フォームや主催者への連絡は誰がどこまで進めていますか？（まだ未着手？サイト確認済み？問い合わせ済み？）"))

story.append(task_block("A-2", "6月25日",
    "企業情報（英語）準備 — CRUX G.K. 正式登録情報",
    "英語での会社情報（登録番号・代表者名・住所等）は手元にありますか？申込フォームに必要な項目は確認していますか？"))

story.append(task_block("A-3", "6月25日",
    "企業情報（アラビア語）準備 — 翻訳・確認",
    "アラビア語翻訳は必要ですか？翻訳者のあてはありますか？（主催者が英語のみで受け付ける場合は不要かも）"))

story.append(task_block("A-4", "6月30日",
    "製品カテゴリ登録（Coatings / Surface Treatment）",
    "出展カテゴリは主催者の選択肢で確認しましたか？「Coatings」以外に登録すべきカテゴリはありますか？"))

story.append(task_block("A-5", "6月30日",
    "ロゴ入稿 — kichi ブランドロゴ（デザイナー納品予定：6月30日）",
    "kichi ブランドロゴの制作は誰に依頼していますか？進捗は？6月30日に間に合いそうですか？"))

story.append(task_block("A-6", "6月30日",
    "ブース概要・展示計画の提出（展示品目・ブースレイアウト概要）",
    "ブースのサイズ・形式（小間数）は決まっていますか？何を展示する予定ですか？"))

story.append(task_block("A-7", "6月30日",
    "申込費用の支払い（クレジットカードまたは銀行送金）",
    "費用の金額は確認していますか？支払い方法・支払い口座は誰が手配しますか？"))

# ══ カテゴリ B ════════════════════════════════════════════════════
story.append(cat_header("B", "書類・契約（目標：2026年7月末）", colors.HexColor("#1A5276")))
story.append(Spacer(1, 3*mm))

story.append(task_block("B-1", "6月20日",
    "NDA日英V4・販売契約書日英V2 弁護士送付（草稿完成済み・弁護士名待ち）",
    "依頼する弁護士・法律事務所は決まっていますか？国際取引に詳しい先生はいますか？",
    status="🔄 草稿完成"))

story.append(task_block("B-2", "7月15日",
    "NDA英語版V4 最終署名版 準備（商談用10部）",
    "10部という数は適切ですか？印刷は日本で？ドバイ現地で？電子署名（DocuSign等）は検討していますか？"))

story.append(task_block("B-3", "7月31日",
    "NDA アラビア語版 翻訳・確認（必要に応じて）",
    "アラビア語版のNDAは必要だと思いますか？翻訳者・法律翻訳のあてはありますか？"))

story.append(task_block("B-4", "7月31日",
    "販売契約書日英V2 弁護士レビュー完了（B-1と同時送付）",
    "販売契約書で特に弁護士に確認したい点はありますか？（価格・支払い条件・テリトリー等）",
    status="🔄 草稿完成"))

story.append(task_block("B-5", "7月31日",
    "代理店規約（骨子→正式版）弁護士確認",
    "代理店規約は販売契約書とは別に用意する予定ですか？独占代理店を想定していますか？"))

story.append(task_block("B-6", "キーストン回答後+2週間",
    "SDS英語版 EHS専門家レビュー（キーストン回答後に着手）",
    "EHS（環境・健康・安全）の専門家に心当たりはありますか？外注費用の見積もりはしていますか？"))

story.append(task_block("B-7", "8月15日",
    "SDS アラビア語版 翻訳・確認",
    "SDSのアラビア語翻訳は法律・化学の専門用語が必要です。対応できる翻訳者・機関に心当たりはありますか？"))

# ══ カテゴリ C ════════════════════════════════════════════════════
story.append(cat_header("C", "製品・パッケージ（目標：2026年8月末）", colors.HexColor("#1E8449")))
story.append(Spacer(1, 3*mm))

story.append(task_block("C-1", "7月15日",
    "200ml容器 × 5本セット サンプル作成依頼（キーストンに確認）",
    "200ml容器はドバイ現地調達が合理的という案が出ています。日本から持参 vs 現地調達、どちらを想定していますか？"))

story.append(task_block("C-2", "7月31日",
    "サンプル受領・品質確認",
    "サンプルの品質確認は誰が行いますか？判定基準はありますか？"))

story.append(task_block("C-3", "7月31日",
    "kichi ブランド ラベルデザイン確定（英語版・アラビア語版）",
    "デザインはどこに依頼しますか？kichi のロゴ・ブランドカラーはすでに決まっていますか？"))

story.append(task_block("C-4", "8月15日",
    "ラベル印刷 — 英語版（UAE輸出用ラベル規制対応）",
    "印刷会社はすでに決まっていますか？UAE規制対応の確認はどこに依頼しますか？"))

story.append(task_block("C-5", "8月15日",
    "ラベル印刷 — アラビア語版（RTL対応・UAE義務9項目）",
    "アラビア語の右から左（RTL）レイアウトに対応できるデザイナー・印刷会社はいますか？"))

story.append(task_block("C-6", "8月15日",
    "バーコード取得 — EAN-13（GS1 Japan または GS1 UAE登録）",
    "GS1への登録は誰が手配しますか？日本（GS1 Japan）で取得予定ですか？"))

story.append(task_block("C-7", "7月31日",
    "容器の輸入規制確認（UAE向け — ESMA規制、容量表記等）",
    "この確認はドバイ側（山田さん）にお願いできますか？それとも日本側で調べますか？"))

story.append(task_block("C-8", "8月31日",
    "パッケージ最終仕様確認・サンプル承認",
    "最終承認は誰が行いますか？（吉岡さん？キーストン社？）承認の基準・フローはありますか？"))

# ══ カテゴリ D ════════════════════════════════════════════════════
story.append(cat_header("D", "規制・認証（目標：2026年8月末）", colors.HexColor("#6E2F8A")))
story.append(Spacer(1, 3*mm))

story.append(task_block("D-1", "6月15日",
    "キーストンへの技術確認（シリカ種類CAS番号、PFAS非含有証明、製品成分詳細）",
    "キーストンへの問い合わせはすでに送りましたか？回答の見込みはいつ頃ですか？窓口は誰ですか？"))

story.append(task_block("D-2", "キーストン回答後",
    "シリカ種類確認（非晶質CAS確認）",
    "この確認がなぜ重要か理解していますか？（結晶質だとSDS全体の発癌性分類が変わります）誰が判断しますか？"))

story.append(task_block("D-3", "キーストン回答後",
    "PFAS非含有証明書 取得（キーストンから）",
    "キーストン社はPFAS非含有証明書を発行できると言っていますか？証明書のフォーマットは確認していますか？"))

story.append(task_block("D-4", "8月15日",
    "UAE向けSDS最終版作成（EHS専門家と協力）",
    "EHS専門家はUAE規制（ESMA/MOHAP）に詳しい人が必要です。どこかあてはありますか？"))

story.append(task_block("D-5", "7月31日",
    "UAE Consumer Protection Law（連邦法15号）適合確認",
    "UAE法規制の確認は山田さん（ドバイ）経由でできますか？現地の法務・コンサルタントを使いますか？"))

story.append(task_block("D-6", "8月15日",
    "ラベル義務9項目の確認・対応（英語・アラビア語両方）",
    "UAE義務9項目（製品名・製造者・原産国・容量・ロット番号・保管方法・使用方法・危険表示・有効期限）は把握していますか？"))

story.append(task_block("D-7", "8月31日",
    "REACH規制適合確認（EU輸出も視野に入れる場合）",
    "今回の展示会でEU向け展開も視野に入れていますか？REACH対応は急ぎですか？"))

story.append(task_block("D-8", "7月31日",
    "展示会での化学品取扱規制確認（Expo City Dubai の規則）",
    "展示会場での化学品の持ち込み・展示ルールは確認していますか？山田さんに調べてもらえますか？"))

# ══ カテゴリ E ════════════════════════════════════════════════════
story.append(cat_header("E", "現地対応・物流（目標：2026年9月初旬）", colors.HexColor("#784212")))
story.append(Spacer(1, 3*mm))

story.append(task_block("E-1", "7月31日",
    "ドバイ法人設立完了確認（M&A先との最終確認、JPY 3,000,000決済確認）",
    "山田さんのドバイ法人はいつから使えますか？JPY 300万の決済は完了していますか？"))

story.append(task_block("E-2", "7月15日",
    "現地担当者（山田さん）への書類共有・役割分担確認",
    "山田さんとはどのくらいの頻度で連絡を取っていますか？役割分担（何を山田さんに任せるか）は決まっていますか？"))

story.append(task_block("E-3", "8月15日",
    "展示会用サンプル・備品リスト作成",
    "どんなサンプルや備品を持参する予定ですか？（石材サンプル・施工デモ機器・カタログ・名刺等）誰がリストを作りますか？"))

story.append(task_block("E-4", "8月31日",
    "サンプル輸出手配（DHL等）— 輸出書類一式作成",
    "DHLや他のフォワーダーに見積もりを取りましたか？化学品の航空輸送規制（IATA）は確認しましたか？"))

story.append(task_block("E-5", "8月31日",
    "輸出書類作成：Invoice（商業インボイス）",
    "インボイスは誰が作成しますか？英語・アラビア語どちらが必要ですか？フォーマットはありますか？"))

story.append(task_block("E-6", "8月31日",
    "輸出書類作成：Packing List（梱包明細書）",
    "梱包明細書は誰が作りますか？輸出物の品目・数量・重量は決まっていますか？"))

story.append(task_block("E-7", "8月31日",
    "輸出書類作成：Certificate of Origin（原産地証明書）",
    "原産地証明書は商工会議所で取得が必要です。手続きは誰が担当しますか？"))

story.append(task_block("E-8", "8月31日",
    "UAE輸入通関手続き確認（現地エージェントまたはフォワーダー手配）",
    "ドバイ側での通関は山田さんが手配できますか？現地の通関業者に心当たりはありますか？"))

story.append(task_block("E-9", "8月31日",
    "ブース設営計画確定（レイアウト・展示什器・電源・インターネット等）",
    "ブースレイアウトのイメージはありますか？設営は山田さんがドバイで手配しますか？什器は現地レンタルですか？"))

story.append(task_block("E-10", "9月15日",
    "ブース備品・什器手配（現地調達またはJapanから発送）",
    "ブースに必要な什器（テーブル・椅子・パネル・モニター等）は現地調達予定ですか？費用の見積もりはありますか？"))

story.append(task_block("E-11", "9月15日",
    "展示サンプル（石材等への施工済みサンプル）作成・発送",
    "施工済みサンプルは誰が作りますか？どんな石材を使いますか？大きさ・枚数は？"))

# ══ カテゴリ F ════════════════════════════════════════════════════
story.append(cat_header("F", "商談準備（目標：2026年9月 展示会本番）", colors.HexColor("#922B21")))
story.append(Spacer(1, 3*mm))

story.append(task_block("F-1", "7月31日",
    "価格表（英語版）確定 — ※現在 $5,000/L、要再設定",
    "現行価格 $5,000/L は展示会向けとして適切だと思いますか？希釈倍率を考慮した施工コスト訴求はできますか？"))

story.append(task_block("F-2", "8月15日",
    "価格表（アラビア語版）翻訳",
    "価格表のアラビア語翻訳は誰に依頼しますか？AED（ディルハム）表記も必要ですか？"))

story.append(task_block("F-3", "8月31日",
    "製品カタログ（英語版）最終版 印刷",
    "英語版カタログのデザインは誰が担当しますか？TBD項目（キーストン回答待ち）が埋まってから印刷できますか？"))

story.append(task_block("F-4", "8月31日",
    "製品カタログ（アラビア語版）最終版 印刷",
    "アラビア語版カタログのデザイン・印刷は日本とドバイどちらで手配しますか？"))

story.append(task_block("F-5", "8月15日",
    "TDS英語版 最終版（キーストン技術確認後）",
    "TDSの最終確認はキーストンに承認してもらう必要がありますか？誰が確認のやり取りをしますか？"))

story.append(task_block("F-6", "8月31日",
    "TDS アラビア語版 翻訳",
    "TDSのアラビア語翻訳は専門家が必要ですか？SDSアラビア語版と同じ翻訳者に依頼できますか？"))

story.append(task_block("F-7", "9月20日",
    "商談用NDA署名済みセット 準備（10部）",
    "NDAは紙の署名ですか？電子署名ですか？英語版だけですか？アラビア語版も必要ですか？"))

story.append(task_block("F-8", "9月20日",
    "デモ用施工サンプル（御影石・大理石・砂岩等）現地持参分準備",
    "どの石材のサンプルを持参しますか？施工済みと未施工の比較セットにする予定ですか？誰が施工しますか？"))

story.append(task_block("F-9", "8月31日",
    "展示会用名刺 — kichi ブランド対応版（英語・アラビア語併記）",
    "名刺の英語版はありますか？アラビア語の名前・役職表記は準備していますか？全員分必要ですか？"))

story.append(task_block("F-10", "8月31日",
    "商談シート / ヒアリングシート作成（見込み客情報収集用）",
    "商談シートで収集したい情報は何ですか？（会社名・連絡先・興味製品・購入量・流通エリア等）誰が作りますか？"))

story.append(task_block("F-11", "8月31日",
    "ターゲット顧客リスト作成（UAE/GCC 石材業者・建設会社・コーティング販売業者）",
    "ターゲット顧客の情報はどこから集めますか？山田さんのネットワークを活用できますか？"))

story.append(task_block("F-12", "9月25日",
    "展示会期間中のアポイント事前設定（登録参加者リスト活用）",
    "主催者から参加者リストは提供されますか？事前アポはメール・LinkedInどちらで取りますか？英語とアラビア語どちらで連絡しますか？"))

# ── フッター ──────────────────────────────────────────────────────
story.append(HRFlowable(width=W, thickness=0.5, color=GRAY, spaceAfter=2*mm))
story.append(Paragraph(
    "CRUX G.K.（クラックス合同会社）　担当：宮脇 利夫　miyawaki.toshio@gmail.com　"
    "｜ 53タスク全確認シート　記入後、宮脇さんにご返却ください",
    ST_FOOTER))

# ── ビルド ──────────────────────────────────────────────────────
doc.build(story)
print(f"✅ PDF生成完了: {OUTPUT}")
