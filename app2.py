import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    st.title("Hello, World! EDA Streamlit App")

    st.header("Upload your CSV data file")
    data_file = st.file_uploader("Upload CSV", type=["csv"])

    data = None  # Initialize data as None

    if data_file is not None:
        data = pd.read_csv(data_file, nrows=5000)  # Read only the first 5000 rows
        st.write("Data overview:")
        st.write(data.head())

        st.sidebar.header("Visualizations")
        plot_options = ["Bar plot", "Scatter plot", "Histogram", "Box plot", "Heatmap"]
        selected_plot = st.sidebar.selectbox("Choose a plot type", plot_options)

        # Show number of null values in each column
        st.sidebar.header("Null Values")
        null_counts = data.isnull().sum()
        st.sidebar.write("Number of null values in each column:")
        st.sidebar.write(null_counts)

        # Fill null values
        st.sidebar.header("Fill Null Values")
        fill_methods = ["Mean", "Median", "Mode", "Custom Value"]
        selected_method = st.sidebar.selectbox("Choose a fill method", fill_methods)
        if selected_method == "Custom Value":
            custom_value = st.sidebar.text_input("Enter custom value")
        else:
            custom_value = None

        if st.sidebar.button("Fill Null Values"):
            if selected_method == "Mean":
                data.fillna(data.mean(), inplace=True)
            elif selected_method == "Median":
                data.fillna(data.median(), inplace=True)
            elif selected_method == "Mode":
                data.fillna(data.mode().iloc[0], inplace=True)
            elif selected_method == "Custom Value" and custom_value is not None:
                data.fillna(custom_value, inplace=True)
            st.sidebar.success("Null values filled successfully.")

        # Drop null values
        st.sidebar.header("Drop Null Values")
        if st.sidebar.button("Drop Null Values"):
            data.dropna(inplace=True)
            st.sidebar.success("Null values dropped successfully.")

        # Replace value in column
        st.sidebar.header("Replace Value in Column")
        column_to_replace = st.sidebar.selectbox("Select a column", data.columns, key="replace_column_select")
        old_value = st.sidebar.text_input("Enter old value to replace", key="replace_old_value")
        new_value = st.sidebar.text_input("Enter new value", key="replace_new_value")
        if st.sidebar.button("Replace Value"):
            data[column_to_replace] = data[column_to_replace].replace(old_value, new_value)
            st.sidebar.success(f"Value '{old_value}' replaced with '{new_value}' successfully.")
            st.write("Data overview (after replacing values):")
            st.write(data.head())

        # Replace column name
        data2 = None
        st.sidebar.header("Replace Column Name")
        old_column_name = st.sidebar.selectbox("Select a column", data.columns, key="rename_column_select")
        new_column_name = st.sidebar.text_input("Enter new column name", key="rename_new_column_name")
        if st.sidebar.button("Replace Column Name"):
            data.rename(columns={old_column_name: new_column_name}, inplace=True)
            data2 = data.copy()  # Copy the modified DataFrame to data2
            st.sidebar.success(f"Column '{old_column_name}' renamed to '{new_column_name}' successfully.")
            st.write("Data overview (after renaming column):")
            st.write(data2.head())


        selected_columns = []
        if selected_plot in ["Bar plot", "Scatter plot"]:
            selected_columns.append(st.sidebar.selectbox("Select x-axis", data.columns, key="plot_x_axis"))
            selected_columns.append(st.sidebar.selectbox("Select y-axis", data.columns, key="plot_y_axis"))

        if selected_plot == "Histogram":
            selected_columns.append(st.sidebar.selectbox("Select a column", data.columns, key="histogram_column"))

        if selected_plot == "Box plot":
            selected_columns.append(st.sidebar.selectbox("Select a column", data.columns, key="boxplot_column"))

        if selected_plot == "Heatmap":
            st.write("Heatmap:")
            fig, ax = plt.subplots()
            sns.heatmap(data.corr(), annot=True, cmap="coolwarm", fmt=".2f")
            st.pyplot(fig)

        if st.sidebar.button("Plot"):
            st.write(f"{selected_plot}:")
            fig, ax = plt.subplots()
            if selected_plot == "Bar plot":
                sns.barplot(x=data[selected_columns[0]], y=data[selected_columns[1]], ax=ax)
            elif selected_plot == "Scatter plot":
                sns.scatterplot(x=data[selected_columns[0]], y=data[selected_columns[1]], ax=ax)
            elif selected_plot == "Histogram":
                sns.histplot(data[selected_columns[0]], bins=20, ax=ax)
            elif selected_plot == "Box plot":
                sns.boxplot(data[selected_columns[0]], ax=ax)
            st.pyplot(fig)

if __name__ == "__main__":
    main()
