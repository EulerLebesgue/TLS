# 深層学習day1
- ディープラーニングの目的はプログラムでモデルを明示するのではなく、中間層を重ね重みとバイアスを学習させることで自動的にモデルを作成する。
## Section1 入力層～中間層
- 入力層と中間層で一つのユニットと考える。
- 中間層は何層でも重ねることができる。
- 数字で置き換えられるものはどのようなものでも入力として扱うことができる。
- 入力と重みとバイアスの線形結合はPythonでnp.arrayとnp.dotで簡単に実装できる。まんま一次関数の直線式と変わらない。
### 確認テスト
中間層入力
```
u = np.dot(x, W) + b
```
中間層出力(活性化関数はReLu関数)
```
z = functions.relu(u)
```
### 実装
パラメータの初期化の種類
```
#0でしきつめ
W = np.zeros(2)
#1 でしきつめ
W = np.ones(2)
#0-1の値で敷き詰め(小数)
W = np.random.rand(2)
# 5までの整数でしきつめ
W = np.random.randint(5, size=(2))
# -5から5までの範囲で出力　random.rand()で0-1の乱数を生成 
b = np.random.rand() * 10 -5
```
ReLuじゃなくて、シグモイドを使うことも可能。もちろん出力は0-1
```
z = functions.sigmoid(u)
```
結果：0.9484770701710731
## Section2 活性化関数
- 線形の定義は加法性と斉次性を満たすこと。
- 活性化関数で、次の入力の強弱を設定することができる。
- 中間層用の活性化関数は以下
- - ステップ関数　最近はあまり使われていない。線形分離可能な問いしか使えない。
- - シグモイド関数　ステップ関数の連続版のようなもの。勾配消失問題を起こしやすい。
- - ReLU関数　0より大きい入力に対して、恒等写像を返す。勾配消失とスパース化に貢献。
### 確認テスト
順伝播（単層・複数ユニット）中間層の出力箇所
```
z = functions.sigmoid(u)
```
### 実装
それぞれの活性化関数の定義。ReLuは場合分けと使わなくても最大値で記述できる。
```
### シグモイド関数
def sigmoid(x):
    return 1/(1 + np.exp(-x))

# ReLU関数
def relu(x):
    return np.maximum(0, x)

# ステップ関数（閾値0）
def step_function(x):
    return np.where( x > 0, 1, 0) 
```
重みが配列となっても初期化可能。ベクトルと大差ない
```
#W = np.zeros((4,3))
W = np.ones((4,3))
W = np.random.rand(4,3)
W = np.random.randint(5, size=(4,3))
```
## Section3 出力層
### 中間層と出力層の出力の役割について
- 中間層：閾値の前後で、出力の強弱を調整。
- 出力層：出力の比率はそのままに変換。分類問題においては総和が１となるように変換する。
- 出力層の活性化関数は以下
- - ソフトマックス関数：多クラス分類問題で利用。誤差関数は交差エントロピーを利用
- - 恒等写像：回帰問題で利用。誤差関数は二乗和誤差
- - シグモイド関数：２値分類問題で利用。誤差関数は交差エントロピーを利用
### 確認テスト
2乗和誤差について
- 二乗和誤差でないと、異符号の誤差が打ち消しあって誤差を表すことができないために、二乗する。係数の1/2は微分計算のためのものであり、本質的ではない。
ソフトマックス関数について
- 出力は配列。np.exp(x)はスカラーではなくベクトル値。np.sum(np.exp(x))は総和なのでスカラー
交差エントロピーについて
- 真数部分が０とならないように微小な値を加えておく。
`y[np.arange(batch_size), d] + 1e-7)` 
- 総和の形式だが、d_iは正解のラベルのみ１・その他は０の場合(One-Hot-Vector)、実質的に返すのは正解についての対数値。

### 実装箇所
平均二乗誤差(MSE)
```
def mean_squared_error(d, y):
    return np.mean(np.square(d - y)) / 2
```

