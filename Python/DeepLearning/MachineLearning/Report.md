# 機械学習
## Chapter1 線形回帰モデル
- 回帰問題を解くための教師あり学習
- 与えられたデータを一次式で予測する。  
基本的には説明変数がn次元、目的変数が１次元する。  
出力を多次元にすることも可能  
誤差項は偶発誤差だけでなく、隠れた説明変数の項が乗っていることがある。
目的変数に対して、目的変数が少ないとき。
基本的に目的変数の次元より、重みの次元は低い
- 誤差(最小二乗誤差)を最小とするのが目的
- - ただし外れ値に弱い。影響されやすい

### 補足 決定係数
- 推定された回帰式の当てはまりの良さ（度合い）を表す。
- 0から1までの値をとる
- 1に近いほど、回帰式が実際のデータに当てはまっていることを表しており、説明変数が目的変数をよく説明していると言える。

### ハンズオン
テーマ：bostonの住宅価格モデル  
sklearnを使うと簡単に回帰・分類・クラスタリングで同様のインターフェイスを使うことができる。
単線形回帰も重線形回帰も下記で予測できる。

``
model = LinearRegression()
model.fit(data, target)
model.predict([[7]])
``

単線形回帰と重線形回帰を比較した場合、重線形回帰の方が精度が若干良い
```
print('単回帰決定係数: %.3f, 重回帰決定係数 : %.3f' % (model.score(data,target), model2.score(data2,target2)))
```
単回帰決定係数: 0.483, 重回帰決定係数 : 0.542 

## Chapter2 非線形回帰モデル
- 非線形であるのは入力パラメータについて、重みについては線形。
- 線形回帰と異なるのは、入力を基底関数で射影した後に線形結合を行う点
- 学習後の重みの計算も線形回帰と本質は変わらない。
- 基底関数の影響が大きくなりすぎて、過学習を起こす可能性がある

