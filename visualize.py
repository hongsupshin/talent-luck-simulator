import matplotlib
import numpy as np
import matplotlib.pyplot as plt
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
plt.style.use('ggplot')


def plot_C_over_t(Cs_t, results_t, s_title='', scale='log', fname='test'):

    """
    visualize an individual's capital changes over time
    :param Cs_t: array of capital values
    :param results_t: array of event history (1:lucky, -1:unlucky, 0:no event)
    :param s_title: plot title
    :param scale:
    :param fname: filename for saving
    :return:
    """

    plt.figure(figsize=(20, 8))

    # visualize capital changes over time
    plt.plot(Cs_t, ':', color='black')

    for event_ind, color in zip([1, -1], (colors[0], colors[3])):
        inds = np.argwhere(results_t == event_ind)
        plt.plot(inds, Cs_t[inds], '.', color=color, markersize=30)

    plt.title(s_title, fontsize=30)
    plt.xlabel('Time', fontsize=30)
    plt.ylabel('Capital', fontsize=30)
    plt.yscale(scale)
    plt.tick_params(labelsize='x-large')
    plt.legend(['Lucky', 'Unlucky'])
    plt.tight_layout()

    if fname:
        plt.savefig(fname + '.png')

    plt.show()
