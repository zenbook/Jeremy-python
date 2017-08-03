# -*- coding: utf-8 -*-

class AdalineGD(object):
    """ADAptive LInear NEuron classifier.

    Parameters
    ----------------
    eta: float
        Learning rate (between 0.0 and 1.0)
    n_iter: int
        Passes over the training dataset.

    Attributes:
    ------------------
    w_: 1d-array
        Weights after fitting.
    errors_: int
        Number of misclassification in every epoch.

    """

    def __init__(self, eta=0.01, n_iter=50):
        self.eta = eta
        self.n_iter = n_iter

    def fit(self, X, y):
        """Fit training data.

        Parameters
        ---------------
        X: {array-like}, shape=[n_samples, n_features]
            Training vectors,
        y: array-like, shape=[n_samples]
            Target values.

        Returns
        -----------
        self: object 
        """
        self.w_ = np.zeros(1 + X.shape[1])
        self.cost_ = []

        for i in range(self.n_iter):
            output = self.net_input(X)
            errors = (y - output)
            self.w_[1:] += self.eta * X.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()
            cost = (errors ** 2).sum() / 2.0 
            self.cost_.append(cost)
        return self

    def net_input(self, X):
        """ Calculate net input"""
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def activation(self, X):
        """ Compute linear activation"""
        return self.net_input(X)

    def predict(self, X):
        """ Return class label after unit step"""
        return np.where(self.activation(X) >= 0.0, 1, -1)


# load packages ==================================================
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# load dataset ====================================================
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header = None)


# data pre-processing ==============================================
y = df.iloc[0:100, 4].values
y = np.where(y == 'Iris-setosa', -1, 1)
X = df.iloc[0:100, [0, 2]].values


# modeling =====================================================
# 在将Adaline应用到实际问题中时，通常需要先确定一个好的学习率这样才能保证算法真正收敛
# 学习率,迭代轮数n_iter也被称为超参数(hyperparameters),超参数对于模型至关重要

fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (8, 4))
ada1 = AdalineGD(n_iter = 10, eta = 0.01).fit(X, y)
ax[0].plot(range(1, len(ada1.cost_) + 1), 
                   np.log10(ada1.cost_), marker = 'o')
ax[0].set_xlabel('Epochs')
ax[0].set_ylabel('log(Sum-square-error)')
ax[0].set_title('Adalin-Learning rate 0.01')

ada2 = AdalineGD(n_iter = 10, eta = 0.0001).fit(X, y)
ax[1].plot(range(1, len(ada2.cost_) + 1), 
                   np.log10(ada2.cost_), marker = 'o')
ax[1].set_xlabel('Epochs')
ax[1].set_ylabel('log(Sum-square-error)')
ax[1].set_title('Adalin-Learning rate 0.0001')

plt.show()

# 学习率太大，模型的损失函数并未减小反而增大，说明学习率太大对模型有害无利
# 学习率太低，模型的损失函数确实在减小，但是减小速度让人着急，可能要耗时相当长才能达到模型收敛

# Standardization and Normalization ======================================
# 标准化和归一化有利于模型收敛

X_std = np.copy(X)
X_std[:, 0] = (X[:, 0] - X[:, 0].mean()) / X[:, 0].std()
X_std[:, 1] = (X[:, 1] - X[:, 1].mean()) / X[:, 1].std()


# modeling =======================================================
ada = AdalineGD(n_iter = 15, eta = 0.01)
ada.fit(X_std, y)



def plot_decision_region(X, y, classifier, resolution = 0.02):
    # setup marker generator and color map
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), 
                                                np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)

    plt.contourf(xx1, xx2, Z, alpha = 0.4, cmap = cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    # plot class samples
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x = X[y == cl, 0], y = X[y == cl, 1], 
                            alpha = 0.8, c = cmap(idx), 
                            marker = markers[idx], label = cl)


# plot ====================================================
plot_decision_region(X_std, y, classifier = ada)
plt.show()




