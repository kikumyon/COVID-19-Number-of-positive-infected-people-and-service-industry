from os import linesep
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib 
import matplotlib.dates as mdates
from pandas.core.frame import DataFrame 
import numpy as np
from pandas_estat import set_appid
from pandas_estat import read_statslist
from pandas_estat import read_statsdata 

# 「e-Stat」のAPI機能を用いるためappIdを入力しますが,個人情報に当たりますので,IDは伏せさせていただきます
appID = "xxxxxxxxxxxxxxxxxx" 
set_appid(appID) 

# サービス産業動向調査の政府統計コードを指定する
statslist = read_statslist("00200544")  
statslist = statslist[statslist.CYCLE == "月次"] 
statslist[["TABLE_INF", "TITLE"]]

#　「事業活動の産業(中分類)別売上高」のコードを指定する
df = read_statsdata("0003191203")  
df.columns
set(df["事業活動の産業"])

# 「サービス産業動向調査」の政府統計コードを指定する 
statslist = read_statslist("00200544")  
statslist = statslist[statslist.CYCLE == "月次"] 
statslist[["TABLE_INF", "TITLE"]]

#　「事務者・企業等の産業(中分類)別事業従事者数」のコードを指定する
sdf = read_statsdata("0003179101")  
sdf.columns
set(sdf["事業所･企業等の産業"])

#　調査対象とした業種を書き出しておく
service = ["サービス産業計","37通信業","38放送業","39情報サービス業","41映像・音声・文字情報制作業","42鉄道業","43道路旅客運送業","44道路貨物運送業","47倉庫業","73広告業","75宿泊業","76飲食店","77持ち帰り・配達飲食サービス業","80娯楽業","83医療業"]

#　複数の業種のデータを一度に取得,分析,可視化するため,それぞれの業種を同じプロセスで作業させる
for i in service:
    
    #　「サービス産業動向調査」の全ての業種の調査を,ループを回し実行する
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
            ndfd += [line.rstrip().split("p")[0]]
        else:
            ndfd += [line.rstrip()]

    ndfb["時間軸（月次）"] = ndfd

    # XX億円に換算する
    y1 = ndfa["value"].values.astype(float) * 1.e-2  
    y2 = ndfb["value"].values.astype(float) * 1.e-2
    
    #　リストに変換する
    y1a=y1.tolist()
    y1b=y2.tolist()

    #　相関係数計算のため,2020年と2021年のサービス産業動向調査の売上高を合計する
    x=y1a+y1b
    
    #　「事務者・企業等の産業(中分類)別事業従事者数」の全ての業種の調査を,ループを回し実行する
    nndf = sdf[sdf["事業所･企業等の産業"] ==  i ] 
    
    #　2020年のデータを取得する
    nndf1 = nndf[nndf["時間軸（月・四半期・年）"].str.contains("2020年")]
    nndf1 = nndf1[nndf1["時間軸（月・四半期・年）"].str.contains("月")]
    tdf = nndf1[["時間軸（月・四半期・年）", "value", "unit"]]
    nndfa=tdf[~tdf["時間軸（月・四半期・年）"].str.contains("期")]
    
    #　2021年のデータを取得する
    nndf2 = nndf[nndf["時間軸（月・四半期・年）"].str.contains("2021年")]
    nndf2 = nndf2[nndf2["時間軸（月・四半期・年）"].str.contains("月")]
    tdf = nndf2[["時間軸（月・四半期・年）", "value", "unit"]]
    nndf2=tdf[~tdf["時間軸（月・四半期・年）"].str.contains("期")]
    
    #　警告が出てしまうので,コピーしたものをグラフへのプロットに用いる
    nndfb = nndf2.copy()[["時間軸（月・四半期・年）", "value", "unit"]]
    nndfc = nndfb["時間軸（月・四半期・年）"].values
    nndfd = []
    for line in nndfc:
        if " p" in line : 
            nndfd += [line.rstrip().split(" p")[0]]
        else : 
            nndfd += [line.rstrip()]

    nndfb["時間軸（月・四半期・年）"] = nndfd

    #　整数値に変換する
    yn1 = nndfa["value"].values.astype(float)
    yn2 = nndfb["value"].values.astype(float)

    #　リストに変換する
    yn1a=yn1.tolist()
    yn1b=yn2.tolist()

    #　相関係数計算のため,2020年と2021年の事業従事者数を合計する
    yn=yn1a+yn1b

    #　２つのデータの相関係数を計算する
    xx= np.array(x); yy= np.array(yn)
    r = np.corrcoef(xx,yy) 
    corrcoef=r[0,1] 

    #　書式を設定する
    fig=plt.figure(figsize=(15,8)) 
    ax=fig.add_subplot(111)
    ax.set_facecolor("#D3DEF1")

    #　グラフに可視化する
    ax.set_title(str(i)+"の収益と事業者数の相関関係") 
    ax.set_xlabel(str(i)+"の収益(億円)") 
    ax.set_ylabel("事業者数(人)")
    ax.grid(True,axis="both",color="w", linestyle="dotted", linewidth=0.8)
    ax.text(0.1,0.9, "r="+str("%5.2f" % corrcoef), transform=ax.transAxes,fontsize=12)

    #　プロットした点に,2020年,2021年の区別をつけ,それぞれ月表示をさせる
    ax.scatter(y1a,yn1a,marker="o",s=15,color="blue",zorder=20000,alpha=0.7,label="2020年")
    ax.scatter(y1b,yn1b,marker="o",s=15,color="red",zorder=20000,alpha=0.7,label="2021年")

    for f in range(12):
        ax.text(y1a[f]+10,yn1a[f]+7.5,str(f+1)+"月",color="k",fontsize=10)
    
    for f in range(len(yn1b)):
        ax.text(y1b[f]+10,yn1b[f]+7.5,str(f+1)+"月",color="k",fontsize=10)
    ax.legend()

    #　コンピュータ上にグラフを表示する
    plt.show()
    plt.close() 
