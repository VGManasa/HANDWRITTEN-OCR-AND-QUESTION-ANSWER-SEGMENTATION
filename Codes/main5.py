import cv2
import pytesseract
import os
import numpy as np
import re

# -----------------------------
# 1️⃣ Tesseract path
# -----------------------------
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\VGMan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)

# -----------------------------
# 2️⃣ Folders
# -----------------------------
IMAGE_FOLDER = r"C:\Users\VGMan\Downloads\Handwritten_OCR_QA\images"
OUTPUT_FOLDER = r"C:\Users\VGMan\Downloads\Handwritten_OCR_QA\outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------
# 3️⃣ OCR + Preprocessing
# -----------------------------
def ocr_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return ""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.medianBlur(gray, 3)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 10
    )

    config = "--oem 3 --psm 6 -c preserve_interword_spaces=1"
    text = pytesseract.image_to_string(thresh, config=config)
    
    # -----------------------------
    # Clean OCR text
    # -----------------------------
    text = text.replace("\n", " ")        # merge lines
    text = re.sub(r"\s+", " ", text)     # collapse multiple spaces
    text = re.sub(r"([.?!])", r"\1\n", text)  # put sentences on new lines
    return text.strip()

# -----------------------------
# 4️⃣ Rule-based Q&A splitter
# -----------------------------
def split_qa(text):
    lines = [line.strip() for line in text.split("\n") if line.strip() != ""]
    qa_pairs = []
    current_q = None
    current_a = ""

    for line in lines:
        if re.match(r"^(\d+\.|Q\d+)", line.lower()) or \
           any(line.lower().startswith(w) for w in
               ["what", "why", "how", "define", "explain", "describe"]):
            if current_q:
                qa_pairs.append((current_q + "?", current_a.strip()))
            current_q = line.rstrip("?")
            current_a = ""
        else:
            current_a += line + " "

    if current_q:
        qa_pairs.append((current_q + "?", current_a.strip()))
    return qa_pairs

# -----------------------------
# 5️⃣ Process all images
# -----------------------------
all_text = ""
for filename in sorted(os.listdir(IMAGE_FOLDER)):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        img_path = os.path.join(IMAGE_FOLDER, filename)
        print(f"Processing: {filename}")
        text = ocr_image(img_path)
        all_text += text + "\n"

# -----------------------------
# 6️⃣ Extract Q&A pairs
# -----------------------------
qa_pairs = split_qa(all_text)

# -----------------------------
# 7️⃣ Save to text file
# -----------------------------
output_path = os.path.join(OUTPUT_FOLDER, "final_qa_clean.txt")
with open(output_path, "w", encoding="utf-8") as f:
    for i, (q, a) in enumerate(qa_pairs, 1):
        f.write(f"Q{i}: {q}\n")
        f.write(f"A{i}: {a}\n\n")

print(f"✅ Done! Clean QA pairs saved at {output_path}")
