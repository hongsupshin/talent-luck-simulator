# talent-luck-simulator

This is a repository for code and analysis to simulate the results from my Medium blog post [**Talent, luck and success: simulating meritocracy and inequality with stochasticity**](https://medium.com/@hongsupshin/talent-luck-and-success-simulating-meritocracy-and-inequality-with-stochasticity-501e0c1b4969).

The blog post and the main notebook contains a summary and replication of the results from the paper, [Talent vs Luck: the role of randomness in success and failure](https://arxiv.org/abs/1802.07068) (Pluchino et al. 2018), and simulations of various socioeconomical scenarios based on the model with certain modifications.

Those scenarios described in the blog post are:
## Scenario 1. Balanced unlucky events
In the original paper, unlucky events always punished individuals regardless of their talent. Here, individuals with higher talent have higher likelihood of not being affected by bad luck.

## Scenario 2. Talent directly affects the return of luck
Talent directly affects how much individuals may profit or lose from the lucky or unlucky events, respectively.

## Scenario 3. Paycheck (“Hard work pays off”)
Individuals have fixed income added to their asset (capital) regularly regardless of the luck-related events.

## Scenario 4. Interest rate
At every time step (every 6 months), the capital increases based on an interest rate.

## Scenario 5. "The rich get luckier, the poor get unluckier"
The rich is more likely to get away with unlucky events but the poor is likely to face unlucky events more often.

## Scenario 6. Income tax
Individuals pay income-based tax at every time period.

## Scenario 7. Social safety net
One’s capital cannot go lower than the starting amount.
