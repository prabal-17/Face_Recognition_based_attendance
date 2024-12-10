import os
import cv2
import uuid
import shutil
import numpy as np
import pandas as pd
import face_recognition
import streamlit as st
from datetime import datetime

# Defining constants and paths
VISITOR_DB = "visitor_database"
VISITOR_HISTORY = "visitor_history"
COLS_ENCODE = [f'feature_{i}' for i in range(128)]  # 128 dimensions for face encoding
COLS_INFO = ["Name"]  # Column for storing name of the visitor
ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png"]

# Ensure directories exist
if not os.path.exists(VISITOR_DB):
    os.makedirs(VISITOR_DB)

if not os.path.exists(VISITOR_HISTORY):
    os.makedirs(VISITOR_HISTORY)

# Define function to convert BGR to RGB
def BGR_to_RGB(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Initialize the visitor database
def initialize_data():
    if os.path.exists(VISITOR_DB):
        files = os.listdir(VISITOR_DB)
        data = []
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(VISITOR_DB, file)
                image = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(image)
                if len(encodings) > 0:
                    name = file.split('.')[0]  # Name is the file name without extension
                    data.append([name] + encodings[0].tolist())
        df = pd.DataFrame(data, columns=COLS_INFO + COLS_ENCODE)
        return df
    else:
        return pd.DataFrame(columns=COLS_INFO + COLS_ENCODE)

# Save the visitor data to the database
def add_data_db(new_data):
    df = initialize_data()
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(os.path.join(VISITOR_DB, 'visitor_data.csv'), index=False)

# Mark attendance
def attendance(visitor_id, name):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(VISITOR_HISTORY, "attendance.csv"), 'a') as file:
        file.write(f"{visitor_id},{name},{date_time}\n")

# View attendance history
def view_attendance():
    if os.path.exists(os.path.join(VISITOR_HISTORY, "attendance.csv")):
        df = pd.read_csv(os.path.join(VISITOR_HISTORY, "attendance.csv"))
        st.write(df)
    else:
        st.write("No attendance records found.")

# Sidebar content
st.sidebar.header("Face Recognition Attendance System")
st.sidebar.info("This webapp uses face recognition for visitor monitoring.")

# Clear data buttons
if st.sidebar.button('Clear All Data'):
    shutil.rmtree(VISITOR_DB, ignore_errors=True)
    os.mkdir(VISITOR_DB)
    shutil.rmtree(VISITOR_HISTORY, ignore_errors=True)
    os.mkdir(VISITOR_HISTORY)

# Main interface
def main():
    selected_menu = st.sidebar.radio("Choose an option", ['Visitor Validation', 'View Visitor History', 'Add to Database'])

    if selected_menu == 'Visitor Validation':
        visitor_id = uuid.uuid1()
        img_file_buffer = st.camera_input("Take a picture")

        if img_file_buffer is not None:
            bytes_data = img_file_buffer.getvalue()
            image_array = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            image_array_copy = image_array.copy()

            # Saving the captured image to history
            with open(os.path.join(VISITOR_HISTORY, f'{visitor_id}.jpg'), 'wb') as file:
                file.write(img_file_buffer.getbuffer())
                st.success('Image Saved Successfully!')

            # Detect faces in the loaded image
            face_locations = face_recognition.face_locations(image_array)
            encodings = face_recognition.face_encodings(image_array, face_locations)

            if len(encodings) > 0:
                # Draw rectangle around faces
                for idx, (top, right, bottom, left) in enumerate(face_locations):
                    cv2.rectangle(image_array, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(image_array, f"Face {idx}", (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                st.image(BGR_to_RGB(image_array), width=720)

                # Compare detected faces with the database
                df = initialize_data()
                if len(df) > 0:
                    similarities = []
                    for encoding in encodings:
                        distances = face_recognition.face_distance(df[COLS_ENCODE].values, encoding)
                        min_distance = min(distances)
                        if min_distance < 0.6:  # Similarity threshold
                            matching_row = df.loc[distances.argmin()]
                            similarities.append((matching_row['Name'], min_distance))

                    if similarities:
                        st.write("Matching Visitors:")
                        for name, similarity in similarities:
                            st.write(f"Name: {name}, Similarity: {round(1 - similarity, 2)}")
                            attendance(visitor_id, name)
                    else:
                        st.write("No match found. Marking as Unknown.")
                        attendance(visitor_id, 'Unknown')
            else:
                st.error("No face detected. Please try again.")
                
    elif selected_menu == 'View Visitor History':
        st.subheader("Visitor History")
        view_attendance()

    elif selected_menu == 'Add to Database':
        name = st.text_input('Enter Name')
        image_option = st.radio('Upload Image', ['Upload Image', 'Take a Picture'])

        if image_option == 'Upload Image':
            uploaded_file = st.file_uploader('Choose an image...', type=ALLOWED_IMAGE_TYPES)
            if uploaded_file is not None:
                image_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                image_array = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
                st.image(BGR_to_RGB(image_array), width=300)

        elif image_option == 'Take a Picture':
            img_file_buffer = st.camera_input("Take a picture")
            if img_file_buffer is not None:
                image_bytes = np.frombuffer(img_file_buffer.getvalue(), np.uint8)
                image_array = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
                st.image(BGR_to_RGB(image_array), width=300)

        if name and st.button('Save to Database') and image_option:
            if img_file_buffer is not None or uploaded_file is not None:
                face_locations = face_recognition.face_locations(image_array)
                encodings = face_recognition.face_encodings(image_array, face_locations)

                if len(encodings) > 0:
                    df_new = pd.DataFrame([encodings[0].tolist()], columns=COLS_ENCODE)
                    df_new[COLS_INFO] = name
                    add_data_db(df_new)
                    st.success(f"{name} added to the database.")
                else:
                    st.error("No face detected in the image.")
            else:
                st.error("Please upload or take a picture.")

if __name__ == "__main__":
    main()
