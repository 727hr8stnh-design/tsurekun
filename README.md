# つれくん 3Dダンスビューアー

公開対象は docs/。GitHub Pagesのmainブランチ /docs から配信。

ローカル起動: `python3 -m http.server 8768 --directory docs --bind 127.0.0.1`

指1本で回転、2本指で拡大縮小。ダンスボタンで切替、一時停止で停止。

model-viewer 4.1.0 (Apache-2.0) を vendor/ に同梱。モデルは既存つれくん素材から取得。

公開URL: https://727hr8stnh-design.github.io/tsurekun/

Safari対応範囲: https://modelviewer.dev/ （iOS/macOS Safariの直近2メジャー版）。iPhone実機での検証は未実施。

## クマとの双方向会話（OpenCode・無料モデル）

`python3 chat/start.py --base-url https://<MacのTailscale名>:8447` でローカル会話サーバーを起動。
Tailscaleが起動中の場合は次の専用ポートを利用する。

`/Applications/Tailscale.app/Contents/MacOS/Tailscale serve --bg --https=8447 http://127.0.0.1:8870`

会話画面は `https://<MacのTailscale名>:8447/bear/chat.html`。
初回は `.runtime/chat/private-link.txt` の専用リンク（秘密のアクセスキー付き）を使う。キーは外部公開しない。
マイクを許可して「話しかける」、または文字を入れて「送る」。返事が読み上げられない端末では下の「話して」を押す。

固定モデルは `opencode/mimo-v2.6-flash-free`。無料判定・実モデル・cost 0の検証に失敗したら停止する。
Macが停止・スリープ中は利用不可。会話の文字はOpenCodeのモデル提供元へ送信され、ローカルのOpenCode DBにも保存される。
履歴リセットは画面内の履歴だけを消す。DBの削除は自動実行しない。

停止: `python3 chat/stop.py`。Tailscale側のこのポートだけを外す場合:
`/Applications/Tailscale.app/Contents/MacOS/Tailscale serve --https=8447 off`

検証: `python3 -m unittest discover -s chat -p 'test_*.py' -v`
GitHub Pagesは静的ホスティングのため、OpenCodeの会話サーバーは動かせない。
