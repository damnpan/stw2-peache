# import the necessary packages
import tensorflow as tf
from tensorflow import keras
import numpy as np
import urllib.request as ur
import cv2
import random

# importing dataset
fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# preprocessing data for training machine- normalizing inputs in range 0 to 1
train_images = train_images / 255.0 

test_images = test_images / 255.0

# training model
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)), 
    keras.layers.Dense(128, activation='relu'), # 128 nodes, rectified linear unit
    keras.layers.Dense(10) 
])

# optimizer - minimizing loss(penalty for bad prediction)
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# train in 10 epochs
model.fit(train_images, train_labels, epochs=10)

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print('\nTest accuracy:', test_acc)

probability_model = tf.keras.Sequential([model, 
                                         tf.keras.layers.Softmax()])

labels = []

# get the category of image
def get_label(image):
  if np.argmax(probability_model.predict(image)[0]) == 0 or np.argmax(probability_model.predict(image)[0]) == 6 or np.argmax(probability_model.predict(image)[0]) == 2:
    return "top"
  elif np.argmax(probability_model.predict(image)[0]) == 1:
    return "btm"
  elif np.argmax(probability_model.predict(image)[0]) == 3 or np.argmax(probability_model.predict(image)[0]) == 4:
    return "dress"
  elif np.argmax(probability_model.predict(image)[0]) == 5 or np.argmax(probability_model.predict(image)[0]) == 7 or np.argmax(probability_model.predict(image)[0]) ==  9:
    return "shoe"
  else:
    return "bag"

# OpenCV, NumPy, and urllib
# reading url
def url_to_image(link):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = ur.urlopen(link)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
	# return the image
	return image


# reading products.txt for links
prep_products = []
prep_aproducts=[]
fp = open("PRODUCTS.txt", "r")
for line in fp:
  for word in line.split():
    prep_products.append(word)
  prep_aproducts.append(prep_products)
  prep_pruducts=[]
fp.close()


# appending links from products.txt file
urls = []
for i in range(len(prep_aproducts)):
  urls.append(prep_aproducts[i][-2])


# getting image
for url in urls:
  image = url_to_image(url)
  # masking background
  r = 150.0 / image.shape[1]
  dim = (150, int(image.shape[0] * r))
  resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA) 
  lower_white = np.array([220, 220, 220], dtype=np.uint8)
  upper_white = np.array([255, 255, 255], dtype=np.uint8)
  mask = cv2.inRange(resized, lower_white, upper_white) # getting just the white parts
  res = cv2.bitwise_not(resized, resized, mask) # changing white parts to black

  res_cvt = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY) # converting to grayscale img

  # reshaping image to 28 x 28 numpy array
  resized_image = cv2.resize(res_cvt, (28, 28))
  resized_image = resized_image.reshape(28, 28)
  resized_image = resized_image / 255.0

  resized_image = (np.expand_dims(resized_image,0))

  # getting list of labels in order
  labels.append(get_label(resized_image))
               


# read txt file, create list of product info
products = []
aproducts=[]
fp = open("PRODUCTS.txt", "r")
for line in fp:
  for word in line.split():
    products.append(word)
  products.append(labels[line])
  aproducts.append(products)
  products=[]
fp.close()




#initialise
dress = []
shoe = []
top = []
btm = []
bag = []
img_links = []
selected_images = []
buy_links = []

# sort dress
def dress_sort(array):
  for i in range(len(array)):
    if array[i][-1] == "dress":
      dress.append(i)
    else:
      continue
  return dress
  
# sort top
def top_sort(array):
  for i in range(len(array)):
    if array[i][-1] == "top":
      top.append(i)
    else:
      continue
  return top 

# sort btm
def btm_sort(array):
  for i in range(len(array)):
    if array[i][-1] == "btm":
      btm.append(i)
    else:
      continue
  return btm

# sort shoe
def shoe_sort(array):
  for i in range(len(array)):
    if array[i][-1] == "shoe":
      shoe.append(i)
    else:
      continue
  return shoe

# sort bag
def bag_sort(array):
  for i in range(len(array)):
    if array[i][-1] == "bag":
      bag.append(i)
    else:
      continue
  return bag

# randomiser, keep id
def rselect(lst):
  select = random.choice(lst[random.randint(0, len(lst))])
  img_links.append(select[-2])
  buy_links.append(select[-3])
  return img_links, buy_links


# https://stackoverflow.com/questions/930397/getting-the-last-element-of-a-list

# promote using the id (select is the id)

### main ###
dress_sort(aproducts)
top_sort(aproducts)
btm_sort(aproducts)
shoe_sort(aproducts)
bag_sort(aproducts)

for i in range(5):
  rselect(random.choice([dress, top, btm, shoe, bag]))



for i in range(len(img_links)):
  selected_images = url_to_image(img_links[i]) 

