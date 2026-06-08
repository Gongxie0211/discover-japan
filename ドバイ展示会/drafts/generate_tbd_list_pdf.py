#!/usr/bin/env python3
"""
ドバイ展示会 未決定・未回答項目リスト PDF 生成スクリプト
出力: 20260606_未決定項目リスト_社長確認用.pdf
"""

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ── フォント登録（ヒラギノ角ゴシック W3）──────────────────────────────
FONT_PATH = "/tmp/NotoSansJP.ttf"
pdfmetrics.registerFont(TTFont("NotoSansJP", FONT_PATH))
BASE_FONT = "NotoSansJP"

# ── 出力先 ──────────────────────────────────────────────────────────────
OUTPUT_DIR  = "/Users/gon/Documents/AIMemory/crux/ドバイ展示会/drafts"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "20260606_未決定項目リスト_社長確認用.pdf")

# ── スタイル定義 ─────────────────────────────────────────────────────────
def s(name, **kw):
    kw.setdefault("fontName", BASE_FONT)
    return ParagraphStyle(name, **kw)

ST_TITLE    = s("title",   fontSize=18, leading=26, textColor=colors.HexColor("#1B2A4A"), spaceAfter=2*mm)
ST_SUB      = s("sub",     fontSize=10, leading=14, textColor=colors.HexColor("#555555"), spaceAfter=6*mm)
ST_H1       = s("h1",      fontSize=12, leading=16, textColor=colors.white,
                            backColor=colors.HexColor("#1B2A4A"),
                            leftIndent=3*mm, spaceBefore=6*mm, spaceAfter=2*mm,
                            borderPad=3)
ST_H2       = s("h2",      fontSize=10, leading=14, textColor=colors.HexColor("#1B2A4A"),
                            spaceBefore=4*mm, spaceAfter=1*mm)
ST_BODY     = s("body",    fontSize=8.5, leading=13)
ST_CELL     = s("cell",    fontSize=8,   leading=12)
ST_CELL_RED = s("cellR",   fontSize=8,   leading=12, textColor=colors.HexColor("#CC0000"))
ST_CELL_ORG = s("cellO",   fontSize=8,   leading=12, textColor=colors.HexColor("#C45000"))
ST_NOTE     = s("note",    fontSize=7.5, leading=11, textColor=colors.HexColor("#777777"),
                            spaceBefore=1*mm)
ST_FOOTER   = s("footer",  fontSize=7,   leading=10, textColor=colors.HexColor("#999999"))

def P(text, style=None):
    return Paragraph(text, style or ST_CELL)

def section_header(text, icon=""):
    full = f"{icon} {text}" if icon else text
    return Paragraph(full, ST_H1)

def subsection(text):
    return Paragraph(text, ST_H2)

def note(text):
    return Paragraph(text, ST_NOTE)

