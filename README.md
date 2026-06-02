# AI-Driven Collision Detection and Autonomous Emergency Response System for Automobiles

Built an AI-based collision detection system using **Python**, **Machine Learning**, **Computer Vision**, and **OpenCV**. The system detects possible collision risks in real-time, sends automated alerts, and simulates emergency responses to improve vehicle safety and faster decision-making.

## 🎯 Features

- **Real-Time Collision Detection**: Processes video streams to detect collision risks in real-time
- **Computer Vision Analysis**: 
  - Canny edge detection
  - Contour and object detection
  - Optical flow for motion detection
  - Histogram analysis
- **Machine Learning Classification**: Random Forest classifier trained on extracted visual features
- **Severity-Based Emergency Response**: 
  - **MAJOR**: Driver + Family + Hospital (Ambulance) + Police + Logging
  - **MODERATE**: Driver + Family + Police + Logging
  - **MINOR**: Driver + Family + Logging
  - **NORMAL**: System monitoring only
- **Automated Alerts**: Triggers alert notifications when collision risk is detected
- **Emergency Services Integration**: Contacts hospital, police, and family members based on severity
- **Accident Logging**: Comprehensive logging with JSON export
- **Visual Feedback**: Real-time visualization with risk scores and collision warnings

## 📋 System Architecture

### Core Components

#### 1. **Collision Detector** (`collision_detector.py`)
- Video-based collision detection using OpenCV
- Sensor-based collision detection (accelerometer/IMU data)
- Severity classification based on impact force and deceleration
- Integration with emergency response system

#### 2. **Emergency Response System** (`emergency_response.py`)
- Handles collision severity levels (NORMAL, MINOR, MODERATE, MAJOR)
- Manages emergency contacts (family members)
- Sends notifications to:
  - **Driver**: Real-time alerts with severity information
  - **Family Members**: SMS and Email notifications
  - **Hospital**: Emergency ambulance requests (MAJOR only)
  - **Police**: Accident notifications and inspection requests (MODERATE & MAJOR)
- Maintains detailed accident logs in JSON format

#### 3. **Example Usage** (`example_usage.py`)
- Demonstrates all 4 collision severity levels
- Shows emergency contact registration
- Illustrates accident logging and history tracking

### Legacy Components

1. **Feature Extraction** (`extract_features_from_frame`):
   - Edge density (Canny edge detection)
   - Contour count and largest object area
   - Object aspect ratio
   - Histogram statistics
   - Optical flow magnitude

2. **Collision Risk Detection** (`detect_collision_risk`):
   - Processes extracted features through ML model
   - Generates risk score (0-1 probability)
   - Determines collision risk based on threshold (default: 0.7)

3. **Alert System** (`send_alert`):
   - Generates timestamped alert messages
   - Triggers emergency response simulation
   - Email alert capability (configurable)

4. **Real-Time Processing** (`run_real_time_detection`):
   - Captures video from camera or video file
   - Detects collisions in continuous loop
   - Multi-threaded alert handling
   - Visual display with annotated detections

## 🚀 Installation

### Prerequisites
- Python 3.7+
- OpenCV
- scikit-learn
- NumPy

### Setup

```bash
# Clone the repository
git clone https://github.com/SwaroopMR/AI-Driven-Collision-Detection-and-Autonomous-Emergency-Response-System-for-Automobiles.git
cd AI-Driven-Collision-Detection-and-Autonomous-Emergency-Response-System-for-Automobiles

# Install dependencies
pip install opencv-python scikit-learn numpy
```

## 💻 Usage

### Emergency Response System

#### 1. Initialize the System

```python
from emergency_response import (
    EmergencyResponseSystem,
    CollisionSeverity,
    Location,
    EmergencyContact
)

# Create system instance
vehicle_id = "VEHICLE_ABC_12345"
driver_info = {
    "name": "John Doe",
    "phone": "+1-555-0101",
    "email": "john.doe@example.com",
    "license": "DL12345678"
}

system = EmergencyResponseSystem(vehicle_id, driver_info)
```

#### 2. Register Emergency Contacts

```python
# Add family members
family_contact = EmergencyContact(
    name="Jane Doe",
    phone="+1-555-0102",
    email="jane.doe@example.com",
    relationship="Spouse"
)
system.register_emergency_contact(family_contact)
```

#### 3. Handle Collision Events

```python
from emergency_response import Location

location = Location(
    latitude=40.7128,
    longitude=-74.0060,
    address="5th Avenue and 34th Street, Manhattan, NY"
)

collision_data = {
    "impact_force": 85.5,
    "vehicle_speed": 65,
    "deceleration": 0.8,
    "confidence": 0.98
}

# Handle major collision - triggers FULL emergency response
result = system.handle_collision(
    CollisionSeverity.MAJOR,
    location,
    collision_data
)
```

### Collision Detection Integration

#### Using Video-Based Detection

```python
from collision_detector import CollisionDetector
from emergency_response import EmergencyResponseSystem

system = EmergencyResponseSystem(vehicle_id, driver_info)
detector = CollisionDetector(system)

# Detect from video
result = detector.detect_collision_from_video("path/to/video.mp4")

if result["collision_detected"]:
    detector.trigger_emergency_response(result, location)
```

#### Using Sensor-Based Detection

```python
# Detect from sensor data (accelerometer, gyroscope, etc.)
sensor_data = {
    "acceleration_x": 9.2,  # g-force
    "acceleration_y": 0.5,
    "acceleration_z": -0.1,
    "velocity": 65,  # mph
    "impact_detection": True,
    "confidence": 0.95
}

result = detector.detect_collision_from_sensors(sensor_data)
```

