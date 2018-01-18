#This script was written to model fictional sales data for a homework assignment

library('dplyr')
library('forecast')
library('fma')
library('tseries')
library('expsmooth')
library('lmtest')
library('zoo')

AZ.SALES = read.csv(file = "C:/Users/mabre/Google Drive/Fall 2 Homework (Team 10)/Time Series 2/HW3/Data/AZ_SALES.csv",header = TRUE, sep = ',')

is.na(AZ.SALES$SALES_PH)
AZ.SALES.NONMISSING <- na.omit(AZ.SALES)

i = c(1:260)
AZ.SALES.NONMISSING = cbind(AZ.SALES.NONMISSING,i)

#PLOTTING
plot(x = AZ.SALES.NONMISSING$i, y = AZ.SALES.NONMISSING$SALES_PH)
plot(x = AZ.SALES.NONMISSING$i, y = AZ.SALES.NONMISSING$SALES_TU)

#creating linear model for tuscon
lm.ts = lm(AZ.SALES.NONMISSING$SALES_TU ~ i)
summary(lm.ts)
plot(lm.ts)

#create time series object using training set, create validation set
lm.ts$residuals
tu.ts = ts(lm.ts$residuals[1:244])
tu.valid = AZ.SALES.NONMISSING$SALES_TU[245:260]

#differencing one lag for pheonix, creating TS object from residuals
ph.diff = diff(AZ.SALES.NONMISSING$SALES_PH, lag = 1, differences = 1)
length(ph.diff)

#create time series object using training set, create validation set
#ph.ts = ts(ph.diff[1:243])
#ph.valid = ph.diff[244:259]
ph.ts = ts(AZ.SALES.NONMISSING$SALES_PH[1:244])
ph.valid = AZ.SALES.NONMISSING$SALES_PH[245:260]

#ADF Tests
adf.test(lm.ts$residuals, alternative = "stationary", k = 0)
adf.test(ph.diff,alternative = "stationary", k = 0)

#ARIMA Modeling
acf(tu.ts,ylim=c(-0.2, 1.0),main='Deterministic Model Residuals - Tucson ACF')
pacf(tu.ts,ylim=c(-0.2, 1.0),main='Deterministic Model Residuals - Tucson PACF')
acf(ts(ph.diff),ylim=c(-0.2, 1.0),main='Differenced Data - Phoenix ACF')
pacf(ts(ph.diff),ylim=c(-0.2, 1.0),main='Differenced Data - Phoenix PACF')
acf(ph.ts)
pacf(ph.ts)

tu.arima = arima(tu.ts, order = c(0,0,1))
summary(tu.arima)
acf(tu.arima$residuals)
pacf(tu.arima$residuals,ylim=c(-0.2, 0.8))

ph.arima = arima(ph.ts, order = c(1,1,0))
summary(ph.arima)
acf(ph.arima$residuals)
pacf(ph.arima$residuals)

#testing for white noise
tu.white.LB <- rep(NA, 10)
for(i in 1:10){
  tu.white.LB[i] <- Box.test(tu.arima$residuals, lag = i, type = "Ljung", fitdf = 1)$p.value
}

tu.white.LB <- pmin(tu.white.LB, 0.2)
barplot(tu.white.LB, main = "Tucson Ljung-Box Test P-values", ylab = "Probabilities", xlab = "Lags", ylim = c(0, 0.2))
abline(h = 0.01, lty = "dashed", col = "black")
abline(h = 0.05, lty = "dashed", col = "black")

ph.white.LB <- rep(NA, 10)
for(i in 1:10){
  ph.white.LB[i] <- Box.test(ph.arima$residuals, lag = i, type = "Ljung", fitdf = 1)$p.value
}

ph.white.LB <- pmin(ph.white.LB, 0.2)
barplot(ph.white.LB, main = "Phoenix Ljung-Box Test P-values", ylab = "Probabilities", xlab = "Lags", ylim = c(0, 0.2))
abline(h = 0.01, lty = "dashed", col = "black")
abline(h = 0.05, lty = "dashed", col = "black")

#calculating forecasts
tu.forecast = forecast(tu.arima, h = 16)
tu.predict = rbind(tu.forecast$mean, c(245:260))
tu.predict = 40.39121 + tu.predict[2,]*0.19889 + tu.predict[1,]
#tu.predict = 40.7889 + tu.predict[2,]*0.1946 + tu.predict[1,]


ph.forecast = forecast(ph.arima, h = 16)
ph.predict = ph.forecast$mean

#calculating MAPE
mean(abs((tu.valid - tu.predict)/tu.valid)*100) # 5.829801%
mean(abs((ph.valid - ph.predict)/ph.valid)*100) # 1.515173%

#calculating RMSE
sqrt(mean((tu.valid - tu.predict)^2)) # 6.350969
sqrt(mean((ph.valid - ph.predict)^2)) # 2.101343

