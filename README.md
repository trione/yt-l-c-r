# これはなに？  
### ライブチャットの分単位の量を可視化するツール  
このツールは __ライブ配信済みの動画__ が持つ __ライブチャットのリプレイを抽出__ します  
そして __ライブチャットの量を分単位で計測しグラフとして表示__ します  
このグラフは __どの時間にどれ程のチャットが投稿されたのか__ を視覚的に理解するのを助けるでしょう  

<details><summary>ライブチャット？</summary>
Youtubeのライブ配信中に視聴者がリアルタイムで投稿・閲覧できるチャットのこと<br>
</details>  
<details><summary>ライブチャットのリプレイ？</summary>
過去のライブ配信のライブチャットを再現するもの<br>
ただし、投稿はできない、閲覧はできる
</details>

# 使い方
## インストール
#### 必要なもの[前提]
* Python>=3.5
* pip>=10.0.1

#### 必要なこと
* このリポジトリを download または clone する  
* freeze.txt の module を installする  
'pip install -r freeze.txt'  

## ツールの起動
#### 起動方法
* コマンドライン(コマンドプロンプト)から以下のコマンドを実行する  
'python gui.py'  
* 画面が立ち上がる  

#### 使用方法
* Youtubeで ライブ配信済み かつ ライブチャットのリプレイが見られる 動画 を開きます  
* GUIのテキスト入力欄に その動画のID を ctrl + v で 貼り付けます
<details><summary>[動画のIDとは]</summary>
例えば、ブラウザのURL欄に v=aB3defghi_k のような部分があります<br>
それが、動画のIDであり、v=[動画のID]となっています<br>
この場合、動画のIDは aB3defghi_k に当たります<br>
</details>
* すぐ下のボタンを押すとライブチャットのリプレイの抽出作業を始めます  
* 抽出作業が終わると、その結果のグラフが表示されます  
終わっても、グラフが表示されない場合は、Graphボタンを押すことでグラフが表示されます  

###### ※使用上の注意  
* __抽出時間は__ 動画の時間やチャットの量によって5~10分程度の __時間がかかります__  
(なので動画を見ながら結果を待つのが良いと思います)  
* Windows でボタンを押し実行した場合、GUIが(応答なし)状態になりますが、実際には動いています  
コマンドラインにプリントされる文でそれを確認できます  
* 動画の時間が長すぎると、途中で抽出作業を終えてしまうことがあり、全てのチャットを抽出できない場合があります  
