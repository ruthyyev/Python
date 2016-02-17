from scipy.optimize import curve_fit
import pylab as plt
import numpy as np

def blackbody_lam(lam, T): 

#define a function that fits a blackbody as a function of wavelength in um and temperature in K

#this will return units of erg/s/cm^2/cm/Steradian

    from scipy.constants import h,k,c #planck, boltzmann and light speed constants
    lam = 1e-6 * lam #converts wavelength to metres
    return 2 * h * c ** 2 / (lam ** 5 * (np.exp(h * c / (lam * k * T)) - 1))
    
wa = np.linspace(0.1, 2, 100) #inputs the wavelength in um
T1 = 5000.
T2 = 8000.
y1 = blackbody_lam(wa, T1)
y2 = blackbody_lam(wa, T2)
ytot = y1 + y2

np.random.seed(1) #randomises the fake data...

#make synthetic data with Gaussian errors

sigma = np.ones(len(wa)) * 1 * np.median(ytot)
ydata = ytot + np.random.randn(len(wa)) * sigma

#plot the input blackbody model and synthetic data

plt.figure()
plt.plot(wa, y1, ':', lw=2, label = 'T1=%.0f' % T1)
plt.plot(wa, y2, ':', lw=2, label = 'T2=%.0f' % T2)
plt.plot(wa, ytot, ':', lw=2, label = 'T1 + T2\n(true model)')
plt.plot(wa, ydata, ls='steps-mid',lw=2, label = 'Fake data')
plt.xlabel('Wavelength (microns)')
plt.ylabel('Intensity (erg/s/cm$^2$/cm/Steradian)')

#fit two blackbodies to the synthetic data:

def func(wa, T1, T2):
    return blackbody_lam(wa, T1) + blackbody_lam(wa, T2)
        


popt, pcov = curve_fit(func, wa, ydata, p0=(1000,3000), sigma=sigma)

#get the best fitting parameter values and their 1 sigma errors

bestT1, bestT2 = popt
sigmaT1, sigmaT2 = np.sqrt(np.diag(pcov))

ybest = blackbody_lam(wa, bestT1) + blackbody_lam(wa, bestT2)

print 'True model values'
print 'T1 = %.2f' % T1
print 'T2 = %.2f' % T2

print 'Parameters of best-fitting model:'
print 'T1 = %.2f +/- %.2f' % (bestT1, sigmaT1)
print 'T2 = %.2f +/- %.2f' % (bestT2, sigmaT2)

degrees_of_freedom = len(wa) - 2
resid = (ydata - func(wa, *popt)) / sigma
chisq = np.dot(resid, resid)

print degrees_of_freedom, 'dof'
print 'chi squared %.2f' % chisq
print 'nchi2 %.2f' % (chisq / degrees_of_freedom)

#plot the solution:

plt.plot(wa, ybest, label='Best fitting\nmodel')
plt.legend(frameon=False)
plt.savefig('fit_bb.png')
plt.show()