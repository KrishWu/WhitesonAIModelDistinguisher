import torch
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib

def load_model():

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

    scaler = joblib.load('scaler.pkl')

    return model,scaler

# data is [ HeavyTParticle_Px,HeavyTParticle_Py,HeavyTParticle_Pz,HeavyTParticle_E, TParticle_Px,TParticle_Py,TParticle_Pz,TParticle_E ]                            
def eval_model(model,scaler,data):

    print ("data = ",data)

    # scale inputs                                                                                                                                                 
    data_scaled = scaler.transform(data)
    print ("scaled = ",data_scaled)

    inputs = torch.tensor(data_scaled, dtype=torch.float32)  # Use float32 for the model input                                                                     
    print ("inputs = ",inputs)

    model.eval()  # Set model to evaluation mode (important for layers like Dropout)                                                                               
    with torch.no_grad():  # Disable gradient calculations                                                                                                         
        outputs = model(inputs)

        outputs = torch.round(outputs)

    return outputs

def test():

    model,scaler = load_model()


    # df = pd.read_csv("data/v5/data.csv", index_col=0)                                                                                                            
    # df = df.drop(columns=['Transverse Momentum', 'Delta Angle'])                                                                                                 

    data = np.array([[  32.672529648860916, -1330.293078183176, -244.44821410324784, 1490.642541187895,
			385.30475257,   492.94182467  , 515.25724637 ,  810.5192316 ]])

    res = eval_model(model,scaler,data)
    print ("res = ",res)

test()
