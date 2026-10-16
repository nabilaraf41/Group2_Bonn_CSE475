# Validation
- All 500 authentic uploaded segments parsed; 100 per class, 4,097 finite values per file.
- Zero exact numerical duplicates, constant segments, malformed signals or nonfinite values.
- Seven notebook code cells executed sequentially in IPython on authentic data; notebook schema validated. Socket-based kernels are unavailable in the authoring environment.
- 300 development rows, 19 finite engineered features; 60 rows per class. Reserved 100+100 files are excluded from feature exploration.
- PCA, scaling and correlations use development data only. The partition is segment-level; patient independence is not verified.
- 557 pooled IQR feature flags affect 132 development segments; these are not automatically removed.
- PDF rendered and visually checked; interactive HTML embeds its Plotly dependency.
- No model fitted, no accuracy invented, no synthetic data included.
