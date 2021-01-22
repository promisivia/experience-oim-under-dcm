import csv
import numpy as np
import pandas as pd
import os


def array2CumulativeArray(rawArray):
    tmpRes = np.arange(len(rawArray))
    for i in range(len(rawArray)):
        tmpRes[i] = np.sum(rawArray[:(i + 1)])
    return tmpRes


def array2AverageArray(rawArray):
    tmpRes = np.arange(len(rawArray), dtype=float)
    for i in range(len(rawArray)):
        tmpRes[i] = np.sum(rawArray[:(i + 1)]) / float(i + 1.0)
    return tmpRes


def getDataOfOneAlg(fileFolderPath, algo, count, drawType="Default"):
    # 构造路径
    fileList = []
    for filename in os.listdir(fileFolderPath):
        if filename[-4:] == ".csv":
            csv_reader = csv.reader(open(fileFolderPath + "/" + filename, encoding='utf-8'))
            length = np.array(list(csv_reader)).shape[0]
            # print(filename, length)
            if length >= count:
                fileList.append(fileFolderPath + "/" + filename)
    print(len(fileList))

    data_list = []

    for fileTotalPath in fileList:
        # 读取
        data = pd.read_csv(fileTotalPath)
        data = data[algo].values
        # 进行处理
        data = array2AverageArray(data)
        print("file path:", fileTotalPath, "length is:", len(data), "average is", data[-1])
        data_list.append(data[-1])

    average = np.mean(data_list)

    return average


def average(fileFolderPath, alg_list, count, y_start=-1, y_end=-1, drawType="Default", Title=None, issave=False, file_name='', subTitile=''):
   for (path_tail, algor, color, label) in alg_list:
        path = fileFolderPath + path_tail
        average = getDataOfOneAlg(path, algor, count=count, drawType=drawType)
        print("algo:", path_tail, "average is", average)