ソフトマックス関数
```
def softmax(x):
    if x.ndim == 2:
        x = x.T
        x = x - np.max(x, axis=0)
        y = np.exp(x) / np.sum(np.exp(x), axis=0)
        return y.T

    x = x - np.max(x) # オーバーフロー対策
    return np.exp(x) / np.sum(np.exp(x))
```
交差エントロピー:本質的な出力は、return文の箇所
```
def cross_entropy_error(d, y):
    if y.ndim == 1:
        d = d.reshape(1, d.size)
        y = y.reshape(1, y.size)
        
    # 教師データがone-hot-vectorの場合、正解ラベルのインデックスに変換
    if d.size == y.size:
        d = d.argmax(axis=1)
             
    batch_size = y.shape[0]
    return -np.sum(np.log(y[np.arange(batch_size), d] + 1e-7)) / batch_size
```
## Section4 勾配降下法
深層学習の目的は、精度を高めるパラメータを求めること。そのため結果から、誤差の分だけパラメータを修正する。  
学習の際には学習率によって、学習の精度が大きく変わる。
- 学習率が大きすぎる場合：解にたどり着かず、発散する。
- 学習率が小さすぎる場合：学習が遅い。また局所極小解に捕らわれやすい。
入力 - 出力 - 誤差の計算 - パラメータの更新という一つの流れをエポックという。
### 勾配降下法
全サンプルの平均誤差を計算する。
### 確認テスト
コードの記載箇所
- 勾配の更新式
`network[key]  -= learning_rate * grad[key]`
- 微分の計算式
`grad = backward(x, d, z1, y)`
これは一気に更新を行っている。  
この中でも特に微分の関数の計算式は  
`delta2 = functions.d_mean_squared_error(d, y)`
### 学習率についてコードで遊んで確認
学習率を0.0001,0.5とかにすると全く誤差が収束しない。  
### 確率的勾配降下法
ランダムに抽出したサンプルの誤差を計算。利点は次の三点
- データが冗長な場合の計算コストの削減
- 鞍点への収束を回避しやすい
- オンライン学習が可能。
### 実装箇所
データセットからランダムにデータを抽出している。
```
random_datasets = np.random.choice(data_sets, epoch)
```
### ミニバッチ勾配降下法
ランダムに分割したデータの集合に属するサンプルの平均誤差。利点は次  
確率的勾配降下法のメリットを損なわず、計算機の計算資源を有効利用できる。このため、CPUを利用したスレッド並列化やGPUを利用したSIMD並列化

### 確認テスト(オンライン学習とは)
データをすべて学習させるのではなく、その都度学習させる。そのため、すべてのデータをそろえる必要がない。
### 数値微分の実装箇所
本質的な箇所は`grad[idx] = (fxh1 - fxh2) / (2 * h)`微分という概念操作を行うことができないので、近似的に計算する。
```
def numerical_gradient(f, x):
    h = 1e-4
    grad = np.zeros_like(x)

    for idx in range(x.size):
        tmp_val = x[idx]
        # f(x + h)の計算
        x[idx] = tmp_val + h
        fxh1 = f(x)

        # f(x - h)の計算
        x[idx] = tmp_val - h
        fxh2 = f(x)

        grad[idx] = (fxh1 - fxh2) / (2 * h)
        # 値を元に戻す
        x[idx] = tmp_val

    return grad
```
## Section5 誤差逆伝搬
## 誤差の計算
数値微分(パラメータに微小な値の加えたものと引いたものの差をとって、微小量の２倍で割る。)を用いる。  
しかし入力層から出力層に向けての計算をすべての層の重みに対して行うので、計算量が多くなる。(順伝搬)  
そのため、誤差逆伝搬法を使う。
## 誤差逆伝搬とは
産出された誤差を、出力層側から順に微分し、入力層に向かって伝搬していく。各パラメータの微分値を解析的に計算する。そのため、不要な再帰計算を避けることができる。  
実現するために微分の連鎖律を用いる。  
### 確認テスト(再帰的な処理を避けている箇所。)
```
delta2 = functions.d_mean_squared_error(d, y)
```
### 実装(誤差逆伝搬の処理)
出力層の活性化関数が1である少し特殊な状況であることに注意
```
# 誤差関数の偏微分
    delta2 = functions.d_mean_squared_error(d, y)
# b2の勾配更新量(bが定数項なので微分すると1となるのでシンプル)
    grad['b2'] = np.sum(delta2, axis=0)
# W2の勾配更新量(中間層の入力を重みで微分すると入力そのもの)
    grad['W2'] = np.dot(z1.T, delta2)
# いままでの更新と中間層の活性化関数の微分の連鎖律
    delta1 = np.dot(delta2, W2.T) * functions.d_relu(z1)
    delta1 = delta1[np.newaxis, :]
# b1の勾配更新量
    grad['b1'] = np.sum(delta1, axis=0)
    x = x[np.newaxis, :]
# W1の勾配更新量(中間層の入力を重みで微分すると入力そのもの)
    grad['W1'] = np.dot(x.T, delta1)
 ```
