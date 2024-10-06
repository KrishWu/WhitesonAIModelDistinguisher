import torch
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib


model = torch.nn.Sequential(
    torch.nn.Linear(8, 100),
    torch.nn.ReLU(),
    torch.nn.Linear(100, 80),
    torch.nn.ReLU(),
    torch.nn.Linear(80, 20),
    torch.nn.ReLU(),
    torch.nn.Linear(20, 1),
    torch.nn.Sigmoid()
)
model.load_state_dict(torch.load("net.pth"))

# data = pd.read_csv("data/v5/data.csv")
# data = data.to_numpy()
# indices = np.array([3, 4, 5, 6, 17, 18, 19, 20])
# dataLabels = data[:,26:]
# data = data[:,indices]

# Temp 1 Line Data
data = np.array([[417.97728222, -837.35125351,  270.80903227, 2301.16177279,  385.30475257, 492.94182467,  515.25724637,  810.5192316]])
dataLabels = np.array([[1]])

scaler = joblib.load('scaler.pkl')
data_scaled = scaler.transform(data)
inputs = torch.tensor(data_scaled, dtype=torch.float32)  # Use float32 for the model input

model.eval()  # Set model to evaluation mode (important for layers like Dropout)
    
with torch.no_grad():  # Disable gradient calculations
    outputs = model(inputs)

outputs = torch.round(outputs)

output_df = pd.DataFrame(outputs.numpy(), columns=["Model Output"])
result_df = pd.concat([pd.DataFrame(dataLabels, columns=["Label"]), output_df], axis=1)  # Merge inputs with outputs
print(result_df)

i = 0
for row in result_df.to_numpy():
    if i == 50:
        break

    print(row)
    i += 1