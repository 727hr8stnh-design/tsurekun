# つれくん 3Dダンスビューアー

公開対象は docs/。GitHub Pagesのmainブランチ /docs から配信。

ローカル起動: `python3 -m http.server 8768 --directory docs --bind 127.0.0.1`

指1本で回転、2本指で拡大縮小。ダンスボタンで切替、一時停止で停止。

model-viewer 4.1.0 (Apache-2.0) を vendor/ に同梱。モデルは既存つれくん素材から取得。
