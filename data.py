import pandas as pd
from pathlib import Path
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
import joblib

data_signed = pd.read_csv(Path("C:\\Users\\barto\\PycharmProjects\\test\\moves4.csv"))
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


x_data_signed_test= x_data_signed_test.drop("type", axis = 1)

log_reg.fit(x_data_signed_train, y_data_signed_train["type"])
print(log_reg.score(x_data_signed_test, y_data_signed_test["type"]))
joblib.dump(log_reg, "solitaire4.0")