library("urca")
library("vars")
library('mFilter')
library("tseries")
library("TSstudio")
library("forecast")
library("tidyverse")

setwd('/users/felipe/desktop/code/corcovado/inflation_MktCap_analysis')

data <- read_csv(file.choose())
head(data)

# Convert to time series

infl <- ts(data$inflation, start = c(1981), frequency = 1)
MktCap <- ts(data$MktCap, start = c(1981), frequency = 1)
M2 <- ts(data$M2, start = c(1981), frequency = 1)
M1 <- ts(data$M1, start = c(1981), frequency = 1)
M0 <- ts(data$M0, start = c(1981), frequency = 1)
GDP <- ts(data$GDP, start = c(1981), frequency = 1)
M1V <- ts(data$M1V, start = c(1981), frequency = 1)
M2V <- ts(data$M2V, start = c(1981), frequency = 1)


# SVAR restrictions

amat <- diag(8)
#mktcap -> 
amat[1,2] <- NA
amat[6,2] <- NA
amat[7,2] <- NA
amat[8,2] <- NA
#M2 ->
amat[1,3] <- NA
#M1 ->
amat[3,4] <- NA
#M0 ->
amat[3,5] <- NA
amat[4,5] <- NA
#GDP
amat[1,6] <- NA
#M1V
amat[1,7] <- NA
#M2V
amat[1,8] <- NA


sv <- cbind(infl, MktCap, M2, M1, M0, GDP, M1V, M2V)

lagselect = VARselect(sv, lag.max = 8, type = 'both')
lagselect

Model <- VAR(sv, p = 5, season = NULL, exog = NULL, type = 'const')
SVARModel <- SVAR(Model, Amat = amat)
summary(SVARModel)
fevd(SVARModel)

Phi(SVARModel)
A = SVARModel

SVARplot <- irf(SVARModel, impulse = 'MktCap', response = 'infl')
SVARplot
plot(SVARplot)

SVARGDP <- irf(SVARModel, impulse = 'GDP', response = 'infl')
plot(SVARGDP)

SVARM2 <- irf(SVARModel, impulse = 'M2', response = 'infl')
plot(SVARM2)

SVARM2V <- irf(SVARModel, impulse = 'M2V', response = 'infl')
plot(SVARM2V)


### Regression model analysis

model1 = lm(inflation ~ M2 + GDP + M2V, data = data)
model2 = lm(inflation ~ M2 + GDP + M2V + MktCap, data = data)

anova(model1, model2)
