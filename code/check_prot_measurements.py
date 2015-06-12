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
                np.isfinite(flux_err) * (q > 0)
        x.extend(time[m])
        yerr.extend(flux_err[m]/np.median(flux[m]))
        y.extend(flux[m]/np.median(flux[m]) - 1)
    return np.array(x), np.array(y), np.array(yerr)

if __name__ == "__main__":

    kid, koi, teff, p, rpl, porb = np.genfromtxt("../data/results.txt",
                                                 skip_header=2).T

    for i, k in enumerate(kid):
        print str(int(k)), p[i]
        x, y, yerr = load_data(str(int(k)))

        plt.clf()
        plt.errorbar(x, y, yerr, **reb)
        plt.savefig("%s_lc" % str(int(k)))

        corr_run(x, y, yerr, int(k), "allq",
                 "/Users/angusr/Python/HotStarsInc/ACFresults")
