#!/usr/bin/env python
"""
Generate beautiful comparison distribution charts for Exam Total % and Exam Total Scaled
Automatically detects and processes CSV files in the data folder
Creates overlapping histograms comparing older vs newer cohorts
"""
from pathlib import Path
import re
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Must be before importing pyplot

# Set style for beautiful plots
plt.style.use('seaborn-v0_8-darkgrid')
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
matplotlib.rcParams['axes.labelweight'] = 'bold'
matplotlib.rcParams['axes.titleweight'] = 'bold'


def find_csv_files(data_folder):
    """Find CSV files directly in data folder (not subdirectories)"""
    csv_files = []
    # Only look at files directly in the data folder, not subdirectories
    if os.path.exists(data_folder):
        for file in os.listdir(data_folder):
            filepath = os.path.join(data_folder, file)
            if os.path.isfile(filepath) and file.endswith('.csv'):
                csv_files.append(filepath)
    return csv_files


def extract_info_from_filename(filepath):
    """Extract year and exam name from filename"""
    filename = os.path.basename(filepath)
    # Extract year pattern like 2019-2020, 2025-2026, etc.
    year_match = re.search(r'(\d{4}-\d{4})', filename)
    year = year_match.group(1) if year_match else "Unknown"

    # Extract exam name (e.g., "Foundations", "Metabolism 1", "Comprehensive Clerkship Exam")
    name_match = re.search(r'Med \d+_(.*?)_detailed_export', filename)
    exam_name = name_match.group(1) if name_match else "Exam"

    return year, exam_name


def group_files_by_exam(csv_files):
    """Group CSV files by exam name"""
    exam_groups = {}

    for filepath in csv_files:
        year, exam_name = extract_info_from_filename(filepath)

        if exam_name not in exam_groups:
            exam_groups[exam_name] = []

        exam_groups[exam_name].append({
            'path': filepath,
            'year': year,
            'year_start': int(year.split('-')[0]) if '-' in year else 0
        })

    # Sort each group by year
    for exam_name in exam_groups:
        exam_groups[exam_name].sort(key=lambda x: x['year_start'])

    return exam_groups


def create_beautiful_chart(scores_old, scores_new, year_old, year_new, column_name, filename, exam_name):
    """Create a beautiful comparison histogram chart"""

    fig, ax = plt.subplots(figsize=(14, 7), facecolor='white')

    # Define bins
    bins = np.arange(35, 100, 5)

    # Create overlapping histograms with clean, solid colors
    n1, bins1, patches1 = ax.hist(scores_old, bins=bins, alpha=0.8,
                                  color='#6B9FFF', edgecolor='#2C5AA0',
                                  linewidth=1.3, label=f'{year_old} Cohort',
                                  zorder=3)

    n2, bins2, patches2 = ax.hist(scores_new, bins=bins, alpha=0.8,
                                  color='#FF6B6B', edgecolor='#CC4444',
                                  linewidth=1.3, label=f'{year_new} Cohort',
                                  zorder=3)

    # Customize axes and labels
    ax.set_xlabel('Raw Score (%)', fontsize=15, fontweight='bold', labelpad=10)
    ax.set_ylabel('Number of Students', fontsize=15,
                  fontweight='bold', labelpad=10)
    title = f'Comparison of {exam_name} {column_name} Distributions: {year_old} vs. {year_new} Cohorts'
    ax.set_title(title, fontsize=17, fontweight='bold', pad=20)

    # Enhance grid
    ax.grid(True, axis='y', alpha=0.4, linestyle='-',
            linewidth=0.8, color='gray', zorder=1)
    ax.set_axisbelow(True)

    # Set x-axis ticks
    ax.set_xticks(range(40, 100, 10))
    ax.tick_params(axis='both', which='major',
                   labelsize=12, width=1.5, length=6)

    # Set y-axis to start from 0
    ax.set_ylim(bottom=0)

    # Add student count annotations at the top left
    ax.text(0.02, 0.98, f'{year_old}: n={len(scores_old)}',
            transform=ax.transAxes, fontsize=12, fontweight='bold',
            verticalalignment='top', horizontalalignment='left',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#5B8FF9',
                      edgecolor='#1F2937', alpha=0.8, linewidth=1.5),
            color='white')

    ax.text(0.02, 0.88, f'{year_new}: n={len(scores_new)}',
            transform=ax.transAxes, fontsize=12, fontweight='bold',
            verticalalignment='top', horizontalalignment='left',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FF7A7A',
                      edgecolor='#1F2937', alpha=0.8, linewidth=1.5),
            color='white')

    # Enhanced legend with frame
    legend = ax.legend(fontsize=13, loc='upper right', frameon=True,
                       shadow=True, fancybox=True, framealpha=0.95)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('#999999')
    legend.get_frame().set_linewidth(1.5)

    # Add subtle background color
    ax.set_facecolor('#FAFAFA')

    # Adjust spines
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
        spine.set_edgecolor('#333333')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"✓ Chart saved: {filename}")
    plt.close(fig)

    # Print statistics
    print(f"\n{column_name} - {year_old} Cohort Statistics:")
    print(f"  Mean:    {scores_old.mean():.2f}%")
    print(f"  Median:  {scores_old.median():.2f}%")
    print(f"  Std Dev: {scores_old.std():.2f}")
    print(f"  Min:     {scores_old.min():.2f}%")
    print(f"  Max:     {scores_old.max():.2f}%")
    print(f"  Count:   {len(scores_old)}")

    print(f"\n{column_name} - {year_new} Cohort Statistics:")
    print(f"  Mean:    {scores_new.mean():.2f}%")
    print(f"  Median:  {scores_new.median():.2f}%")
    print(f"  Std Dev: {scores_new.std():.2f}")
    print(f"  Min:     {scores_new.min():.2f}%")
    print(f"  Max:     {scores_new.max():.2f}%")
    print(f"  Count:   {len(scores_new)}")


