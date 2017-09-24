import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def erfunc(x, a, b, c):
    return a / 2. * (erf((x - b) / (np.sqrt(2.) * c)) + 1.)


x_fit = np.linspace(1780, 2251, num=2251. - 1780.)
x_data = [1780., 1808., 1854., 1906., 1952., 2001.,
          2051., 2103., 2158., 2201., 2251.]
y_data4 = [14., 33., 181., 531., 1039., 1508.,
           1609., 1926., 1834., 1880., 1933.]
y_data3 = [2259., 2249., 2204., 2166.,
           2249., 2205., 2128., 2263., 2164., 2101., 2172.]
y_data = [y_data4[i] / y_data3[i] for i in range(len(x_data))]
y_err = [np.sqrt((np.sqrt(y_data4[i]) / y_data4[i])**2. +
                 (np.sqrt(y_data3[i]) / y_data3[i])**2.) * y_data[i] for i in range(len(x_data))]

y_err = np.array(y_err)
print y_err


params, extras = curve_fit(
    erfunc, x_data, y_data,  p0=[1., 1850., 10.])

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
