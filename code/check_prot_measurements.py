import numpy as np
import matplotlib.pyplot as plt
import subprocess
import kplr
client = kplr.API()
import pyfits
import glob
from plotstuff import params
reb = params()
from Kepler_ACF import corr_run
from astropy import constants as const

def load_data(kid):
    lcdir = "/Users/angusr/.kplr/data/lightcurves/%s" % kid.zfill(9)
    fnames = glob.glob("%s/*.fits" % lcdir)
    if len(fnames) == 0:  # download the light curves if you don't already havm
        print "downloading light curve"
        star = client.star("%s" % str(int(k)))
        star.get_light_curves(fetch=True, shortcadence=False)
    x, y, yerr = [], [], []
    for fname in fnames[:5]:
        hdulist = pyfits.open(fname)
        tbdata = hdulist[1].data
        time = tbdata["TIME"]
        flux = tbdata["PDCSAP_FLUX"]
        flux_err = tbdata["PDCSAP_FLUX_ERR"]
        q = tbdata["SAP_QUALITY"]
        m = np.isfinite(time) * np.isfinite(flux) * \
                np.isfinite(flux_err) * (q == 0)
        x.extend(time[m])
        yerr.extend(flux_err[m]/np.median(flux[m]))
        y.extend(flux[m]/np.median(flux[m]) - 1)
    return np.array(x), np.array(y), np.array(yerr)

def vsini2i(vsini, radius, prot):

    # units
    vsini_ms = vsini * 1000
    radius_m = radius * 6.955e8
    prot_secs = prot * 24 * 3600
    v = radius_m*2*np.pi / prot_secs
    sini = vsini / v
    i = np.arcsin(sini)
    print "i = ", i/2/np.pi * 360, "degrees"
    return i/2/np.pi * 360

if __name__ == "__main__":

    kid, koi, teff, p, rpl, porb = np.genfromtxt("../data/results.txt",
                                                 skip_header=2).T

    inclinations = []
    for i, k in enumerate(kid):
        print str(int(k))

        radius, r_err, vsini, vsini_err = \
                np.genfromtxt("../data/%s_cfop.txt" % str(int(k)),
                              skip_header=4, usecols=(6, 8, 9, 11)).T
        m = np.isfinite(radius)
        r, rerr = radius[m][0], r_err[m][0]
        m = np.isfinite(vsini)
        if len(vsini[m]):
            v, verr = vsini[m][0], vsini_err[m][0]
        else: v, verr = np.nan, np.nan

        x, y, yerr = load_data(str(int(k)))
        x -= x[0]

        result1 = np.genfromtxt("../ACFresults/%s_allq_result.txt" % str(int(k)))
        result2 = np.genfromtxt("../ACFresults/%s_result.txt" % str(int(k)))

        print result1, result2, p[i]
        print len(x)

        nplots, n = 10, 4 * p[i]
        for i in range(nplots):
            plt.clf()
            m = (x > n * i) * (x < n * (i + 1))
            plt.plot(x[m], y[m], "k.")
            plt.show()
        raw_input("e")

#         plt.savefig("%s_lc" % str(int(k)))

#         savedir = "/Users/angusr/Python/HotStarsInc/ACFresults"
#         corr_run(x, y, yerr, int(k), savedir)

        inclinations.append(vsini2i(v, r, p[i]))

    print inclinations
    plt.clf()
    plt.plot(teff, inclinations, "k.")
    plt.savefig("inclination_vs_teff")
