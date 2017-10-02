import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


def erfunc(x, a, b, c):
    return a / 2. * (erf((x - b) / (np.sqrt(2.) * c)) + 1.)


x_fit = np.linspace(1749, 2248, num=2248. - 1749.)
x_data = [1749., 1807., 1852., 1898., 1951.,
          2009., 2047., 2096., 2146., 2199., 2248.]
y_data4 = [14., 68., 225., 555., 1056.,
           1508., 1656., 1803., 1919., 1907., 1960.]
y_data3 = [2413., 2407., 2422., 2362.,
           2386., 2412., 2275., 2433., 2342., 2389., 2310.]
noise = [71., 237., 688., 4866., 34017., 92231.,
         142371., 184274., 216195., 250940., 299885.]
y_purity = [y_data4[i] / noise[i] for i in range(len(x_data))]
y_err_purity = [np.sqrt((np.sqrt(noise[i]) / noise[i])**2. +
                        (np.sqrt(y_data3[i]) / y_data3[i])**2.) * y_purity[i] for i in range(len(x_data))]
y_data = [y_data4[i] / y_data3[i] for i in range(len(x_data))]
y_err = [np.sqrt((np.sqrt(y_data4[i]) / y_data4[i])**2. +
                 (np.sqrt(y_data3[i]) / y_data3[i])**2.) * y_data[i] for i in range(len(x_data))]


interpolation = interp1d(x_data, y_purity, kind='cubic')

params, extras = curve_fit(
    erfunc, x_data, y_data, sigma=y_err, p0=[1., 1850., 10.])

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
plt.savefig('efficiency_fitPMT_3_third.pdf', format='pdf')

print "mean: ", params[1]
print "mean unc.: ", np.sqrt(extras[1, 1])
print "sigma: ", params[2]
print "sigma unc.: ", np.sqrt(extras[2, 2])
print "mean+2*sigma: ", params[1] + 2. * params[2]
print "mean+2*sigma unc.: ", np.sqrt(extras[1, 1] + 2 * extras[2, 2])
print "purity: ", interpolation(params[1] + 2. * params[2])

with open('PMT3_third.txt', 'wb') as f:
    f.write('mean: ' + str(params[1]) + '\n')
    f.write('mean unc.: ' + str(np.sqrt(extras[1, 1])) + '\n')
    f.write('sigma: ' + str(params[2]) + '\n')
    f.write('sigma unc.: ' + str(np.sqrt(extras[2, 2])) + '\n')
    f.write('mean+2*sigma: ' + str(params[1] + 2. * params[2]) + '\n')
    f.write('mean+2*sigma unc.: ' +
            str(np.sqrt(extras[1, 1] + 2 * extras[2, 2])) + '\n')
    f.write('purity: ' + str(interpolation(params[1] + 2. * params[2])))
    f.close()
