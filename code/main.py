import numpy as np
import matplotlib.pyplot as plt
import glob
from GProtation import MCMC, make_plot
from GPgrid import bin_data
import george
from george.kernels import ExpSquaredKernel, ExpSine2Kernel
from colours import plot_colours
cols = plot_colours()
from params import plot_params
reb = plot_params()
from check_prot_measurements import load_data
import os

if __name__ == "__main__":
    kids, koi, teff, p, rpl, porb = np.genfromtxt("../data/results.txt",
                                                 skip_header=2).T
    for i, kid in enumerate(kids[1:]):
        x, y, yerr = load_data(str(int(kid)))
        x -= x[0]
        m = x < 5
        x, y, yerr = x[m], y[m], yerr[m]

        # initialise
        init_file = "../data/%s_init.txt" % int(kid)
        if os.path.exists(init_file): theta_init = np.genfromtxt(init_file).T
        else: theta_init = [1, 1, 1, np.log(p[i]), 1.]

        k = theta_init[0] * ExpSquaredKernel(theta_init[1]) \
                * ExpSine2Kernel(theta_init[2], theta_init[3])
        gp = george.GP(k)
        gp.compute(x, np.sqrt(theta_init[4]**2+yerr**2))

        # predict
        xs = np.linspace(x[0], x[-1], 1000)
        mu, cov = gp.predict(y, xs)
        plt.clf()
        plt.errorbar(x, y, yerr=yerr, **reb)
        plt.plot(xs, mu)
        plt.show()

        plims = [2., 30.]
        DIR = "../figs"
        sampler = MCMC(theta_init, x, y, yerr, plims, 100, 200, int(kid), DIR)
        make_plot(sampler, x, y, yerr, int(kid), DIR, traces=True)
        assert 0
