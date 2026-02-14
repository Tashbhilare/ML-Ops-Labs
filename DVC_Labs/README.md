# DVC Lab 1: Data Version Control with Google Cloud Storage

**Course:** IE 7374 — MLOps | Northeastern University  
**Lab Topic:** Data Version Control (DVC)  
**Remote Storage:** Google Cloud Storage (GCS)  
**Dataset:** [CC_GENERAL.csv](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata) — Credit Card Customer Clustering Dataset

---

## Overview

In ML projects, datasets change frequently — new records arrive, features get engineered, bugs get fixed. Without data versioning, it's impossible to reproduce past experiments or know which data trained a production model.

**DVC (Data Version Control)** solves this by working alongside Git. Git tracks code and small `.dvc` metafiles, while DVC manages the actual large data files in remote storage. Each data version is identified by a unique **md5 hash**, so multiple versions can coexist in the remote without conflicts.

This lab walks through the full DVC workflow using **Google Cloud Storage** as the remote backend.


**Key idea:** Git never sees the large CSV. It only tracks the tiny `.dvc` file. DVC handles uploading/downloading the actual data to/from GCS.

## Dataset

- **CC_GENERAL.csv** — Credit card usage data for customer segmentation
- ~8,950 rows × 18 features (balance, purchases, credit limit, payments, tenure, etc.)
- Source: [Kaggle](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata)

## Project Structure
```
DVC_Labs/
├── README.md                  # This file
├── CC_GENERAL.csv.dvc         # DVC metafile (pointer to data in GCS)
├── params.yaml                # Pipeline parameters
├── .dvc/
│   ├── config                 # DVC remote configuration (GCS bucket + credentials)
│   └── .gitignore
└── .dvcignore
```

## Prerequisites

- Python 3.9+
- Git installed
- A Google Cloud Platform (GCP) account
- [CC_GENERAL.csv](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata) downloaded from Kaggle

---

## Steps to Reproduce

### 1. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install "dvc[gs]"
```

`dvc[gs]` installs DVC with Google Cloud Storage support. Other options include `[s3]` for AWS, `[azure]` for Azure, or `[all]` for everything.

### 2. Initialize Git and DVC
```bash
git init
dvc init
```

`dvc init` creates a `.dvc/` directory that stores DVC's internal configuration — similar to how `git init` creates `.git/`.

### 3. Create GCS Bucket & Service Account

**Create a bucket:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g., `MLOps-DVC-Lab`)
3. Navigate to **Cloud Storage → Buckets → Create**
4. Name it uniquely (e.g., `mlops-dvc-lab-tanish`)
5. Region: **us-east1**, keep all other defaults
6. Click **Create**

**Create service account credentials:**
1. Go to **IAM & Admin → Service Accounts**
2. Click **Create Service Account** → Name: `dvc-lab`
3. Grant **Owner** role → Click **Done**
4. Click **Actions (⋮) → Manage Keys → Add Key → JSON**
5. Download the JSON file — this authenticates DVC with GCS

> **Never commit the JSON credentials file to Git.** Add it to `.gitignore`.

### 4. Configure DVC Remote
```bash
dvc remote add -d myremote gs://<your-bucket-name>
dvc remote modify myremote credentialpath <path/to/credentials.json>
```

Verify with `cat .dvc/config`:
```ini
[core]
    remote = myremote
['remote "myremote"']
    url = gs://mlops-dvc-lab-tanish
    credentialpath = /path/to/credentials.json
```

### 5. Track Data with DVC
```bash
mkdir -p data
cp /path/to/CC\ GENERAL.csv data/CC_GENERAL.csv
dvc add data/CC_GENERAL.csv
```

This creates `data/CC_GENERAL.csv.dvc` — the metafile containing the md5 hash:
```yaml
outs:
- md5: c9b0bb7fc9e241b81da92c3528103664
  size: 902879
  hash: md5
  path: CC_GENERAL.csv
```

Commit the metafile to Git and push data to GCS:
```bash
git add data/CC_GENERAL.csv.dvc data/.gitignore
git commit -m "Track CC_GENERAL.csv with DVC"
dvc push    # uploads actual CSV to GCS bucket
```

### 6. Handle Data Changes

When the dataset is updated, DVC detects the change through a new hash:
```bash
# Simulate data change (e.g., keep first 5000 rows)
head -5000 data/CC_GENERAL.csv > data/temp.csv
mv data/temp.csv data/CC_GENERAL.csv

# Re-track — DVC computes new hash
dvc add data/CC_GENERAL.csv

# New .dvc metafile now shows different hash:
# md5: 3ceae1dc79c365d1181659805f6b5a92
# size: 509413

git add data/CC_GENERAL.csv.dvc
git commit -m "v2: Cleaned dataset - reduced to 5000 rows"
dvc push    # both versions now stored in GCS
```

### 7. Revert to Previous Version

This is the core power of DVC — switching between dataset versions:
```bash
# Check git log to find the commit hash
git log --oneline

# Checkout the old .dvc metafile
git checkout <previous-commit-hash> data/CC_GENERAL.csv.dvc

# DVC restores the matching data from cache/remote
dvc checkout

# Verify: file is back to original size
wc -l data/CC_GENERAL.csv    # 8951 lines (original)
```

To return to the latest version:
```bash
git checkout main data/CC_GENERAL.csv.dvc
dvc checkout
```

---

## References

- [DVC Documentation](https://dvc.org/doc)
- [DVC with Google Cloud Storage](https://dvc.org/doc/user-guide/data-management/remote-storage/google-cloud-storage)
- [CC General Dataset — Kaggle](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata)
- Course: IE 7374 MLOps, Prof. Ramin Mohammadi, Northeastern University
