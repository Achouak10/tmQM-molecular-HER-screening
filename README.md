# Machine Learning-Guided Discovery of Metal-Ligand Catalysts

This repository contains the complete reproducible data pipeline, unsupervised machine learning workflows, and candidate screening criteria used to identify viable non-platinum HER catalysts from the tmQM database.

## 📊 Pipeline Sequence
1. **Extraction & Preprocessing**: Extracts identifiers and computes "Molecular Size" using a discrete atom-counting algorithm.
2. **Exploratory Dimensionality Reduction**: PCA tracking on the 5 targeted descriptors.
3. **Unsupervised Partitioning**: Side-by-side clustering implementation utilizing K-Means, DBSCAN, and Gaussian Mixture Models (GMM).
4. **Targeted Selection**: Boundary thresholding, composite scoring, and candidate distribution mapping.

## ⚙️ Reproducibility and Model Configurations
To ensure fully identical replication of clusters and visual graphs, all models must be evaluated under the following rigid parameter criteria:

* **Feature Standardization**: Features are scaled globally via Z-score standardization (`sklearn.preprocessing.StandardScaler`), ensuring zero mean and unit variance across features.
* **Deterministic Random Initialization**: A fixed seed of `random_state=42` is strictly declared across all probabilistic algorithm variants (PCA, K-Means, GMM).
* **Final Model Hyperparameters**:
  * **K-Means**: `n_clusters=6`, `init='k-means++'`, `n_init='auto'` (or `10`)
  * **GMM**: `n_components=6`, `covariance_type='full'`, `init_params='kmeans'`
  * **DBSCAN**: `eps=0.5`, `min_samples=5`

## 🚀 Getting Started
1. Clone this repository to your local directory.
2. Install the pinned package configurations: 
   ```bash
   pip install -r requirements.txt