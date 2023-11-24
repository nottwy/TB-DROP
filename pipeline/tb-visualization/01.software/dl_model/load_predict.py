import numpy as np
import sys
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow.keras.models import load_model
from dlCallback import CustomMCP
from clr_callback import CyclicLR
from custom_function import bce_without_nan,acc_without_nan

#usage
#python % feature 

#1. load the model
custom_objects={'CustomMCP': CustomMCP,
                'CyclicLR': CyclicLR,
                'masked_weighted_accuracy':acc_without_nan,
                'masked_multi_weighted_bce':bce_without_nan}

model_path="/root/pipeline/tb-visualization/01.software/dl_model/best_mlp"

final_model = load_model(model_path,custom_objects=custom_objects)

#2. load the feature
feature = np.loadtxt(sys.argv[1],delimiter=",")
indices = np.load("/root/pipeline/tb-visualization/01.software/dl_model//indices.npy")
feature = feature.reshape(1,feature.shape[0])
feature = feature[:,indices]
#3. predict
#final_model.predict(self.feature[index])
probs = final_model.predict(feature)

#4. interpret
drug_name = ["ISONIAZID","RIFAMPICIN","ETHAMBUTOL","PYRAZINAMIDE"]
thresholds = [0.10845331847667694,0.13310736417770386,0.48224586248397827,0.15203750133514404]

for drug,th,p in zip(drug_name,thresholds,probs[0]):
    if p >= th:
        with open('/root/pipeline/tb-visualization/05.drug_resistance_prediction/'+sys.argv[2],'a') as f:
            f.write("%s,resistant" % drug + '\n')
#    print("%s,resistant" % drug)
    else:
        with open('/root/pipeline/tb-visualization/05.drug_resistance_prediction/'+sys.argv[2],'a') as f:
            f.write("%s,sensitive" % drug + '\n')
#    print("%s,sensitive" % drug)
