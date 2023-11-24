def bce_without_nan(alpha, y_pred):
    #upweight sparser class
    #resistant ,+1>0,P=y_pred
    #susceptive,-1<0,P=1-y_pred
    epsilon = 1e-07
    y_pred = tf.clip_by_value(y_pred, epsilon, 1.0 - epsilon)
    y_true_mask = tf.cast(tfmath.greater(alpha,0.),tf.float32)
    pheno_mask = tf.cast(tfmath.not_equal(alpha,0.),tf.float32) # 0 or 1
    ind_pheno_n = tfmath.reduce_sum(pheno_mask,axis=1)
    alpha = tfmath.abs(alpha)

    bce = - alpha * y_true_mask * tfmath.log(y_pred) - (1.0 - alpha) * (1 - y_true_mask) * tfmath.log(1 - y_pred)
    masked_bce = bce * pheno_mask
    # todo: every drug could own its own weight,so we could get a different sum
    return tfmath.reduce_sum(masked_bce,axis = 1) / ind_pheno_n

def acc_without_nan(alpha, y_pred):
    total   = tfmath.reduce_sum(
                tf.cast(tf.not_equal(alpha, 0.), tf.float32),
                axis=1
              )
    y_true_mask = tf.cast(tfmath.greater(  alpha, 0.), tf.float32)
    pheno_mask  = tf.cast(tfmath.not_equal(alpha, 0.), tf.float32)
    correct = tf.reduce_sum(
                tf.cast(tf.equal(y_true_mask, tf.round(y_pred)), tf.float32) * pheno_mask,
                axis=1
              )
    return correct / total
