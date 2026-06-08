/**
 * 業務メモ Drive API — Google Apps Script
 *
 * doGet:
 *   ?action=listInbox&date=YYYY-MM-DD
 *   ?action=getPendingTasks&username=miyawakiMM
 *   ?action=getAllPendingTasks
 *
 * doPost:
 *   { action: 'saveInbox',        username, date, time, content }
 *   { action: 'saveReport',       username, date, content }
 *   { action: 'savePendingTasks', username, date, tasks: [] }
 *   { action: 'updateHeatmap',    date, submitters: [] }
 *
 * デプロイ設定:
 *   - 実行するユーザー: 自分 (miyawaki.toshio@gmail.com)
 *   - アクセスできるユーザー: 全員
 */

const INBOX_FOLDER_ID       = '174PXmcgyIvVJaeZnbCk9O_F9NfG3a5l7';
const WIKI_NIPPOU_FOLDER_ID = '1nYzOQsIlJYobdFl2QyJPQ_T3_EKbLTqQ';
const HEATMAP_FILE_ID       = '13tMkd0V3przz6tlj5EBHD9mcFVB0om1_';

const MEMBER_MAP = {
  miyawakiMM: '宮脇',
  yoshioka:   '吉岡',
  kobayashi:  '小林',
  takada:     '高田',
  kitashoji:  '北庄司',
};

// ─── ルーター ────────────────────────────────────────────────────────────────

function doGet(e) {
  try {
    const action = (e.parameter.action || '').trim();
    if (action === 'listInbox')       return json(listInboxFiles(e.parameter.date));
    if (action === 'getPendingTasks') return json(getPendingTasks(e.parameter.username));
    if (action === 'getAllPendingTasks') return json(getAllPendingTasks());
    return json({ success: false, error: `Unknown action: ${action}` });
  } catch (err) {
    return json({ success: false, error: err.message });
  }
}

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    const { action } = body;
    if (action === 'saveInbox')        return json(saveInboxFile(body.username, body.date, body.time, body.content));
    if (action === 'saveReport')       return json(saveWikiReport(body.username, body.date, body.content));
    if (action === 'savePendingTasks') return json(savePendingTasks(body.username, body.date, body.tasks));
    if (action === 'updateHeatmap')    return json(updateHeatmap(body.date, body.submitters));
    return json({ success: false, error: `Unknown action: ${action}` });
  } catch (err) {
    return json({ success: false, error: err.message });
  }
}

// ─── INBOX 書き込み（Session 1 用）────────────────────────────────────────────

function saveInboxFile(username, date, time, content) {
  if (!username || !date || !time || !content) {
    return { success: false, error: 'Missing required fields: username, date, time, content' };
  }
  const inboxRoot = DriveApp.getFolderById(INBOX_FOLDER_ID);
  const dateFolders = inboxRoot.getFoldersByName(date);
  const dateFolder = dateFolders.hasNext() ? dateFolders.next() : inboxRoot.createFolder(date);

  const hhmm = time.replace(':', '');
  const filename = `${username}_${hhmm}.md`;
  const oldFiles = dateFolder.getFilesByName(filename);
  while (oldFiles.hasNext()) oldFiles.next().setTrashed(true);

  const created = dateFolder.createFile(filename, content, MimeType.PLAIN_TEXT);
  return { success: true, filename, fileId: created.getId() };
}

// ─── INBOX 読み取り────────────────────────────────────────────────────────────

function listInboxFiles(date) {
  if (!date) return { success: false, error: 'date parameter is required (YYYY-MM-DD)' };
  const inboxRoot = DriveApp.getFolderById(INBOX_FOLDER_ID);
  const dateFolders = inboxRoot.getFoldersByName(date);
  if (!dateFolders.hasNext()) return { success: true, files: [], date, count: 0 };

  const dateFolder = dateFolders.next();
  const files = [];
  const iter = dateFolder.getFiles();
  while (iter.hasNext()) {
    const file = iter.next();
    const name = file.getName();
    if (!name.endsWith('.md')) continue;
    const m = name.match(/^(.+)_(\d{4})\.md$/);
    if (!m) continue;
    files.push({
      filename: name,
      username: m[1],
      time:     `${m[2].slice(0, 2)}:${m[2].slice(2)}`,
      content:  file.getBlob().getDataAsString('UTF-8'),
      fileId:   file.getId(),
    });
  }
  files.sort((a, b) => a.time.localeCompare(b.time));
  return { success: true, files, date, count: files.length };
}

// ─── Wiki/日報 保存────────────────────────────────────────────────────────────

function saveWikiReport(username, date, content) {
  if (!username || !date || !content) {
    return { success: false, error: 'Missing required fields: username, date, content' };
  }
  const nippouRoot = DriveApp.getFolderById(WIKI_NIPPOU_FOLDER_ID);
  const memberName = resolveMemberName(username);
  if (!memberName) return { success: false, error: `Unknown username: ${username}` };

  const memberFolders = nippouRoot.getFoldersByName(memberName);
  const memberFolder = memberFolders.hasNext() ? memberFolders.next() : nippouRoot.createFolder(memberName);

  let filename = `${date}.md`;
  let counter = 1;
  while (memberFolder.getFilesByName(filename).hasNext()) {
    counter++;
    filename = `${date}_${counter}.md`;
  }
  const created = memberFolder.createFile(filename, content, MimeType.PLAIN_TEXT);
  return { success: true, filename, memberName, fileId: created.getId() };
}

