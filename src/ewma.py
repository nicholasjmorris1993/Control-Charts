# -*- coding: utf-8 -*-
"""
Creates control charts for analyzing time series

@author: Nick
"""

import numpy as np
import pandas as pd


def EWMA(x: list, alpha: float):
    L = 0.1 * np.log(alpha) + 3

    data = pd.DataFrame({
        "Observation": np.arange(len(x)) + 1,
        "X": x,
    })

    ewma = list()
    baseline = np.mean(x[:5])
    for i, value in enumerate(x):
        if i == 0:
            ewma.append(alpha * value + (1 - alpha) * baseline)
        else:
            ewma.append(alpha * value + (1 - alpha) * ewma[i-1])
    data["EWMA"] = ewma

    EWMAbar = data["EWMA"].mean()
    sdev = data["X"].std()

    margin = L * sdev * np.sqrt((alpha/(2 - alpha)) * (1 - (1 - alpha)**(2*data["Observation"].to_numpy())))

    EWMA_UCL = EWMAbar + margin
    EWMA_LCL = EWMAbar - margin
    EWMA_CL = EWMAbar

    df = data[["Observation"]].copy()
    df["EWMA"] = data["EWMA"]
    df["EWMA UCL"] = EWMA_UCL
    df["EWMA LCL"] = EWMA_LCL
    df["EWMA CL"] = EWMA_CL

    return df
