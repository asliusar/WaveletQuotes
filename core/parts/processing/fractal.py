import nolds
import numpy as np

rwalk = np.cumsum(np.random.random(1000))
print("fractal {}".format(nolds.dfa(rwalk)))
print("Lup {}".format(nolds.lyap_e(rwalk)))
print("Lup {}".format(nolds.lyap_r(rwalk)))
print("Hurst {}".format(nolds.hurst_rs(rwalk)))

