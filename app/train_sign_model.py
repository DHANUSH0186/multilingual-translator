import cv2
import mediapipe as mp
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

class SignLanguageTrainer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.data = []
        self.labels = []
    
    def extract_hand_features(self, frame):
        """Extract hand landmark coordinates"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            features = []
            
            for landmark in hand_landmarks.landmark:
                features.extend([landmark.x, landmark.y, landmark.z])
            
            return np.array(features)
        return None
    
    def collect_data_for_sign(self, sign_label, num_samples=100):
        """Collect training data for a specific sign"""
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        collected = 0
        
        print(f"Collecting data for sign: {sign_label}")
        print(f"Show the sign and press SPACE to capture")
        print(f"Need {num_samples} samples. Press Q to finish early.")
        
        while collected < num_samples:
            ret, frame = cap.read()
            if not ret:
                break
            
            cv2.putText(frame, f"Sign: {sign_label}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Collected: {collected}/{num_samples}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, "Press SPACE to capture", (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            features = self.extract_hand_features(frame)
            if features is not None:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                if results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(
                        frame, 
                        results.multi_hand_landmarks[0],
                        self.mp_hands.HAND_CONNECTIONS
                    )
            
            cv2.imshow('Data Collection', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' ') and features is not None:
                self.data.append(features)
                self.labels.append(sign_label)
                collected += 1
                print(f"Captured {collected}/{num_samples}")
            elif key == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print(f"Finished collecting data for {sign_label}")
    
    def train_model(self, save_path='models/sign_language_model.pkl'):
        """Train the classification model"""
        if len(self.data) == 0:
            print("No data collected!")
            return
        
        print(f"Training model with {len(self.data)} samples...")
        
        X = np.array(self.data)
        y = np.array(self.labels)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        accuracy = model.score(X_test, y_test)
        print(f"Model accuracy: {accuracy * 100:.2f}%")
        
        os.makedirs('models', exist_ok=True)
        with open(save_path, 'wb') as f:
            pickle.dump(model, f)
        
        print(f"Model saved to {save_path}")
        return model, accuracy

def main():
    trainer = SignLanguageTrainer()
    
    print("SIGN LANGUAGE MODEL TRAINER")
    
    signs_to_train = ['A', 'B', 'C', 'Hello', 'Thanks']
    
    print("Signs to train:", signs_to_train)
    
    for sign in signs_to_train:
        collect = input(f"Collect data for {sign}? (y/n): ")
        if collect.lower() == 'y':
            trainer.collect_data_for_sign(sign, 50)
    
    if len(trainer.data) > 0:
        train = input("Train model now? (y/n): ")
        if train.lower() == 'y':
            trainer.train_model()
            print("Training complete!")

if __name__ == "__main__":
    main()