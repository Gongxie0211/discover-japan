from weasyprint import HTML, CSS
import os

output_path = "/Users/gon/Documents/AIMemory/crux/ドバイ展示会/XOP競合分析レポート_MECS2026.pdf"

html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;700&display=swap');

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic", sans-serif;
    font-size: 9.5pt;
    line-height: 1.6;
    color: #0D1B3E;
    background: #F4F6F9;
  }

  /* PAGE */
  @page {
    size: A4;
    margin: 0;
  }

  .page {
    width: 210mm;
    min-height: 297mm;
    position: relative;
    padding: 0 0 12mm 0;
  }

  /* HEADER */
  .header {
    background: #0D1B3E;
    padding: 10mm 18mm 6mm;
    border-bottom: 2mm solid #C9A84C;
  }
  .header h1 {
    font-size: 18pt;
    font-weight: 700;
    color: white;
    margin-bottom: 2mm;
  }
  .header .sub {
    font-size: 9pt;
    color: #C9A84C;
    font-weight: 300;
  }

  /* FOOTER */
  .footer {
    position: fixed;
    bottom: 0;
    left: 0; right: 0;
    background: #0D1B3E;
    padding: 2.5mm 18mm;
    font-size: 7.5pt;
    color: #C9A84C;
    display: flex;
    justify-content: space-between;
  }

  /* CONTENT */
  .content {
    padding: 6mm 18mm 0;
  }

  /* SECTION */
  .section-title {
    font-size: 12pt;
    font-weight: 700;
    color: #0D1B3E;
    margin: 6mm 0 3mm;
    padding-bottom: 1.5mm;
    border-bottom: 0.5mm solid #C9A84C;
  }

  /* CARD */
  .card {
    background: white;
    border: 0.3mm solid #DDE2EA;
    border-radius: 3mm;
    padding: 5mm 6mm;
    margin-bottom: 4mm;
  }
  .card-title {
    font-size: 10.5pt;
    font-weight: 700;
    color: #0D1B3E;
    margin-bottom: 3mm;
  }

  /* TAGS */
  .tag {
    display: inline-block;
    padding: 1mm 4mm;
    border-radius: 2mm;
    font-size: 8pt;
    font-weight: 700;
    color: white;
    margin-bottom: 3mm;
  }
  .tag-red    { background: #C0392B; }
  .tag-orange { background: #E67E22; }
  .tag-navy   { background: #0D1B3E; }

  /* TABLE */
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 9pt;
  }
  th {
    background: #0D1B3E;
    color: white;
    font-weight: 700;
    padding: 3mm 4mm;
    text-align: left;
  }
  td {
    padding: 3mm 4mm;
    vertical-align: top;
    border: 0.3mm solid #DDE2EA;
  }
  tr:nth-child(even) td { background: #F4F6F9; }
  tr:nth-child(odd)  td { background: white; }

  .td-label {
    font-weight: 700;
    color: #0D1B3E;
    width: 28mm;
    white-space: nowrap;
  }

  /* SCORE */
  .s5 { color: #1A7A4A; font-weight: 700; font-size: 12pt; }
  .s4 { color: #E67E22; font-weight: 700; font-size: 12pt; }
  .s3 { color: #AAAAAA; font-weight: 700; font-size: 12pt; }
  .s1 { color: #C0392B; font-weight: 700; font-size: 12pt; }

  /* MATRIX */
  .matrix th { text-align: center; }
  .matrix td { text-align: center; vertical-align: middle; }
  .matrix td:first-child { text-align: left; font-weight: 700; background: #F4F6F9 !important; }
  .matrix .xop { background: #E8F5EE !important; }

  /* WIN ITEMS */
  .win-item {
    display: flex;
    margin-bottom: 3mm;
    gap: 3mm;
  }
  .win-num {
    background: #00B4D8;
    color: white;
    font-weight: 700;
    font-size: 13pt;
    width: 9mm;
    min-width: 9mm;
    height: 9mm;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 1mm;
  }
  .win-body .win-title {
    font-weight: 700;
    font-size: 10pt;
    color: #0D1B3E;
    margin-bottom: 1mm;
  }
  .win-body .win-desc {
    font-size: 9pt;
    color: #333;
    line-height: 1.5;
  }

  /* RISK */
  .risk-item {
    padding: 3mm 4mm 3mm 8mm;
    border-left: 2mm solid #C0392B;
    background: #FFF5F5;
    margin-bottom: 2.5mm;
    font-size: 9pt;
    border-radius: 0 2mm 2mm 0;
  }
  .risk-label {
    font-weight: 700;
    color: #C0392B;
  }
</style>
</head>
<body>
<div class="page">

  <!-- HEADER -->
  <div class="header">
    <h1>ProtoCare XOP 競合分析レポート</h1>
    <div class="sub">Middle East Coatings Show 2026（2026年9月28〜30日 ／ ドバイ）　調査日：2026年6月7日　作成：CRUX G.K.</div>
  </div>

  <div class="content">

    <!-- 1. 展示会概要 -->
    <div class="section-title">1. 調査対象展示会</div>
    <div class="card">
      <table>
        <tr><td class="td-label">名　称</td><td>Middle East Coatings Show 2026</td></tr>
        <tr><td class="td-label">開催日程</td><td>2026年9月28〜30日</td></tr>
        <tr><td class="td-label">会　場</td><td>ドバイ展示センター（DEC）Expo City Dubai</td></tr>
        <tr><td class="td-label">規　模</td><td>出展社 350社以上 ／ 来場者 5,000人以上 ／ 展示面積 15,000m² 以上 ／ 出展国 24カ国以上</td></tr>
        <tr><td class="td-label">位置付け</td><td>中東・北アフリカ最大の塗料・コーティング業界展示会</td></tr>
      </table>
    </div>

    <!-- 2. XOP概要 -->
    <div class="section-title">2. ProtoCare XOP 製品概要</div>
    <div class="card">
      <table>
        <tr><td class="td-label">技術分類</td><td>高分子浸透性フッ素ポリマー（C-C+F結合）</td></tr>
        <tr><td class="td-label">結合エネルギー</td><td>116 kcal/mol</td></tr>
        <tr><td class="td-label">耐UV原理</td><td>解離波長 250nm ＜ 地表UV限界 280nm → 物理法則により劣化しない</td></tr>
        <tr><td class="td-label">撥水・撥油</td><td>水・油・排気ガス・油性マジックを完全拒絶</td></tr>
        <tr><td class="td-label">透明性・透湿性</td><td>外観変化なし、石材の「呼吸」を完全維持</td></tr>
        <tr><td class="td-label">白華リスク</td><td>ゼロ（無機ケイ酸塩系との決定的差異）</td></tr>
        <tr><td class="td-label">保　証</td><td>15年保証（認定施工者適用）</td></tr>
        <tr><td class="td-label">LCC削減効果</td><td>70〜75%削減</td></tr>
        <tr><td class="td-label">ターゲット市場</td><td>ラグジュアリー不動産（高級ホテル・GINZA SIXレベルの施設）</td></tr>
      </table>
    </div>

    <!-- 3. 競合分析 -->
    <div class="section-title">3. 競合分析</div>

    <!-- FILA -->
    <div class="card">
      <span class="tag tag-red">Tier 1 直接競合 ／ 最大の脅威</span>
      <div class="card-title">FILA Solutions（イタリア）</div>
      <table>
        <tr><td class="td-label">技　術</td><td>浸透型石材保護シーラー（MP90 ECO XTREME 等）</td></tr>
        <tr><td class="td-label">中東実績</td><td>ルーブル美術館（アブダビ）、バーレーン空港、カタール国際空港、Expo2020</td></tr>
        <tr><td class="td-label">現地拠点</td><td>ドバイに現地GM・法人あり</td></tr>
        <tr><td class="td-label">主な訴求</td><td>"Lifetime performance and warranty"</td></tr>
        <tr><td class="td-label">XOPとの差</td><td>C-F結合の耐UV理論的優位なし／撥油性は限定製品のみ／Ca系白華リスクあり</td></tr>
        <tr><td class="td-label">MECS出展</td><td>可能性が高い（同市場・同顧客層で競合）</td></tr>
      </table>
    </div>

    <!-- DryTreat -->
    <div class="card">
      <span class="tag tag-orange">Tier 1 直接競合</span>
      <div class="card-title">DryTreat / STAIN-PROOF（オーストラリア）</div>
      <table>
        <tr><td class="td-label">技　術</td><td>シラン＋フッ素ポリマー混合型浸透シーラー</td></tr>
        <tr><td class="td-label">防汚等級</td><td>ISO 10545-14 Class 5（最高等級）</td></tr>
        <tr><td class="td-label">保証年数</td><td>15年保証（認定施工者適用）</td></tr>
        <tr><td class="td-label">中東拠点</td><td>UAE・オマーンに代理店あり（市場参入済み）</td></tr>
        <tr><td class="td-label">XOPとの差</td><td>シランベース＋フッ素添加型。Si-C結合は340nmで崩壊リスク。純粋C-C+F結合ではない</td></tr>
        <tr><td class="td-label">総　評</td><td>保証年数は同等。技術純度・白華ゼロ・ラグジュアリー特化でXOPが差別化可能</td></tr>
      </table>
    </div>

    <!-- Tier 2 -->
    <div class="card">
      <span class="tag tag-navy">Tier 2 間接競合</span>
      <table>
        <thead>
          <tr>
            <th style="width:30%">企業名</th>
            <th style="width:35%">技術・特徴</th>
            <th style="width:15%">MECS出展</th>
            <th>XOPとの関係</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>AGC LUMIFLON</strong><br>（日本・欧州）</td>
            <td>FEVE樹脂（塗料原料）<br>表面被膜型コーティング</td>
            <td style="text-align:center">2026<br><strong>出展確定</strong></td>
            <td>「フッ素コーティング＝LUMIFLON」という来場者認知が競合になり得る</td>
          </tr>
          <tr>
            <td><strong>Wacker Chemicals</strong><br>（ドイツ）</td>
            <td>シリコーン・シランシロキサン系<br>撥水性は高いが撥油性なし</td>
            <td style="text-align:center">過去出展<br>確認済み</td>
            <td>石材保護市場での先行認知が脅威</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 4. 差別化比較表 -->
    <div class="section-title">4. 差別化比較表</div>
    <div class="card">
      <table class="matrix">
        <thead>
          <tr>
            <th style="width:28%;text-align:left">差別化軸</th>
            <th style="width:18%">XOP</th>
            <th style="width:18%">FILA</th>
            <th style="width:18%">DryTreat</th>
            <th style="width:18%">Wacker</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>撥油性</td>
            <td class="xop"><span class="s5">◎</span></td>
            <td><span class="s3">△</span></td>
            <td><span class="s4">○</span></td>
            <td><span class="s1">×</span></td>
          </tr>
          <tr>
            <td>耐UV（物理保証）</td>
            <td class="xop"><span class="s5">◎</span></td>
            <td><span class="s3">△</span></td>
            <td><span class="s3">△</span></td>
            <td><span class="s1">×</span></td>
          </tr>
          <tr>
            <td>白華リスクゼロ</td>
            <td class="xop"><span class="s5">◎</span></td>
            <td><span class="s1">×</span></td>
            <td><span class="s3">△</span></td>
            <td><span class="s3">△</span></td>
          </tr>
          <tr>
            <td>透湿性維持</td>
            <td class="xop"><span class="s5">◎</span></td>
            <td><span class="s5">◎</span></td>
            <td><span class="s5">◎</span></td>
            <td><span class="s3">△</span></td>
          </tr>
          <tr>
            <td>保証年数</td>
            <td class="xop">15年</td>
            <td>Lifetime</td>
            <td>15年</td>
            <td>—</td>
          </tr>
          <tr>
            <td>中東実績</td>
            <td class="xop"><span class="s1">×</span></td>
            <td><span class="s5">◎</span></td>
            <td><span class="s4">○</span></td>
            <td><span class="s3">△</span></td>
          </tr>
          <tr>
            <td>ラグジュアリー特化</td>
            <td class="xop"><span class="s5">◎</span></td>
            <td><span class="s4">○</span></td>
            <td><span class="s3">△</span></td>
            <td><span class="s1">×</span></td>
          </tr>
        </tbody>
      </table>
      <p style="font-size:7.5pt;color:#666;margin-top:2mm">◎ 最強優位　○ 優位　△ 限定的　× なし　／　XOP列を緑色でハイライト</p>
    </div>

    <!-- 5. 勝ち筋 -->
    <div class="section-title">5. XOPの勝ち筋</div>
    <div class="card">
      <div class="win-item">
        <div class="win-num">1</div>
        <div class="win-body">
          <div class="win-title">物理法則による絶対的優位</div>
          <div class="win-desc">C-C+F結合（解離波長250nm）を破壊するエネルギーは地球上に存在しない。FILAもDryTreatもこの理論的根拠を持たない。</div>
        </div>
      </div>
      <div class="win-item">
        <div class="win-num">2</div>
        <div class="win-body">
          <div class="win-title">撥油性の決定的差異</div>
          <div class="win-desc">水だけでなく「油」を弾けるのはフッ素系の専売特許。FILA・Wackerには撥油機能がない。排気ガス・油性マジックまで拒絶できる唯一の製品。</div>
        </div>
      </div>
      <div class="win-item">
        <div class="win-num">3</div>
        <div class="win-body">
          <div class="win-title">白華リスクゼロ保証</div>
          <div class="win-desc">高級大理石・御影石へのCa系白華リスクはFILAの潜在的弱点。数百万ドルの美観が一度の化学反応で失われるリスクをXOPは構造的に排除する。</div>
        </div>
      </div>
      <div class="win-item">
        <div class="win-num">4</div>
        <div class="win-body">
          <div class="win-title">認定施工者システム（ゴールド階層・地域独占）</div>
          <div class="win-desc">品質保証を施工者の資格制度で担保する構造。アマチュアリスクをゼロにする仕組みは他社にない。地域独占権はパートナー獲得のインセンティブになる。</div>
        </div>
      </div>
      <div class="win-item">
        <div class="win-num">5</div>
        <div class="win-body">
          <div class="win-title">日本品質 × ラグジュアリー特化</div>
          <div class="win-desc">中東市場における日本ブランドの希少性と信頼性。「汎用品ではなくラグジュアリーのために設計された製品」という唯一性がFILAとの差別化軸になる。</div>
        </div>
      </div>
    </div>

    <!-- 6. 課題・リスク -->
    <div class="section-title">6. 課題・リスク</div>
    <div class="card">
      <div class="risk-item">
        <span class="risk-label">中東実績ゼロ：</span>FILAはルーブル美術館級の実績を持つ。展示会で最初に突かれるポイント。実績の代替として「日本国内の高級施設実績＋技術理論（物理法則）」で補完する準備が必要。
      </div>
      <div class="risk-item">
        <span class="risk-label">市場認知の遅れ：</span>DryTreatはUAE代理店経由ですでに施工業者の認知を得ている。XOPは「知られていない」状態からのスタートになる。
      </div>
      <div class="risk-item">
        <span class="risk-label">展示会トーク準備：</span>「なぜFILAではなくXOPか」「DryTreatと何が違うのか」を30秒で答えられる営業トークの事前準備が必須。競合比較を明示したワンペーパーの用意を推奨。
      </div>
    </div>

  </div><!-- /content -->

  <!-- FOOTER -->
  <div class="footer">
    <span>CRUX G.K.  ｜  ProtoCare XOP  ｜  Confidential</span>
    <span>2026年6月7日作成</span>
  </div>

</div>
</body>
</html>"""

html_path = "/Users/gon/Documents/AIMemory/crux/ドバイ展示会/report_temp.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

HTML(filename=html_path).write_pdf(output_path)
os.remove(html_path)
print(f"✅ PDF生成完了: {output_path}")
