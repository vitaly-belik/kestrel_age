import cv2
import sys
import datetime
import time

DUR = 900

def record_chunk(cap, duration = DUR):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"chunk_{timestamp}.mp4"

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"avc1")  # H.264 / AVC
    writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    print(f"Recording {output_file} for {duration} seconds")
    start = time.time()
    while time.time() - start < duration:
        ret, frame = cap.read()
        if not ret:
            print("Stream ended or frame read error")
            break
        writer.write(frame)

    writer.release()
    print(f"Finished {output_file}")

def record_stream(stream_url, chunk_duration = DUR):
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("Error: could not open stream")
        sys.exit(1)

    print("Starting continuous 2-minute chunk recording...")
    try:
        while True:
            record_chunk(cap, chunk_duration)
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        cap.release()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python record_stream.py <stream_url>")
        sys.exit(1)

    record_stream(sys.argv[1])
