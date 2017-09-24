import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def erfunc(x, a, b, c):
    return a / 2. * (erf((x - b) / (np.sqrt(2.) * c)) + 1.)


x_fit = np.linspace(1778, 2254, num=476)
x_data = [1778., 1808., 1848., 1900., 1951.,
          2001., 2054., 2102., 2155., 2203., 2254.]
y_data4 = [29., 46., 185., 464., 929.,
           1340., 1529., 1580., 1680., 1727., 1857.]
y_data3 = [2129., 2096., 2174., 2073.,
           2127., 2134., 2128., 2072., 2081., 2085., 2162.]
y_data = [y_data4[i] / y_data3[i] for i in range(len(x_data))]
y_err = [np.sqrt((np.sqrt(y_data4[i]) / y_data4[i])**2. +
                 (np.sqrt(y_data3[i]) / y_data3[i])**2.) * y_data[i] for i in range(len(x_data))]

params, extras = curve_fit(
    erfunc, x_data, y_data, p0=[1., 1850., 10.])

fig = plt.figure()
plt.plot(x_fit, erfunc(x_fit, *params))
plt.errorbar(x_data, y_data, yerr=y_err, fmt='.')
plt.axvline(params[1] + params[2], 0., 1.)
plt.axvline(params[1] + 2. * params[2], 0., 1.)
plt.title('Errorfunction fit')
plt.show()
plt.savefig('efficiency_fitPMT_3.pdf', format='pdf')

print "mean: ", params[1]
print "mean unc.: ", np.sqrt(extras[1, 1])
print "sigma: ", params[2]
print "sigma unc.: ", np.sqrt(extras[2, 2])
print "mean+2*sigma: ", params[1] + 2. * params[2]
print "mean+2*sigma unc.: ", np.sqrt(extras[1, 1] + 2 * extras[2, 2])
