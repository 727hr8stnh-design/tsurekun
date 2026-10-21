# 進捗

## 2026-10-22 JST / v0.2.1
- ChatGPTライブラリから取得した原本を source/、展開物を imported_publish_v02/ にローカル保存。原本はGit対象外。
- source/SPEC.md は別プロジェクトの文書だったため不採用。正本はルート SPEC.md。
- 派生GLBの22ジョイント、01_Groove_4s / 02_Breakbeat_4s を構造確認。
- 表示ライブラリ同梱、読み込み中の操作無効化、エラーとタイムアウト案内を追加。
- GitHub: https://github.com/727hr8stnh-design/tsurekun
- 公開URL: https://727hr8stnh-design.github.io/tsurekun/
- Pagesビルド b383179b5907d10a4621455631a2f80af44e56fa: built、エラーなし。
- 公開HTMLとローカルHTMLの完全一致、公開GLBとローカルGLBのSHA256一致を確認。
- Chromeで公開モデルの描画、ダンス切替、一時停止表示、ドラッグ回転、390px幅の横はみ出しなしを確認。
- 公開画面の証拠: verification/public-mobile.png（ローカルのみ）。
- iPhone Safari実機: 未確認（接続された実機なし）。Mac SafariのUI取得もタイムアウトのため未確認。Safari対応はmodel-viewerの公式対応範囲に基づく。
- 共有ボタンの実送信は未実施。

## 2026-10-22 JST / v0.2.2 軸修正
- 原因: 元GLBの骨格と頂点がZ-up、ビューアーはY-up。
- ルート全体にX軸-90度の変換を適用。形状・スキン・アニメーションのバイナリ部分は元と完全一致をスクリプトで検証。
- ローカルChromeで正面の直立、水平ドラッグ後の側面でも直立維持、ダンス2への切替を目視確認。
- モデルURLに版を付与して古いモデルのキャッシュを回避。iPhone実機は未確認。
- 公開確認: cb6400d のPagesビルド成功。公開HTML・GLBは修正版と完全一致。公開URLでも直立姿勢と水平ドラッグ後の側面表示を確認。証拠: verification/axis-fixed.png。
