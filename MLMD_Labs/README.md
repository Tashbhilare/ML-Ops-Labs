# MLMD Lab 1: Tracking a Sports Analytics ML Pipeline with ML Metadata

**Author:** Tanish Dhongade  
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

1. Clone this repository:
```bash
   git clone <your-repo-url>
   cd mlmd-sports-analytics-lab1
```

2. Create a virtual environment and install dependencies:
```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
```

3. Open and run the notebook:
```bash
   jupyter notebook mlmd_sports_analytics_lab1.ipynb
```

4. Execute all cells sequentially. The notebook uses an in-memory database, so no external database setup is required.

## Project Structure
```
mlmd-sports-analytics-lab1/
├── README.md
├── requirements.txt
├── .gitignore
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