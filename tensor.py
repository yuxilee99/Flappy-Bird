# #initialise 2 constants
# x1 = tf.constant([1,2,3,4])
# x2 = tf.constant([5,6,7,8])
# 
# # Multiply
# result = tf.multiply(x1, x2)
# 
# # Print the result
# print(result)

'''tensorflow tutorial https://www.datacamp.com/community/tutorials/tensorflow-tutorial'''

import tensorflow as tf 

#initialize placeholders 
x = tf.placeholder(dtype = tf.float32, shape = [None, 28, 28])
y = tf.placeholder(dtype = tf.int32, shape = [None])

#flatten the input data
images_flat = tf.contrib.layers.flatten(x)

#fully connected layer 
logits = tf.contrib.layers.fully_connected(images_flat, 62, tf.nn.relu)

#define a loss function
loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels = y, 
                                                                    logits = logits))
#define an optimizer 
train_op = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

#convert logits to label indexes
correct_pred = tf.argmax(logits, 1)

#define an accuracy metric
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))