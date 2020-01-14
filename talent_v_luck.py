import numpy as np
import scipy as sp


def neutral(interest_rate, w_T, Ts, Cs_prev):

    """
    compute capital for t+1 when no event happens
    :param interest_rate:
    :param w_T: linear coefficient defining salary amount
    :param Ts: talent of individuals
    :param Cs_prev: capital at time step, t
    :return: capital at time step, t+1
    """
    Cs_next = Cs_prev*(1+interest_rate) + w_T*Ts
    return Cs_next


def lucky(interest_rate, Ts, Cs_prev, use_default=False):

    """
    compute the consequence of a lucky event
    :param interest_rate:
    :param Ts: talent of individuals
    :param Cs_prev: capital at time step, t
    :param use_default: whether to use the default (fixed linear coefficient for capital)
    :return:
    """
    if use_default:
        Cs_next = 2*Cs_prev*(1+interest_rate)
    else:
        Cs_next = (1+Ts)*Cs_prev*(1+interest_rate)
    return Cs_next


def unlucky(interest_rate, Ts, Cs_prev, use_default=False):

    """
    compute the consequence of an unlucky event
    :param interest_rate:
    :param Ts: talent of individuals
    :param Cs_prev: capital at time step, t
    :param use_default: whether to use the default (fixed linear coefficient for capital)
    :return:
    """

    if use_default:
        Cs_next = 0.5*Cs_prev*(1+interest_rate)
    else:
        Cs_next = Ts*Cs_prev*(1+interest_rate)
    return Cs_next


def run_sim_all(P_event=1/20, P_lucky0=0.5, use_default=False,
                w_Talent=1, interest_rate=0,
                min_tax_rate=0.1, max_tax_rate=0.4,
                N_timestamps=80, mu_T=0.6, std_T=0.1, N=1000,
                turn_on_rich=False, turn_on_tax=False, turn_on_safenet=False,
                T_dist='normal', C_even=True, mu_C=10, std_C=2):

    """
    Simulating talent and luck relationship in various socioeconomic scenarios
    :param P_event: probability of an event happen at a time step
    :param P_lucky0: probability of the event being lucky (initial probability)
    :param use_default: whether to use a fixed linear coeff. for capital
    :param w_Talent:
    :param interest_rate:
    :param min_tax_rate:
    :param max_tax_rate:
    :param N_timestamps:
    :param mu_T:
    :param std_T:
    :param N:
    :param turn_on_rich:
    :param turn_on_tax:
    :param turn_on_safenet:
    :param T_dist:
    :param C_even:
    :param mu_C:
    :param std_C:
    :return:
    """

    # talent distribution
    if T_dist == 'normal':
        Ts = np.clip(np.random.normal(mu_T, std_T, N), 0, 1)
    elif T_dist == 'uniform':
        Ts = np.random.random(N)

    # capital distribution
    if C_even:
        # everyone has the same starting point
        C0s = np.ones(N) * mu_C
    else:
        # normally distributed capital
        C0s = np.random.normal(mu_C, std_C, N)

    # generating events for all time steps and every individual
    events_all = np.random.binomial(1, P_event, (N_timestamps, len(Ts)))

    # assumption: everyone has the same amount of luck (at the beginning)
    P_lucky0 = np.ones(N) * P_lucky0

    # initializing
    Cs_prev = C0s
    P_lucky = P_lucky0
    Cs_all = [Cs_prev]
    results_all = []

    # loop over events (time steps)
    for event_all in events_all:

        # compute lucky/unlucky events at once for all INDIVIDUALS
        # no event=0, lucky event (good_luck)=1, unlucky event(bad_luck)=-1
        rands = np.random.random(N)
        good_luck = (rands < P_lucky) * event_all
        bad_luck = -1 * (rands >= P_lucky) * event_all
        results = good_luck + bad_luck

        # apply events
        # Scenario 1. `lucky` and `unlucky` functions are already balanced when use_default=True
        # Scenario 2. Otherwise, talent affects the return of luck
        # Scenario 3. `neutral` function adds salary to capital when no events occur
        # Scenario 4. Interest rate is implemented in all the functions
        Cs_next = (results == 0) * neutral(interest_rate, w_Talent, Ts, Cs_prev) \
                  + (results > 0) * lucky(interest_rate, Ts, Cs_prev, use_default) \
                  + (results < 0) * unlucky(interest_rate, Ts, Cs_prev, use_default)

        # Scenario 5. the rich get luckier, the poor get unluckier
        if turn_on_rich:
            P_lucky = sp.norm.cdf(sp.mstats.zscore(Cs_next))

        # Scenario 6. Income tax
        if turn_on_tax:
            # tax rate is calculated relatively depending on the income
            # :recalibrate luck based on capital distribution
            tax_rates = sp.norm.cdf(sp.mstats.zscore(Cs_next)) * (
                        max_tax_rate - min_tax_rate) + min_tax_rate
            Cs_next = Cs_next * (1 - tax_rates)

        # Scenario 7. Social safety net (capital can't go below C0s)
        if turn_on_safenet:
            Cs_next = np.max([Cs_next, C0s], axis=0)

        # update
        Cs_prev = Cs_next
        Cs_all.append(Cs_next)
        results_all.append(results)

    results_all.append(np.zeros(N))

    return Cs_next, Ts, np.array(Cs_all), np.array(results_all)
