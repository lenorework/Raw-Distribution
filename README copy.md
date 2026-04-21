# Exam Score Distribution Comparison

This tool automatically generates beautiful comparison charts for exam scores. **Works with ANY two CSV files** - just place them directly in the data folder!

## Quick Start

1. Place exactly 2 CSV files directly in the `data/` folder
2. Run:

```bash
python generate_charts.py
```

The script will automatically compare the two cohorts and generate beautiful distribution charts.

## Important Notes

⚠️ **The script only processes CSV files DIRECTLY in the `data/` folder**

- Files in subdirectories (like `data/Foundational/`) are ignored
- You need exactly 2 CSV files in the `data/` folder
- The script will compare the older cohort vs the newer cohort

## What It Does

**Automatic Processing:**

1. Finds the 2 CSV files directly in the `data/` folder
2. Automatically detects exam type and year from filenames
3. Compares the older vs newer cohort
4. Generates both "Exam Total %" and "Exam Total Scaled" charts (if available)
5. Saves with descriptive filenames based on exam name

## Example Usage

**Current Setup (Comprehensive Clerkship Exam):**

```
data/
  ├── 2019-2020_Med 3_Comprehensive Clerkship Exam_detailed_export.csv
  ├── 2024-2025_Med 3_Comprehensive Clerkship Exam_detailed_export.csv
  └── Foundational/   (ignored - subdirectory)
```

**To Process Different Exams:**

- Just replace the 2 CSV files in `data/` with your new exam files
- Keep other exams organized in subdirectories if needed
- Run the script - it will automatically detect and process the new files

## Output Files

Charts are named automatically based on exam type:

- `{ExamName}_exam_total_percentage_distribution.png` - Raw score comparison
- `{ExamName}_exam_total_scaled_distribution.png` - Scaled score comparison

**Current outputs:**

- `Comprehensive_Clerkship_Exam_exam_total_percentage_distribution.png`
- `Comprehensive_Clerkship_Exam_exam_total_scaled_distribution.png`

## Chart Features

✨ **Enhanced Visual Design:**

- Professional color scheme (blue for older cohort, coral red for newer cohort)
- Bold fonts and clean typography
- Enhanced grid and axis styling
- Elegant legend with shadow and frame
- Student count labels showing year and sample size (n)
- High-resolution output (300 DPI)
- Subtle background coloring for better readability

📊 **Statistics Included:**

- Mean, Median, Standard Deviation
- Min, Max values
- Student count for each cohort

## File Naming Convention

Your CSV files should follow this pattern:

```
YYYY-YYYY_Med [Year]_{ExamName}_detailed_export.csv
```

Examples:

- `2019-2020_Med 1_Foundations_detailed_export.csv`
- `2024-2025_Med 1_Metabolism 1_detailed_export.csv`
- `2019-2020_Med 3_Comprehensive Clerkship Exam_detailed_export.csv`

The script works with any Med year (Med 1, Med 2, Med 3, etc.)

## Requirements

- Python 3.x
- pandas
- matplotlib
- numpy
