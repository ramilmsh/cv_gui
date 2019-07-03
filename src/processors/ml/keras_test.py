import matplotlib.pyplot as plt
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
import numpy as np

X_train = np.load('data/train_in.npy')  # type: np.ndarray
y_train = np.load('data/train_out.npy')  # type: np.ndarray
tmp = sorted(zip(X_train, y_train), key=lambda pair: pair[1], reverse=True)
X_train = np.array([x for x, _ in tmp]).astype(np.float32) / 255.
y_train = np.array([y for _, y in tmp])

print(X_train.shape)
y_train = to_categorical(y_train)

model = Sequential([
    Flatten(),
    Dense(75, activation='relu', ),
    Dense(25, activation='relu', ),
    Dense(2, activation='sigmoid'),
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=4)
model.save('model')
