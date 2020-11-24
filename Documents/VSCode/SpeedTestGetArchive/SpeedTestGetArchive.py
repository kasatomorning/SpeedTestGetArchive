from matplotlib import pyplot as plt
import numpy
import json
from collections import OrderedDict
import pprint
import subprocess
import re

dataLength = 100  # １つのデータの配列の点数
frame = 50  # プロットするフレーム数
sleepTime = 0.0001  # １フレーム表示する時間[s]
yMax = 100 # y軸最大値
yMin = 0 # y軸最小値
ylabel = "Mbps"

def ProcessString(Strings):
    arr1 = str(Strings[1:]).replace("'","").split("\\r\\n")
    arr1.pop(-1)
    arr2 = []
    pattern=r'([+-]?[0-9]+\.?[0-9]*)'
    for item in arr1:
        num = re.search(pattern, item).groups()
        arr2.append(float(num[0]))
    #arr2[ping,download,upload]
    if len(arr2) >= frame:
        arr2.pop(0)
    return arr2 if arr2 != [] else [0,0,0]

def main():
    url_and_options = ["speedtest-cli","--simple"]
    Data = []
    #fig, axes = plt.subplots(0, 0, figsize=(100, 50))
    for i in range(frame): # フレーム回数分グラフを更新
        #data = numpy.random.rand(dataLength) # プロットするデータを作成
        try:
            res = subprocess.run(url_and_options,stdout=subprocess.PIPE)
        except:
            print("Error.")
        OutPut = res.stdout 
        Data.append(ProcessString(OutPut))
        print(Data)

        plt.cla() #プロットした点を消してグラフを初期化

        plt.ylim(yMin, yMax)
        plt.ylabel("Mbps")
        plt.grid(True)

        plt.plot([_lis[1] for _lis in Data],label="Download") # データをプロット
        plt.plot([_lis[2] for _lis in Data],label="Upload") # データをプロット
        plt.legend()#labelの後に

        plt.draw() # グラフを画面に表示開始
        plt.pause(sleepTime) # SleepTime時間だけ表示を継続

if __name__ == "__main__":
    main()  