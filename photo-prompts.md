# CRUX — AI参考写真プロンプト集

**ブランド**: 建築資産保護の専門家 CRUX  
**作成日**: 2026-05-29  
**対応プラットフォーム**: Midjourney v6 / Stable Diffusion XL / DALL-E 3

---

## 共通スタイル定義（全プロンプトに必須）

```
architectural photography, professional, ultra-detailed,
cool tone, high contrast, desaturated (-15 saturation), cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP, editorial quality,
black and dark navy color palette, gold accent tones, off-white highlights
```

---

## 1. Hero / メインビジュアル

---

### 1-1. 世界都市の高層ビル外壁クローズアップ（ドバイ）

**用途**: トップページ Hero セクション背景、ファーストビュー

**英語プロンプト**:
```
Extreme close-up of a luxury high-rise tower facade in Dubai,
architectural photography, glass curtain wall with dark anodized aluminum framing,
geometric precision in reflective panels, harsh desert midday light creating sharp shadow lines,
gold metallic trim details catching specular highlights,
abstract architectural texture filling the entire frame,
cool tone, high contrast, desaturated, cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP, editorial quality,
vertical composition, no sky visible, pure architectural abstraction
```

**ネガティブプロンプト**:
```
people, tourists, smiling faces, cars, street level, cheap materials,
warm tones, oversaturated colors, HDR glow, lens flare, noise, blur,
construction workers, scaffolding (unless intentional), local signage,
ugly weather, overcast flat lighting
```

**補足メモ**:
- アスペクト比: `--ar 9:16`（モバイル Hero）または `--ar 16:9`（デスクトップ Hero）
- Midjourney では末尾に `--v 6 --style raw --chaos 5` を追加
- ドバイ特有の「砂漠の逆光で輝くガラスカーテンウォール」の質感を狙う

---

### 1-2. 朝の光が当たる高層ビル全景（威厳・資産感）

**用途**: About ページ冒頭、サービス概要セクション背景

**英語プロンプト**:
```
Full elevation shot of a monolithic luxury skyscraper at dawn,
Tokyo metropolitan backdrop, golden hour side-lighting from low angle on the east face,
building facade glowing with warm gold against deep navy-blue pre-dawn sky,
glass and stone cladding with perfect geometric symmetry,
long vertical lines emphasizing height and permanence,
foreground: polished granite plaza, no people,
architectural photography, professional, ultra-detailed,
cool tone sky contrasting with gold-lit facade, high contrast, cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP, editorial quality,
--ar 2:3
```

**ネガティブプロンプト**:
```
people, cars, busy street, midday flat light, overcast sky,
cartoon style, illustration, 3D render look, lens distortion,
ugly buildings in background, low-rise context, clutter
```

**補足メモ**:
- 東京を指定しているが「日本らしさ」は抑えること。国際的な都市景観として処理。
- 空の色がダークネイビー〜ディープブルーになるよう `dawn` または `blue hour` を指定するとよい
- 建物の比率は縦長（タワー）が望ましい

---

### 1-3. 外壁の石材・コンクリートの質感接写（精密感）

**用途**: 技術訴求セクション、XOP説明の補足、テクスチャ背景素材

**英語プロンプト**:
```
Extreme macro close-up of premium building facade material,
honed travertine limestone panel with micro-crystalline surface texture,
raking side-light from 15 degrees revealing every micro-pore and grain,
shallow depth of field transitioning from razor-sharp center to soft edges,
f/2.8 tilt-shift lens effect, silver-grey stone tones with subtle warm veining,
water droplets sitting on surface demonstrating material porosity,
architectural photography, professional, ultra-detailed,
cool tone, high contrast, desaturated, cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP with 120mm macro lens, editorial quality
```

**ネガティブプロンプト**:
```
dirty surface, damage, cracks, stains (unless for before/after set),
people, tools, color cast, warm yellow light, plastic texture,
tile grout, low-quality material, synthetic surface
```

**補足メモ**:
- この画像は「XOP技術が守るべき対象」を表すため、あくまでクリーンで高級な素材感を示す
- セクション 2-2（施工前）とのトーン差を付けるために、ここは必ず清潔な状態で生成すること

---

## 2. XOP技術説明用

---

### 2-1. コーティング剤が石材に浸透するイメージ（断面図的・マクロ）

**用途**: XOP技術ページ、製品説明セクション、動画サムネイル

