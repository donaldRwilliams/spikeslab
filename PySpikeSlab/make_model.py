def make_model_code(family = "gaussian", 
                    prior = "normal", 
                    ss_type = "ssvs", 
                    scale_sl = 1,
                    scale_sp = 0.01,
                    pi = 0.5):
    if family == "gaussian":
        lik = '''
        model{
            for (i in 1:N){
                mu[i]  <- alpha + inprod(X[i,], beta)
                y[i] ~ dnorm(mu[i], prec)
                }
            ''' 
    elif family == "binomial":
        lik = '''
        model{
            for (i in 1:N){
                logit(mu[i])  <- alpha + inprod(X[i,], beta)
                y[i] ~ dbern(mu[i])
                }
            ''' 
    elif family == "poisson":
        lik = '''
        model{
            for (i in 1:N){
                log(mu[i])  <- alpha + inprod(X[i,], beta)
                y[i] ~ dpois(mu[i])
                }
            ''' 
    elif family == "student_t":
            lik = '''
            model{
            for (i in 1:N){
                mu[i]  <- alpha + inprod(X[i,], beta)
                y[i] ~ dt(mu[i], prec, nu)
                }
            nu ~ rgamma(2, 10)
            ''' 
    if ss_type == "ssvs":
        if prior == "normal":
               coefs = ''' 
               for(i in 1:p){
                   gamma[i] ~ dbern(pi)
                   beta_sl[i] ~ dnorm(0, pow(scale_sl, -2))
                   beta_sp[i] ~ dnorm(0, pow(scale_sp, -2))
                   beta[i] <- (gamma[i] * beta_sl[i]) + ((1 - gamma[i]) * beta_sp[i])
                }
             '''
        elif prior == "lasso":
                coefs = ''' 
                for(i in 1:p){
                    gamma[i] ~ dbern(pi)
                    beta_sl[i] ~ ddexp(0, pow(scale_sl, -2))
                    beta_sp[i] ~ ddexp(0, pow(scale_sp, -2))
                    beta[i] <- (gamma[i] * beta_sl[i]) + ((1 - gamma[i]) * beta_sp[i])
                }
            '''
    elif ss_type == "km":
        if prior == "normal":
               coefs = ''' 
               for(i in 1:p){
                   gamma[i] ~ dbern(pi)
                   beta_sl[i] ~ dnorm(0, pow(scale_sl, -2))
                   beta[i] <- (gamma[i] * beta_sl[i])
                }
             '''
        elif prior == "lasso":
                coefs = ''' 
                for(i in 1:p){
                    pi[i] ~ dbern(0.5)
                    beta_sl[i] ~ ddexp(0, pow(scale_sl, -2))
                    beta[i] <- (gamma[i] * beta_sl[i])
                }
            '''
    priors = '''
            alpha ~ dnorm(0, 0.01)
            prec ~ dgamma(0.001, 0.001)
            sigma <- sqrt(1 / prec)
            }'''
    
    return lik + coefs + priors