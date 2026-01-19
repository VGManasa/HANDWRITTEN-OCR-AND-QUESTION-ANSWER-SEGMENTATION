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

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Tell Python where Tesseract is
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\VGMan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)

# -----------------------------
# IMAGE PREPROCESSING
# -----------------------------
def preprocess(img_path):
    img = cv2.imread(img_path)

    if img is None:
        print(f"❌ Image not found: {img_path}")
        return None

    # Upscale image to improve OCR
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 10
    )
    return thresh

# -----------------------------
# OCR FUNCTION
# -----------------------------
def ocr_image(img_path):
    processed = preprocess(img_path)
    if processed is None:
        return ""

    config = "--oem 3 --psm 6 -c preserve_interword_spaces=1"
    text = pytesseract.image_to_string(processed, config=config)
    return text

# -----------------------------
# QA SEPARATION (MCQ SAFE)
# -----------------------------
def split_qa_mcq(text):
    """
    Splits text into Q&A including MCQs.
    - MCQ options (A/B/C/D) are part of the answer.
    - Every question ends with '?'.
    """
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    qa = []
    q = None
    a = []

    option_pattern = re.compile(r"^[A-D]\.?\s")  # Matches A. B. C. D.

    for line in lines:
        is_option = bool(option_pattern.match(line))
        is_question = False

        # Question detection rules
        if line.endswith("?"):
            is_question = True
        elif re.match(r"^\d+\.", line):
            is_question = True
        elif not is_option and (q is None):  # first line or unclear line is treated as question
            is_question = True

        if is_question:
            if q:
                qa.append((q, " ".join(a)))
            q = line.rstrip(".") + "?"  # ensure question mark
            a = []
        else:
            a.append(line)

    if q:
        qa.append((q, " ".join(a)))

    return qa

# -----------------------------
# MAIN EXECUTION
# -----------------------------
def main():
    full_text = ""

    # Process all images
    for file in sorted(os.listdir(IMAGE_FOLDER)):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            print(f"Processing: {file}")
            text = ocr_image(os.path.join(IMAGE_FOLDER, file))
            full_text += text + "\n"

    # Save raw OCR text
    raw_file = os.path.join(OUTPUT_FOLDER, "raw_ocr_text.txt")
    with open(raw_file, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"📄 Raw OCR text saved: {raw_file}")

    # Extract QA pairs
    qa_pairs = split_qa_mcq(full_text)

    # Save QA pairs
    qa_file = os.path.join(OUTPUT_FOLDER, "qa_pairs.txt")
    with open(qa_file, "w", encoding="utf-8") as f:
        for i, (q, a) in enumerate(qa_pairs, 1):
            f.write(f"Q{i}: {q}\n")
            f.write(f"A{i}: {a}\n\n")
    print(f"✅ QA pairs saved: {qa_file}")

if __name__ == "__main__":
    main()
