
from math import log, sqrt, exp, pi
from scipy.stats import norm
import numpy as np
S = 100
r = 0.05
q = 0.02
sigma = 0.5
T = 0.4
K1 = 90
K2 = 98
K3 = 102
K4 = 110

'''
Option price when K4 is 110: 1.1717
Option price when K4 is 104: 0.9013
'''

def d(K, is_d1=True):
    term1 = log(S/K) + (r - q + (sigma**2)/2)*T
    term2 = log(S/K) + (r - q - (sigma**2)/2)*T
    if is_d1:
        return term2 / (sigma*sqrt(T))
    else:
        return term1 / (sigma*sqrt(T))
    
# Distribution
def N(x):
    return norm.cdf(x)
def black_scholes_custom(K4=110):

    price = (
        S*exp(-q*T)*(N(-d(K2, False))-N(-d(K1, False)))
        -K1*exp(-r*T)*(N(-d(K2, True))-N(-d(K1, True)))
        +exp(-r*T)*(K2-K1)*(N(-d(K3, True))-N(-d(K2, True)))
        -S*exp(-q*T)*((K2-K1)/(K4-K3))*(N(-d(K4, False))-N(-d(K3, False)))
        +(((K2-K1)/(K4-K3))*K3 + K2 - K1)*exp(-r*T)*(N(-d(K4, True))-N(-d(K3, True)))
    )
    return np.round(price, 4)

def main():
    print("Option price when K4 is 110:", black_scholes_custom())
    print("Option price when K4 is 104:", black_scholes_custom(K4 = 104))
    


def d(sigma, S, K, r, t):
    d1 = 1 / (sigma * sqrt(t)) * ( log(S/K) + (r + sigma**2/2) * t)
    d2 = d1 - sigma * sqrt(t)
    return d1, d2


def call_price(sigma, S, K, r, t, d1, d2):
    C = norm.cdf(d1) * S - norm.cdf(d2) * K * exp( -r*t)
    return C

import numpy as np
import matplotlib.pyplot as plt
# option parameters
S = 100.0
K = 90.0
t = 30.0/365.0
r = 0.01
c0 = 10.50

sigma = np.linspace(0, 1)
d1, d2 = d(sigma, S=S, K=K, r=r, t=t)
C = call_price(sigma, S, K, r, t, d1, d2)
print(d1, d2)
print("Call price: ", C)
plt.plot(sigma, C - c0)
plt.show()


# tolerances 
tol = 1e-3
print(tol)
epsilon = 1
count = 0
max_iter = 1000
C0 = 2.3
# initial guess
vol = 0.50

while epsilon > tol:
    count += 1
    print(count)
    if count >= max_iter:
        print("Break")
        break
    
    orig_vol = vol
    d1, d2 = d(sigma=vol, S=S, K=K, r=r, t=t)
    function_value = call_price(vol, S, K, r, t, d1, d2) - C0

    vega = S * norm.pdf(d1) * sqrt(t)
    vol = -function_value / vega + vol

    epsilon = abs((vol - orig_vol) / orig_vol)



print("Sigma: ", vol)
print("Code took ", count, " iterations.")
