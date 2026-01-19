# VERSION 4

A Python pipeline that processes handwritten document images containing multiple-choice questions (MCQs) and extracts structured question-answer pairs while preserving MCQ options.

## Features

- Batch processing of multiple images from a folder
- OpenCV-based image preprocessing for enhanced OCR accuracy
- Tesseract OCR integration with optimized configuration
- MCQ-aware question-answer segmentation
- Preserves A/B/C/D options as part of answers
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
python mcq_ocr_extractor.py
```

3. Check outputs in `OUTPUT_FOLDER`:
   - `raw_ocr_text.txt` - Combined raw OCR from all images
   - `qa_pairs.txt` - Structured Q&A pairs with MCQ options

## How It Works

### 1. Image Preprocessing
- **Upscaling**: 2x resize using cubic interpolation for better character recognition
- **Grayscale conversion**: Eliminates color noise
- **Median blur (kernel=3)**: Removes salt-and-pepper noise
- **Adaptive thresholding**: Gaussian-based binarization with block size 31 and constant 10

### 2. OCR Text Extraction
- **OEM Mode 3**: Default Tesseract engine (legacy + LSTM)
- **PSM Mode 6**: Assumes uniform block of text
- **Preserve interword spaces**: Maintains spacing for better structure
- Processes images in alphabetical order
- Concatenates text from all images sequentially

### 3. MCQ-Aware Question-Answer Segmentation

**Question Detection Rules**:
- Lines ending with `?`
- Lines starting with numbers (`1.`, `2.`, etc.)
- First line in document (fallback rule)

**MCQ Option Detection**:
- Lines matching pattern `A.`, `B.`, `C.`, `D.` (with or without spaces)
- Options are treated as part of the answer, NOT as new questions
- Regex pattern: `^[A-D]\.?\s`

**Answer Grouping**:
- All lines after a question become the answer
- MCQ options are included in the answer
- Multi-line content is joined with spaces
- Continues until next question is detected

### 4. Question Cleaning
- Strips trailing periods from questions
- Adds missing question marks automatically
- Ensures consistent formatting

### 5. Output Formatting
- Sequential numbering (Q1, Q2, Q3...)
- Format: `Q{n}: question?` and `A{n}: answer with options`
- Double newline separation between pairs
- UTF-8 encoding for international characters

## Input/Output Examples

### Input: images/exam_page1.png
```
1. What is the capital of France
A. London
B. Paris
C. Berlin
D. Madrid

2. Which gas do plants absorb
A. Oxygen
B. Nitrogen
C. Carbon dioxide
D. Hydrogen
```

### Output: raw_ocr_text.txt
```
1. What is the capital of France
A. London
B. Paris
C. Berlin
D. Madrid

2. Which gas do plants absorb
A. Oxygen
B. Nitrogen
C. Carbon dioxide
D. Hydrogen
```

### Output: qa_pairs.txt
```
Q1: 1. What is the capital of France?
A1: A. London B. Paris C. Berlin D. Madrid

Q2: 2. Which gas do plants absorb?
A2: A. Oxygen B. Nitrogen C. Carbon dioxide D. Hydrogen
```

## File Structure

```
project/
├── mcq_ocr_extractor.py        # Main script
├── images/
│   ├── page1.png               # Input image 1
│   ├── page2.jpg               # Input image 2
│   └── page3.jpeg              # Input image 3
└── outputs/
    ├── raw_ocr_text.txt        # Combined raw OCR
    └── qa_pairs.txt            # Structured Q&A pairs
```

## Preprocessing Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Upscale Factor | 2x | Doubles image resolution |
| Interpolation | INTER_CUBIC | Smooth upscaling algorithm |
| Median Blur Kernel | 3 | Noise reduction strength |
| Threshold Method | ADAPTIVE_GAUSSIAN | Local adaptive binarization |
| Block Size | 31 | Neighborhood size for threshold |
| Constant | 10 | Subtracted from weighted mean |

## OCR Configuration

| Parameter | Value | Purpose |
|-----------|-------|---------|
| OEM | 3 | Default Tesseract engine mode |
| PSM | 6 | Uniform block of text |
| preserve_interword_spaces | 1 | Maintains word spacing |

## Supported Image Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)

## MCQ Option Detection

The script recognizes these option patterns:

| Pattern | Detected |
|---------|----------|
| `A. Option text` | Yes |
| `B. Option text` | Yes |
| `C.Option text` | Yes |
| `D .Option text` | Yes |
| `E. Option text` | No (only A-D) |
| `a. Option text` | No (case-sensitive) |

## Key Differences from Standard QA Extraction

| Feature | Standard QA | MCQ-Aware QA |
|---------|-------------|--------------|
| Option Detection | Options treated as questions | Options included in answers |
| Pattern Matching | No MCQ logic | Regex for A/B/C/D detection |
| Answer Format | Plain text | Includes all options |
| Use Case | Subjective questions | Multiple-choice exams |

## Limitations

- Performance depends on handwriting legibility
- Only supports A/B/C/D options (not E, F, etc.)
- Case-sensitive option detection (lowercase a/b/c/d not recognized)
- Cannot handle diagrams or images within questions
- Works best with single-column layouts
- No support for multi-part questions (1a, 1b, 1c)
- Requires clear question numbering or punctuation

## Future Improvements

- Support for extended options (E, F, G, etc.)
- Case-insensitive option detection
- Confidence-based OCR filtering
- Automatic correct answer extraction (if marked)
- Table and diagram detection
- Multi-column layout support
- Answer key generation
- JSON/CSV export formats
- GUI interface for easier use

## Troubleshooting

**Issue**: Tesseract not found
- **Solution**: Verify installation path and update `tesseract_cmd` variable

**Issue**: MCQ options detected as separate questions
- **Solution**: Ensure options follow A/B/C/D format with period

**Issue**: Poor OCR accuracy
- **Solution**: Use higher resolution scans (300+ DPI), adjust threshold parameters

**Issue**: Images processed in wrong order
- **Solution**: Rename files with numeric prefixes (001_page.png, 002_page.png)

**Issue**: Options missing from answers
- **Solution**: Check if options use correct format (A., B., C., D.)

**Issue**: Non-MCQ content misinterpreted
- **Solution**: Review option pattern, ensure A-D letters don't appear accidentally

## Use Cases

Perfect for:
- Digitizing handwritten MCQ exam papers
- Processing competitive exam answer sheets
- Converting quiz documents to digital format
- Creating question banks from scanned materials
- Automating exam paper archival

## Performance Tips

- Use high-resolution scans (300+ DPI minimum)
- Ensure good lighting with minimal shadows
- Use black ink on white paper for best contrast
- Keep handwriting neat and well-spaced
- Number questions consistently (1., 2., 3.)
- Write MCQ options clearly with A., B., C., D. format
- Avoid smudges and erasure marks



