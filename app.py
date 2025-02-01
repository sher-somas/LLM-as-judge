import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit App Title
st.title("CSV File Uploader and Viewer with Analytics")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display the dataframe
    st.write("### Data Preview:")
    st.dataframe(df)
    
    # Display basic statistics
    st.write("### Basic Statistics:")
    st.write(df.describe())
    
    # Display column information
    st.write("### Column Information:")
    st.write(df.dtypes)
    
    # Visualization: Distribution of numerical columns
    st.write("### Data Distribution:")
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    for col in numerical_cols:
        fig, ax = plt.subplots()
        sns.histplot(df[col], bins=20, kde=True, ax=ax)
        st.pyplot(fig)
    
    # Correlation heatmap
    st.write("### Correlation Heatmap:")
    fig, ax = plt.subplots()
    # sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
    numeric_df = df.select_dtypes(include=['float64', 'int64'])  # Select only numeric columns
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)

    st.pyplot(fig)
    
    # Filtering option
    st.write("### Filter Data:")
    filter_column = st.selectbox("Select a column to filter", numerical_cols)
    filter_value = st.slider(f"Select {filter_column} threshold", float(df[filter_column].min()), float(df[filter_column].max()), float(df[filter_column].mean()))
    filtered_df = df[df[filter_column] >= filter_value]
    st.write("Filtered Data:")
    st.dataframe(filtered_df)