### よく使われる基底関数
- 多項式関数(x^j)
- ガウス型基底関数(exp{(x-x_ave}^2/2h_i}
- スプライン関数/Bスプライン関数

### コード確認
sklearのKernelRidgeで基底関数を変更して回帰が使える
```
### ガウシアン基底関数
from sklearn.kernel_ridge import KernelRidge
clf = KernelRidge(alpha=0.0002, kernel='rbf')
```
多項式で次数をやみくもに上げても過学習が起きる
```
### 多項式関数
from sklearn.kernel_ridge import KernelRidge
clf = KernelRidge(alpha=0.0002, kernel='polynomial',degree=10)
```
### 未学習と過学習
- 未学習：学習誤差に対して、十分小さなモデルが得られない状態
- 過学習：学習誤差は小さいが、テスト集合誤差との差が大きい状態
ここでいう誤差は3つある。
- バリアンス：訓練データの選び方による誤差
- バイアス：モデルの表現力が不足していることによる誤差。
- ノイズ：データの測定誤差によるもの
#### バイアスとバリアンスのトレードオフ
単純なモデルではバイアスが低く、バリアンスが大きくなる。一方で複雑なモデルだとバイアスが大きく・バリアンスが小さい

### 過学習の対策
- 学習データの数を増やす(たくさん学習させる)
- 不要な基底関数を削除(表現力の抑止)
- 正則化(罰則項)により、重みパラメータの値を制限する。(表現力の抑止)

### 正則化の種類
- Rigde正規化：L2ノルム(重みの条件は2次元だと円周)の罰則項を追加。滑らかなためパラメータを0に近づけるような推定を行う
- Lasso正規化：L1ノルム(ひし形)の罰則項を追加。とがっているためいくつかのパラメータを0にする。(スパース化)

### モデルの汎化性能評価
- ホールドアウト法：データを学習用と検証用の２つに分けて一気に学習する。データ数が多い時には簡単。ただしデータ数が少ない時には使うべきではない。
- 交差検証法(クロスバリデーション)：データをｋ個に重複を許さず分割して、k-1個を学習用、1個を検証用に使う。これをk回繰り返す。このk回の学習の平均(CV値)で精度を見る
- ホールドアウト法とクロスバリデーションであれば、後者の方が精度が良い。たとえ前者の数値がよかったとしても後者の方が汎化性能が高い場合がある。

## Chapter3 ロジスティック回帰モデル
- 回帰には識別的アプローチ(直接確率を計算)・生成的アプローチ(ベイズの定理からを間接的に確率を計算)がある。ロジスティック回帰は識別的アプローチ
- 出力値は0か1の値とする。
- 線形結合で得た値を、出力が0から1の確率として捉えられるように関数をかませる。例えばシグモイド関数。xの係数を大きくするとステップ関数に近づく
- 尤度関数とする重みを探す。
- 桁落ちが起こる可能性があるため、実装では尤度関数を対数をとり計算する。
### 勾配降下法と確率的勾配降下法
通常の勾配降下法では1回の計算で、パラメータを１回更新する。しかしそれでは計算がメモリに乗らない。そのため確率的勾配降下法を用いる。
### モデル評価
- 再現率(Recall)：本当にPositiveの(TP+FN)からモデルがPositive(TP)と判定したものの割合(TP/TP+FN)
- - Positiveの抜け漏れを少なくしたい。（病気の検査指標など、陽性の患者は絶対に逃したくないなど）
- 適合率(Precision)：Positiveと予測したもの(TP+FP)から本当にPositive(TP)なものの割合(TP/TP+FP)
- - 見逃しを許容しても、Positiveの推定の正確さを上げたい（スパムメールなど、異常と判断されたものは確実に異常であってほしい）
- F値：RecallとPrecisionの調和平均。現場では3つを見比べることもある。
### 実装
覚えておくと使うときに便利な機能
```
#matplotlibをinlineで表示するためのおまじない (plt.show()しなくていい)
%matplotlib inline
```
1. 前処理。使わないデータの削除と欠損値の補完
```
### いらないデータを削除してnullの列を表示
titanic_df.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1, inplace=True)
titanic_df[titanic_df.isnull().any(1)].head(10)
### 新しい列を作成して、欠損値を中央値で補完
titanic_df['AgeFill'] = titanic_df['Age'].fillna(titanic_df['Age'].mean())
```
2. モデルの学習
sklearnからロジスティック回帰のモジュールをインポート。その後ロジスティック回帰モデルのインスタンスを生成して使用。  
APIなので、書き方が同じ。とても便利
```
from sklearn.linear_model import LogisticRegression
model=LogisticRegression()
model.fit(data1, label1)
```
3. 学習からわかること  
もちろん予測した結果はわかるが、`predict_proba()`で実際の確率が出力される。
これを使うと判断した確率がわかる。(運賃が62の人だとモデルが生と判断しても、確率は五分五分)
```
model.predict([[62]])
model.predict_proba([[62]])
```
array([[0.49978123, 0.50021877]])
4. あらたな特徴量を追加
性別を2値に分類して、階級を足し合わせる。(階級とレディーファースト)
```
titanic_df['Gender'] = titanic_df['Sex'].map({'female': 0, 'male': 1}).astype(int)
titanic_df['Pclass_Gender'] = titanic_df['Pclass'] + titanic_df['Gender']
```
上記の特徴量はうまく傾向を表しているので、よい特徴量

5. 交差検証と精度評価
テストデータ：訓練データを8:2に分割する。
```
traindata1, testdata1, trainlabel1, testlabel1 = train_test_split(data1, label1, test_size=0.2)
```
下記で回帰の結果を出力できる
```
metrics.classification_report(testlabel1, predictor_eval1))
```
※出力はマークダウンで加工している。
|item|precision|recall|f1-score|support|
|-|-|-|-|-|
|0|0.65|0.98|0.78|105|
|1|0.90|0.26|0.40|74|
|accuracy|||0.68|179|
|macro avg|0.78|0.62|0.59|179|
|weighted avg|0.76|0.68|0.62|179|

運賃と年齢から予測したもの。
運賃だけよりはましかなという感じ。生存のリコールが低く、生存の推定に漏れが多い。

下記で混合行列を出力可能。
```
from sklearn.metrics import confusion_matrix
confusion_matrix1=confusion_matrix(testlabel1, predictor_eval1)
```


## Chapter4 主成分分析
多変量データの持つ構造をより少数個の指標に圧縮することが目標(次元圧縮)
データの散らばりが残る(分散が最大化する)ような散らばり方を選択する。
ラグランジュ未定乗数法により、分散共分散行列の固有値と固有ベクトルが求める。
### 寄与率
元のデータの分散は、すべての主成分の総和に等しい。
- 寄与率：第ｋ主成分の分散が主成分の総分散にどれほどの割合を占めるのかを表したもの
- 累積寄与率：第1～第ｋ主成分の分散が主成分の総分散にどれほどの割合を占めるのかを表したもの
### ハンズオン
30次元のままロジスティック回帰を行う
```
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
# ロジスティック回帰で学習
logistic = LogisticRegressionCV(cv=10, random_state=0)
logistic.fit(X_train_scaled, y_train)
# 検証
print('Train score: {:.3f}'.format(logistic.score(X_train_scaled, y_train)))
print('Test score: {:.3f}'.format(logistic.score(X_test_scaled, y_test)))
print('Confustion matrix:\n{}'.format(confusion_matrix(y_true=y_test, y_pred=logistic.predict(X_test_scaled))))
```
Train score: 0.988
Test score: 0.972
Confustion matrix:
[89  1]
[ 3 50]]

主成分分析。n_componentsはcomponentsの数
```
pca = PCA(n_components=30)
pca.fit(X_train_scaled)
```

データを2次元に圧縮。
```
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.fit_transform(X_test_scaled)
```
ここで、二次元に圧縮したデータで学習してみる。
```
logistic1 = LogisticRegressionCV(cv=10, random_state=0)
logistic1.fit(X_train_pca, y_train)

# 検証
print('Train score: {:.3f}'.format(logistic1.score(X_train_pca, y_train)))
print('Test score: {:.3f}'.format(logistic1.score(X_test_pca, y_test)))
print('Confustion matrix:\n{}'.format(confusion_matrix(y_true=y_test, y_pred=logistic1.predict(X_test_pca))))
```
悪くない。
Train score: 0.965
Test score: 0.916
Confustion matrix:
[[83  7]
 [ 5 48]]

