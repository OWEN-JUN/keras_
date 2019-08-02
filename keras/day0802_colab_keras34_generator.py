# -*- coding: utf-8 -*-
"""day0802_colab_keras34_generator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BD1V7kSwXEcyZPCjefxp46ykxvbARkQs
"""

from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from keras.models import *
from keras.utils import np_utils
from keras.layers import *
from keras.callbacks import *

from keras.datasets import mnist
(x_train, y_train),(x_test,y_test) = mnist.load_data()

x_train, _, y_train, _ = train_test_split(x_train, y_train, random_state=66, test_size = 0.995)


x_train = x_train.reshape(x_train.shape[0], 28 ,28 ,1).astype('float32') / 255 # 6만행(무시) 나머지는 아래 input_shape값이 된다.
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1).astype('float32') / 255 # 0~1 사이로 수렴(minmax)시키기 위해 minmaxscaler같은거 필요없이 각 픽셀당 255의 값을 나누어서 아주 간단하게 데이터 전처리를 하는 과정
y_train = np_utils.to_categorical(y_train) # One Hot Incoding으로 데이터를 변환시킨다. 분류
y_test = np_utils.to_categorical(y_test)



data_generator = ImageDataGenerator(
    rotation_range=30,
    width_shift_range = 0.09,
    height_shift_range = 0.04,
    horizontal_flip=True)

model = Sequential()
#conv 신경망 설정

model.add(Conv2D(10,kernel_size=(3,3), input_shape=(28,28,1),activation="relu",padding="same"))
model.add(BatchNormalization())

# model.add(Dropout(0.3))
model.add(Conv2D(10,(4,4),activation="relu"))
model.add(BatchNormalization())

model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.3))



# model.add(MaxPooling2D(pool_size=4))
# model.add(Conv2D(30,(3,3),activation="relu",padding="same"))
# model.add(BatchNormalization())

# model.add(Conv2D(30,(3,3),activation="relu"))
# model.add(BatchNormalization())

# model.add(MaxPooling2D(pool_size=2))
# model.add(Dropout(0.3))


model.add(Conv2D(128,(3,3),activation="relu",padding="same"))
model.add(BatchNormalization())

model.add(Conv2D(128,(3,3),activation="relu",padding="same"))
model.add(BatchNormalization())

model.add(MaxPooling2D(pool_size=3))
model.add(Dropout(0.3))





model.add(Flatten())
# model.add(Dense(1500, activation="relu"))
# model.add(Dropout(0.3))

# model.add(Dense(350, activation="relu"))
# model.add(Dropout(0.3))

# model.add(Dense(30, activation="relu"))
# model.add(Dropout(0.5))
model.add(Dense(10,activation="softmax"))

model.compile(loss="categorical_crossentropy",optimizer="adam",metrics=["accuracy"])

early_stoping_callback = EarlyStopping(monitor="val_loss",patience=30)

model.fit_generator(data_generator.flow(x_train, y_train, batch_size=10), 
                    # steps_per_epoch=len(x_train)//32,
                    steps_per_epoch=100,
                    epochs=300,
                    
                    validation_data=(x_test, y_test),
                    verbose=1,
                    callbacks=[early_stoping_callback]
                    )

print("\n test acc: %.4f"%(model.evaluate(x_test, y_test)[1]))

data_generator.flow(x_train, y_train, batch_size=10)[0][0].shape

len(data_generator.flow(x_train, y_train, batch_size=10))

