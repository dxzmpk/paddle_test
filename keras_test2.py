import keras # 导入Keras
import numpy as np
from keras.datasets import mnist # 从keras中导入mnist数据集
from keras.models import Sequential # 导入序贯模型
from keras.layers import Dense, Activation  # 导入全连接层
import cv2 as cv
from keras.optimizers import SGD # 导入优化函数
import matplotlib.pyplot as plt # 导入可视化的包
from keras.models import load_model

(x_train, y_train), (x_test, y_test) = mnist.load_data() # 下载mnist数据集
print(x_train.shape,y_train.shape)
print(x_test.shape,y_test.shape)
test_num = 12345
im = plt.imshow(x_train[test_num],cmap='gray')
plt.show()
x_train = x_train.reshape(60000,784)
x_test = x_test.reshape(10000,784)
x_train = x_train / 255
x_test = x_test / 255

image = cv.imread("2_1.png",0)
image = cv.resize(image,(28,28),)
image_to_array = np.asarray(image)
image_to_array_test = image_to_array.reshape(1,784)/255
print(image_to_array_test)
# 对label进行处理
y_train = keras.utils.to_categorical(y_train,10)
y_test = keras.utils.to_categorical(y_test,10)
print(x_train.shape, "还有：", y_train.shape)
"""
1.define a set of function
"""
model = Sequential()
model.add(Dense(input_dim= 28*28,
                output_dim = 500))
model.add(Activation('relu'))

model.add(Dense(output_dim = 500))
model.add(Activation('relu'))

for i in range(9):
    model.add(Dense(output_dim=500))
    model.add(Activation('relu'))

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
model.fit(x_train, y_train, batch_size=2000, nb_epoch=5)


model.save('model.h5')
model = load_model('model.h5')

# 构造选择例子
predict_example = np.array(x_train[test_num])
# result = model.predict(predict_example.reshape(1,784))
result = model.predict(image_to_array_test)

# 用训练集和测试集预测
train_score = model.evaluate(x_train,y_train,batch_size=60000)
test_score = model.evaluate(x_test, y_test, batch_size=10000)


print("train Acc",train_score[1])
print("test Acc",test_score[1])
# 找到最有可能的值并打印输出
result = list(result[0])
print(result.index(max(result)))

im = plt.imshow(image,cmap='gray')
plt.show()
cv.imwrite("new_image.png",image)

