# VERSION 3

A Python pipeline that converts handwritten document images into structured question-answer pairs using OCR and rule-based segmentation.

## Features

- OpenCV-based image preprocessing for enhanced OCR accuracy
- Tesseract OCR integration for text extraction
- Automatic image upscaling and noise reduction
- Rule-based question-answer segmentation
- Automatic question mark addition and sequential numbering
- Saves both raw OCR output and structured Q&A pairs
- No use of LLMs or semantic models

## Tech Stack

- Python 3.6+
- OpenCV (cv2)
- Tesseract OCR
- pytesseract
- NumPy
- Regular Expressions

## Installation

1. Install Python dependencies:
```bash
pip install opencv-python pytesseract numpy
```

2. Install Tesseract OCR:
   - **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Linux**: `sudo apt-get install tesseract-ocr`
   - **macOS**: `brew install tesseract`

3. Update Tesseract path in script:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\path\to\tesseract.exe"
```

## Configuration

Update these paths before running:

```python
IMAGE_PATH = r"C:\path\to\your\handwritten_image.png"
OUTPUT_FOLDER = r"C:\path\to\outputs"
```

## Usage

```bash
python ocr_qa_pipeline.py
```

## How It Works

### 1. Image Preprocessing
- **Upscaling**: 2x resize using cubic interpolation for better OCR
- **Grayscale conversion**: Reduces color noise
- **Median blur**: Removes salt-and-pepper noise
- **Adaptive thresholding**: Binarizes image while handling varying lighting

### 2. OCR Text Extraction
- Uses Tesseract with custom configuration (`--oem 3 --psm 6`)
- Preserves interword spaces for better text structure
- Saves raw OCR output to `raw_ocr_text.txt`

### 3. Question-Answer Segmentation
Detects questions using three rule-based strategies:
- Lines ending with `?`
- Lines starting with numbers (`1.`, `2.`, etc.)
- Lines beginning with question keywords: what, why, how, define, explain, state, list, describe, write, give

### 4. Answer Grouping
- Groups all lines after a question as the answer
- Continues until next question is detected
- Joins multi-line answers into single paragraphs

### 5. Output Formatting
- Removes old numbering from questions
- Adds missing question marks
- Renumbers all pairs sequentially (Q1, Q2, Q3...)
- Saves to `qa_pairs.txt`

## Input/Output Examples

### Input Image
Handwritten document with questions and answers:
```
1. What is photosynthesis
Plants use sunlight to make food through chlorophyll

2 Why is water important
Water is essential for all living organisms
```

### Output: raw_ocr_text.txt
```
1. What is photosynthesis
Plants use sunlight to make food through chlorophyll

2 Why is water important
Water is essential for all living organisms
```

### Output: qa_pairs.txt
```
Q1: What is photosynthesis?
A1: Plants use sunlight to make food through chlorophyll

Q2: Why is water important?
A2: Water is essential for all living organisms
```

## File Structure

```
project/
├── ocr_qa_pipeline.py          # Main script
├── images/
│   └── img1.png                # Input handwritten images
└── outputs/
    ├── raw_ocr_text.txt        # Raw OCR extraction
    └── qa_pairs.txt            # Structured Q&A pairs
```

## Preprocessing Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Upscale Factor | 2x | Improves character recognition |
| Median Blur Kernel | 3 | Noise reduction |
| Adaptive Threshold Block | 31 | Local binarization |
| Threshold Constant | 10 | Fine-tuning brightness |

## Limitations

- Performance depends on handwriting quality and clarity
- Heuristic-based segmentation may fail for ambiguous layouts
- Cannot handle diagrams or mathematical equations
- Requires clear question-answer structure in document
- Single-column layout works best
- No multi-page document support in current version

## Future Improvements

- Confidence-based OCR filtering to remove low-quality detections
- Diagram and equation detection/extraction
- Multi-column layout handling
- Support for processing multiple images sequentially
- Table structure recognition
- Advanced preprocessing for poor quality images
- Custom training data for handwritten text recognition

## Troubleshooting

**Issue**: Tesseract not found
- **Solution**: Verify installation path and update `tesseract_cmd` variable

**Issue**: Poor OCR accuracy
- **Solution**: Increase image quality, adjust preprocessing parameters, or use higher resolution scans

**Issue**: Questions not detected
- **Solution**: Check if questions start with keywords or end with `?`, manually add markers if needed

**Issue**: Answers split incorrectly
- **Solution**: Review heuristic rules, ensure clear spacing between Q&A pairs in original document

