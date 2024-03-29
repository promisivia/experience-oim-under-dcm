import csv
from scipy import signal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.interpolate import make_interp_spline


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
    fileList = []
    for filename in os.listdir(fileFolderPath):
        if filename[-4:] == ".csv":
            csv_reader = csv.reader(open(fileFolderPath + "/" + filename, encoding='utf-8'))
            length = np.array(list(csv_reader)).shape[0]
            if length >= count:
                fileList.append(fileFolderPath + "/" + filename)
    print(len(fileList))

    data_list = []

    for fileTotalPath in fileList:
        data = pd.read_csv(fileTotalPath)
        data = data[algo].values[:count]

        if drawType == "Cumulative":
            data = array2CumulativeArray(data)

        elif drawType == "Average":
            data = array2AverageArray(data)

        else:
            pass
        print("file path:", fileTotalPath, "average is", data[-1])
        data_list.append(data)

    timeStamp = np.arange(1, data_list[0].shape[0] + 1)
    sqrtNSequence = np.sqrt(timeStamp)

    data_list_Array = np.vstack(data_list)
    data_Array_Average = np.mean(data_list_Array, axis=0)
    data_Array_STD = np.std(data_list_Array, ddof=1, axis=0)
    data_Array_STE = data_Array_STD / sqrtNSequence

    return data_Array_Average, data_Array_STE, timeStamp, sqrtNSequence


def draw_Reward(fileFolderPath, alg_list, count, y_start=-1, y_end=-1, drawType="Default", Title=None, issave=False,
                file_name='', subTitile=''):
    ax = plt.gca()

    for (path_tail, algor, color, label) in alg_list:
        path = fileFolderPath + path_tail
        data_Array_Average, data_Array_STE, timeStamp, sqrtNSequence = getDataOfOneAlg(path, algor, count=count, drawType=drawType)

        y_smooth = signal.savgol_filter(data_Array_Average, 301, 3)
        # y_smooth = data_Array_Average
        print("algo:", path_tail, "average is", data_Array_Average[-1])

        # y_smooth = data_Array_Average

        ax.fill_between(timeStamp, y_smooth - data_Array_STE, y_smooth + data_Array_STE,
                        facecolors='gray')
        plt.plot(y_smooth, color=color, linestyle='-', label=label)

    # if Title is not None:
    #     plt.title(Title)
    plt.title(subTitile, fontsize=16)
    plt.tick_params(labelsize=12)
    # plt.text(0, 0, subTitile, fontsize=15, verticalalignment="top", horizontalalignment="right")
    plt.legend(loc='lower right', fontsize=13)
    plt.xlabel('Iteration', fontsize=13)
    plt.ylabel(drawType + "d " + 'Reward', fontsize=13)
    # plt.title(fileFolderPath[25:len(fileFolderPath) - 1] + "_" + drawType + "_count=" + str(count))
    if y_start != -1:
        plt.ylim(ymin=y_start)
    if y_end != -1:
        plt.ylim(ymax=y_end)

    if file_name == '':
        file_name = fileFolderPath[25:len(fileFolderPath) - 1] + "_count=" + str(count) + ".pdf"
    else:
        file_name = file_name + ".pdf"

    save_address = '../SimulationResults/result/'
    isExist = os.path.exists(save_address)
    if not isExist:
        os.makedirs(save_address)
    print(save_address)
    if issave:
        plt.savefig(save_address + file_name)
        print("Saved")
    plt.show()