**英語プロンプト**:
```
Scientific macro photography of liquid nano-coating penetrating into natural stone,
cross-section visualization concept, limestone or granite sample cut in half,
transparent liquid seeping into micro-pores visible as crystal-clear fluid channels,
bioluminescent-style blue-white illumination showing penetration depth,
dramatic studio lighting: one sidelight with dark background,
photorealistic, not illustrated, tactile material quality,
depth markers suggestion through sharp-to-blur focus transition,
architectural photography, professional, ultra-detailed,
cool tone, high contrast, desaturated, cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP, editorial quality
```

**ネガティブプロンプト**:
```
cartoon, diagram, infographic style, text overlay, arrows, labels,
syringe, chemical symbols, cheap plastic lab equipment,
warm color cast, yellow tones, oversaturated blue, unrealistic glow
```

**補足メモ**:
- 「浸透している」ことを液体の動きで示すのが理想。静的な素材写真にならないよう `liquid`, `seeping`, `penetrating` を強調
- 背景は黒またはダークグレーで統一するとブランドトーンに合う
- Midjourney: `--ar 4:5 --v 6 --style raw`

---

### 2-2. 施工前：外壁の劣化・汚れ・ひび割れのクローズアップ

**用途**: ビフォーアフター比較、問題提起セクション、課題訴求

**英語プロンプト**:
```
Close-up architectural detail photography of deteriorated building facade,
aged concrete surface with hairline cracks, efflorescence white salt deposits,
biological growth staining, water ingress dark tide marks,
rough texture with micro spalling at surface level,
harsh clinical top-light revealing every flaw and surface damage,
grey and brown tones, desaturated, no color grading warmth,
sense of neglect and material fatigue,
architectural photography, professional, ultra-detailed,
cool tone, high contrast, desaturated, cinematic lighting,
premium documentation quality, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP, editorial quality
```

**ネガティブプロンプト**:
```
clean surface, beautiful material, warm lighting, people,
text overlays, cartoon, illustration, extreme destruction or collapse,
cheap residential building, visible brand names
```

**補足メモ**:
- 「問題提起」用なので意図的に劣化を見せるが、崩壊・廃墟レベルではなく「プロ目線でわかる微細な劣化」を表現
- 2-3（施工後）と同一アングル・同一ライティングになるよう両プロンプトを揃えること
- `--ar 1:1` で正方形にするとSNS投稿にも転用しやすい

---

### 2-3. 施工後：クリーンに蘇った外壁（ビフォーアフター対比用）

**用途**: ビフォーアフター比較（2-2 の対になる画像）、実績・効果訴求

**英語プロンプト**:
```
Close-up architectural detail photography of pristine restored building facade,
same concrete surface now clean and uniformly colored, all cracks sealed invisible,
micro-crystalline surface sheen indicating nano-coating protection layer,
water beading effect visible in subtle specular highlight across the surface,
same harsh top-light as before/after counterpart, revealing flawless smooth texture,
grey stone tones with subtle silver sheen, desaturated except for the protective sheen gloss,
sense of precision restoration and long-term protection,
architectural photography, professional, ultra-detailed,
cool tone, high contrast, desaturated, cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP, editorial quality
```

**ネガティブプロンプト**:
```
cracks, stains, dirt, biological growth, damage, deterioration,
warm color cast, people, text overlays, cartoon, illustration,
visible repair lines, patchwork texture, cheap materials
```

**補足メモ**:
- 2-2 と同一構図・アングルで生成し、並列配置のビフォーアフターとして使用
- 「水を弾いている微細な光沢」(`water beading`, `specular sheen`) を入れるとXOPの効果を視覚的に示せる
- Stable Diffusion では img2img で 2-2 の画像をベースに生成すると構図一致が取れる

---

## 3. 世界の現場レポート用

---

### 3-1. ドバイの高層ビル群・砂漠の乾燥した空気感

**用途**: 海外実績紹介ページ、ドバイ現場レポート記事ヘッダー

**英語プロンプト**:
```
Wide establishing shot of Dubai skyline from elevated vantage point,
Burj Khalifa and surrounding towers emerging from heat haze and fine desert dust,
atmospheric perspective causing buildings to fade into pale warm haze in distance,
foreground: polished dark marble terrace edge suggesting luxury hotel observation deck,
late afternoon sun at 20-degree angle casting long shadows between towers,
sky: deep cobalt blue at zenith fading to pale bleached white near horizon,
architectural photography, professional, ultra-detailed,
cool tone upper atmosphere contrasting with dry haze at horizon,
high contrast, desaturated, cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP with 70mm lens, editorial quality
```

