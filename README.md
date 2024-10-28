# Hand-Gesture-Controlled Gamepad for Car Simulation

This project uses computer vision and hand gestures to control a gamepad, simulating a car's movement. The program captures hand movements via a camera, calculates slope and distance between hands, and uses these metrics to control acceleration, deceleration, and steering.

## Requirements
To install the required packages, run:
```bash
pip install -r requirements.txt
```

## Usage
Run the main code file to start hand tracking and gamepad control.

Press `q` to quit the application.

### Video Demo
Here is the Video Demonstration

https://github.com/user-attachments/assets/3bf0b92c-110c-4ae5-959a-5306846c9c8b

## Libraries Used
- **OpenCV**: Used for capturing video frames and displaying outputs.
- **Mediapipe**: For hand landmark detection and tracking.
- **VGamepad**: For virtual gamepad control.

## Explanation of Functions
- **calculate_slope**: Calculates the slope between two detected hand landmarks.
- **calculate_distance**: Measures the distance between two hand landmarks.
- **control_car**: Controls the car's movement based on slope and distance, adjusting the virtual gamepad’s triggers and joystick.

## License
This project is licensed under the MIT License.
