import cv2
from ultralytics import YOLO
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# --------------------------
# Email function
# --------------------------
def send_alert_email(count):
    sender = "jhanvisharma.0021@gmail.com"
    app_password = "jrqsfiiivbjlzvhe"
    receiver = "jhanvisharma140@gmail.com"

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "⚠ People Count Alert"

    body = f"Alert! Current people count = {count}, which exceeds the threshold."
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, app_password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        print("Alert Email Sent!")
    except Exception as e:
        print("Error sending email:", e)

# --------------------------
# People Counting
# --------------------------
model = YOLO("yolov8n.pt")  # COCO model where 'person' = class 0
threshold = 5
alert_sent = False

cap = cv2.VideoCapture(0)  # webcam

while True:
    ret, frame = cap.read()
    results = model(frame)
    
    count = 0
    for r in results[0].boxes:
        if int(r.cls[0]) == 0:  # class 0 = person
            count += 1
            x1, y1, x2, y2 = r.xyxy[0]
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 2)

    cv2.putText(frame, f"People Count: {count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

    cv2.imshow("People Counting", frame)

    # --------------------------
    # Threshold Check
    # --------------------------
    if count > threshold and not alert_sent:
        send_alert_email(count)
        alert_sent = True

    if count <= threshold:
        alert_sent = False

    if cv2.waitKey(1) & 0xFF == 27:  # press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
