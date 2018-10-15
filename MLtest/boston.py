from keras.datasets import boston_housing
(traind, traint), (testd, testt) = boston_housing.load_data()
mean = traind.mean(axis=0)
traind -= mean
std = traind.std(axis=0)
traind /= std
testd -= mean
testd /= std