def main():
    # Find CSV files directly in the data folder only
    data_folder = "data"

    print("="*70)
    print("  EXAM SCORE DISTRIBUTION COMPARISON GENERATOR")
    print("  Processing CSV Files in Data Folder")
    print("="*70)

    print(f"\n🔍 Searching for CSV files in '{data_folder}' folder...")
    csv_files = find_csv_files(data_folder)

    if not csv_files:
        print(f"❌ No CSV files found in '{data_folder}' folder!")
        return

    if len(csv_files) < 2:
        print(
            f"⚠️  Found only {len(csv_files)} CSV file - need 2 files for comparison!")
        return

    if len(csv_files) > 2:
        print(
            f"⚠️  Found {len(csv_files)} CSV files - will use the first 2 for comparison")

    # Sort files by year (older first)
    files_with_info = []
    for filepath in csv_files:
        year, exam_name = extract_info_from_filename(filepath)
        year_start = int(year.split('-')[0]) if '-' in year else 0
        files_with_info.append({
            'path': filepath,
            'year': year,
            'exam_name': exam_name,
            'year_start': year_start
        })

    files_with_info.sort(key=lambda x: x['year_start'])

    # Take first two files (oldest and next)
    file_old = files_with_info[0]
    file_new = files_with_info[1]

    print(f"\n📋 Files to compare:")
    print(
        f"   • Older: {os.path.basename(file_old['path'])} ({file_old['year']})")
    print(
        f"   • Newer: {os.path.basename(file_new['path'])} ({file_new['year']})")

    exam_name = file_old['exam_name']

    print(f"\n{'='*70}")
    print(f"📊 Processing: {exam_name}")
    print(f"   Comparing {file_old['year']} vs {file_new['year']}")
    print("="*70)

    # Read the CSV files (skip first row which is the title)
    print("\n📂 Reading CSV files...")
    df_old = pd.read_csv(file_old['path'], skiprows=1)
    df_new = pd.read_csv(file_new['path'], skiprows=1)
    print(f"   • Loaded {len(df_old)} students from {file_old['year']}")
    print(f"   • Loaded {len(df_new)} students from {file_new['year']}")

    # Check if required columns exist
    if 'Exam Total %' not in df_old.columns or 'Exam Total %' not in df_new.columns:
        print(f"   ⚠️  Missing 'Exam Total %' column - cannot generate charts")
        return

    # Clean exam name for filename
    safe_exam_name = exam_name.replace(' ', '_').replace('/', '_')

    total_charts = 0

    # Chart 1: Exam Total %
    print(f"\n📈 Generating Chart 1: Exam Total % Distribution...")
    scores_pct_old = df_old['Exam Total %'].dropna()
    scores_pct_new = df_new['Exam Total %'].dropna()

    filename_pct = f'{safe_exam_name}_exam_total_percentage_distribution.png'
    create_beautiful_chart(
        scores_pct_old,
        scores_pct_new,
        file_old['year'],
        file_new['year'],
        'Exam Total %',
        filename_pct,
        exam_name
    )
    total_charts += 1

    # Chart 2: Exam Total Scaled (if it exists)
    if 'Exam Total Scaled' in df_old.columns and 'Exam Total Scaled' in df_new.columns:
        print(f"\n📈 Generating Chart 2: Exam Total Scaled Distribution...")
        scores_scaled_old = df_old['Exam Total Scaled'].dropna()
        scores_scaled_new = df_new['Exam Total Scaled'].dropna()

        filename_scaled = f'{safe_exam_name}_exam_total_scaled_distribution.png'
        create_beautiful_chart(
            scores_scaled_old,
            scores_scaled_new,
            file_old['year'],
            file_new['year'],
            'Exam Total Scaled',
            filename_scaled,
            exam_name
        )
        total_charts += 1
    else:
        print(f"   ℹ️  'Exam Total Scaled' column not found - skipping scaled chart")

    print("\n" + "="*70)
    print(f"✅ COMPLETED! Generated {total_charts} chart(s) successfully!")
    print("="*70)


if __name__ == "__main__":
    main()
