import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def erfunc(x, a, b, c):
    return a / 2. * (erf((x - b) / (np.sqrt(2.) * c)) + 1.)


x_fit = np.linspace(1750, 2289, num=539)
x_data = [1750., 1801., 1850., 1900., 1952., 2003.,
          2052., 2101., 2152., 2200., 2252., 2289.]
y_data4 = [5., 30., 166., 559., 1090., 1676.,
           1910., 1963., 2004., 2024., 2071., 2004.]
y_data3 = [2456., 2434., 2456., 2451.,
           2369., 2451., 2438., 2320., 2311., 2283., 2340., 2277.]
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
