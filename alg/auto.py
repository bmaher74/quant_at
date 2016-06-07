#!/usr/bin/env python
#
# Given data samples sequentially this class computes and stores the needed second
# order statistics and can then return autocovariance and autocorrelations for real valued data.
#
# Namely the sample autocovariance is given by 
#
# \gamma_k = \frac{ 1 }{ T - k } \sum_{s=k+1}^{T} x_s x_{s-k}
#
# and the sample autocorrelation is given by
#
# \rho_k = \frac{ \gamma_k }{ \gamma_0 }
#
# Written by:
# -- 
# John L. Weatherwax                2007-07-05
# 
# email: wax@alum.mit.edu
# 
# Please send comments and especially bug reports to the
# above email address.
# 
#-----

import numpy; from numpy import nan, asarray 

class Autocovariance(object):
    """
    A class that stores information needed to recursively compute the sample autocorrelation when provided sample values 
    """

    def __init__(self,N=1):
        self.N = N # maximum autocorrelation to compute; N=1 will compute \gamma_0 and \gamma_1 
        self.n = 0 # number of samples processed 
        self.pastSamples = N * [0.] # rolling buffer of past samples
        self.product_pairs = (N+1) * [0.] # estimates of the pairwise products needed to calculate gamma_0, gamma_1, \cdots, gamma_{N-1}, gamma_N


    def addSample(self,sample):

        self.n += 1

        # Extend our history of samples to include this new one: 
        #
        self.pastSamples.append(sample)

        # Compute the pairwise products needed:
        #
        for ii in range(len(self.product_pairs)):
            self.product_pairs[ii] += sample * self.pastSamples[-(ii+1)] 

        # Drop this sample off the end:
        #
        self.pastSamples.pop(0)

        assert len(self.product_pairs) == len(self.pastSamples)+1, "incorrect lengths"


    def gamma_k(self):

        if self.n <= self.N : return None 
        gamma_k_hat = asarray( self.product_pairs[:] )
        denom = self.n - asarray( range(len(gamma_k_hat)) )
        gamma_k_hat /= denom 

        return gamma_k_hat 
    
    def rho_k(self):

        gamma_k_hat = self.gamma_k()
        rho_k = gamma_k_hat / ( gamma_k_hat[0] * numpy.ones(len(gamma_k_hat)) )

        return rho_k 
    

if __name__ == "__main__":
    """
    > ts.sim = arima.sim( list(ma=-0.5), n=100 )
    > ts.sim
    """

    ts_sim = asarray( [ 
        -0.19152261,  0.24311414,  1.14698345, -0.39240771,  0.45224881,  0.08313432, 
         0.45951847, -1.39048660,  0.54379945, -1.01406587, -0.35466795, -0.40761576, 
         1.15995601, -0.18134112, -0.28176396,  0.68850908, -0.50814753, -1.04393618, 
         0.56516430, -0.31344298, -0.47494378, -2.08720719,  0.11403360,  0.47482930, 
         0.28336282,  1.12671785,  0.13760795, -0.63653001, -0.03986714,  0.63556745, 
        -0.68104508, -1.25175265, -0.65141305,  0.55619500, -0.42384804,  1.93386427, 
        -1.68813708,  0.20122715, -0.07917019, -0.27962501, -0.40236857, -0.13291797, 
         1.27959053,  1.12878176, -1.29147072,  0.58955505, -0.23248120,  0.35844150, 
         0.61468978, -1.29617737,  0.48857542, -3.09991002,  1.40147913, -0.06059393, 
         0.93370186, -0.59728663, -0.63585512,  0.11828885,  0.83025296,  1.02275397, 
        -1.33733847,  0.57322808, -2.06688757,  1.71250394, -0.56082298, -1.11913094, 
         0.40511408,  0.95957116, -1.32882612,  2.22604307, -1.79884992,  1.29432723, 
        -0.06402859, -0.74370095, -0.54481705,  1.95150783, -0.97488693,  0.97122587, 
        -1.21812671, -0.41006716,  0.03602930,  0.04229312, -0.22375490, -0.12943953, 
         0.31413482,  0.04938972, -0.59890389,  0.22422772, -0.85851560,  1.67498484, 
        -1.51242812,  0.17448620, -0.15463671, -0.30208034,  0.63337405, -0.15475645, 
        -1.18639082,  0.62502794, -0.15798528,  0.44167714 ] )

    ac = Autocovariance(N=2)
    for samp in ts_sim:
        ac.addSample( samp )
    print "Autocovariance= ", ac.gamma_k()
    print "Autocorrelation= ", ac.rho_k()

    
