# DVC Lab 1: Data Version Control with Google Cloud Storage


## Overview

This lab demonstrates **Data Version Control (DVC)** with **Google Cloud Storage (GCS)** as the remote backend. DVC extends Git by versioning large data files — instead of storing datasets in Git, DVC stores lightweight `.dvc` metafiles (pointers) in Git while the actual data lives in GCS, organized by content hash.

## Dataset

- **CC_GENERAL.csv** — Credit Card customer clustering dataset from [Kaggle](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata)
- ~8950 rows, 18 features describing credit card usage behavior

## Setup & Tools

- **DVC** with Google Cloud support (`pip install "dvc[gs]"`)
- **Google Cloud Storage** bucket as remote storage
- **GCP Service Account** (JSON key) for authentication

## Steps to Reproduce

### 1. Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install "dvc[gs]"
```

### 2. Initialize Git and DVC
```bash
git init
dvc init
```

### 3. Create GCS Bucket & Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and a **Cloud Storage bucket** (region: us-east1)
3. Go to **IAM & Admin → Service Accounts** → Create service account with **Owner** role
4. **Manage Keys → Add Key → JSON** → Download the credentials file

### 4. Configure DVC Remote
```bash
dvc remote add -d myremote gs://<your-bucket-name>
dvc remote modify myremote credentialpath <path/to/credentials.json>
```

### 5. Track Data with DVC
```bash
# Place CC_GENERAL.csv in data/ folder
dvc add data/CC_GENERAL.csv
git add data/CC_GENERAL.csv.dvc data/.gitignore
git commit -m "Track CC_GENERAL.csv with DVC"
dvc push
```

After `dvc add`, a `.dvc` metafile is created containing the md5 hash:
```yaml
outs:
- md5: c9b0bb7fc9e241b81da92c3528103664
  size: 902879
  hash: md5
  path: CC_GENERAL.csv
```

### 6. Handle Data Changes

When the dataset is updated, DVC computes a new hash automatically:
```bash
# Modify the dataset (e.g., clean/reduce rows)
dvc add data/CC_GENERAL.csv     # new hash generated
git add data/CC_GENERAL.csv.dvc
git commit -m "Updated dataset"
dvc push                         # both versions now in GCS
```

### 7. Revert to Previous Version
```bash
git checkout <previous-commit-hash> data/CC_GENERAL.csv.dvc
dvc checkout    # restores the dataset matching that commit
```

To return to latest:
```bash
git checkout main data/CC_GENERAL.csv.dvc
dvc checkout
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| `.dvc` metafile | Small YAML file containing md5 hash — pointer to actual data in remote storage |
| `dvc add` | Starts tracking a file; computes hash and creates `.dvc` metafile |
| `dvc push` | Uploads data to GCS remote, stored by content hash |
| `dvc pull` | Downloads data from GCS based on current `.dvc` metafile |
| `dvc checkout` | Restores local data to match the current `.dvc` pointer |
| Hash-based versioning | Each data version has a unique md5 hash — both versions coexist in GCS |

## References

- [DVC Documentation](https://dvc.org/doc)
- [DVC with Google Cloud Storage](https://dvc.org/doc/user-guide/data-management/remote-storage/google-cloud-storage)
- [CC General Dataset — Kaggle](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata)
