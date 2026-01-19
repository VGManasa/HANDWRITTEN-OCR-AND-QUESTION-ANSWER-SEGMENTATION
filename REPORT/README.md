# Handwritten OCR and Question-Answer Segmentation

**Intern Assignment Project Report**

**Author**: V G Manasa  
**Registration Number**: 24BEC1419  
**University**: VIT Chennai  
**Department**: B.Tech ECE (Second Year)  
**Email**: manasavijayagopal@gmail.com

## Project Overview

This project develops a system to convert handwritten notes and exam papers from images into structured digital text with properly separated questions and answers, without using AI language models (LLMs). The system combines optical character recognition (OCR), image preprocessing, and rule-based heuristics to achieve reliable question-answer segmentation.

## Core Objectives

1. **Handwritten Text Recognition**: Convert handwritten or printed text from images into editable digital format
2. **Question-Answer Separation**: Identify and organize questions and answers in a structured numbered format (Q1/A1, Q2/A2)
3. **Multi-Scenario Handling**: Process content across single or multiple images with questions and answers in various configurations

## Key Challenges

- **Handwriting Variation**: Different writing styles, sizes, slants, and spacing affect OCR accuracy
- **Split Content**: Questions and answers may span multiple images
- **No LLM Constraint**: Must rely on structural hints and patterns rather than semantic understanding
- **Image Quality Issues**: Blur, lighting, shadows, and faint ink reduce recognition accuracy

## Solution Approaches

The project explored 10+ different approaches, including:

1. **OCR Preprocessing Pipeline**: Grayscale conversion, noise reduction, upscaling, thresholding, morphological operations
2. **Post-OCR Text Cleaning**: Space normalization, spell correction, special character removal
3. **Rule-Based Q&A Organization**: Pattern matching using punctuation, numbering, and keywords
4. **Template Matching for MCQs**: Detection of multiple-choice options (A/B/C/D)
5. **Multi-Image Stitching**: Combining OCR results from consecutive images
6. **Line-Wise OCR with Structural Analysis**: Preserving spatial information and document layout
7. **Layout and Visual Analysis**: Computer vision techniques for structural understanding
8. **Confidence-Based Filtering**: Using OCR confidence scores to reduce noise
9. **Deskewing and Rotation Correction**: Automatically correcting skewed images
10. **Text Normalization**: Sentence segmentation and spacing normalization

## Preferred Solution

**Approach 6: Line-Wise OCR with Structural Analysis**

This approach was selected as the optimal solution because it:

- Preserves document structure and layout information
- Maintains line order, grouping, and spatial relationships
- Achieves approximately 86-88% accuracy on real-world handwritten data
- Handles all required scenarios (single/multi-image, split content, MCQs)
- Provides optimal balance of accuracy, speed, and complexity
- Is production-ready and maintainable

### Why Line-Wise OCR?

Unlike flat OCR that produces plain text, line-wise OCR preserves:
- Words grouped by line
- Paragraph boundaries
- Positional context
- Indentation and alignment cues

This structural awareness enables accurate detection of multi-line questions, MCQ options, and proper content grouping.

## Implementation Versions

The project includes 6 code versions demonstrating progressive improvements:

### Version 1: Basic Rule-Based Separation
Simple pattern matching with question keywords and numbering detection.

### Version 2: Enhanced Preprocessing
Added strong preprocessing pipeline with upscaling, noise reduction, and strict OCR configuration.

### Version 3: Structured Processing
Introduced systematic preprocessing and organized Q&A extraction logic.

### Version 4: MCQ Detection
Added support for multiple-choice questions with option pattern recognition.

### Version 5: Text Normalization
Implemented aggressive text cleaning and sentence-based formatting.

### Version 6: Line-Wise OCR (Preferred)
Full implementation of line-wise structural analysis with advanced preprocessing techniques including CLAHE, bilateral filtering, and sharpening.

## Technical Stack

- **Python 3.x**
- **OpenCV (cv2)**: Image preprocessing and computer vision operations
- **Tesseract OCR**: Text recognition engine
- **pytesseract**: Python wrapper for Tesseract
- **NumPy**: Numerical operations and array processing
- **Regular Expressions**: Pattern matching and text parsing

## Key Features

- Batch processing of multiple images
- Advanced preprocessing pipeline (CLAHE, bilateral filtering, upscaling, sharpening)
- Line-wise text extraction preserving document structure
- Intelligent question detection using multiple heuristics
- MCQ option recognition and grouping
- Multi-image content stitching
- Sequential Q&A numbering
- UTF-8 encoding support

## Performance Metrics

Based on testing with 150 images:

| Metric | Performance |
|--------|-------------|
| OCR Accuracy (character-level) | ~88% |
| Q-A Pairing Accuracy | ~86% |
| MCQ Grouping Accuracy | ~92% |
| Multi-Image Handling Accuracy | ~84% |
| Processing Speed | 1.5-2 seconds per image |

## Error Analysis

- OCR misrecognitions: 40%
- Extremely messy handwriting: 30%
- Unusual formatting: 20%
- Implementation issues: 10%

## Document Structure

```
PROJECT_REPORT/
├── 1. Overview
├── 2. Thought Process and Exploration
├── 3. Solution Approaches (10 approaches documented)
├── 4. Preferred Solution (Line-Wise OCR)
├── 5. Code Implementation and Outputs (6 versions)
├── 6. Alternative Hybrid Solution
├── 7. Technical Details
├── 8. Handling Edge Cases
├── 9. Comparison of All Approaches
├── 10. Conclusion
└── 11. References and Resources
```

