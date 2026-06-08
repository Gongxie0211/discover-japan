/**
 * normalize.js — XOP 音声入力 正規化ノード (n8n Code node)
 *
 * n8n の「🔤 テキスト正規化」コードノードとして使用。
 * Whisper の誤認識パターンをClaudeに渡す前に修正する。
 *
 * 入力:  $input.first().json.question  (前ノード「📝 変数抽出」より)
 * 出力:  { ...同じフィールド, question: <正規化後テキスト> }
 */

const item = $input.first().json;
let text = item.question || '';

// ────────────────────────────────────────
// 1. 製品・技術用語
// ────────────────────────────────────────
text = text.replace(/ゾップ|ゾッポ|ExOP|X\.O\.P/gi, 'XOP');
text = text.replace(/プロテア(?!ケア)|プロテカ|プロテーケア|プロテラ/g, 'プロテケア');
text = text.replace(/ウォーターセラミックス|水セラミック/g, 'ウォーターセラミック');
text = text.replace(/クラック(?!ス)|クラクス/g, 'クラックス');

// ────────────────────────────────────────
// 2. 人名
// ────────────────────────────────────────
text = text.replace(/湯沢/g, '湯澤');
text = text.replace(/稲沢/g, '稲澤');
text = text.replace(/中沢/g, '中澤');
text = text.replace(/笹木/g, '佐々木');

// ────────────────────────────────────────
// 3. 会社名
// ────────────────────────────────────────
text = text.replace(/パナホーム(?!リフォーム)/g, 'Panaホームリフォーム');
text = text.replace(/アルティス/g, 'Artis');
text = text.replace(/マリナベイシップ/g, 'MarinaBayShip株式会社');
text = text.replace(/アナザーストーリージャパン/g, 'AnotherStoryJapan');
text = text.replace(/起訴者/g, 'キーストーン社');

// ────────────────────────────────────────
// 4. 一般的な誤変換
// ────────────────────────────────────────
// 全角→半角数字（任意）
// text = text.replace(/[０-９]/g, s => String.fromCharCode(s.charCodeAt(0) - 0xFEE0));

// ────────────────────────────────────────
// 5. 先頭記号の除去・トリム
// ────────────────────────────────────────
// = + - @ で始まるとスプレッドシートが数式として誤解釈される
text = text.replace(/^[=+\-@]+/, '');
text = text.trim();

return {
  ...item,
  question: text,
  _normalized: text !== item.question  // デバッグ用: 正規化されたかどうか
};
