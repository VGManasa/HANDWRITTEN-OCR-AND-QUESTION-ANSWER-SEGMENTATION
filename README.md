# HANDWRITTEN-OCR-AND-QUESTION-ANSWER-SEGMENTATION
This project implements a non-LLM pipeline for converting handwritten document images into structured question–answer pairs.

## Features
- OpenCV-based image preprocessing
- Line-wise OCR using Tesseract
- Rule-based question–answer segmentation
- Handles multi-image document continuity
- No use of LLMs or semantic models

## Tech Stack
- Python
- OpenCV
- Tesseract OCR

## How It Works
1. Preprocess images to enhance OCR quality
2. Extract line-wise text using Tesseract
3. Merge multiple pages while preserving order
4. Segment questions and answers using heuristics

## Limitations
- Performance depends on handwriting quality
- Heuristic-based segmentation may fail for ambiguous layouts

## Future Improvements
- Confidence-based OCR filtering
- Diagram detection
- Multi-column layout handling
