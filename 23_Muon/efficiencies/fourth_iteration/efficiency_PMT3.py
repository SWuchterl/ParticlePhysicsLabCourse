import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


def erfunc(x, a, b, c):
    return a / 2. * (erf((x - b) / (np.sqrt(2.) * c)) + 1.)


x_fit = np.linspace(1747, 2250, num=2250. - 1747.)
x_data = [1747., 1803., 1849., 1903., 1951.,
          2001., 2048., 2105., 2149., 2201., 2250.]
y_data4 = [15., 61., 193., 573., 1116.,
           1410., 1777., 1830., 1945., 1917., 2033.]
y_data3 = [2420., 2473., 2433., 2236,
           2411., 2316., 2398., 2312., 2376., 2284., 2374.]
noise = [48., 228., 680., 4674., 33864., 93626.,
         143209., 183382., 210260., 242282., 302262.]
y_purity = [y_data4[i] / noise[i] for i in range(len(x_data))]
y_err_purity = [np.sqrt((np.sqrt(noise[i]) / noise[i])**2. +
                        (np.sqrt(y_data3[i]) / y_data3[i])**2.) * y_purity[i] for i in range(len(x_data))]
y_data = [y_data4[i] / y_data3[i] for i in range(len(x_data))]
y_err = [np.sqrt((np.sqrt(y_data4[i]) / y_data4[i])**2. +
                 (np.sqrt(y_data3[i]) / y_data3[i])**2.) * y_data[i] for i in range(len(x_data))]


interpolation = interp1d(x_data, y_purity, kind='cubic')

params, extras = curve_fit(
    erfunc, x_data, y_data, sigma=y_err, p0=[1., 1850., 10.])

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
plt.savefig('efficiency_fitPMT_3_fourth.pdf', format='pdf')

print "mean: ", params[1]
print "mean unc.: ", np.sqrt(extras[1, 1])
print "sigma: ", params[2]
print "sigma unc.: ", np.sqrt(extras[2, 2])
print "mean+2*sigma: ", params[1] + 2. * params[2]
print "mean+2*sigma unc.: ", np.sqrt(extras[1, 1] + 2 * extras[2, 2])
print "purity: ", interpolation(params[1] + 2. * params[2])

with open('PMT3_fourth.txt', 'wb') as f:
    f.write('mean: ' + str(params[1]) + '\n')
    f.write('mean unc.: ' + str(np.sqrt(extras[1, 1])) + '\n')
    f.write('sigma: ' + str(params[2]) + '\n')
    f.write('sigma unc.: ' + str(np.sqrt(extras[2, 2])) + '\n')
    f.write('mean+2*sigma: ' + str(params[1] + 2. * params[2]) + '\n')
    f.write('mean+2*sigma unc.: ' +
            str(np.sqrt(extras[1, 1] + 2 * extras[2, 2])) + '\n')
    f.write('purity: ' + str(interpolation(params[1] + 2. * params[2])))
    f.close()