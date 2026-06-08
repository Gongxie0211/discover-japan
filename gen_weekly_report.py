#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRUX/XOP 週次レポートPDF生成スクリプト
- 案件アップデート依頼（期限超過・やばいDeal）
- タスクアップデート依頼（期限超過・未完了Task）
出力先: ~/Documents/AIMemory/crux/YYYY-MM-DD_*.pdf

使い方:
  python3 gen_weekly_report.py          # 本日日付で生成
  python3 gen_weekly_report.py 2026-06-08  # 指定日付で生成
"""

import sys
import json
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── 設定 ────────────────────────────────────────────
NOCODB_TOKEN   = "nc_pat_X4viBFETV6ysHcupzJgei5enTIh2aFOds7mQPfV9"
NOCODB_BASE    = "https://app.nocodb.com"
BASE_ID        = "pj7eh38xeqjhasz"
TABLE_DEAL     = "m4dt4qlrw9ag6k0"
TABLE_TASKS    = "m83uxghrdtij7gc"
OUT_DIR        = Path(__file__).parent

# ── フォント ─────────────────────────────────────────
FONT = 'HeiseiKakuGo-W5'
pdfmetrics.registerFont(UnicodeCIDFont(FONT))

# ── カラー ───────────────────────────────────────────
NAVY   = colors.HexColor('#1A3A5C')
RED    = colors.HexColor('#C0392B')
DKRED  = colors.HexColor('#922B21')
ORANGE = colors.HexColor('#E67E22')
BLUE   = colors.HexColor('#2980B9')
GREEN  = colors.HexColor('#27AE60')
PURPLE = colors.HexColor('#8E44AD')
YELLOW = colors.HexColor('#F39C12')
GRAY   = colors.HexColor('#7F8C8D')
LGRAY  = colors.HexColor('#ECF0F1')
WHITE  = colors.white

PAGE_W, PAGE_H = A4
ML = MR = 18*mm
MT = MB = 16*mm

# ────────────────────────────────────────────────────
# ヘルパー
# ────────────────────────────────────────────────────

def S(fontSize=9, textColor=colors.black, leading=None, leftIndent=0, alignment=TA_LEFT):
    return ParagraphStyle('_', fontName=FONT, fontSize=fontSize, textColor=textColor,
                          leading=leading or fontSize*1.55, leftIndent=leftIndent,
                          alignment=alignment, wordWrap='CJK')

def badge(text, bg, fg=WHITE, fs=7.5):
    return Paragraph(f'<b> {text} </b>',
        ParagraphStyle('b', fontName=FONT, fontSize=fs, textColor=fg, backColor=bg,
                       leading=fs*1.6, alignment=TA_CENTER, wordWrap='CJK',
                       borderPadding=(2,3,2,3)))

def days_diff(due_str, today_str):
    d1 = date.fromisoformat(due_str[:10])
    d2 = date.fromisoformat(today_str)
    return (d2 - d1).days

def is_new_this_week(due_str, today_str):
    """期限が今週（過去7日以内）に超過したか = 🆕 新規"""
    due = date.fromisoformat(due_str[:10])
    today = date.fromisoformat(today_str)
    week_ago = today - timedelta(days=7)
    return week_ago <= due < today

def continuity_badge(due_str, today_str):
    """🆕 今週新規 / 🔁 前回継続 のバッジ情報を返す"""
    if is_new_this_week(due_str, today_str):
        return '🆕 今週新規', colors.HexColor('#1ABC9C')   # teal
    else:
        od = days_diff(due_str, today_str)
        weeks = od // 7
        label = f'🔁 {weeks}週継続' if weeks > 1 else '🔁 前回継続'
        return label, colors.HexColor('#95A5A6')           # gray

def noco_fetch_all(table_id):
    """NocoDB API から全レコードを取得"""
    headers = {'xc-token': NOCODB_TOKEN, 'Content-Type': 'application/json'}
    all_rows, offset = [], 0
    while True:
        url = f"{NOCODB_BASE}/api/v1/db/data/noco/{BASE_ID}/{table_id}?limit=100&offset={offset}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        rows = data.get('list', [])
        all_rows.extend(rows)
        total = data.get('pageInfo', {}).get('totalRows', 0)
        if len(all_rows) >= total:
            break
        offset += 100
    return all_rows


# ────────────────────────────────────────────────────
# Deal PDF
# ────────────────────────────────────────────────────

DEAL_PRI_COLORS = {'最優先': RED, 'AA': DKRED, 'A': ORANGE, '高': BLUE, 'B': PURPLE, '中': YELLOW, 'C': GRAY, '低': GREEN}
DEAL_PRI_LABELS = {'最優先': '🔴 最優先', 'AA': '🔴 AA', 'A': '🟠 A', '高': '🔵 高', 'B': '🟣 B', '中': '🟡 中', 'C': '⚫ C', '低': '🟢 低'}
DEAL_PHASE_COLORS = {
    '①初接触':  colors.HexColor('#1ABC9C'),
    '②提案中':  colors.HexColor('#3498DB'),
    '③見積提出': colors.HexColor('#9B59B6'),
    '④交渉中':  colors.HexColor('#E67E22'),
    '⑤FIX直前': colors.HexColor('#E74C3C'),
    '⑥施工中':  colors.HexColor('#27AE60'),
    '⑦完了':    GRAY,
}

def get_stale_deals(today_str):
    from datetime import datetime, timedelta
    rows = noco_fetch_all(TABLE_DEAL)
    done_phases = ['⑦完了', '失注', '不要']
    today_dt = datetime.fromisoformat(today_str)
    two_weeks_ago = (today_dt - timedelta(days=14)).strftime('%Y-%m-%d')
    result = []
    for r in rows:
        if r.get('フェーズ') in done_phases:
            continue
        next_contact = r.get('次回コンタクト予定日') or ''
        last_contact = r.get('最終コンタクト日') or ''
        # 次回コンタクト予定日が今日より前
        if next_contact and next_contact[:10] < today_str:
            result.append(r)
            continue
        # 最終コンタクトが2週間以上前（次回未設定の場合）
        if not next_contact and last_contact and last_contact[:10] < two_weeks_ago:
            result.append(r)
    # 優先度順ソート
    pri_order = {'AA':0,'最優先':1,'A':2,'高':3,'B':4,'中':5,'C':6,'低':7}
    result.sort(key=lambda r: (pri_order.get(r.get('優先度',''), 9),
                               r.get('次回コンタクト予定日') or '9999'))
    return result[:10]

def build_deal_card(r, today_str):
    elems = []
    did = r.get('D-ID') or f"D-{r['Id']}"
    phase = r.get('フェーズ', '')
    priority = r.get('優先度', '')
    # 営業担当名はリスト形式の場合がある
    staff_raw = r.get('営業担当名') or r.get('担当者') or ''
    staff = '・'.join(staff_raw) if isinstance(staff_raw, list) else str(staff_raw)
    deal_name = r.get('Deal名', '') or ''
    company = r.get('会社名', '') or ''
    next_contact = r.get('次回コンタクト予定日') or ''
    last_contact = r.get('最終コンタクト日') or ''
    next_action = r.get('次回アクション') or ''
    profit = r.get('予想利益') or ''
    notes = r.get('備考') or ''

    pri_color = DEAL_PRI_COLORS.get(priority, GRAY)
    phase_color = DEAL_PHASE_COLORS.get(phase, GRAY)

    # バッジ行: 次回コンタクト予定日の超過日数 + 継続フラグ
    ref_date = next_contact or last_contact or ''
    if next_contact and next_contact[:10] < today_str:
        od = days_diff(next_contact[:10], today_str)
        contact_label = f"次回:{next_contact[5:10].replace('-','/')} ⚠{od}日超過"
        contact_color = RED if od >= 14 else ORANGE
    elif last_contact:
        od = days_diff(last_contact[:10], today_str)
        contact_label = f"最終:{last_contact[5:10].replace('-','/')} {od}日前"
        contact_color = ORANGE if od >= 14 else GRAY
    else:
        contact_label = 'コンタクト未記録'
        contact_color = GRAY

    cont_label, cont_color = continuity_badge(ref_date[:10], today_str) if ref_date else ('🔁 前回継続', colors.HexColor('#95A5A6'))

    bdata = [[
        badge(did, NAVY),
        badge(cont_label, cont_color),
        badge(DEAL_PRI_LABELS.get(priority, priority), pri_color),
        badge(phase, phase_color),
        badge(contact_label, contact_color),
        badge(f"担当:{staff}", NAVY),
    ]]
    bt = Table(bdata, colWidths=[20*mm, 26*mm, 22*mm, 24*mm, 44*mm, 36*mm])
    bt.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LEFTPADDING',(0,0),(-1,-1),2),('RIGHTPADDING',(0,0),(-1,-1),2),
        ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)]))
    elems.append(bt)
    elems.append(Spacer(1,2*mm))

    # タイトル行
    elems.append(Paragraph(f"{deal_name}　{company}", S(10, NAVY)))
    if profit:
        elems.append(Paragraph(f'💰 予想利益: {profit}', S(8, GREEN)))
    elems.append(Spacer(1,1*mm))

    # コンタクト情報・次回アクション
    if last_contact:
        elems.append(Paragraph(f'📅 最終コンタクト: {last_contact[:10]}', S(8, GRAY)))
    if next_action:
        elems.append(Paragraph(f'➡ 次回アクション: {next_action}', S(8, colors.HexColor('#555'))))
    if notes:
        elems.append(Paragraph(f'📌 {notes}', S(7.5, colors.HexColor('#777'))))
    elems.append(Spacer(1,2*mm))

    # 質問
    questions = generate_deal_questions(r, today_str)
    for q in questions:
        elems.append(Paragraph(f'❓ {q}', S(8.5, RED, leftIndent=3*mm)))
        elems.append(Spacer(1,1*mm))

    # 回答欄
    elems.append(Spacer(1,1*mm))
    elems.append(Paragraph('回答・状況メモ：', S(7.5, GRAY)))
    elems.append(HRFlowable(width='100%', thickness=0.5, color=LGRAY))
    elems.append(Spacer(1,3.5*mm))
    elems.append(HRFlowable(width='100%', thickness=0.5, color=LGRAY))
    elems.append(Spacer(1,2*mm))
    return elems

def generate_deal_questions(r, today_str):
    phase = r.get('フェーズ', '')
    next_contact = r.get('次回コンタクト予定日') or ''
    next_action = r.get('次回アクション') or ''
    last_contact = r.get('最終コンタクト日') or ''
    qs = []

    # 次回コンタクト超過
    if next_contact and next_contact[:10] < today_str:
        od = days_diff(next_contact[:10], today_str)
        qs.append(f'次回コンタクト予定日（{next_contact[:10]}）から{od}日経過しています。連絡しましたか？')

    # フェーズ別質問
    if '見積' in phase:
        qs.append('見積提出後の反応はいかがですか？返答・修正依頼はありましたか？')
    elif '提案' in phase:
        qs.append('提案後のお客様の反応を教えてください。次回アポは取れましたか？')
    elif '交渉' in phase or 'FIX' in phase:
        qs.append('交渉の現状を教えてください。契約締結の見込み時期はいつですか？')
    elif '初接触' in phase or '接触' in phase:
        qs.append('初回接触後の状況はいかがですか？次のステップに進めましたか？')
    elif '施工' in phase:
        qs.append('施工の進捗状況を教えてください。完了・追加受注の見込みは？')

    # 次回アクションが未完了
    if next_action and not qs:
        qs.append(f'「{next_action}」は完了しましたか？結果を教えてください。')

    if not qs:
        qs.append('現在の状況と次のアクションを教えてください。')

    qs.append('次回コンタクト予定日と具体的なアクションを更新してください。')
    return qs[:3]

def build_deal_pdf(output_path, today_str):
    print(f"  Dealデータ取得中...")
    deals = get_stale_deals(today_str)
    print(f"  {len(deals)}件のやばいDealを取得")

    doc = SimpleDocTemplate(output_path, pagesize=A4,
        leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
        title=f'案件アップデート依頼 {today_str}')
    story = []

    def deal_ref_date(r):
        return (r.get('次回コンタクト予定日') or r.get('最終コンタクト日') or '')[:10]
    new_count  = sum(1 for r in deals if deal_ref_date(r) and is_new_this_week(deal_ref_date(r), today_str))
    cont_count = len(deals) - new_count

    story.append(Paragraph('⚠ 案件アップデート依頼レポート', S(15, NAVY, alignment=TA_CENTER)))
    story.append(Spacer(1,1.5*mm))
    story.append(Paragraph(
        f'{today_str}　対象: フォロー必要な案件 {len(deals)}件　'
        f'（🆕 今週新規 {new_count}件　／　🔁 前回継続 {cont_count}件）',
        S(8.5, GRAY, alignment=TA_CENTER)))
    story.append(Spacer(1,1*mm))
    story.append(Paragraph('担当者の方は各案件の現状と次のアクションをご回答ください。', S(9, RED, alignment=TA_CENTER)))
    story.append(HRFlowable(width='100%', thickness=1.5, color=NAVY))
    story.append(Spacer(1,3*mm))

    for i, r in enumerate(deals, 1):
        story.append(Paragraph(f'No.{i} / {len(deals)}', S(7.5, GRAY)))
        story.append(Spacer(1,1*mm))
        card_elems = build_deal_card(r, today_str)
        priority = r.get('優先度', '')
        pri_color = DEAL_PRI_COLORS.get(priority, GRAY)
        ct = Table([[card_elems]], colWidths=[PAGE_W - ML - MR])
        ct.setStyle(TableStyle([
            ('BOX',(0,0),(-1,-1),1.5,pri_color),
            ('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#FAFAFA')),
            ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
            ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ]))
        story.append(ct)
        story.append(Spacer(1,4*mm))

    doc.build(story)
    print(f"  ✅ 案件PDF: {output_path}")


# ────────────────────────────────────────────────────
# Task PDF
# ────────────────────────────────────────────────────

TASK_PRI_ORDER  = {'AA':0,'最優先':1,'A':2,'高':3,'B':4,'中':5,'C':6,'低':7}
TASK_PRI_COLORS = {'AA': DKRED,'最優先': RED,'A': ORANGE,'高': BLUE,
                   'B': PURPLE,'中': YELLOW,'C': GRAY,'低': GREEN}
TASK_PRI_LABELS = {'AA':'🔴 AA','最優先':'🔴 最優先','A':'🟠 A','高':'🔵 高',
                   'B':'🟣 B','中':'🟡 中','C':'⚫ C','低':'🟢 低'}
TASK_STATUS_LABELS = {'未着手':'⬜ 未着手','着手':'🔷 着手中','済':'✅ 済'}

TASK_QUESTIONS = {
    'T-039': ['.com/.ae/.sg/.tw の各ドメインは取得済みですか？','IG / X / LinkedIn のアカウントは確保しましたか？','完了予定日を教えてください。'],
    'T-001': ['キーストン社へのメールは送付しましたか？','未送付なら何が止まっていますか？','送付完了の予定日を教えてください。'],
    'T-002': ['価格・MOQの社内合意はとれていますか？','打合せのスケジュールは決まりましたか？','確定予定日を教えてください。'],
    'T-003': ['候補事務所はリストアップしましたか？','初回コンタクトはしましたか？','着手金支払いの目処はいつですか？'],
    'T-038': ['海外出願実績のある特許事務所を探しましたか？','1社でも問い合わせしましたか？','契約締結の目処を教えてください。'],
    'T-048': ['競争参加資格の必要条件を確認しましたか？','外為法・安保貿管の自社適用範囲は把握していますか？','次の具体的アクションと担当者を教えてください。'],
    'T-049': ['NocoDB/クラウドツールへの機密情報格納は許可されますか？','社内情報管理ルールの草案はありますか？','ルール確定の目処はいつですか？'],
    'T-060': ['現在の各部門の人数と不足数を把握していますか？','採用開始の目標時期は決まりましたか？','採用計画書のドラフトはいつ出せますか？'],
}

def get_overdue_tasks(today_str):
    rows = noco_fetch_all(TABLE_TASKS)
    done = ['済']
    active = [r for r in rows if r.get('ステータス') not in done and r.get('ステータス') is not None]
    overdue = [r for r in active if r.get('期限') and r['期限'][:10] < today_str]
    overdue.sort(key=lambda r: (TASK_PRI_ORDER.get(r.get('優先度',''),9), r.get('期限','9999')))
    return overdue

def get_task_questions(r, today_str):
    tid = r.get('T-ID','')
    if tid in TASK_QUESTIONS:
        return TASK_QUESTIONS[tid]
    # 汎用質問生成
    od = days_diff(r['期限'], today_str)
    status = r.get('ステータス','')
    title = r.get('タスク名','')
    qs = [f'期限（{r["期限"][:10]}）から{od}日経過しています。現在の状況を教えてください。']
    if status == '未着手':
        qs.append('着手できていない理由を教えてください。')
    qs.append('完了予定日を教えてください。')
    return qs[:3]

def build_task_card(r, today_str):
    elems = []
    tid = r.get('T-ID', f"T-{r['Id']}")
    priority = r.get('優先度','')
    status = r.get('ステータス','')
    due = r['期限'][:10]
    od = days_diff(due, today_str)
    assignee = r.get('担当','')
    title = r.get('タスク名','')
    phase = r.get('フェーズ','')
    project = r.get('所属プロジェクト','')
    notes = r.get('備考','') or ''

    pri_color = TASK_PRI_COLORS.get(priority, GRAY)
    due_label = f"期限:{due[5:].replace('-','/')}  ⚠{od}日超過"
    cont_label, cont_color = continuity_badge(due, today_str)

    bdata = [[
        badge(tid, NAVY),
        badge(cont_label, cont_color),
        badge(TASK_PRI_LABELS.get(priority, priority), pri_color),
        badge(TASK_STATUS_LABELS.get(status, status), GRAY),
        badge(due_label, RED if od >= 7 else ORANGE),
        badge(f"担当:{assignee}", NAVY),
    ]]
    bt = Table(bdata, colWidths=[20*mm, 26*mm, 24*mm, 24*mm, 44*mm, 36*mm])
    bt.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LEFTPADDING',(0,0),(-1,-1),2),('RIGHTPADDING',(0,0),(-1,-1),2),
        ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)]))
    elems.append(bt)
    elems.append(Spacer(1,2*mm))
    elems.append(Paragraph(title, S(10, NAVY)))
    elems.append(Spacer(1,1*mm))
    elems.append(Paragraph(f'📁 {project}　｜　🗂 {phase}', S(7.5, GRAY)))
    if notes:
        elems.append(Paragraph(f'📌 {notes}', S(7.5, colors.HexColor('#555'))))
    elems.append(Spacer(1,2*mm))

    for q in get_task_questions(r, today_str):
        elems.append(Paragraph(f'❓ {q}', S(8.5, RED, leftIndent=3*mm)))
        elems.append(Spacer(1,1*mm))

    elems.append(Spacer(1,1*mm))
    elems.append(Paragraph('回答・状況メモ：', S(7.5, GRAY)))
    elems.append(HRFlowable(width='100%', thickness=0.5, color=LGRAY))
    elems.append(Spacer(1,3.5*mm))
    elems.append(HRFlowable(width='100%', thickness=0.5, color=LGRAY))
    elems.append(Spacer(1,2*mm))
    return elems

PROJECT_ORDER = [
    'XOP海外原液販売プロジェクト',
    '海軍・防衛関連プロジェクト',
    'XOP国内販売プロジェクト',
    '建築・建設プロジェクト',
    '社内体制・パートナー戦略プロジェクト',
]
PROJECT_COLORS = {
    'XOP海外原液販売プロジェクト':       colors.HexColor('#1A3A5C'),
    '海軍・防衛関連プロジェクト':         colors.HexColor('#6C3483'),
    'XOP国内販売プロジェクト':           colors.HexColor('#1E8BC3'),
    '建築・建設プロジェクト':             colors.HexColor('#1E8449'),
    '社内体制・パートナー戦略プロジェクト': colors.HexColor('#784212'),
}

def build_task_pdf(output_path, today_str):
    print(f"  Taskデータ取得中...")
    tasks = get_overdue_tasks(today_str)
    print(f"  {len(tasks)}件の期限超過Taskを取得")

    # プロジェクトごとにグループ化
    from collections import defaultdict
    groups = defaultdict(list)
    for r in tasks:
        proj = r.get('所属プロジェクト') or 'その他'
        groups[proj].append(r)

    # 表示順: PROJECT_ORDER の順 → その他
    ordered_projects = [p for p in PROJECT_ORDER if p in groups]
    ordered_projects += [p for p in groups if p not in PROJECT_ORDER]

    new_count  = sum(1 for r in tasks if is_new_this_week(r['期限'][:10], today_str))
    cont_count = len(tasks) - new_count

    doc = SimpleDocTemplate(output_path, pagesize=A4,
        leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
        title=f'タスクアップデート依頼 {today_str}')
    story = []

    # ── ヘッダー
    story.append(Paragraph('⚠ 期限超過タスク 状況確認レポート', S(15, NAVY, alignment=TA_CENTER)))
    story.append(Spacer(1,1.5*mm))
    story.append(Paragraph(
        f'{today_str}　期限超過・未完了タスク {len(tasks)}件　'
        f'（🆕 今週新規 {new_count}件 ／ 🔁 前回継続 {cont_count}件）',
        S(8.5, GRAY, alignment=TA_CENTER)))
    story.append(HRFlowable(width='100%', thickness=1.5, color=NAVY))
    story.append(Spacer(1,2*mm))

    # ── メンバーへの注意書き
    notice_items = [
        '各タスクの現状を記入し、写真を撮って返送してください。',
        '担当・優先度・ステータスに変更がある場合も教えてください。\n印刷→写メでもOKです。T-XXXの番号だけでも構いません。',
        '自分のタスクが載っていない場合 → NocoDBにタスク・優先度・ステータス・担当者が未登録の可能性があります。\nお互いの状況が見えるよう、必ず登録してください。',
    ]
    notice_table_data = []
    for item in notice_items:
        notice_table_data.append([
            Paragraph('●', S(8.5, NAVY)),
            Paragraph(item, S(8.5, colors.HexColor('#333'))),
        ])
    notice_table = Table(notice_table_data, colWidths=[5*mm, PAGE_W - ML - MR - 5*mm])
    notice_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ]))

    notice_box = Table([[notice_table]], colWidths=[PAGE_W - ML - MR])
    notice_box.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, ORANGE),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFBF0')),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(notice_box)
    story.append(Spacer(1,4*mm))

    # ── プロジェクト別タスク
    total_no = 0
    for proj in ordered_projects:
        proj_tasks = groups[proj]
        proj_color = PROJECT_COLORS.get(proj, NAVY)

        # プロジェクトヘッダー
        proj_new = sum(1 for r in proj_tasks if is_new_this_week(r['期限'][:10], today_str))
        proj_cont = len(proj_tasks) - proj_new
        header_data = [[
            Paragraph(f'📁 {proj}', S(10, WHITE)),
            Paragraph(
                f'{len(proj_tasks)}件  🆕{proj_new}  🔁{proj_cont}',
                S(8.5, colors.HexColor('#DDDDDD'), alignment=TA_CENTER)),
        ]]
        header_table = Table(header_data, colWidths=[PAGE_W - ML - MR - 40*mm, 40*mm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), proj_color),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(header_table)
        story.append(Spacer(1,2*mm))

        for r in proj_tasks:
            total_no += 1
            story.append(Paragraph(f'No.{total_no} / {len(tasks)}', S(7, GRAY)))
            story.append(Spacer(1,0.5*mm))
            card_elems = build_task_card(r, today_str)
            priority = r.get('優先度','')
            pri_color = TASK_PRI_COLORS.get(priority, GRAY)
            ct = Table([[card_elems]], colWidths=[PAGE_W - ML - MR])
            ct.setStyle(TableStyle([
                ('BOX',(0,0),(-1,-1),1.5,pri_color),
                ('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#FAFAFA')),
                ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
                ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
            ]))
            story.append(ct)
            story.append(Spacer(1,3*mm))

        story.append(Spacer(1,3*mm))

    doc.build(story)
    print(f"  ✅ タスクPDF: {output_path}")


# ────────────────────────────────────────────────────
# メイン
# ────────────────────────────────────────────────────

if __name__ == '__main__':
    today_str = sys.argv[1] if len(sys.argv) > 1 else date.today().strftime('%Y-%m-%d')
    print(f"📅 レポート対象日: {today_str}")

    deal_path = OUT_DIR / f"{today_str}_案件アップデート依頼.pdf"
    task_path = OUT_DIR / f"{today_str}_タスクアップデート依頼.pdf"
    dep_path  = OUT_DIR / f"{today_str}_タスク依存関係マップ.pdf"

    print("\n📋 案件レポート生成中...")
    build_deal_pdf(str(deal_path), today_str)

    print("\n📋 タスクレポート生成中...")
    build_task_pdf(str(task_path), today_str)

    print("\n🔗 依存関係マップ生成中...")
    from gen_dependency_map import build_dependency_pdf
    build_dependency_pdf(str(dep_path), today_str)

    print(f"\n✅ 完了！")
    print(f"   {deal_path}")
    print(f"   {task_path}")
    print(f"   {dep_path}")
