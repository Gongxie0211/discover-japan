/**
 * XOP Wiki API — Google Apps Script
 *
 * XOP_Wiki フォルダ内のすべての .md ファイルを再帰的に取得し、
 * 結合したテキストを JSON で返すエンドポイント。
 *
 * デプロイ設定:
 *   - 実行するユーザー: 自分 (miyawaki.toshio@gmail.com)
 *   - アクセスできるユーザー: 全員
 */

const XOP_WIKI_FOLDER_ID = '1mzZnlFGEwy8fGceH3lA2t-RsXa2ZYRp3';

// QA ログ記録先スプレッドシート ID
// → Google スプレッドシートのURLの /d/XXXX/edit の XXXX 部分を貼り付ける
const QA_LOG_SHEET_ID = 'FILL_ME_SHEET_ID';

// ─────────────────────────────────────────────────────────────────────────────
// GET エンドポイント — Wiki コンテンツ取得
// ─────────────────────────────────────────────────────────────────────────────
function doGet(e) {
  try {
    const files = getFilesRecursive(XOP_WIKI_FOLDER_ID, '');

    // index.md を先頭に並び替え
    files.sort((a, b) => {
      if (a.name === 'index.md') return -1;
      if (b.name === 'index.md') return 1;
      return a.path.localeCompare(b.path);
    });

    const combined = files
      .map(f => `# 📄 ${f.path}\n\n${f.content}`)
      .join('\n\n---\n\n');

    const result = {
      success: true,
      fileCount: files.length,
      fileList: files.map(f => f.path),
      content: combined
    };

    return ContentService
      .createTextOutput(JSON.stringify(result))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// POST エンドポイント — action によって処理を振り分け
// ─────────────────────────────────────────────────────────────────────────────
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const action = data.action || '';

    if (action === 'log_qa') {
      return logQA(data);
    }

    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: `Unknown action: ${action}` }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// QA ログをスプレッドシートに記録
// ─────────────────────────────────────────────────────────────────────────────
function logQA(data) {
  const ss = SpreadsheetApp.openById(QA_LOG_SHEET_ID);
  const sheet = ss.getSheets()[0];  // 先頭シートを使用

  // ヘッダー行がなければ自動作成
  if (sheet.getLastRow() === 0) {
    const headers = ['タイムスタンプ', 'ユーザー名', '質問', '回答', 'チャットID'];
    sheet.appendRow(headers);
    sheet.getRange(1, 1, 1, headers.length)
      .setFontWeight('bold')
      .setBackground('#4a86e8')
      .setFontColor('#ffffff');
    sheet.setFrozenRows(1);
  }

  // JST に変換（UTC+9）
  const ts = data.timestamp
    ? new Date(data.timestamp).toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' })
    : new Date().toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' });

  // = で始まる文字列は数式として解釈されるのを防ぐ
  function safeText(val) {
    const s = String(val || '');
    return s.startsWith('=') || s.startsWith('+') || s.startsWith('-') || s.startsWith('@')
      ? "'" + s   // 先頭にアポストロフィを付けてテキスト扱いにする
      : s;
  }

  // 質問・回答列をテキスト形式に設定してから書き込む
  const newRow = sheet.getLastRow() + 1;
  sheet.getRange(newRow, 1, 1, 5).setNumberFormat('@').setValues([[
    ts,
    safeText(data.username),
    safeText(data.question),
    safeText(data.answer),
    safeText(data.chatId)
  ]]);

  return ContentService
    .createTextOutput(JSON.stringify({ success: true }))
    .setMimeType(ContentService.MimeType.JSON);
}

// ─────────────────────────────────────────────────────────────────────────────
// 再帰的にフォルダ内の .md ファイルを取得
// ─────────────────────────────────────────────────────────────────────────────
function getFilesRecursive(folderId, parentPath) {
  const folder = DriveApp.getFolderById(folderId);
  const results = [];

  // テキストファイル（.md は text/plain で保存される）
  const fileIterator = folder.getFiles();
  while (fileIterator.hasNext()) {
    const file = fileIterator.next();
    const name = file.getName();
    // .md ファイルのみ対象
    if (name.endsWith('.md')) {
      const path = parentPath ? `${parentPath}/${name}` : name;
      results.push({
        name: name,
        path: path,
        content: file.getBlob().getDataAsString('UTF-8')
      });
    }
  }

  // サブフォルダを再帰処理
  const folderIterator = folder.getFolders();
  while (folderIterator.hasNext()) {
    const subFolder = folderIterator.next();
    const subPath = parentPath ? `${parentPath}/${subFolder.getName()}` : subFolder.getName();
    const subFiles = getFilesRecursive(subFolder.getId(), subPath);
    results.push(...subFiles);
  }

  return results;
}

// ─────────────────────────────────────────────────────────────────────────────
// 動作確認用（GASエディタから直接実行）
// ─────────────────────────────────────────────────────────────────────────────
function testWikiApi() {
  const files = getFilesRecursive(XOP_WIKI_FOLDER_ID, '');
  console.log(`取得ファイル数: ${files.length}`);
  files.forEach(f => console.log(`  - ${f.path} (${f.content.length}文字)`));
}

function testLogQA() {
  const result = logQA({
    timestamp: new Date().toISOString(),
    username: 'テストユーザー',
    question: 'XOPの特徴は何ですか？',
    answer: 'XOPはプロテケア技術を使った製品です。',
    chatId: '12345678'
  });
  console.log(result.getContent());
}