**ネガティブプロンプト**:
```
people in foreground, tourists, selfies, cars, commercial signage,
rain, clouds, green vegetation, non-desert atmosphere,
warm orange sunset tones, oversaturated, HDR
```

**補足メモ**:
- `heat haze` と `desert dust` のキーワードが中東の乾燥した空気感を出す鍵
- `--ar 16:9` でワイドスクリーン用ヘッダー画像として生成推奨
- 縦位置（`--ar 4:5`）でInstagram投稿用バリエーションも生成しておくと汎用性が上がる

---

### 3-2. ハワイの海沿いマンション・塩害を連想させる海景

**用途**: ハワイ現場レポート、塩害問題の訴求、海外資産オーナー向けコンテンツ

**英語プロンプト**:
```
Luxury oceanfront high-rise condominium tower in Hawaii, Honolulu coastal setting,
building facade facing open Pacific Ocean, salt-air corrosion visible as subtle white oxidation
on metal window frames and concrete spandrel panels,
foreground: crashing waves and ocean spray creating salt mist atmosphere,
overcast Pacific sky with diffused silver-white light,
teal and grey ocean tones, building facade in concrete and glass,
strong wind implied by ocean texture, sense of relentless environmental exposure,
architectural photography, professional, ultra-detailed,
cool tone, high contrast, desaturated, cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP, editorial quality
```

**ネガティブプロンプト**:
```
tourists, beach umbrellas, people in swimwear, tropical cliché,
palm trees (unless subtle background), bright sunshine, golden hour warmth,
boats, lifeguard towers, cheap motels, oversaturated teal water
```

**補足メモ**:
- 「塩害」の問題意識を視覚化するため `salt-air corrosion`, `salt mist` を明示
- ただし廃墟感は出さず、あくまで「高級物件が塩害リスクに晒されている」緊張感を表現
- `--ar 3:2` で横長アイキャッチ推奨

---

### 3-3. 韓国ソウルの現代的なオフィスビル

**用途**: 韓国現場レポート、アジア実績紹介、グローバル展開訴求

**英語プロンプト**:
```
Contemporary glass and steel office tower in Seoul business district, Gangnam or Yeouido,
clean modernist facade with precise aluminum grid curtain wall system,
overcast Korean winter sky providing soft shadowless grey diffused light,
reflections of neighboring towers in the glass panels creating abstract geometry,
street level absent, mid-height perspective emphasizing vertical scale,
monochromatic silver and dark grey tones, minimal color variation,
architectural photography, professional, ultra-detailed,
cool tone, high contrast, desaturated, cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP with 50mm tilt-shift lens, editorial quality
```

**ネガティブプロンプト**:
```
Korean signage visible, street food stalls, people, cars,
K-pop aesthetics, bright neon, warm color tones,
traditional Korean architecture, residential buildings,
ugly neighboring buildings cluttering the frame
```

**補足メモ**:
- ソウルのビジネス街（汝矣島 / 江南）の無機質で現代的な建築を意識
- 韓国語の看板が見えるとローカル感が出てしまうため `--no Korean signage` または negative prompt で除外
- `--ar 2:3` 縦位置でビルの高さを強調

---

### 3-4. 日本の職人が外壁を点検・施工している後ろ姿

**用途**: 日本現場レポート、職人技・技術品質の訴求、施工プロセス紹介

**英語プロンプト**:
```
Back view of a Japanese master craftsman inspecting a high-rise building facade,
figure wearing clean white work uniform and protective gloves,
standing on suspended access gondola at high altitude, city skyline below,
craftsman examining concrete panel surface closely with a measuring tool,
no face visible, anonymous silhouette of expertise and precision,
late afternoon directional light from the west creating strong rim light on figure,
city background softly out of focus below,
architectural photography, professional, ultra-detailed,
cool tone, high contrast, desaturated, cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP, editorial quality,
--ar 4:5
```

**ネガティブプロンプト**:
```
face visible, smiling, looking at camera, casual clothing,
messy construction site, cheap equipment, safety violations,
low-rise buildings, rural Japan, cartoon, illustration,
crowded scene, multiple workers
```

