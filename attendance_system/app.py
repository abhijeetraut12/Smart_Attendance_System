from flask import Flask, jsonify, render_template, Response, send_file
import face_recognition
import cv2
import numpy as np
import csv
import smtplib  # For sending email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import winsound

app = Flask(__name__)

# Sound function to play a beep
def play_sound():
    winsound.Beep(700, 500)

# Function to send email notifications
def send_email(name, time):
    sender_email = "abhijeetrautproject@gmail.com"
    receiver_email = "rautabhi12103@gmail.com"
    password = "vucwkvhrozvyontu" 

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Attendance Notification: {name}"

    body = f"{name} was detected at {time}."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print(f"Email sent for {name} at {time}")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()

# Ensure the 'logs' folder exists for storing CSV files
if not os.path.exists('logs'):
    os.makedirs('logs')

# Function to create the CSV log file
def create_csv_log():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    file_path = os.path.join('logs', current_date + '.csv')
    f = open(file_path, 'w+', newline='')
    lnwriter = csv.writer(f)
    lnwriter.writerow(["Name", "First Detected Time", "Detection Count"])
    return f, lnwriter

# Create the CSV log at the start
f, lnwriter = create_csv_log()

# Function to log attendance in the CSV file
def log_attendance(name, time, count):
    lnwriter.writerow([name, time, count])
    f.flush()  # Ensure data is written to the file
    print(f"Logged {name} at {time} with count {count}")

# Load known faces and encodings
def load_known_faces():
    abhay_image = face_recognition.load_image_file(os.path.join("photos", "abhay.jpg")
    abhay_encoding = face_recognition.face_encodings(abhay_image)[0]

    deva_image = face_recognition.load_image_file(os.path.join("photos", "deva.png")
    deva_encoding = face_recognition.face_encodings(deva_image)[0]

    mohan_image = face_recognition.load_image_file(os.path.join("photos", "mohan.png")
    mohan_encoding = face_recognition.face_encodings(mohan_image)[0]

    shubham_image = face_recognition.load_image_file(os.path.join("photos", "shubham.png")
    shubham_encoding = face_recognition.face_encodings(shubham_image)[0]

    vinit_image = face_recognition.load_image_file(os.path.join("photos", "vinit.png")
    vinit_encoding = face_recognition.face_encodings(vinit_image)[0]

    omd_image = face_recognition.load_image_file(os.path.join("photos", "omd.png")
    omd_encoding = face_recognition.face_encodings(omd_image)[0]

    chetan_image = face_recognition.load_image_file(os.path.join("photos", "chetan.png")
    chetan_encoding = face_recognition.face_encodings(chetan_image)[0]

    kushal_image = face_recognition.load_image_file(os.path.join("photos", "kushal.png")
    kushal_encoding = face_recognition.face_encodings(kushal_image)[0]

    abhijeet_image = face_recognition.load_image_file(os.path.join("photos", "abhijeet.png")
    abhijeet_encoding = face_recognition.face_encodings(abhijeet_image)[0]

    om_image = face_recognition.load_image_file(os.path.join("photos", "om.png")
    om_encoding = face_recognition.face_encodings(om_image)[0]

    sumit_image = face_recognition.load_image_file(os.path.join("photos", "sumit.png")
    sumit_encoding = face_recognition.face_encodings(sumit_image)[0]

    known_face_encodings = [
        abhay_encoding, deva_encoding, mohan_encoding, shubham_encoding, vinit_encoding, 
        omd_encoding, chetan_encoding, kushal_encoding, 
        abhijeet_encoding, om_encoding, sumit_encoding
    ]

    known_face_names = [
        "Abhay Mendhe", "Devanand Salunke", "Mohan Chaple", "Shubham Sir", "Vinit Wandile", 
        "Om Deshmukh", "Chetan Kuyate", "Kushal Borkar", 
        "Abhijeet Raut", "Om Khandekar", "Sumit Kshirsagar"
    ]
    return known_face_encodings, known_face_names

# Load the known faces and encodings at startup
known_face_encodings, known_face_names = load_known_faces()

# Attendance log and detection count
attendance_log = {}
detection_count = {}
students_not_detected = known_face_names.copy()

# Route to capture attendance and stream video with face detection
def gen_frames():
    video_capture = cv2.VideoCapture(0)
    
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            # Resize frame for faster processing and face detection
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

                    if name not in attendance_log:
                        attendance_log[name] = current_time
                        detection_count[name] = 1
                        play_sound()
                        send_email(name, current_time)
                        log_attendance(name, current_time, detection_count[name])

                        if name in students_not_detected:
                            students_not_detected.remove(name)

                    face_names.append(name) 

            # Draw face boxes and names on the frame
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Encode the frame into JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route for real-time attendance summary
@app.route('/api/summary', methods=['GET'])
def attendance_summary():
    present_students = [{"name": name, "time": time} for name, time in attendance_log.items()]
    absent_students = students_not_detected  # List of students who are not detected yet

    return jsonify({
        "present_students": present_students,
        "absent_students": absent_students
    })


@app.route('/download_attendance')
def download_attendance():
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join("logs", current_date + ".csv")
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "No attendance file available for today.", 404
    
@app.after_request
def cleanup(response):
    # Perform any cleanup tasks
    return response


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


# Home route (serving HTML frontend)
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)