### 計算速度
処理速度と値段は次の関係。CPU < GPU <FPGA < ASIC(TPU)TPUはクラウドのものを間借りする。
### 入力層の設計
入力層としてとるべきでないデータ
- 欠損値が多いデータ
- 誤差の大きいデータ
- 出力を加工した情報　生のデータから出力を得るニューラルネットワークをエンドtoエンドという。
- 連続性のないデータ
- 無意味な数が割り当てられているデータ
### 欠損値の取り扱い
- ゼロ詰め
- 欠損値を含む集合を除外
- 入力として採用しない。
### 正規化と正則化
正規化は入力を0-1に収める。(入力の最大値で割る。)  
正則化は平均0、分散１のガウス分布に収める。
# 深層学習day2
## Section1 勾配消失問題
誤差逆伝搬法が階層に進んでいくにつれて、勾配がどんどん緩やかになる。そのため学習によるパラメータ更新が進まなくなる。  
学習しても正解率が上がらない、連鎖律で伝わる結果が0-1の間をとるため、積をとると値が小さくなる。


### 対策1　活性化関数の工夫
- ReLu関数：0以上の時、y=x,0未満の場合は0を返す関数。勾配消失問題およびスパース化に貢献する。
- - この関数により、重み更新に貢献しない重みの更新を行わない。
### 実装
活性化関数がシグモイド関数だと学習がうまくいかない。ReLuだとうまくいっている。過学習も起きてなさそう。
### 対策2　初期値の設定方法
重みの初期値は乱数によって設定する。
#### Xavierの初期値
正規分布をとった後、前のlayerのノードの平方根で割る。S字カーブの活性化関数に対して有効
実装例
```
    network['W1'] = np.random.randn(input_layer_size, hidden_layer_1_size) / (np.sqrt(input_layer_size))
    network['W2'] = np.random.randn(hidden_layer_1_size, hidden_layer_2_size) / (np.sqrt(hidden_layer_1_size))
    network['W3'] = np.random.randn(hidden_layer_2_size, output_layer_size) / (np.sqrt(hidden_layer_2_size))
```
np.random.rand()は標準正規分布に沿った乱数を返す。変数の指定で出力される行列のサイズを決定する。
### 実装結果
活性化関数がシグモイド関数でもある程度成果が出る。ReLuほどではない。  
ReLuに対してこの初期値を使うと、逆に精度が落ちる。
#### 比較
- 正規分布による初期化：出力値が0または1に集中する。勾配消失が起きやすい
- 正規分布の標準偏差を極端(0.01)に小さくする。出力値が0.5に集中する。表現が失われ学習できていない。
#### Heの初期値
正規分布の重みに2/ｎの平方根をかける。nは前層のノード数。ReLu関数に対して有効
実装例
```
    network['W1'] = np.random.randn(input_layer_size, hidden_layer_1_size) / np.sqrt(input_layer_size) * np.sqrt(2)
    network['W2'] = np.random.randn(hidden_layer_1_size, hidden_layer_2_size) / np.sqrt(hidden_layer_1_size) * np.sqrt(2)
    network['W3'] = np.random.randn(hidden_layer_2_size, output_layer_size) / np.sqrt(hidden_layer_2_size) * np.sqrt(2)
```
#### 比較
- 正規分布による初期化：出力値が0に集中する。
- 正規分布の標準偏差を極端(0.01)に小さくする。出力値が0に集中する。
### 実装結果
ReLuに対してはかなり早い段階から学習が収束する。シグモイドに対しては一定以上の精度が出ない
### 対策3　バッチ正規化
ミニバッチ単位で、入力値のデータの偏りを抑制する手法  
※ミニバッチサイズは処理能力で目安がある。GPUは64枚まで、TPUは256枚まで  
統計の標準的な正規化(入力から平均を引いた後、標準偏差に微小値を加えたもので割る。)をおこなって、パラメータを移動させる。
### 確認テスト
シグモイド関数f(x)=1/（1+exp(-x))より、f(0)= 0.5  
f'(x) = f(x)(1-f(x))よりf'(0) = 0.25  
ここで、f'(x) = -(f(x)-0.5)^2 + 1/4、f(x)が単調増加関数、0<f(x)<1よりf'(0)が最大値。よって逆伝搬の時最大値が0.25のため、積をとると限りなく0に近づいていく。
### 確認テスト
重みをすべて0(同じ値に設定する)と重みの値が均一に更新される。多数の重みをもつ意味がない。
### 例題チャレンジ
ミニバッチサイズで処理を進める実装。バッチサイズ分だけずらしてスライシングする。
```
for epoch in range(n_epoch):
    shuffle_idx = np.random.permutation(N)
    for i in range(0,N,batch_size):
        i_end = i + batch_size
        batch_x,batch_t = data_x[i:i_end],data_t[i:i_end]
```
## Section2 学習率最適化手法
初期の学習率を大きく設定し、徐々に学習率を小さくしていく。(学習率を可変させる。)
### モメンタム
前回の重みに慣性量をかけて値から、学習量と誤差の微分値をかけたものを引き、それを現在の重みに加える。  
大域的局所解に到達しやすい。極小解に捕らわれると一気に学習が進む。株価の移動平均に近い動きをする。  
実装箇所
```
for key in params.keys():
    self.v[key] = self.momentum * self.v[key] - self.learning_rate * grad[key] 
    params[key] += self.v[key]
```
### AdaGrant
変数に誤差関数の微分値の二乗を保持するものを用意して、それを用いて学習率を更新する。  
勾配の緩やかな斜面に対して、最適値に近づける。  
学習率が徐々に小さくなるので、鞍点問題を引き起こすことがある。  
実装箇所
```
for key in params.keys():
    self.h[key] += grad[key] * grad[key]
    params[key] -= self.learning_rate * grad[key] / (np.sqrt(self.h[key]) + 1e-7)
```
### RMSProp
AdaGrantの式に回の誤差の二乗と、前回までの勾配情報をどの程度使用するかを変える。  
局所的最適解にはならず、大域的最適解となる。  
ハイパーパラメータの調整が必要な場合が少ない。  
実装箇所
```
for key in params.keys():
    self.h[key] *= self.decay_rate
    self.h[key] += (1 - self.decay_rate) * grad[key] * grad[key]
    params[key] -= self.learning_rate * grad[key] / (np.sqrt(self.h[key]) + 1e-7)
```
### Adam
モメンタムとRMSPropのいいとこどりをしたような手法。  
実装箇所
```
def update(self, params, grad):
    if self.m is None:
        self.m, self.v = {}, {}
        for key, val in params.items():
            self.m[key] = np.zeros_like(val)
            self.v[key] = np.zeros_like(val)
    self.iter += 1
    # lr_t = e * sqrt(1-b_2)/(1-b_1)
    
    lr_t  = self.learning_rate * np.sqrt(1.0 - self.beta2 ** self.iter) / (1.0 - self.beta1 ** self.iter)         
        
    for key in params.keys():
        # m_t+1 = m_t + (1-b_1) * (g - m_t )
        self.m[key] += (1 - self.beta1) * (grad[key] - self.m[key])
        # v_t+1 = v_t + (1-b_2) * (g^2 - v_t )
        self.v[key] += (1 - self.beta2) * (grad[key] ** 2 - self.v[key])
        # w_t+1 = w - lr_t * m_t+1 / sqrt(v_t+1) + f
        params[key] -= lr_t * self.m[key] / (np.sqrt(self.v[key]) + 1e-7
```
### 実装演習
SDGは明らかに未学習。それ以外は学習できている。今回はRMSPropとAdamだとRMSPropの方がよく見える
#### バッチ正規化を行うとどう変わるか？
- SDGでもバッチ正規化だけで7割程度の正答率が得られる。
### 活性化関数・初期値の設定
- ReLu,Heの組み合わせでSDGでも8割強の正解率が出る。バッチ正規化をしてもしなくても同じくらいの精度。落ち着くのが少し早いか？
- RMSPropだとほぼ満点に近い。しかも最初から正答率が高い。
## Section3 過学習
### 過学習とは
テスト誤差と訓練誤差とで学習曲線が乖離すること。要因としては
- パラメータが多い
- パラメータの値が適切ではない。
- ノードが多い
自由度が高いためおきるので、対策はネットワークの自由度を抑える。

