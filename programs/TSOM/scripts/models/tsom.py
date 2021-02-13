import numpy as np
from scipy.spatial import distance
# from tqdm import tqdm
import sys
sys.path.append("scripts\tools")
from tools.create_zeta import create_zeta
import scipy.spatial.distance as dist
from sklearn.decomposition import PCA

class TSOM2():
    def __init__(self, X, X_after, check_dim, latent_dim, resolution, SIGMA_MAX, SIGMA_MIN, TAU, init='random'):

        # 入力データXについて
        if X.ndim == 2:
            self.X = X.reshape((X.shape[0], X.shape[1], 1))  # 二次元だから似非三次元化してる
            self.N1 = self.X.shape[0]
            self.N2 = self.X.shape[1]
            self.observed_dim = self.X.shape[2]  # 観測空間の次元

        elif X.ndim == 3:
            self.X = X
            self.N1 = self.X.shape[0]
            self.N2 = self.X.shape[1]
            self.observed_dim = self.X.shape[2]  # 観測空間の次元
            print('N1', self.N1)
            print('N2', self.N2)
            print('OB', self.observed_dim)

        else:
            raise ValueError("invalid X: {}\nX must be 2d or 3d ndarray".format(X))

        # 検証データの次元数(照合にかける次元について)
        self.Check_dim = check_dim

        # 学習後の入力データX_afterについて
        if X.ndim == 2:
            self.X_after = X_after.reshape((X_after.shape[0], X_after.shape[1], 1)) # 二次元だから似非三次元化してる
            self.X_after_answer = self.X_after[:, :, self.Check_dim:self.X_after.shape[2]]
            self.X_after = self.X_after[:, :, 0:self.Check_dim]
            self.N1_after = self.X_after.shape[0]
            self.N2_after = self.X_after.shape[1]
            self.observed_dim_after = self.X_after.shape[2]  # 観測空間の次元

        elif X.ndim == 3:
            self.X_after = X_after
            self.X_after_answer = self.X_after[:, :, self.Check_dim:self.X_after.shape[2]]
            self.X_after = self.X_after[:, :, 0:self.Check_dim] #ここでキリトリ
            self.N1_after = self.X_after.shape[0]
            self.N2_after = self.X_after.shape[1]
            self.observed_dim_after = self.X_after.shape[2]  # 観測空間の次元

        else:
            raise ValueError("invalid X_after: {}\nX must be 2d or 3d ndarray".format(X))

        print('self.X_after_answer', self.X_after_answer.shape)
        print('self.X_after', self.X_after.shape)

        # 最大近傍半径(SIGMAX)の設定
        if type(SIGMA_MAX) is float:
            self.SIGMA1_MAX = SIGMA_MAX
            self.SIGMA2_MAX = SIGMA_MAX
        elif isinstance(SIGMA_MAX, (list, tuple)):
            self.SIGMA1_MAX = SIGMA_MAX[0]
            self.SIGMA2_MAX = SIGMA_MAX[1]
        else:
            raise ValueError("invalid SIGMA_MAX: {}".format(SIGMA_MAX))

        # 最小近傍半径(SIGMA_MIN)の設定
        if type(SIGMA_MIN) is float:
            self.SIGMA1_MIN = SIGMA_MIN
            self.SIGMA2_MIN = SIGMA_MIN
        elif isinstance(SIGMA_MIN, (list, tuple)):
            self.SIGMA1_MIN = SIGMA_MIN[0]
            self.SIGMA2_MIN = SIGMA_MIN[1]
        else:
            raise ValueError("invalid SIGMA_MIN: {}".format(SIGMA_MIN))

        # 時定数(TAU)の設定
        if type(TAU) is int:
            self.TAU1 = TAU
            self.TAU2 = TAU
        elif isinstance(TAU, (list, tuple)):
            self.TAU1 = TAU[0]
            self.TAU2 = TAU[1]
        else:
            raise ValueError("invalid TAU: {}".format(TAU))

        # resolutionの設定
        if type(resolution) is int:
            resolution1 = resolution
            resolution2 = resolution
        elif isinstance(resolution, (list, tuple)):
            resolution1 = resolution[0]
            resolution2 = resolution[1]
        else:
            raise ValueError("invalid resolution: {}".format(resolution))

        # 潜在空間の設定
        if type(latent_dim) is int:  # latent_dimがintであればどちらのモードも潜在空間の次元は同じ
            self.latent_dim1 = latent_dim
            self.latent_dim2 = latent_dim

        elif isinstance(latent_dim, (list, tuple)):
            self.latent_dim1 = latent_dim[0]
            self.latent_dim2 = latent_dim[1]
        else:
            raise ValueError("invalid latent_dim: {}".format(latent_dim))
            # latent_dimがlist,float,3次元以上はエラーかな?
        # 各ユニットの座標(resolution*resolution*2)
        self.Zeta1 = create_zeta(-1.0, 1.0, latent_dim=self.latent_dim1, resolution=resolution1, include_min_max=True)
        self.Zeta2 = create_zeta(-1.0, 1.0, latent_dim=self.latent_dim2, resolution=resolution2, include_min_max=True)

        # K1とK2は潜在空間の設定が終わった後がいいよね
        self.K1 = self.Zeta1.shape[0]
        self.K2 = self.Zeta2.shape[0]

        # 勝者ノードの初期化
        self.Z1 = None
        self.Z2 = None
        if isinstance(init, str) and init in 'random':
            #pca1 = PCA(self.latent_dim1)
            #pca2 = PCA(self.latent_dim2)
            #pca1.fit(self.X[:, :, 0])
            #pca2.fit(self.X[:, :, 1])
            #self.Z1 = pca1.inverse_transform(np.sqrt(pca1.explained_variance_)[None, :] * self.Zeta1)
            #self.Z2 = pca2.inverse_transform(np.sqrt(pca2.explained_variance_)[None, :] * self.Zeta2)
            self.Z1 = np.random.rand(self.N1, self.latent_dim1) * 2.0 - 1.0
            self.Z2 = np.random.rand(self.N2, self.latent_dim2) * 2.0 - 1.0
            print('X', self.X[0,0,0])
            print('Zeta1', self.Zeta1.shape)
            print('Zeta2', self.Zeta2.shape)
            print('Z1', self.Z1.shape)
            print('Z2', self.Z2.shape)

        elif isinstance(init, (tuple, list)) and len(init) == 2:
            if isinstance(init[0], np.ndarray) and init[0].shape == (self.N1, self.latent_dim1):
                self.Z1 = init[0].copy()
            else:
                raise ValueError("invalid inits[0]: {}".format(init))
            if isinstance(init[1], np.ndarray) and init[1].shape == (self.N2, self.latent_dim2):
                self.Z2 = init[1].copy()
            else:
                raise ValueError("invalid inits[1]: {}".format(init))
        else:
            raise ValueError("invalid inits: {}".format(init))

        self.history = {}

    def fit(self, nb_epoch=100):
        print('start fitting!!')
        self.history['y'] = np.zeros((nb_epoch, self.K1, self.K2, self.observed_dim))
        self.history['z1'] = np.zeros((nb_epoch, self.N1, self.latent_dim1))
        self.history['z2'] = np.zeros((nb_epoch, self.N2, self.latent_dim2))
        self.history['sigma1'] = np.zeros(nb_epoch)
        self.history['sigma2'] = np.zeros(nb_epoch)
        self.history['y_sa'] = np.zeros(nb_epoch)

