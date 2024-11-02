# CS50 AI Traffic Project

## `get_model` Experimentation

When writing the code for the `get_model` function, I first simply copied and slightly modified the code used in the lecture for the handwritten digit recognition sample. This got the project running, but did not produce stellar results.

```
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.0574 - loss: 3.4960  
333/333 - 1s - 4ms/step - accuracy: 0.0566 - loss: 3.4954
```

Curiously, using the same code on the smaller dataset produced far more accurate results.

```
Epoch 10/10
16/16 ━━━━━━━━━━━━━━━━━━━━ 0s 5ms/step - accuracy: 0.9801 - loss: 0.0677 
11/11 - 0s - 8ms/step - accuracy: 0.9970 - loss: 0.0080
```

Next, I tried bumping the number of units in my dense layer from 128 to 256. This massively improved the accuracy of the model, with only 128 units, the model might have been underfitting, meaning it was too simple to capture the underlying structure of the data. Increasing the number of trainable parameters in the model allows the network to learn more complex patterns and relationships within the data

```
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 7ms/step - accuracy: 0.0668 - loss: 13.4500     
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 9ms/step - accuracy: 0.1094 - loss: 3.3974      
...
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 10ms/step - accuracy: 0.4057 - loss: 2.0194 
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 10ms/step - accuracy: 0.4335 - loss: 1.9148 
333/333 - 2s - 6ms/step - accuracy: 0.6331 - loss: 1.2328
```

To try and increase the accuracy of the model, I experimented with the output layer's activation function by changing it to `sigmoid`. However, the Sigmoid function is used for binary classification tasks, so this only resulted in lowering the accuracy drastically.

```
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.0509 - loss: 3.5013 
333/333 - 2s - 7ms/step - accuracy: 0.0507 - loss: 3.4926
```

Adding a second hidden layer with 64 units and the "relu" activation function gave me the best results so far.

```
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 7ms/step - accuracy: 0.0618 - loss: 12.5086
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.7610 - loss: 0.8548 
333/333 - 2s - 6ms/step - accuracy: 0.8832 - loss: 0.4515
```

Interestingly, setting both hidden layer's units to 128 put me back on a poor model accuracy of just 5%.

Setting the first hidden layer's units to 512 did not do much to improve accuracy, infact it fell to 78%. So I kept it at 256.

Upping the first layer's dropout to 0.75, killed accuracy. 0.5%

Changing the pooling size to (3, 3) slightly dropped the improvement rate and final model accuracy, so I changed it back.

```
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 9ms/step - accuracy: 0.6614 - loss: 1.1056  
333/333 - 1s - 4ms/step - accuracy: 0.8186 - loss: 0.6426
```

Doubling the number of epochs did not behave as I expected.

```
Epoch 1/20
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 7ms/step - accuracy: 0.0475 - loss: 17.4671         
Epoch 2/20
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 9ms/step - accuracy: 0.1361 - loss: 3.2806
...
Epoch 19/20
500/500 ━━━━━━━━━━━━━━━━━━━━ 7s 13ms/step - accuracy: 0.5699 - loss: 1.3809 
Epoch 20/20
500/500 ━━━━━━━━━━━━━━━━━━━━ 7s 14ms/step - accuracy: 0.5857 - loss: 1.2874 
333/333 - 3s - 9ms/step - accuracy: 0.7847 - loss: 0.7064
```

Adding a second convolution and pooling layer, this time with double the number of filters produced the best model yet. Improving very quickly and reaching an accuracy of 92.25% on the test set.

```python
# Convolutional layer. Learn 32 filters using a 3x3 kernel
keras.layers.Conv2D(32, (3, 3), activation="relu"),
# Max-pooling layer, using 2x2 pool size
keras.layers.MaxPooling2D(pool_size=(2, 2)),
# Convolutional layer. Learn 64 filters using a 3x3 kernel
keras.layers.Conv2D(64, (3, 3), activation="relu"),
# Max-pooling layer, using 2x2 pool size
keras.layers.MaxPooling2D(pool_size=(2, 2)),
```

