import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
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
noise = [177., 873., 2676., 9238., 21354., 31362.,
         36802., 43514., 49794., 67795., 101920., 132768.]
y_purity = [y_data4[i] / noise[i] for i in range(len(x_data))]
y_err_purity = [np.sqrt((np.sqrt(noise[i]) / noise[i])**2. +
                        (np.sqrt(y_data3[i]) / y_data3[i])**2.) * y_purity[i] for i in range(len(x_data))]
y_data = [y_data4[i] / y_data3[i] for i in range(len(x_data))]
y_err = [np.sqrt((np.sqrt(y_data4[i]) / y_data4[i])**2. +
                 (np.sqrt(y_data3[i]) / y_data3[i])**2.) * y_data[i] for i in range(len(x_data))]


interpolation = interp1d(x_data, y_purity, kind='cubic')

params, extras = curve_fit(
    erfunc, x_data, y_data, sigma=y_err,  p0=[1., 1850., 1.])

fig, ax1 = plt.subplots()
ax1.plot(x_fit, erfunc(x_fit, *params), label='Errorfunction fit')
ax1.errorbar(x_data, y_data, yerr=y_err, fmt='.',
             label='Efficiency data points')
ax2 = ax1.twinx()
ax2.plot(x_data, interpolation(x_data), '--',
         label='Spline interpolation (purity)', color='green')
ax2.errorbar(x_data, y_purity, yerr=y_err_purity,
             fmt='.', label='Purity data points', color='r')
ax1.plot([params[1] + 2. * params[2]], [erfunc(params[1] + 2. *
                                               params[2], *params)], marker='*', markersize=10, color="red", label='Working point')

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=7)

ax1.set_xlabel('Voltage [V]')
ax1.set_ylabel('Efficiency')
ax2.set_ylabel('Purity')
plt.title('Efficiency and Purity')
fig.tight_layout()
plt.savefig('efficiency_fitPMT_1_first.pdf', format='pdf')

print "mean: ", params[1]
print "mean unc.: ", np.sqrt(extras[1, 1])
print "sigma: ", params[2]
print "sigma unc.: ", np.sqrt(extras[2, 2])
print "mean+2*sigma: ", params[1] + 2. * params[2]
print "mean+2*sigma unc.: ", np.sqrt(extras[1, 1] + 2 * extras[2, 2])
print "purity: ", interpolation(params[1] + 2. * params[2])

with open('PMT1_first.txt', 'wb') as f:
    f.write('mean: ' + str(params[1]) + '\n')
    f.write('mean unc.: ' + str(np.sqrt(extras[1, 1])) + '\n')
    f.write('sigma: ' + str(params[2]) + '\n')
    f.write('sigma unc.: ' + str(np.sqrt(extras[2, 2])) + '\n')
    f.write('mean+2*sigma: ' + str(params[1] + 2. * params[2]) + '\n')
    f.write('mean+2*sigma unc.: ' +
            str(np.sqrt(extras[1, 1] + 2 * extras[2, 2])) + '\n')
    f.write('purity: ' + str(interpolation(params[1] + 2. * params[2])))
    f.close()
