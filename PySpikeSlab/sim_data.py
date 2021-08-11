import numpy as np

class simdata:
    def __init__(self, _y, _X, _betas, _alpha):
            self.y = _y
            self.X = _X
            self.betas = _betas
            self.alpha = _alpha
    
    @property
    def _y(self):
        return self.y

    @property
    def _X(self):
        return self.X

    @property
    def _beta(self):
        return self.betas
    
    @property
    def _alpha(self):
        return self.alpha


def simulate_data(p = 10, n = 200, cors = None, prob = 0.2, 
                  snr = 0.5, family =  "gaussian", 
                  alpha = None):
    
    """
    This function generates data for a multiple regression.
    
    Parameters
    ----------
    p: the number of variables
    
    n: the number of observations
    
    cors: correlation structure for the predictors (defaults to an identity matrix)
    
    prob: proportion of non-zero effects (of p)
    
    snr: signal-to-noise ratio(R2 = SNR / (1 + SNR))
    
    family: which family (defaults to Gaussian)?
    
    alpha: value for the intercept (defaults to 5)

    
    Returns
    -------
    y: outcome
    
    X: predictors
    
    beta: true coefficients (sampled from a uniform distribution)

    alpha: true intercept
    """
    
    
    # probability of 1
    prob_1 = np.round(prob, 1)
    
    # probability of 0
    prob_0 = 1 - prob_1
    
    # mean of mvn
    mu = np.repeat(0, p)
    
    non_zero = np.random.uniform(0.5, 2, int(p * prob_1))

    # regression coefficients
    betas = np.concatenate([non_zero, np.repeat(0, p * prob_0)])
    
    # intercept (defaults to 5)
    if alpha is None: alpha = 5

    # correlation structure (defaults to identity)
    if cors is None: cors = np.identity(p)

    if family == "gaussian":
        
        sigma = np.sqrt(betas @ cors @ betas / snr)
        
        X = np.random.multivariate_normal(mu, cors, n)
        
        y = alpha + X @ betas + np.random.normal(0, sigma, n)
    
    return simdata(y_ = y, _X = X, _betas = betas, _alpha = alpha)
    