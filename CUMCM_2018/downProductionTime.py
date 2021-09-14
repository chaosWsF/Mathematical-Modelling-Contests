import numpy as np
import pandas as pd


def find_down_time(data_frame):
    cnc = data_frame.cnc.values
    time = data_frame.time.values
    total = len(cnc)
    for cnc_index in range(total):
        aim = list(cnc[cnc_index + 1:]).index(cnc[cnc_index])
        print(time[aim + cnc_index + 1])


rootPath = './data/'
# filePath = rootPath + 'Case2_comb3.txt'
filePath = rootPath + 'Case3_result2_comb3.txt'
df = pd.read_csv(filePath, sep='\t', header=None, names=['code', 'cnc', 'time', 'error'])
df1 = df[df.code != 'None']
df2 = df[df.code == 'None']

find_down_time(df1)
# find_down_time(df2)
