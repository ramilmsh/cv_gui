import cv2
import numpy as np
from keras import Model
from keras.models import load_model
from matplotlib import pyplot as plt


X_train = np.load('data/test_in.npy')
y_train = np.load('data/test_out.npy')
# tmp = sorted(zip(X_train, y_train), key=lambda pair: pair[1], reverse=True)
# X_train = np.array([x for x, _ in tmp]).astype(np.float32) / 255.
# y_train = np.array([y for _, y in tmp])
# print(X_train[y_train == 1][:4])
print(X_train.shape)

model = load_model('model')  # type: Model
result = model.predict(X_train)
img = np.array(result[:, 1] * 255., np.uint8)
img = img.reshape((1496, 496))

img2 = np.array(y_train * 255., np.uint8)
img2 = img2.reshape((1496, 496))
print(img.shape)
# plt.subplot(1, 2, 1)
# plt.imshow(img)
# plt.subplot(1, 2, 2)
img = np.hstack((img, img2))
cv2.imshow('bla', img)
cv2.waitKey(0)

exit(0)
count = 0
epsilon = .3
for i in range(0, len(y_train), 100):
    plt.imshow(X_train[i])
    print(result[i], " :: ", y_train[i], " :: ", 1. - result[i][y_train[i]])
    plt.show()
    if 1. - result[i][y_train[i]] > epsilon:
        print('no match')
        count += 1

print("fail rate: %.2f%%" % (count / len(y_train)))
