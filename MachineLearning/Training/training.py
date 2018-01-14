# NumPy is often used to load, manipulate and preprocess data.
import numpy as np
import tensorflow as tf

def trainSignsCore():
	x = tf.placeholder(tf.float32, [None,136*22])
	W = tf.Variable(tf.zeros([136*22,95]))
	b = tf.Variable(tf.zeros([95]))
	y = tf.nn.softmax(tf.matmul(x,W) + b)
	y_ = tf.placeholder(tf.float32, [None,95])
	
	cross_entropy = tf.reduce_mean(
		tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
	train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

	sess = tf.InteractiveSession()
	tf.global_variables_initializer().run()

	with np.load(".\etc\DataSet\pickledData\savedData.npz") as data:
		features = data["features"]
		labels = data["labels"]

	assert features.shape[0] == labels.shape[0]
	dataset = tf.data.Dataset.from_tensors((tf.constant(features), tf.constant(labels)))
	print("from tensors")
	print(dataset)

trainSignsCore()