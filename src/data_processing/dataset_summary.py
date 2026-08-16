import streamlit as st


def show_dataset_summary(df):

    st.subheader("📊 Dataset Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())

    col4, col5 = st.columns(2)

    with col4:
        st.metric("Duplicate Rows", df.duplicated().sum())

    with col5:
        memory = round(df.memory_usage(deep=True).sum() / 1024, 2)
        st.metric("Memory (KB)", memory)

    st.subheader("📌 Dataset Structure")

    numerical_columns = df.select_dtypes(include=["number"]).columns.tolist()

    categorical_columns = df.select_dtypes(exclude=["number"]).columns.tolist()

    st.write(f"**Total Features:** {len(df.columns)}")

    st.write(f"**Numerical Columns ({len(numerical_columns)}):**")
    st.write(numerical_columns)

    st.write(f"**Categorical Columns ({len(categorical_columns)}):**")
    st.write(categorical_columns)

    st.subheader("📈 Statistical Summary")

    st.dataframe(df.describe())