## Chapter5 アルゴリズム
### kNN法
教師あり学習。分類のタスク。ある点から近い順にk個の点を探し、そのk個の点が属している集合のうち最も多いものを割り当てる。(多数決)
### 実装部
sklearnは相変わらず一瞬で終わる
```
from sklearn.neighbors import KNeighborsClassifier
knc = KNeighborsClassifier(n_neighbors=n_neighbors).fit(X_train, ys_train)
```
numpyも単純
```
def knc_predict(n_neighbors, x_train, y_train, X_test):
    y_pred = np.empty(len(X_test), dtype=y_train.dtype)
    for i, x in enumerate(X_test):
        distances = distance(x, X_train)
### argsortで降順に並べて、近傍で指定した箇所まで取り出す
        nearest_index = distances.argsort()[:n_neighbors]
        mode, _ = stats.mode(y_train[nearest_index])
        y_pred[i] = mode
    return y_pred
```
### k-means法
教師なし学習。クラスタリング。分類したいクラスと初期値(クラスタの中心)を決めて、近い中心のクラスを割り当てる。その後中心を再計算するという手続きを繰り返す手法。
- 初期値(中心点)の位置により結果が大きく変わる。その解消のためk-means++法というのがある。
上記2つはどちらの手法も距離計算が入るので、計算コストが高い。
### 実装部分
sklearnだと一瞬で終わる
```
from sklearn.cluster import KMeans
model = KMeans(n_clusters=5)
labels = model.fit_predict(X)
```

numpyによる実装
```
# まず距離を定義。
def distance(x1, x2):
    return np.sum((x1 - x2)**2, axis=1)

#クラスター数と最大繰り返し回数を決める
n_clusters = 3
iter_max = 100

# 各クラスタ中心をランダムに初期化
centers = X_train[np.random.choice(len(X_train), n_clusters, replace=False)]

for _ in range(iter_max):
# 更新後の中心と比較するために更新前の中心を保存
    prev_centers = np.copy(centers)
    D = np.zeros((len(X_train), n_clusters))
    # 各データ点に対して、各クラスタ中心との距離を計算
    for i, x in enumerate(X_train):
        D[i] = distance(x, centers)
    # 各データ点に、最も距離が近いクラスタを割り当て。横方向のargminでindexを返す
    
    cluster_index = np.argmin(D, axis=1)
    # 各クラスタの中心を計算
    for k in range(n_clusters):
    ### 真偽値を計算
        index_k = cluster_index == k
        centers[k] = np.mean(X_train[index_k], axis=0)
    # 収束判定
    if np.allclose(prev_centers, centers):
        break
```
## Chapter6 SVM
- 教師あり学習。2値分類問題に適用。
### ハードSVM
- 与えられた集合を線形分離する超平面(2次元だと直線)を探す。この時データとのマージンが最大となる直線を探す。
- 決定境界に最も近い点(サポートベクター)以外は予測に影響を与えない。
- 上記からサポートベクターは2本存在する
### ソフトSVM
線形分離不能な問題へ対応するため、いくつかの誤差を許容する。そのために最適化問題にスラック変数を導入する。  
ペナルティ項の係数が誤差の許容度を表す。係数が大きいほど誤差を許さない。
### カーネル法
与えられた集合を線形分離する超局面(2次元だと曲線)で分離する。  
高次元空間に射影した場合、計算コストが上がるが、変換の選び方を工夫すれば変換の内積の関数のみ考慮すればよい(カーネルトリック)
有名なカーネル関数
- RBF関数(動径基底関数)：ガウシアン
- シグモイドカーネル
- 多項式カーネル
- 指数カーネル
- 線形カーネル(単なる内積)
### 実装
学習は最急勾配法で学習を行う。方法によってそれまでの処理は異なるが根本は同じ
```
for _ in range(n_iter):
    grad = 1 - H.dot(a)
    a += eta1 * grad
    a -= eta2 * a.dot(t) * t
    a = np.where(a > 0, a, 0)
```
予測部分も大きくは変わらない
```
サポートベクター(a=0)以外は予測に影響を与えないので取り除く。
index = a > 1e-6
support_vectors = X_train[index]
support_vector_t = t[index]
support_vector_a = a[index]

term2 = K[index][:, index].dot(support_vector_a * support_vector_t)
b = (support_vector_t - term2).mean()

xx0, xx1 = np.meshgrid(np.linspace(-5, 5, 100), np.linspace(-5, 5, 100))
xx = np.array([xx0, xx1]).reshape(2, -1).T

X_test = xx
y_project = np.ones(len(X_test)) * b
for i in range(len(X_test)):
    for a, sv_t, sv in zip(support_vector_a, support_vector_t, support_vectors):
        y_project[i] += a * sv_t * sv.dot(X_test[i])
y_pred = np.sign(y_project)
````