### L1正則化、L2正則化
コンセプトはWeight decay(荷重減衰)
- 過学習は一部の重みが極端に大きくなることで、特定の入力に過剰に反応してしまうことによる。
- そのため、正則化項（どちらかというと条件か？）を加算することで、重みを抑制する。
### L1正則化(Lasso正則)
罰則項としてL1ノルムを採用している。(ひし形)そのため、最適解を得た場合、重みが0となる箇所があることがある。(スパース推定)  
実装箇所
```
#誤差関数にL1ノルム(絶対値の総和)を加える
weight_decay += weight_decay_lambda * np.sum(np.abs(network.params['W' + str(idx)]))
loss = network.loss(x_batch, d_batch) + weight_decay
```
### L2正則化
罰則項としてL1ノルムを採用している。(円)最適解を得た場合、重みが0とならない縮小推定。  
実装箇所
```
#誤差関数にL2ノルム(2乗の総和の平方根)を加える
weight_decay += 0.5 * weight_decay_lambda * np.sqrt(np.sum(network.params['W' + str(idx)] ** 2))
loss = network.loss(x_batch, d_batch) + weight_decay
```
### 例題チャレンジ
L2正則化で勾配更新(微分)を行う。その結果、係数が吸収されてgrad += rate * paramとなる。　　
L1正則化で勾配更新(微分)を行う。結果は定数(-1,0,1)となるのでnumpyのsign(param)(符号関数)を用いる。
### ドロップアウト
ランダムにノードを削除して学習させること。そのため、データ量を変化させずに、異なるモデルを学習させていると解釈できる。  
実装箇所
```
### dropout_ratioを超える重みはdropout_ratioと重みの積をとる。dropout_ratioの値が小さければ過剰に反応する。
self.mask = np.random.rand(*x.shape) > self.dropout_ratio
return x * self.mask
```
### 実装演習
- L1ノルムだけだと、地震計みたいな挙動となる。学習ができていない。
- weigth_decay_lambda：正則化の強さを変えると過学習が抑えられない、または未学習になる。意外と些細な変化で結果が変わるので調整が難しい。解析的には計算できないのか？
- dropout_ratioを小さくすると、テストの正答率が上がる。ほとんどの重みが消えてそうだが。大きくすると未学習
- optimaizerがadamだとしても、適切に決めないと学習がうまくいかない