// ─── 未完了タスク 読み取り────────────────────────────────────────────────────

/**
 * 特定メンバーの pending_tasks.md を取得
 * @returns { success, memberName, tasks: string[], hasTasks: bool }
 */
function getPendingTasks(username) {
  const memberName = resolveMemberName(username);
  if (!memberName) return { success: false, error: `Unknown username: ${username}` };

  const memberFolder = getMemberFolder(memberName, false);
  if (!memberFolder) return { success: true, memberName, tasks: [], hasTasks: false };

  const files = memberFolder.getFilesByName('pending_tasks.md');
  if (!files.hasNext()) return { success: true, memberName, tasks: [], hasTasks: false };

  const content = files.next().getBlob().getDataAsString('UTF-8');
  const tasks = (content.match(/^- \[ \] .+/gm) || [])
    .map(t => t.replace(/^- \[ \] /, '').trim())
    .filter(t => t.length > 0);

  return { success: true, memberName, tasks, hasTasks: tasks.length > 0 };
}

/**
 * 全メンバーの pending_tasks.md を一括取得（WF4 朝ブリーフィング用）
 * @returns { success, members: { 名前: [task, ...] } }
 */
function getAllPendingTasks() {
  const members = {};
  for (const username of Object.keys(MEMBER_MAP)) {
    const result = getPendingTasks(username);
    if (result.success && result.hasTasks) {
      members[result.memberName] = result.tasks;
    }
  }
  return { success: true, members };
}

// ─── 未完了タスク 保存────────────────────────────────────────────────────────

/**
 * pending_tasks.md を上書き保存（毎回最新状態で上書き）
 * tasks: string[] — タスク本文のみ（"- [ ] " プレフィックスなし）
 */
function savePendingTasks(username, date, tasks) {
  if (!username || !date || !Array.isArray(tasks)) {
    return { success: false, error: 'Missing required fields: username, date, tasks[]' };
  }
  const memberName = resolveMemberName(username);
  if (!memberName) return { success: false, error: `Unknown username: ${username}` };

  const memberFolder = getMemberFolder(memberName, true);
  const content = tasks.length > 0
    ? `# 未完了タスク（${memberName}）\n更新: ${date}\n\n${tasks.map(t => `- [ ] ${t}`).join('\n')}\n`
    : `# 未完了タスク（${memberName}）\n更新: ${date}\n\n該当なし\n`;

  const existing = memberFolder.getFilesByName('pending_tasks.md');
  while (existing.hasNext()) existing.next().setTrashed(true);

  memberFolder.createFile('pending_tasks.md', content, MimeType.PLAIN_TEXT);
  return { success: true, memberName, taskCount: tasks.length, date };
}

// ─── ヒートマップ更新────────────────────────────────────────────────────────

function updateHeatmap(date, submitters) {
  if (!date || !Array.isArray(submitters)) {
    return { success: false, error: 'Missing required fields: date, submitters[]' };
  }
  const file = DriveApp.getFileById(HEATMAP_FILE_ID);
  let html = file.getBlob().getDataAsString('UTF-8');

  const dateKey = JSON.stringify(date);
  const newEntry = `${dateKey}: ${JSON.stringify(submitters)}`;
  const pattern = new RegExp(`${dateKey}\\s*:\\s*\\[.*?\\]`, 'g');

  html = pattern.test(html)
    ? html.replace(pattern, newEntry)
    : html.replace(/(const SUBMISSIONS\s*=\s*\{)/, `$1\n  ${newEntry},`);

  file.setContent(html);
  return { success: true, date, submitters };
}

// ─── ヘルパー ─────────────────────────────────────────────────────────────────

function resolveMemberName(username) {
  if (MEMBER_MAP[username]) return MEMBER_MAP[username];
  for (const [prefix, name] of Object.entries(MEMBER_MAP)) {
    if (username.toLowerCase().startsWith(prefix.toLowerCase())) return name;
  }
  return null;
}

/** Wiki/日報/{memberName}/ フォルダを取得。create=trueなら存在しなければ作成 */
function getMemberFolder(memberName, create) {
  const nippouRoot = DriveApp.getFolderById(WIKI_NIPPOU_FOLDER_ID);
  const iter = nippouRoot.getFoldersByName(memberName);
  if (iter.hasNext()) return iter.next();
  if (create) return nippouRoot.createFolder(memberName);
  return null;
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

// ─── テスト ──────────────────────────────────────────────────────────────────

function testGetPendingTasks()    { Logger.log(JSON.stringify(getPendingTasks('miyawakiMM'), null, 2)); }
function testGetAllPendingTasks() { Logger.log(JSON.stringify(getAllPendingTasks(), null, 2)); }
function testSavePendingTasks() {
  const r = savePendingTasks('miyawakiMM', '2026-05-21', ['キーストーン見積もり送付', '入札案件の判断を確認']);
  Logger.log(JSON.stringify(r, null, 2));
}
function testListInbox() {
  const today = Utilities.formatDate(new Date(), 'Asia/Tokyo', 'yyyy-MM-dd');
  Logger.log(JSON.stringify(listInboxFiles(today), null, 2));
}
