# CODES 

This repository contains a series of Python scripts to **convert handwritten documents into structured Question–Answer (Q&A) pairs** using OCR and rule-based segmentation.  
All versions are organized under the `Codes` folder.

---

## Overview

Handwritten OCR outputs are often messy:
- Questions and answers may be mixed
- Question numbers may be inconsistent
- Some questions may miss question marks

This repository provides **multiple iterations** of scripts to handle:
- Raw OCR text cleanup
- Multi-line answer grouping
- Multi-image document processing
- Strong preprocessing for better OCR accuracy

All versions are **non-LLM**, purely heuristic and image-processing-based.

---

## Features

- Rule-based question detection (no AI/LLM)
- Handles multi-line answers
- Sequential numbering of questions and answers
- Strong image preprocessing for handwritten notes
- Works on multiple images in a folder
- Outputs both raw OCR text and structured Q&A
- Multiple script versions included for experimentation and comparison

---

## Tech Stack

- Python
- OpenCV
- Tesseract OCR
- Regular Expressions (`re`)

---