**補足メモ**:
- 「顔不要」を確実にするため `back view`, `no face visible`, `anonymous silhouette` を明示
- 白い作業着は日本の職人の誠実さと清潔感を体現し、ブランドトーンとも合致
- ゴンドラ（ロープアクセス）での高所点検シーンが「本格的な技術力」の訴求に有効

---

## 4. 社長・現場視察イメージ

---

### 4-1. スーツ姿の男性がビルを見上げている後ろ姿

**用途**: 会社概要ページ、代表挨拶セクション、LinkedIn プロフィール記事

**英語プロンプト**:
```
Back view of a distinguished Japanese man in his mid-fifties,
wearing a tailored dark charcoal wool suit, perfectly fitted,
standing on a city plaza looking up at a monumental glass skyscraper,
figure positioned off-center to the left, building filling right two-thirds of frame,
early morning blue hour light, building facade lit with warm interior lights
contrasting cool exterior dawn sky,
sense of ownership, mastery, and quiet authority,
no face visible, only the silhouette and back of head with silver-streaked hair,
architectural photography, professional, ultra-detailed,
cool tone, high contrast, desaturated, cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP, editorial quality
```

**ネガティブプロンプト**:
```
face visible, smiling, looking at camera, casual clothing,
young person, woman (unless requested), group of people,
tourist pose, hands in pockets looking casual,
bright daylight, warm tones, greenery, non-urban background
```

**補足メモ**:
- `silver-streaked hair` で55歳前後の貫禄を表現しつつ顔は見せない
- 人物とビルの対比構図（小さな人間 vs 巨大な建築）が「資産の規模感」を伝える
- `--ar 2:3` 縦位置でWebページの縦スクロールデザインに適合

---

### 4-2. タブレットを持ちながら外壁を確認している横顔シルエット

**用途**: サービス紹介ページ、技術的専門性の訴求、ヘッダービジュアル

**英語プロンプト**:
```
Side silhouette profile of a business executive holding a tablet device,
standing in front of a glass building facade, 3/4 back view avoiding face recognition,
rim-lit by late afternoon sun creating a sharp halo around figure,
tablet screen shows building facade data (no readable text),
executive in dark suit, slight forward lean suggesting engagement and analysis,
building behind is out of focus bokeh — dark glass, gold-framed panels,
atmosphere of quiet intelligence and methodical evaluation,
architectural photography, professional, ultra-detailed,
cool tone, high contrast, desaturated, cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP with 85mm f/1.4, editorial quality
```

**ネガティブプロンプト**:
```
full face visible, smiling directly at camera, casual pose,
cartoon tablet UI, brand logos on tablet, recognizable software UI,
casual clothing, woman (unless requested), bright sun, warm tones,
cluttered background, street level noise
```

**補足メモ**:
- `side silhouette profile`, `3/4 back view` で確実に顔を隠す
- タブレット画面には「読めないデータ表示」程度でOK。具体的なテキストは避ける
- リム光（rim light）で人物の輪郭を際立たせることで、暗いトーンでも存在感が出る

---

## 5. LinkedIn・Instagram投稿用

---

### 5-1. 会議室で資産家と打ち合わせをしている場面（俯瞰・手元）

**用途**: LinkedIn 活動報告投稿、商談プロセス訴求、信頼関係の表現

**英語プロンプト**:
```
Top-down overhead flat-lay perspective of a luxury boardroom meeting,
two pairs of hands visible on a dark walnut conference table,
one set in tailored suit sleeve, other in premium casual,
architectural drawings and a closed leather portfolio on the table,
two crystal glasses of still water, a fine-point pen,
gold business card holder partially visible at edge,
table surface reflecting soft diffused overhead lighting,
no faces visible, pure hands-and-table composition,
architectural photography, professional, ultra-detailed,
cool tone, high contrast, desaturated, cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP directly overhead, editorial quality
```

**ネガティブプロンプト**:
```
faces visible, casual clothing, laptops with visible screens and brand logos,
coffee cups, food, cheap furniture, cluttered desk, fluorescent office lighting,
printed contracts with readable text, smartphones, overly staged feel
```

**補足メモ**:
- 完全俯瞰（真上）構図で人物の身元を隠しつつ「高級な打ち合わせ」の空気を表現
- `architectural drawings` をテーブル上に置くことでCRUXの専門性を暗示
- `--ar 1:1` 正方形でInstagram投稿用、`--ar 4:5` でLinkedIn縦投稿用

