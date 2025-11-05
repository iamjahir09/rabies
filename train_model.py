from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
import joblib


df = pd.read_csv('rabies_dataset.csv')


X = df.drop('Risk_Level', axis=1)
y = df['Risk_Level']


label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)


categorical_cols = ['Location_Risk', 'Animal_Type', 'Bite_Severity', 'Vaccination_Status', 'PEP', 'Wound_Location', 'Animal_Vaccination']
numerical_cols = ['Age', 'Time_Since_Exposure']


preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(), categorical_cols)
    ])


model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, random_state=42))
])


X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)


model.fit(X_train, y_train)


joblib.dump((model, label_encoder), 'rabies_gb_model.pkl')


sample = X_test.iloc[0:1]
pred_score = model.predict(sample)[0]


predicted_class = label_encoder.inverse_transform([int(round(pred_score))])[0]

print(f"Predicted Risk Level: {predicted_class}, Score: {pred_score:.2f}")
