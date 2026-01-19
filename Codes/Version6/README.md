# VERSION 6

A Python pipeline that processes handwritten document images containing questions and multiple-choice options, extracting structured question-answer pairs while preserving MCQ formatting.

## Features

- Batch processing of multiple images from a folder
- Advanced OpenCV-based image preprocessing with CLAHE and bilateral filtering
- Tesseract OCR integration with line-wise text extraction
- Intelligent question-answer segmentation using pattern matching
- MCQ-aware option detection (A/B/C/D)
- Preserves MCQ options as part of answers
- Automatic question mark normalization
- Sequential Q&A numbering
- Saves both raw OCR output and structured Q&A pairs
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
python advanced_ocr_qa.py
```

3. Check outputs in `OUTPUT_FOLDER`:
   - `raw_text.txt` - Combined raw OCR from all images
   - `qa_pairs.txt` - Structured Q&A pairs with MCQ options

## How It Works

### 1. Advanced Image Preprocessing
- **Grayscale conversion**: Eliminates color noise
- **CLAHE (Contrast Limited Adaptive Histogram Equalization)**: 
  - Clip limit: 2.0
  - Tile grid size: 8x8
  - Enhances local contrast without amplifying noise
- **Bilateral filter**: 
  - Diameter: 9
  - Sigma color: 75
  - Sigma space: 75
  - Removes noise while preserving edges
- **Upscaling**: 2x resize using cubic interpolation for better character recognition
- **Sharpening**: Custom 3x3 kernel `[[0,-1,0],[-1,5,-1],[0,-1,0]]` to enhance text edges
- **Adaptive thresholding**: Gaussian-based binarization with block size 31 and constant 10

### 2. OCR Text Extraction with Line Preservation
- **OEM Mode 3**: Default Tesseract engine (legacy + LSTM)
- **PSM Mode 6**: Assumes uniform block of text
- **Line-wise extraction**: Uses `image_to_data` to preserve line structure
- Groups words by line number for better formatting
- Processes images in alphabetical order
- Concatenates text from all images sequentially

### 3. Question-Answer Segmentation

**Question Detection Rules**:
- Lines ending with `?`
- Lines starting with question keywords: `what`, `why`, `how`, `define`, `explain`, `state`, `list`, `describe`, `give`, `write`
- Lines starting with numbers (`1.`, `2.`, etc.)
- Case-insensitive matching

**MCQ Option Detection**:
- Lines matching pattern `A.`, `B.`, `C.`, `D.` or `A)`, `B)`, `C)`, `D)`
- Regex pattern: `^[A-D][\.\)]`
- Options are treated as part of the answer, NOT as new questions

**Answer Grouping**:
- All lines after a question become the answer
- MCQ options are included in the answer
- Multi-line content is joined with spaces
- Continues until next question is detected

### 4. Question Normalization
- Strips numbered prefixes from questions (e.g., `1.`, `2.`)
- Adds question mark automatically to ensure consistency
- Format: `question text?`

### 5. Output Formatting
- Sequential numbering (Q1, Q2, Q3...)
- Format: `Q{n}: question?` and `A{n}: answer text with options`
- Double newline separation between pairs
- UTF-8 encoding for international characters

## Input/Output Examples

### Input: images/exam_page1.png
```
1. What is the capital of France?
A. London
B. Paris
C. Berlin
D. Madrid

2. Which gas do plants absorb?
A. Oxygen
B. Nitrogen
C. Carbon dioxide
D. Hydrogen
```

### Output: raw_text.txt
```
1. What is the capital of France?
A. London
B. Paris
C. Berlin
D. Madrid

2. Which gas do plants absorb?
A. Oxygen
B. Nitrogen
C. Carbon dioxide
D. Hydrogen
```

### Output: qa_pairs.txt
```
Q1: What is the capital of France?
A1: A. London B. Paris C. Berlin D. Madrid

Q2: Which gas do plants absorb?
A2: A. Oxygen B. Nitrogen C. Carbon dioxide D. Hydrogen
```

## File Structure

```
project/
├── advanced_ocr_qa.py          # Main script
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
| CLAHE Clip Limit | 2.0 | Controls contrast enhancement |
| CLAHE Tile Grid | 8x8 | Size of local regions |
| Bilateral Filter Diameter | 9 | Neighborhood diameter |
| Bilateral Sigma Color | 75 | Filter sigma in color space |
| Bilateral Sigma Space | 75 | Filter sigma in coordinate space |
| Upscale Factor | 2x | Doubles image resolution |
| Interpolation | INTER_CUBIC | Smooth upscaling algorithm |
| Sharpen Kernel | Custom 3x3 | Edge enhancement matrix |
| Threshold Method | ADAPTIVE_GAUSSIAN | Local adaptive binarization |
| Block Size | 31 | Neighborhood size for threshold |
| Constant | 10 | Subtracted from weighted mean |

