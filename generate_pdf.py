from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUTPUT = "/Users/gon/Documents/AIMemory/crux/CRUX-BRANDING-REPORT.pdf"

# Register Japanese font (use system font)
pdfmetrics.registerFont(TTFont("JP", "/Library/Fonts/Arial Unicode.ttf"))
print("Using font: Arial Unicode.ttf")

# Colors
GOLD = colors.HexColor("#C9A84C")
BLACK = colors.HexColor("#0A0A0A")
NAVY = colors.HexColor("#1C2B3A")
OFFWHITE = colors.HexColor("#F5F3EF")
GRAY = colors.HexColor("#8C8C8C")

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=20*mm,
    leftMargin=20*mm,
    topMargin=20*mm,
    bottomMargin=20*mm,
)

styles = getSampleStyleSheet()

def S(name, **kw):
    kw.setdefault("fontName", "JP")
    return ParagraphStyle(name, **kw)

title_style = S("Title", fontSize=20, leading=30, textColor=BLACK, spaceAfter=2*mm)
subtitle_style = S("Subtitle", fontSize=11, leading=16, textColor=GRAY, spaceAfter=8*mm)
h1_style = S("H1", fontSize=14, leading=20, textColor=NAVY, spaceBefore=8*mm, spaceAfter=3*mm, borderPad=2*mm)
h2_style = S("H2", fontSize=12, leading=18, textColor=GOLD, spaceBefore=5*mm, spaceAfter=2*mm)
body_style = S("Body", fontSize=9.5, leading=17, textColor=BLACK, spaceAfter=3*mm)
bullet_style = S("Bullet", fontSize=9.5, leading=17, textColor=BLACK, leftIndent=8*mm, spaceAfter=1*mm)
note_style = S("Note", fontSize=8.5, leading=14, textColor=GRAY, spaceAfter=2*mm)
highlight_style = S("Highlight", fontSize=11, leading=18, textColor=NAVY, leftIndent=8*mm, spaceAfter=3*mm, fontName="JP")

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=GOLD, spaceAfter=4*mm, spaceBefore=4*mm)

def p(text, style=None):
    if style is None:
        style = body_style
    return Paragraph(text, style)

def h1(text):
    return Paragraph(text, h1_style)

def h2(text):
    return Paragraph(text, h2_style)

def sp(n=4):
    return Spacer(1, n*mm)

story = []

# Cover
story.append(sp(10))
story.append(p("CRUX ブランディング・プロジェクト報告書", title_style))
story.append(p("2026年5月29日", subtitle_style))
story.append(hr())

# Intro
story.append(p(
    "この報告書は、2026年5月29日に行ったCRUXのブランディング・Web制作・SNS戦略立案の全工程を、"
    "社長に説明するためにまとめたものです。「何をやったか」だけでなく、「なぜそうしたか」「これからどこへ向かうか」を軸に書いています。"
))

# 1
story.append(hr())
story.append(h1("1. 出発点：何が課題だったか"))
story.append(p(
    "CRUXは今まで、外から見ると「キーストンの代理店」に見えていました。"
    "XOPという優れた製品を持ちながら、それを売るだけの会社——という印象です。"
    "これは事実と大きく違います。しかし、現在の見せ方ではその差が伝わりません。"
))
story.append(p(
    "さらに、社長はこれまで築いてきた人脈がハワイ・ドバイ・韓国・モロッコなど世界中に広がっています。"
    "その多くが「海外に資産を持つ日本人実業家」です。これは非常に希少な顧客基盤です。"
    "にもかかわらず、CRUXのWebサイトは日本語しかなく、デザインも「街の業者」の域を出ていませんでした。"
))

# 2
story.append(hr())
story.append(h1("2. 最初の決断：何者になるか"))
story.append(p("ブランディングの核心は、「自分たちが何者か」を決めることです。今回、CRUXは次のように再定義しました。"))
story.append(p("　　「建築資産保護の専門家」", highlight_style))
story.append(p("　　XOPはその手段のひとつ。CRUXはそれを超えた存在。", note_style))
story.append(p("英語では："))
story.append(p("　　Building Asset Protection. Japanese Precision.", highlight_style))
story.append(p("この一行に込めた意味："))
story.append(p("・Building Asset Protection — 建物を守るだけでなく、オーナーの「資産」を守る専門家", bullet_style))
story.append(p("・Japanese Precision — 日本の職人技・誠実さ・正確さへの信頼を、ブランドの核に置く", bullet_style))
story.append(p(
    "海外に資産を持つ日本人は、「信頼できる日本人業者」を切実に求めています。"
    "現地業者への不信、言葉の壁、手抜き工事への不安——そこへ「日本の技術・日本人の誠実さ」で応えるポジションは、世界中でほぼ空席です。"
))

