import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


def erfunc(x, a, b, c):
    return a / 2. * (erf((x - b) / (np.sqrt(2.) * c)) + 1.)


x_fit = np.linspace(1749, 2256, num=2256. - 1749.)
x_data = [1749., 1802., 1850., 1905., 1955., 2000.,
          2054., 2100., 2148., 2200., 2256.]
y_data4 = [7., 43., 197., 638., 1189., 1555.,
           1821., 1802., 1918., 1851., 1909.]
y_data3 = [2274., 2280., 2260., 2329.,
           2298., 2236., 2263., 2145., 2163., 2092., 2146.]
noise = [15., 198., 820., 2419., 7180., 20692.,
         42398., 61143., 78582., 98810., 124525.]
y_purity = [y_data4[i] / noise[i] for i in range(len(x_data))]
y_err_purity = [np.sqrt((np.sqrt(noise[i]) / noise[i])**2. +
                        (np.sqrt(y_data3[i]) / y_data3[i])**2.) * y_purity[i] for i in range(len(x_data))]
y_data = [y_data4[i] / y_data3[i] for i in range(len(x_data))]
y_err = [np.sqrt((np.sqrt(y_data4[i]) / y_data4[i])**2. +
                 (np.sqrt(y_data3[i]) / y_data3[i])**2.) * y_data[i] for i in range(len(x_data))]


interpolation = interp1d(x_data, y_purity, kind='cubic')

params, extras = curve_fit(
    erfunc, x_data, y_data, sigma=y_err, p0=[1., 1850., 1.])

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
plt.savefig('efficiency_fitPMT_2_fourth.pdf', format='pdf')

print "mean: ", params[1]
print "mean unc.: ", np.sqrt(extras[1, 1])
print "sigma: ", params[2]
print "sigma unc.: ", np.sqrt(extras[2, 2])
print "mean+2*sigma: ", params[1] + 2. * params[2]
print "mean+2*sigma unc.: ", np.sqrt(extras[1, 1] + 2 * extras[2, 2])
print "purity: ", interpolation(params[1] + 2. * params[2])

with open('PMT2_fourth.txt', 'wb') as f:
    f.write('mean: ' + str(params[1]) + '\n')
    f.write('mean unc.: ' + str(np.sqrt(extras[1, 1])) + '\n')
    f.write('sigma: ' + str(params[2]) + '\n')
    f.write('sigma unc.: ' + str(np.sqrt(extras[2, 2])) + '\n')
    f.write('mean+2*sigma: ' + str(params[1] + 2. * params[2]) + '\n')
    f.write('mean+2*sigma unc.: ' +
            str(np.sqrt(extras[1, 1] + 2 * extras[2, 2])) + '\n')
    f.write('purity: ' + str(interpolation(params[1] + 2. * params[2])))
    f.close()
