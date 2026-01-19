import cv2
import pytesseract
import numpy as np
import os
import re

# ==================================================
# PATH CONFIGURATION
# ==================================================
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\VGMan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)

IMAGE_PATH = r"C:\Users\VGMan\Downloads\Handwritten_OCR_QA\images\img1.png"
OUTPUT_FOLDER = r"C:\Users\VGMan\Downloads\Handwritten_OCR_QA\outputs"

RAW_TEXT_FILE = os.path.join(OUTPUT_FOLDER, "raw_ocr_text.txt")
QA_OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "qa_pairs.txt")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ==================================================
# IMAGE PREPROCESSING
# ==================================================
def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise FileNotFoundError("Image not found")

    # Upscale for better OCR
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise reduction
    gray = cv2.medianBlur(gray, 3)

    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )

    return thresh


# ==================================================
# OCR FUNCTION
# ==================================================
def extract_text(image_path):
    processed = preprocess_image(image_path)

    config = "--oem 3 --psm 6 -c preserve_interword_spaces=1"
    text = pytesseract.image_to_string(processed, config=config)

    return text


# ==================================================
# QUESTION–ANSWER SEPARATION (RULE-BASED)
# ==================================================
def split_qa(text):
    lines = [line.strip() for line in text.split("\n") if len(line.strip()) > 2]

    QUESTION_KEYWORDS = (
        "what", "why", "how", "define", "explain",
        "state", "list", "describe", "write", "give"
    )

    qa_pairs = []
    current_question = None
    current_answer = []

    for line in lines:
        lower = line.lower()
        is_question = False

        # Heuristics to detect question
        if line.endswith("?"):
            is_question = True
        elif re.match(r"^\d+\.", line):
            is_question = True
        elif any(lower.startswith(k) for k in QUESTION_KEYWORDS):
            is_question = True

        if is_question:
            if current_question:
                qa_pairs.append({
                    "question": current_question,
                    "answer": " ".join(current_answer).strip()
                })

            clean_q = re.sub(r"^\d+\.", "", line).strip()
            if not clean_q.endswith("?"):
                clean_q += "?"

            current_question = clean_q
            current_answer = []
        else:
            current_answer.append(line)

    if current_question:
        qa_pairs.append({
            "question": current_question,
            "answer": " ".join(current_answer).strip()
        })

    # Proper numbering
    final_output = []
    for i, qa in enumerate(qa_pairs, start=1):
        final_output.append(
            f"Q{i}: {qa['question']}\nA{i}: {qa['answer']}\n"
        )

    return final_output


# ==================================================
# MAIN EXECUTION
# ==================================================
def main():
    print("📸 Processing image:", IMAGE_PATH)

    raw_text = extract_text(IMAGE_PATH)

    # Save raw OCR output
    with open(RAW_TEXT_FILE, "w", encoding="utf-8") as f:
        f.write(raw_text)

    print("📝 Raw OCR saved")

    qa_pairs = split_qa(raw_text)

    # Save structured Q&A
    with open(QA_OUTPUT_FILE, "w", encoding="utf-8") as f:
        for qa in qa_pairs:
            f.write(qa + "\n")

    print("✅ Q&A extraction completed")
    print("📄 Outputs saved in:", OUTPUT_FOLDER)


# ==================================================
if __name__ == "__main__":
    main()
