import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import binom
from scipy.stats import poisson
from plotnine import *

st.set_page_config(page_title="Analise dos Dados", layout="wide")

st.title("Analise dos Dados")

@st.cache_data
def load_data():
    df = pd.read_csv("LifeExpectancy.csv")
    return df

df = load_data()

#https://github.com/dataprofessor/llama2/blob/master/streamlit_app_v2.py
# Codigo que utiliza o OLLama

st.write(df.head(5))