#        for epoch in tqdm(np.arange(nb_epoch))
        for epoch in np.arange(nb_epoch):

            print('Epoch',epoch)

            # 学習量の決定
            # sigma1 = self.SIGMA1_MIN + (self.SIGMA1_MAX - self.SIGMA1_MIN) * np.exp(-epoch / self.TAU1)
            # epoch毎に学習率を計算
            #sigma1 = max(self.SIGMA1_MIN, self.SIGMA1_MAX * (1 - (epoch / self.TAU1)))
            sigma1 = max(self.SIGMA1_MIN, self.SIGMA1_MAX * np.exp(-(epoch / self.TAU1)))
            # BMUと各ユニットとの距離を計算
            print('Distance')
            distance1 = distance.cdist(self.Zeta1, self.Z1, 'sqeuclidean')  # 距離行列をつくるDはN*K行列
            # 学習量を計算
            H1 = np.exp(-distance1 / (2 * pow(sigma1, 2)))  # かっこに気を付ける

            G1 = np.sum(H1, axis=1)  # Gは行ごとの和をとったベクトル
            R1 = (H1.T / G1).T  # 行列の計算なので.Tで転置を行う

            # sigma2 = self.SIGMA2_MIN + (self.SIGMA2_MAX - self.SIGMA2_MIN) * np.exp(-epoch / self.TAU2)
            #sigma2 = max(self.SIGMA2_MIN, self.SIGMA2_MAX * (1 - (epoch / self.TAU2)))
            sigma2 = max(self.SIGMA2_MIN, self.SIGMA2_MAX * np.exp(-(epoch / self.TAU2)))
            distance2 = distance.cdist(self.Zeta2, self.Z2, 'sqeuclidean')  # 距離行列をつくるDはN*K行列
            H2 = np.exp(-distance2 / (2 * pow(sigma2, 2)))  # かっこに気を付ける
            G2 = np.sum(H2, axis=1)  # Gは行ごとの和をとったベクトル
            R2 = (H2.T / G2).T  # 行列の計算なので.Tで転置を行う
            # １次モデル，２次モデルの決定
            self.U = np.einsum('lj,ijd->ild', R2, self.X)
            self.V = np.einsum('ki,ijd->kjd', R1, self.X)
            self.Y = np.einsum('ki,lj,ijd->kld', R1, R2, self.X)
            self.RR = np.einsum('ki, lj->kl', R1, R2)
            self.RRR = np.stack([self.RR, self.RR, self.RR], 2)
            # 勝者決定
            print('Deside the BMU')
            self.k_star1 = np.argmin(np.sum(np.square(self.U[:, None, :, :]
                                                      - self.Y[None, :, :, :]), axis=(2, 3)), axis=1)
            print('k_star1',self.k_star1.shape)
            self.k_star2 = np.argmin(np.sum(np.square(self.V[:, :, None, :]
                                                      - self.Y[:, None, :, :]), axis=(0, 3)), axis=1)
            print('k_star2', self.k_star2.shape)
            print('Saving.....')
            self.Z1 = self.Zeta1[self.k_star1, :]  # k_starのZの座標N*L(L=2
            self.Z2 = self.Zeta2[self.k_star2, :]  # k_starのZの座標N*L(L=2

            self.history['y'][epoch, :, :] = self.Y
            self.history['z1'][epoch, :] = self.Z1
            self.history['z2'][epoch, :] = self.Z2
            self.history['sigma1'][epoch] = sigma1
            self.history['sigma2'][epoch] = sigma2

            # 前回追加分
            #　学習が収束しているかどうかの確認用(Moeko)
            self.history['y_sa'][epoch] = np.sum(abs((self.history['y'][epoch, :, :])
                                                     - (self.history['y'][epoch - 1, :, :])))
            print(epoch, self.history['y_sa'][epoch])

            s1 = np.vstack(self.history['y_sa'])
            s2 = np.vstack(self.history['sigma1'])
            #s3 = self.history['y'][epoch, :, :].reshape((25*self.observed_dim, 25))
            s3 = self.history['y'][epoch, :, :].reshape((100 * self.observed_dim, 100))
            s4 = self.k_star1
            s5 = self.k_star2
            np.savetxt('y_sa.csv', s1, delimiter=',')
            np.savetxt('sigma1.csv', s2, delimiter=',')
            np.savetxt('y.csv', s3, delimiter=',')
            np.savetxt('k_star1.csv', s4, delimiter=',')
            np.savetxt('k_star2.csv', s5, delimiter=',')

        #print('k_star1', self.k_star1)

    # 実際にこのTSOMの評価をする用
    def ploof(self):

        self.history['BMU_Results_x'] = np.zeros((self.N2, self.N1_after))
        self.history['BMU_Results_y'] = np.zeros((self.N2, self.N1_after))
        #self.history['BMU_Results_z'] = np.zeros((self.N2_after, self.N1_after))
        # 学習量の決定
        # 近傍半径は最小値で固定
        sigma_ploof = self.SIGMA2_MIN
        # BMUとして選択されたユニットの要素を格納するためのもの
        BMU_Results_1 = np.zeros((self.N2, self.observed_dim, self.N1_after))
        BMU_Results_2 = np.zeros((self.N2, self.observed_dim, self.N1_after))
        # BMUの正答率を出すためのもの
        BMU_k_star = np.zeros((self.N1, self.observed_dim_after+2))
        BMU_k_star[:, 0] = self.k_star1
        conpare_with_real_and_results = np.zeros((3, self.N1_after))

        for n in range(self.N1_after):
            print('ploof epoch:', n)

            # キリトリ
            # self.Z2 = self.Z2[0:self.Check_dim, :]

            # BMUと各ユニットとの距離を計算
            distance_ploof = distance.cdist(self.Zeta2, self.Z2, 'sqeuclidean')  # 距離行列をつくるDはN*K行列
            # 学習量を計算
            H_ploof = np.exp(-distance_ploof / (2 * pow(sigma_ploof, 2)))  # かっこに気を付ける

            G_ploof = np.sum(H_ploof, axis=1)  # Gは行ごとの和をとったベクトル
            R_ploof = (H_ploof.T / G_ploof).T  # 行列の計算なので.Tで転置を行う


            # ================全選手一気に確認=============================
            # １次モデル，２次モデルの決定
            # print('R_ploof', R_ploof.shape)
            # print('self.X_after[n, :, :]', self.X_after[n, :, :].shape)
            U_ploof_1 = np.einsum('lj,jd->ld', R_ploof, self.X_after[n, :, :])
            #self.V = np.einsum('ki,ijd->kjd', R1, self.X)
            # 勝者決定
            # print('U_ploof', U_ploof.shape)
            self.Y_ = self.Y[:, :, 0:self.Check_dim]
            k_star_ploof_1 = np.argmin(np.sum(np.square(U_ploof_1[None, :, :]
                                                           - self.Y_[:, :, :]), axis=(1, 2)), axis=0)

            BMU_k_star[n, 1] = k_star_ploof_1

            # print('check :', self.Y[k_star_ploof, self.k_star2, :])
            # print('check2 :', self.Y[k_star_ploof, self.k_star2, :].shape)
            BMU_Results_1[:, :, n] = self.Y[k_star_ploof_1, self.k_star2, :]

            # ================前選手一気に確認=============================

            # ================各選手個別に確認=============================
            for m in range(self.observed_dim_after):
                # １次モデル，２次モデルの決定
                U_ploof_2 = np.einsum('lj,j->l', R_ploof, self.X_after[n, :, m])
                # self.V = np.einsum('ki,ijd->kjd', R1, self.X)
                # 勝者決定
                k_star_ploof_2 = np.argmin(np.sum(np.square(U_ploof_2[None, :, None]
                                                           - self.Y[:, :, :]), axis=(1, 2)), axis=0)

                # ログに残すために収納
                BMU_k_star[n, 2 + m] = k_star_ploof_2

                BMU_Results_2[:, :, n] = self.Y[k_star_ploof_2, self.k_star2, :]
            # ================各選手個別に確認=============================


        # ============ログを残す=============================
        for l in range(self.N2):

            # ファイルの名前ラベル用処理
            number = l + 1
            filename1 = 'BMU_Results_players_fin1_{0}.csv'.format(number)
            filename2 = 'BMU_Results_players_fin2_{0}.csv'.format(number)
            # 各選手個別に確認したBMUの要素を格納
            self.history['BMU_Results_players_test_1'] = BMU_Results_1[l, :, :]
            self.history['BMU_Results_players_test_2'] = BMU_Results_2[l, :, :]

            # 学習結果と成果を結合
            s5 = np.hstack((self.history['BMU_Results_players_test_1'].T, self.X_after_answer[:, l, :]))
            s6 = np.hstack((self.history['BMU_Results_players_test_2'].T, self.X_after_answer[:, l, :]))

            # 学習結果と成果の平均二乗誤差を計算
            MSE1 = np.sqrt((np.sum((s5[:, self.Check_dim] - s5[:, self.Check_dim + 1]) ** 2)) / self.N1_after)
            MSE2 = np.sqrt((np.sum((s6[:, self.Check_dim] - s6[:, self.Check_dim + 1]) ** 2)) / self.N1_after)
            print('MSE1', l + 1, ':', MSE1)
            print('MSE2', l + 1, ':', MSE2)
            np.savetxt(filename1, s5, delimiter=',', header='BMU_elements+Answer', comments='#comments#')
            np.savetxt(filename2, s6, delimiter=',', header='BMU_elements+Answer', comments='#comments#')

            # 平均二乗誤差の追記
            file1 = open(filename1, 'a')
            file1.write('MSE:')
            file1.write(str(MSE1))
            file1.close()

            file2 = open(filename2, 'a')
            file2.write('MSE:')
            file2.write(str(MSE2))
            file2.close()

        # ============ログを残す=============================


        self.history['BMU_k_star'] = BMU_k_star
        s11 = np.vstack(self.history['BMU_k_star'])
        np.savetxt('BMU_k_star.csv', s11, delimiter=',', header='LearningBMU, AlltogetherBMU, situation1BMU,'
                                                                'situation2BMU,situation3BMU',comments='#Comment#')




