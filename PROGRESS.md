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

## 白いクマ試作 / 2026-10-22
- 提供された正面・側面・背面写真を参考に手続き生成したGLBと独立ビューアーを docs/bear/ に作成。
- Y-up、ゆれる・手を振るの2クリップ。写真測量ではなく簡略化した形状モデル。リアルな毛並みは未再現。
- ローカルChromeで実モデル読み込みと正面描画を確認。iPhone実機は未確認。
- 公開URL: https://727hr8stnh-design.github.io/tsurekun/bear/
- 577c38d のPagesビルド成功。公開HTML・GLBとローカル成果物の一致、公開ブラウザで2クリップ読み込み・モデル描画を確認。ローカルでHELLO切替確認。証拠 verification/bear-public.png。

## クマ手足修正 / v0.1.1
- 以前は腕の中心が回転支点で、足も胴体から独立した形だった。
- 肩支点＋下へ伸びる腕、短い脚と足の階層、揺れ幅縮小へ変更。
- ローカルで正面・側面とHELLO切替を確認。iPhone実機未確認。
- 公開検証: d34de3b のPagesビルド成功。配信HTML・GLBがローカル修正版と一致。公開ブラウザでモデル描画、HELLO切替、一時停止を確認。証拠 verification/bear-limbs-v2.png。

## 腕の取付位置 / v0.1.2
- 追加の側面参考写真に合わせ、肩を外側・後方へ移し、腕中心の前方オフセットを除去。
- ローカルChromeで正面・側面を目視確認。側面で腕が胴体中央付近から下がる位置へ変更。iPhone実機未確認。
- 公開検証: 4a6ed47 のPagesビルド成功。配信HTMLとGLBが修正版に一致。公開ブラウザの側面で腕位置を確認。証拠 verification/bear-shoulder-v3.png。

## 胴体の厚み / v0.1.3
- 茶色のクマの側面写真を参考に、胴体の前後の厚みを約30%増加。中心を少し後方に移し、腹部・背中の丸みを調整。
- ローカルChromeで側面を目視確認。肩位置は前回修正版を維持。iPhone実機未確認。
- 公開検証: be8a265 のPagesビルド成功。公開HTML・GLBは修正版と一致。公開ページの側面表示と停止操作を確認。証拠 verification/bear-depth-v4.png。

## 体型と服 / v0.1.4
- 肩位置を0.14下げ、胴体の幅・前後厚を増加。尾を後方へ調整。
- 茶色と生成りの横縞ベストを独立メッシュで追加。編み目は簡略化。
- ローカルChromeで正面・側面と袖ぐりを目視確認。iPhone実機未確認。
- 公開検証: 60e3a0f のPagesビルド成功。配信HTML・GLBの一致、公開ブラウザでベスト姿の表示とHELLO切替・停止を確認。証拠 verification/bear-vest-v5.png。

## 袖ぐり・襟 / v0.1.5
- 袖ぐりを楕円の開口と丸い縁取りへ変更。前襟を丸く下げ、生成りの縁取りを追加。
- ローカルChromeで正面・側面を目視確認。iPhone実機未確認。
- 公開検証: 6910f5d のPagesビルド成功。公開HTML・GLBはローカル修正版と一致。公開ページの正面襟・側面袖ぐりと停止操作を確認。証拠 verification/bear-neck-v6.png、verification/bear-armhole-v6.png。

## おしゃべり / v0.1.6
- セリフ入力・日本語読み上げ・停止と口パククリップを追加。APIキー不要。
- node --check成功。ローカルChromeでボタン操作後の発話終了イベントとUI復帰を確認。
- 実音声の聴取・iPhone Safari実機・発話中口パクの視認は未確認。自由AI会話は未実装。
- 公開検証: fcd3639 のPagesビルド成功。HTML・speech.js配信一致。公開モデル読み込みと「話して」操作後の終了イベント・UI復帰を確認。実音声の聴取は未確認。証拠 verification/bear-talk-v7.png。

