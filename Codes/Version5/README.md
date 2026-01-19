# VERSION 5

A Python pipeline that processes handwritten document images and extracts structured question-answer pairs using OCR technology.

## Features

- Batch processing of multiple images from a folder
- OpenCV-based image preprocessing for enhanced OCR accuracy
- Tesseract OCR integration with optimized configuration
- Intelligent question-answer segmentation using pattern matching
- Automatic question mark normalization
- Sequential Q&A numbering
- Saves clean, structured Q&A pairs
- No use of LLMs or semantic models

## Tech Stack

- Python 3.x
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
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\VGMan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
```

## Configuration

Update these paths before running:

```python
IMAGE_FOLDER = r"C:\Users\VGMan\Downloads\Handwritten_OCR_QA\images"
OUTPUT_FOLDER = r"C:\Users\VGMan\Downloads\Handwritten_OCR_QA\outputs"
```

## Usage

1. Place all handwritten images in the `IMAGE_FOLDER`
2. Run the script:
```bash
python ocr_qa_extractor.py
```

3. Check output in `OUTPUT_FOLDER`:
   - `final_qa_clean.txt` - Structured Q&A pairs

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

### 3. Text Cleaning and Formatting
- **Line merging**: Converts newlines to spaces for continuous text
- **Space normalization**: Collapses multiple spaces into single space using regex `\s+`
- **Sentence formatting**: Places sentences on new lines by detecting punctuation (`.?!`)
- Strips extra whitespace from final output

### 4. Question-Answer Segmentation

**Question Detection Rules**:
- Lines starting with numbers (`1.`, `2.`, etc.) or `Q` followed by digit (`Q1`, `Q2`)
- Lines starting with question words: `what`, `why`, `how`, `define`, `explain`, `describe`
- Case-insensitive matching

**Answer Grouping**:
- All lines after a question become the answer
- Multi-line content is joined with spaces
- Continues until next question is detected

### 5. Question Normalization
- Strips trailing question marks
- Adds question mark automatically to ensure consistency
- Format: `question text?`

### 6. Output Formatting
- Sequential numbering (Q1, Q2, Q3...)
- Format: `Q{n}: question?` and `A{n}: answer text`
- Double newline separation between pairs
- UTF-8 encoding for international characters

## Input/Output Examples

### Input: images/exam_page1.png
```
1. What is photosynthesis
Photosynthesis is the process by which plants convert
light energy into chemical energy.

2. Why is water important for plants
Water is essential for photosynthesis and helps
transport nutrients throughout the plant.
```

### Output: final_qa_clean.txt
```
Q1: 1. What is photosynthesis?
A1: Photosynthesis is the process by which plants convert light energy into chemical energy.

Q2: Why is water important for plants?
A2: Water is essential for photosynthesis and helps transport nutrients throughout the plant.
```

## File Structure

```
project/
├── ocr_qa_extractor.py         # Main script
├── images/
│   ├── page1.png               # Input image 1
│   ├── page2.jpg               # Input image 2
│   └── page3.jpeg              # Input image 3
└── outputs/
    └── final_qa_clean.txt      # Structured Q&A pairs
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

## Question Detection Patterns

The script recognizes these question patterns:

| Pattern | Detected |
|---------|----------|
| `1. What is...` | Yes (numbered) |
| `Q1 Why did...` | Yes (Q-prefixed) |
| `What causes...` | Yes (question word) |
| `How does...` | Yes (question word) |
| `Define the term...` | Yes (question word) |
| `explain this concept` | Yes (case-insensitive) |
| `Random statement.` | No |

## Limitations

- Performance depends on handwriting legibility
- Rule-based detection may miss non-standard question formats
- Works best with single-column layouts
- Cannot handle diagrams or images within questions
- No support for multi-part questions (1a, 1b, 1c)
- Requires clear question indicators (numbers, keywords, or question marks)
- May incorrectly split complex multi-sentence questions

## Future Improvements

- Confidence-based OCR filtering
- Support for multi-column layouts
- Better handling of multi-part questions
- Configurable question detection patterns
- JSON/CSV export formats
- GUI interface for easier use
- OCR quality metrics and reporting
- Support for answer key extraction

## Troubleshooting

**Issue**: Tesseract not found
- **Solution**: Verify installation path and update `tesseract_cmd` variable

**Issue**: Poor OCR accuracy
- **Solution**: Use higher resolution scans (300+ DPI), adjust threshold parameters, ensure good lighting

**Issue**: Questions not detected
- **Solution**: Ensure questions start with numbers, Q-prefix, or question words (what, why, how, etc.)

**Issue**: Images processed in wrong order
- **Solution**: Rename files with numeric prefixes (001_page.png, 002_page.png)

**Issue**: Answers incorrectly split across multiple Q&A pairs
- **Solution**: Review question detection patterns, ensure answer text doesn't start with question keywords

**Issue**: Special characters corrupted in output
- **Solution**: Verify UTF-8 encoding support in your text editor

## Use Cases

Perfect for:
- Digitizing handwritten exam papers
- Processing student assignments and quizzes
- Converting interview notes to digital format
- Creating question banks from scanned materials
- Automating document archival

## Performance Tips

- Use high-resolution scans (300+ DPI minimum)
- Ensure good lighting with minimal shadows
- Use black ink on white paper for best contrast
- Keep handwriting neat and well-spaced
- Number questions consistently (1., 2., 3.)
- Start questions with clear keywords
- Avoid smudges and erasure marks
- Process images in batches for efficiency
