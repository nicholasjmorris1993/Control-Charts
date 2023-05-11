# -*- coding: utf-8 -*-
"""
Creates control charts for analyzing time series

@author: Nick
"""

import numpy as np
import pandas as pd


constants = pd.DataFrame({
    "n": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], 
    "A2": [1.88, 1.023, 0.729, 0.577, 0.483, 0.419, 0.373, 0.337, 0.308, 0.285, 0.266, 0.249, 0.235, 0.223, 0.212, 0.203, 0.194, 0.187, 0.18, 0.173, 0.167, 0.162, 0.157, 0.153], 
    "A3": [2.659, 1.954, 1.628, 1.427, 1.287, 1.182, 1.099, 1.032, 0.975, 0.927, 0.886, 0.85, 0.817, 0.789, 0.763, 0.739, 0.718, 0.698, 0.68, 0.663, 0.647, 0.633, 0.619, 0.606], 
    "d2": [1.128, 1.693, 2.059, 2.326, 2.534, 2.704, 2.847, 2.97, 3.078, 3.173, 3.258, 3.336, 3.407, 3.472, 3.532, 3.588, 3.64, 3.689, 3.735, 3.778, 3.819, 3.858, 3.895, 3.931], 
    "D3": [0.0, 0.0, 0.0, 0.0, 0.0, 0.076, 0.136, 0.184, 0.223, 0.256, 0.283, 0.307, 0.328, 0.347, 0.363, 0.378, 0.391, 0.403, 0.415, 0.425, 0.434, 0.443, 0.451, 0.459], 
    "D4": [3.267, 2.574, 2.282, 2.114, 2.004, 1.924, 1.864, 1.816, 1.777, 1.744, 1.717, 1.693, 1.672, 1.653, 1.637, 1.622, 1.608, 1.597, 1.585, 1.575, 1.566, 1.557, 1.548, 1.541], 
    "B3": [0.0, 0.0, 0.0, 0.0, 0.03, 0.118, 0.185, 0.239, 0.284, 0.321, 0.354, 0.382, 0.406, 0.428, 0.448, 0.466, 0.482, 0.497, 0.51, 0.523, 0.534, 0.545, 0.555, 0.565], 
    "B4": [3.267, 2.568, 2.266, 2.089, 1.97, 1.882, 1.815, 1.761, 1.716, 1.679, 1.646, 1.618, 1.594, 1.572, 1.552, 1.534, 1.518, 1.503, 1.49, 1.477, 1.466, 1.455, 1.445, 1.435],
})


def Xbar(x: list, n: int):
    if n > 25:
        n = 25
    elif n < 2:
        n = 2
    
    if n <= 10:
        return XbarR(x, n)
    else:
        return XbarS(x, n)

def XbarR(x: list, n: int):
    A2 = constants.loc[constants["n"] == n, "A2"].values[0]
    D4 = constants.loc[constants["n"] == n, "D4"].values[0]
    D3 = constants.loc[constants["n"] == n, "D3"].values[0]

    groups = np.repeat(
        a=np.arange(len(x)//n + 1) + 1, 
        repeats=n,
    )[:len(x)]

    data = pd.DataFrame({
        "Group": groups,
        "X": x,
    })

    data = data.groupby(["Group"]).agg({"X": ["mean", "min", "max"]}).reset_index()
    data.columns = [" ".join(col).strip() for col in data.columns.values]
    data["X range"] = data["X max"] - data["X min"]

    Xbarbar = data["X mean"].mean()
    Rbar = data["X range"].mean()

    Xbar_UCL = Xbarbar + A2*Rbar
    Xbar_LCL = Xbarbar - A2*Rbar
    Xbar_CL = Xbarbar

    R_UCL = Rbar*D4
    R_LCL = Rbar*D3
    R_CL = Rbar

    df = data[["Group"]].copy()
    df["Xbar"] = data["X mean"]
    df["Xbar UCL"] = Xbar_UCL
    df["Xbar LCL"] = Xbar_LCL
    df["Xbar CL"] = Xbar_CL
    df["R"] = data["X range"]
    df["R UCL"] = R_UCL
    df["R LCL"] = R_LCL
    df["R CL"] = R_CL

    return df

def XbarS(x: list, n: int):
    A3 = constants.loc[constants["n"] == n, "A3"].values[0]
    B4 = constants.loc[constants["n"] == n, "B4"].values[0]
    B3 = constants.loc[constants["n"] == n, "B3"].values[0]

    groups = np.repeat(
        a=np.arange(len(x)//n + 1) + 1, 
        repeats=n,
    )[:len(x)]

    data = pd.DataFrame({
        "Group": groups,
        "X": x,
    })

    data = data.groupby(["Group"]).agg({"X": ["mean", "std"]}).reset_index()
    data.columns = [" ".join(col).strip() for col in data.columns.values]

    Xbarbar = data["X mean"].mean()
    Sbar = data["X std"].mean()

    Xbar_UCL = Xbarbar + A3*Sbar
    Xbar_LCL = Xbarbar - A3*Sbar
    Xbar_CL = Xbarbar

    S_UCL = Sbar*B4
    S_LCL = Sbar*B3
    S_CL = Sbar

    df = data[["Group"]].copy()
    df["Xbar"] = data["X mean"]
    df["Xbar UCL"] = Xbar_UCL
    df["Xbar LCL"] = Xbar_LCL
    df["Xbar CL"] = Xbar_CL
    df["S"] = data["X std"]
    df["S UCL"] = S_UCL
    df["S LCL"] = S_LCL
    df["S CL"] = S_CL

    return df
