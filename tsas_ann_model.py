import torch
import torch.nn as nn
import numpy as np

# -------------------------------------------------
# ANN MODEL DEFINITION
# -------------------------------------------------
class ThreatANN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(5, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 4)
        )

    def forward(self, x):
        return self.net(x)


# -------------------------------------------------
# TSAS MODEL WRAPPER (USED BY FASTAPI)
# -------------------------------------------------
class TSASModel:
    def __init__(self, weights_path: str = None):
        """
        Initializes ANN model.
        Loads trained weights if provided.
        """
        self.device = torch.device("cpu")

        self.model = ThreatANN().to(self.device)

        if weights_path:
            self.model.load_state_dict(
                torch.load(weights_path, map_location=self.device)
            )

        self.model.eval()  # IMPORTANT

        self.softmax = nn.Softmax(dim=1)

    def predict(self, features):
        """
        Input:
            features -> list or array of length 5
        Output:
            (predicted_class, probability_vector)
        """
        x = torch.tensor(features, dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            logits = self.model(x)
            probs = self.softmax(logits)

        predicted_class = torch.argmax(probs, dim=1).item()

        return predicted_class, probs.squeeze(0).cpu().numpy()
