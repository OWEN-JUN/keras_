import tensorflow as tf
import matplotlib.pyplot as plt
import random
import numpy as np
from sklearn.model_selection import train_test_split
tf.set_random_seed(8)

iris_data = np.load("./data/iris_data.npy")
# iris_label = np.load("./Study_DL/TF/data/iris_label.npy")

print("iris_data:",iris_data.shape)
# print("iris_label:",iris_label.shape)
# print(iris_data)
# print(iris_label)

x_train = iris_data[:,:-1]

y_train = iris_data[:,[-1]]
# y_train = np.array(y_train,dtype=np.int32)

print(x_train)
print(y_train)
print(x_train.shape, y_train.shape)
x_train, x_test, y_train, y_test = train_test_split(x_train,y_train,test_size=0.2)
print(x_train.shape, y_train.shape)

# w1 = tf.get_variable("w1",shape=[?,?],initializer=tf.random_uniform_initializer())
# b1 = tf.Variable(tf.random_normal([512]))


# tf.constant_initializer()
# tf.zeros_initializer()
# tf.random_uniform_initializer()
# tf.random_normal_initializer()
# tf.contrib.layers.xavier_initializer()


cnt = 1


X = tf.placeholder(tf.float32,[None, 4])
Y = tf.placeholder(tf.int32,[None, 1])
keep_prob = 0

Y_one_hot = tf.one_hot(Y, 3) # one-hot
print("one_hot:", Y_one_hot)
Y_one_hot = tf.reshape(Y_one_hot, [-1, 3])
print("reshape one_hot:", Y_one_hot)


l1 = tf.layers.dense(X, 3, activation=tf.nn.relu)
l2 = tf.layers.dense(l1, 50, activation=tf.nn.relu)
l3 = tf.layers.dense(l2, 100, activation=tf.nn.relu)
logits = tf.layers.dense(l3, 3, activation=tf.nn.relu)



hypothesis = tf.nn.softmax(logits)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits = logits, labels=tf.stop_gradient([Y_one_hot])))

# train = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(cost)
train = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(cost)
# train = tf.train.AdadeltaOptimizer(learning_rate=0.1).minimize(cost)

prediction = tf.argmax(hypothesis, 1)


correct_prediction = tf.equal(prediction, tf.argmax(Y_one_hot, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))




with tf.Session() as sess:
    # Initialize TensorFlow variables
    

    sess.run(tf.global_variables_initializer())
    
    for step in range(10001):
        _, cost_val, acc_val,l1 = sess.run([train, cost, accuracy,l1], feed_dict={X: x_train, Y: y_train})
        if step % 100 == 0:
            print("Step: {:5}\tCost: {:.3f}\tAcc: {:.2%},{}".format(step, cost_val, acc_val,l1))

    # Let's see if we can predict
    a, pred = sess.run([accuracy, prediction], feed_dict={X: x_test,Y: y_test})
    # y_data: (N, 1) = flatten => (N, ) matches pred.shape
    for p, y in zip(pred, y_test.flatten()):
        print("[{}] Prediction: {} True Y: {}".format(p == int(y), p, int(y)))
    print(a)
    writer = tf.summary.FileWriter('./board/sample_1', sess.graph)
   



