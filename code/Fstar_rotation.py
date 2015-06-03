import numpy as np
import matplotlib.pyplot as plt
from plotstuff import params
reb = params()

plotpar = {'axes.labelsize': 18,
           'text.fontsize': 18,
           'legend.fontsize': 18,
           'xtick.labelsize': 18,
           'ytick.labelsize': 18,
           'text.usetex': True}
plt.rcParams.update(plotpar)

# load data
koi, kid, teff, logg, Rpl, Porb, Prot, Prot_err, Rvar, flag = \
        np.genfromtxt("../data/KOIrotation_periods.txt", skip_header=20,
                      delimiter=",").T

m = (teff > 6250) * np.isfinite(Prot)
print kid[m]
print len(kid[m])
for i, k in enumerate(kid[m]):
    print "%s %s %s %s %s" % (str(int(koi[m][i])).zfill(4),
                              str(int(k)).zfill(9), teff[m][i],
                              str(Prot[m][i]).zfill(6), Prot_err[m][i])

plt.clf()
plt.errorbar(teff, Prot, yerr=Prot_err, fmt="k.", capsize=0, ecolor=".7")
plt.xlim(7100, min(teff))
plt.xlabel("$\mathrm{T}_{\mathrm{eff}}\mathrm{~(K)}$")
plt.ylabel("$\mathrm{P}_{\mathrm{rot}}\mathrm{~(days)}$")
plt.savefig("koi_rotation")
