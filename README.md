
# Face Recognition Attendance System

This project implements a **Face Recognition Attendance System** using **OpenCV** and **Face Recognition** libraries in Python. It leverages **Streamlit** for a web-based interface, where users can upload or capture images, and the system will recognize and record visitor attendance.

## Features:
- **Visitor Validation**: Take a picture or upload an image to check if a visitor is already in the database. If a match is found, the visitor's name is displayed along with their recognition similarity.
- **Add to Database**: Add new visitors to the database by uploading their photo or taking a picture with your webcam.
- **Attendance Tracking**: Automatically records the time of attendance when a match is found or when a new visitor is added.
- **Visitor History**: View a table of all the visitors and their attendance history.

## Requirements

To run this project, you need the following Python libraries:
- **Streamlit**: A fast way to create custom web apps.
- **OpenCV**: For image processing and face detection.
- **Face Recognition**: For facial feature extraction and matching.
- **Pandas**: For data management and storing visitor information.
- **Numpy**: For handling arrays and image data.
- **UUID**: To generate unique IDs for visitors.

Install the required dependencies using `pip`:

```bash
pip install streamlit opencv-python face_recognition pandas numpy
```

## Project Structure

```plaintext
face_recognition_attendance/
│
├── streamlit_app.py          # Main application code (Streamlit app)
├── visitor_database/         # Folder to store images and face encodings of visitors
│   └── visitor_data.csv      # CSV file to store visitor data (name + face encodings)
│
├── visitor_history/          # Folder to store visitor attendance records
│   └── attendance.csv        # CSV file to store attendance logs
│
└── README.md                 # This README file
```

## How It Works

1. **Initialization**: The app initializes by reading existing visitor data and face encodings from the `visitor_database` directory.
2. **Adding New Visitors**: You can add a new visitor by uploading an image or taking a picture with your webcam. The face encodings are then extracted and stored in the `visitor_database`.
3. **Visitor Validation**: Once a picture is taken or uploaded, the system performs face recognition and checks if the face matches any of the stored visitor images. If a match is found, the system logs the attendance and displays the visitor's name.
4. **View Visitor History**: The app can display a table showing all the visitors and their attendance history (name, date, and time).

## Usage

1. **Launch the Streamlit App**:
   In your terminal, navigate to the project folder and run the following command:

   ```bash
   streamlit run streamlit_app.py
   ```

   This will start a local server and open the application in your browser.

2. **Add a New Visitor**:
   - Navigate to the "Add to Database" section.
   - Enter the visitor's name and upload an image or use your webcam to capture a picture of the visitor.
   - The system will extract the face encoding and save the visitor data in the `visitor_database`.

3. **Validate a Visitor**:
   - Navigate to the "Visitor Validation" section.
   - Capture or upload a picture of the visitor.
   - The system will match the face with the database and display the name of the recognized visitor if a match is found.
   - The visitor's attendance will be logged with the time and date.

4. **View Visitor History**:
   - Navigate to the "View Visitor History" section to see all recorded visitors' names along with the attendance times.

## Clear All Data
- If you want to clear all the visitor data and history, click the "Clear All Data" button in the sidebar.

## File Structure
- **visitor_database**: This folder contains images and encodings of visitors. It will be populated as visitors are added to the system.
- **visitor_history**: This folder stores the attendance logs, with each entry recording the visitor’s name and the date/time of attendance.

## Troubleshooting

- **No Face Detected**: Ensure that the image or video feed contains a clearly visible face. The system requires a clear view of the face for recognition.
- **Error in Adding New Visitor**: Make sure that the image or webcam feed contains a face, as the system relies on face recognition encodings.

## License

This project is open-source and free to use for educational and personal purposes. However, please ensure to give proper attribution if using or modifying the code.

---

Feel free to customize this file based on your project needs. The README file provides an overview of the system, installation steps, usage instructions, and how to troubleshoot common issues.