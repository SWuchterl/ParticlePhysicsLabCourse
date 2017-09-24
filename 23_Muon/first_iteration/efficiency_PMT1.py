import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def erfunc(x, a, b, c):
    return a / 2. * (erf((x - b) / (np.sqrt(2.) * c)) + 1.)


x_fit = np.linspace(1750, 2289, num=539)
x_data = [1750., 1800., 1851., 1901., 1951., 2004.,
          2048., 2100., 2151., 2202., 2253., 2285.]
y_data4 = [61., 317., 896., 1434., 1760., 1943.,
           1993., 2040., 2024., 2145., 2037., 1978.]
y_data3 = [2342., 2255., 2399., 2319.,
           2295., 2305., 2282., 2260., 2220., 2359., 2201., 2147.]
y_data = [y_data4[i] / y_data3[i] for i in range(len(x_data))]
y_err = [np.sqrt((np.sqrt(y_data4[i]) / y_data4[i])**2. +
                 (np.sqrt(y_data3[i]) / y_data3[i])**2.) * y_data[i] for i in range(len(x_data))]

y_err = np.array(y_err)
print y_err


params, extras = curve_fit(
    erfunc, x_data, y_data,  p0=[1., 1850., 1.])

fig = plt.figure()
plt.plot(x_fit, erfunc(x_fit, *params))
plt.errorbar(x_data, y_data, yerr=y_err, fmt='.')
plt.axvline(params[1] + params[2], 0., 1.)
plt.axvline(params[1] + 2. * params[2], 0., 1.)
plt.title('Errorfunction fit')
plt.show()
plt.savefig('efficiency_fitPMT_2.pdf', format='pdf')

print "mean: ", params[1]
print "mean unc.: ", np.sqrt(extras[1, 1])
print "sigma: ", params[2]
print "sigma unc.: ", np.sqrt(extras[2, 2])
print "mean+2*sigma: ", params[1] + 2. * params[2]
print "mean+2*sigma unc.: ", np.sqrt(extras[1, 1] + 2 * extras[2, 2])
