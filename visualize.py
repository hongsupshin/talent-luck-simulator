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

    # visualize the events
    for event_ind, color in zip([1, -1], (colors[0], colors[3])):
        inds = np.argwhere(results_t == event_ind)
        plt.plot(inds, Cs_t[inds], '.', color=color, markersize=30)

    plt.title(s_title, fontsize=30)
    plt.xlabel('Time', fontsize=30)
    plt.ylabel('Capital', fontsize=30)
    plt.yscale(scale)
    plt.tick_params(labelsize='x-large')
    plt.legend(['Lucky event', 'Unlucky event'], fontsize=20)
    
    # visualize capital changes over time
    plt.plot(Cs_t, ':', color='black', label='')
    
    plt.tight_layout()

    if fname:
        plt.savefig(fname + '.png')

    plt.show()

    
def scatter_talent_capital_P_events(P_events, 
                                    Cs_dict, 
                                    Ts_dict, 
                                    ylim=[10e-11, 10e11], 
                                    scale='log',
                                    figsize=(20,7),
                                    fname='test'):

    """
    scatter-plot talent-capital relationship for various P_event values
    :param Cs_dict: Final capital values for all individuals for various P_events (key: P_event)
    :param Ts_dict: Talent values for all individuals for various P_events (key: P_event)
    :param ylim: ylim of the plot
    :param scale: scale
    :param figsize: figure size
    :param fname: filename for saving
    :return:
    """
    
    fig, axes = plt.subplots(1, len(P_events), sharey=True, figsize=figsize)
    for i, (P_event, ax) in enumerate(zip(P_events, axes)):
        
        Cs = Cs_dict[P_event]
        Ts = Ts_dict[P_event]

        ax.plot(Ts, Cs, '.', alpha=0.5, markersize=5)
        ax.set_xlim(0.2, 1)
        ax.set_ylim(ylim)
        ax.set_xticks([0.2, 0.6, 1])
        ax.set_yscale(scale)
        if i == 0:
            ax.set_title('$P_{event}=$'+str(P_event), fontsize=30)
        else:
            ax.set_title(str(P_event), fontsize=30)
        if i == 0:
            ax.set_ylabel('Capital', fontsize=30)
        if i == 2:
            ax.set_xlabel('Talent', fontsize=30)
        ax.tick_params(labelsize='x-large')

    plt.tight_layout()
    if fname:
        plt.savefig(fname + '.png')
    plt.show()
    
    
def scatter_talent_capital_P_events_comparison(P_events, 
                                               data_groupA, 
                                               data_groupB,
                                               labels,
                                               ylim=[10e-11, 10e11], 
                                               scale='log',
                                               figsize=(20,7),
                                               fname='test'):

    """
    scatter-plot talent-capital relationship for various P_event values for two different scenarios
    :param data_groupA: {'C':Cs_dict, 'T':Ts_dict} pair for group A (see scatter_talent_capital_P_events)
    :param data_groupB: {'C':Cs_dict, 'T':Ts_dict} pair for group B
    :param labels: {'A': label for A, 'B': label for B} for legend
    :param ylim: ylim of the plot
    :param scale: scale
    :param figsize: figure size
    :param fname: filename for saving
    :return:
    """

    fig, axes = plt.subplots(1, len(P_events), sharey=True, figsize=figsize)
    for i, (P_event, ax) in enumerate(zip(P_events, axes)):
        
        Cs_A, Ts_A = data_groupA['C'][P_event], data_groupA['T'][P_event]
        Cs_B, Ts_B = data_groupB['C'][P_event], data_groupB['T'][P_event]

        ax.plot(Ts_A, Cs_A, '.', alpha=0.5, markersize=5, label=labels['A'])
        ax.plot(Ts_B, Cs_B, '.', alpha=0.5, markersize=5, label=labels['B'])
        ax.set_xlim(0.2, 1)
        ax.set_ylim(ylim)
        ax.set_xticks([0.2, 0.6, 1])
        ax.set_yscale(scale)
        if i == 0:
            ax.set_title('$P_{event}=$'+str(P_event), fontsize=30)
        else:
            ax.set_title(str(P_event), fontsize=30)
        if i == 0:
            ax.set_ylabel('Capital', fontsize=30)
            lgnd = ax.legend(fontsize=25, loc='lower left')
            lgnd.legendHandles[0]._legmarker.set_markersize(20)
            lgnd.legendHandles[1]._legmarker.set_markersize(20)
        if i == 2:
            ax.set_xlabel('Talent', fontsize=30)
        ax.tick_params(labelsize='x-large')

    plt.tight_layout()
    if fname:
        plt.savefig(fname + '.png')
    plt.show()
