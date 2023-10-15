# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit.hello.utils import show_code


def plotting_demo():
    child_max = st.slider("How old was considered a 'child?'", 0, 100, 18)
    t = pd.read_csv("titanic.csv")
    t = t.rename(columns={"pclass": "Traveler's Class",
                      "sex":"Sex",
                      "age":"Age",
                  "survived":"Survived"})
    t['Perished'] = [1 if s == 0 else 0 for s in t.Survived]
    t['Age Category'] = ["Child" if a <=child_max else "Adult" for a in t['Age']]
    tg = t[['Age Category','Survived','Perished']].groupby(by=["Age Category"])
    tg_sum = tg.sum()

    ax = tg_sum.plot(kind="bar")

    # Get a Matplotlib figure from the axes object for formatting purposes
    fig = ax.get_figure()

    # Change the axes labels
    ax.set_xlabel("Age Category", fontsize = 15)
    ax.set_ylabel("Count", fontsize = 15)

    # Use this to show the plot in a new window
    plt.xticks(rotation = 0)
    plt.show();


st.set_page_config(page_title="Plotting Demo", page_icon="📈")
st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

plotting_demo()

show_code(plotting_demo)