# ── テーブルスタイル ─────────────────────────────────────────────────────
def make_table_style(header_color=colors.HexColor("#1B2A4A")):
    return TableStyle([
        # ヘッダー行
        ("BACKGROUND",  (0,0), (-1,0), header_color),
        ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
        ("FONTNAME",    (0,0), (-1,0), BASE_FONT),
        ("FONTSIZE",    (0,0), (-1,0), 8),
        ("BOTTOMPADDING",(0,0),(-1,0), 4),
        ("TOPPADDING",  (0,0), (-1,0), 4),
        # データ行
        ("FONTNAME",    (0,1), (-1,-1), BASE_FONT),
        ("FONTSIZE",    (0,1), (-1,-1), 8),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#F5F7FA")]),
        ("VALIGN",      (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",  (0,1), (-1,-1), 3),
        ("BOTTOMPADDING",(0,1),(-1,-1), 3),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING",(0,0), (-1,-1), 4),
        # 枠線
        ("BOX",         (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ("INNERGRID",   (0,0), (-1,-1), 0.3, colors.HexColor("#DDDDDD")),
    ])

# ── ページ設定 ───────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN = 18*mm
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=20*mm, bottomMargin=20*mm,
    title="ドバイ展示会 未決定項目リスト",
    author="CRUX G.K.",
)
W = PAGE_W - 2*MARGIN   # 有効幅 ≈ 174mm

story = []

# ══════════════════════════════════════════════════════════════════
# タイトルブロック
# ══════════════════════════════════════════════════════════════════
story.append(Paragraph("ドバイ展示会 未決定・未回答項目リスト", ST_TITLE))
story.append(Paragraph(
    "Middle East Coatings Show 2026（9月27〜30日 / Expo City Dubai）　"
    "作成日：2026年6月6日　　確認者：吉岡 正彦 代表", ST_SUB))
story.append(HRFlowable(width=W, thickness=1.5, color=colors.HexColor("#1B2A4A"), spaceAfter=4*mm))

# 凡例
legend_data = [
    [P("🔴 最優先", ST_CELL_RED),
     P("今週〜6月中旬に対応が必要。放置すると他タスクが全部止まる", ST_CELL)],
    [P("🟠 重要", ST_CELL_ORG),
     P("弁護士送付・ラベル設計などに直結。7月末までに確定が必要", ST_CELL)],
    [P("🟡 通常",  ST_CELL),
     P("弁護士レビュー後または現地法人確定後に自然に確定する項目", ST_CELL)],
]
legend_tbl = Table(legend_data, colWidths=[28*mm, W-28*mm])
legend_tbl.setStyle(TableStyle([
    ("BOX",         (0,0),(-1,-1), 0.5, colors.HexColor("#CCCCCC")),
    ("INNERGRID",   (0,0),(-1,-1), 0.3, colors.HexColor("#DDDDDD")),
    ("BACKGROUND",  (0,0),(-1,-1), colors.HexColor("#FAFAFA")),
    ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
    ("TOPPADDING",  (0,0),(-1,-1), 3),
    ("BOTTOMPADDING",(0,0),(-1,-1), 3),
    ("LEFTPADDING", (0,0),(-1,-1), 5),
]))
story.append(legend_tbl)
story.append(Spacer(1, 5*mm))

# ══════════════════════════════════════════════════════════════════
# A. キーストン確認項目
# ══════════════════════════════════════════════════════════════════
story.append(section_header("A．キーストン株式会社への確認事項", "🔴"))
story.append(note("担当：北庄司さん（送付済み問い合わせへの回答を催促）　回答期限目標：2026年6月15日"))
story.append(note("⚠ A-1・A-2 は SDS・TDS・ラベル全書類のボトルネック。未回答のまま最終化は不可。"))
story.append(Spacer(1, 2*mm))

a_data = [
    [P("No.", ST_CELL), P("確認事項", ST_CELL), P("影響する書類", ST_CELL), P("重要度", ST_CELL)],
    [P("A-1", ST_CELL_RED),
     P("シリカの種類（非晶質 CAS 7631-86-9 ／ 結晶質 CAS 14808-60-7 どちらか）", ST_CELL),
     P("SDS 英語・AR（Section 2,3,8,11）", ST_CELL),
     P("🔴 最重要\n結晶質なら発癌性再分類・全Section改訂", ST_CELL_RED)],
    [P("A-2", ST_CELL_RED),
     P("PFAS 非含有証明（フッ素系ポリマーが PFAS 物質に該当するか否か）", ST_CELL),
     P("SDS 英語・AR（Section 12）、TDS", ST_CELL),
     P("🔴 UAE／EU 規制対応の根幹", ST_CELL_RED)],
    [P("A-3", ST_CELL_ORG),
     P("保管有効期限（Shelf life）", ST_CELL),
     P("TDS 全3言語、ラベル全3言語（Item 7）、SDS Section 7", ST_CELL),
     P("🟠 容器設計・ラベル印刷の前提", ST_CELL_ORG)],
    [P("A-4", ST_CELL_ORG),
     P("容器サイズ（市販用の容量ラインナップ：例 200mL / 1L / 4L）", ST_CELL),
     P("TDS、ラベル全3言語（Item 5）、SDS、カタログ AR", ST_CELL),
     P("🟠 ラベル・パッケージ設計の前提", ST_CELL_ORG)],
    [P("A-5", ST_CELL_ORG),
     P("社名 TEL / FAX / Email / Website（正式な連絡先）", ST_CELL),
     P("SDS 英語・AR（Section 1.3）、ラベル全3言語（Item 2）", ST_CELL),
     P("🟠", ST_CELL_ORG)],
    [P("A-6", ST_CELL_ORG),
     P("緊急連絡先（24時間対応の有無、CHEMTREC 登録の有無）", ST_CELL),
     P("SDS 英語・AR（Section 1.4）", ST_CELL),
     P("🟠", ST_CELL_ORG)],
    [P("A-7"),
     P("TiO₂ の正確な含有量（% w/w）", ST_CELL),
     P("SDS 英語・AR（Section 3）", ST_CELL),
     P("🟡")],
    [P("A-8"),
     P("臭気・臭気閾値", ST_CELL),
     P("SDS 英語・AR（Section 9）", ST_CELL),
     P("🟡")],
    [P("A-9"),
     P("粘度（mPa·s）、VOC 含有量、表面張力、固形分含有量", ST_CELL),
     P("SDS 英語・AR（Section 9）", ST_CELL),
     P("🟡")],
    [P("A-10"),
     P("DNEL/PNEC データ（毒性評価用）", ST_CELL),
     P("SDS 英語・AR（Section 8）", ST_CELL),
     P("🟡")],
    [P("A-11"),
     P("皮膚・呼吸器 感作性データ", ST_CELL),
     P("SDS 英語・AR（Section 11）", ST_CELL),
     P("🟡")],
]

cw_a = [12*mm, 70*mm, 58*mm, 34*mm]
tbl_a = Table(a_data, colWidths=cw_a, repeatRows=1)
tbl_a.setStyle(make_table_style())
story.append(tbl_a)
story.append(Spacer(1, 5*mm))

# ══════════════════════════════════════════════════════════════════
# B. 社内決定事項
# ══════════════════════════════════════════════════════════════════
story.append(section_header("B．社内で決定が必要な事項", "🟠"))
story.append(note("担当：吉岡さん（事業判断）、宮脇さん（手続き）"))
story.append(Spacer(1, 2*mm))

b_data = [
    [P("No."), P("決定が必要な事項"), P("影響する書類"), P("期限"), P("重要度")],
    [P("B-1", ST_CELL_RED),
     P("弁護士の氏名・法律事務所名", ST_CELL),
     P("弁護士メール草稿（即日送付可能）", ST_CELL),
     P("今週中", ST_CELL_RED),
     P("🔴 これが決まれば全書類送付可能", ST_CELL_RED)],
    [P("B-2", ST_CELL_ORG),
     P("最低発注数量（MOQ）—— 例：1L単位 / 最低○L", ST_CELL),
     P("販売契約書 日英 V2（第5条・Article 5）", ST_CELL),
     P("弁護士送付前", ST_CELL_ORG),
     P("🟠", ST_CELL_ORG)],
    [P("B-3", ST_CELL_ORG),
     P("販売契約書の契約期間（第17条：__年間）", ST_CELL),
     P("販売契約書 日英 V2（第17条・Article 17）", ST_CELL),
     P("弁護士送付前", ST_CELL_ORG),
     P("🟠", ST_CELL_ORG)],
    [P("B-4", ST_CELL_ORG),
     P("遅延損害金の利率（年__% ／ または法定利率）", ST_CELL),
     P("販売契約書 日英 V2（第7条5項・Article 7.5）", ST_CELL),
     P("弁護士確認後", ST_CELL_ORG),
     P("🟠 弁護士へ確認依頼済み", ST_CELL_ORG)],
    [P("B-5", ST_CELL_RED),
     P("違約金額の日英統一\n英語版：¥50,000,000 ／ 日本語版：$100,000\nどちらに統一するか（または変更するか）", ST_CELL),
     P("NDA 日本語 V4（第8条2項）\nNDA 英語 V4（Article 11.2）", ST_CELL),
     P("弁護士確認後", ST_CELL_RED),
     P("🔴 書類間の齟齬 — 要統一", ST_CELL_RED)],
    [P("B-6", ST_CELL_ORG),
     P("会社の受取銀行口座情報\n（口座名義・銀行名・支店・口座番号・SWIFT/BIC・IBAN）", ST_CELL),
     P("見積書テンプレート（銀行情報欄）", ST_CELL),
     P("7月末", ST_CELL_ORG),
     P("🟠", ST_CELL_ORG)],
    [P("B-7", ST_CELL_ORG),
     P("販売価格の再検討\n（現在 $5,000/L — 中東市場での妥当性・希釈倍率による施工コスト訴求）", ST_CELL),
     P("見積書テンプレート、カタログ（価格表）", ST_CELL),
     P("7月末", ST_CELL_ORG),
     P("🟠", ST_CELL_ORG)],
]

cw_b = [12*mm, 55*mm, 50*mm, 22*mm, 35*mm]
tbl_b = Table(b_data, colWidths=cw_b, repeatRows=1)
tbl_b.setStyle(make_table_style(colors.HexColor("#C45000")))
story.append(tbl_b)
story.append(Spacer(1, 5*mm))

# ══════════════════════════════════════════════════════════════════
# C. 弁護士レビュー後に確定する項目
# ══════════════════════════════════════════════════════════════════
story.append(section_header("C．弁護士レビュー後に確定する事項", "🟡"))
story.append(note("弁護士に書類送付後、2〜3週間以内に弁護士より回答予定"))
story.append(Spacer(1, 2*mm))

c_data = [
    [P("No."), P("弁護士への確認事項"), P("影響する書類")],
    [P("C-1"),
     P("ICC仲裁条項（シンガポール）の適否・文言の最終確認", ST_CELL),
     P("NDA 日英 V4・販売契約書 日英 V2（全4通）", ST_CELL)],
    [P("C-2"),
     P("競業避止条項の有効性（終了後2年・地域限定）の確認", ST_CELL),
     P("NDA 日英 V4（第6条の2・第7条2項・Article 5,10）", ST_CELL)],
    [P("C-3"),
     P("テリトリー独占権条項のひな型提案（独占 / 非独占 選択式）", ST_CELL),
     P("販売契約書 日英 V2（第21条・Article 21）", ST_CELL)],
    [P("C-4"),
     P("MOQ・契約期間・遅延損害金利率の国際標準推奨値（B-2〜B-4 確認）", ST_CELL),
     P("販売契約書 日英 V2（第5条・第17条・第7条5項）", ST_CELL)],
]

cw_c = [12*mm, 85*mm, 77*mm]
tbl_c = Table(c_data, colWidths=cw_c, repeatRows=1)
tbl_c.setStyle(make_table_style(colors.HexColor("#7A8FA6")))
story.append(tbl_c)
story.append(Spacer(1, 5*mm))

# ══════════════════════════════════════════════════════════════════
# D. ドバイ法人・山田さん待ち
# ══════════════════════════════════════════════════════════════════
story.append(section_header("D．ドバイ法人・山田さんの確認待ち事項", "🔵"))
story.append(note("担当：吉岡さん → 山田さんへ確認　期限：7月末"))
story.append(Spacer(1, 2*mm))

d_data = [
    [P("No."), P("確認事項"), P("影響する書類"), P("期限")],
    [P("D-1"),
     P("ドバイ法人の使用可能時期（M&A先法人がいつ実際に動けるか）\n※ 輸出・物流全体スケジュールの前提", ST_CELL),
     P("輸出計画・物流フロー全体", ST_CELL),
     P("最優先\n今すぐ確認")],
    [P("D-2"),
     P("UAE現地エージェント／代理店の名称・住所", ST_CELL),
     P("ラベル全3言語（Item 3）\nカタログ AR（連絡先欄）", ST_CELL),
     P("7月末")],
    [P("D-3"),
     P("展示会ブース番号（申込確定後）", ST_CELL),
     P("カタログ AR（最終ページ）", ST_CELL),
     P("申込確定後")],
]

cw_d = [12*mm, 75*mm, 55*mm, 32*mm]
tbl_d = Table(d_data, colWidths=cw_d, repeatRows=1)
tbl_d.setStyle(make_table_style(colors.HexColor("#1A5276")))
story.append(tbl_d)
story.append(Spacer(1, 5*mm))

# ══════════════════════════════════════════════════════════════════
# E. 将来的に確定する項目（今は空欄のまま可）
# ══════════════════════════════════════════════════════════════════
story.append(section_header("E．商談・契約時に自然確定する項目（今は空欄のまま）", "⚪"))
story.append(Spacer(1, 2*mm))

e_data = [
    [P("No."), P("項目"), P("確定タイミング"), P("影響する書類")],
    [P("E-1"), P("契約締結日"),       P("商談相手との署名時"),   P("NDA・販売契約書（日英）")],
    [P("E-2"), P("買主情報（社名・住所・代表者）"), P("商談相手決定時"), P("NDA・販売契約書（日英）")],
    [P("E-3"), P("発注書番号・見積番号"),  P("個別発行時"),          P("見積書テンプレート")],
    [P("E-4"), P("EAN/JANバーコード番号"), P("GS1登録後"),           P("ラベル全言語")],
    [P("E-5"), P("ウェブサイト URL"),      P("サイト開設後"),         P("ラベル・カタログ")],
    [P("E-6"), P("価格・数量・合計金額（見積書本文）"), P("商談相手ごとに個別記入"), P("見積書テンプレート")],
]

cw_e = [12*mm, 55*mm, 45*mm, 62*mm]
tbl_e = Table(e_data, colWidths=cw_e, repeatRows=1)
tbl_e.setStyle(make_table_style(colors.HexColor("#555555")))
story.append(tbl_e)
story.append(Spacer(1, 6*mm))

# ══════════════════════════════════════════════════════════════════
# ボトルネック サマリー
# ══════════════════════════════════════════════════════════════════
story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor("#CCCCCC"), spaceAfter=3*mm))
story.append(Paragraph("優先順序サマリー", ST_H2))

summary_data = [
    [P("優先度"), P("アクション"), P("担当"), P("期限")],
    [P("🔴 最優先", ST_CELL_RED),
     P("B-1 弁護士名を確定 → メール送付（5書類の草稿完成済み）", ST_CELL_RED),
     P("宮脇さん", ST_CELL), P("今週中", ST_CELL_RED)],
    [P("🔴 最優先", ST_CELL_RED),
     P("A-1/A-2 キーストンへ回答催促（シリカ種類・PFAS証明）", ST_CELL_RED),
     P("北庄司さん", ST_CELL), P("6月15日", ST_CELL_RED)],
    [P("🟠 重要", ST_CELL_ORG),
     P("B-2/B-3 MOQ・契約期間を社内決定（弁護士送付前に記入）", ST_CELL_ORG),
     P("吉岡さん", ST_CELL), P("弁護士送付前", ST_CELL_ORG)],
    [P("🟠 重要", ST_CELL_ORG),
     P("B-5 違約金額の日英統一方針を決定", ST_CELL_ORG),
     P("吉岡さん", ST_CELL), P("弁護士送付前", ST_CELL_ORG)],
    [P("🟠 重要", ST_CELL_ORG),
     P("D-1 山田さんにドバイ法人使用可能時期を確認（物流計画の大前提）", ST_CELL_ORG),
     P("吉岡さん", ST_CELL), P("今すぐ", ST_CELL_ORG)],
    [P("🟡 通常"),
     P("B-6/B-7 銀行口座情報・価格再設定", ST_CELL),
     P("吉岡さん＋宮脇さん", ST_CELL), P("7月末")],
    [P("🟡 通常"),
     P("A-3〜A-13 キーストン回答次第で SDS・ラベル全書類を一気に最終化", ST_CELL),
     P("宮脇さん＋AI", ST_CELL), P("回答後随時")],
]

cw_s = [18*mm, 90*mm, 28*mm, 28*mm]
tbl_s = Table(summary_data, colWidths=cw_s, repeatRows=1)
tbl_s.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#1B2A4A")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,-1), BASE_FONT),
    ("FONTSIZE",     (0,0), (-1,-1), 8),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#F5F7FA")]),
    ("VALIGN",       (0,0), (-1,-1), "TOP"),
    ("TOPPADDING",   (0,0), (-1,-1), 3),
    ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ("LEFTPADDING",  (0,0), (-1,-1), 4),
    ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ("BOX",          (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
    ("INNERGRID",    (0,0), (-1,-1), 0.3, colors.HexColor("#DDDDDD")),
]))
story.append(tbl_s)
story.append(Spacer(1, 4*mm))

# ── フッター ─────────────────────────────────────────────────────────────
story.append(HRFlowable(width=W, thickness=0.5, color=colors.HexColor("#CCCCCC"), spaceAfter=2*mm))
story.append(Paragraph(
    "CRUX G.K.（クラックス合同会社）　担当：宮脇 利夫　miyawaki.toshio@gmail.com　"
    "⚠ 本資料は社内共有用。外部への配布・転送不可。",
    ST_FOOTER))

# ── ビルド ───────────────────────────────────────────────────────────────
doc.build(story)
print(f"✅ PDF生成完了: {OUTPUT_FILE}")
