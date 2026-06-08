/**
 * CRUX INBOX API — Google Apps Script
 *
 * 音声メモの整形済みテキストを Drive INBOX に保存するエンドポイント（doPost）と
 * INBOX の日付フォルダ内ファイルを返す読み取りエンドポイント（doGet）を提供する。
 *
 * デプロイ設定:
 *   - 実行するユーザー: 自分 (miyawaki.toshio@gmail.com)
 *   - アクセスできるユーザー: 全員
 *
 * GAS プロジェクト名: CRUX_Inbox_API（XOP_Wiki_API とは別プロジェクト）
 *
 * doPost の action:
 *   "saveInbox"（省略可）    → INBOX/YYYY-MM-DD/{username}_{HHMM}.md に保存
 *   "saveWiki"               → Wiki/日報/{memberName}/YYYY-MM-DD.md に保存（連番対応）
 *   "savePendingTasks"       → Wiki/日報/{memberName}/pending_tasks.md に上書き保存
 *
 * doGet の action:
 *   （省略）                 → INBOX/YYYY-MM-DD/ のファイル一覧
 *   "getPendingTasks"        → Wiki/日報/{memberName}/pending_tasks.md の内容（単一メンバー）
 *   "getAllPendingTasks"     → 全メンバーの pending_tasks.md をまとめて返す（WF4 用）
 */

const INBOX_FOLDER_ID      = '174PXmcgyIvVJaeZnbCk9O_F9NfG3a5l7';
const WIKI_NIPPO_FOLDER_ID = '1nYzOQsIlJYobdFl2QyJPQ_T3_EKbLTqQ'; // Wiki/日報/

