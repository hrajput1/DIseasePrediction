from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score 

iris = load_iris()

X = pd.DataFrame(iris.data, columns=iris.feature_names)
#print(X)
y = pd.Categorical.from_codes(iris.target, iris.target_names)
#print(y)

#print(X.head())

y = pd.get_dummies(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)

y_pred = dt.predict(X_test)

acc = accuracy_score(y_test,y_pred)*100

print(acc)

