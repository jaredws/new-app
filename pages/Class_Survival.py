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

from urllib.error import URLError

import altair as alt
import pandas as pd
import numpy as np
## Anytime you add a package, you need to...
#  Add it to requirements.text and 
# "> Rebuild Container" in the command bar above
import matplotlib.pyplot as plt

import streamlit as st
from streamlit.hello.utils import show_code


def data_frame_demo():
    @st.cache_data
    def get_data():
        
        df = pd.read_csv("titanic.csv")
        return df.sort_values("pclass")

    try:
        df = get_data()
        tclass = st.multiselect(
            "Choose Traveler's Class", list(df.pclass.unique()), [1, 2,3]
        )
        if not tclass:
            st.error("Please select at least one Traveler's Class.")
        else:
            t = df.rename(columns={"pclass": "Traveler's Class",
                      "sex":"Sex",
                      "age":"Age",
                  "survived":"Survived"})
            t['Perished'] = [1 if s == 0 else 0 for s in t.Survived]
            tg = t[["Traveler's Class",'Survived','Perished']].groupby(by=["Traveler's Class"])
            table1 = tg.mean("Survived")
            table1.Survived = (np.round(table1.Survived,3)*100).astype(str)+"%"

            st.write("### Chance of Survival", table1[["Survived"]])

            tg_sum = tg.sum()

            ax = tg_sum.plot(kind="bar")

            # Get a Matplotlib figure from the axes object for formatting purposes
            fig = ax.get_figure()

            # Change the axes labels
            ax.set_xlabel("Traveler's Class", fontsize = 15)
            ax.set_ylabel("Count", fontsize = 15)

            # Use this to show the plot in a new window
            plt.xticks(rotation = 0)
            plt.show();

    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )


st.set_page_config(page_title="DataFrame Demo", page_icon="📊")
st.markdown("# DataFrame Demo")
st.sidebar.header("DataFrame Demo")
st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames."""
)

data_frame_demo()

show_code(data_frame_demo)
