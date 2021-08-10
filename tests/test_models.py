import pytest
import pyjags

def test_testing():
    mod =    '''
       model{
           temp ~ dnorm(0, 1)
           }
        '''
        
    n_chains = 2
    coinflip_model = pyjags.Model(mod, chains = n_chains)
    coinflip_burnin = coinflip_model.sample(500, vars=['temp']) #warmup/burn-in
    coinflip_samples = coinflip_model.sample(2500, vars=['temp'])

test_testing()