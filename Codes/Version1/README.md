# VERSION 1 

This module implements a **rule-based, non-LLM approach** to organize raw OCR text extracted from handwritten documents into structured **Question–Answer (Q&A) pairs**.

It is designed to handle noisy OCR outputs where questions and answers are not clearly separated.

---

## Features

- Rule-based question detection (no ML / no LLM)
- Automatic Question–Answer pairing
- Ensures proper question formatting
- Handles multi-line answers
- Sequential renumbering of questions and answers
- Works directly on OCR-generated text files

---

## Tech Stack

- Python
- Regular Expressions (`re`)
- File-based text processing

---

## How It Works

1. Reads raw OCR text from a `.txt` file
2. Cleans and preprocesses OCR lines
3. Detects questions using heuristic rules:
   - Lines ending with `?`
   - Lines starting with numbers (`1.`, `2.`) or `Q1`, `Q2`
   - Lines starting with question keywords (`what`, `how`, `define`, etc.)
4. Groups subsequent lines as answers until the next question is detected
5. Ensures every question ends with a `?`
6. Renumbers all questions as `Q1, Q2, Q3...`
7. Outputs structured Q&A pairs to a new text file

---

## Question Detection Rules

A line is classified as a **question** if **any** of the following conditions are met:

- Ends with a question mark (`?`)
- Starts with a number or question label (e.g., `1.`, `Q3`)
- Starts with keywords such as:
  - what
  - why
  - how
  - define
  - explain
  - state
  - list
  - describe
  - give
  - write

All other lines are treated as part of the answer.

---

## Input File

**`raw_ocr_text.txt`**

- Contains unstructured OCR output
- May include:
  - Missing question marks
  - Broken numbering
  - Multi-line answers
  - OCR noise

---

## Output File

**`qa_pairs.txt`**


---

## Limitations

- Heuristic-based detection may fail for:
  - Very ambiguous sentence structures
  - Poor OCR quality
- Does not perform semantic validation
- No support for diagrams or tables

---

## Future Improvements

- Confidence-based OCR filtering
- Improved question classification rules
- Layout-aware segmentation
- Integration with scanned PDF pipelines

---

