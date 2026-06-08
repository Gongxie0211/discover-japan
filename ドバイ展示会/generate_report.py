from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Japanese fonts
pdfmetrics.registerFont(TTFont("HiraW3", "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"))
pdfmetrics.registerFont(TTFont("HiraW6", "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"))

# Color palette
NAVY   = colors.HexColor("#0D1B3E")
GOLD   = colors.HexColor("#C9A84C")
CYAN   = colors.HexColor("#00B4D8")
LGRAY  = colors.HexColor("#F4F6F9")
MGRAY  = colors.HexColor("#DDE2EA")
WHITE  = colors.white
RED    = colors.HexColor("#C0392B")
GREEN  = colors.HexColor("#1A7A4A")

# Styles
def S(name, **kw):
    base = dict(fontName="HiraW3", fontSize=10, leading=16, textColor=NAVY)
    base.update(kw)
    return ParagraphStyle(name, **base)

s_title   = S("title",   fontName="HiraW6", fontSize=22, leading=28, textColor=WHITE, spaceAfter=4)
s_sub     = S("sub",     fontName="HiraW3", fontSize=11, leading=16, textColor=GOLD,  spaceAfter=8)
s_h1      = S("h1",      fontName="HiraW6", fontSize=14, leading=20, textColor=NAVY,  spaceBefore=14, spaceAfter=6)
s_h2      = S("h2",      fontName="HiraW6", fontSize=11, leading=16, textColor=NAVY,  spaceBefore=10, spaceAfter=4)
s_body    = S("body",    fontSize=9.5, leading=16, spaceAfter=4)
s_bullet  = S("bullet",  fontSize=9.5, leading=15, leftIndent=12, spaceAfter=2)
s_caption = S("caption", fontSize=8,   leading=12, textColor=colors.HexColor("#666666"), spaceAfter=6)
s_tag     = S("tag",     fontName="HiraW6", fontSize=9, textColor=WHITE)
s_risk    = S("risk",    fontName="HiraW6", fontSize=9.5, leading=15, textColor=RED, leftIndent=12, spaceAfter=2)

W, H = A4

output_path = "/Users/gon/Documents/AIMemory/crux/ドバイ展示会/XOP競合分析レポート_MECS2026.pdf"

doc = SimpleDocTemplate(
    output_path, pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm,
    topMargin=14*mm, bottomMargin=14*mm
)

def page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(LGRAY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Header bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 22*mm, W, 22*mm, fill=1, stroke=0)
    # Gold accent line
    canvas.setFillColor(GOLD)
    canvas.rect(0, H - 23.5*mm, W, 1.5*mm, fill=1, stroke=0)
    # Footer
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    canvas.setFont("HiraW3", 8)
    canvas.setFillColor(GOLD)
    canvas.drawString(18*mm, 3.2*mm, "CRUX G.K.  |  ProtoCare XOP  |  Confidential")
    canvas.drawRightString(W - 18*mm, 3.2*mm, f"Page {doc.page}")
    canvas.restoreState()

def white_card(story, content_fn):
    """Wrap content in a white rounded card via a 1-cell table."""
    inner = []
    content_fn(inner)
    t = Table([[inner]], colWidths=[W - 36*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), WHITE),
        ("ROUNDEDCORNERS", [6]),
        ("BOX", (0,0), (-1,-1), 0.5, MGRAY),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))

story = []

# ── HEADER (placed as table over background) ──────────────────────────────
header_data = [[
    Paragraph("ProtoCare XOP 競合分析レポート", s_title),
    Paragraph("Middle East Coatings Show 2026<br/>調査日：2026年6月7日　作成：CRUX G.K.", s_sub),
]]
ht = Table(header_data, colWidths=[W - 36*mm])
ht.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,-1), colors.transparent),
    ("TOPPADDING",   (0,0), (-1,-1), 4),
    ("BOTTOMPADDING",(0,0), (-1,-1), 0),
    ("LEFTPADDING",  (0,0), (-1,-1), 0),
    ("RIGHTPADDING", (0,0), (-1,-1), 0),
]))
story.append(Spacer(1, 14*mm))   # push below nav bar drawn by page_bg
story.append(ht)
story.append(Spacer(1, 6))

