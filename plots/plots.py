import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter

class Plotter:
    def make_plot_all(self, id, data):
        fig = plt.figure(figsize=(9,9))
        ax = fig.subplots()
        plt.title('Services all')
        plt.xlabel('Date')
        plt.ylabel('Quantity')
        servises_set = {i['Service'] for i in data}
        for servise in servises_set:
            x = np.array([np.datetime64(i['Date'], 'M') for i in data if i['Service'] == servise])
            y = np.array([i['Summ'] for i in data if i['Service'] == servise])
            plt.plot(x, y, label = f"{servise}", marker='o')
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f$"))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%Y-%m"))
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.savefig(f'{id}-all.png', format='png')
        plt.clf()
        return f'{id}-all.png'

    def make_plot_name(self, id, data):
        fig = plt.figure(figsize=(9,9))
        ax = fig.subplots()
        plt.title(data[0]['Service'])
        plt.xlabel('Date')
        plt.ylabel('Quantity')
        x = np.array([np.datetime64(i['Date']) for i in data])
        y_summ = np.array([i['Summ'] for i in data])
        plt.plot(x, y_summ, label = "Summ", marker='o')
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f$"))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%Y-%m"))
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.savefig(f'{id}-by-name.png', format='png')
        plt.clf()
        return f'{id}-by-name.png'

    def make_plot_date(self, id, data):
        fig = plt.figure()
        ax = fig.add_subplot()
        summ_all = sum([i['Summ'] for i in data])
        plt.title(f"Servises summ = {summ_all:.2f}$")
        labels = [f"{i['Service']}\n{i['Summ']:.2f}$, {round((i['Summ'] / summ_all * 100), 2)}%" for i in data]
        vals = [i['Summ'] for i in data]
        ax.pie(vals, labels=labels)
        ax.grid()
        plt.savefig(f'{id}-by-date.png', format='png')
        plt.clf()
        return f'{id}-by-date.png'