```
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 7ms/step - accuracy: 0.0696 - loss: 7.7483         
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 8ms/step - accuracy: 0.3017 - loss: 2.6358  
...
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.8126 - loss: 0.6135 
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.8338 - loss: 0.5429
333/333 - 2s - 5ms/step - accuracy: 0.9225 - loss: 0.2863
```

The next adjustment that had the most impact was lowering the dropout rates to 0.3%. This greatly improved the learning rate, as well as the final accuracy of the model against the test set.

```python
# Create a convolutional neural network
model = keras.models.Sequential(
    [
        keras.Input((30, 30, 3)),
        # Convolutional layer. Learn 32 filters using a 3x3 kernel
        keras.layers.Conv2D(32, (3, 3), activation="relu"),
        # Max-pooling layer, using 2x2 pool size
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        # Convolutional layer. Learn 64 filters using a 3x3 kernel
        keras.layers.Conv2D(64, (3, 3), activation="relu"),
        # Max-pooling layer, using 2x2 pool size
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        # Flatten units
        keras.layers.Flatten(),
        # Add a hidden layer with dropout
        keras.layers.Dense(256, activation="relu"),
        keras.layers.Dropout(0.3),
        # Add a hidden layer with dropout
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dropout(0.3),
        # Add an output layer with output units for all 43 signs
        keras.layers.Dense(NUM_CATEGORIES, activation="softmax"),
    ]
)
```

```
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 7ms/step - accuracy: 0.1886 - loss: 5.4556     
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 9ms/step - accuracy: 0.5895 - loss: 1.3951 
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 10ms/step - accuracy: 0.7611 - loss: 0.8002
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.8482 - loss: 0.4898 
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 11ms/step - accuracy: 0.8976 - loss: 0.3709 
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 11ms/step - accuracy: 0.9161 - loss: 0.2891 
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 11ms/step - accuracy: 0.9355 - loss: 0.2381 
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 12ms/step - accuracy: 0.9418 - loss: 0.2126 
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 12ms/step - accuracy: 0.9507 - loss: 0.1717 
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 12ms/step - accuracy: 0.9521 - loss: 0.1754 
333/333 - 3s - 8ms/step - accuracy: 0.9733 - loss: 0.1094
```

As a final experiment, I tried removed the extra dense layer and simply doubling the number of units on the leftover one.

```python
# Create a convolutional neural network
model = keras.models.Sequential(
    [
        keras.Input((30, 30, 3)),
        # Convolutional layer. Learn 32 filters using a 3x3 kernel
        keras.layers.Conv2D(32, (3, 3), activation="relu"),
        # Max-pooling layer, using 2x2 pool size
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        # Convolutional layer. Learn 64 filters using a 3x3 kernel
        keras.layers.Conv2D(64, (3, 3), activation="relu"),
        # Max-pooling layer, using 2x2 pool size
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        # Flatten units
        keras.layers.Flatten(),
        # Add a hidden layer with dropout
        keras.layers.Dense(512, activation="relu"),
        keras.layers.Dropout(0.3),
        # Add an output layer with output units for all 43 signs
        keras.layers.Dense(NUM_CATEGORIES, activation="softmax"),
    ]
)
```

```
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.3997 - loss: 8.3665         
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 10ms/step - accuracy: 0.8312 - loss: 0.5884 
... 
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 12ms/step - accuracy: 0.9675 - loss: 0.1356 
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 6s 12ms/step - accuracy: 0.9675 - loss: 0.1203 
333/333 - 2s - 5ms/step - accuracy: 0.9678 - loss: 0.1764
```

The model performed arguably the same. The rationale behind this change was that deeper models run a higher risk of overfitting, where the model learns noise rather than meaningful patterns.