// ─────────────────────────────────────────────────────────────────────────────
// POST: ファイル保存エンドポイント
//
// リクエストボディ (JSON):
//   { "username": "yoshioka", "content": "## 2026-05-24 業務メモ\n- ..." }
//
// レスポンス (JSON):
//   { "success": true, "path": "2026-05-24/yoshioka_1430.md", "fileId": "..." }
// ─────────────────────────────────────────────────────────────────────────────
function doPost(e) {
  try {
    const body   = JSON.parse(e.postData.contents);
    const action = body.action || 'saveInbox';

    if (action === 'saveWiki')         return saveWiki(body);
    if (action === 'savePendingTasks') return savePendingTasks(body);
    return saveInbox(body);

  } catch (err) {
    return jsonResponse({ success: false, error: err.message });
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// saveInbox: INBOX/YYYY-MM-DD/{username}_{HHMM}.md に保存
// リクエスト: { username: "yoshioka", content: "..." }
// ─────────────────────────────────────────────────────────────────────────────
function saveInbox(body) {
  const username = (body.username || '').trim();
  const content  = (body.content  || '').trim();

  if (!username || !content) {
    return jsonResponse({ success: false, error: 'username and content are required' });
  }
  if (/[\/\\\.:]/.test(username) || username.length > 50) {
    return jsonResponse({ success: false, error: 'invalid username format' });
  }

  const now     = getNowJST();
  const dateStr = formatDate(now);
  const timeStr = formatTime(now);

  const inboxFolder = DriveApp.getFolderById(INBOX_FOLDER_ID);
  const dateFolder  = getOrCreateFolder(inboxFolder, dateStr);
  const fileName    = `${username}_${timeStr}.md`;

  const existing = dateFolder.getFilesByName(fileName);
  while (existing.hasNext()) existing.next().setTrashed(true);

  const file = dateFolder.createFile(fileName, content, MimeType.PLAIN_TEXT);
  return jsonResponse({ success: true, path: `${dateStr}/${fileName}`, fileId: file.getId() });
}

// ─────────────────────────────────────────────────────────────────────────────
// saveWiki: Wiki/日報/{memberName}/YYYY-MM-DD.md に保存（連番対応）
// リクエスト: { action: "saveWiki", memberName: "吉岡", date: "2026-05-24", content: "..." }
// ─────────────────────────────────────────────────────────────────────────────
function saveWiki(body) {
  const memberName = (body.memberName || '').trim();
  const date       = (body.date       || formatDate(getNowJST())).trim();
  const content    = (body.content    || '').trim();

  if (!memberName || !content) {
    return jsonResponse({ success: false, error: 'memberName and content are required' });
  }

  const nippoFolder  = DriveApp.getFolderById(WIKI_NIPPO_FOLDER_ID);
  const memberFolder = getOrCreateFolder(nippoFolder, memberName);
  const fileName     = resolveFileName(memberFolder, date);

  const file = memberFolder.createFile(fileName, content, MimeType.PLAIN_TEXT);
  return jsonResponse({
    success   : true,
    path      : `日報/${memberName}/${fileName}`,
    fileId    : file.getId(),
    memberName: memberName
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// getPendingTasks: Wiki/日報/{memberName}/pending_tasks.md を読む
// クエリ: ?action=getPendingTasks&memberName=宮脇
// レスポンス: { success, memberName, content, exists }
// ─────────────────────────────────────────────────────────────────────────────
function getPendingTasks(param) {
  const memberName = (param.memberName || '').trim();
  if (!memberName) {
    return jsonResponse({ success: false, error: 'memberName is required' });
  }

  const nippoFolder  = DriveApp.getFolderById(WIKI_NIPPO_FOLDER_ID);
  const memberFolders = nippoFolder.getFoldersByName(memberName);
  if (!memberFolders.hasNext()) {
    return jsonResponse({ success: true, memberName, content: '', exists: false });
  }

  const memberFolder = memberFolders.next();
  const files = memberFolder.getFilesByName('pending_tasks.md');
  if (!files.hasNext()) {
    return jsonResponse({ success: true, memberName, content: '', exists: false });
  }

  const content = files.next().getBlob().getDataAsString('UTF-8');
  return jsonResponse({ success: true, memberName, content, exists: true });
}

// ─────────────────────────────────────────────────────────────────────────────
// savePendingTasks: Wiki/日報/{memberName}/pending_tasks.md を上書き保存
// リクエスト: { action: "savePendingTasks", memberName: "宮脇", content: "- [ ] ..." }
// content が空の場合はファイルを削除（タスクなし状態）
// ─────────────────────────────────────────────────────────────────────────────
function savePendingTasks(body) {
  const memberName = (body.memberName || '').trim();
  const content    = (body.content    || '').trim();

  if (!memberName) {
    return jsonResponse({ success: false, error: 'memberName is required' });
  }

  const nippoFolder  = DriveApp.getFolderById(WIKI_NIPPO_FOLDER_ID);
  const memberFolder = getOrCreateFolder(nippoFolder, memberName);

  // 既存ファイルを削除（上書き）
  const existing = memberFolder.getFilesByName('pending_tasks.md');
  while (existing.hasNext()) existing.next().setTrashed(true);

  if (content.length === 0) {
    return jsonResponse({ success: true, memberName, action: 'cleared' });
  }

  const file = memberFolder.createFile('pending_tasks.md', content, MimeType.PLAIN_TEXT);
  return jsonResponse({
    success   : true,
    memberName: memberName,
    path      : `日報/${memberName}/pending_tasks.md`,
    fileId    : file.getId()
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// getAllPendingTasks: 全メンバーの pending_tasks.md をまとめて返す（WF4 用）
// クエリ: ?action=getAllPendingTasks
// レスポンス: { success, members: { "宮脇": ["- [ ] タスクA", ...], "吉岡": [...] } }
// ─────────────────────────────────────────────────────────────────────────────
function getAllPendingTasks() {
  const nippoFolder = DriveApp.getFolderById(WIKI_NIPPO_FOLDER_ID);
  const members = {};

  const folderIter = nippoFolder.getFolders();
  while (folderIter.hasNext()) {
    const memberFolder = folderIter.next();
    const memberName   = memberFolder.getName();

    const files = memberFolder.getFilesByName('pending_tasks.md');
    if (!files.hasNext()) continue;

    const content = files.next().getBlob().getDataAsString('UTF-8');
    // 未完了タスク（- [ ] ...）のみ抽出
    const tasks = content
      .split('\n')
      .map(l => l.trim())
      .filter(l => /^- \[ \]/.test(l));

    if (tasks.length > 0) {
      members[memberName] = tasks;
    }
  }

  return jsonResponse({ success: true, members });
}

/** 連番ファイル名を解決: YYYY-MM-DD.md / YYYY-MM-DD_2.md / ... */
function resolveFileName(folder, date) {
  const base = `${date}.md`;
  if (!fileExists(folder, base)) return base;
  for (let i = 2; i <= 10; i++) {
    const name = `${date}_${i}.md`;
    if (!fileExists(folder, name)) return name;
  }
  return `${date}_${Date.now()}.md`;
}

function fileExists(folder, name) {
  return folder.getFilesByName(name).hasNext();
}

// ─────────────────────────────────────────────────────────────────────────────
// GET: INBOX 読み取りエンドポイント（ワークフロー #2 用）
//
// クエリパラメータ:
//   ?date=2026-05-24      (省略時は今日の JST 日付)
//   ?username=yoshioka    (省略時は全員)
//
// レスポンス (JSON):
//   { "success": true, "date": "2026-05-24", "files": [
//       { "name": "yoshioka_1430.md", "username": "yoshioka", "content": "..." }
//   ]}
// ─────────────────────────────────────────────────────────────────────────────
function doGet(e) {
  try {
    const param   = e.parameter || {};
    const action  = param.action || '';

    // pending_tasks.md の読み取り（単一メンバー）
    if (action === 'getPendingTasks')    return getPendingTasks(param);
    // 全メンバーの pending_tasks をまとめて返す（WF4 朝ブリーフィング用）
    if (action === 'getAllPendingTasks') return getAllPendingTasks();

    const dateStr        = param.date     || formatDate(getNowJST());
    const filterUsername = param.username || null;

    const inboxFolder = DriveApp.getFolderById(INBOX_FOLDER_ID);

    // 日付フォルダを検索
    const dateFolders = inboxFolder.getFoldersByName(dateStr);
    if (!dateFolders.hasNext()) {
      return jsonResponse({ success: true, date: dateStr, files: [] });
    }
    const dateFolder = dateFolders.next();

    // ファイル一覧取得
    const files = [];
    const fileIterator = dateFolder.getFiles();
    while (fileIterator.hasNext()) {
      const file = fileIterator.next();
      const name = file.getName();
      if (!name.endsWith('.md')) continue;

      // username フィルタ（指定があれば一致するもののみ）
      const username = name.replace(/_\d{4}\.md$/, '');
      if (filterUsername && username !== filterUsername) continue;

      files.push({
        name    : name,
        username: username,
        content : file.getBlob().getDataAsString('UTF-8'),
        fileId  : file.getId()
      });
    }

    // ファイル名昇順（時刻順）
    files.sort((a, b) => a.name.localeCompare(b.name));

    return jsonResponse({ success: true, date: dateStr, files: files });

  } catch (err) {
    return jsonResponse({ success: false, error: err.message });
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// ユーティリティ
// ─────────────────────────────────────────────────────────────────────────────

/** UTC+9 に補正した Date を返す（GAS タイムゾーン設定に依存しない） */
function getNowJST() {
  const now = new Date();
  return new Date(now.getTime() + 9 * 60 * 60 * 1000);
}

/** Date → "YYYY-MM-DD" (UTC 基準で読む ← getNowJST() 使用前提) */
function formatDate(d) {
  const y   = d.getUTCFullYear();
  const m   = String(d.getUTCMonth() + 1).padStart(2, '0');
  const day = String(d.getUTCDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

/** Date → "HHMM" */
function formatTime(d) {
  const h   = String(d.getUTCHours()).padStart(2, '0');
  const min = String(d.getUTCMinutes()).padStart(2, '0');
  return `${h}${min}`;
}

/** フォルダが存在すれば返し、なければ作成して返す */
function getOrCreateFolder(parent, name) {
  const existing = parent.getFoldersByName(name);
  if (existing.hasNext()) return existing.next();
  return parent.createFolder(name);
}

/** JSON レスポンスを返す */
function jsonResponse(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

// ─────────────────────────────────────────────────────────────────────────────
// 動作確認用（GAS エディタから直接実行）
// ─────────────────────────────────────────────────────────────────────────────

function testDoPost() {
  const mockEvent = {
    postData: {
      contents: JSON.stringify({
        username: 'testuser',
        content : '## テスト日報\n\n- 午前: 顧客 A 訪問\n- 午後: 見積書作成\n'
      })
    }
  };
  const result = doPost(mockEvent);
  console.log(result.getContent());
}

function testDoGet() {
  const result = doGet({ parameter: {} });
  console.log(result.getContent());
}

function testDoGetByUser() {
  const result = doGet({ parameter: { username: 'testuser' } });
  console.log(result.getContent());
}

function testSaveWiki() {
  const mock = {
    postData: { contents: JSON.stringify({
      action    : 'saveWiki',
      memberName: '吉岡',
      date      : '2026-05-24',
      content   : '## 2026-05-24 日報 — 吉岡\n\n### 本日の活動\n- XOP 提案\n'
    })}
  };
  console.log(doPost(mock).getContent());
}
