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
- **Automated Alerts**: Triggers alert notifications when collision risk is detected
- **Emergency Response Simulation**: Activates automated emergency protocols:
  - Automatic braking engagement
  - Hazard light activation
  - Emergency services notification
  - Incident recording
- **Visual Feedback**: Real-time visualization with risk scores and collision warnings

## 📋 System Architecture

### Core Components

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

### Basic Usage - Real-Time Detection with Webcam

```python
from collision_detection_system import CollisionDetectionSystem

# Initialize the system
collision_detector = CollisionDetectionSystem()

# Run real-time detection (0 = default webcam)
collision_detector.run_real_time_detection(0)
```

### Using Video File

```python
collision_detector = CollisionDetectionSystem()
collision_detector.run_real_time_detection("path/to/video.mp4")
```

### Training with Custom Data

```python
import numpy as np

# Prepare training data
X_train = np.array([...])  # Feature vectors
y_train = np.array([...])  # Labels (0: no collision, 1: collision risk)

collision_detector = CollisionDetectionSystem()
collision_detector.train_model(X_train, y_train)
collision_detector.save_model("trained_model.pkl")
```

### Load Pre-trained Model

```python
collision_detector = CollisionDetectionSystem(model_path="trained_model.pkl")
collision_detector.run_real_time_detection(0)
```

## 🎮 Keyboard Controls

- Press **'q'** to quit the real-time detection loop

## 📊 Key Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `alert_threshold` | 0.7 | Risk score threshold for triggering alerts |
| `n_estimators` | 100 | Number of trees in Random Forest |
| `random_state` | 42 | Random seed for reproducibility |
| `Canny edges` | (100, 200) | Edge detection thresholds |

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

## 🚨 Alert System

When collision risk is detected:
- Displays visual warning with red border and "COLLISION RISK DETECTED!" message
- Logs alert with timestamp and risk score
- Triggers emergency response simulation in separate thread
- Email alerts can be configured (SMTP setup required)

## 📈 Emergency Response Protocol

The system simulates the following emergency actions:

```
[EMERGENCY RESPONSE ACTIVATED]
- Automatic braking engaged
- Hazard lights activated
- Emergency services notified
- Recording incident for analysis
```

## 🛠️ Advanced Usage

### Adjusting Alert Threshold

```python
collision_detector = CollisionDetectionSystem()
collision_detector.alert_threshold = 0.65  # Lower threshold = more sensitive
```

### Custom Video Source

```python
# Use IP camera
collision_detector.run_real_time_detection("http://camera-ip:port/stream")

# Use RTSP stream
collision_detector.run_real_time_detection("rtsp://stream-url")
```

## 📝 Model Training Workflow

1. **Data Collection**: Gather labeled video frames
2. **Feature Extraction**: Extract 7-dimensional feature vectors
3. **Data Normalization**: Scale features using StandardScaler
4. **Model Training**: Train Random Forest on labeled data
5. **Model Persistence**: Save trained model for deployment
6. **Real-Time Inference**: Load model for real-time detection

## 🔐 Safety Considerations

- **Threshold Tuning**: Adjust `alert_threshold` based on false positive tolerance
- **Hardware Requirements**: Real-time processing requires decent GPU/CPU
- **Video Input Quality**: Better video quality improves detection accuracy
- **Model Retraining**: Periodically retrain with diverse driving scenarios

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Camera not detected | Verify camera is connected, try `video_source=0` |
| Slow performance | Reduce video resolution, use GPU acceleration |
| High false positives | Increase `alert_threshold` value |
| Model not found | Check model path and file exists |

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
