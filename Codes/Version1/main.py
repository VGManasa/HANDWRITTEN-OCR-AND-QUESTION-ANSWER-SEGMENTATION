import os
import re

# ===============================
# INPUT & OUTPUT FILES
# ===============================
INPUT_TEXT_FILE = r"C:\Users\VGMan\Downloads\Handwritten_OCR_QA\outputs\raw_ocr_text.txt"
OUTPUT_QA_FILE = r"C:\Users\VGMan\Downloads\Handwritten_OCR_QA\outputs\qa_pairs.txt"


# ===============================
# QA SEPARATION LOGIC
# ===============================
def split_qa(text):
    """
    Organises messy OCR text into clean Question–Answer pairs.
    Guarantees:
    - Proper numbering (Q1, Q2, ...)
    - Every question ends with '?'
    - Answers appear under the correct question
    """

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

        # Rule 1: Ends with '?'
        if line.endswith("?"):
            is_question = True

        # Rule 2: Starts with number or Q
        elif re.match(r"^(\d+\.|q\d+)", lower_line):
            is_question = True

        # Rule 3: Starts with question keyword
        elif any(lower_line.startswith(k) for k in QUESTION_KEYWORDS):
            is_question = True

        if is_question:
            # Save previous QA pair
            if current_question is not None:
                qa_pairs.append({
                    "question": current_question,
                    "answer": " ".join(current_answer).strip()
                })

            # Clean question
            clean_q = re.sub(r"^(\d+\.|q\d+)", "", line).strip()

            # Ensure question mark
            if not clean_q.endswith("?"):
                clean_q += "?"

            current_question = clean_q
            current_answer = []

        else:
            current_answer.append(line)

    # Save last QA
    if current_question is not None:
        qa_pairs.append({
            "question": current_question,
            "answer": " ".join(current_answer).strip()
        })

    # Renumber questions properly
    final_qa = []
    for i, qa in enumerate(qa_pairs, start=1):
        final_qa.append({
            "question": f"Q{i}: {qa['question']}",
            "answer": f"A{i}: {qa['answer']}"
        })

    return final_qa


# ===============================
# MAIN EXECUTION
# ===============================
if __name__ == "__main__":

    # Read OCR text (from file or OCR pipeline)
    with open(INPUT_TEXT_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    qa_pairs = split_qa(raw_text)

    # Save organised Q&A
    with open(OUTPUT_QA_FILE, "w", encoding="utf-8") as f:
        for qa in qa_pairs:
            f.write(qa["question"] + "\n")
            f.write(qa["answer"] + "\n\n")

    print("Question–Answer organisation completed successfully.")
