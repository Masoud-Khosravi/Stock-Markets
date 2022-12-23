import matplotlib.pylab as plt
import seaborn as sns


def plot_line(dataframe, column='close'):
    """
    pass raw dataframe
    and select column name to plot --> default:'close'

    Note: in Large dataframe may not be good
    """
    sns.set_style('whitegrid')
    dataframe[column].plot(figsize=(12, 4), color='blue')
    a = plt.xticks()
    df_last_idx = dataframe.index[-1]
    if a[0][-2] > df_last_idx:
        labels = dataframe['time'][a[0][1:-2]]
        labels[df_last_idx] = dataframe['time'].iloc[-1]
    else:
        labels = dataframe['time'][a[0][1:-1]]
    labels = labels.apply(lambda x: x.strftime('%d-%m %H:%M'))
    plt.xticks(a[0][1:-1], labels=labels)
    plt.tight_layout()
    plt.margins(x=0)
    plt.show()


def plot_candlestick(dataframe):
    """
    pass raw dataframe

    Note: in Large dataframe may not be good
    """
    plt.figure(figsize=(16, 6), dpi=250)
    plt.style.use('dark_background')
    plt.grid(True, alpha=0.35, color='w', linestyle=':', linewidth=1)
    # define width of candlestick elements
    width = 0.8
    width2 = 0.2

    # define up and down prices
    up = dataframe[dataframe.close >= dataframe.open]
    down = dataframe[dataframe.close < dataframe.open]

    # define colors to use
    col1 = 'green'
    col2 = 'gold'

    # plot up prices
    plt.bar(up.index, up.high - up.low, width=width2, bottom=up.low, color=col1, edgecolor='none')
    plt.bar(up.index, up.close - up.open, width=width, bottom=up.open, color=col1, edgecolor='none')

    # plot down prices
    plt.bar(down.index, down.high - down.low, width=width2, bottom=down.low, color=col2, edgecolor='none')
    plt.bar(down.index, down.open - down.close, width=width, bottom=down.close, color=col2, edgecolor='none')

    # this part change xtick labels to datetime and plot good even pass discontinuous data
    a = plt.xticks()
    df_last_idx = dataframe.index[-1]
    if a[0][-2] > df_last_idx:
        labels = dataframe['time'][a[0][1:-2]]
        labels[df_last_idx] = dataframe['time'].iloc[-1]
    else:
        labels = dataframe['time'][a[0][1:-1]]
    labels = labels.apply(lambda x: x.strftime('%d-%m %H:%M'))
    plt.xticks(a[0][1:-1], labels=labels)

    plt.tight_layout()
    plt.margins(x=0)
    # plt.legend(loc='lower left')
    # plt.savefig('Mas')
    plt.show()
