from os import linesep
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib 
import matplotlib.dates as mdates
from pandas_estat import set_appid
from pandas_estat import read_statslist
from pandas_estat import read_statsdata 

# 「e-Stat」のAPI機能を用いるためappIdを入力しますが,個人情報に当たりますので,IDは伏せさせていただきます
appID = "xxxxxxxxxxxxxxxxxxxx" 
set_appid(appID) 

# 「サービス産業動向調査」の政府統計コードを指定する
statslist = read_statslist("00200544")  
statslist = statslist[statslist.CYCLE == "月次"] 
statslist[["TABLE_INF", "TITLE"]]

#　「事業活動の産業(中分類)別売上高」のコードを指定する
df = read_statsdata("0003191203")  
df.columns
set(df["事業活動の産業"])

#　調査対象とした業種を書き出しておく
service = ["サービス産業計","37通信業","38放送業","39情報サービス業","41映像・音声・文字情報制作業","42鉄道業","43道路旅客運送業","44道路貨物運送業","47倉庫業","73広告業","75宿泊業","76飲食店","77持ち帰り・配達飲食サービス業","80娯楽業","83医療業"]

#　複数の業種のデータを一度に取得,分析,可視化するため,それぞれの業種を同じプロセスで作業させる
for i in service:

    ndf = df[df["事業活動の産業"] == i ]

    #　2020年のデータを取得する
    ndf1 = ndf[ndf["時間軸（月次）"].str.contains("2020年")]
    ndfa = ndf1[["時間軸（月次）", "value", "unit"]]
    
    #　2021年のデータを取得する
    ndf2 = ndf[ndf["時間軸（月次）"].str.contains("2021年")] 
    
    #　警告が出てしまうので,コピーしたものをグラフへのプロットに用いる
    ndfb = ndf2.copy()[["時間軸（月次）", "value", "unit"]]
    ndfc = ndfb["時間軸（月次）"].values
    ndfd = []
    
    #　もしデータの未確定値を表す"p"があったら"P"を取り除く
    for line in ndfc:
        if " p" in line : 
            ndfd += [line.rstrip().split(" p")[0]] 
        else : 
            ndfd += [line.rstrip()]

    ndfb["時間軸（月次）"] = ndfd

    #DateFrameからvaluesに変換する
    x1 = ndfa["時間軸（月次）"].values
    x2 = ndfb["時間軸（月次）"].values
    x=list(x1)+list(x2)

    # XX億円に換算する
    y1 = ndfa["value"].values.astype(float) * 1.e-2  
    y2 = ndfb["value"].values.astype(float) * 1.e-2
    y=list(y1)+list(y2)

    #　書式を設定する
    fig = plt.figure(figsize=(20, 12)) 
    ax = fig.add_subplot(111)  
    ax.set_facecolor("#e0e0e0")
    
    #　グラフに可視化する
    ax.set_ylabel(str(i)+"の収益(億円)")
    ax.grid(True,axis="both",color="w", linestyle="dotted", linewidth=0.8,zorder=1)
    ax.set_title(str(i)+"の収益変化")
    ax.plot(x,y,marker="o",zorder=100)
    ax.legend()

    #　コンピュータ上にグラフを表示する
    plt.show()
    plt.close()
