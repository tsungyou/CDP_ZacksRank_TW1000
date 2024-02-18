import yfinance as yf
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

# loading the data
indices = ["^GSPC","TLT", ]
data = yf.download(indices,start='2020-01-01')
data = data['Adj Close']
inv_growth = (data.pct_change().dropna() + 1).cumprod()

# plotting the data

fig, ax = plt.subplots()

ax.set_xlim(inv_growth.index[0], inv_growth.index[-1])
ax.set_ylim(940, 1100)

line, = ax.plot(inv_growth.index[0], 1000)

x_data = []
y_data = []

def animation_frame(date):
    x_data.append(date)
    y_data.append(inv_growth.loc[date])
    
    line.set_xdata(x_data)
    line.set_ydata(y_data)
    
    return line,

animation = FuncAnimation(fig, 
                          func=animation_frame, 
                          frames=list(inv_growth.index), 
                          interval = 100)
plt.show()