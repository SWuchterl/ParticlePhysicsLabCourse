import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


def erfunc(x, a, b, c):
    return a / 2. * (erf((x - b) / (np.sqrt(2.) * c)) + 1.)


x_fit = np.linspace(1756, 2249, num=2249. - 1756.)
x_data = [1756., 1803., 1852., 1904., 1962., 2004.,
          2053., 2103., 2158., 2205., 2249.]
y_data4 = [59., 273., 783., 1392., 1736., 1875.,
           1942., 1927., 1845., 1899., 1979.]
y_data3 = [2203., 2178., 2148., 2229.,
           2197., 2203., 2178., 2121., 2028., 2061., 2143.]
noise = [206., 837., 2492., 9648., 23028., 30940.,
         36837., 42219., 48905., 66766., 95913.]
y_purity = [y_data4[i] / noise[i] for i in range(len(x_data))]
y_err_purity = [np.sqrt((np.sqrt(noise[i]) / noise[i])**2. +
                        (np.sqrt(y_data3[i]) / y_data3[i])**2.) * y_purity[i] for i in range(len(x_data))]
y_data = [y_data4[i] / y_data3[i] for i in range(len(x_data))]
y_err = [np.sqrt((np.sqrt(y_data4[i]) / y_data4[i])**2. +
                 (np.sqrt(y_data3[i]) / y_data3[i])**2.) * y_data[i] for i in range(len(x_data))]


interpolation = interp1d(x_data, y_purity, kind='cubic')

params, extras = curve_fit(
    erfunc, x_data, y_data,  p0=[1., 1850., 1.])

fig = plt.figure()
plt.plot(x_fit, erfunc(x_fit, *params), label='Errorfunction fit')
plt.errorbar(x_data, y_data, yerr=y_err, fmt='.',
             label='Efficiency data points')
plt.plot(x_data, interpolation(x_data), '--',
         label='Spline interpolation (purity)')
plt.errorbar(x_data, y_purity, yerr=y_err_purity,
             fmt='.', label='Purity data points')
plt.plot([params[1] + 2. * params[2]], [erfunc(params[1] + 2. *
                                               params[2], *params)], marker='*', markersize=10, color="red", label='Working point')
plt.legend()
plt.title('Efficiency and Purity')
plt.savefig('efficiency_fitPMT_1.pdf', format='pdf')
plt.show()

print "mean: ", params[1]
print "mean unc.: ", np.sqrt(extras[1, 1])
print "sigma: ", params[2]
print "sigma unc.: ", np.sqrt(extras[2, 2])
print "mean+2*sigma: ", params[1] + 2. * params[2]
print "mean+2*sigma unc.: ", np.sqrt(extras[1, 1] + 2 * extras[2, 2])
