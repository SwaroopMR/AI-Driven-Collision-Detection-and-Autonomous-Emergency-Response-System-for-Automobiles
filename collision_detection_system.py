import cv2
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle
import threading
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

class CollisionDetectionSystem:
    """
    AI-Driven Collision Detection and Emergency Response System
    Integrates Computer Vision, ML, and OpenCV for real-time collision detection
    """
    
    def __init__(self, model_path=None):
        """Initialize the collision detection system"""
        self.cascade_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.model = self._load_or_create_model(model_path)
        self.scaler = StandardScaler()
        self.cap = None
        self.alert_threshold = 0.7
        
    def _load_or_create_model(self, model_path):
        """Load pre-trained model or create a new one"""
        if model_path and os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                return pickle.load(f)
        else:
            # Create a Random Forest classifier for collision risk classification
            return RandomForestClassifier(n_estimators=100, random_state=42)
    
    def extract_features_from_frame(self, frame):
        """
        Extract computer vision features from a frame
        Features: edge detection, motion detection, object size, distance metrics
        """
        features = {}
        
        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Canny edge detection
        edges = cv2.Canny(gray, 100, 200)
        features['edge_density'] = np.sum(edges) / (frame.shape[0] * frame.shape[1])
        
        # Contour detection for object identification
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        features['contour_count'] = len(contours)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            features['largest_object_area'] = cv2.contourArea(largest_contour)
            features['object_aspect_ratio'] = self._get_aspect_ratio(largest_contour)
        else:
            features['largest_object_area'] = 0
            features['object_aspect_ratio'] = 0
        
        # Histogram analysis for object detection
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        features['hist_mean'] = np.mean(hist)
        features['hist_std'] = np.std(hist)
        
        # Optical flow for motion detection
        if hasattr(self, 'prev_gray'):
            flow = cv2.calcOpticalFlowFarneback(
                self.prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
            )
            mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            features['optical_flow_magnitude'] = np.mean(mag)
        
        self.prev_gray = gray.copy()
        
        return features
    
    def _get_aspect_ratio(self, contour):
        """Calculate aspect ratio of a contour"""
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        width = np.linalg.norm(box[0] - box[1])
        height = np.linalg.norm(box[1] - box[2])
        return width / (height + 1e-5)
    
    def detect_collision_risk(self, frame):
        """
        Detect collision risk using ML and Computer Vision
        Returns risk score and decision
        """
        features = self.extract_features_from_frame(frame)
        
        # Convert features dict to numpy array for ML model
        feature_vector = np.array([
            features.get('edge_density', 0),
            features.get('contour_count', 0),
            features.get('largest_object_area', 0),
            features.get('object_aspect_ratio', 0),
            features.get('hist_mean', 0),
            features.get('hist_std', 0),
            features.get('optical_flow_magnitude', 0)
        ]).reshape(1, -1)
        
        # Scale features
        feature_vector_scaled = self.scaler.fit_transform(feature_vector)
        
        # Predict collision risk using ML model
        risk_score = self.model.predict_proba(feature_vector_scaled)[0][1]
        is_collision_risk = risk_score > self.alert_threshold
        
        return risk_score, is_collision_risk
    
    def visualize_detections(self, frame, risk_score, is_collision_risk):
        """
        Visualize detection results on frame with OpenCV
        """
        frame_copy = frame.copy()
        
        # Draw detection boxes
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            cv2.drawContours(frame_copy, contours, -1, (0, 255, 0), 2)
        
        # Add risk score text
        risk_color = (0, 0, 255) if is_collision_risk else (0, 255, 0)
        risk_text = f"Risk: {risk_score:.2f}"
        cv2.putText(
            frame_copy, risk_text, (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, risk_color, 2
        )
        
        if is_collision_risk:
            cv2.rectangle(frame_copy, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 3)
            cv2.putText(
                frame_copy, "COLLISION RISK DETECTED!", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3
            )
        
        return frame_copy
    
    def send_alert(self, risk_score):
        """Send automated alert for collision detection"""
        alert_message = f"""
        COLLISION ALERT - {datetime.now()}
        Risk Score: {risk_score:.2f}
        
        Initiating emergency response:
        - Engaging automatic braking
        - Activating hazard lights
        - Notifying emergency services
        """
        
        print(alert_message)
        
        # Send email alert (configure with actual email settings)
        # self._send_email_alert(alert_message)
        
        # Trigger emergency response simulation
        self._emergency_response()
    
    def _emergency_response(self):
        """Simulate emergency response"""
        print("[EMERGENCY RESPONSE ACTIVATED]")
        print("- Automatic braking engaged")
        print("- Hazard lights activated")
        print("- Emergency services notified")
        print("- Recording incident for analysis")
    
    def run_real_time_detection(self, video_source=0):
        """Run real-time collision detection from video source"""
        self.cap = cv2.VideoCapture(video_source)
        self.prev_gray = None
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Detect collision risk
            risk_score, is_collision_risk = self.detect_collision_risk(frame)
            
            # Send alert if collision detected
            if is_collision_risk:
                threading.Thread(target=self.send_alert, args=(risk_score,)).start()
            
            # Visualize detections
            output_frame = self.visualize_detections(frame, risk_score, is_collision_risk)
            
            # Display
            cv2.imshow('Collision Detection System', output_frame)
            
            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
    
    def train_model(self, X_train, y_train):
        """Train the ML model with labeled data"""
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        print("Model trained successfully")
    
    def save_model(self, path):
        """Save the trained model"""
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {path}")


# Example usage
if __name__ == "__main__":
    # Initialize the system
    collision_detector = CollisionDetectionSystem()
    
    # Run real-time detection (use 0 for webcam, or provide video file path)
    collision_detector.run_real_time_detection(0)
