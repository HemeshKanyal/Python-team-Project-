# Initialize the model
model = Sequential()  # (1) A linear journey of sequences

# Add a hidden layer
model.add(Dense(units=32, activation='ReLU'))  # (2) A web of connections

# Add an output layer
model.add(Dense(units=1, activation='sigmoid'))  # (2) A web of connections for output

# Prepare to train the model
model.compile(optimizer='Adam',  # (3) The crucial step for preparation
              loss='binary_crossentropy',  # (4) The price of mistakes
              metrics=['accuracy'])

# Fit the model to the data
model.fit(X_train, y_train, epochs=10, batch_size=32)
