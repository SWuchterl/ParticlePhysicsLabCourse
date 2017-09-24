import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def erfunc(x, a, b, c):
    return a / 2. * (erf((x - b) / (np.sqrt(2.) * c)) + 1.)


x_fit = np.linspace(1743, 2271, num=2271. - 1743.)
x_data = [1743., 1800., 1850., 1901., 1950.,
          2000., 2055., 2101., 2154., 2206., 2271.]
y_data4 = [15., 44., 109., 565., 1070.,
           1410., 1728., 1780., 1884., 1903., 2024.]
y_data3 = [2440., 2384., 2331., 2413.,
           2378., 2285., 2332., 2308., 2333., 2295., 2366.]
y_data = [y_data4[i] / y_data3[i] for i in range(len(x_data))]
y_err = [np.sqrt((np.sqrt(y_data4[i]) / y_data4[i])**2. +
                 (np.sqrt(y_data3[i]) / y_data3[i])**2.) * y_data[i] for i in range(len(x_data))]

params, extras = curve_fit(
    erfunc, x_data, y_data, p0=[1., 1850., 5.])

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
