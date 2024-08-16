import streamlit as st
import pandas as pd
import numpy as np
import base64
import plotly.express as px

def main():
    st.set_page_config(layout="wide")  # Use wide mode

    st.header("PawangData App :chart:")
    st.subheader("Helping you handle your data with care and simplicity")
    
    # Custom CSS for responsive table
    st.markdown("""
    <style>
    .stDataFrame {
        width: 100%;
        max-width: 100%;
    }
    .stDataFrame table {
        width: 100%;
        max-width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.subheader("Original Data:")
        display_dataframe_with_search(df, "original")
        
        # Data Exploration Step
        if st.sidebar.checkbox("Explore column data"):
            column_to_explore = st.sidebar.selectbox("Select column to explore:", df.columns, key="explore_column")
            st.sidebar.write(f"Data type: {df[column_to_explore].dtype}")
            st.sidebar.write("Value counts:")
            st.sidebar.write(df[column_to_explore].value_counts())
        
        st.sidebar.header("Data Wrangling Operations")
        option = st.sidebar.selectbox(
            "Select an operation:",
            ["Sort", "Filter", "Drop column", "Select column", "Rename column", 
             "Drop missing values", "Drop duplicate rows", "Convert text to lowercase", 
             "Convert text to uppercase", "Fill missing values", "Find and replace", 
             "Strip whitespace", "Group by column and aggregate", "Split text"],
            key="operation_select"
        )
        
        # Apply the selected operation
        if option == "Sort":
            df = sort_dataframe(df)
        elif option == "Filter":
            df = filter_dataframe(df)
        elif option == "Drop column":
            df = drop_column(df)
        elif option == "Select column":
            df = select_column(df)
        elif option == "Rename column":
            df = rename_column(df)
        elif option == "Drop missing values":
            df = drop_missing_values(df)
        elif option == "Drop duplicate rows":
            df = drop_duplicate_rows(df)
        elif option == "Convert text to lowercase":
            df = convert_to_lowercase(df)
        elif option == "Convert text to uppercase":
            df = convert_to_uppercase(df)
        elif option == "Fill missing values":
            df = fill_missing_values(df)
        elif option == "Find and replace":
            df = find_and_replace(df)
        elif option == "Strip whitespace":
            df = strip_whitespace(df)
        elif option == "Group by column and aggregate":
            df = group_and_aggregate(df)
        elif option == "Split text":
            df = split_text(df)
        
        st.subheader("Modified Data:")
        display_dataframe_with_search(df, "modified")
        
        if st.button("Export Data"):
            export_data(df)
        
        # New function to visualize preprocessing steps
        if st.sidebar.checkbox("Visualize Preprocessing"):
            visualize_preprocessing(df)

def display_dataframe_with_search(df, key):
    search_term = st.text_input(f"Search {key} dataframe:", key=f"search_{key}")
    if search_term:
        filtered_df = df[df.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)]
        st.dataframe(filtered_df, height=300)
    else:
        st.dataframe(df, height=300)

def visualize_preprocessing(df):
    st.sidebar.subheader("Visualization Options")
    chart_type = st.sidebar.selectbox("Select chart type:", ["Bar", "Line", "Scatter", "Histogram"], key="viz_chart_type")
    
    if chart_type in ["Bar", "Line", "Scatter"]:
        x_column = st.sidebar.selectbox("Select X-axis column:", df.columns, key="viz_x_column")
        y_column = st.sidebar.selectbox("Select Y-axis column:", df.columns, key="viz_y_column")
        
        # Add filter option
        filter_column = st.sidebar.selectbox("Select column to filter:", df.columns, key="viz_filter_column")
        filter_value = st.sidebar.text_input("Enter filter value:", key="viz_filter_value")
        
        # Apply filter
        if filter_value:
            df = df[df[filter_column].astype(str).str.contains(filter_value, case=False)]
        
        if chart_type == "Bar":
            fig = px.bar(df, x=x_column, y=y_column)
        elif chart_type == "Line":
            fig = px.line(df, x=x_column, y=y_column)
        else:  # Scatter
            fig = px.scatter(df, x=x_column, y=y_column)
    
    elif chart_type == "Histogram":
        column = st.sidebar.selectbox("Select column for histogram:", df.columns, key="viz_hist_column")
        
        # Add filter option
        filter_column = st.sidebar.selectbox("Select column to filter:", df.columns, key="viz_hist_filter_column")
        filter_value = st.sidebar.text_input("Enter filter value:", key="viz_hist_filter_value")
        
        # Apply filter
        if filter_value:
            df = df[df[filter_column].astype(str).str.contains(filter_value, case=False)]
        
        fig = px.histogram(df, x=column)
    
    st.plotly_chart(fig, use_container_width=True)

def sort_dataframe(df):
    column = st.sidebar.selectbox("Select column to sort by:", df.columns, key="sort_column")
    sort_order = st.sidebar.radio("Sort order:", ("Ascending", "Descending"), key="sort_order")
    return df.sort_values(by=column, ascending=(sort_order == "Ascending"))

def filter_dataframe(df):
    column = st.sidebar.selectbox("Select column to filter:", df.columns, key="filter_column")
    filter_value = st.sidebar.text_input("Enter filter value:", key="filter_value")
    return df[df[column].astype(str).str.contains(filter_value, case=False)]

def drop_column(df):
    column = st.sidebar.selectbox("Select column to drop:", df.columns, key="drop_column")
    return df.drop(columns=[column])

def select_column(df):
    columns = st.sidebar.multiselect("Select columns to keep:", df.columns, key="select_columns")
    return df[columns]

def rename_column(df):
    column = st.sidebar.selectbox("Select column to rename:", df.columns, key="rename_column")
    new_name = st.sidebar.text_input("Enter new column name:", key="new_column_name")
    return df.rename(columns={column: new_name})

def drop_missing_values(df):
    return df.dropna()

def drop_duplicate_rows(df):
    return df.drop_duplicates()

def convert_to_lowercase(df):
    column = st.sidebar.selectbox("Select column to convert to lowercase:", df.select_dtypes(include=['object']).columns, key="lowercase_column")
    df[column] = df[column].str.lower()
    return df

def convert_to_uppercase(df):
    column = st.sidebar.selectbox("Select column to convert to uppercase:", df.select_dtypes(include=['object']).columns, key="uppercase_column")
    df[column] = df[column].str.upper()
    return df

def fill_missing_values(df):
    column = st.sidebar.selectbox("Select column to fill missing values:", df.columns, key="fill_missing_column")
    fill_value = st.sidebar.text_input("Enter value to fill missing data:", key="fill_missing_value")
    df[column] = df[column].fillna(fill_value)
    return df

def find_and_replace(df):
    column = st.sidebar.selectbox("Select column for find and replace:", df.columns, key="find_replace_column")
    find_value = st.sidebar.text_input("Enter value to find:", key="find_value")
    replace_value = st.sidebar.text_input("Enter value to replace with:", key="replace_value")
    df[column] = df[column].replace(find_value, replace_value)
    return df

def strip_whitespace(df):
    for column in df.select_dtypes(include=['object']):
        df[column] = df[column].str.strip()
    return df

def group_and_aggregate(df):
    group_column = st.sidebar.selectbox("Select column to group by:", df.columns, key="group_column")
    agg_column = st.sidebar.selectbox("Select column to aggregate:", df.columns, key="agg_column")
    agg_function = st.sidebar.selectbox("Select aggregation function:", ["mean", "sum", "count", "min", "max"], key="agg_function")
    
    df[agg_column] = pd.to_numeric(df[agg_column].replace(',','', regex=True), errors='coerce')
    df_clean = df.dropna(subset=[agg_column])
    
    if df_clean.empty:
        st.sidebar.error(f"No numeric data in '{agg_column}' after conversion. Please choose another column.")
        return df
    
    result = df_clean.groupby(group_column).agg({agg_column: agg_function}).reset_index()
    
    if result.empty:
        st.sidebar.error(f"Grouping resulted in an empty dataframe. Please check your data and selections.")
        return df
    
    return result

def split_text(df):
    column = st.sidebar.selectbox("Select column to split:", df.select_dtypes(include=['object']).columns, key="split_column")
    separator = st.sidebar.text_input("Enter separator:", key="split_separator")
    max_splits = st.sidebar.number_input("Maximum number of splits (leave at -1 for no limit):", value=-1, key="max_splits")
    
    if separator:
        max_split_count = df[column].str.split(separator).str.len().max()
        st.sidebar.write(f"Maximum number of splits found: {max_split_count}")
        
        default_new_columns = [f"{column}_split_{i+1}" for i in range(max_split_count)]
        
        new_columns = st.sidebar.text_input("Enter new column names (comma-separated, leave blank for default names):", key="new_split_columns")
        
        if new_columns:
            new_columns = [col.strip() for col in new_columns.split(",")]
        else:
            new_columns = default_new_columns
        
        split_df = df[column].str.split(separator, n=max_splits, expand=True)
        
        for i in range(len(split_df.columns)):
            if i < len(new_columns):
                df[new_columns[i]] = split_df[i]
            else:
                df[f"{column}_split_{i+1}"] = split_df[i]
        
        st.sidebar.success(f"Text split into {len(split_df.columns)} columns.")
    else:
        st.sidebar.warning("Please enter a separator.")
    
    return df

def export_data(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="exported_data.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

# Footer
st.markdown("---")
st.markdown("Built with 💖 using Claude.ai, Streamlit, and GitHub. 👨‍💻 Adnuri Mohamidi – PawangData Project")