from models.tsom import TSOM2
from datasets.real.beverage import load_data
from datasets.real.beverage import load_data_after_learning
from visualization.tsom.tsom2_viewer import TSOM2_Viewer as TSOM2_V
import numpy as np

#input array data 3-D
# Learnig_file_name = 'ALL_V_3068_13_3.npy'
Learnig_file_name = 'robot.npy'
#validation array data
Checking_file_name = 'P1.npy'
# Checking_file_name = 'checkdata_norm_2020_10_19 00-49-55-simulation_01.npy'


check_dim = 11
latent_dim = 2
resolution = 10
SIGMA_MAX = 2.0
SIGMA_MIN = 0.2
TAU = 50 #50 #500
Epoch = 200

if __name__ == '__main__':

    # 訓練データの読み込みです
    X, beverage, situation, age = load_data(load_file_name=Learnig_file_name,
                                            ret_beverage_label=True, 
                                            ret_situation_label=True, 
                                            ret_age_label=True)
    # 検証データの読み込みです
    X_after = load_data_after_learning(load_file_name=Checking_file_name)

    #人間ロボット混合データの作成時のもの
    #X_mix = np.dstack([X_after[:,0,:], X[:,1,:]])
    #X_mix = np.dstack([X_mix, X[:,2,:]])
    #X_mix = X_mix.transpose(0,2,1)
    #print("X_mix_size:", X_mix.shape)

    # tsomのイニシャライズです
    tsom = TSOM2(X, 
              X_after, 
              check_dim=check_dim,
              latent_dim=latent_dim, 
              resolution=resolution,
              SIGMA_MAX=SIGMA_MAX, 
              SIGMA_MIN=SIGMA_MIN, 
              TAU=TAU)

    # 学習です
    tsom.fit(nb_epoch=Epoch)
    # 検証です
    tsom.ploof()

    # マップ表示のための準備です
    comp = TSOM2_V(y=tsom.Y, winner1=tsom.k_star1, winner2=tsom.k_star2,
                   label2=beverage, button_label=situation)

    # マップ表示です
    comp.draw_map()

    # 学習時のパラメータのログとりです
    Param = [check_dim, latent_dim, resolution, SIGMA_MAX, SIGMA_MIN, TAU, Epoch]
    np.savetxt('Parameter.csv', Param, delimiter=',',
               header='check_dim, latent_dim, resolution, SIGMA_MAX, SIGMA_MIN, TAU, Epoch,'
                      'Learnig_file_name, Checking_file_name, Checking_file_name',
               footer=Checking_file_name, comments='#comments#')

    print("Yの形：", tsom.Y.shape)
    print("Uの形：", tsom.U.shape)
    print("Vの形：", tsom.V.shape)