# 3
story.append(hr())
story.append(h1("3. ブランドの構築"))
story.append(h2("ビジュアル"))
story.append(p("・カラー: 黒（#0A0A0A）× 金（#C9A84C）× ネイビー（#1C2B3A）", bullet_style))
story.append(p("　→ 高級感・信頼・精密さを表現。ゴールドは「価値あるものを守る」象徴。", note_style))
story.append(p("・フォント: 英語はCormorant Garamond（クラシックな格調）、日本語はNoto Serif JP", bullet_style))
story.append(p("　→「老舗の信頼感」と「現代的な洗練さ」を両立。", note_style))
story.append(h2("キャッチフレーズ"))

table_data = [
    ["日本語", "あなたの建築資産を、日本の技術で守る。"],
    ["英語", "Building Asset Protection. Japanese Precision."],
]
tbl = Table(table_data, colWidths=[30*mm, 130*mm])
tbl.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,-1), "JP"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#F5F3EF")),
    ("TEXTCOLOR", (0,0), (0,-1), NAVY),
    ("TEXTCOLOR", (1,0), (1,-1), BLACK),
    ("GRID", (0,0), (-1,-1), 0.3, GOLD),
    ("PADDING", (0,0), (-1,-1), 5),
    ("LEADING", (0,0), (-1,-1), 16),
]))
story.append(tbl)
story.append(sp(3))

story.append(h2("ブランドの姿勢"))
story.append(p("・言う：「資産を守る」「信頼できるパートナー」「世界基準の技術」", bullet_style))
story.append(p("・言わない：「安い」「お気軽に」「なんでもやります」", bullet_style))
story.append(p("高級感と専門性を、すべての言葉・デザインで一貫させる方針を決めました。"))

# 4
story.append(hr())
story.append(h1("4. Webサイトの制作"))
story.append(p("今日、CRUXの新しいWebサイトを1日で完成・公開しました。"))
story.append(p("公開URL：https://website-eight-pi-70.vercel.app（将来的には crux-japan.com に切り替え）", note_style))

table_data2 = [
    ["ページ", "役割"],
    ["ホーム", "世界中の日本人オーナーへの第一印象。問題提起から始まり、CRUXへの信頼に導く"],
    ["技術（XOP）", "XOPの仕組みを図解。比較表で「なぜXOPか」を説明"],
    ["施工実績", "実績が少ない今は「Trust Bridge」方式で誠実に説明。ドバイ・ハワイの事例を掲載"],
    ["CRUXについて", "社長の人物像とCRUXの物語。「南十字星」の比喩でブランドの哲学を語る"],
    ["お問い合わせ", "7項目のフォーム。「急かさない、まず話を聞く」姿勢を前面に"],
]
tbl2 = Table(table_data2, colWidths=[35*mm, 125*mm])
tbl2.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,-1), "JP"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("TEXTCOLOR", (0,0), (-1,0), OFFWHITE),
    ("BACKGROUND", (0,1), (0,-1), colors.HexColor("#F5F3EF")),
    ("TEXTCOLOR", (0,1), (0,-1), NAVY),
    ("GRID", (0,0), (-1,-1), 0.3, GOLD),
    ("PADDING", (0,0), (-1,-1), 5),
    ("LEADING", (0,0), (-1,-1), 15),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#FAFAFA")]),
]))
story.append(tbl2)
story.append(sp(3))
story.append(p("・日英バイリンガル：ヘッダーのボタンひとつで日本語⇔英語に切り替わる", bullet_style))
story.append(p("・スマートフォン対応：世界中どこからでも快適に閲覧できる", bullet_style))
story.append(p("・高速・無料：GitHub + Vercelの仕組みで、サーバー費用なし", bullet_style))

# 5
story.append(hr())
story.append(h1("5. SNS戦略"))
story.append(h2("なぜSNSか"))
story.append(p(
    "社長の人脈は世界中に広がっています。その人たちに「CRUXは今も動いている」「こんな仕事をしている」を伝え続けることが、"
    "次の仕事につながります。SNSは、その「継続的な存在感」を作る道具です。"
))
story.append(h2("LinkedIn（ビジネス系）"))
story.append(p("・目的：信頼・専門性の発信。「建築資産保護の専門家」としての社長ブランド確立", bullet_style))
story.append(p("・投稿頻度：週1〜2回", bullet_style))
story.append(p("・内容例：「ドバイの建物に日本の技術を導入した話」「なぜ外壁保護が資産価値に直結するか」", bullet_style))
story.append(p("・運用モデル：社長が現場写真1枚＋一言メモを送る → AIが投稿文に整える → 確認して公開", bullet_style))
story.append(h2("Instagram（ビジュアル系）　@crux_buildingprotection"))
story.append(p("・目的：世界各地の現場・景色・仕事の様子を発信。「かっこいいCRUX」を視覚で伝える", bullet_style))
story.append(p("・投稿頻度：週1〜2回（火・木 19〜21時JST）", bullet_style))
story.append(p("・内容例：施工前後の写真、ドバイの風景、ハワイの物件", bullet_style))
story.append(p("社長がSNSに不慣れでも続けられる仕組みを設計しました。「写真を撮って一言送るだけ」でAIが整えます。完璧より継続を優先します。"))

# 6
story.append(hr())
story.append(h1("6. AI写真の制作"))
story.append(p("「まだ実績が少ない」という課題に対し、AIで見本写真15枚を生成しました。"))

