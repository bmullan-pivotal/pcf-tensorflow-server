from tensorflow import keras
import flask
from flask import request
from flask import Flask
import os
import random
import numpy as np

# create the flask app
app = Flask(__name__)

# load the model and print summary
model = keras.models.load_model('./model/my_model.h5')
model.summary()

fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

train_images = train_images / 255.0
test_images = test_images / 255.0
input_shape = train_images.shape

# Evaluate the restored model
loss, acc = model.evaluate(test_images,  test_labels, verbose=2)
print('Restored model, accuracy: {:5.2f}%'.format(100*acc))
print(model.predict(test_images).shape)
print("Starting application ....................................\n")

# set the port dynamically with a default of 8000 for local development
cf_port = int(os.getenv('PORT', '8000'))

# app.run(host='0.0.0.0', port=port)
app.debug=True

@app.route('/')
def home():
	return "tf-sample"

@app.route('/test-predict')
def test_predict():
    # pick a random test image
    image = test_images[random.randint(0,len(test_images)-1)]
    # return predicted class
    p = model.predict(np.array([image]))[0]
    return class_names[np.argmax(p)]

print("name: ",__name__)

if __name__ == '__main__':
	app.run(port=cf_port,host='0.0.0.0')
