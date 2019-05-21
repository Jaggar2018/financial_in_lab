import tensorflow as tf

images_placeholder = tf.placeholder(tf.float32, shape=(batch_size, IMAGE_PIXELS))
labels_placeholder = tf.placeholder(tf.int32, shape=(batch_size))

wtih tf.name_scope('hideen1') as scope:
    weights = tf.Variable(
        tf.truncated_normal([IMAGE_PICELS, hidden1_units],
                            stddev=1.0/math.sqrt(float(IMAGE_PIXELS)))
        name='weights')
    biases = tf.Variable(tf.zeros([hidden1_units]),name='biases')
    hidden1 = tf.nn.relu(tf.matmul(images,weights)+biases)
    hidden2 = tf.nn.relu(tf.matmul(hidden1,weights)+biases)
    logits = hidden2*weights + biases
    batch_size = tf.size(labels)
    labels = tf.expand_dims(labels, 1)
    indices = tf.expand_dims(tf.range(0,batch_size,1),1)
    concated = tf.concat(1,[indices, labels])
    onehot_labels = tf.sparse_to_dense(concated, tf.pack([batch_size,NU8M_CLASSES]),1.0,0.0)
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits, onehot_labels, name='xentropy')
    loss = tf.reduce_mean(cross_entropy, name='xentropy_mean')
    tf.scalar_summary(loss.op.name, loss)
    optimizer = tf.train.GradientDescentOptimizer(FLAGS.learning_rate)
    global_step = tf.Variable(0,name='global_step',trainable=False)
    train_op = optimizer.minimize(loss, global_step=global_step)

with tf.Graph().as_default():
    sess = tf.Session()
    init =tf.initialize_all_variables()
    sess.run(init)
    for step in range(max_steps):
        sess.run(train_op)
        images_feed, labels_feed = data_set.next_batch(FLAS.batch_size)
        feed_dict={
            images_placeholder: images_feed,
            labels_placeholder: labels_feed,
        }
        _, loss_value = sess.run([train_op, loss], feed_dict=feed_dict)
        if step%100 == 0:
            print('step %d: loss = %.2f(%.3f sec)' % (step, loss_value, duration))
    print('traning data eval')
    do_eval(sess,
            eval_correct,
            images_placeholder,
            labels_placeholder,
            data_sets.train)
