#!/bin/bash
# 週次レポート 自動生成＆Telegram送信スクリプト
# 毎週月曜 05:30 Myanmar時間（= 08:00 JST）に実行

VENV="/Users/gon/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/e1dd8ece-ed08-48b8-9a3e-8cb6b62c1e18/c09b15d1-1017-4c85-b4f7-11876b733615/skills/xlsx/.venv"
SCRIPT_DIR="/Users/gon/Documents/AIMemory/crux"
BOT_TOKEN="8940109810:AAGEWtDv8l3abF748UEH82mzoXLCJIfRf5c"
CHAT_ID="-5163292172"
TODAY=$(date +%Y-%m-%d)
LOG="$SCRIPT_DIR/weekly_report.log"

echo "=== $TODAY $(date +%H:%M) ===" >> "$LOG"

# 1. PDF生成
"$VENV/bin/python3" "$SCRIPT_DIR/gen_weekly_report.py" "$TODAY" >> "$LOG" 2>&1

DEAL_PDF="$SCRIPT_DIR/${TODAY}_案件アップデート依頼.pdf"
TASK_PDF="$SCRIPT_DIR/${TODAY}_タスクアップデート依頼.pdf"
DEP_PDF="$SCRIPT_DIR/${TODAY}_タスク依存関係マップ.pdf"

# 2. ファイル確認
if [ ! -f "$DEAL_PDF" ] || [ ! -f "$TASK_PDF" ] || [ ! -f "$DEP_PDF" ]; then
  echo "❌ PDF生成失敗（存在確認）" >> "$LOG"
  [ ! -f "$DEAL_PDF" ] && echo "  Missing: $DEAL_PDF" >> "$LOG"
  [ ! -f "$TASK_PDF" ] && echo "  Missing: $TASK_PDF" >> "$LOG"
  [ ! -f "$DEP_PDF"  ] && echo "  Missing: $DEP_PDF"  >> "$LOG"
  exit 1
fi

# 3. Telegram送信（テキスト）
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d chat_id="${CHAT_ID}" \
  -d text="📋 週次レポート ${TODAY}（月）

期限超過・フォロー必要な案件・タスクをまとめました。
担当者の方は各項目の現状と完了予定日をご確認・ご回答ください。

🗂 案件アップデート依頼
🗂 タスクアップデート依頼（🆕新規・🔁継続）
🔗 タスク依存関係マップ（ブロッカー＆依存チェーン）" >> "$LOG" 2>&1

# 4. 案件PDF送信
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendDocument" \
  -F chat_id="${CHAT_ID}" \
  -F document=@"${DEAL_PDF}" \
  -F caption="案件アップデート依頼 ${TODAY}" >> "$LOG" 2>&1

# 5. タスクPDF送信
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendDocument" \
  -F chat_id="${CHAT_ID}" \
  -F document=@"${TASK_PDF}" \
  -F caption="タスクアップデート依頼 ${TODAY}" >> "$LOG" 2>&1

# 6. 依存関係マップPDF送信
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendDocument" \
  -F chat_id="${CHAT_ID}" \
  -F document=@"${DEP_PDF}" \
  -F caption="🔗 タスク依存関係マップ ${TODAY}｜ブロッカーと依存チェーンの可視化" >> "$LOG" 2>&1

echo "✅ 完了（3PDF送信）" >> "$LOG"
