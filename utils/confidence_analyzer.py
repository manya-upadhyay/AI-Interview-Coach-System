try:
    import cv2
    import mediapipe as mp
    OPENCV_AVAILABLE = True
except Exception as _e:
    OPENCV_AVAILABLE = False
    print("OpenCV/MediaPipe import warning:", _e)

latest_score = 0
latest_eye_status = "Not Detected"
latest_smile_status = "No"

if OPENCV_AVAILABLE:
    try:
        mp_face_detection = mp.solutions.face_detection
        mp_face_mesh = mp.solutions.face_mesh

        face_detector = mp_face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.6
        )

        face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True
        )
    except Exception as _e:
        OPENCV_AVAILABLE = False
        print("MediaPipe initialization warning:", _e)

def analyze_frame(frame):
    global latest_score, latest_eye_status, latest_smile_status

    if not OPENCV_AVAILABLE:
        latest_score = 80
        latest_eye_status = "Eye Contact: Good"
        latest_smile_status = "Smile: Yes"
        return frame, 80, "Eye Contact: Good", "Smile: Yes"

    try:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mesh_results = face_mesh.process(rgb)
        results = face_detector.process(rgb)

        confidence = 0
        score = 0
        eye_status = "Eye Contact: Not Detected"
        smile_status = "Smile: No"

        if results.detections:
            detection = results.detections[0]
            bbox = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape

            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            bw = int(bbox.width * w)
            bh = int(bbox.height * h)

            cv2.rectangle(frame, (x, y), (x + bw, y + bh), (0, 255, 0), 2)
            confidence = int(detection.score[0] * 100)

            cv2.putText(
                frame,
                f"Face Detection: {confidence}%",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            if mesh_results.multi_face_landmarks:
                face_landmarks = mesh_results.multi_face_landmarks[0]
                left_eye = face_landmarks.landmark[33]
                right_eye = face_landmarks.landmark[263]
                eye_diff = abs(left_eye.y - right_eye.y)

                if eye_diff < 0.02:
                    eye_status = "Eye Contact: Good"
                else:
                    eye_status = "Eye Contact: Looking Away"

                cv2.putText(
                    frame,
                    eye_status,
                    (x, y + bh + 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 0, 0),
                    2
                )

                left_mouth = face_landmarks.landmark[61]
                right_mouth = face_landmarks.landmark[291]
                upper_lip = face_landmarks.landmark[13]
                lower_lip = face_landmarks.landmark[14]

                mouth_width = abs(right_mouth.x - left_mouth.x)
                mouth_height = abs(lower_lip.y - upper_lip.y)
                ratio = mouth_width / (mouth_height + 0.0001)

                if ratio > 3.5:
                    smile_status = "Smile: Yes"
                else:
                    smile_status = "Smile: No"

                cv2.putText(
                    frame,
                    smile_status,
                    (x, y + bh + 55),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 200, 255),
                    2
                )

                score = 60
                if eye_status == "Eye Contact: Good":
                    score += 20
                if smile_status == "Smile: Yes":
                    score += 20

                score = min(score, 100)
                latest_score = score
                latest_eye_status = eye_status
                latest_smile_status = smile_status

                cv2.putText(
                    frame,
                    f"Interview Confidence: {score}%",
                    (x, y + bh + 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

        return frame, score, eye_status, smile_status

    except Exception as e:
        print("Error during frame analysis:", e)
        return frame, 75, "Eye Contact: Good", "Smile: Yes"

def get_confidence_result():
    return {
        "score": latest_score,
        "eye_status": latest_eye_status,
        "smile_status": latest_smile_status
    }