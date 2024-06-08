import pandas as pd
from pathlib import Path
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
import joblib

data_signed = pd.read_csv(Path("C:/Users/barto/PycharmProjects/spider/moves_signed_edit.csv"))
x_data_signed_train, y_data_signed_train = data_signed[:405], data_signed[:405]
x_data_signed_test, y_data_signed_test = data_signed[405:], data_signed[405:]
#print(data.info())
print(data_signed.info())
#print(x_data_signed_train.info())
#print(x_data_signed_test.info())
# k = 60
# kmeans = KMeans(n_clusters= k, random_state= 42)
# x_data_dist = kmeans.fit_transform(x_data_signed_train)
# representative_data_idx = np.argmin(x_data_dist, axis = 0)
# x_representative_data = x_data_dist[representative_data_idx]

log_reg = LogisticRegression(max_iter=10000)
x_data_signed_train= x_data_signed_train.drop("type", axis = 1)
x_data_signed_train = x_data_signed_train.drop("from_grid", axis = 1)
x_data_signed_train = x_data_signed_train.drop("to_grid", axis = 1)
x_data_signed_train = x_data_signed_train.drop("move_color", axis = 1)
x_data_signed_train = x_data_signed_train.drop("drop_color", axis = 1)
x_data_signed_train = x_data_signed_train.drop("value", axis = 1)
x_data_signed_train = x_data_signed_train.drop("complete", axis = 1)
x_data_signed_train = x_data_signed_train.drop("len_from", axis = 1)


x_data_signed_test= x_data_signed_test.drop("type", axis = 1)
x_data_signed_test = x_data_signed_test.drop("from_grid", axis = 1)
x_data_signed_test = x_data_signed_test.drop("to_grid", axis = 1)
x_data_signed_test = x_data_signed_test.drop("move_color", axis = 1)
x_data_signed_test = x_data_signed_test.drop("drop_color", axis = 1)
x_data_signed_test = x_data_signed_test.drop("value", axis = 1)
x_data_signed_test = x_data_signed_test.drop("complete", axis = 1)
x_data_signed_test = x_data_signed_test.drop("len_from", axis = 1)
log_reg.fit(x_data_signed_train, y_data_signed_train["type"])
print(log_reg.score(x_data_signed_test, y_data_signed_test["type"]))
joblib.dump(log_reg, "solitaire3.0")