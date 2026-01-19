import cv2
import pytesseract
import numpy as np
import os
import re

# ==============================
# PATHS
# ==============================
IMAGE_FOLDER = r"C:\Users\VGMan\Downloads\Handwritten_OCR_QA\images"
OUTPUT_FOLDER = r"C:\Users\VGMan\Downloads\Handwritten_OCR_QA\outputs"
RAW_TEXT_FILE = os.path.join(OUTPUT_FOLDER, "raw_text.txt")
QA_FILE = os.path.join(OUTPUT_FOLDER, "qa_pairs.txt")

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\VGMan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==============================
# IMAGE PREPROCESSING
# ==============================
def preprocess_image(img_path):
    img = cv2.imread(img_path)

    if img is None:
        print(f"❌ Image not found: {img_path}")
        return None

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # CLAHE for contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Bilateral filter to remove noise but preserve edges
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    # Resize for better OCR
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Sharpening
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    gray = cv2.filter2D(gray, -1, kernel)

    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 10
    )

    return thresh

# ==============================
# OCR FUNCTION
# ==============================
def ocr_image(img_path):
    processed = preprocess_image(img_path)
    if processed is None:
        return ""

    # Use line-wise OCR to preserve formatting
    data = pytesseract.image_to_data(processed, config="--oem 3 --psm 6", output_type=pytesseract.Output.DICT)
    lines = {}
    for i, text in enumerate(data['text']):
        text = text.strip()
        if text != "":
            line_num = data['line_num'][i]
            if line_num not in lines:
                lines[line_num] = []
            lines[line_num].append(text)

    # Combine lines
    ocr_text = "\n".join([" ".join(lines[key]) for key in sorted(lines.keys())])
    return ocr_text

# ==============================
# QA SEPARATION FUNCTION
# ==============================
def split_qa(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    QUESTION_KEYWORDS = (
        "what", "why", "how", "define", "explain",
        "state", "list", "describe", "give", "write"
    )
    qa_pairs = []
    current_question = None
    current_answer = []

    for line in lines:
        lower_line = line.lower()
        is_question = False
        is_option = False

        # Detect MCQ options
        if re.match(r"^[A-D][\.\)]", line):
            is_option = True

        # Detect questions
        if line.endswith("?") or any(lower_line.startswith(k) for k in QUESTION_KEYWORDS) or re.match(r"^\d+\.", line):
            is_question = True

        if is_question:
            # Save previous QA
            if current_question is not None:
                qa_pairs.append({
                    "question": current_question,
                    "answer": " ".join(current_answer).strip()
                })
            # Clean question
            clean_q = re.sub(r"^\d+\.", "", line).strip()
            if not clean_q.endswith("?"):
                clean_q += "?"
            current_question = clean_q
            current_answer = []

        else:
            # Append options or normal lines to answer
            current_answer.append(line)

    # Save last QA
    if current_question is not None:
        qa_pairs.append({
            "question": current_question,
            "answer": " ".join(current_answer).strip()
        })

    # Proper numbering
    final_qa = []
    for i, qa in enumerate(qa_pairs, start=1):
        final_qa.append({
            "question": f"Q{i}: {qa['question']}",
            "answer": f"A{i}: {qa['answer']}"
        })

    return final_qa

# ==============================
# MAIN FUNCTION
# ==============================
def main():
    full_text = ""

    # OCR all images
    for file in sorted(os.listdir(IMAGE_FOLDER)):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            print(f"Processing: {file}")
            text = ocr_image(os.path.join(IMAGE_FOLDER, file))
            full_text += text + "\n"

    # Save raw OCR text
    with open(RAW_TEXT_FILE, "w", encoding="utf-8") as f:
        f.write(full_text)

    # Split into Q&A
    qa_pairs = split_qa(full_text)

    # Save QA text
    with open(QA_FILE, "w", encoding="utf-8") as f:
        for qa in qa_pairs:
            f.write(qa["question"] + "\n")
            f.write(qa["answer"] + "\n\n")

    print("✅ OCR and Q&A extraction completed!")
    print(f"📄 Raw OCR text: {RAW_TEXT_FILE}")
    print(f"📄 QA pairs: {QA_FILE}")

if __name__ == "__main__":
    main()
