import cv2
import threading
from cvzone.HandTrackingModule import HandDetector

class CameraManager:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(detectionCon=0.8, maxHands=1)
        self.pulse_detected = False
        self.running = True

        # Iniciar el hilo de detección
        self.thread = threading.Thread(target=self._detect_pulse, daemon=True)
        self.thread.start()

    def _detect_pulse(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            hands, frame = self.detector.findHands(frame, draw=False)

            if hands:
                hand1 = hands[0]
                fingers = self.detector.fingersUp(hand1)
                self.pulse_detected = all(f == 0 for f in fingers)  # Si todos los dedos están cerrados, detecta el pulso

            cv2.imshow("Camera Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()
                break

    def stop(self):
        """Detiene la detección y libera la cámara"""
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()
