# VERSION 2

This project implements a **non-LLM, end-to-end pipeline** to convert handwritten document images into structured **Question–Answer (Q&A) pairs** using OpenCV and Tesseract OCR.

It is designed to handle multiple images, strong preprocessing, and heuristic-based QA segmentation without using any AI or LLM models.

---

## Features

- Strong image preprocessing for better OCR accuracy
- Upscaling, denoising, and adaptive thresholding
- Line-wise OCR using Tesseract in strict mode
- Rule-based question–answer segmentation
- Handles multiple images in a folder
- Outputs raw OCR text and structured Q&A text
- No use of LLMs or semantic models

---

## Tech Stack

- Python
- OpenCV
- Tesseract OCR
- Regular expressions (`re`)

---

## How It Works

1. Preprocess each image to enhance OCR quality:
   - Upscale by 2x
   - Convert to grayscale
   - Apply median blur
   - Apply adaptive thresholding
2. Extract text line by line using Tesseract OCR
3. Merge text from multiple images while preserving order
4. Identify questions using heuristics:
   - Lines starting with numbers (e.g., `1.`)
   - Lines starting with keywords (`what`, `why`, `how`, `define`, `explain`, `state`, `write`, `describe`)
5. Group subsequent lines as answers until the next question
6. Ensure each question ends with a `?`
7. Sequentially number questions and answers (`Q1, A1, Q2, A2...`)
8. Save:
   - Raw OCR text (`raw_text.txt`)
   - Structured Q&A (`qa_pairs.txt`)

---

## Input Folder

**`images/`**

- Place all handwritten images (`.png`, `.jpg`, `.jpeg`) here
- The script automatically processes all files in this folder

---

## Output Folder

**`outputs/`**

- `raw_text.txt` → Full OCR text from all images
- `qa_pairs.txt` → Structured Question–Answer pairs

---

## QA Segmentation Rules

A line is considered a **question** if:

- It starts with a number (e.g., `1.`, `2.`)
- It starts with keywords such as:
  - what
  - why
  - how
  - define
  - explain
  - state
  - write
  - describe

All other lines are considered part of the **answer**.

---

## Limitations

- OCR quality depends on handwriting clarity
- Rule-based question detection may fail for ambiguous sentences
- Multi-column or diagram-heavy pages are not supported

---

## Future Improvements

- Confidence-based OCR filtering
- Layout-aware segmentation (multi-column, tables)
- Diagram or equation detection
- Integration with PDF workflows

---
