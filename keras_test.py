#导入所需包
import subprocess
import numpy
import platform

from keras.layers import Dense, Activation
from keras.models import Sequential

"""
1.define a set of function
"""
model = Sequential()
model.add(Dense(input_dim= 28*28,
                output_dim = 500))
model.add(Activation('sigmoid'))

model.add(Dense(output_dim = 500))
model.add(Activation('sigmoid'))

model.add(Dense(output_dim = 10))
model.add(Activation('softmax'))
"""
2.how to compute loss
"""
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
"""
3.training(find the best function)
"""
# model.fit(x_train, y_train, batch_size=100, nb_epoch=20)

#定义变量
image_filename='train-images-idx3-ubyte.gz'
label_filename='train-labels-idx1-ubyte.gz'
image_filename_test='t10k-images-idx3-ubyte.gz'
label_filename_test='t10k-labels-idx1-ubyte.gz'

buffer_size=10000
buffer_size_test=1000
# 定义函数读取image，并保存为数组
def get_images(image_filename, buffer_size):
    m = subprocess.Popen(['zcat', image_filename], stdout=subprocess.PIPE)
    m.stdout.read(16)
    images = numpy.fromfile(m.stdout, 'ubyte', count=buffer_size *28 *28).reshape((buffer_size, 28 * 28)).astype('float32')
    images = images / 255.0 * 2.0 - 1.0
    m.terminate()
    return images

# 定义函数读取labels，并保存为数组
def get_labels(label_filename, buffer_size):
    l = subprocess.Popen(['zcat', label_filename], stdout=subprocess.PIPE)
    l.stdout.read(8)  # skip some magic bytes
    labels = numpy.fromfile(l.stdout, 'ubyte', count=buffer_size).astype("int")
    #print labels.shape
    l.terminate()
    return labels

x_train = get_images(image_filename, buffer_size)
y_train = get_images(label_filename, buffer_size)
x_test = get_images(image_filename_test, buffer_size_test)
y_test = get_images(label_filename_test, buffer_size_test)
model.fit(x_train, y_train, batch_size=100, epochs=20)
score = model.evaluate(x_test, y_test, batch_size=10)
model.save('model_weight.h5')



