"""
Collision Detection Module
Integrates with ML/CV model to detect collisions and classify severity
"""

import cv2
import numpy as np
from typing import Tuple, Dict, Any, Optional
from enum import Enum
from emergency_response import CollisionSeverity, Location, EmergencyResponseSystem


class CollisionDetector:
    """
    Detects collisions using computer vision and sensor data
    Classifies severity and triggers emergency responses
    """
    
    def __init__(self, emergency_system: EmergencyResponseSystem):
        """
        Initialize collision detector with emergency response system
        
        Args:
            emergency_system: EmergencyResponseSystem instance
        """
        self.emergency_system = emergency_system
        self.frame_buffer = []
        self.collision_threshold = 0.7
        
        # Severity thresholds (can be tuned based on testing)
        self.severity_thresholds = {
            "major": {"impact_force": 60, "deceleration": 0.6},
            "moderate": {"impact_force": 30, "deceleration": 0.3},
            "minor": {"impact_force": 10, "deceleration": 0.1}
        }
    
    def detect_collision_from_video(self, video_path: str) -> Dict[str, Any]:
        """
        Detect collision from video stream
        
        Args:
            video_path: Path to video file or camera index
            
        Returns:
            Dictionary containing detection results
        """
        cap = cv2.VideoCapture(video_path)
        collision_detected = False
        severity = CollisionSeverity.NORMAL
        collision_data = {}
        
        frame_count = 0
        max_frames = 300  # Process up to 300 frames
        
        print(f"🎥 Processing video: {video_path}")
        
        while cap.isOpened() and frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Preprocess frame
            processed_frame = self._preprocess_frame(frame)
            
            # Detect potential collisions
            detection_result = self._detect_collision_in_frame(processed_frame)
            
            if detection_result["collision_detected"]:
                collision_detected = True
                severity, collision_data = self._classify_collision_severity(detection_result)
                print(f"✓ Collision detected with severity: {severity.value}")
                break
            
            frame_count += 1
        
        cap.release()
        
        return {
            "collision_detected": collision_detected,
            "severity": severity,
            "collision_data": collision_data,
            "frames_processed": frame_count
        }
    
    def detect_collision_from_sensors(self, sensor_data: Dict[str, float]) -> Dict[str, Any]:
        """
        Detect collision from sensor data (accelerometer, gyroscope, etc.)
        
        Args:
            sensor_data: Dictionary with sensor readings
                - acceleration_x, acceleration_y, acceleration_z (g-force)
                - velocity (mph)
                - impact_detection (bool)
                
        Returns:
            Dictionary containing detection results
        """
        collision_detected = sensor_data.get("impact_detection", False)
        severity = CollisionSeverity.NORMAL
        collision_data = {}
        
        if collision_detected:
            # Calculate deceleration magnitude
            accel_x = sensor_data.get("acceleration_x", 0)
            accel_y = sensor_data.get("acceleration_y", 0)
            accel_z = sensor_data.get("acceleration_z", 0)
            
            deceleration = np.sqrt(accel_x**2 + accel_y**2 + accel_z**2)
            velocity = sensor_data.get("velocity", 0)
            
            # Estimate impact force (simplified)
            impact_force = deceleration * velocity * 10  # Calibration factor
            
            collision_data = {
                "impact_force": impact_force,
                "vehicle_speed": velocity,
                "deceleration": deceleration,
                "acceleration_vector": {
                    "x": accel_x,
                    "y": accel_y,
                    "z": accel_z
                },
                "confidence": sensor_data.get("confidence", 0.8)
            }
            
            severity = self._classify_severity_from_sensors(collision_data)
        
        return {
            "collision_detected": collision_detected,
            "severity": severity,
            "collision_data": collision_data
        }
    
    def _preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Preprocess video frame for collision detection
        
        Args:
            frame: Input frame from video
            
        Returns:
            Processed frame
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply histogram equalization for better contrast
        equalized = cv2.equalizeHist(blurred)
        
        return equalized
    
    def _detect_collision_in_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Detect collision indicators in a single frame
        
        Args:
            frame: Preprocessed frame
            
        Returns:
            Detection results
        """
        # Store frame for analysis
        self.frame_buffer.append(frame)
        keep_buffer_size = 5
        if len(self.frame_buffer) > keep_buffer_size:
            self.frame_buffer.pop(0)
        
        # Detect edges
        edges = cv2.Canny(frame, 100, 200)
        
        # Find contours (potential objects)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Analyze motion and structural changes
        collision_score = 0
        
        if len(self.frame_buffer) > 1:
            # Frame difference analysis
            frame_diff = cv2.absdiff(self.frame_buffer[-1], self.frame_buffer[-2])
            motion_pixels = np.sum(frame_diff > 30)
            
            # If significant motion detected, increase collision score
            if motion_pixels > 5000:
                collision_score += 0.3
        
        # Check for significant contours (potential impact)
        large_contours = [c for c in contours if cv2.contourArea(c) > 500]
        if len(large_contours) > 3:
            collision_score += 0.4
        
        # Edge density analysis
        edge_density = np.sum(edges > 0) / (frame.shape[0] * frame.shape[1])
        if edge_density > 0.3:
            collision_score += 0.3
        
        return {
            "collision_detected": collision_score >= self.collision_threshold,
            "collision_score": collision_score,
            "edge_count": len(contours),
            "edge_density": edge_density
        }
    
    def _classify_collision_severity(self, detection_result: Dict[str, Any]) -> Tuple[CollisionSeverity, Dict[str, Any]]:
        """
        Classify collision severity from detection result
        
        Args:
            detection_result: Detection result dictionary
            
        Returns:
            Tuple of (severity level, collision data)
        """
        collision_score = detection_result.get("collision_score", 0)
        
        # Collision data (mock values for demonstration)
        collision_data = {
            "impact_force": collision_score * 100,
            "vehicle_speed": 45,
            "deceleration": collision_score * 0.8,
            "confidence": collision_score
        }
        
        if collision_score >= 0.85:
            severity = CollisionSeverity.MAJOR
        elif collision_score >= 0.70:
            severity = CollisionSeverity.MODERATE
        elif collision_score >= 0.50:
            severity = CollisionSeverity.MINOR
        else:
            severity = CollisionSeverity.NORMAL
        
        return severity, collision_data
    
    def _classify_severity_from_sensors(self, collision_data: Dict[str, float]) -> CollisionSeverity:
        """
        Classify collision severity from sensor data
        
        Args:
            collision_data: Sensor collision data
            
        Returns:
            Collision severity level
        """
        impact_force = collision_data.get("impact_force", 0)
        deceleration = collision_data.get("deceleration", 0)
        
        # Check against thresholds
        if impact_force >= self.severity_thresholds["major"]["impact_force"] or \
           deceleration >= self.severity_thresholds["major"]["deceleration"]:
            return CollisionSeverity.MAJOR
        
        elif impact_force >= self.severity_thresholds["moderate"]["impact_force"] or \
             deceleration >= self.severity_thresholds["moderate"]["deceleration"]:
            return CollisionSeverity.MODERATE
        
        elif impact_force >= self.severity_thresholds["minor"]["impact_force"] or \
             deceleration >= self.severity_thresholds["minor"]["deceleration"]:
            return CollisionSeverity.MINOR
        
        else:
            return CollisionSeverity.NORMAL
    
    def trigger_emergency_response(self, detection_result: Dict[str, Any], 
                                  location: Location) -> Dict[str, Any]:
        """
        Trigger emergency response based on detection
        
        Args:
            detection_result: Detection result from detect_collision methods
            location: Vehicle location
            
        Returns:
            Emergency response result
        """
        if not detection_result.get("collision_detected"):
            return {"status": "no_collision", "action": "monitoring"}
        
        severity = detection_result.get("severity", CollisionSeverity.NORMAL)
        collision_data = detection_result.get("collision_data", {})
        
        # Trigger emergency response system
        response = self.emergency_system.handle_collision(
            severity=severity,
            location=location,
            collision_data=collision_data
        )
        
        return response
