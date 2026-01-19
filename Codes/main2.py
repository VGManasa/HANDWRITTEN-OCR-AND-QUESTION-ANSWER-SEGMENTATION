import cv2
import pytesseract
import os
import re
import numpy as np

# -----------------------------
# PATHS
# -----------------------------
IMAGE_FOLDER = r"C:\Users\VGMan\Downloads\Handwritten_OCR_QA\images"
OUTPUT_FOLDER = r"C:\Users\VGMan\Downloads\Handwritten_OCR_QA\outputs"

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\VGMan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------
# STRONG PREPROCESSING
# -----------------------------
def preprocess(img_path):
    img = cv2.imread(img_path)

    # Upscale (VERY important)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Remove noise
    gray = cv2.medianBlur(gray, 3)

    # Strong threshold
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 5
    )

    return thresh

# -----------------------------
# OCR (STRICT MODE)
# -----------------------------
def ocr_image(img_path):
    processed = preprocess(img_path)

    config = (
        "--oem 1 "
        "--psm 4 "
        "-c tessedit_char_whitelist="
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,?:()/- "
    )

    text = pytesseract.image_to_string(processed, config=config)
    return text

# -----------------------------
# QA SEPARATION (DEFENSIVE)
# -----------------------------
def split_qa(text):
    lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 3]

    qa = []
    q = None
    a = []

    for line in lines:
        is_question = False

        if re.match(r"^\d+\.", line):
            is_question = True
        elif line.lower().startswith(
            ("what", "why", "how", "define", "explain", "state", "write", "describe")
        ):
            is_question = True

        if is_question:
            if q:
                qa.append((q, " ".join(a)))
            q = line.rstrip(".") + "?"
            a = []
        else:
            a.append(line)

    if q:
        qa.append((q, " ".join(a)))

    return qa

# -----------------------------
# MAIN
# -----------------------------
full_text = ""

for file in os.listdir(IMAGE_FOLDER):
    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        print("Processing:", file)
        text = ocr_image(os.path.join(IMAGE_FOLDER, file))
        full_text += text + "\n"

# Save raw OCR (for proof)
with open(os.path.join(OUTPUT_FOLDER, "raw_text.txt"), "w", encoding="utf-8") as f:
    f.write(full_text)

qa_pairs = split_qa(full_text)

with open(os.path.join(OUTPUT_FOLDER, "qa_pairs.txt"), "w", encoding="utf-8") as f:
    for i, (q, a) in enumerate(qa_pairs, 1):
        f.write(f"Q{i}: {q}\n")
        f.write(f"A{i}: {a}\n\n")

print("Done")
