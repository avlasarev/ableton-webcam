import cv2
import time
import rtmidi

# MIDI message constants
NOTE_ON = 0x90
NOTE_OFF = 0x80

# Initialize MIDI
try:
    midiout = rtmidi.RtMidiOut()
    print("RtMidiOut initialized successfully.")
    available_ports = midiout.getPortCount()
    print(f"Available ports: {available_ports}")
except Exception as e:
    print("Error initializing RtMidiOut:", e)
    exit(1)

# Open the loopMIDI port
port_name = "from_python_port"  # Ensure this matches the name of your loopMIDI port
port_opened = False
for i in range(available_ports):
    port_name_available = midiout.getPortName(i)
    print(f"Checking port: {port_name_available}")
    if port_name in port_name_available:
        midiout.openPort(i)
        print(f"Opened port: {port_name_available}")
        port_opened = True
        break

if not port_opened:
    raise Exception(f"Port named '{port_name}' not found. Ensure loopMIDI is running and the port is created.")

# Load Haar Cascade for face detection
hand_cascade = cv2.CascadeClassifier('D:/ableton_python_duet_project/hand_detection/haarcascade_frontalface_default.xml')

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Face detection parameters
def detect_hands(gray_frame):
    hands = hand_cascade.detectMultiScale(
        gray_frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return hands

def send_midi_signal(note, track, velocity=112, duration=0.1):
    on_message = rtmidi.MidiMessage.noteOn(track, note, velocity)
    off_message = rtmidi.MidiMessage.noteOff(track, note)
    print(f"Sending MIDI ON message: {on_message}")
    midiout.sendMessage(on_message)
    time.sleep(duration)
    print(f"Sending MIDI OFF message: {off_message}")
    midiout.sendMessage(off_message)

def detect_and_control():
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detect_hands(gray)

        height, width, _ = frame.shape
        section_width = width // 2
        section_height = height // 2

        print(f"Frame {frame_count}: Detected {len(faces)} faces")
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cx = x + w // 2
            cy = y + h // 2

            print(f"Face position - x: {cx}, y: {cy}")
            # Determine the section based on hand position
            if cx < section_width and cy < section_height:
                track = 0  # Top-left section, MIDI channel 1 (track 1)
                print("Face in top-left section")
                send_midi_signal(note=60, track=track)  # Example note C4
            elif cx >= section_width and cy < section_height:
                track = 1  # Top-right section, MIDI channel 2 (track 2)
                print("Face in top-right section")
                send_midi_signal(note=62, track=track)  # Example note D4
            elif cx < section_width and cy >= section_height:
                track = 2  # Bottom-left section, MIDI channel 3 (track 3)
                print("Face in bottom-left section")
                send_midi_signal(note=64, track=track)  # Example note E4
            else:
                track = 3  # Bottom-right section, MIDI channel 4 (track 4)
                print("Face in bottom-right section")
                send_midi_signal(note=65, track=track)  # Example note F4

        # Draw lines to split the frame into four sections
        cv2.line(frame, (section_width, 0), (section_width, height), (0, 255, 0), 2)
        cv2.line(frame, (0, section_height), (width, section_height), (0, 255, 0), 2)

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    midiout.closePort()

if __name__ == "__main__":
    detect_and_control()
