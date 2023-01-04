# thesis-bst

## 概要
神戸大学システム情報学研究科の卒論・修論用に参考文献リストを出力するスクリプトです。
.bibファイルを入力すると、latexのthebibliography環境にそのままペーストできるbibitemのリストを出力します。

## 動作環境
- Python 3.9以上
- (pytest 7.2.0)

使うだけならpytestは要りません。
開発の場合も、外部パッケージはpytestしか使っていないので、適当なPythonでvenv等を作って手でpip installしたら事足りると思います。

Python 3.9以上というのは`dict[foo, bar]`の型アノテーションのためなので、古いPythonで動かしたければ適当に削ってください。

## 使い方
1. 参考文献を普通のbibtexの流儀に従って.bibファイルにまとめる
2. `python bib2bibitem.py <.bib file> -o <output file>`を実行する
3. output fileを論文内でinputする（参考：test.tex）

`-o`オプションを省くと結果を標準出力に出力します。簡単な確認や、手でのコピペを想定した動作です。

## 注意
bibitemのソートはしません。  
入力の.bibファイルの記述順を保証するようには作っていない（現状そうなっているかもしれないが、わざわざそうしたわけではない）ので、出力物を適当に入れ替えるのが確実です。
研究科の『手引き』では著者名アルファベット順・本文出現順等の指定は無かったと思いますが、何らかの基準でソートされていたほうが親切だと思います。

## テスト
```
pytest
```
あんまりちゃんとテストしていません。

## 書式情報
2022年12月改訂版『修士論文および卒業論文の手引き』
http://www.csi.kobe-u.ac.jp/current_students/kyougaku/file/InstructionR4.pdf