---

### 5-2. 南十字星が見える夜空（ブランドストーリー投稿用）

**用途**: ブランドストーリー投稿、CRUX（南十字星）の名前の由来説明

**英語プロンプト**:
```
Astrophotography of the Southern Cross constellation (Crux) in the southern hemisphere night sky,
crystal-clear Milky Way band visible, Southern Cross prominently centered,
deep space photograph showing star density and galactic core,
foreground: dark silhouette of a modern building rooftop edge suggesting architecture,
star colors: white and pale blue-white, no color gimmicks,
infinite depth of field from near-infinity, long exposure smoothness,
atmospheric: profound, navigational, orientation, permanence,
architectural photography style adapted for astrophotography, professional, ultra-detailed,
cool tone, high contrast, desaturated, cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Sony A7R V with 24mm f/1.4 Sigma Art, editorial quality
```

**ネガティブプロンプト**:
```
Northern hemisphere sky, Big Dipper prominent, light pollution, orange glow,
clouds obscuring stars, aurora, people, oversaturated purple/green,
cartoon stars, flat illustration style, lens flare streaks
```

**補足メモ**:
- CRUX = 南十字星 というブランド名の由来を視覚化する重要なイメージ
- 建物のシルエットを前景に入れることで建築との接点を作る
- オーストラリア・ニュージーランド・南米から見える南十字星を想定。南半球の空であることを `southern hemisphere` で指定
- `--ar 4:5` でInstagram縦投稿に最適

---

### 5-3. CRUXゴールドカラーの名刺を渡している手元クローズアップ

**用途**: 初回接触・商談開始の象徴、LinkedIn プロフィール用、ブランドビジュアル

**英語プロンプト**:
```
Extreme close-up of a hand extending a premium business card,
card design: matte black with gold foil embossed text and geometric minimal logo,
receiving hand partially visible from opposite side,
shallow depth of field f/1.4, sharp focus on the card face,
gold foil catching directional studio light creating specular highlight,
card corners perfectly square, heavy stock weight implied by slight bend during handoff,
background: blurred dark luxury interior — glass and dark wood,
architectural photography, professional, ultra-detailed,
cool tone, high contrast, desaturated, cinematic lighting,
premium, luxury, Japanese precision aesthetic,
8K resolution, shot on Phase One IQ4 150MP with 100mm macro, editorial quality
```

**ネガティブプロンプト**:
```
faces visible, casual clothing sleeves, cheap card stock, glossy lamination,
cluttered background, bright colourful business card, readable text on card,
smudged or bent card, tacky gold foil, warm orange light,
full handshake scene, multiple cards
```

**補足メモ**:
- 名刺に読めるテキストを入れないことで汎用性を保つ（`no readable text` または negative prompt で処理）
- 金箔の光沢 (`gold foil`, `specular highlight`) がCRUXのブランドカラーと直結する
- `--ar 4:5` でSNS縦投稿用。`--ar 1:1` で正方形バリエーションも有用

---

## Appendix: プラットフォーム別調整ガイド

### Midjourney v6
- 末尾に `--v 6 --style raw --q 2` を追加
- スタイル強調: `--stylize 200`（高品質写真調）
- 縦横比: `--ar 16:9` / `--ar 4:5` / `--ar 1:1`

### Stable Diffusion XL
- Checkpoint: `RealVisXL` または `SDXL-base-1.0` + `Juggernaut XL`
- Sampler: `DPM++ 2M Karras`, Steps: 35-50, CFG: 7-8
- ネガティブプロンプト全体に `(worst quality:1.4), (bad quality:1.4), (low quality:1.4)` を追加

### DALL-E 3 (ChatGPT / API)
- 「as a professional photograph」「in the style of editorial photography」を先頭に追加
- DALL-E は技術的パラメータより自然言語の方が効果的
- 人物の顔は自動的に生成される場合があるため、`back view only, face not visible` を冒頭で明示

### Flux 1.1 Pro
- 詳細な自然言語記述がそのまま有効
- `photorealistic` キーワードよりも具体的な機材・状況描写を優先
- 生成時間が長いため、重要な画像のみに使用推奨

---

*Generated by CRUX Image Prompt Engineer — 2026-05-29*
