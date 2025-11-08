import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, f1_score

st.set_page_config(page_title="Adaptive Intrusion Detection Dashboard", layout="wide")
st.title("🚀 Adaptive Intrusion Detection System")
st.markdown("### Using Autoencoder + Reinforcement Learning")

# Load the results
ae_df = pd.read_csv('ae_results.csv')
rl_df = pd.read_csv('rl_adaptive_results.csv')

option = st.sidebar.selectbox("Select View", ["Overview", "Autoencoder Results", "RL-Adaptive Results", "Comparison"])

if option == "Overview":
    st.subheader("Dataset Overview")
    st.write("Autoencoder Results", ae_df.head())
    st.write("RL Adaptive Results", rl_df.head())

elif option == "Autoencoder Results":
    st.subheader("Autoencoder IDS Results")
    acc = accuracy_score(ae_df['Label'], ae_df['Predicted'])
    f1 = f1_score(ae_df['Label'], ae_df['Predicted'])
    st.metric("Accuracy", f"{acc:.3f}")
    st.metric("F1-Score", f"{f1:.3f}")

elif option == "RL-Adaptive Results":
    st.subheader("Reinforcement Learning IDS Results")
    acc = accuracy_score(rl_df['Label'], rl_df['RL_Predicted'])
    f1 = f1_score(rl_df['Label'], rl_df['RL_Predicted'])
    st.metric("Accuracy", f"{acc:.3f}")
    st.metric("F1-Score", f"{f1:.3f}")

elif option == "Comparison":
    st.subheader("Performance Comparison")
    metrics = ['Accuracy','F1-Score']
    ae_scores = [accuracy_score(ae_df['Label'], ae_df['Predicted']),
                 f1_score(ae_df['Label'], ae_df['Predicted'])]
    rl_scores = [accuracy_score(rl_df['Label'], rl_df['RL_Predicted']),
                 f1_score(rl_df['Label'], rl_df['RL_Predicted'])]

    fig, ax = plt.subplots()
    x = np.arange(len(metrics))
    ax.bar(x-0.2, ae_scores, width=0.4, label='Autoencoder')
    ax.bar(x+0.2, rl_scores, width=0.4, label='RL-Adaptive')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()
    st.pyplot(fig)