# ── 1. 調査対象展示会 ───────────────────────────────────────────────────────
story.append(Paragraph("1. 調査対象展示会", s_h1))
def card1(s):
    s.append(Paragraph("Middle East Coatings Show 2026", s_h2))
    rows = [
        ["開催日程", "2026年9月28〜30日"],
        ["会　場",   "ドバイ展示センター（DEC）Expo City Dubai"],
        ["規　模",   "出展社 350社以上 ／ 来場者 5,000人以上 ／ 展示面積 15,000㎡以上"],
        ["出展国数",  "24カ国以上"],
        ["位置付け",  "中東・北アフリカ最大の塗料・コーティング業界展示会"],
    ]
    t = Table(rows, colWidths=[32*mm, W - 36*mm - 32*mm - 20*mm])
    t.setStyle(TableStyle([
        ("FONTNAME",  (0,0), (-1,-1), "HiraW3"),
        ("FONTSIZE",  (0,0), (-1,-1), 9.5),
        ("TEXTCOLOR", (0,0), (0,-1), NAVY),
        ("FONTNAME",  (0,0), (0,-1), "HiraW6"),
        ("TEXTCOLOR", (1,0), (1,-1), NAVY),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, LGRAY]),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("GRID", (0,0), (-1,-1), 0.3, MGRAY),
    ]))
    s.append(t)
white_card(story, card1)

# ── 2. ProtoCare XOP 製品概要 ────────────────────────────────────────────
story.append(Paragraph("2. ProtoCare XOP 製品概要", s_h1))
def card2(s):
    s.append(Paragraph("コア技術", s_h2))
    tech = [
        ["技術分類", "高分子浸透性フッ素ポリマー（C-C+F結合）"],
        ["結合エネルギー", "116 kcal/mol"],
        ["耐UV原理", "解離波長 250nm ＜ 地表UV限界 280nm → 物理的に劣化しない"],
        ["撥水・撥油", "水・油・排気ガス・油性マジックを完全拒絶"],
        ["透明性・透湿性", "外観変化なし、石材の「呼吸」を維持"],
        ["白華リスク", "ゼロ（無機ケイ酸塩系との決定的差異）"],
        ["保証", "15年保証（認定施工者適用）"],
        ["LCC削減効果", "70〜75%削減"],
        ["ターゲット市場", "ラグジュアリー不動産（高級ホテル・GINZA SIXレベル）"],
    ]
    t = Table(tech, colWidths=[38*mm, W - 36*mm - 38*mm - 20*mm])
    t.setStyle(TableStyle([
        ("FONTNAME",  (0,0), (-1,-1), "HiraW3"),
        ("FONTSIZE",  (0,0), (-1,-1), 9.5),
        ("FONTNAME",  (0,0), (0,-1), "HiraW6"),
        ("TEXTCOLOR", (0,0), (0,-1), NAVY),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, LGRAY]),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("GRID", (0,0), (-1,-1), 0.3, MGRAY),
    ]))
    s.append(t)
white_card(story, card2)

# ── 3. 競合分析 ─────────────────────────────────────────────────────────────
story.append(Paragraph("3. 競合分析", s_h1))

# Tier 1
def card_fila(s):
    # Tag
    tag_t = Table([[Paragraph("Tier 1 直接競合 ／ 最大の脅威", s_tag)]],
                  colWidths=[60*mm])
    tag_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), RED),
        ("ROUNDEDCORNERS",[4]),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
    ]))
    s.append(tag_t)
    s.append(Spacer(1,4))
    s.append(Paragraph("FILA Solutions（イタリア）", s_h2))
    rows = [
        ["技　術", "浸透型石材保護シーラー（MP90 ECO XTREME 等）"],
        ["中東実績", "ルーブル美術館（アブダビ）、バーレーン空港、カタール国際空港、Expo2020"],
        ["現地拠点", "ドバイに現地GM・法人あり"],
        ["主な訴求", '"Lifetime performance and warranty"'],
        ["XOPとの差", "C-F結合の耐UV理論的優位なし／撥油性は限定製品のみ／白華リスクあり"],
        ["MECS出展", "可能性が高い（同市場・同顧客層で競合）"],
    ]
    t = Table(rows, colWidths=[28*mm, W - 36*mm - 28*mm - 20*mm])
    t.setStyle(TableStyle([
        ("FONTNAME",  (0,0), (-1,-1), "HiraW3"),
        ("FONTSIZE",  (0,0), (-1,-1), 9.5),
        ("FONTNAME",  (0,0), (0,-1), "HiraW6"),
        ("TEXTCOLOR", (0,0), (0,-1), NAVY),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, LGRAY]),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("GRID", (0,0), (-1,-1), 0.3, MGRAY),
    ]))
    s.append(t)
white_card(story, card_fila)

