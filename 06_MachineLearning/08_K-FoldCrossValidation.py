import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(
    root_path, 'data', 'smoking_driking_dataset_Ver01.csv')
data = pd.read_csv(data_path)

# 전처리
# print(data.isnull().sum())  # null 값 확인
data['sex'] = data['sex'].map({'Male': 0, 'Female': 1})
data['DRK_YN'] = data['DRK_YN'].map({'N': 0, 'Y': 1})

data_sample = data.sample(frac=0.1, random_state=1)

# target 확인
target = 'DRK_YN'

# 데이터 분리
x = data_sample.drop(target, axis=1)
y = data_sample.loc[:, target]

# 7:3으로 분리
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=1)

# 정규화
scaler = MinMaxScaler()
scaler.fit(x_train)
x_train_s = scaler.transform(x_train)
x_test_s = scaler.transform(x_test)

result = {}

# 모델링
model = DecisionTreeClassifier(max_depth=5, random_state=1)
cv_score = cross_val_score(model, x_train, y_train, cv=10)
result['DecisionTree'] = cv_score.mean()

model = KNeighborsClassifier(n_neighbors=5)
cv_score = cross_val_score(model, x_train_s, y_train, cv=10)
result['KNN'] = cv_score.mean()

model = LogisticRegression(max_iter=1000)
cv_score = cross_val_score(model, x_train_s, y_train, cv=10)
result['LogisticRegression'] = cv_score.mean()

# 시각화
plt.figure(figsize=(10, 10))
sns.barplot(x=list(result.keys()), y=list(result.values()))
plt.show()

# data: https://www.kaggle.com/datasets/sooyoungher/smoking-drinking-dataset
