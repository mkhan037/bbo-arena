import sys
from models import models
import json
import os
import time
import pandas as pd

number_of_nodes = {
'large': [4, 6, 8, 10, 12, 16, 24, 32, 40, 48],
'xlarge': [4, 6, 8, 10, 12, 16, 20, 24],
'2xlarge': [4, 6, 8, 10, 12]
}
types = ['m4', 'c4', 'r4']
sizes = ['large', 'xlarge', '2xlarge']
parent_dir = '../scout/dataset/osr_multiple_nodes/'

# python plot_all_runtimes.py pagerank spark
config = json.load(open(sys.argv[1], 'r'))

budget = config["budget"]

for system in config["systems"]:
    for app in config["applications"][system]:
        for datasize in config["datasizes"]:
            data = list()
            for algo in config["bbo_algos"]:
                filename = system + '_' + app + '_' + datasize + '_' + algo
                if algo == "bo":
                    for estimator in config["bo_estimators"]:
                        for acq_method in config["bo_acq"][estimator]:
                            new_filename = filename + '_' + estimator + '_' + acq_method
                            print(new_filename)
                            m = models(new_filename, app, system, datasize, budget, parent_dir, types, sizes, number_of_nodes, optimizer=estimator, initial_samples=6, acquisition_method=acq_method)
                            # print(new_filename)
                            d = m.buildModel()
                            mse = d['mse']
                            rmse = d['rmse']
                            for e1, e2 in zip(mse, rmse):
                                data.append([ e1, e2, algo+'_'+estimator+'_'+acq_method])

            df = pd.DataFrame(data, columns=['mse', 'rmse', 'algorithm'])
            df.to_csv('error/'+'error_'+system + '_' + app + '_' + datasize+'.csv', index=False)