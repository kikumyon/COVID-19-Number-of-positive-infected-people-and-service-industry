from os import linesep
import pandas as pd 
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import japanize_matplotlib
import matplotlib.dates as mdates
import numpy as np
from pandas_estat import set_appid
from pandas_estat import read_statslist
from pandas_estat import read_statsdata 

#　事前に作成しておいた月毎のPCR検査陽性者数のCSVファイルを読み込む
#　パス名は個人情報に当たりますので,一部伏せさせていただきます
df=pd.read_csv('/xxxxx/xxxxx/pcr.csv')
dfc=df['pcr']
x=dfc


#　2020年のPCR検査陽性者数をlist型に変換する
xx=x.tolist()
xx=(xx[0:12])

#　2021年のPCR検査陽性者数をlist型に変換する
xz=x.tolist()
xy=(xz[12:])

#　2020年と2021年のPCR検査陽性者数を合計する
xd=xx+xy
print(xd)

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
    print(i)

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

    # XX億円に換算
    y1 = ndfa["value"].values.astype(float) * 1.e-2  
    y2 = ndfb["value"].values.astype(float) * 1.e-2

    y1a=y1.tolist()
    y1b=y2.tolist()

    #　相関係数計算のため,2020年と2021年のサービス業を合計する
    y=y1a+y1b

    #　２つのデータの相関係数を計算する
    xs= np.array(xd); yy= np.array(y)
    r = np.corrcoef(xs,yy)  
    corrcoef=r[0,1]    
    
    #　書式を設定する
    fig=plt.figure(figsize=(15,8)) 
    ax=fig.add_subplot(111)
    ax.set_facecolor("#D3DEF1")

    #　グラフに可視化する
    ax.set_title("月別PCR検査陽性者数と"+str(i)+"の収益の相関関係") 
    ax.set_xlabel("月別PCR検査陽性者数(人)") 
    ax.set_ylabel(str(i)+"の収益(億円)")
    ax.grid(True,axis="both",color="w", linestyle="dotted", linewidth=0.8)
    ax.text(0.1,0.9, "r="+str("%5.2f" % corrcoef), transform=ax.transAxes,fontsize=12)

    #　プロットした点に,2020年,2021年の区別をつけ,それぞれ月表示をさせる
    ax.scatter(x[0:12],y1a[0:12],marker="o",s=15,color="blue",zorder=20000,alpha=0.7,label="2020年")
    ax.scatter(xy[0:4],y1b[0:4],marker="o",s=15,color="red",zorder=20000,alpha=0.7,label="2021年")

    for f in range(12):
        ax.text(x[f]+1000,y1a[f],str(f+1)+"月",color="k",fontsize=10)
    
    for f in range(4):
        ax.text(xy[f]+1000,y1b[f],str(f+1)+"月",color="k",fontsize=10)
    ax.legend()
    
    #　保存する
    #　パス名は個人情報に当たりますので,一部伏せさせていただきます
    plt.savefig("/xxxxx/xxxxx/"+str(i)+"v0710.pdf")
    
    #　コンピュータ上にグラフを表示する
    plt.show()
    plt.close() 