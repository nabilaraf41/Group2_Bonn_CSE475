# CSE475 Task 1 - Bonn EEG

Completed empirical EDA and research review using the five user-supplied archives from https://neurophysicsbonn.de/downloads . No mirror datasets or synthetic results.

## Team

| Name | Student ID |
|---|---|
| Md. Anwar Nabil Araf | 2023-2-60-242 |
| Jagannath Banik | 2023-2-60-144 |
| Md Naimul Islam Rafi | 2023-2-60-209 |
| Mst Mahabuba Akter Eka | 2023-1-60-134 |

**Submitted to:** Associate Professor Dr. Raihan ul Islam

**Group number:** 02.

## Main files
- `report/task1/Group02_Bonn_task1_report.pdf`: report with real findings, figures, five-paper review, research gap and limitations.
- `code/task1/Group02_Bonn_task1_eda.ipynb`: executed notebook with outputs and explanations.
- `code/task1/eda.py`: reusable analysis functions.
- `related_work/Group02_Bonn_literature_review.md`: detailed review table (also JSON).
- `data/raw/`: 500 authentic TXT signals, unchanged numerical content.
- `data/provenance.json`: original archive hashes and user-reported source.
- `data/manifest.json`: file IDs and labels; subject_id is null, not inferred.
- `outputs/task1/`: computed statistics, split manifest, figures and interactive HTML.

## Run
1. Extract the full ZIP, preserving folders.
2. Install Python 3.12 and run `python -m pip install -r requirements.txt`.
3. Open `code/task1/Group02_Bonn_task1_eda.ipynb` in Jupyter or VS Code and run all cells. Start within the project folder. A GPU is unnecessary.
4. Open the three `H_*.html` files directly in a browser for offline interaction.

## Rubric map
A: A_dataset_summary.csv, manifest and notebook summary.
B: B_feature_statistics.csv and B_statistics_by_class.csv (quartiles/skewness/kurtosis included).
C: C_raw_quality_audit.csv, C_feature_quality.csv, C_iqr_outlier_flags.csv.
D: D_manifest_class_counts.csv, D_class_balance.png, split_manifest.csv.
E: E_signal_examples.png, E_histograms.png, E_boxplots.png, E_violinplots.png.
F: F_correlations.csv, F_redundant_pairs.csv, F_heatmap.png.
G: G_pca_2d.png, G_pca_coordinates.csv, G_pca_metadata.json.
H: H_pca_interactive.html, H_pca_3d.html, H_rms_interactive.html.
Related work and gap: report and related_work/.

## Scope and limits
All 500 segments were audited. Feature EDA uses a fixed development subset of 300, with 100+100 reserved from feature exploration. Each partition is balanced by class. Seeds: 475 and 476. No model is trained. `train` in split_manifest.csv denotes the provisional development allocation.

These are released-segment IDs, NOT known independent recording or patient IDs. Patient/parent-recording separation cannot be verified. This EDA does not claim subject-wise generalization or instructor approval of a segment-level modelling protocol. Resolve that limitation before Tasks 2-3. No instructor permission was fabricated.

One reviewed paper (R5) was accessible only through its publisher abstract; that evidence limit is stated. The research question is a controlled project extension, not a global novelty claim. Group: 02. Main submission files use the Group02_Bonn prefix.

The data page says 4,096 samples; all uploaded files contain 4,097. All actual samples are retained. Sampling rate: 173.61 Hz. No extra filtering is applied in EDA. Numeric amplitudes are labelled in raw units rather than assuming an undocumented conversion.

The Class Z/O versus N/F/S acquisition difference (scalp versus intracranial) is a confound; five-class separation should not be interpreted as real-world seizure detection capability.

## Dataset citation
Andrzejak RG, Lehnertz K, Mormann F, Rieke C, David P, Elger CE (2001). Indications of nonlinear deterministic and finite-dimensional structures in time series of brain electrical activity: Dependence on recording region and brain state. Physical Review E 64, 061907. https://doi.org/10.1103/PhysRevE.64.061907 . Cite this in addition to the five recent GNN papers.
