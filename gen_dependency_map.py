#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRUX タスク依存関係マップ PDF生成
毎週 NocoDB から最新ステータスを取得し、
ブロッカーと依存チェーンをカラーコードで可視化する。
"""

import json
import urllib.request
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── 設定 ────────────────────────────────────────────
NOCODB_TOKEN = "nc_pat_X4viBFETV6ysHcupzJgei5enTIh2aFOds7mQPfV9"
NOCODB_BASE  = "https://app.nocodb.com"
BASE_ID      = "pj7eh38xeqjhasz"
TABLE_TASKS  = "m83uxghrdtij7gc"
OUT_DIR      = Path(__file__).parent

FONT = 'HeiseiKakuGo-W5'
pdfmetrics.registerFont(UnicodeCIDFont(FONT))

PAGE_W, PAGE_H = A4
ML = MR = 18 * mm
MT = MB = 14 * mm
CONTENT_W = PAGE_W - ML - MR   # ≈ 174mm

# ── カラー ───────────────────────────────────────────
NAVY    = colors.HexColor('#1A3A5C')
RED     = colors.HexColor('#C0392B')
DKRED   = colors.HexColor('#8B0000')
ORANGE  = colors.HexColor('#D35400')
BLUE    = colors.HexColor('#2471A3')
GREEN   = colors.HexColor('#1E8449')
YELLOW  = colors.HexColor('#B7950B')
GRAY    = colors.HexColor('#717D7E')
LGRAY   = colors.HexColor('#ECF0F1')
WHITE   = colors.white
BLACK   = colors.black

C_DONE    = colors.HexColor('#D5F5E3')  # 完了 背景
C_INPROG  = colors.HexColor('#D6EAF8')  # 進行中 背景
C_WAITING = colors.HexColor('#FDEBD0')  # 着手待ち 背景
C_BLOCK   = colors.HexColor('#FADBD8')  # ブロッカー 背景

BD_DONE    = colors.HexColor('#27AE60')
BD_INPROG  = colors.HexColor('#2980B9')
BD_WAITING = colors.HexColor('#E67E22')
BD_BLOCK   = colors.HexColor('#C0392B')

STATUS_DONE    = {'済', '完了'}
STATUS_INPROG  = {'着手', '進行中', '着手中'}
STATUS_WAITING = {'未着手'}

# ── 依存チェーン定義 ─────────────────────────────────
# 各チェーンは (task_id または "→" / "+" / テキスト) のリスト
# blocker=True のタスクは赤枠で強調表示

DEPENDENCY_CHAINS = [
    # ======= XOP海外原液販売 =======
    {
        'project': '🌏 XOP海外原液販売プロジェクト',
        'proj_color': colors.HexColor('#1A3A5C'),
        'chains': [
            {
                'title': '⛓ 法務・契約チェーン',
                'rows': [
                    # row: list of (tid_or_label, blocker_flag)
                    [('T-003', True), ('→',), ('T-007',)],
                    [('T-006', False), ('→',), ('T-007 へ合流',)],
                    [('T-002', False), ('→',), ('MOQ社内確定',), ('→',), ('T-007 へ合流',)],
                ],
                'note': '⚡ T-003（弁護士選定）が未着手のままT-007に着手不可。T-006ドラフト・T-002価格は完了済み。MOQ数量・契約期間・遅延利息率の社内確定も並行要。',
                'note_level': 'danger',
            },
            {
                'title': '⛓ 商標チェーン',
                'rows': [
                    [('T-038', True), ('→',), ('T-041',)],
                ],
                'note': 'T-038（弁理士選定）が完了すれば T-041 マドリッド出願に即着手可能。',
                'note_level': 'warn',
            },
            {
                'title': '⛓ ブランド・ドキュメント（独立着手可）',
                'rows': [
                    [('T-039',), ('→',), ('独立着手可',)],
                    [('T-040',), ('→',), ('独立着手可',)],
                    [('T-008',), ('→',), ('T-009',), ('→',), ('T-011',)],
                ],
                'note': 'T-039・T-040 は他タスクに依存しない。今すぐ着手できる。',
                'note_level': 'ok',
            },
        ],
    },

    # ======= XOP国内代理店 =======
    {
        'project': '🏪 XOP国内代理店プロジェクト',
        'proj_color': colors.HexColor('#4A235A'),
        'chains': [
            {
                'title': '⛓ チェーンA 契約・スキーム（5件連鎖）',
                'rows': [
                    [('T-104 ✅',), ('→',), ('T-107',), ('→',), ('T-109',), ('→',), ('T-112',), ('→',), ('T-116',), ('→',), ('T-118',)],
                ],
                'note': '⚡ T-107（進行中）の完成待ちで T-109 以降4件が全停止。T-107 完成 → 社長承認 → T-109 着手 の流れ。',
                'note_level': 'danger',
            },
            {
                'title': '⛓ チェーンB 認定制度（8件連鎖 ← T-107解除で全解放）',
                'rows': [
                    [('T-111 ✅',), ('+',), ('T-109',), ('→',), ('T-117',), ('→',), ('T-119',), ('→',), ('T-120',), ('→',), ('T-122',), ('→',), ('T-123',), ('→',), ('T-124',), ('→',), ('T-125',)],
                    [('',), ('',), ('T-117',), ('→',), ('T-121',), ('→',), ('T-120 へ',)],
                ],
                'note': '⚡ T-109（代理店契約書ドラフト）が開始されるまでこの8件は手がつけられない。T-107 → T-109 の解除が最優先。',
                'note_level': 'danger',
            },
            {
                'title': '⛓ チェーンC 提案資料（T-104確定済みで今すぐ着手可）',
                'rows': [
                    [('T-104 ✅',), ('→',), ('T-106',), ('→',), ('今すぐ作成可',)],
                    [('T-104 ✅',), ('→',), ('T-110',), ('→',), ('今すぐ作成可',)],
                ],
                'note': '✅ T-104・T-111・T-114 が完了済みのため T-106・T-110 は今すぐ着手できる。',
                'note_level': 'ok',
            },
        ],
    },

    # ======= XOP国内販売テンプレート =======
    {
        'project': '🏠 XOP国内販売プロジェクト（テンプレート段階依存）',
        'proj_color': colors.HexColor('#1A5276'),
        'chains': [
            {
                'title': '⛓ 営業プロセス 7段階 依存構造',
                'rows': [
                    [('①初接触\nT-079,080,081',), ('→',), ('②提案中\nT-082,083,084',), ('→',), ('③見積提出\nT-085,086,087',), ('→',), ('④交渉中\nT-088,089,090',)],
                    [('④交渉中',), ('→',), ('⑤Fix直前\nT-091〜094',), ('→',), ('⑥施工中\nT-095〜098',), ('→',), ('⑦完了\nT-099〜103',)],
                ],
                'note': 'T-078（国内方針決め・進行中）の確定後、①②から着手可能。テンプレートは段階をまたいで並行作成OK。',
                'note_level': 'warn',
            },
        ],
    },

    # ======= 海軍・防衛 =======
    {
        'project': '🛡 海軍・防衛関連プロジェクト',
        'proj_color': colors.HexColor('#4A4A4A'),
        'chains': [
            {
                'title': '⛓ 基盤整備 → 運用ルール',
                'rows': [
                    [('T-048',), ('→',), ('T-049',), ('→',), ('クラウド使用可否確定',)],
                ],
                'note': 'T-049（機密保持ルール）確定までNocoDB等クラウドツールへの機密情報登録可否が不明。プロジェクト全体の情報管理に影響。',
                'note_level': 'warn',
            },
        ],
    },

    # ======= 建築・建設 =======
    {
        'project': '🏗 建築・建設プロジェクト',
        'proj_color': colors.HexColor('#1E5631'),
        'chains': [
            {
                'title': '⛓ 許認可 → 受注活動',
                'rows': [
                    [('T-056',), ('→',), ('建設業許可確認',), ('→',), ('受注活動の前提確定',)],
                ],
                'note': 'T-056 は独立して今すぐ着手可能。建設業許可の有無は他案件にも波及する可能性あり。',
                'note_level': 'warn',
            },
        ],
    },
]

# ── NocoDB タスク取得 ──────────────────────────────────

def fetch_task_statuses():
    """NocoDB から T-ID → {status, name} の辞書を返す"""
    headers = {'xc-token': NOCODB_TOKEN}
    all_rows, offset = [], 0
    while True:
        url = f"{NOCODB_BASE}/api/v1/db/data/noco/{BASE_ID}/{TABLE_TASKS}?limit=100&offset={offset}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        rows = data.get('list', [])
        all_rows.extend(rows)
        if len(all_rows) >= data.get('pageInfo', {}).get('totalRows', 0):
            break
        offset += 100

    result = {}
    for r in all_rows:
        tid = r.get('T-ID', '')
        if tid:
            result[tid] = {
                'status': r.get('ステータス', ''),
                'name':   r.get('タスク名', ''),
            }
    return result

# ── スタイルヘルパー ──────────────────────────────────

def S(fs=9, color=BLACK, leading=None, align=TA_LEFT, indent=0):
    return ParagraphStyle('_', fontName=FONT, fontSize=fs, textColor=color,
                          leading=leading or fs * 1.5, alignment=align,
                          leftIndent=indent, wordWrap='CJK')

def resolve_node_style(cell_text, is_blocker, task_statuses):
    """
    セルのテキストから T-ID を検出し、状態に応じた色を返す。
    (bg_color, border_color, text_color)
    """
    # 矢印・ラベルセル
    if cell_text in ('→', '+', '') or '合流' in cell_text or '着手可' in cell_text or '確定' in cell_text:
        return None, None, None  # 特殊セル

    # T-ID 検出
    import re
    tid_match = re.match(r'(T-\d+)', cell_text)
    if not tid_match:
        # 段階セル（①初接触など）
        return C_WAITING, BD_WAITING, ORANGE

    tid = tid_match.group(1)
    info = task_statuses.get(tid, {})
    status = info.get('status', '')

    if status in STATUS_DONE or '✅' in cell_text:
        return C_DONE, BD_DONE, GREEN
    elif status in STATUS_INPROG:
        return C_INPROG, BD_INPROG, BLUE
    elif is_blocker:
        return C_BLOCK, BD_BLOCK, RED
    else:
        return C_WAITING, BD_WAITING, ORANGE

def make_node_cell(cell_text, is_blocker, task_statuses, w):
    """タスクノードのテーブルセルを返す"""
    if cell_text in ('→', '+'):
        return Paragraph(f'<b>{cell_text}</b>', S(12, GRAY, align=TA_CENTER))
    if cell_text == '':
        return Paragraph('', S(8))

    bg, bd, tc = resolve_node_style(cell_text, is_blocker, task_statuses)

    if bg is None:
        # ラベルセル（合流・着手可など）
        return Paragraph(cell_text, S(7.5, GRAY, align=TA_CENTER))

    # T-ID 検出して名前を補完
    import re
    tid_match = re.match(r'(T-\d+)', cell_text)
    if tid_match:
        tid = tid_match.group(1)
        info = task_statuses.get(tid, {})
        name = info.get('name', '')
        status = info.get('status', '未着手')
        display_status = '✅完了' if status in STATUS_DONE else ('▶進行中' if status in STATUS_INPROG else '⬜未着手')
        # ✅ already in cell_text
        if '✅' in cell_text:
            display_status = '✅完了'

        inner = Table([
            [Paragraph(f'<b>{tid}</b>', S(7.5, NAVY, align=TA_CENTER))],
            [Paragraph(name[:14] + ('…' if len(name) > 14 else ''), S(6.5, BLACK, align=TA_CENTER))],
            [Paragraph(display_status, S(6.5, tc, align=TA_CENTER))],
        ], colWidths=[w - 4])
    else:
        # 段階セル
        inner = Table([
            [Paragraph(cell_text.replace('\n', '<br/>'), S(7, BLACK, align=TA_CENTER))],
        ], colWidths=[w - 4])

    inner.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))

    outer = Table([[inner]], colWidths=[w])
    border_w = 2.0 if is_blocker else 1.5
    outer.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), border_w, bd),
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    return outer


def render_chain_row(row_cells, task_statuses, blockers):
    """
    1行のチェーンを横並びのテーブルとして描画する。
    row_cells: list of (text,) or (text, blocker_flag)
    """
    ARROW_W   = 8 * mm
    LABEL_W   = 22 * mm
    NODE_W    = 26 * mm

    cells = []
    col_widths = []

    for item in row_cells:
        text       = item[0]
        is_blocker = (len(item) > 1 and item[1]) or (text.split()[0] if text else '') in blockers

        if text in ('→', '+'):
            cells.append(make_node_cell(text, False, task_statuses, ARROW_W))
            col_widths.append(ARROW_W)
        elif text == '':
            cells.append(Paragraph('', S(8)))
            col_widths.append(NODE_W)
        elif '合流' in text or '着手可' in text or '確定' in text or '前提' in text:
            cells.append(make_node_cell(text, False, task_statuses, LABEL_W))
            col_widths.append(LABEL_W)
        else:
            cells.append(make_node_cell(text, is_blocker, task_statuses, NODE_W))
            col_widths.append(NODE_W)

    # 合計幅がCONTENT_Wを超える場合は最後のセルを伸ばす
    total = sum(col_widths)
    if total < CONTENT_W and col_widths:
        col_widths[-1] += CONTENT_W - total

    t = Table([cells], colWidths=col_widths)
    t.setStyle(TableStyle([
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING',  (0,0), (-1,-1), 1),
        ('RIGHTPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING',   (0,0), (-1,-1), 2),
        ('BOTTOMPADDING',(0,0), (-1,-1), 2),
    ]))
    return t


# ── ブロッカーサマリー ───────────────────────────────

CRITICAL_BLOCKERS = [
    {
        'tid':    'T-003',
        'name':   '国際法務弁護士の選定・着手金支払い',
        'blocks': ['T-007', 'NDA V4'],
        'owner':  '宮脇',
    },
    {
        'tid':    'T-107',
        'name':   '契約スキーム説明資料（進行中）',
        'blocks': ['T-109→T-112→T-116→T-118', 'T-117→T-125（計11件）'],
        'owner':  '吉岡＋宮脇',
    },
    {
        'tid':    'T-038',
        'name':   '国際商標弁理士の選定・契約',
        'blocks': ['T-041'],
        'owner':  '宮脇',
    },
    {
        'tid':    '社内確定',
        'name':   'MOQ数量・契約期間・遅延利息率',
        'blocks': ['T-007 弁護士送付'],
        'owner':  '吉岡＋宮脇',
    },
]

def build_blocker_summary(task_statuses):
    """ブロッカーサマリーボックス"""
    elems = []
    rows = []
    for b in CRITICAL_BLOCKERS:
        tid  = b['tid']
        info = task_statuses.get(tid, {})
        status = info.get('status', '未着手')
        resolved = status in STATUS_DONE
        status_label = '✅ 解決済' if resolved else '🔴 未解決'
        status_color = GREEN if resolved else RED

        blocks_str = ' / '.join(b['blocks'])
        rows.append([
            Paragraph(f"<b>{tid}</b>", S(8, NAVY if resolved else DKRED, align=TA_CENTER)),
            Paragraph(b['name'], S(8, BLACK)),
            Paragraph(f"→ {blocks_str}", S(7.5, GRAY)),
            Paragraph(b['owner'], S(7.5, GRAY, align=TA_CENTER)),
            Paragraph(f"<b>{status_label}</b>", S(8, status_color, align=TA_CENTER)),
        ])

    header = [
        Paragraph('タスクID',  S(7.5, WHITE, align=TA_CENTER)),
        Paragraph('ブロッカー', S(7.5, WHITE)),
        Paragraph('ブロックしているタスク', S(7.5, WHITE)),
        Paragraph('担当',       S(7.5, WHITE, align=TA_CENTER)),
        Paragraph('状態',       S(7.5, WHITE, align=TA_CENTER)),
    ]

    col_w = [22*mm, 50*mm, 62*mm, 20*mm, 20*mm]
    t = Table([header] + rows, colWidths=col_w)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFF5F5'), colors.HexColor('#FFFFFF')]),
        ('BOX',     (0,0), (-1,-1), 1, GRAY),
        ('GRID',    (0,0), (-1,-1), 0.3, LGRAY),
        ('VALIGN',  (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING',   (0,0), (-1,-1), 4),
        ('RIGHTPADDING',  (0,0), (-1,-1), 4),
    ]))
    elems.append(t)
    return elems


# ── メイン PDF ビルダー ───────────────────────────────

BLOCKER_TIDS = {'T-003', 'T-038', 'T-107', 'T-078', 'T-048'}

NOTE_STYLES = {
    'danger': (colors.HexColor('#F9EBEA'), RED),
    'warn':   (colors.HexColor('#FEF9E7'), YELLOW),
    'ok':     (colors.HexColor('#EAFAF1'), GREEN),
}

def build_dependency_pdf(output_path, today_str):
    print("  依存関係マップデータ取得中...")
    task_statuses = fetch_task_statuses()
    print(f"  {len(task_statuses)} タスクのステータスを取得")

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
        title=f'タスク依存関係マップ {today_str}'
    )
    story = []

    # ── タイトル
    story.append(Paragraph('🔗 タスク依存関係マップ', S(16, NAVY, align=TA_CENTER)))
    story.append(Spacer(1, 1.5*mm))
    story.append(Paragraph(
        f'{today_str}　／　①が決まらないと②が決められない依存チェーンの可視化',
        S(8.5, GRAY, align=TA_CENTER)
    ))
    story.append(Spacer(1, 1*mm))
    story.append(HRFlowable(width='100%', thickness=1.5, color=NAVY))
    story.append(Spacer(1, 3*mm))

    # ── 凡例
    legend_data = [[
        Paragraph('■ 完了', S(8, GREEN)),
        Paragraph('■ 進行中', S(8, BLUE)),
        Paragraph('■ 未着手（着手待ち）', S(8, ORANGE)),
        Paragraph('■ ブロッカー', S(8, RED)),
        Paragraph('→ 依存の向き', S(8, GRAY)),
    ]]
    lt = Table(legend_data, colWidths=[25*mm, 25*mm, 40*mm, 35*mm, 35*mm])
    lt.setStyle(TableStyle([
        ('VALIGN', (0,0),(-1,-1),'MIDDLE'),
        ('LEFTPADDING', (0,0),(-1,-1), 4),
        ('TOPPADDING', (0,0),(-1,-1), 2),
        ('BOTTOMPADDING', (0,0),(-1,-1), 2),
        ('BOX', (0,0),(-1,-1), 0.5, LGRAY),
        ('BACKGROUND', (0,0),(-1,-1), colors.HexColor('#F8F9FA')),
    ]))
    story.append(lt)
    story.append(Spacer(1, 4*mm))

    # ── ブロッカーサマリー
    story.append(Paragraph('⚠ 最優先ブロッカー一覧', S(11, RED)))
    story.append(Spacer(1, 1.5*mm))
    story.extend(build_blocker_summary(task_statuses))
    story.append(Spacer(1, 5*mm))

    # ── プロジェクト別チェーン
    for proj_def in DEPENDENCY_CHAINS:
        proj_title = proj_def['project']
        proj_color = proj_def['proj_color']

        # プロジェクトヘッダー
        ph = Table([[Paragraph(proj_title, S(10.5, WHITE))]], colWidths=[CONTENT_W])
        ph.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(-1,-1), proj_color),
            ('LEFTPADDING', (0,0),(-1,-1), 8),
            ('TOPPADDING', (0,0),(-1,-1), 5),
            ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ]))
        story.append(ph)
        story.append(Spacer(1, 2*mm))

        for chain_def in proj_def['chains']:
            chain_title = chain_def['title']
            rows        = chain_def['rows']
            note        = chain_def.get('note', '')
            note_level  = chain_def.get('note_level', 'warn')

            block_elems = []

            # チェーンタイトル
            block_elems.append(Paragraph(chain_title, S(8.5, NAVY)))
            block_elems.append(Spacer(1, 1.5*mm))

            # 各行を描画
            for row in rows:
                block_elems.append(render_chain_row(row, task_statuses, BLOCKER_TIDS))
                block_elems.append(Spacer(1, 2*mm))

            # ノート
            if note:
                nc, _ = NOTE_STYLES.get(note_level, NOTE_STYLES['warn'])
                _, nc_border = NOTE_STYLES.get(note_level, NOTE_STYLES['warn'])
                note_t = Table(
                    [[Paragraph(note, S(7.5, BLACK))]], colWidths=[CONTENT_W - 8*mm]
                )
                note_t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0),(-1,-1), nc),
                    ('BOX', (0,0),(-1,-1), 0.75, nc_border),
                    ('LEFTPADDING', (0,0),(-1,-1), 5),
                    ('RIGHTPADDING', (0,0),(-1,-1), 5),
                    ('TOPPADDING', (0,0),(-1,-1), 4),
                    ('BOTTOMPADDING', (0,0),(-1,-1), 4),
                ]))
                block_elems.append(note_t)

            block_elems.append(Spacer(1, 4*mm))

            try:
                story.append(KeepTogether(block_elems))
            except Exception:
                story.extend(block_elems)

        story.append(Spacer(1, 3*mm))

    # ── フッター：解除ロードマップ
    story.append(HRFlowable(width='100%', thickness=1, color=LGRAY))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('📊 ブロッカー解除ロードマップ（優先順）', S(11, NAVY)))
    story.append(Spacer(1, 2*mm))

    roadmap = [
        [Paragraph('<b>優先</b>',  S(8, WHITE, align=TA_CENTER)),
         Paragraph('<b>解除タスク</b>', S(8, WHITE)),
         Paragraph('<b>解除後に動き出す件数</b>', S(8, WHITE)),
         Paragraph('<b>担当</b>', S(8, WHITE, align=TA_CENTER))],
        [Paragraph('🔴 最優先', S(8, RED)), Paragraph('T-003 弁護士選定', S(8)), Paragraph('T-007・NDA V4', S(8)), Paragraph('宮脇', S(8, align=TA_CENTER))],
        [Paragraph('🔴 最優先', S(8, RED)), Paragraph('T-107 契約スキーム説明資料 完成', S(8)), Paragraph('T-109〜T-118（契約4件）＋T-117〜T-125（認定7件）= 11件', S(8)), Paragraph('吉岡＋宮脇', S(8, align=TA_CENTER))],
        [Paragraph('🟡 高優先', S(8, YELLOW)), Paragraph('T-038 弁理士選定', S(8)), Paragraph('T-041（商標出願）', S(8)), Paragraph('宮脇', S(8, align=TA_CENTER))],
        [Paragraph('🟡 高優先', S(8, YELLOW)), Paragraph('MOQ・契約期間・遅延利息率の社内決定', S(8)), Paragraph('T-007 弁護士送付可能に', S(8)), Paragraph('吉岡＋宮脇', S(8, align=TA_CENTER))],
        [Paragraph('🟢 今すぐ可', S(8, GREEN)), Paragraph('（ブロッカーなし）', S(8)), Paragraph('T-039・T-040・T-056・T-048・T-106・T-110・T-079〜T-083', S(8)), Paragraph('各担当', S(8, align=TA_CENTER))],
    ]

    rt = Table(roadmap, colWidths=[22*mm, 55*mm, 72*mm, 25*mm])
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1),(-1,-1), [colors.HexColor('#FFF0F0'), WHITE, colors.HexColor('#FFFDE7'), colors.HexColor('#FFFDE7'), colors.HexColor('#F0FFF4')]),
        ('BOX',  (0,0),(-1,-1), 1, GRAY),
        ('GRID', (0,0),(-1,-1), 0.3, LGRAY),
        ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0),(-1,-1), 3),
        ('BOTTOMPADDING', (0,0),(-1,-1), 3),
        ('LEFTPADDING',   (0,0),(-1,-1), 4),
        ('RIGHTPADDING',  (0,0),(-1,-1), 4),
    ]))
    story.append(rt)
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        f'Generated {today_str} ／ NocoDB リアルタイムステータス反映',
        S(7, GRAY, align=TA_CENTER)
    ))

    doc.build(story)
    print(f"  ✅ 依存関係マップPDF: {output_path}")


# ── 単体実行 ─────────────────────────────────────────
if __name__ == '__main__':
    import sys
    from datetime import date
    today_str = sys.argv[1] if len(sys.argv) > 1 else date.today().strftime('%Y-%m-%d')
    out = OUT_DIR / f"{today_str}_タスク依存関係マップ.pdf"
    print(f"📅 {today_str}")
    build_dependency_pdf(str(out), today_str)
    print(f"\n✅ 完了: {out}")
