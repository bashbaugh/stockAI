from keras.datasets import mnist
from keras import models, layers
from keras.utils import to_categorical
print("Modules Loaded")

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images = train_images.reshape((60000, 28*28))
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28*28))
test_images = test_images.astype('float32') / 255
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)
print("Data Loaded and Prepared")

nn = models.Sequential()
nn.add(layers.Dense(512, activation='relu', input_shape=(28*28,)))
nn.add(layers.Dense(10, activation='softmax'))
nn.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
print("Network Prepared")

print("Fitting Model")
nn.fit(train_images, train_labels, epochs=5, batch_size=128)
print("Done Fitting Model")

test_loss, test_acc = nn.evaluate(test_images, test_labels)
print("test accuracy: " + str(test_acc)) 
