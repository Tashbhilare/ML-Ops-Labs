# MLMD Lab 1: Tracking a Sports Analytics ML Pipeline with ML Metadata

**Author:** Tanish Bhilare  
**Course:** IE 7374 -- Machine Learning Operations (MLOps), Northeastern University  
**Original Lab:** [raminmohammadi/MLOps -- MLMD Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/MLMD_Labs)

## Overview

This lab demonstrates how to use [ML Metadata (MLMD)](https://www.tensorflow.org/tfx/guide/mlmd) to record, query, and trace lineage across an end-to-end ML pipeline. Rather than the generic training example from the original repository, this version is built around a **football (soccer) player market valuation pipeline** using Bundesliga match event data.

The pipeline tracks four stages through MLMD:
```
Data Ingestion --> Feature Engineering --> Model Training --> Model Evaluation
```

Two full pipeline runs are recorded, allowing side-by-side experiment comparison entirely through MLMD queries.

## What Changed from the Original Lab

| Aspect | Original Lab | This Version |
|---|---|---|
| **Domain** | Generic ML training (DataSet, SavedModel) | Football player valuation (match events, player features, valuation models) |
| **Artifact types** | 2 (DataSet, SavedModel) | 4 (MatchEventData, PlayerFeatureSet, ValuationModel, EvaluationMetrics) |
| **Pipeline steps** | Single trainer execution | 4 steps: Ingest, Feature Engineer, Train, Evaluate |
| **Context usage** | Single experiment | Season-based experiment grouping with two runs |
| **Querying** | Basic artifact retrieval | Recursive upstream lineage tracing, conditional filter queries, experiment comparison |

## How to Run

> **Note:** `ml-metadata` does not support Python 3.12 or Apple Silicon natively. The recommended way to run this notebook is on **Google Colab**.

1. Open the notebook in [Google Colab](https://colab.research.google.com/) by uploading `mlmd_sports_analytics_lab1.ipynb`
2. Run all cells sequentially (**Runtime > Run all**)
3. The first cell installs Python 3.10 and `ml-metadata`. The main cell uses `%%script python3.10` to execute the pipeline.

### Alternative: Local (Linux x86 with Python 3.10)
```bash
git clone https://github.com/Tashbhilare/ML-Ops-Labs.git
cd ML-Ops-Labs/MLMD_Labs
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
jupyter notebook mlmd_sports_analytics_lab1.ipynb
```
## Project Structure
```
MLMD_Labs/
├── README.md
├── requirements.txt
└── mlmd_sports_analytics_lab1.ipynb
```

## Expected Output

After running the full notebook, the metadata store will contain:
- **4 artifact types**, **4 execution types**, **1 context type**
- **8 artifacts** and **8 executions** across two pipeline runs
- **2 contexts** (exp1 and exp2)
- **14 events** linking artifacts to executions

The experiment comparison shows that the v2 feature set (58 features with progressive carries and pressing metrics) improved model performance from R2=0.847 to R2=0.912.

## References

- [ML Metadata Guide](https://www.tensorflow.org/tfx/guide/mlmd)
- [MLMD API Documentation](https://www.tensorflow.org/tfx/ml_metadata/api_docs/python/mlmd)
- [Original Lab Repository](https://github.com/raminmohammadi/MLOps/tree/main/Labs/MLMD_Labs)
