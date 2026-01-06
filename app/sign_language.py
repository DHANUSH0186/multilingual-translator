import cv2
import mediapipe as mp
import numpy as np

class SignLanguageDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
    
    def detect_signs(self, frame):
        """Detect hand landmarks from camera frame"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        detected_text = ""
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on frame
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
                
                # Simple gesture detection (you can expand this)
                detected_text = "Hand detected!"
        
        return detected_text, frame
    
    def start_camera(self):
        """Start real-time sign language detection"""
        cap = cv2.VideoCapture(0)
        print("Camera started! Press 'q' to quit.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            text, annotated_frame = self.detect_signs(frame)
            
            # Display detected text on frame
            cv2.putText(annotated_frame, text, (10, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow('Sign Language Detection - Press Q to quit', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = SignLanguageDetector()
    detector.start_camera()