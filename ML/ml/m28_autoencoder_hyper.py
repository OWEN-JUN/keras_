from keras.datasets import mnist
import numpy as np
(x_train, _),(x_test, _) = mnist.load_data()

x_train = x_train.astype("float32")/255
# x_train = list(map(lam,x_train ))
# print(x_train[1][1].shape)
# def lab(x):
#     for i in range(len(x)):
#         for j in range(len(x[i])):
#             for k in range(len(x[i][j])):
#                 if x[i][j][k] < 0.2:
#                     x[i][j][k] = 0
                
#         if i % 1000 == 0:
#             print(i)
#     return x

# # x_train = list(map(lambda x: 1 if x>0.2 else 0), x_train)
# x_train = lab(x_train)
# x_test = lab(x_test)

print(x_train[0])

x_test = x_test.astype("float32")/255
x_train = x_train.reshape((len(x_train),np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test),np.prod(x_test.shape[1:])))
print(x_train.shape)
print(x_test.shape)



###모델구성###

from keras.layers import *
from keras.models import *


def build_network_dnn(optimizer = "adam",keep_prob=0.5,encoding_dim = 30):
    encoding_dim = encoding_dim
    input_img = Input(shape=(784,))

    x = Dense(30, activation="relu")(input_img)
    x = Dense(50, activation="relu")(x)
    x = Dense(100, activation="relu")(x)
    x = Dropout(keep_prob)(x)
    encoded = Dense(encoding_dim, activation="relu")(x)
    x = Dense(100, activation="relu")(encoded)
    x = Dense(50, activation="relu")(x)
    x = Dense(30, activation="relu")(x)
    x = Dropout(keep_prob)(x)
    #디코더는 입력의 손실있는 재구성 (lossy reconstryction)
    decoded = Dense(784, activation="sigmoid")(x)
    # decoded = Dense(784, activation="relu")(encoded)





    autoencoder = Model(input_img, decoded) #784 -> 32 -> 784
    autoencoder.compile(loss="binary_crossentropy",optimizer=optimizer,metrics=["acc"])
    return autoencoder
# encoder = Model(input_img, encoded) # 754 -> 32



# encoded_input = Input(shape=(encoding_dim,))
# x = Dense(100, activation="relu")(encoded_input)
# x = Dense(50, activation="relu")(x)
# x = Dense(30, activation="relu")(x)
# decoder_layer = autoencoder.layers[-1]
# decoder = Model(encoded_input, decoder_layer(x)) #32->784

# autoencoder.summary()
# encoder.summary()
# decoder.summary()
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from keras.wrappers.scikit_learn import KerasClassifier


model =KerasClassifier(build_fn = build_network_dnn, verbose=1)
def create_hyperparameters():
    batches=[5,7,9,10]
    optimizers = ["SGD", "adam"]
    dropout = np.linspace(0,0.1, 2)
    encoding_dim = [30,40,50,60]
    return{"batch_size":batches, "optimizer":optimizers,"keep_prob":dropout,"encoding_dim":encoding_dim}

hyper = create_hyperparameters()
search=RandomizedSearchCV(estimator=model, param_distributions=hyper, n_iter=10,n_jobs=-1, cv=4, verbose=1)


# autoencoder.compile(optimizer="adadelta",loss="categorical_crossentropy",metrics=["acc"])

search.fit(x_train, x_train)

print(search.best_params_)
print("best score : ", search.best_score_)
print("score:",search.score(x_test,x_test))
# encoded_imgs = encoder.predict(x_test)
# decoded_imgs = autoencoder.predict_(x_test)

decoded_imgs = search.predict(x_test)
# print(encoded_imgs)
# print(decoded_imgs)
# print(encoded_imgs.shape)
# print(decoded_imgs.shape)

import sys
sys.exit()
##########이미지출력#########
import matplotlib.pyplot as plt

n=10
plt.figure(figsize=(20,4))
for i in range(n):
    ax = plt.subplot(2,n,i+1)
    plt.imshow(x_test[i].reshape(28,28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    ax=plt.subplot(2,n,i+1+n)
    plt.imshow(decoded_imgs[i].reshape(28,28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

plt.show()


############그래프 출력#############
def plot_acc(history, title=None):
    if not isinstance(history, dict):
        history = history.history

    plt.plot(history["acc"])
    plt.plot(history["val_acc"])
    if title is not None:
        plt.title(title)

    plt.ylabel("Aaccracy")
    plt.xlabel("epoch")
    plt.legend(["Training data", "validation data"], loc=0)

def plot_loss(history, title=None):
    if not isinstance(history, dict):
        history = history.history

    plt.plot(history["loss"])
    plt.plot(history["val_loss"])
    if title is not None:
        plt.title(title)

    plt.ylabel("loss")
    plt.xlabel("epoch")
    plt.legend(["Training data", "validation data"], loc=0)

plot_acc(history, "(a)학습 경과에 따른 정확도 변화 추이")
plt.show()
plot_loss(history, "(a)학습 경과에 따른 손실값 변화 추이")
plt.show()

loss, acc = autoencoder.evaluate(x_test, x_test)
print(loss, acc)

