import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE  # Handling class imbalance

# Load dataset
df = pd.read_csv("Augmented_mental_health_dataset_expanded.csv", low_memory=False)

# Convert all object (string) columns to strings explicitly
df = df.astype(str)

# Drop irrelevant columns
df = df.drop(columns=["User_ID", "Date", "Motivational_Quote"])

# Fill missing values
for column in df.columns:
    if df[column].dtype == 'object':  
        df[column].fillna(df[column].mode()[0], inplace=True)  # Fill categorical with mode
    else:  
        df[column] = pd.to_numeric(df[column], errors='coerce')  # Convert numbers properly
        df[column].fillna(df[column].mean(), inplace=True)  # Fill numerical with mean

# Encode categorical variables
label_encoders = {}
for column in df.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Define features (X) and target (y)
target_column = "Mental_Health_Condition"  # Adjust this if needed
X = df.drop(columns=[target_column])
y = df[target_column]

# Handle class imbalance using SMOTE
smote = SMOTE(random_state=42)
X, y = smote.fit_resample(X, y)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale numerical features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train Random Forest Classifier with Hyperparameter Tuning
rf_model = RandomForestClassifier(n_estimators=200, max_depth=20, min_samples_split=5, class_weight="balanced", random_state=42)
rf_model.fit(X_train, y_train)

# Predictions
y_pred = rf_model.predict(X_test)

# Evaluate performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Improved Accuracy: {accuracy:.4f}")  # More decimal places for better analysis
print("Classification Report:\n", classification_report(y_test, y_pred))



