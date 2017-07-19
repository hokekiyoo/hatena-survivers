## はてなサバイバー

- はてなブロガーは、どのくらいの期間活発に活動するのか
- ずっと続けられる人はいるのか

## 使い方

次の順番で使う
- `get_hatena_blogger.py`
- `get_info.py`
- `analyze.ipynb`

### `get_hatena_blogger.py`

- はてなブロガーを集めてくる
- デフォルトは1000人
- 数を増やしたい/減らしたいときは下記のようにオプション実行

```
python get_hatena_blogger.py -m 2000
```

- 出力は`blog_url.csv`に吐き出される

### `get_info.py`

- 集めたurlから必要情報を抜き出す
    - url
    - 始めた年月
    - 継続期間
    - 記事数
    - 読者数
- 特にオプションは用意していないので、下記

```
python get_info.py
```

- 出力は`blog_info.csv`に吐き出される

### `analyze.ipynb`
- blog_info.csvを分析する
    - 継続期間ヒストグラム
    - 読者ヒストグラム
    - 継続期間と読者数の相関

