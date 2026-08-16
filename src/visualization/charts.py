import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff


def show_missing_value_chart(df):

    missing_df = (
        df.isnull()
        .sum()
        .reset_index()
    )

    missing_df.columns = [
        "Column",
        "Missing Values"
    ]

    missing_df = missing_df[
        missing_df["Missing Values"] > 0
    ]

    if missing_df.empty:

        st.success("✅ No Missing Values Found")

        return

    fig = px.bar(
        missing_df,
        x="Column",
        y="Missing Values",
        title="Missing Values by Column"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def show_data_type_chart(df):

    numerical = len(
        df.select_dtypes(include=["number"]).columns
    )

    categorical = len(
        df.select_dtypes(exclude=["number"]).columns
    )

    import pandas as pd

    chart_df = pd.DataFrame({

        "Type": [
            "Numerical",
            "Categorical"
        ],

        "Count": [
            numerical,
            categorical
        ]
    })

    fig = px.pie(

        chart_df,

        names="Type",

        values="Count",

        title="Column Type Distribution"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def show_correlation_heatmap(df):

    numerical_df = df.select_dtypes(include=["number"])

    if numerical_df.shape[1] < 2:

        st.warning("At least two numerical columns are required.")

        return

    corr = numerical_df.corr()

    fig = ff.create_annotated_heatmap(

        z=corr.values,

        x=list(corr.columns),

        y=list(corr.index),

        annotation_text=round(corr, 2).values,

        colorscale="Viridis",

        showscale=True

    )

    fig.update_layout(
        title="Correlation Heatmap"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
def show_histogram(df):

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    if len(numerical_columns) == 0:

        st.warning("No numerical columns found.")

        return

    selected_column = st.selectbox(

        "Select a numerical column",

        numerical_columns,

        key="histogram_column"

    )

    fig = px.histogram(

        df,

        x=selected_column,

        title=f"Distribution of {selected_column}"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )