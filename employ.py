from os import linesep
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.algorithms import value_counts
from pandas.core.arrays.categorical import contains
import japanize_matplotlib 
import matplotlib.dates as mdates
import numpy as np
from pandas_estat import set_appid
from pandas_estat import read_statslist
from pandas_estat import read_statsdata 

# 「e-Stat」のAPI機能を用いるためappIdを入力しますが,個人情報に当たりますので,IDは伏せさせていただきます
#　実行したい方は右記のURLからアクセスし,ユーザー登録した後にappIDを取得し,appIDに貼り付けて下さい。https://www.e-stat.go.jp/mypage/user/preregister
appID = "xxxxxxxxxxxxxxxxxxxx" 
set_appid(appID) 

# 「サービス産業動向調査」の政府統計コードを指定する
statslist = read_statslist("00200544")  
statslist = statslist[statslist.CYCLE == "月次"] 
statslist[["TABLE_INF", "TITLE"]]

#　「事務者・企業等の産業(中分類)別事業従事者数」のコードを指定する
df = read_statsdata("0003179101")  
df.columns

set(df["事業所･企業等の産業"])

#　調査対象とした業種を書き出しておく
service = ["サービス産業計","37通信業","38放送業","39情報サービス業","41映像・音声・文字情報制作業","42鉄道業","43道路旅客運送業","44道路貨物運送業","47倉庫業","73広告業","75宿泊業","76飲食店","77持ち帰り・配達飲食サービス業","80娯楽業","83医療業"]

#　複数の業種のデータを一度に取得,分析,可視化するため,それぞれの業種を同じプロセスで作業させる
for i in service:

    ndf = df[df["事業所･企業等の産業"] ==  i ]
    
    #　2020年のデータを取得する
    ndf1 = ndf[ndf["時間軸（月・四半期・年）"].str.contains("2020年")]
    ndf1 = ndf1[ndf1["時間軸（月・四半期・年）"].str.contains("月")]
    tdf = ndf1[["時間軸（月・四半期・年）", "value", "unit"]]
    ndfa=tdf[~tdf["時間軸（月・四半期・年）"].str.contains("期")]
    
    #print(ndfa1["value"].values,type(ndfa1))
    #print( np.mean(list(map(int,list(ndfa1["value"].values)))) )
    #print(np.mean(ndfa1["value"].values,type))

    #　2021年のデータを取得する
    ndf2 = ndf[ndf["時間軸（月・四半期・年）"].str.contains("2021年")]
    ndf2 = ndf2[ndf2["時間軸（月・四半期・年）"].str.contains("月")]
    tdf = ndf2[["時間軸（月・四半期・年）", "value", "unit"]]
    ndf2=tdf[~tdf["時間軸（月・四半期・年）"].str.contains("期")]
    
    #　警告が出てしまうので,コピーしたものをグラフへのプロットに用いる
    ndfb = ndf2.copy()[["時間軸（月・四半期・年）", "value", "unit"]]
    ndfc = ndfb["時間軸（月・四半期・年）"].values
    ndfd = []

    #　もしデータの未確定値を表す"p"があったら"P"を取り除く
    for line in ndfc:
        if " p" in line : 
            ndfd += [line.rstrip().split(" p")[0]]
        else : 
            ndfd += [line.rstrip()]


    ndfb["時間軸（月・四半期・年）"] = ndfd

    #DateFrameからvaluesに変換する
    x1 = ndfa["時間軸（月・四半期・年）"].values
    x2 = ndfb["時間軸（月・四半期・年）"].values
    x=list(x1)+list(x2)

    #　整数値に変換する
    y1 = ndfa["value"].values.astype(float)
    y2 = ndfb["value"].values.astype(float)
    y=list(y1)+list(y2)

    #　書式を設定する
    fig = plt.figure(figsize=(20, 12))
    ax = fig.add_subplot(111)  
    ax.set_facecolor("#e0e0e0")
    
    #　グラフに可視化する
    ax.set_ylabel(str(i)+"の事業者数(人)")
    ax.grid(True,axis="both",color="w", linestyle="dotted", linewidth=0.8,zorder=1)
    ax.set_title(str(i)+"の事業者数変化")
    ax.plot(x,y,marker="o",zorder=100)
    #ax.plot(x2,y2,label="2021年",marker="o",zorder=200)
    ax.legend()

    #　コンピュータ上にグラフを表示する
    plt.show()
    plt.close()
