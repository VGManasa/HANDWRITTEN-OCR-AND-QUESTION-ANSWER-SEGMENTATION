# VERSION 2

A robust Python pipeline that processes multiple handwritten document images and extracts structured question-answer pairs using strict OCR preprocessing and rule-based segmentation.

## Features

- Batch processing of multiple images from a folder
- Strong image preprocessing for enhanced OCR accuracy
- Character whitelist filtering for cleaner text extraction
- Multi-image text merging with preserved order
- Defensive question-answer segmentation
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
IMAGE_FOLDER = r"C:\path\to\images"
OUTPUT_FOLDER = r"C:\path\to\outputs"
```

## Usage

1. Place all handwritten images in the `IMAGE_FOLDER`
2. Run the script:
```bash
python multi_image_ocr.py
```

3. Check outputs in `OUTPUT_FOLDER`:
   - `raw_text.txt` - Combined raw OCR from all images
   - `qa_pairs.txt` - Structured Q&A pairs

## How It Works

### 1. Image Preprocessing (Strong Mode)
- **Upscaling**: 2x resize using cubic interpolation for better character recognition
- **Grayscale conversion**: Eliminates color noise
- **Median blur (kernel=3)**: Removes salt-and-pepper noise
- **Adaptive thresholding**: Strong binarization with block size 31 and constant 5

### 2. OCR with Character Whitelist
- **OEM Mode 1**: LSTM neural network engine for modern accuracy
- **PSM Mode 4**: Assumes single column of text
- **Character whitelist**: Only allows `A-Z`, `a-z`, `0-9`, and punctuation `.,?:()/-`
- Prevents garbage characters from entering output

### 3. Multi-Image Processing
- Iterates through all `.png`, `.jpg`, `.jpeg` files in folder
- Processes images in alphabetical order
- Concatenates text from all images sequentially
- Preserves document continuity across multiple pages

### 4. Question-Answer Segmentation (Defensive)
Detects questions using two strict rules:
- Lines starting with numbers followed by period (`1.`, `2.`, etc.)
- Lines beginning with question keywords: what, why, how, define, explain, state, write, describe

**Defensive features**:
- Filters out lines shorter than 3 characters (noise reduction)
- Groups all subsequent lines as answer until next question
- Strips trailing periods from questions and adds `?`
- Handles multi-line answers by joining with spaces

### 5. Output Formatting
- Renumbers all questions sequentially (Q1, Q2, Q3...)
- Formats as `Q{n}: question?` and `A{n}: answer`
- Double newline separation between Q&A pairs
- UTF-8 encoding for international character support

## Input/Output Examples

### Input: images/page1.png
```
1. What is photosynthesis
Plants convert sunlight into chemical energy

2. Why is water important
Essential for all life processes
```

### Input: images/page2.png
```
3. How does gravity work
Attracts objects with mass toward each other
```

### Output: raw_text.txt
```
1. What is photosynthesis
Plants convert sunlight into chemical energy

2. Why is water important
Essential for all life processes

3. How does gravity work
Attracts objects with mass toward each other
```

### Output: qa_pairs.txt
```
Q1: 1. What is photosynthesis?
A1: Plants convert sunlight into chemical energy

Q2: 2. Why is water important?
A2: Essential for all life processes

Q3: 3. How does gravity work?
A3: Attracts objects with mass toward each other
```

## File Structure

```
project/
├── multi_image_ocr.py          # Main script
├── images/
│   ├── page1.png               # Input image 1
│   ├── page2.jpg               # Input image 2
│   └── page3.jpeg              # Input image 3
└── outputs/
    ├── raw_text.txt            # Combined raw OCR
    └── qa_pairs.txt            # Structured Q&A pairs
```

## Preprocessing Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Upscale Factor | 2x | Doubles image resolution |
| Interpolation | INTER_CUBIC | Smooth upscaling |
| Median Blur Kernel | 3 | Noise reduction |
| Threshold Method | ADAPTIVE_GAUSSIAN | Local adaptive binarization |
| Block Size | 31 | Neighborhood size for threshold |
| Constant | 5 | Subtracted from weighted mean |

## OCR Configuration

| Parameter | Value | Purpose |
|-----------|-------|---------|
| OEM | 1 | LSTM neural network mode |
| PSM | 4 | Single column text assumption |
| Whitelist | A-Za-z0-9.,?:()/- | Allowed characters only |

## Supported Image Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)

## Limitations

- Performance depends on handwriting legibility and image quality
- Heuristic-based segmentation requires clear question structure
- Cannot handle diagrams, tables, or mathematical equations
- Works best with single-column layouts
- Character whitelist may remove valid special characters
- Questions must start with numbers or specific keywords
- No support for multi-language documents (English only)

## Future Improvements

- Confidence-based OCR filtering to remove uncertain detections
- Automatic image rotation correction for skewed scans
- Table and diagram detection/extraction
- Multi-column layout support
- Customizable question keyword dictionary
- Support for additional image formats (TIFF, BMP)
- Parallel processing for faster batch operations
- Advanced error handling and logging
- GUI interface for easier configuration

## Troubleshooting

**Issue**: Tesseract not found error
- **Solution**: Verify Tesseract installation and update `tesseract_cmd` path

**Issue**: Poor OCR accuracy on handwritten text
- **Solution**: Increase image resolution before scanning, adjust threshold constant from 5 to 10-15

**Issue**: Questions not detected
- **Solution**: Ensure questions are numbered (1., 2.) or start with keywords (what, why, how, etc.)

**Issue**: Special characters missing from output
- **Solution**: Add them to `tessedit_char_whitelist` in OCR config

**Issue**: Images processed in wrong order
- **Solution**: Rename files with numeric prefixes (001_page.png, 002_page.png)

**Issue**: Empty output file
- **Solution**: Check if images are readable, verify file permissions, ensure valid image format

## Performance Tips

- Use high-resolution scans (300+ DPI)
- Ensure good lighting with minimal shadows
- Use black ink on white paper for best contrast
- Keep handwriting neat and well-spaced
- Number questions consistently (1., 2., 3.)
- Avoid cursive writing when possible

