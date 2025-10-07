import schedule
import time
import numpy as np
from ml_detection import MLDetector

# Placeholder: user must implement real data loading

def load_new_data():
    # Return dummy batch: 8 samples of zero sequences
    X = np.zeros((8, 10, 2))
    y = np.zeros((8, 1))
    return X, y


def main():
    detector = MLDetector()
    detector.load_or_init()

    def job():
        X, y = load_new_data()
        detector.retrain(X, y)

    schedule.every().day.at("03:00").do(job)
    print("[SCHEDULER] Retrain scheduler started")
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    main()
