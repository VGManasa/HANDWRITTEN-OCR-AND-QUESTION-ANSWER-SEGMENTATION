# VERSION 5

A Python script that performs OCR on handwritten question-and-answer documents and automatically extracts Q&A pairs into a clean text format.

## Features

- **Optical Character Recognition (OCR)**: Extracts text from handwritten images using Tesseract OCR
- **Advanced Image Preprocessing**: 
  - Grayscale conversion for consistent processing
  - 2x image upscaling (INTER_CUBIC interpolation) for enhanced OCR accuracy
  - Median blur filtering (3x3 kernel) to reduce noise
  - Adaptive Gaussian thresholding for optimal binarization
- **Intelligent Text Cleaning**:
  - Automatic line merging and space normalization
  - Sentence boundary detection and formatting
  - Whitespace consolidation using regex patterns
- **Smart Q&A Detection**:
  - Numbered question pattern recognition (1., Q1, etc.)
  - Keyword-based question identification (what, why, how, define, explain, describe)
  - Automatic answer extraction between questions
  - Question mark normalization
- **Batch Processing**: Processes multiple images (PNG, JPG, JPEG) from a folder automatically
- **Sorted Processing**: Alphabetically sorted file processing for consistent output order
- **Automatic Directory Management**: Creates output folder if it doesn't exist
- **Structured Text Output**: 
  - Sequential Q&A pair numbering
  - Clean, formatted text file generation
  - UTF-8 encoding support for special characters
- **Progress Monitoring**: Console output showing which files are being processed
- **Tesseract Configuration**: Optimized OCR settings with custom config string (OEM 3, PSM 6, interword space preservation)

## Prerequisites

### Software Requirements

- Python 3.x
- Tesseract OCR installed on your system

### Python Dependencies

```bash
pip install opencv-python pytesseract numpy
```

### Tesseract Installation

Download and install Tesseract OCR from:
- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- macOS: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

## Configuration

Update the following paths in the script to match your system:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Path\To\tesseract.exe"
IMAGE_FOLDER = r"C:\Path\To\Your\Images"
OUTPUT_FOLDER = r"C:\Path\To\Your\Outputs"
```

## Usage

1. Place your handwritten Q&A images (PNG, JPG, JPEG) in the `IMAGE_FOLDER` directory
2. Run the script:
   ```bash
   python ocr_qa_extractor.py
   ```
3. Find the extracted Q&A pairs in `OUTPUT_FOLDER/final_qa_clean.txt`

## How It Works

### Image Processing Pipeline

1. **Image Loading**: Reads images from the specified folder
2. **Preprocessing**:
   - Converts to grayscale
   - Upscales 2x for better OCR accuracy
   - Applies median blur to reduce noise
   - Uses adaptive thresholding for binarization
3. **OCR Extraction**: Uses Tesseract with optimized configuration
4. **Text Cleaning**: Removes extra whitespace and formats sentences

### Q&A Detection

The script identifies questions using multiple patterns:
- Numbered questions (e.g., "1.", "Q1")
- Question keywords (what, why, how, define, explain, describe)
- Question marks

Answers are captured as all text following a question until the next question is detected.

## Output Format

```
Q1: What is photosynthesis?
A1: Photosynthesis is the process by which plants convert light energy into chemical energy.

Q2: Why is water important for plants?
A2: Water is essential for photosynthesis and helps transport nutrients throughout the plant.
```

## Customization

### OCR Configuration

Modify the Tesseract config string for different use cases:
```python
config = "--oem 3 --psm 6 -c preserve_interword_spaces=1"
```

- `--oem 3`: Use LSTM OCR engine
- `--psm 6`: Assume uniform text block
- Adjust PSM modes (1-13) based on document layout

### Image Preprocessing

Adjust preprocessing parameters for different image qualities:
```python
gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)  # Scaling factor
gray = cv2.medianBlur(gray, 3)  # Blur kernel size
cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10)  # Threshold parameters
```

## Limitations

- OCR accuracy depends heavily on handwriting legibility
- Rule-based Q&A detection may miss non-standard question formats
- Best results with clear, well-spaced handwritten text
- Does not handle multi-column layouts

## Troubleshooting

**Tesseract not found error**: Verify the `tesseract_cmd` path is correct for your system

**Poor OCR accuracy**: Try adjusting preprocessing parameters or improving image quality (higher resolution, better lighting)

**Questions not detected**: Check if questions follow standard formats or add custom patterns to the regex