#ESM models
#simple for Phoenix, holt for Tucson
tu.esm = holt(ts(AZ.SALES.NONMISSING$SALES_TU[1:244]), initial = "optimal", h = 16)
ph.esm = ses(ts(AZ.SALES.NONMISSING$SALES_PH[1:244]), initial = "optimal", h = 16)

#MAPE for ESMs
mean(abs((tu.valid - tu.esm$mean)/tu.valid)*100) # 5.543916%
mean(abs((ph.valid - ph.esm$mean)/ph.valid)*100) # 1.489981%

#RMSE for ESMs
sqrt(mean((tu.valid - tu.esm$mean)^2)) # 6.538433
sqrt(mean((ph.valid - ph.esm$mean)^2)) # 2.066722

#rebuild model using full time series data
tu_all.ts = ts(lm.ts$residuals)
ph_all.ts = ts(AZ.SALES.NONMISSING$SALES_PH)

tu_all.arima = arima(tu_all.ts, order = c(0,0,1))
tu_all.forecast = forecast(tu_all.arima, h = 16)
TU_PREDICTIONS = 40.39121 + c(261:276)*0.19889 + tu_all.forecast$mean

ph_all.arima = arima(ph_all.ts, order = c(1,1,0))
ph_all.forecast = forecast(ph_all.arima, h = 16)
PH_PREDICTIONS = ph_all.forecast$mean

acf(tu_all.arima$residuals,ylim=c(-0.2, 1.0),main='Tucson ACF')
pacf(tu_all.arima$residuals,ylim=c(-0.2, 1.0),main = 'Tucson PACF')
acf(ph_all.arima$residuals,ylim=c(-0.2, 1.0),main='Phoenix ACF')
pacf(ph_all.arima$residuals,ylim=c(-0.2, 1.0),main='Phoenix PACF')

#testing for white noise (full model)
tu_all.white.LB <- rep(NA, 10)
for(i in 1:10){
  tu_all.white.LB[i] <- Box.test(tu_all.arima$residuals, lag = i, type = "Ljung", fitdf = 1)$p.value
}

tu_all.white.LB <- pmin(tu_all.white.LB, 0.2)
names(tu_all.white.LB) = c('0','1','2','3','4','5','6','7','8','9')
barplot(tu_all.white.LB, main = "Tucson Ljung-Box Test P-values", ylab = "Probabilities", xlab = "Lags", ylim = c(0, 0.2))
abline(h = 0.01, lty = "dashed", col = "black")
abline(h = 0.05, lty = "dashed", col = "black")

ph_all.white.LB <- rep(NA, 10)
for(i in 1:10){
  ph_all.white.LB[i] <- Box.test(ph_all.arima$residuals, lag = i, type = "Ljung", fitdf = 1)$p.value
}

ph_all.white.LB <- pmin(ph_all.white.LB, 0.2)
names(ph_all.white.LB) = c('0','1','2','3','4','5','6','7','8','9')
barplot(ph_all.white.LB, main = "Phoenix Ljung-Box Test P-values", ylab = "Probabilities", xlab = "Lags", ylim = c(0, 0.2))
abline(h = 0.01, lty = "dashed", col = "black")
abline(h = 0.05, lty = "dashed", col = "black")

#need to redo model for Tucson to get the plot to look right
linear.arima = Arima(AZ.SALES.NONMISSING$SALES_TU, order = c(0,0,1), xreg = AZ.SALES.NONMISSING$i)
linear.forecast = forecast(linear.arima, h = 16, xreg = c(261:276))
autoplot(linear.forecast)+labs(x = 'Week Index', y='Sales') + ggtitle('Tucson Sixteen-Week Forecast')+theme(plot.title = element_text(hjust = 0.5))
autoplot(ph_all.forecast)+labs(x = 'Week Index', y='Sales') + ggtitle('Phoenix Sixteen-Week Forecast')+theme(plot.title = element_text(hjust = 0.5))


#trying some things in auto.arima
# ph.test = auto.arima(ph.ts)
# summary(ph.test)
# tu.test = auto.arima(tu.ts)
# summary(tu.test)
# 
# tu.ts2 = ts(AZ.SALES.NONMISSING$SALES_TU)
# tu.test2 = Arima(tu.ts2, order = c(0,0,1), include.drift = TRUE)
# summary(tu.test2)
# summary(tu.test)
# tu.forecast2 = forecast(tu.test2, h = 16)
# tu.forecast2$mean
# TU_PREDICTIONS
# autoplot(tu.forecast)
# autoplot(tu.esm)
# 
# autoplot(linear.arima)
# linear.forecast = forecast(linear.arima, h = 16, xreg = c(245:260))
# autoplot(linear.forecast)
# linear.forecast$mean
# TU_PREDICTIONS
# 
# #MAPE for ESMs
# mean(abs((tu.valid - linear.forecast$mean)/tu.valid)*100) # 5.543916%
# mean(abs((ph.valid - ph.esm$mean)/ph.valid)*100) # 1.489981%