## Section4 畳み込みニューラルネットワークの概念
画像処理によく用いられるネットワーク。次元的なつながり(データが近い箇所で入力が似ている)があるものなら応用が利くもの。
- 単一チャンネル:各次元の入力がスカラーのもの(例(2次元)：音声データのフーリエ変換(時刻、周波数、強度))
- 複数チャンネル：次元の入力がベクトルのものが存在(例(2次元)：カラー画像(x、y、(R,G,B)))
全結合層は今まで学習したニューラルネットワークのこと  
全結合層までは次元の情報を保ったままの出力を得る。(特徴量の抽出機能)  
全結合層からは人間のほしい処理へと変換する作業。
### 畳み込み層
チェンネルに対して、フィルターをずらしながら出力を得る。その後はバイアスを加え活性化関数の処理を行う。  
全結合層では各チャンネルの関連性が学習に反映させられない。  
フィルターにより、画像であれば周辺の情報を取得しながら処理を行うことになるので、次元間の関係を保存できる。  
実装する際には処理を高速化するために、読み込んだ要素を行、または列で並べる。これにより、重みのドット積が簡単に計算できる。
出力画像のサイズの公式があるが、覚えにくいので等差数列の公式等から導くのが安全。
### バイアス
フィルターで処理した情報に定数を加える。ニューラルネットワークのバイアスと同義。
### パディング
出力画像が入力画像と同じサイズになるように、入力を押し広げる
- すべて0で埋める。
- 隣と同じ数字を入れていく。
### ストライド
フィルターが一度に動く量を決める。
### チャンネル
フィルターの数を決定する要素。
### 実装演習
畳み込み層の計算
```
self.layers['Conv1'] = layers.Convolution(self.params['W1'], self.params['b1'], conv_param['stride'], conv_param['pad'])
self.layers['Relu1'] = layers.Relu()
self.layers['Pool1'] = layers.Pooling(pool_h=2, pool_w=2, stride=2)
self.layers['Affine1'] = layers.Affine(self.params['W2'], self.params['b2'])
self.layers['Relu2'] = layers.Relu()
self.layers['Affine2'] = layers.Affine(self.params['W3'], self.params['b3'])
```
高速化の工夫  
im2col
```
# 軸を取り換えて、フィルターで読み取った範囲を出力する
col = col.transpose(0, 4, 5, 1, 2, 3)
# 上記の内容を一列に並べる
col = col.reshape(N * out_h * out_w, -1)
```
col2im:元の配列に戻す  
```
col = col.reshape(N, out_h, out_w, C, filter_h, filter_w).transpose(0, 3, 4, 5, 1, 2) # (N, filter_h, filter_w, out_h, out_w, C)
```
### プーリング層
フィルター内で特定の操作を行い出力する。フィルター内の出力を取得(MaxPooling)、平均値を取得(AvgPooling)
実装確認。ここでもプーリングの演算を高速化するために、行列の変換を行ったのち、最大値をとる
```
 col = im2col(x, self.pool_h, self.pool_w, self.stride, self.pad)
 # プーリングのサイズに合わせてリサイズ
 col = col.reshape(-1, self.pool_h*self.pool_w)
        
 #maxプーリング
 arg_max = np.argmax(col, axis=1)
 out = np.max(col, axis=1)
 out = out.reshape(N, out_h, out_w, C).transpose(0, 3, 1, 2)
```
## Section5 最新のCNN
### AlexNet
5層の畳み込み層およびプーリング層など、それに続く3層の全結合層から構成される。  
全結合層への処理
- Ftatten そのまま一列に数字を並べる
- Global Max Pooling チャンネルの中で最大値を出力する。  
- Global Avg Pooling チャンネルの中の平均値を出力する。  
サイズ4096の全結合層の出力に過学習を防ぐためドロップアウトを使用している。
### 確認テスト
フィルターサイズの畳み込んだ際の出力は等差数列の公式を持ちいることで暗記をしなくてよい。
### AlexNetの有用性について
- 2012 年前までの画像分類では人が特徴量を設計していた。いかに特徴量を決めるかが大切だった。
- それが、2012年にAlexNetにより、十分なデータが存在すれば、学習によって機会が自動的に特徴量を抽出することができるようになった。
