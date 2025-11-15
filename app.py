import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Adaptive IDS Dashboard", layout="wide")

st.title("🔐 Adaptive Intrusion Detection System (Autoencoder + Reinforcement Learning)")

# -----------------------------------------------
# FILE UPLOAD SECTION (NEW FEATURE)
# -----------------------------------------------

st.sidebar.header("📂 Upload New Data (Optional)")
ae_upload = st.sidebar.file_uploader("Upload Autoencoder CSV", type="csv")
rl_upload = st.sidebar.file_uploader("Upload RL-Adaptive CSV", type="csv")

# -----------------------------------------------
# LOAD DATA: uploaded → otherwise fallback to GitHub files
# -----------------------------------------------

@st.cache_data
def load_data(ae_file, rl_file):
    try:
        ae_df = pd.read_csv(ae_file)
    except:
        ae_df = pd.read_csv("ae_results.csv")

    try:
        rl_df = pd.read_csv(rl_file)
    except:
        rl_df = pd.read_csv("rl_adaptive_results.csv")

    return ae_df, rl_df

ae_df, rl_df = load_data(ae_upload, rl_upload)

# -----------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to:", ["Overview", "Autoencoder Results", "RL-Adaptive Results", "Comparison"])

# -----------------------------------------------
# PAGE 1: OVERVIEW
# -----------------------------------------------
if page == "Overview":
    st.header("📘 Dataset Overview")

    st.subheader("Autoencoder Dataset")
    st.dataframe(ae_df.head())

    st.subheader("RL-Adaptive Dataset")
    st.dataframe(rl_df.head())

# -----------------------------------------------
# METRIC CALCULATOR
# -----------------------------------------------
def calculate_metrics(df, label_col, pred_col):
    try:
        accuracy = (df[label_col] == df[pred_col]).mean()
        tp = ((df[label_col] == 1) & (df[pred_col] == 1)).sum()
        fp = ((df[label_col] == 0) & (df[pred_col] == 1)).sum()
        fn = ((df[label_col] == 1) & (df[pred_col] == 0)).sum()
        precision = tp / (tp + fp + 1e-7)
        recall = tp / (tp + fn + 1e-7)
        f1 = 2 * (precision * recall) / (precision + recall + 1e-7)
        return accuracy, precision, recall, f1
    except:
        return None, None, None, None

# -----------------------------------------------
# PAGE 2: AUTOENCODER RESULTS
# -----------------------------------------------
if page == "Autoencoder Results":
    st.header("🤖 Autoencoder Model Results")

    accuracy, precision, recall, f1 = calculate_metrics(ae_df, "Label", "Predicted")

    st.metric("Accuracy", f"{accuracy:.2f}")
    st.metric("F1 Score", f"{f1:.2f}")

    st.subheader("Confusion Matrix")

    fig, ax = plt.subplots()
    ax.scatter(ae_df.index, ae_df["Predicted"], label="Predicted", alpha=0.7)
    ax.scatter(ae_df.index, ae_df["Label"], label="Actual", alpha=0.7)
    ax.legend()
    st.pyplot(fig)

# -----------------------------------------------
# PAGE 3: RL-ADAPTIVE RESULTS
# -----------------------------------------------
if page == "RL-Adaptive Results":
    st.header("🧠 Reinforcement Learning Adaptive Model Results")

    accuracy, precision, recall, f1 = calculate_metrics(rl_df, "Label", "RL_Predicted")

    st.metric("Accuracy", f"{accuracy:.2f}")
    st.metric("F1 Score", f"{f1:.2f}")

    st.subheader("Confusion Matrix")

    fig, ax = plt.subplots()
    ax.scatter(rl_df.index, rl_df["RL_Predicted"], label="RL_Predicted", alpha=0.7)
    ax.scatter(rl_df.index, rl_df["Label"], label="Actual", alpha=0.7)
    ax.legend()
    st.pyplot(fig)

# -----------------------------------------------
# PAGE 4: COMPARISON
# -----------------------------------------------
if page == "Comparison":
    st.header("📊 Model Comparison: Autoencoder vs RL-Adaptive")

    ae_acc, _, _, ae_f1 = calculate_metrics(ae_df, "Label", "Predicted")
    rl_acc, _, _, rl_f1 = calculate_metrics(rl_df, "Label", "RL_Predicted")

    st.write("### 🔎 Accuracy Comparison")
    fig, ax = plt.subplots()
    ax.bar(["Autoencoder", "RL-Adaptive"], [ae_acc, rl_acc])
    st.pyplot(fig)

    st.write("### 🔎 F1-Score Comparison")
    fig, ax = plt.subplots()
    ax.bar(["Autoencoder", "RL-Adaptive"], [ae_f1, rl_f1])
    st.pyplot(fig)

st.success("App Loaded Successfully!")
