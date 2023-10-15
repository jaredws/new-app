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
                  "survived":"Survived"})
            tg = t[["Traveler's Class",'Survived']].groupby(by="Traveler's Class")
            table1 = tg.mean("Survived")
            table1.Survived = (round(table1.Survived,2) *100).astype(str)+"%"
            st.write("### Chance of Survival", table1)

            chart = (
                alt.Chart(table1)
                .mark_area(opacity=0.3)
                .encode(
                    x="Traveler's Class:O",
                    y=alt.Y("Survived:Q", stack=None),
                    #color="Region:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
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
