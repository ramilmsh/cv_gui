import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

result = cv2.imread('raw_data/test8.png')
result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
img = cv2.imread('raw_data/test8_1.jpg')

bounds = [1000, 1000, 2500, 3000]
train_in = img[bounds[0]:bounds[2], bounds[1]:bounds[3]]
train_out = result[bounds[0]:bounds[2], bounds[1]:bounds[3]]

bounds = [1000, 3000, 2500, 3500]
test_in = img[bounds[0]:bounds[2], bounds[1]:bounds[3]]
test_out = result[bounds[0]:bounds[2], bounds[1]:bounds[3]]

# img = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9], [0, 1, 2], [3, 4, 5]],
#                 [[1, 2, 3], [4, 5, 6], [7, 8, 9], [0, 1, 2], [3, 4, 5]],
#                 [[1, 2, 3], [4, 5, 6], [7, 8, 9], [0, 1, 2], [3, 4, 5]],
#                 [[1, 2, 3], [4, 5, 6], [7, 8, 9], [0, 1, 2], [3, 4, 5]],
#                 [[1, 2, 3], [4, 5, 6], [7, 8, 9], [0, 1, 2], [3, 4, 5]]])

kernel_size = 5
offset = math.floor(kernel_size / 2)
data = []
output = []
step = 2

assert kernel_size % 2 == 1
for i in range(offset, train_in.shape[0] - offset, step):
    for j in range(offset, train_in.shape[1] - offset, step):
        data.append(train_in[i - offset: i + offset + 1, j - offset: j + offset + 1, :])
        output.append(1 if train_out[i][j] > 50 else 0)

np.save('data/train_in', data)
np.save('data/train_out', output)

data = []
output = []
step = 1

for i in range(offset, test_in.shape[0] - offset, step):
    for j in range(offset, test_in.shape[1] - offset, step):
        data.append(test_in[i - offset: i + offset + 1, j - offset: j + offset + 1, :])
        output.append(1 if test_out[i][j] > 50 else 0)

print(len(data))
np.save('data/test_in', data)
np.save('data/test_out', output)