## OCR Configuration

| Parameter | Value | Purpose |
|-----------|-------|---------|
| OEM | 3 | Default Tesseract engine mode |
| PSM | 6 | Uniform block of text |
| Output Type | DICT | Line-wise structured data |

## Supported Image Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)

## Question Detection Keywords

The script recognizes these question starter words (case-insensitive):

| Keyword | Example |
|---------|---------|
| what | What is photosynthesis? |
| why | Why does water boil? |
| how | How does gravity work? |
| define | Define momentum. |
| explain | Explain the water cycle. |
| state | State Newton's first law. |
| list | List three types of rocks. |
| describe | Describe cellular respiration. |
| give | Give an example of a mammal. |
| write | Write the formula for water. |

## MCQ Option Detection Patterns

The script recognizes these MCQ option patterns:

| Pattern | Detected |
|---------|----------|
| `A. Option text` | Yes |
| `B. Option text` | Yes |
| `C. Option text` | Yes |
| `D. Option text` | Yes |
| `A) Option text` | Yes |
| `B) Option text` | Yes |
| `E. Option text` | No (only A-D) |
| `a. Option text` | No (uppercase only) |

## Key Differences from Basic OCR

| Feature | Basic OCR | Advanced OCR |
|---------|-----------|--------------|
| Contrast Enhancement | None | CLAHE algorithm |
| Noise Reduction | Median blur | Bilateral filter (edge-preserving) |
| Edge Enhancement | None | Custom sharpening kernel |
| Line Preservation | Lost during merging | Preserved with line_num tracking |
| MCQ Detection | Not supported | Regex pattern matching |
| Question Keywords | 6 keywords | 10 keywords |
| Option Format | N/A | Supports both `.` and `)` |

## Limitations

- Performance depends on handwriting legibility
- Only supports A/B/C/D options (not E, F, etc.)
- Case-sensitive option detection (lowercase a/b/c/d not recognized)
- Cannot handle diagrams or images within questions
- Works best with single-column layouts
- No support for multi-part questions (1a, 1b, 1c)
- Requires clear question indicators
- CLAHE may over-enhance very poor quality images

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
- Configurable preprocessing parameters
- OCR quality metrics and reporting

## Troubleshooting

**Issue**: Tesseract not found
- **Solution**: Verify installation path and update `tesseract_cmd` variable

**Issue**: Image not found error
- **Solution**: Check that images exist in IMAGE_FOLDER and paths are correct

**Issue**: MCQ options detected as separate questions
- **Solution**: Ensure options follow A/B/C/D format with period or parenthesis

**Issue**: Poor OCR accuracy despite preprocessing
- **Solution**: Use higher resolution scans (300+ DPI), adjust CLAHE parameters, ensure good lighting

**Issue**: Over-enhanced or washed out images
- **Solution**: Reduce CLAHE clip limit (try 1.5 or 1.0)

**Issue**: Options missing from answers
- **Solution**: Check if options use correct format (A., B., C., D. or A), B), C), D))

**Issue**: Lines merged incorrectly
- **Solution**: Verify line_num extraction is working, check for consistent line spacing in images

**Issue**: Excessive noise in output
- **Solution**: Increase bilateral filter diameter or adjust sigma values

## Use Cases

Perfect for:
- Digitizing handwritten MCQ exam papers
- Processing competitive exam answer sheets
- Converting quiz documents to digital format
- Creating question banks from scanned materials
- Automating exam paper archival
- Educational content digitization
- Student assessment processing

## Performance Tips

- Use high-resolution scans (300+ DPI minimum)
- Ensure good lighting with minimal shadows
- Use black ink on white paper for best contrast
- Keep handwriting neat and well-spaced
- Number questions consistently (1., 2., 3.)
- Write MCQ options clearly with A., B., C., D. format
- Avoid smudges and erasure marks
- Process images in batches for efficiency
- Maintain consistent line spacing between questions
- Use clean, uncrumpled paper for scanning

## Advanced Preprocessing Benefits

**CLAHE (Contrast Limited Adaptive Histogram Equalization)**:
- Superior to global histogram equalization
- Prevents over-amplification of noise
- Works well with varying lighting conditions
- Ideal for handwritten documents with inconsistent ink density

**Bilateral Filtering**:
- Better than Gaussian blur for text
- Preserves sharp edges while removing noise
- Prevents text from becoming blurry
- Maintains character boundaries

**Sharpening Kernel**:
- Enhances text edges after resizing
- Improves Tesseract's character recognition
- Compensates for slight blur from bilateral filter
- Makes thin strokes more prominent