def card_drytreat(s):
    tag_t = Table([[Paragraph("Tier 1 直接競合", s_tag)]], colWidths=[36*mm])
    tag_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), colors.HexColor("#E67E22")),
        ("ROUNDEDCORNERS",[4]),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
    ]))
    s.append(tag_t)
    s.append(Spacer(1,4))
    s.append(Paragraph("DryTreat / STAIN-PROOF（オーストラリア）", s_h2))
    rows = [
        ["技　術", "シラン＋フッ素ポリマー混合型浸透シーラー"],
        ["防汚等級", "ISO 10545-14 Class 5（最高等級）"],
        ["保証年数", "15年保証（認定施工者適用）"],
        ["中東拠点", "UAE・オマーンに代理店あり（市場参入済み）"],
        ["XOPとの差", "シランベース＋フッ素添加型。Si-C結合は340nmで崩壊リスク。純粋C-C+F結合ではない"],
        ["総　評", "保証年数は同等。技術純度・白華ゼロ・ラグジュアリー特化でXOPが差別化可能"],
    ]
    t = Table(rows, colWidths=[28*mm, W - 36*mm - 28*mm - 20*mm])
    t.setStyle(TableStyle([
        ("FONTNAME",  (0,0), (-1,-1), "HiraW3"),
        ("FONTSIZE",  (0,0), (-1,-1), 9.5),
        ("FONTNAME",  (0,0), (0,-1), "HiraW6"),
        ("TEXTCOLOR", (0,0), (0,-1), NAVY),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, LGRAY]),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("GRID", (0,0), (-1,-1), 0.3, MGRAY),
    ]))
    s.append(t)
white_card(story, card_drytreat)

# Tier 2
def card_tier2(s):
    tag_t = Table([[Paragraph("Tier 2 間接競合", s_tag)]], colWidths=[36*mm])
    tag_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), NAVY),
        ("ROUNDEDCORNERS",[4]),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
    ]))
    s.append(tag_t)
    s.append(Spacer(1,4))

    tier2 = [
        ["企業名", "技術・特徴", "MECS", "XOPとの関係"],
        ["AGC LUMIFLON\n（日本・欧州）",
         "FEVE樹脂（塗料原料）\n表面被膜型",
         "2026\n出展確定",
         "来場者の「フッ素=LUMIFLON」\n認知が競合になり得る"],
        ["Wacker Chemicals\n（ドイツ）",
         "シリコーン・シランシロキサン系\n撥水性は高いが撥油性なし",
         "過去\n出展確認",
         "石材保護市場での\n先行認知が脅威"],
    ]
    col_w = [(W - 36*mm - 20*mm) / 4] * 4
    t = Table(tier2, colWidths=col_w)
    t.setStyle(TableStyle([
        ("FONTNAME",     (0,0), (-1,-1), "HiraW3"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("FONTNAME",     (0,0), (-1,0),  "HiraW6"),
        ("BACKGROUND",   (0,0), (-1,0),  NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0),  WHITE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LGRAY]),
        ("ALIGN",        (0,0), (-1,-1), "LEFT"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("GRID",         (0,0), (-1,-1), 0.3, MGRAY),
    ]))
    s.append(t)
white_card(story, card_tier2)

# ── 4. 差別化比較表 ───────────────────────────────────────────────────────
story.append(Paragraph("4. 差別化比較表", s_h1))
def card_matrix(s):
    def mark(v):
        style = ParagraphStyle("m", fontName="HiraW6", fontSize=12,
                               alignment=1, leading=16,
                               textColor=(GREEN if v=="◎" else
                                          colors.HexColor("#E67E22") if v=="○" else
                                          colors.HexColor("#AAAAAA") if v=="△" else RED))
        return Paragraph(v, style)

    matrix = [
        [Paragraph("差別化軸", s_tag),
         Paragraph("XOP", s_tag),
         Paragraph("FILA", s_tag),
         Paragraph("DryTreat", s_tag),
         Paragraph("Wacker", s_tag)],
        ["撥油性",      mark("◎"), mark("△"), mark("○"), mark("×")],
        ["耐UV（物理保証）", mark("◎"), mark("△"), mark("△"), mark("×")],
        ["白華リスクゼロ", mark("◎"), mark("×"), mark("△"), mark("△")],
        ["透湿性維持",   mark("◎"), mark("◎"), mark("◎"), mark("△")],
        ["保証年数",
         Paragraph("15年", s_body),
         Paragraph("Lifetime", s_body),
         Paragraph("15年", s_body),
         Paragraph("—", s_body)],
        ["中東実績",     mark("×"), mark("◎"), mark("○"), mark("△")],
        ["ラグジュアリー特化", mark("◎"), mark("○"), mark("△"), mark("×")],
    ]

    cw = (W - 36*mm - 20*mm)
    col_widths = [cw*0.32, cw*0.17, cw*0.17, cw*0.17, cw*0.17]
    t = Table(matrix, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("FONTNAME",     (0,0), (-1,-1), "HiraW3"),
        ("FONTSIZE",     (0,0), (-1,-1), 9.5),
        ("BACKGROUND",   (0,0), (-1,0),  NAVY),
        ("TEXTCOLOR",    (0,0), (0,-1),  NAVY),
        ("FONTNAME",     (0,0), (0,-1),  "HiraW6"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LGRAY]),
        ("BACKGROUND",   (1,1), (1,-1),  colors.HexColor("#E8F5EE")),
        ("ALIGN",        (1,0), (-1,-1), "CENTER"),
        ("ALIGN",        (0,0), (0,-1),  "LEFT"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("GRID",         (0,0), (-1,-1), 0.3, MGRAY),
        ("BOX",          (1,1), (1,-1),  1.2, GREEN),
    ]))
    s.append(t)
    s.append(Spacer(1,4))
    s.append(Paragraph("◎ 最強優位　○ 優位　△ 限定的　× なし", s_caption))
