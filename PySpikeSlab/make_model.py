def make_model_code(family: str="gaussian", 
                    prior: str="normal", 
                    ss_type: str="ssvs", 
                    pi: float=0.5) -> str:
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
                    gamma[i] ~ dbern(pi)
                    beta_sl[i] ~ ddexp(0, pow(scale_sl, -2))
                    beta[i] <- (gamma[i] * beta_sl[i])
                }
            '''
        elif ss_type == "invlog":
                coefs = ''' 
                for(i in 1:p){
                    lambda_hat[i] ~ dnorm(0, pow(scale_sl, -2))
                    sp_raw[i] ~ dnorm(0, 1)
                    beta[i] <- (tau * beta_sl[i] * ilogit(lambda_hat[i]))
                }
            '''
    priors = '''
            alpha ~ dnorm(0, 0.01)
            prec ~ dgamma(0.001, 0.001)
            sigma <- sqrt(1 / prec)
            }'''
    
    return lik + coefs + priors