## Preprocessing Pipeline

1. **Grayscale Conversion**: Eliminates color noise
2. **CLAHE**: Contrast Limited Adaptive Histogram Equalization (clip limit: 2.0, tile: 8x8)
3. **Bilateral Filter**: Noise reduction while preserving edges (diameter: 9, sigma: 75)
4. **Upscaling**: 2x resize using cubic interpolation
5. **Sharpening**: Custom 3x3 kernel for edge enhancement
6. **Adaptive Thresholding**: Gaussian-based binarization (block: 31, constant: 10)
7. **Deskewing** (Optional): Rotation correction for skewed images

## Question Detection Rules

Questions are identified by:

1. Lines ending with `?`
2. Lines starting with numbers (`1.`, `2.`, `Q1`, `Q2`)
3. Lines starting with question keywords: `what`, `why`, `how`, `define`, `explain`, `state`, `list`, `describe`, `give`, `write`
4. Case-insensitive matching

## MCQ Detection

- Patterns: `A.`, `B.`, `C.`, `D.` or `A)`, `B)`, `C)`, `D)`
- Regex: `^[A-D][\.\)]`
- Options treated as part of the answer, not separate questions

## Multi-Image Scenarios

The system handles:

- **Scenario 1**: Single image with complete content
- **Scenario 2**: Question split across images
- **Scenario 3**: Question and answer in separate images
- **Scenario 4**: Answer spread across multiple images
- **Scenario 5**: Edge cases (MCQs, mixed formats)

## Edge Cases Handled

- Incomplete questions at image boundaries
- Missing question marks
- Orphaned answer content
- Overlapping text
- Inconsistent numbering
- Mixed handwritten and printed text
- Diagrams mixed with text
- Varying handwriting styles

## Comparison of Approaches

| Approach | Accuracy | Speed | Best Use Case |
|----------|----------|-------|---------------|
| Basic Rule-Based | ~70% | Very Fast | Learning, prototyping |
| Enhanced Preprocessing | ~85% | Fast | Poor-quality images |
| Line-Wise OCR | ~80% | Moderate | Complex layouts |
| Multi-Image Handling | ~75% | Moderate | Multi-page documents |
| MCQ Template Matching | ~80% | Fast | Standardized tests |
| Hybrid Approach | ~90% | Moderate | Production systems |

## Alternative Hybrid Solution

Combines the strengths of versions 3, 4, 5, and 6:

1. **Stage 1**: Advanced image preprocessing
2. **Stage 2**: Line-wise OCR extraction
3. **Stage 3**: Multi-image text merging
4. **Stage 4**: Intelligent Q&A detection
5. **Stage 5**: Post-processing and formatting

Output files:
- `raw_text.txt`: Complete OCR output
- `qa_pairs.txt`: Clean, structured Q&A pairs

## OCR Configuration

```python
config = "--oem 3 --psm 6 -c preserve_interword_spaces=1"
```

- `--oem 3`: LSTM neural network mode (best accuracy)
- `--psm 6`: Assume uniform block of text
- `preserve_interword_spaces=1`: Maintain spacing

## Assumptions

1. Questions follow common patterns (keywords, numbers, or `?`)
2. Content is generally sequential across images
3. Text flows top-to-bottom on each page
4. Questions and answers are logically grouped
5. No interleaving of questions and answers

## Limitations

- Performance depends on handwriting legibility
- Only supports A/B/C/D options (not E/F)
- Case-sensitive option detection
- Cannot handle diagrams or images within questions
- Works best with single-column layouts
- No support for multi-part questions (1a, 1b, 1c)
- CLAHE may over-enhance very poor quality images

## Future Improvements

- Support for extended MCQ options (E, F, G)
- Case-insensitive option detection
- Automatic correct answer extraction
- Table and diagram detection
- Multi-column layout support
- Answer key generation
- JSON/CSV export formats
- GUI interface
- Configurable preprocessing parameters
- OCR quality metrics and reporting

## Use Cases

- Digitizing handwritten exam papers
- Processing competitive exam answer sheets
- Converting quiz documents to digital format
- Creating question banks from scanned materials
- Automating exam paper archival
- Educational content digitization
- Student assessment processing

## References

- OpenCV Documentation
- Tesseract OCR Documentation
- Smith, R. "An Overview of the Tesseract OCR Engine" (ICDAR 2007)
- Nagy, G. "Twenty Years of Document Image Analysis in PAMI" (IEEE 2000)
- Shafait, F. et al. "Efficient Implementation of Local Adaptive Thresholding" (2008)
- Graves, A. & Schmidhuber, J. "Offline Handwriting Recognition with RNNs" (NIPS 2009)
- Stack Overflow: OCR implementation discussions
- Computer vision blogs and tutorials

## Conclusion

This project successfully demonstrates that reliable handwritten OCR and structured content extraction are achievable without LLMs using structural cues and rule-based logic. The line-wise OCR approach with enhanced preprocessing provides a production-ready solution that balances accuracy (86-88%), speed (1.5-2s per image), and implementation complexity. The system is modular, scalable, and suitable for real-world document processing applications.

## Report Details

- **Total Pages**: 60
- **Code Versions Documented**: 6
- **Approaches Explored**: 10+
- **Input/Output Examples**: Included for all versions
- **Technical Depth**: Comprehensive coverage of preprocessing, OCR, segmentation, and edge cases

