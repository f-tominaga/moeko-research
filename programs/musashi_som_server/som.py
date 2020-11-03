# -*- coding: utf-8 -*-

import os
import tkinter
import tkinter.filedialog
import numpy as np
from scipy.spatial import distance
import json
# from musashi_som_server import tsom2_viewer as TSOM2_V
import create_zeta
# import create_zeta
import tsom2_viewer as TSOM2_V

class SOM:
    def __init__(self,):
        print('create SOM instance')

    def open(self, cfg_file: str):
        # Load config file
        json_file = open(cfg_file)
        json_data = json.load(json_file)
        # print('Config:{}'.format(json_data))
        mode1_model_file = os.path.abspath(json_data['mode1_model'])
        mode2_model_file = os.path.abspath(json_data['mode2_model'])
        som_model_file = os.path.abspath(json_data['som_model'])
        label_path1 = os.path.abspath(json_data['label1'])
        label_path2 = os.path.abspath(json_data['label2'])
        label_path3 = os.path.abspath(json_data['label3'])

        # make som models
        self.model = np.loadtxt(som_model_file, delimiter=',')
        self.bmu1 = np.loadtxt(mode1_model_file, delimiter=',')
        self.bmu2 = np.loadtxt(mode2_model_file, delimiter=',')
        
        self.model = self.model.reshape((100, 100, 3))
        self.bmu1 = np.int64(np.round(self.bmu1))
        self.bmu2 = np.int64(np.round(self.bmu2))
        
        label1 = np.genfromtxt(label_path1, dtype=str)
        label2 = np.genfromtxt(label_path2, dtype=str)
        label3 = np.genfromtxt(label_path3, dtype=str)
        
        print('--- T-SOM parameters ----------')
        print('model shape:', self.model.shape)
        print('bmu1:', self.bmu1)
        print('bmu2:', self.bmu2)
        print('Label1:', label1)
        print('Label2:', label2)
        print('Label3:', label3)
        print('-------------------------------')

        # Viewer's setting
        # comp = TSOM2_V.TSOM2_Viewer(y=self.model,
        #                             winner1=self.bmu1,
        #                             winner2=self.bmu2,
        #                             label2=label2,
        #                             button_label=label3)
        # comp.draw_map()

    def ploof(self, sim_data):

        print('ploof入りました')

        # データをとってきました！！
        X_after = list(sim_data)
        ball_x = X_after[0] / 10
        ball_y = X_after[1] / 10
        teammate_info = np.zeros((2, 3))
        teammate_info[0, :] = [X_after[5], X_after[6], X_after[7]]
        teammate_info[1, :] = [(X_after[2]/15)*2 - 1, (X_after[3]/15)*2 - 1, (X_after[4]/15)*2 - 1]
        haveball = X_after[8]*2 - 1
        my_role = X_after[9] -1

        # 入力用にいじりました！！
        # まず距離のそーと
        np.sort(teammate_info, axis=1)
        X_after = [ball_x, ball_y, teammate_info[1, 0], teammate_info[1, 1], teammate_info[1, 2], haveball]
        X_after = np.array(X_after)

        # Y = self.model

        # 学習量の決定
        # 近傍半径は最小値で固定
        sigma_ploof = 0.2
        # Zetaは各ユニットの座標ですね
        self.Zeta2 = create_zeta.create_zeta(-1.0, 1.0, latent_dim=2, resolution=10, include_min_max=True)
        self.Y = self.model
        self.Z2 = self.Zeta2[self.bmu2, :]
        # 確認用入力を切り取るときに使用
        self.Z2 = self.Z2[0:6, :]

        # BMUと各ユニットとの距離を計算
        distance_ploof = distance.cdist(self.Zeta2, self.Z2, 'sqeuclidean')  # 距離行列をつくるDはN*K行列
        # 学習量を計算
        H_ploof = np.exp(-distance_ploof / (2 * pow(sigma_ploof, 2)))  # かっこに気を付ける

        G_ploof = np.sum(H_ploof, axis=1)  # Gは行ごとの和をとったベクトル
        R_ploof = (H_ploof.T / G_ploof).T  # 行列の計算なので.Tで転置を行う

        # ================各選手個別に確認=============================
        # １次モデル，２次モデルの決定
        U_ploof_2 = np.einsum('lj,j->l', R_ploof, X_after.T)
        # 勝者決定
        k_star_ploof_2 = np.argmin(np.sum(np.square(U_ploof_2[None, :, None]
                                                           - self.Y[:, :, my_role]), axis=(1, 2)), axis=0)

        BMU_Results_2 = self.Y[k_star_ploof_2, self.bmu2, my_role]
        function = np.round((BMU_Results_2[6]+1)*(7/2))
        print('BMUresult', BMU_Results_2)
        print('function', function)
        return function
        # ================各選手個別に確認=============================

if __name__ == '__main__':
    print('Try to load T-SOM')
    som = SOM()
    # som.open('cfg/test.json')
    som.open('musashi_som_server/cfg/test.json')
