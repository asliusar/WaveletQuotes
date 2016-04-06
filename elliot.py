import numpy as np
import matplotlib.pyplot as plt

def showPlot(date, data, file_name):
    fig, ax = plt.subplots()
    ax.plot(date, data)
    fig.savefig(file_name)
    plt.close(fig)

x = [1, 3, 2, 4]
z = [1, 3, 2, 4, 3, 5]
template = x
trend = 1 / 3 * np.arange(len(template))
template = template + trend
showPlot(np.arange(len(template)), template, 'test.jpg')