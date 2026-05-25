# CIRBP Gene Analysis on DNA Repair

## General Information

### Title
CIRBP Gene Analysis on DNA Repair

### Author Information
- **Principal Investigator:** Dr. Ruben Petreaca (The Ohio State University)
- **Associate / Co-investigator:** Dr. Golrokh Mirzaei (The Ohio State University)
- **Technical Lead / Alternate Contact:** Abhishek Kanakia (Undergraduate Research Intern, Computer Science and Engineering, The Ohio State University)

### Date of Data Collection and Creation
May 19, 2026 – May 25, 2026

### Geographic Location
Columbus, OH, USA

### Funders and Sponsors
The Ohio State University

---

## Sharing / Access Information

### Direct Links to Publicly Accessible Source Data
- **Master Genomic Expression Database:** COSMIC (Catalogue of Somatic Mutations in Cancer) Complete Gene Expression v104 (GRCh37 Build). 
- **Source Link:** https://cancer.sanger.ac.uk/cosmic/download/cosmic/v104/completegeneexpression

### Source Datasets
1. `Cosmic_CompleteGeneExpression_v104_GRCh37.tsv`: The raw, vertical master database (11+ GB) containing Level 3 TCGA RNA-Seq and microarray expression profiling across all human genes and patient cohorts.
2. `CIRBP complete expression.xlsx`: The baseline file provided by Dr. Ruben Petreaca, containing the pre-classified cohort categorization based on *CIRBP* baseline expression.

---

## Data & File Overview

### Repository Directory Structure
Following quality control standards, all operational script binaries and processed datasets are strictly isolated into distinct, task-specific directories to map the experimental workflow clearly.

```text
📁 MIRZAEI, GOLROKH'S FILES - CIRBP_project/
│
├── 📁 .venv/                                       <-- Python virtual environment execution binaries
├── 📁 above_under_expression_sorting_data/         <-- Task 1 Operational Folder
│   ├── 📄 CIRBP_normal.xlsx                       <-- Normal-expressed cohort patient sample IDs
│   ├── 📄 CIRBP_over.xlsx                         <-- Over-expressed cohort patient sample IDs
│   ├── 📄 CIRBP_under.xlsx                        <-- Under-expressed cohort patient sample IDs
│   └── 📄 sample_sort.py                          <-- Code for Task 1 (Cohort Binning)
│
├── 📁 data_sources_original/                       <-- Source Data Storage
│   ├── 📄 CIRBP complete expression.xlsx          <-- Original baseline dataset provided by PI
│   ├── 📄 Cosmic_CompleteGeneExpression_v104...   <-- Raw 11+ GB master database from COSMIC
│   └── 📄 README_Cosmic_CompleteGeneExpression    <-- Source documentation database readme
│
├── 📁 github_documents/                            <-- Project Version Control Documents
│   ├── 📄 .gitignore                              <-- Configuration preventing massive data uploads
│   └── 📄 LICENSE                                 <-- Project distribution license
│
├── 📁 normal_datasets/                             <-- Task 3 Processed Wide Matrices
│   └── ... (Pivoted horizontal CSV files for normal cohorts by cancer type)
│
├── 📁 over_datasets/                               <-- Task 3 Processed Wide Matrices
│   └── ... (Pivoted horizontal CSV files for over cohorts by cancer type)
│
├── 📁 under_datasets/                              <-- Task 2 Processed Wide Matrices
│   └── ... (Pivoted horizontal CSV files for under cohorts by cancer type)
│
├── 📄 desktop.ini                                  <-- Local system configuration file (hidden)
└── 📄 README.md                                    <-- Main project documentation and methodology

```
---

## Methodological Information

This pipeline implements a multi-stage data-engineering workflow designed to isolate specific target sub-populations and cross-reference them against genome-wide transcription expression profiles.

### Stage 1: Cohort Stratification and Binning (Task 1)
- **Input Data:** `CIRBP complete expression.xlsx` (Source: Petreaca Lab).
- **Processing Logic:** A specialized Python sorting routine (`sample_sort.py`) parsed the patient population based on standardized Z-score standard deviation intervals of the CIRBP gene. 
- **Mathematical Thresholding:**
  - **Over-Expressed Cohort:** Samples demonstrating an expression footprint above threshold (Z > 2.0).
  - **Under-Expressed Cohort:** Samples demonstrating an expression footprint below threshold (Z < -2.0).
  - **Normal Cohort:** Samples maintaining steady-state baseline parameters (-2.0 <= Z <= 2.0).
- **Output:** Three decoupled spreadsheets (`CIRBP_over.xlsx`, `CIRBP_under.xlsx`, `CIRBP_normal.xlsx`) capturing unique TCGA patient `SAMPLE_NAME` identifiers.

### Stage 2: Streaming, Filtering, and Extraction (Tasks 2 & 3 - Phase 1)
- **Input Data:** Raw 11GB `Cosmic_CompleteGeneExpression_v104_GRCh37.tsv`.
- **Processing Logic:** To prevent hardware memory execution exhaustion from processing multi-gigabyte data files, the data was chunked using the Python Pandas module.
- **Data Reduction Configuration:** Data streams are read iteratively in hyper-optimized blocks of 50,000 rows. For each block, rows are cross-referenced using high-speed set tracking against the target patient IDs isolated in Stage 1. Unmatched rows are discarded instantly. Missing features are omitted, and columns are stripped down strictly to the target features (`SAMPLE_NAME`, `GENE_SYMBOL`, `Z_SCORE`), discarding auxiliary structural overhead text.
- **Intermediate Storage:** Filtered data rows are isolated and written sequentially to regional, vertical intermediate files (e.g., `_temp_vertical.csv`) categorized by their corresponding TCGA cancer type abbreviation (derived via site codes mapped dynamically from sample identifiers).

### Stage 3: Wide-Matrix Flattening and Dimensional Rotation (Tasks 2 & 3 - Phase 2)
- **Processing Logic:** Downstream biological tools cannot digest vertical long-format database schemas (where a single patient sample is broken across 20,000 unique rows for individual gene readings). To transform these files into standard horizontal genomic matrices, the script opens each regional file and handles multi-sample duplicate sequence anomalies safely via a pivot table aggregation function mapping mathematical mean trends: Wide Matrix Cell = mean(Z_score for that specific Gene and Sample).
- This flattens the file, rotating the database entries dynamically so that each unique patient sample occupies precisely **one horizontal row**, with all 20,000 human genes running alphabetically across the page as independent columns.
- **Output Generation:** The script dumps out clean horizontal data matrices, deletes the massive intermediate vertical file artifacts automatically, and logs successful file execution.

---

## File/Format-Specific Information

- **Cohort Lists (`above_under_expression_sorting_data/`):** Excel files tracking the target patient `SAMPLE_NAME` barcodes and baseline CIRBP `Z_SCORE` metrics generated during Task 1.
- **Expression Matrices (`under_datasets/`, `over_datasets/`, `normal_datasets/`):** Transposed genomic matrices saved as `.csv` files. 
  - **Rows:** Each row represents one unique patient sample.
  - **Columns:** Column 1 is `SAMPLE_NAME`, followed by ~20,000 human genes sorted alphabetically.
  - **Values:** Cells contain relative expression Z-scores.
- **Software Compatibility Warning:** Due to containing ~20,000 gene columns, these matrices exceed the standard Microsoft Excel width limit (16,384 columns) and will truncate if opened in Excel.
