import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
# %matplotlib inline

import sklearn
from sklearn.decomposition import PCA

from pathlib import Path

Path().resolve()


# データの読み込みと確認
dir_name='somf_master_simulator_20201103/libs/datasets/real/beverage_data'
file_name = 'PCA_test_20201106.txt'
dir_path = os.path.join(os.path.dirname(Path().resolve()), dir_name)
file_path = os.path.join(dir_path, file_name)
df = pd.read_csv(file_path, sep="\t", index_col=0)


from pandas import plotting
plotting.scatter_matrix(df.iloc[:, 1:], figsize=(8, 8), c=list(df.iloc[:, 0]), alpha=0.5)
plt.title('01')
plt.show()

# 行列の標準化
dfs = df.iloc[:, 1:].apply(lambda x: (x-x.mean())/x.std(), axis=0)
dfs.head()

#主成分分析の実行
pca = PCA()
pca.fit(dfs)
# データを主成分空間に写像
feature = pca.transform(dfs)

# 主成分得点
pd.DataFrame(feature, columns=["PC{}".format(x + 1) for x in range(len(dfs.columns))]).head()

# 第一主成分と第二主成分でプロットする
plt.figure(figsize=(6, 6))
plt.scatter(feature[:, 0], feature[:, 1], alpha=0.8, c=list(df.iloc[:, 0]))
plt.grid()
plt.title('02')
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()

from pandas import plotting
plotting.scatter_matrix(pd.DataFrame(feature,
                        columns=["PC{}".format(x + 1) for x in range(len(dfs.columns))]),
                        figsize=(8, 8), c=list(df.iloc[:, 0]), alpha=0.5)
plt.title('03')
plt.show()

# 寄与率
pd.DataFrame(pca.explained_variance_ratio_, index=["PC{}".format(x + 1) for x in range(len(dfs.columns))])

# 累積寄与率を図示する
import matplotlib.ticker as ticker
plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
plt.plot([0] + list(np.cumsum(pca.explained_variance_ratio_)), "-o")
plt.xlabel("Number of principal components")
plt.ylabel("Cumulative contribution rate")
plt.grid()
plt.title('04')
plt.show()

# PCA の固有値
koyuchi = pd.DataFrame(pca.explained_variance_, index=["PC{}".format(x + 1) for x in range(len(dfs.columns))])
print('koyuchi', koyuchi)

# PCA の固有ベクトル
Koyuvector = pd.DataFrame(pca.components_, columns=df.columns[1:], index=["PC{}".format(x + 1) for x in range(len(dfs.columns))])
filename = 'koyuveotor.csv'
np.savetxt(filename, Koyuvector, delimiter=',')


# 第一主成分と第二主成分における観測変数の寄与度をプロットする
#plt.figure(figsize=(6, 6))
#for x, y, name in zip(pca.components_[0], pca.components_[1], df.columns[1:]):
#    plt.text(x, y, name)
#plt.scatter(pca.components_[0], pca.components_[1], alpha=0.8)
#plt.grid()
#plt.xlabel("PC1")
#plt.ylabel("PC2")
#plt.title('05')
#plt.show()