white_card(story, card_matrix)

# ── 5. XOPの勝ち筋 ───────────────────────────────────────────────────────
story.append(Paragraph("5. XOPの勝ち筋", s_h1))
def card_win(s):
    wins = [
        ("物理法則による絶対的優位",
         "C-C+F結合（解離波長250nm）を破壊するエネルギーは地球上に存在しない。FILAもDryTreatも同等の理論的根拠を持たない。"),
        ("撥油性の決定的差異",
         "水だけでなく「油」を弾けるのはフッ素系の専売特許。FILA・Wackerには撥油機能がない。"),
        ("白華リスクゼロ保証",
         "高級大理石・御影石へのCa系白華リスクはFILAにとっての潜在的弱点。数百万ドルの美観が一度の化学反応で失われるリスクをXOPは排除する。"),
        ("認定施工者システム（ゴールド階層・地域独占）",
         "品質保証を施工者の資格制度で担保する構造。アマチュアリスクをゼロにする仕組みは他社にない。"),
        ("日本品質 × ラグジュアリー特化",
         "中東市場における日本ブランドの希少性と信頼性。「汎用品ではなくラグジュアリーのために設計された製品」という唯一性。"),
    ]
    for i, (title, body) in enumerate(wins, 1):
        row = Table(
            [[Paragraph(str(i), ParagraphStyle("num", fontName="HiraW6",
                        fontSize=14, textColor=WHITE, alignment=1, leading=18)),
              [Paragraph(title, ParagraphStyle("wt", fontName="HiraW6",
                         fontSize=10, textColor=NAVY, leading=15)),
               Paragraph(body, s_body)]]],
            colWidths=[10*mm, W - 36*mm - 10*mm - 20*mm]
        )
        row.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(0,0),  CYAN),
            ("BACKGROUND",    (1,0),(1,0),  WHITE),
            ("VALIGN",        (0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",    (0,0),(-1,-1), 6),
            ("BOTTOMPADDING", (0,0),(-1,-1), 6),
            ("LEFTPADDING",   (0,0),(0,0),   0),
            ("LEFTPADDING",   (1,0),(1,0),   8),
            ("RIGHTPADDING",  (0,0),(-1,-1), 6),
            ("BOX",           (0,0),(-1,-1), 0.3, MGRAY),
        ]))
        s.append(row)
        s.append(Spacer(1,3))
white_card(story, card_win)

# ── 6. 課題・リスク ───────────────────────────────────────────────────────
story.append(Paragraph("6. 課題・リスク", s_h1))
def card_risk(s):
    risks = [
        "中東実績ゼロ：FILAはルーブル美術館級の実績を持つ。展示会で最初に突かれるポイント。実績の代替として「日本国内の高級施設実績＋技術理論」で補完する必要がある。",
        "市場認知の遅れ：DryTreatはUAE代理店経由ですでに施工業者の認知を得ている。XOPは「知られていない」状態からのスタート。",
        "展示会トーク準備：「なぜFILAではなくXOPか」「DryTreatと何が違うのか」を30秒で答えられる営業トークの事前準備が必須。",
    ]
    for r in risks:
        s.append(Paragraph("▲  " + r, s_risk))
        s.append(Spacer(1,2))
white_card(story, card_risk)

story.append(Spacer(1, 8))
story.append(Paragraph(
    "本レポートはMiddle East Coatings Show 2026への出展検討を目的として作成されました。競合情報は公開情報に基づくものです。",
    s_caption
))

doc.build(story, onFirstPage=page_bg, onLaterPages=page_bg)
print(f"✅ PDF生成完了: {output_path}")
