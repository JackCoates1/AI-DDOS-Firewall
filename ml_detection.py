import numpy as np
from tensorflow import keras
import pickle
import os

class MLDetector:
    def __init__(self, model_path="lstm_model.pkl", sequence_length=10, feature_size=2):
        self.model_path = model_path
        self.sequence_length = sequence_length
        self.feature_size = feature_size
        self.model = None
        self.window = []  # sliding feature window

    def build_model(self):
        model = keras.Sequential([
            keras.layers.Input(shape=(self.sequence_length, self.feature_size)),
            keras.layers.LSTM(64, return_sequences=False),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy')
        return model

    def load_or_init(self):
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print("[ML] Loaded existing model")
                return
            except Exception:
                print("[ML] Failed to load existing model, rebuilding")
        self.model = self.build_model()
        # Dummy initial training to finalize weights
        dummy_X = np.zeros((4, self.sequence_length, self.feature_size))
        dummy_y = np.zeros((4, 1))
        self.model.fit(dummy_X, dummy_y, epochs=1, verbose=0)
        print("[ML] Initialized new model")

    def detect_attack(self, feature_vector, ip_counts):
        # feature_vector: [total_packets, unique_ips]
        self.window.append(feature_vector)
        if len(self.window) > self.sequence_length:
            self.window.pop(0)
        if len(self.window) < self.sequence_length:
            # Not enough data to classify yet
            return False, []
        window_arr = np.array(self.window).reshape(1, self.sequence_length, self.feature_size)
        pred = self.model.predict(window_arr, verbose=0)
        attack = pred[0][0] > 0.5  # threshold placeholder
        # naive heuristic for attacker extraction
        attackers = [ip for ip, c in ip_counts.items() if c > 100] if attack else []
        return attack, attackers

    def retrain(self, sequence_batch, labels):
        # sequence_batch shape: (batch, sequence_length, feature_size)
        self.model.fit(sequence_batch, labels, epochs=3, verbose=0)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print("[ML] Model retrained and saved")
