import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy import stats
import matplotlib.pyplot as plt

data = np.loadtxt('dienstag.TKA', skiprows=2)
channel = np.linspace(0., len(data), len(data))

bin_means, bin_edges, binnumber = stats.binned_statistic(
    channel, data, statistic='sum', bins=50)

plt.hlines(bin_means, bin_edges[:-1], bin_edges[1:], color='green')
plt.grid()
plt.title('Muon decay')
plt.ylabel('Events/Bin')
plt.xlabel('Channel')
plt.yscale('log')
plt.savefig('lifetime.pdf', format='pdf')
plt.show()
