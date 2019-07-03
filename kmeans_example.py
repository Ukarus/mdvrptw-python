# Dependencies

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

pr01 = pd.read_csv(r'C:\Users\juanj\Documents\Trabajo de Titulo 2\algorithm\pr01_2.csv')
x = np.array(pr01)
clusters = np.array([[4.163, 13.559], [21.387, 17.105], [-36.118, 49.097], [-31.201, 0.235]])
kmeans = KMeans(n_clusters=4, init=clusters, n_init=1).fit(x)
print(kmeans.labels_)
print(kmeans.cluster_centers_)

# example2 = np.array( [[5,3], [10,15], [15,12], [24,10], [30,45], [85,70], [71,80], [60,78], [55,52], [80,91]])
# means = KMeans(n_clusters=2, init=np.array([ [5,3], [10, 15] ]), n_init=1).fit(example2)
# means = KMeans(n_clusters=2).fit(example2)
# print(means.labels_)
# print(means.cluster_centers_)
# X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])
# kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
# print(kmeans.labels_)
# print(kmeans.predict([[0, 0], [12, 3]]))
# print(kmeans.cluster_centers_)

'''
train_url = "http://s3.amazonaws.com/assets.datacamp.com/course/Kaggle/train.csv"
train = pd.read_csv(train_url)
test_url = "http://s3.amazonaws.com/assets.datacamp.com/course/Kaggle/test.csv"
test = pd.read_csv(test_url)

# print("***** Train_Set *****")
# print(train.head())
# print("\n")
# print("***** Test_Set *****")
# print(test.head())

# print("***** Train_Set *****")
# print(train.describe())
# print("\n")
# print("***** Test_Set *****")
# print(test.describe())

# print(train.columns.values)
# For the train set
train.isna().head()
# For the test set
test.isna().head() 


# print("*****In the train set*****")
# print(train.isna().sum())
# print("\n")
# print("*****In the test set*****")
# print(test.isna().sum())

# Fill missing values with mean column values in the train set
train.fillna(train.mean(), inplace=True)

# Fill missing values with mean column values in the test set
test.fillna(test.mean(), inplace=True)


print("*****In the train set*****")
print(train.isna().sum())
print("\n")
print("*****In the test set*****")
print(test.isna().sum())

# print(train['Ticket'].head())

print(train[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean().sort_values(by='Survived', ascending=False))
print(train[["Sex", "Survived"]].groupby(['Sex'], as_index=False).mean().sort_values(by='Survived', ascending=False))
print(train[["SibSp", "Survived"]].groupby(['SibSp'], as_index=False).mean().sort_values(by='Survived', ascending=False))

# g = sns.FacetGrid(train, col='Survived')
# g.map(plt.hist, 'Age', bins=20)

print(train.info())
train = train.drop(['Name','Ticket', 'Cabin','Embarked'], axis=1)
test = test.drop(['Name','Ticket', 'Cabin','Embarked'], axis=1)

labelEncoder = LabelEncoder()
labelEncoder.fit(train['Sex'])
labelEncoder.fit(test['Sex'])
train['Sex'] = labelEncoder.transform(train['Sex'])
test['Sex'] = labelEncoder.transform(test['Sex'])

# Let's investigate if you have non-numeric data left

# train.info()

x = np.array(train.drop(['Survived'], 1).astype(float))
y = np.array(train['Survived'])

print("\n")
print(" **** After Survived column removed ****")
train.info()
# test.info()
print(x)
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(x)
kmeans = KMeans(n_clusters=2, max_iter=600, algorithm = 'auto') # You want cluster the passenger records into 2: Survived or Not survived
kmeans.fit(X_scaled)

print(X_scaled)
correct = 0
for i in range(len(x)):
    predict_me = np.array(x[i].astype(float))
    predict_me = predict_me.reshape(-1, len(predict_me))
    prediction = kmeans.predict(predict_me)
    if prediction[0] == y[i]:
        correct += 1

print(correct/len(x))
'''