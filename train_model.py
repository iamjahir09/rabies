from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingRegressor

# Load dataset
df = pd.read_csv('rabies_dataset.csv')

# Features and target
X = df.drop('Risk_Level', axis=1)
y = df['Risk_Level']

# Preprocessing
categorical_cols = ['Location_Risk', 'Animal_Type', 'Bite_Severity', 'Vaccination_Status', 'PEP', 'Wound_Location', 'Animal_Vaccination']
numerical_cols = ['Age', 'Time_Since_Exposure']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(), categorical_cols)
    ])

# Pipeline
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'rabies_model.pkl')

# Example prediction
sample = X_test.iloc[0:1]
probs = model.predict_proba(sample)[0]
risk_levels = model.classes_
max_prob_idx = probs.argmax()
predicted_risk = risk_levels[max_prob_idx]
percentage = probs[max_prob_idx] * 100
print(f"Predicted Risk: {predicted_risk}, Probability: {percentage:.2f}%")