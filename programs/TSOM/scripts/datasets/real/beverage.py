import numpy as np
import os


def load_data(load_file_name, ret_beverage_label=True, ret_situation_label=False, ret_age_label=False):
    dir_name = 'beverage_data'
    file_name = load_file_name
    # file_name = 'test_20200706_300_coke_water_check_origin.npy'
    dir_path = os.path.join(os.path.dirname(__file__), dir_name)  # beverage_dataまでのpath
    file_path = os.path.join(dir_path, file_name)  # path to beverage_data.npy

    # xにデータを入力
    x = np.load(file_path)

    # 1:xを返却
    return_objects = [x]

    if ret_beverage_label:
        #label_name = 'beverage_label.txt'
        #label_name = 'learning_label_55.txt'
        #label_name = 'Label_param6.txt'
        # label_name = 'Label_player.txt' #alpha, beta, gamma
        # label_path = os.path.join(dir_path, label_name)
        # beverage_label = np.genfromtxt(label_path, dtype=str)  # loadtxtだと変な文字が入る可能性があるのでgenfromtxt
        # 2:beverage_labelを返却

        # return_objects.append(beverage_label)
        return_objects.append(['alpha', 'beta', 'gamma'])

    if ret_situation_label:
        #label_name = 'situation_label.txt'
        #label_name = 'learning_label_4.txt'
        #label_name = 'Label_3.txt'
        # label_name = 'Label_param8.txt'
        # label_name = 'Label_player.txt'
        # label_path = os.path.join(dir_path, label_name)
        # situation_label = np.genfromtxt(label_path, dtype=str)  # loadtxtだと変な文字が入る可能性があるのでgenfromtxt
        # 3:situation_labelを返却
        # return_objects.append(situation_label)
        return_objects.append(['bx','by','ax','ay','bx','by','cx','cy','d',
                                'wl','t',
                                'shoot','pass','ballget','clear','active','cover','waitpass'])

    if ret_age_label:
        #label_name = 'learning_label_520.txt'
        #label_name = 'learning_label_260.txt'
        #label_name = 'Label_3600.txt'
        # label_name = 'Label_time17003.txt'
        #label_name = 'Beverage604-side_changed.txt'
        # label_path = os.path.join(dir_path, label_name)
        # age_label = np.genfromtxt(label_path, dtype=str)  # loadtxtだと変な文字が入る可能性があるのでgenfromtxt
        # 4:age_labelを返却
        # return_objects.append(age_label)
        return_objects.append(list(np.arange(270)))

    return return_objects



def load_data_after_learning(load_file_name):
    dir_name = 'beverage_data'
    file_name = load_file_name
    dir_path = os.path.join(os.path.dirname(__file__), dir_name)  # beverage_dataまでのpath
    file_path = os.path.join(dir_path, file_name)  # path to beverage_data.npy

    # x_afterにデータを入力
    x_after = np.load(file_path)

    # 1:x_afterを返却
    return_objects = x_after

    return return_objects


