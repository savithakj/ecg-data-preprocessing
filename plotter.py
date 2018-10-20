from matplotlib import pyplot as plt
from matplotlib.figure import Figure


def plotter(data):
    plt = Figure(figsize=(5, 4), dpi=100)
    lower_limit = 0
    upper_limit = 100
    figure_count = 1

    for _ in range(12):
        temp = []
        for index in range(lower_limit, upper_limit):
            temp.append(float(data[index]))
        a = plt.add_subplot(4, 3, figure_count)
        a.plot(temp)
        lower_limit = upper_limit
        upper_limit = upper_limit + 100
        figure_count = figure_count + 1
    return plt, a
