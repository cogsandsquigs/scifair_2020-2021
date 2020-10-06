# Thanks to this GitHub project:
# https://github.com/henrifroese/infectious_disease_modelling
# for the basis of this code

from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# variables to tweak
N = 5000000 # amount of people
Infection_period = 14 # infection period
Incubation_period = 11 # incubation period
days_till_death = 14 # days untill someone dies from disease
starting_infected = 1 # how many people start infected
how_long = 600 # how many days for simulation to run
R_0 = 2.22 # R naught

gamma = 1.0 / Infection_period # infection period
delta = 1.0 / Incubation_period  # incubation period
beta = R_0 * gamma  # R_0 = beta / gamma, so beta = R_0 * gamma
alpha = 0.3  # death rate
rho = 1/days_till_death  # days from infection until death
#hello world
def deriv(y, t, N, beta, gamma, delta, alpha, rho):
    S, E, I, R, D = y
    dSdt = -beta * S * I / N
    dEdt = beta * S * I / N - delta * E
    dIdt = delta * E - (1 - alpha) * gamma * I - alpha * rho * I
    dRdt = (1 - alpha) * gamma * I
    dDdt = alpha * rho * I
    return dSdt, dEdt, dIdt, dRdt, dDdt

S0, E0, I0, R0, D0 = N - starting_infected, 0, starting_infected, 0, 0  # initial conditions: 
                                                                        # one infected, rest 
                                                                        # susceptible

t = np.linspace(0, how_long, 100) # Grid of time points (in days) 
                                  # NOTE: the last variable num is how granular it 
                                  # will be when you integrate the derivatives.

y0 = S0, E0, I0, R0, D0 # Initial conditions vector

# Integrate the SIR equations over the time grid, t.
ret = odeint(deriv, y0, t, args=(N, beta, gamma, delta, alpha, rho))
S, E, I, R, D = ret.T

print('Total amount of people killed: ' + str(round(D[-1])))

# Making the plot
f, ax = plt.subplots(1,1,figsize=(10,4))

# plots for the separate parameters
ax.plot(t, S, 'b', alpha=0.7, linewidth=2, label='Susceptible')
ax.plot(t, E, 'm', alpha=0.7, linewidth=2, label='Incubating')
ax.plot(t, I, 'r', alpha=0.7, linewidth=2, label='Infected')
ax.plot(t, R, 'g', alpha=0.7, linewidth=2, label='Recovered')
ax.plot(t, D, 'k', alpha=0.7, linewidth=2, label='Dead')

ax.set_title('Affect of a virus on a population of 5000000')

ax.set_xlabel('Time (days)')
ax.set_ylabel('Number of people')


ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)

ax.grid(which='major', linestyle='-')

legend = ax.legend()
legend.get_frame().set_alpha(0.5)

plt.show()