table_data3 = [
    ["カテゴリ", "枚数", "用途"],
    ["ヒーロービジュアル（外壁・建築）", "3枚", "サイトのメイン画像"],
    ["XOP技術のビフォー・アフター", "3枚", "技術ページ"],
    ["世界各地の物件（ドバイ・ハワイ等）", "4枚", "実績ページ"],
    ["社長イメージ（会議・対話）", "2枚", "Aboutページ"],
    ["SNS用ビジュアル", "3枚", "Instagram投稿"],
]
tbl3 = Table(table_data3, colWidths=[80*mm, 20*mm, 60*mm])
tbl3.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,-1), "JP"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("TEXTCOLOR", (0,0), (-1,0), OFFWHITE),
    ("GRID", (0,0), (-1,-1), 0.3, GOLD),
    ("PADDING", (0,0), (-1,-1), 5),
    ("LEADING", (0,0), (-1,-1), 15),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#FAFAFA")]),
]))
story.append(tbl3)
story.append(sp(2))
story.append(p("これらは「本物の実績写真が揃うまでの橋渡し」として使います。実績が増えれば順次差し替えていきます。"))

# 7
story.append(hr())
story.append(h1("7. 今後の課題・やること一覧"))
story.append(h2("すぐやること（〜2026年6月）"))
story.append(p("・ロゴ制作 — デザイナーへ発注（ブランドガイドラインを渡す）", bullet_style))
story.append(p("・LinkedIn開設 — 社長本人が開設（プロフィールテキストは準備済み）", bullet_style))
story.append(p("・Webの空欄埋め — 社長名・住所・設立日・メールアドレス・実績数値の確認", bullet_style))
story.append(p("・フォーム連携 — 送信したメールが届くよう設定", bullet_style))
story.append(h2("7月上旬まで"))
story.append(p("・crux-japan.com 取得 — ドメイン購入（年間1,000〜2,000円程度）", bullet_style))
story.append(p("・Vercelにドメイン接続 — 技術作業（30分以内に完了）", bullet_style))
story.append(p("・サイト本公開 — 上記完了後、新URLで公開", bullet_style))
story.append(p("・Instagram開設 — @crux_buildingprotection", bullet_style))
story.append(h2("8月ドバイ展示会まで"))
story.append(p("・英語名刺 — 社長名・肩書き・QRコード（サイトへ）入り", bullet_style))
story.append(p("・A4会社概要（英語） — XOPの仕組み・実績・連絡先", bullet_style))
story.append(p("・写真の差し替え — AI写真から本物の施工写真へ順次更新", bullet_style))

# 8
story.append(hr())
story.append(h1("8. 目指す先"))
story.append(p(
    "2年後のCRUXが目指す姿："
    "世界中に資産を持つ日本人オーナーが、「外壁・建物のことはCRUXに聞く」と思う存在になること。"
))
story.append(p(
    "競合は「現地の業者」ではありません。「信頼できる専門家がいない」という空白が競合です。"
    "その空白に、日本の技術・日本人の誠実さで入り込む——それがCRUXの戦略です。"
))
story.append(p(
    "XOPは今の主力商品ですが、CRUXの本質は「建築資産を守る知識と人脈」です。"
    "将来、XOP以外の技術や工法が生まれても、「CRUXに相談すれば守ってくれる」というポジションがあれば、事業は続きます。"
))
story.append(p(
    "社長が今まで築いてきた「世界中に広がる人脈」と「建築・施工の実績」は、これ以上ない資産です。"
    "今日作ったブランドと仕組みは、その資産を世界に見せるための「舞台」です。"
))

# Appendix
story.append(hr())
story.append(h1("付録：今日作成したファイル一覧"))
files = [
    ("brand-guidelines.md", "デザイナーへの発注書兼ブランド規定（7章・日英）"),
    ("website-copy.md", "全5ページのWebコピー（日英）"),
    ("linkedin-strategy.md", "LinkedInプロフィール文 + 10投稿案"),
    ("instagram-strategy.md", "Instagram運用方針 + 10投稿案"),
    ("photo-prompts-genspark.md", "AI写真生成プロンプト15本"),
    ("PROJECT-INFO.md", "全アカウント・URL・ファイル構成の一元管理"),
    ("website/（Next.jsプロジェクト）", "完成・公開済みのWebサイト本体"),
]
tbl4 = Table(files, colWidths=[65*mm, 95*mm])
tbl4.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,-1), "JP"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("TEXTCOLOR", (0,0), (0,-1), NAVY),
    ("GRID", (0,0), (-1,-1), 0.3, GOLD),
    ("PADDING", (0,0), (-1,-1), 5),
    ("LEADING", (0,0), (-1,-1), 15),
    ("ROWBACKGROUNDS", (0,0), (-1,-1), [colors.white, colors.HexColor("#FAFAFA")]),
]))
story.append(tbl4)
story.append(sp(6))
story.append(p("作成：2026年5月29日　　次回更新予定：ロゴ完成後・ドメイン取得後", note_style))

doc.build(story)
print(f"PDF generated: {OUTPUT}")
