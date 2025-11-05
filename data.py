import pandas as pd
import numpy as np

np.random.seed(42)
n_samples = 3000

data = {
    'Age': np.random.randint(0, 100, n_samples),
    'Location_Risk': np.random.choice(['High', 'Medium', 'Low'], n_samples, p=[0.4, 0.3, 0.3]),
    'Animal_Type': np.random.choice(['Dog', 'Cat', 'Wildlife', 'None'], n_samples, p=[0.8, 0.1, 0.08, 0.02]),
    'Bite_Severity': np.random.choice(['None', 'Minor', 'Major'], n_samples, p=[0.2, 0.5, 0.3]),
    'Vaccination_Status': np.random.choice(['Vaccinated', 'Unvaccinated', 'Partial'], n_samples, p=[0.3, 0.6, 0.1]),
    'PEP': np.random.choice(['Yes', 'No'], n_samples, p=[0.4, 0.6]),
    'Time_Since_Exposure': np.random.exponential(100, n_samples).clip(0, 720),
    'Wound_Location': np.random.choice(['Head/Neck', 'Upper Body', 'Lower Body', 'None'], n_samples, p=[0.15, 0.35, 0.3, 0.2]),
    'Animal_Vaccination': np.random.choice(['Vaccinated', 'Unvaccinated', 'Unknown'], n_samples, p=[0.2, 0.5, 0.3]),
}

# Simulate Risk_Level based on features (simplified logic)
def assign_risk(row):
    score = 0
    if row['Location_Risk'] == 'High': score += 0.3
    if row['Animal_Type'] == 'Dog' and row['Animal_Vaccination'] == 'Unvaccinated': score += 0.3
    if row['Bite_Severity'] == 'Major': score += 0.2
    if row['PEP'] == 'No': score += 0.2
    if row['Wound_Location'] == 'Head/Neck': score += 0.1
    if row['Time_Since_Exposure'] > 48: score += 0.1
    if score > 0.6: return 'High'
    elif score > 0.3: return 'Medium'
    else: return 'Low'

data['Risk_Level'] = pd.DataFrame(data).apply(assign_risk, axis=1)
df = pd.DataFrame(data)
df.to_csv('rabies_dataset.csv', index=False)