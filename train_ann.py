import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

# Load processed data
df = pd.read_csv("data/processed/tsas_processed_data.csv")

X = df[["distance", "speed", "direction", "intent", "signal"]].values
y = df["severity"].values

# One-hot encode labels
y = to_categorical(y, num_classes=4)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Build ANN model
model = Sequential([
    Dense(16, activation="relu", input_shape=(5,)),
    Dense(8, activation="relu"),
    Dense(4, activation="softmax")
])

# Compile model
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Train model
history = model.fit(
    X_train,
    y_train,
    epochs=30,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Evaluate model
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"✅ TSAS ANN Accuracy: {accuracy * 100:.2f}%")

# Save trained model
model.save("model/tsas_model.h5")
print("✅ TSAS ANN model saved successfully")