## OpenCode双方向会話 / v0.2.0 / 2026-10-22
- HALO halo_opencode.py の現物を参照し、独立XDG・認証なし・無料モデル事前検査・DBによる実モデル/cost 0/完了検証を会話用に実装。HALO本体は読取のみ。
- 旧Museモデルは現行カタログにないため使用せず、現行の opencode/mimo-v2.6-flash-free に固定。有料フォールバックなし。
- 実モデルから日本語の返答を取得。CLIとHTTP API、HTTPSブラウザの実返答を別々に確認。記録上cost 0、モデル一致、finish stop。
- 6テスト成功: 料金・モデル証明・入力・HTTP認証/Origin/JSON境界・OS sandboxによる実ファイル読書き拒否。JavaScript構文確認成功。
- Tailscaleは初回Stopped、ユーザーが起動後にRunningを確認。既存Serve設定を維持し、HTTPS:8447 → localhost:8870 を追加。会話キー付き専用リンクは .runtime/chat/private-link.txt のみ保存。
- 作業中の一時Cloudflareトンネルは停止済み。OpenCode自体は外部へ公開していない。
- Tailscale経由のブラウザで「タロウ」と伝えたあと名前を聞き、会話履歴に基づく返答を確認。390px幅の会話UIも目視確認。
- 証拠: verification/opencode-live-summary.json、verification/opencode-conversation-mobile.png（ローカルのみ）。
- iPhone実機のマイク認識・実際の音声聴取・発話中口パクは未確認。ブラウザ側の読み上げ終了イベントとUI復帰は確認。
- GitHub Pagesの既存読み上げページと異なり、双方向会話にはMac・会話サーバー・Tailscaleの起動が必要。Macスリープ・再起動時の自動復帰は未実装。

## iPhone接続の申告 / 2026-10-22
- ユーザーがSafariの「サーバが見つかりません」を報告。MacからのHTTPSページ200・API health正常・Tailscale Runningを再確認。
- iOS peerはOnline=trueだがActive=false、Tailscale pingはタイムアウト。Macでの確認はiPhoneからの到達確認の代わりにならない。
- 一時Cloudflare代替接続も試行したが接続前検査に失敗。未接続トンネルを停止し、代替リンクはユーザーへ渡していない。
- iPhone側のTailscale VPN接続状態を確認中。接続問題は未解決。
- ユーザーのiPhone画像でConnectedを確認後、Mac→iPhoneのTailscale pingがDERP(tok)経由51msで応答。直結は未成立だが中継経路は到達。HTTPSページ200を再確認。iPhone Safariの名前解決・ページ表示は引き続き未確認。

## iPhoneで使用後に固まる申告 / v0.2.1
- ユーザーがiPhoneでページを開けたことを確認。その後の固まりを申告。停止時の正確な状態は未特定。
- サーバーhealthは正常、調査時点でOpenCode推論プロセスなし。
- マイクのonend未通知でlisteningが解除されない経路を修正。毎回認識インスタンス作成、20秒解除、古いコールバック拒否、画面離脱時の停止を追加。
- 常時押せる復帰ボタン、待機取消、遅延返答の無視、入力文復元を追加。推論45秒・待機60秒・音声45秒の上限。
- 会話サーバーのみ再読込。HALOやTailscaleの既存サービスは停止していない。
- Nodeによる障害注入テストで終了通知欠落・遅延通知・リクエスト取消・画面離脱復帰を確認。Pythonの6安全テストも成功。
- Tailscale実画面で返答待ち中に復帰ボタンを押し、マイクと送信ボタンが再び使えることを確認。証拠 verification/chat-recovery-v2.png。
- iPhone実機での再発解消は未確認。端末側の全画面停止・メモリ不足などは未特定。

## 声の雰囲気 / v0.2.2
- 読み上げの高さ・速度を3種類から選択可能にし、初期値を少し高め・ゆっくりの「ふんわり」に変更。
- Nodeテストで3設定のSpeechSynthesisUtterance値と停止処理を確認。会話復帰テストも成功。
- Tailscale実画面で設定切替と読み上げ終了後の復帰を確認。証拠 verification/cute-voice-v3.png。
- iPhoneの実音声のかわいらしさ・聴感は未確認。追加の有料音声APIは使用していない。

## 読み上げ速度 / v0.2.3
- ユーザー希望で全プリセットをゆっくりに調整。声の高さは維持。端末実音声の聴感は未確認。

## 着せ替え / v0.3.0
- ユーザーの作業停止指示後、服の着せ替えという新規指示へ移行。音声調整は追加せず、既に保存済みの状態を維持。
- ベスト・セーター・Tシャツ・服なしのモデルと選択UIを追加。元のモデルは維持。
- 4モデルのGLB長・シーン構成・3アニメーション保持を検査。
- Tailscaleブラウザで4種類の選択と描画、着替え後のHELLO切替、ベストへ戻せることを確認。証拠 verification/wardrobe-sweater.png。
- 会話・読み上げの既存テスト成功。iPhone実機での着せ替えと会話同時操作は未確認。
- 公開検証: bab0173 のPagesビルド成功。公開HTML・wardrobe.js・セーターGLBがローカル成果物と一致。Tailscale配信のJS一致も確認。
