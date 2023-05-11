# -*- coding: utf-8 -*-
"""
Creates control charts for analyzing time series

@author: Nick
"""

import numpy as np
import pandas as pd


def IMR(x: list):
    d2 = 1.128
    D4 = 3.267
    D3 = 0

    data = pd.DataFrame({
        "Observation": np.arange(len(x)) + 1,
        "I": x,
    })
    data["MR"] = data["I"].diff().abs()
    data = data.dropna().reset_index(drop=True)

    Xbar = data["I"].mean()
    MRbar = data["MR"].mean()

    I_UCL = Xbar + 3*MRbar / d2
    I_LCL = Xbar - 3*MRbar / d2
    I_CL = Xbar

    MR_UCL = MRbar*D4
    MR_LCL = MRbar*D3
    MR_CL = MRbar

    df = data[["Observation"]].copy()
    df["I"] = data["I"]
    df["I UCL"] = I_UCL
    df["I LCL"] = I_LCL
    df["I CL"] = I_CL
    df["MR"] = data["MR"]
    df["MR UCL"] = MR_UCL
    df["MR LCL"] = MR_LCL
    df["MR CL"] = MR_CL

    return df
