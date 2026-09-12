import sys
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.model_selection import train_test_split


# ============================================================
# PATH SETUP
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT / "thalayattam_synthetic_dataset.csv"
)

MODEL_PATH = (
    PROJECT_ROOT / "backend" / "ml" / "model.pkl"
)

# Allow importing from backend/
sys.path.append(
    str(PROJECT_ROOT / "backend")
)

from vision.features import FeatureExtractor


# ============================================================
# LOAD DATASET
# ============================================================

print("======================================")
print("       THALAYATTAM ML TRAINING")
print("======================================")

print("\nLoading dataset...")

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found:\n{DATASET_PATH}"
    )

df = pd.read_csv(DATASET_PATH)

print(f"Total rows: {len(df):,}")
print(
    f"Total recordings: "
    f"{df['recording_id'].nunique():,}"
)

print("\nGesture distribution:")
print(
    df.groupby("gesture")["recording_id"]
    .nunique()
)


# ============================================================
# CREATE FEATURES FOR EACH RECORDING
# ============================================================

print("\nExtracting features...")

extractor = FeatureExtractor()

X = []
y = []

recording_ids = []

for recording_id, group in df.groupby("recording_id"):

    sequence = group[
        ["yaw", "pitch", "roll"]
    ].to_dict("records")

    features = extractor.extract(sequence)

    X.append(list(features.values()))

    y.append(
        group["gesture"].iloc[0]
    )

    recording_ids.append(recording_id)


X = pd.DataFrame(
    X,
    columns=list(
        extractor.extract(
            df[
                ["yaw", "pitch", "roll"]
            ].head(10).to_dict("records")
        ).keys()
    )
)

y = pd.Series(y, name="gesture")


print(
    f"Feature matrix: "
    f"{X.shape[0]} recordings × {X.shape[1]} features"
)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")


# ============================================================
# RANDOM FOREST
# ============================================================

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(
    X_train,
    y_train
)


# ============================================================
# PREDICTION
# ============================================================

print("\nEvaluating model...")

y_pred = model.predict(X_test)


# ============================================================
# ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n======================================")
print("             RESULTS")
print("======================================")

print(
    f"\nAccuracy: {accuracy * 100:.2f}%"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

labels = sorted(
    y.unique()
)

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

print("Confusion Matrix:")
print()

print(
    pd.DataFrame(
        cm,
        index=labels,
        columns=labels
    )
)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

print("\nFeature Importance:")

importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    "importance",
    ascending=False
)

print(
    importance.to_string(index=False)
)


# ============================================================
# SAVE MODEL
# ============================================================

MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    {
        "model": model,
        "feature_names": list(X.columns),
        "classes": list(model.classes_)
    },
    MODEL_PATH
)

print("\n======================================")
print("       MODEL SAVED SUCCESSFULLY")
print("======================================")

print(
    f"\nModel location:\n{MODEL_PATH}"
)