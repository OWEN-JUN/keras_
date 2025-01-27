
import tensorflow as tf 
import numpy as np 
tf.set_random_seed(777)

sess = tf.Session()

xy = np.loadtxt('./Study_DL/TF/data/data-04-zoo.csv', delimiter=',', dtype=np.float32)
x_data = xy[:, 0:-1] 
y_data = xy[:, [-1]]

print(x_data.shape, y_data.shape) # x.shape(101, 16) / y.shape(101,1)

# from keras.utils import np_utils
# y_data = np_utils.to_categorical(y_data)

# print(x_data.shape, y_data.shape) # x.shape(101, 16) / y.shape(101,7)

nb_classes = 7 # 0 ~ 6

X = tf.placeholder(tf.float32, [None, 16])
Y = tf.placeholder(tf.int32, [None, 1]) # 0 ~ 6

Y_one_hot = tf.one_hot(Y, nb_classes) # one-hot
print("one_hot:", Y_one_hot)
Y_one_hot = tf.reshape(Y_one_hot, [-1, nb_classes])
print("reshape one_hot:", Y_one_hot)

'''
one_hot: Tensor("one_hot:0", shape=(?, 1, 7), dtype=float32)
reshape one_hot: Tensor("Reshape:0", shape=(?, 7), dtype=float32)
'''

W = tf.Variable(tf.random_normal([16, nb_classes]), name='weight')
b = tf.Variable(tf.random_normal([nb_classes]), name='bias')

# tf.nn.softmax computes softmax activations
# softmax = exp(logits) / reduce_sum(exp(logits), dim)
logits = tf.matmul(X, W) + b
hypothesis = tf.nn.softmax(logits)

# cross entropy cost/loss
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits,
                                        labels=tf.stop_gradient([Y_one_hot])))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost)

prediction = tf.argmax(hypothesis, 1)
correct_prediction = tf.equal(prediction, tf.argmax(Y_one_hot, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Launch graph
with tf.Session() as sess:
    # Initialize TensorFlow variables
    

    sess.run(tf.global_variables_initializer())
    print(y_data)
    for step in range(5001):
        _, cost_val, acc_val = sess.run([optimizer, cost, accuracy], feed_dict={X: x_data, Y: y_data})
        if step % 100 == 0:
            print("Step: {:5}\tCost: {:.3f}\tAcc: {:.2%}".format(step, cost_val, acc_val))

    # Let's see if we can predict
    a, pred = sess.run([accuracy, prediction], feed_dict={X: x_data,Y: y_data})
    # y_data: (N, 1) = flatten => (N, ) matches pred.shape
    for p, y in zip(pred, y_data.flatten()):
        print("[{}] Prediction: {} True Y: {}".format(p == int(y), p, int(y)))
    print(a)
    writer = tf.summary.FileWriter('./board/sample_1', sess.graph)
   
    