from tensorflow import keras
import flask
from flask import request
from flask import Flask, render_template, send_file,jsonify
import os
import random
from random import randrange
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
# matplotlib.use('Agg')
import uuid

# create the flask app
app = Flask(__name__,static_folder="web/app/build/static", template_folder="web/app/build")

def genRandomImageFile():
	image = test_images[random.randint(0,len(test_images)-1)]
	imageAsArray = image.reshape(28, 28);
	plt.imshow(imageAsArray, cmap='gray')
	filename = "./temp/"+str(uuid.uuid4())+".png"
	plt.savefig(filename)
	return filename

def genImageFile(image_id):
	image = test_images[image_id].reshape(28,28)
	plt.imshow(image, cmap='gray')
	plt.axis('off')	
	filename = "./temp/"+str(uuid.uuid4())+".png"
	plt.savefig(filename)
	return filename


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/accuracy')
def accuracy():
	return str('{:5.2f}%'.format(100*acc))

@app.route("/image/<int:image_id>",methods=['GET'])
def image(image_id):
	return send_file(genImageFile(image_id),
		mimetype='image/png', 
		as_attachment=False, attachment_filename='file.png')

@app.route("/get-image-ids",methods=['GET'])
def gen_image_ids():
	vals = []
	for i in range(0,10):
		vals.append(random.randint(0,len(test_images)-1))
	return jsonify(vals)

@app.route("/test-image")
def test_image():
	print(request.path)
	return send_file(genRandomImageFile(),
		mimetype='image/png', 
		as_attachment=False, attachment_filename='file.png')

@app.route('/test-predict')
def test_predict():
    # pick a random test image
    image = test_images[random.randint(0,len(test_images)-1)]
    # return predicted class
    p = model.predict(
    	np.array([image])
    	)[0]
    return class_names[np.argmax(p)]

@app.route('/predict/<int:image_id>',methods=['GET'])
def predict(image_id):
	image = test_images[image_id]
	# return predicted class
	p = model.predict(np.array([image]))
	return class_names[np.argmax(p)]


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

print(model.predict(test_images).shape)
print(len(test_images))
print("Starting application ....................................\n")
# set the port dynamically with a default of 8000 for local development
cf_port = int(os.getenv('PORT', '8000'))

# app.run(host='0.0.0.0', port=port)
app.debug=True

print("name: ",__name__)

if __name__ == '__main__':
	app.run(port=cf_port,host='0.0.0.0')
