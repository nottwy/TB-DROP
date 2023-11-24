import numpy as np
from tensorflow.keras.callbacks import Callback

#重写原则：
#1. For the parameter which exists before and is changed here, we should check every place in the original code where this parameter is used. Because the new value we assign to it may break the original logic.

# MCP: model check point
# rewrite: 20210408
# The reason I write this Custom Model Check Point:
# The ModelCheckPoint provided by the tf has to write the model into the file at each epoch.
# it will slow down the training progress because lots of time is wasted for writing to the file.
# Therefore, I implement my own CustomMCP. It will save the best during training and write the best model to the file after training.

class CustomMCP(Callback):
    def __init__(self,
                 filepath,
                 monitor='val_loss',
                 save_freq='train',
                 save_best_only=True,
                 save_weights_only=False,
                 mode='auto',
                 verbose=0
                 ):
        super(CustomMCP, self).__init__()
        self.filepath = filepath
        self.monitor  = monitor
        self.save_freq = save_freq
        self.save_best_only = save_best_only
        self.save_weights_only = save_weights_only
        self.verbose  = verbose
        self.mode = mode

        #internal variable
        self.best_model = None

        if mode == "min":
            self.monitor_op = np.less
            self.best = np.Inf
        elif mode == 'max':
            self.monitor_op = np.greater
            self.best = -np.Inf

    def on_epoch_end(self,epoch,logs=None):
        if self.save_freq == "train":
            self.save_item_model(epoch=epoch,logs=logs)

    def on_train_end(self, logs=None):
        self.best_model.save(self.filepath,overwrite=True)

    def save_item_model(self,epoch,logs=None):
        if self.save_best_only:
            current = logs.get(self.monitor)
            if current is None:
                if self.verbose == 1:
                  print("\nNOTT's CustomMCP: %s is not available, skip this epoch!\n" %
                      (self.monitor))
            else:
                if self.monitor_op(current, self.best):
                    self.best = current
                    if self.save_weights_only:
                        pass
                    else:
                        self.best_model = self.model
                else:
                    if self.verbose == 1:
                        print("\nNOTT's CustomMCP: Epoch %05d: %s did not improve from %0.5f\n" %
                              (epoch+1,self.monitor,self.best))