### Run Full Example

```bash
python example_usage.py
```

This demonstrates all 4 collision severity levels with their respective emergency responses.

## 🚨 Emergency Response Logic

| Severity | Driver Alert | Family Members | Hospital & Ambulance | Police | Accident Log |
|----------|:-----------:|:-------------:|:-------------------:|:------:|:-----------:|
| **MAJOR** | ✅ | ✅ | ✅ CRITICAL | ✅ | ✅ |
| **MODERATE** | ✅ | ✅ | ❌ | ✅ | ✅ |
| **MINOR** | ✅ | ✅ | ❌ | ❌ | ✅ |
| **NORMAL** | ❌ | ❌ | ❌ | ❌ | Monitoring |

### Response Details

**MAJOR Collision**:
- Driver receives CRITICAL alert
- All family members notified via SMS/Email
- Hospital emergency ambulance requested
- Police notified for accident inspection
- Full accident details logged

**MODERATE Collision**:
- Driver receives alert
- Family members notified
- Police notified for inspection
- Accident logged (NO hospital/ambulance)

**MINOR Collision**:
- Driver receives alert
- Family members notified
- Accident logged (NO police/hospital)

**NORMAL (No Collision)**:
- System continues monitoring
- No emergency response triggered

## 🎮 Keyboard Controls

- Press **'q'** to quit the real-time detection loop

## 📊 Key Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `alert_threshold` | 0.7 | Risk score threshold for triggering alerts |
| `n_estimators` | 100 | Number of trees in Random Forest |
| `random_state` | 42 | Random seed for reproducibility |
| `Canny edges` | (100, 200) | Edge detection thresholds |
| `major_impact_force` | 60 | kN threshold for MAJOR severity |
| `moderate_impact_force` | 30 | kN threshold for MODERATE severity |
| `minor_impact_force` | 10 | kN threshold for MINOR severity |

## 🔍 Feature Vector Details

The system extracts 7 features from each frame:

1. **Edge Density**: Ratio of edge pixels to total pixels (Canny edge detection)
2. **Contour Count**: Number of detected contours in frame
3. **Largest Object Area**: Area of the largest detected object
4. **Object Aspect Ratio**: Width-to-height ratio of largest object
5. **Histogram Mean**: Mean brightness value of frame
6. **Histogram Std**: Standard deviation of brightness distribution
7. **Optical Flow Magnitude**: Average motion magnitude between frames

## 🤖 Machine Learning Model

- **Algorithm**: Random Forest Classifier
- **Trees**: 100 decision trees
- **Feature Scaling**: StandardScaler normalization
- **Predictions**: Binary classification + probability scores
- **Serialization**: Pickle format for model persistence

## 📈 Emergency Response Protocol

The system follows this decision tree:

```
Collision Detected?
├─ YES ─→ Classify Severity
│         ├─ MAJOR ──→ Driver + Family + Hospital + Police + Log
│         ├─ MODERATE ──→ Driver + Family + Police + Log
│         ├─ MINOR ──→ Driver + Family + Log
│         └─ NORMAL (shouldn't reach here)
└─ NO ──→ Continue Monitoring
```

## 📝 Accident Logging

The system maintains a comprehensive accident history:

```python
# Get accident history
history = system.get_accident_history()

# Export accident log to JSON
system.export_accident_log("accident_log.json")
```

## 🛠️ Advanced Usage

### Adjusting Severity Thresholds

```python
detector = CollisionDetector(system)
detector.severity_thresholds = {
    "major": {"impact_force": 70, "deceleration": 0.7},
    "moderate": {"impact_force": 35, "deceleration": 0.35},
    "minor": {"impact_force": 12, "deceleration": 0.12}
}
```

### Custom Video Source

```python
# Use IP camera
result = detector.detect_collision_from_video("http://camera-ip:port/stream")

# Use RTSP stream
result = detector.detect_collision_from_video("rtsp://stream-url")
```

### Collision History Analysis

```python
history = system.get_accident_history()
for entry in history:
    print(f"Severity: {entry['severity']}")
    print(f"Location: {entry['location']['address']}")
    print(f"Responses: {', '.join(entry['responses_triggered'])}")
```

## 🔐 Safety Considerations

- **Threshold Tuning**: Adjust severity thresholds based on vehicle type and usage
- **Hardware Requirements**: Real-time processing requires decent GPU/CPU
- **Video Input Quality**: Better video quality improves detection accuracy
- **Model Retraining**: Periodically retrain with diverse driving scenarios
- **Integration Testing**: Thoroughly test emergency contact notifications
- **Compliance**: Ensure compliance with local regulations for emergency notifications

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Camera not detected | Verify camera is connected, try `video_source=0` |
| Slow performance | Reduce video resolution, use GPU acceleration |
| High false positives | Increase `alert_threshold` value |
| Model not found | Check model path and file exists |
| Emergency contacts not notifying | Verify phone numbers and email addresses are valid |
| Sensor data not detected | Check sensor data format matches required fields |

## 📚 Dependencies

```
opencv-python>=4.5.0
scikit-learn>=0.24.0
numpy>=1.19.0
```

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**SwaroopMR**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve the system.

## 📞 Support

For issues, questions, or suggestions, please open an issue in the GitHub repository.

---

**Note**: This system is designed for educational and research purposes. For production deployment in vehicles, additional safety testing and regulatory compliance is required.
