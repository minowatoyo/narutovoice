# 鳴門市民の声 データ収集 (2026-10-19)

出典はすべて鳴門市公式サイト https://www.city.naruto.lg.jp (旧 city.naruto.tokushima.jp は 2026年に移転、旧URLは404)。

## data/raw/ (PDF原本)
- surveys/              市民意識調査(R3/総合計画), まちづくりWS, 福祉アンケート(R4,3種), 地域福祉計画市民アンケート, スポーツ市民アンケート, こども計画(15-29歳/小中学生/事業所), 子どもの生活調査, 放課後児童クラブ保護者
- public_comments/      パブリックコメント結果公表
- school_lunch_survey/  給食アンケート H29-R7
- school_achievement/   全国学力調査 市結果 H27-R7
- council_minutes/      総合計画審議会 議事概要 H23-R8
- gikai_questions/      市議会 一般質問一覧 (質問項目=議員が拾った市民の声)
- gikai_dayori/ petitions/ gikai_resolutions/  議会だより・請願陳情・議決結果
- plans_context/        各種計画の概要版・人口ビジョン2025(転入転出アンケート/高校生アンケート含む)
- statistics_yearbook/  統計年報 2013-2026 (人口・世帯・産業等)

## data/ocr/  OCRテキスト
PDFの文字層に日本語が入っていない(数字のみ)ため、Windows OCR(ja)で文字起こし。誤認識あり。
`data/text/` は pdftotext の結果だが日本語欠落のため使わない。

## 未取得/リード
- 議会会議録(発言全文): https://ssp.kaigiroku.net/tenant/naruto/pg/index.html (JSアプリ)
- 広報アンケート(Logoform)・市長への手紙・ご意見箱は非公開
- e-Stat / RESAS / 徳島県オープンデータ(市町村別指標) 未取得
- scripts/ : crawl.py crawl2.py dl.py ocr_all.py ; manifest.json = 取得ファイル一覧

## data/free_text/ (自由記述抽出)
comments_tagged.csv / .json : 約990件。kind列で「自由記述(個別回答)」「審議会委員の発言」「理由の集計(件数付き)」を区別。
scripts/extract_free.py -> extract_free2.py -> tag_free.py の順に実行。OCR誤り(で→て等)は一部のみ補正、text_rawに原文。

## data/statistics_csv/ (統計年報の表をCSV化)
2013-2026年の207表 (_index.csv が一覧)。scripts/stat_to_csv.py。ヘッダが複数行の表は先頭数行がヘッダ。△は-に変換。グラフのみの28ファイルは表なし(.txtのみ)。

## data/tokushima_opendata/
shihyo2016_naruto.csv : 徳島県 市町村別指標2016(鳴門市) 85項目。catalog.json: 県オープンデータ全データセット目録(取得中/取得後に鳴門関連を抽出)。

## e-Stat
API利用にはappIdが必要(未取得)。data/estat/ は空。

## 出典・注意
- 鳴門市公式サイトの公開資料(PDF)から作成。元PDFはリポジトリに含めず、manifest.json の取得元から再取得する。OCRテキストは誤認識を含む。
- data/gikai_commons/: 出典: 全国地方議会発言データベース「議会コモンズ」 (https://gikai-commons.isvd.or.jp/) CC BY 4.0 / 取得日: 2026-10-19頃
- data/tokushima_opendata/: 徳島県オープンデータ(市町村別指標2016)
