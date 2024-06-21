
import numpy as np
import math
from scipy.special import factorial
import scipy.stats as stats



class Distributions:
    def exponential(betta, shift):
        # betta среднее время ожидания
        p = np.random.uniform(0, 1)
        return int(-math.log(1 - p) * (betta)) - shift
    
    def normal(mu, sigma):
        p = np.random.uniform(0, 1)
        return stats.norm.ppf(p, loc=mu, scale=sigma)
    
    def uniform(a, b):
        p = np.random.uniform(0, 1)
        return int(a + p*(b-a))
    
    def uniform_scipy(a, b):
        # равномерное распредление на промежутке
        p = np.random.uniform(0, 1)
        return int(stats.uniform.ppf(p, loc=a, scale=b-a))
    
    def gamma(alpha, beta):
        p = np.random.uniform(0, 1)
        return int(stats.gamma.ppf(p, a=alpha, scale=beta))
    
    f_map: dict[str, any] = {
        "exponetial": exponential,
        "normal": normal,
        "uniform": uniform,
        "gamma": gamma,
    }
        
p = np.random.uniform(0, 1)
# print(Distributions.exponential(p, 0.95))
# print(Distributions.exponential_scipy(p, 0.95))

# print(int(Distributions.uniform(0, 5, p)))
# print(int(Distributions.uniform_scipy(0, 5, p)))

print(Distributions.exponential(10, 5))


