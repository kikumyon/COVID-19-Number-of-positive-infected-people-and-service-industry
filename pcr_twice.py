from os import linesep
from numpy import r_
import pandas as pd
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
import japanize_matplotlib 
import matplotlib.pyplot as plt

register_matplotlib_converters()

# 厚生労働省のオープンデータ「陽性者数」へアクセスする
url = "https://www.mhlw.go.jp/content/pcr_positive_daily.csv"

# csvファイルを読み込む
df = pd.read_csv(url,index_col='日付',parse_dates=True)
 
# マルチインデックスで「タイムスタンプ」以外に「年」と「月」をセットする
df = df.set_index([df.index.year, df.index.month, df.index])
df.index.names = ['year', 'month', 'date']      

# 月ごとに集計する
# 年月単位で合計を集計する
summary = df.sum(level=('year', 'month'))        
summary = summary.reset_index()  

# 「year」列を文字列にする
summary['year'] = summary['year'].astype(str) 

# 「month」列を文字列にする
summary['month'] = summary['month'].astype(str)  

df=summary

# 「year」と「month」列を「-」で繋ぎ、タイムスタンプに変換する
date = df['year'].str.cat(df['month'], sep='/')
pytorch = df['PCR 検査陽性者数(単日)']

# 書式を設定する
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
fig = plt.figure(figsize=(18, 8))
axs = [ fig.add_subplot(211), fig.add_subplot(212)]
axs[1].set_yscale("log")

#　グラフに可視化する
for ax in axs:
    ax.set_facecolor("#e0e0e0")
    ax.yaxis.set_ticks_position('both')
    ax.set_ylabel('PCR検査陽性者数')
    ax.grid(True,axis="both",color="w", linestyle="dotted", linewidth=0.8,zorder=1)    
    ax.bar(date, pytorch, label='PCR検査陽性者数', zorder=200)
    ax.legend()     
fig.tight_layout()

#　保存する
#　パス名は個人情報に当たりますので,一部伏せさせていただきます
plt.savefig("/xxxxx/xxxxx/pcr_twice.pdf")

#　コンピュータ上にグラフを表示する
plt.show()
plt.close()