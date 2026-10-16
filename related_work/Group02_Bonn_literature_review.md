# Related work: five EEG/GNN studies (2023-2026)

Published results below are not results of this project. Limitations/gaps are reviewer interpretations unless explicitly stated. R5 is an abstract-level review.

## R1

| Field | Review |
|---|---|
| Title | Self-Supervised Learning for Anomalous Channel Detection in EEG Graphs: Application to Seizure Analysis |
| Authors | Thi Kieu Khanh Ho; Narges Armanfard |
| Year | 2023 (AAAI; preprint 2022) |
| Dataset | TUSZ v1.5.2, 19 channels |
| Area | Seizure clip and channel detection |
| Model | EEG-CGS: GCN autoencoder, contrastive and reconstruction losses |
| Graph | Electrodes are nodes; distance, random, correlation and directed-transfer graph variants. |
| Split | Normal-only training: 35,019 clips; held-out test: 8,848 clips including seizures. |
| Metrics | Combined graphs: clip F1 0.534, sensitivity 0.501, specificity 0.974 (Table 3). |
| Strength | Learns from normal data and compares graph variants. |
| Limitation | Channel-localization task requires multichannel signals; cannot transfer unchanged to a single channel. |
| Gap | Contribution of temporal edges in single-channel graphs is not answered by this multichannel experiment. |
| Relation | Motivates controlled edge-rule ablations; numbers are not Bonn targets. |
| Evidence | Full text, graph construction and Tables 1/3. |
| Url | https://arxiv.org/html/2208.07448v4 |

## R2

| Field | Review |
|---|---|
| Title | Dynamic GNNs for Precise Seizure Detection and Classification from EEG Data |
| Authors | Arash Hajisafi; Haowen Lin; Yao-Yi Chiang; Cyrus Shahabi |
| Year | 2024 (arXiv version reviewed) |
| Dataset | TUSZ v1.5.2 |
| Area | Seizure detection and type classification |
| Model | NeuroGNN: modified residual GCN, BiGRU and hierarchical pooling |
| Graph | Electrodes and brain-region meta-nodes; temporal, spatial and semantic edges. |
| Split | Separate test set; training portion divided 9:1 for training/validation; three random runs. |
| Metrics | With pretraining: detection AUROC 0.876 +/- 0.002; classification weighted F1 0.792 +/- 0.004 (Table 2). |
| Strength | Tests each graph component through ablation. |
| Limitation | Requires electrode geometry and brain-region information absent from isolated single-channel segments. |
| Gap | Does temporal order alone add value when spatial information is unavailable? |
| Relation | Supports matching feature inputs and changing one edge mechanism at a time. |
| Evidence | Full text, Sections 3-4 and Table 2. |
| Url | https://arxiv.org/html/2405.09568v1 |

## R3

| Field | Review |
|---|---|
| Title | Sequential graph convolutional network and DeepRNN based hybrid framework for epileptic seizure detection from EEG signal |
| Authors | Ferdaus Anam Jibon; A. R. Jamil Chowdhury; Mahadi Hasan Miraz; Hwang Ha Jin; Mayeen Uddin Khandaker; Sajia Sultana; Sifat Nur; Fazlul Hasan Siddiqui; AHM Kamal; Mohammad Salman; Ahmed A. F. Youssef |
| Year | 2024 |
| Dataset | CHB-MIT and TUH |
| Area | Seizure detection |
| Model | Sequential GCN plus DeepRNN |
| Graph | Pearson-correlation graph; periodogram-based signal processing. |
| Split | CHB-MIT patient-by-patient experiments: 5-fold CV, repeated 10 times. Subject-disjoint testing not established by this description. |
| Metrics | Table 2 accuracy: CHB-MIT 99.007%; TUH 98.08%. |
| Strength | Compares the hybrid against its individual components. |
| Limitation | Reporting inconsistencies: TUH sensitivity/specificity entries differ between Tables 2 and 5. |
| Gap | Need auditable splits and consistent metric reporting before comparing architectures. |
| Relation | Use reproducible split manifests and distinguish patient-specific from unseen-patient claims. |
| Evidence | Full text, Algorithm 1 and Tables 2/3/5. Results transcribed, not independently reproduced. |
| Url | https://journals.sagepub.com/doi/10.1177/20552076241249874 |

## R4

| Field | Review |
|---|---|
| Title | Multi-branch fusion graph neural network based on multi-head attention for childhood seizure detection |
| Authors | Yang Li; Yang Yang; Shangling Song; Hongjun Wang; Mengzhou Sun; Xiaoyun Liang; Penghui Zhao; Baiyang Wang; Na Wang; Qiyue Sun; Zijuan Han |
| Year | 2024 |
| Dataset | CHB-MIT |
| Area | Childhood seizure detection |
| Model | MGCNA: multi-branch GCN with multi-head attention |
| Graph | Spatial-distance, functional-correlation and trainable graphs over channels. |
| Split | Patient-specific 5-fold CV; patient-independent leave-one-subject-out evaluation. |
| Metrics | Table 1: patient-specific accuracy 99.32%, F1 97.76%. Patient-independent accuracy conflicts: 89.45% in Table 2 versus 85.45% in Table 4. |
| Strength | Separately studies patient-specific and patient-independent performance. |
| Limitation | Requires channel locations; reported cross-patient accuracy is internally inconsistent. |
| Gap | Need simple graph ablations with explicit generalization limits. |
| Relation | Supports reporting source grouping and computational cost rather than chasing a published accuracy. |
| Evidence | Full text, Sections 2.8/4.3 and Tables 1/2/4. |
| Url | https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2024.1439607/full |

## R5

| Field | Review |
|---|---|
| Title | Lightweight Graph Neural Network Framework for Seizure Detection Using Single-Channel EEG |
| Authors | Shobha Sharma; Tapan Kumar Gandhi |
| Year | 2026 (online 17 April; PReMI 2025 proceedings) |
| Dataset | Bonn, five categories Z/N/F/S/O |
| Area | EEG segment classification |
| Model | Lightweight GCN |
| Graph | Eight non-overlapping temporal segments per recording; feature-similarity edges. |
| Split | Ten random seeds; split proportions and subject grouping not disclosed in the accessible abstract. |
| Metrics | Across seeds: accuracy 0.87 +/- 0.0147; macro-F1 0.8681 +/- 0.0157. Best-seed accuracy 91%. |
| Strength | Direct precedent for a single-channel temporal-segment graph. |
| Limitation | Only publisher abstract accessible; exact features, edges and split cannot be verified. |
| Gap | The accessible evidence does not isolate the value of temporal-adjacency edges versus similarity edges. |
| Relation | Closest prior work. Propose a controlled extension, not a claim that Bonn GNNs are new. |
| Evidence | Publisher abstract only; full chapter is subscription content. |
| Url | https://link.springer.com/chapter/10.1007/978-3-032-18477-1_47 |

