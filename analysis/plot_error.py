import pandas as pd 
import sys
import seaborn as sns
import json
import matplotlib.pyplot as plt 

# sns.set(style="whitegrid")
if len(sys.argv) > 1:
    configJsonName = sys.argv[1]
    error = sys.argv[2]
else:
    configJsonName = "test_configs/all_runs.json"
    error = 'rmse'

plt.rcParams.update({'font.size': 16})

error_df = pd.DataFrame()
config = json.load(open(configJsonName, 'r'))
for system in config["systems"]:
    for app in config["applications"][system]:
        for datasize in config["datasizes"]:
            plt.figure(figsize=(4,2.5))
            title = system+"_"+app+"_"+datasize
            # print(title)
            df = pd.read_csv('../algorithms/error/'+'error_'+ title + '.csv')
            error_df = error_df.append(df)
            ax= sns.boxplot(x="algorithm",y=error, data=df, showfliers=False)
            # ax = sns.violinplot(y='rmse', x="algorithm", data=df, cut=0)
            # print(df.groupby(['algorithm']).describe())
            # 
            labels = [l.get_text().replace("bo_", "").replace('_','-').upper() for l in ax.get_xticklabels()]
            ax.set_xticklabels(labels, rotation=45)
            plt.title(title)
            plt.ylabel(error.upper())
            plt.xlabel('Algorithm')
            plt.savefig('plots/error/error_'+ error +'_'+ title + '.pdf', bbox_inches = "tight")

plt.figure()
ax= sns.boxplot(x="algorithm",y=error, data=error_df, showfliers=False)
# ax = sns.violinplot(y='rmse', x="algorithm", data=df, cut=0)
print(df[[error, "algorithm"]].groupby(['algorithm']).describe())
ax.set_xticklabels(labels, rotation=45)
# plt.title(title)
plt.ylabel(error.upper())
plt.xlabel('Algorithm')
plt.savefig('plots/error/error_'+ error + '.pdf', bbox_inches = "tight")