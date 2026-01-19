# VERSION 1 


A standalone Python script that intelligently organizes messy OCR-extracted text into clean, structured question-answer pairs using rule-based heuristics.

## Features

- Processes raw OCR output into structured Q&A format
- Multi-strategy question detection (punctuation, numbering, keywords)
- Automatic question mark addition for proper formatting
- Sequential Q&A numbering (Q1, Q2, Q3...)
- Answer grouping and multi-line merging
- Removes old numbering and cleans questions
- No external dependencies - uses only Python standard library

## Tech Stack

- Python 3.6+
- Regular Expressions (re module)
- File I/O (os module)

## Installation

No installation required! Just Python 3.6+ needed.

```bash
# Verify Python version
python --version
```

## Configuration

Update file paths in the script before running:

```python
INPUT_TEXT_FILE = r"C:\path\to\raw_ocr_text.txt"
OUTPUT_QA_FILE = r"C:\path\to\qa_pairs.txt"
```

## Usage

```bash
python qa_separator.py
```

## How It Works

### 1. Text Input
- Reads raw OCR text from input file
- Splits into lines and removes empty lines
- Processes line-by-line for question detection

### 2. Question Detection (Three Rules)
Identifies questions using intelligent heuristics:

**Rule 1: Punctuation-based**
- Lines ending with `?` are detected as questions

**Rule 2: Numbering-based**
- Lines starting with `1.`, `2.`, `Q1`, `Q2`, etc.

**Rule 3: Keyword-based**
- Lines starting with question keywords:
  - what, why, how
  - define, explain, state
  - list, describe, give, write

### 3. Answer Grouping
- All lines after a question are treated as the answer
- Continues until the next question is detected
- Multi-line answers are joined with spaces
- Preserves complete answer content

### 4. Question Cleaning
- Removes old numbering (strips `1.`, `Q1`, etc.)
- Adds missing question marks
- Trims whitespace for clean formatting

### 5. Sequential Renumbering
- Renumbers all questions as Q1, Q2, Q3...
- Renumbers all answers as A1, A2, A3...
- Ensures consistent output format

### 6. Output Generation
- Writes formatted Q&A pairs to output file
- UTF-8 encoding for international character support
- Double newline separation between pairs

## Input/Output Examples

### Input: raw_ocr_text.txt
```
1. what is photosynthesis
Plants use sunlight to make food
through chlorophyll in leaves

2 Why is water important
Water is essential for all living
organisms to survive

How does gravity work
It pulls objects toward each other
```

### Output: qa_pairs.txt
```
Q1: What is photosynthesis?
A1: Plants use sunlight to make food through chlorophyll in leaves

Q2: Why is water important?
A2: Water is essential for all living organisms to survive

Q3: How does gravity work?
A3: It pulls objects toward each other
```

## File Structure

```
project/
├── qa_separator.py             # Main script
└── outputs/
    ├── raw_ocr_text.txt        # Input: Raw OCR text
    └── qa_pairs.txt            # Output: Structured Q&A
```

## Detection Logic

### Question Pattern Examples

| Input Pattern | Detected As | Cleaned Output |
|---------------|-------------|----------------|
| `1. What is AI?` | Question | `What is AI?` |
| `Q2 Why is it useful` | Question | `Why is it useful?` |
| `Define machine learning` | Question | `Define machine learning?` |
| `How does it work?` | Question | `How does it work?` |
| `Explain the concept` | Question | `Explain the concept?` |

### Answer Pattern Examples

| Input | Behavior |
|-------|----------|
| Single line after question | Treated as complete answer |
| Multiple lines after question | Joined into single answer |
| Empty lines | Ignored/skipped |
| Lines before first question | Ignored |

## Question Keywords

The script recognizes these question starter words:

- **what** - What is, What are, What does
- **why** - Why is, Why do, Why should
- **how** - How does, How can, How to
- **define** - Define the term
- **explain** - Explain the concept
- **state** - State the law
- **list** - List the features
- **describe** - Describe the process
- **give** - Give examples
- **write** - Write about

## Processing Guarantees

The script guarantees:
- Every question ends with `?`
- Proper sequential numbering (Q1, A1, Q2, A2...)
- Answers appear under correct questions
- No duplicate numbering
- No empty questions or answers

## Edge Cases Handled

- Questions without question marks → Adds `?`
- Questions with old numbering → Removes and renumbers
- Multi-line answers → Joins into single paragraph
- Mixed numbering formats → Normalizes to Q1, Q2, Q3
- Leading/trailing whitespace → Strips cleanly
- Empty lines → Filters out

## Limitations

- Requires questions to follow one of three detection rules
- Cannot detect questions phrased as statements
- May misclassify answers starting with keywords
- Works best with clear question-answer structure
- No semantic understanding (rule-based only)
- Cannot handle nested or follow-up questions
- No support for multi-part questions (a, b, c)

## Future Improvements

- Support for sub-questions (1a, 1b, 1c)
- Custom keyword dictionary via config file
- Confidence scoring for question detection
- HTML/Markdown output formats
- Batch processing of multiple files
- Interactive mode for ambiguous cases
- JSON export option
- Question type classification (what/why/how)

## Troubleshooting

**Issue**: Questions not detected
- **Solution**: Ensure questions end with `?` or start with keywords/numbers

**Issue**: Answers split incorrectly
- **Solution**: Check if answer lines accidentally match question patterns

**Issue**: File not found error
- **Solution**: Verify input file path exists and is readable

**Issue**: Unicode decode error
- **Solution**: Ensure input file is UTF-8 encoded

**Issue**: Empty output file
- **Solution**: Check if input contains detectable questions

**Issue**: Wrong question grouping
- **Solution**: Add clearer question markers (numbers, keywords, `?`)

## Use Cases

Perfect for:
- Organizing OCR output from exam papers
- Structuring interview transcripts
- Processing FAQ documents
- Cleaning up questionnaire scans
- Converting notes to Q&A format
- Preparing study materials

## Performance

- **Speed**: Processes ~1000 lines per second
- **Memory**: Minimal (entire file loaded into memory)
- **Scalability**: Suitable for documents up to 10,000 Q&A pairs

## Example Workflow

1. **Extract text** using OCR tool (Tesseract, Google Vision, etc.)
2. **Save** raw OCR output to `raw_ocr_text.txt`
3. **Run** this script: `python qa_separator.py`
4. **Review** structured output in `qa_pairs.txt`
5. **Edit** manually if needed for edge cases


