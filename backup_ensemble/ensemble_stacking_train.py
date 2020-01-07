# -*- coding: utf-8 -*-
"""
@brief : 根据features_path中的数据，对机器学习模型进行训练，并对测试集进行预测，并将结果保存至本地
@How to use：使用前，先对sklearn_config文件进行参数配置，然后才能运行此文件进行学习训练
@author: Jian
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import time
import pickle
from ensemble_stacking_config import clf_name, clf, status_vali

t_start = time.time()

"""=====================================================================================================================
1 读取数据
"""

k = 10
model_num = 7

meta_feature_train_label = pd.read_csv('./stacking/' + str(k) + 'fold/' + str(model_num) + 'models/meta_feature_train_label.csv')
meta_feature_train = pd.read_csv('./stacking/' + str(k) + 'fold/' + str(model_num) + 'models/meta_feature_train.csv')
x_test = pd.read_csv('./stacking/' + str(k) + 'fold/' + str(model_num) + 'models/meta_feature_test.csv')


"""划分训练集和验证集，验证集比例为test_size"""
if status_vali:
    x_train, x_vali, y_train, y_vali = train_test_split(meta_feature_train, meta_feature_train_label, test_size=0.3, random_state=0)

"""=====================================================================================================================
2 训练分类器
"""
clf.fit(x_train, y_train)

"""=====================================================================================================================
3 在验证集上评估模型
"""
score_vali = 0
if status_vali:
    pre_vali = clf.predict(x_vali)
    score_vali = f1_score(y_true=y_vali, y_pred=pre_vali, average='macro')
    print("验证集分数：{}".format(score_vali))

"""=====================================================================================================================
4 对测试集进行预测;将预测结果转换为官方标准格式；并将结果保存至本地
"""


y_test = clf.predict(x_test)
df = pd.read_csv('/home/zhan/zyy/competitions/datafountain350/data/submit_example.csv')
df_result = pd.DataFrame(data={'id':df['id'], 'label': y_test.tolist()})
result_path = './stacking/' + str(k) + 'fold/' + str(model_num) + 'models/results/' + 'stacking_' + str(k) + 'fold_' +  str(model_num) + 'models_' + clf_name + '_' + str(score_vali) + '_' + '.csv'
df_result.to_csv(result_path, index=False)


t_end = time.time()
print("训练结束，耗时:{}min".format((t_end - t_start) / 60))
