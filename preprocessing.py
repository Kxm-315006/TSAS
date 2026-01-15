import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

def preprocess_tsas_data():
    # Paths
    input_path = "data/raw/tsas_raw_data.csv"
    output_dir = "data/processed"
    output_path = os.path.join(output_dir, "tsas_processed_data.csv")

    # Create processed directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load raw dataset
    df = pd.read_csv(input_path)

    # Separate features and label
    features = df[["distance", "speed", "direction", "intent", "signal"]]
    labels = df["severity"]

    # Normalize features (0–1 range)
    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features)

    # Encode severity labels
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    # Create processed DataFrame
    processed_df = pd.DataFrame(
        features_scaled,
        columns=["distance", "speed", "direction", "intent", "signal"]
    )
    processed_df["severity"] = labels_encoded

    # Save processed dataset
    processed_df.to_csv(output_path, index=False)

    print("✅ tsas_processed_data.csv generated successfully")
    print("📍 Saved at:", output_path)

if __name__ == "__main__":
    preprocess_tsas_data()
