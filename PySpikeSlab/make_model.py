def make_model_code(family = "gaussian", prior = "normal", ss_type = "ssvs"):
    if family == "gaussian":
        lik = '''
        model{
            for (i in 1:N){
                mu[i]  <- alpha + inprod(X[i,], beta)
                y[i] ~ dnorm(mu[i], tau)
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
    if ss_type == "ssvs":
        if prior == "normal":
               coefs = ''' 
               for(i in 1:p){
                   pi[i] ~ dbern(0.5)
                   beta_sl[i] ~ dnorm(0, 0.01)
                   beta_sp[i] ~ dnorm(0, pow(0.01, -2))
                   beta[i] <- (pi[i] * beta_sl[i]) + ((1 - pi[i]) * beta_sp[i])
                }
             '''
        elif prior == "lasso":
                coefs = ''' 
                for(i in 1:p){
                    pi[i] ~ dbern(0.5)
                    beta_sl[i] ~ ddexp(0, 0.01)
                    beta_sp[i] ~ ddexp(0, pow(0.01, -2))
                    beta[i] <- (pi[i] * beta_sl[i]) + ((1 - pi[i]) * beta_sp[i])
                }
            '''
    elif ss_type == "km":
        if prior == "normal":
               coefs = ''' 
               for(i in 1:p){
                   pi[i] ~ dbern(0.5)
                   beta_sl[i] ~ dnorm(0, 0.01)
                   beta[i] <- (pi[i] * beta_sl[i])
                }
             '''
        elif prior == "lasso":
                coefs = ''' 
                for(i in 1:p){
                    pi[i] ~ dbern(0.5)
                    beta_sl[i] ~ ddexp(0, 0.01)
                    beta[i] <- (pi[i] * beta_sl[i])
                }
            '''
    priors = '''
            alpha ~ dnorm(0, 0.01)
            sigma ~ dunif(0, 1000)
            tau <- 1/ (sigma * sigma)
            }'''
    
    return lik + coefs + priors