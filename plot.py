import matplotlib.pyplot as plt


def plot_sol(points, vals, title):
    fig, ax = plt.subplots()
    edges = [key for key, value in vals.items() if value > 0.7]
    x_chords = [point[0] for point in points]
    y_chords = [point[1] for point in points]
    ax.plot(x_chords, y_chords, '.')
    for edge in edges:
        x1, y1 = points[edge[0]]
        x2, y2 = points[edge[1]]

        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.8",
                                    color="skyblue",
                                    linewidth=2))
    ax.set_title(title)
    plt.show()


def plot_sol_with_subtour(points, vals, tour):
    fig, ax = plt.subplots()
    edges = [key for key, value in vals.items() if value > 0.7]
    x_chords = [point[0] for point in points]
    y_chords = [point[1] for point in points]
    ax.plot(x_chords, y_chords, '.')
    colors = {edge: ("yellowgreen" if edge[0] in tour else "skyblue") for edge in edges}
    for edge in edges:
        x1, y1 = points[edge[0]]
        x2, y2 = points[edge[1]]

        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.8",
                                    color=colors[edge],
                                    linewidth=2))
    ax.set_title("Eliminated subtour")
    plt.show()
