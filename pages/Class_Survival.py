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
        port = st.multiselect(
            "Choose Traveler's Embarking Port", list(df.embarked.unique()), ["C","Q","S"]
        )
        if not tclass:
            st.error("Please select at least one Traveler's Class.")
        if not port:
            st.error("Please select at least one Traveler's Embarking Port.")
        else:
            df = df[df['pclass'].isin(tclass)]
            df = df[df['embarked'].isin(port)]
            t = df.rename(columns={"pclass": "Traveler's Class",
                        "sex":"Sex",
                        "age":"Age",
                        "embarked":"Embarking Port",
                    "survived":"Survived"})
            t['Perished'] = [1 if s == 0 else 0 for s in t.Survived]
            tg = t[["Traveler's Class",'Survived','Perished', 'Embarking Port']].groupby(by=["Traveler's Class", "Embarking Port"])
            table1 = tg.mean()
            table1.Survived = table1.Survived.apply(lambda s: str(round(s*100,1)).format("{:.f2}")+"%")
            table1.Perished = table1.Perished.apply(lambda p: str(round(p*100,1)).format("{:.f2}")+"%")
            
            st.write("### Chance of Survival", table1)


    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )


st.set_page_config(page_title="Survival Table", page_icon="📊")
st.markdown("# Survival Table")
st.sidebar.header("Survival Table")
st.write(
    """This page shows the percentage of passengers who survived and perished organized by
    their Passenger Class and Embarking Port."""
)

data_frame_demo()

show_code(data_frame_demo)
