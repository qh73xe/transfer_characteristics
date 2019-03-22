=======================================
transfer_characteristics
=======================================

スピーカ計測用簡易ツールキットです．

厳密にしようとする気持ちは毛頭ないのですが，
種々信号処理の練習および，なんかスピーカーやヘッドフォンの計測に
興味を持ってしまったので作成してみました．

基本的には GUI ツールですが，
種々関数を使用できるライブラリとしても機能するかと思います．

GUI では以下のような解析を行えます．

.. image:: https://raw.githubusercontent.com/qh73xe/transfer_characteristics/master/figs/HD650.png
   :scale: 40%
   :align: left

基本的な使い方
=======================================

事前準備
~~~~~~~~~~~~~~~~~~~~~~~~~~~

このツールを起動させるには以下の前準備が必要です::

   $ pip3 install -r requirements.txt

その後, 以下のコマンドから起動します::

   $ python3 ./transfer_characteristics/main.py

SPL の計測
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. まずは, マイクと計測したいスピーカー，ヘッドフォンを PC に接続してください．
2. その後，上記の手順で GUI を起動します．
3. ツールの起動に成功したら右上の Gen signals... ボタンをクリックします:
   すると，画面下に 2 種類の画像が表示されます

   .. image:: https://raw.githubusercontent.com/qh73xe/transfer_characteristics/master/figs/gen.png
      :scale: 40%
      :align: left

   一つ目は生成した音源信号で, 二つ目は，その周波数特性(というか信号全体のパワースペクトル)になります．
   周波数特性に関して，縦軸の単位はデシベルで，横軸は周波数です．

   - つまり，横軸に関してはログスケールではありません．

   作成するスイープ音は，持続時間と, 再生する周波数の開始，修了を設定することができます．

   - それぞれ，右上の入力欄に適当な値をいれてください．

4. 続いて, 左上の Recording ボタンをクリックします．

   すると，上で作成したスイープ音が再生され，同時にマイク収録が行われます．

   マイク収録に成功すると，画面下にある図表示領域に，収録した音源の SPL の結果が図示されます．

Example
=======================================

.. list-table:: 計測例
   :widths: 15 10 10
   :header-rows: 1

   * - 画像
     - 対象
     - その他収録環境
   * - .. image:: https://raw.githubusercontent.com/qh73xe/transfer_characteristics/master/figs/HD650.png
          :scale: 40%
     - SENNHEISER HD650
     - マイク: Roland CS-10EM, DAC: DENNON DA-300USB
   * - .. image:: https://raw.githubusercontent.com/qh73xe/transfer_characteristics/master/figs/HD598SR.png
          :scale: 40%
     - SENNHEISER HD598SR
     - マイク: Roland CS-10EM, DAC: DENNON DA-300USB


できること
=======================================

- SPL: 周波数特性の計測

できるようにすること
=======================================

- 基本機能:
   - 音源ファイルの読み込み
- Phase: 位相特性
   - 正弦波音源を生成する関数の作成
- IR: インパルス応答
- Distortion: 歪み率
- GD: 群遅延特性(位相特性の微分)
