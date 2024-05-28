import cv2
from PIL import Image, ImageDraw, ImageFont
import pywhatkit as kt
import numpy as np

def extract_frames(video_path, output_folder, frame_rate=1):
    cap = cv2.VideoCapture(video_path)
    count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps / frame_rate)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % interval == 0:
            frame_path = f"{output_folder}/frame_{count}.png"
            cv2.imwrite(frame_path, frame)
        count += 1

    cap.release()

def add_ascii_art_to_image(image_path, output_path, ascii_text):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text_width, text_height = draw.textsize(ascii_text, font)
    
    image_width, image_height = image.size
    x = (image_width - text_width) / 2
    y = (image_height - text_height) / 2

    draw.text((x, y), ascii_text, font=font, fill="white")
    image.save(output_path)

def generate_ascii_art(text):
    ascii_art = kt.text_to_handwriting(text, save_to='ascii_art.png')
    with open('ascii_art.png', 'rb') as f:
        img = Image.open(f)
        ascii_text = kt.image_to_ascii(img)
    return ascii_text

def process_video(video_path, output_folder, frame_rate=1):
    extract_frames(video_path, output_folder, frame_rate)

    for frame in os.listdir(output_folder):
        frame_path = os.path.join(output_folder, frame)
        ascii_text = generate_ascii_art('Sample ASCII Art')
        output_path = os.path.join(output_folder, f"ascii_{frame}")
        add_ascii_art_to_image(frame_path, output_path, ascii_text)

if __name__ == "__main__":
    video_path = "video.mp4"
    output_folder = "path/"
    os.makedirs(output_folder, exist_ok=True)
    process_video(video_path, output_folder, frame_rate=1)
