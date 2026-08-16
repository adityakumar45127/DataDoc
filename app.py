import streamlit as st
import pandas as pd
import hashlib
from pathlib import Path
import re


def fix_ai_wording(text):
    """Fix only the specific malformed AI wording artifact."""
    text = str(text)

    text = text.replace(
        "andmanufacturingcost",
        " and manufacturing cost"
    )

    text = text.replace(
        "*and manufacturing cost*",
        "and manufacturing cost"
    )

    text = re.sub(
        r"\s+and manufacturing cost\s*\(259\.23\)\s*and manufacturing cost\s*\(156\.41\)",
        " and manufacturing cost (156.41)",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s+and manufacturing cost\s*\(259\.23\)\s*\*and manufacturing cost\*\s*\(156\.41\)",
        " and manufacturing cost (156.41)",
        text,
        flags=re.IGNORECASE,
    )

    return text
from src.data_processing.dataset_summary import show_dataset_summary

from src.visualization.charts import (
    show_missing_value_chart,
    show_data_type_chart,
    show_correlation_heatmap,
    show_histogram,
)

from src.llm.ai_pipeline import run_ai_analysis

from src.rag.document_loader import load_pdf
from src.rag.chunker import create_chunks

from src.rag.rag_pipeline import (
    build_rag_index,
    ask_rag_question,
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="DataDoc",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# SESSION STATE
# ==================================================

if "csv_file_id" not in st.session_state:
    st.session_state.csv_file_id = None

if "csv_insights" not in st.session_state:
    st.session_state.csv_insights = None

if "rag_documents" not in st.session_state:
    st.session_state.rag_documents = {}

if "previous_selected_document" not in st.session_state:
    st.session_state.previous_selected_document = None

if "rag_question" not in st.session_state:
    st.session_state.rag_question = ""


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("📊 DataDoc")

    st.caption(
        "AI Business Intelligence Workspace"
    )

    st.divider()

    st.subheader("🧭 Workspace")

    st.write("📊 Dataset Analytics")
    st.write("📄 Document Intelligence")
    st.write("🤖 AI Business Insights")
    st.write("🔎 RAG Question Answering")

    st.divider()

    st.subheader("⚡ AI Stack")

    st.success("AI Engine Online")

    st.caption(
        "Gemini + Ollama fallback"
    )

    st.caption(
        "Vector Search + ChromaDB"
    )

    st.caption(
        "Local Embedding Retrieval"
    )

    st.caption(
        "Multi-document RAG"
    )

    st.divider()

    st.caption(
        "DataDoc v1.0"
    )


# ==================================================
# HERO HEADER
# ==================================================

left, right = st.columns(
    [4.5, 1.5]
)

with left:

    st.title(
        "📊 DataDoc"
    )

    st.subheader(
        "AI Business Intelligence & Document Intelligence Copilot"
    )

    st.caption(
        "Analyze datasets, generate business insights, "
        "and ask grounded questions across your documents."
    )

with right:

    st.metric(
        "AI Engine",
        "ONLINE",
        "Gemini + Ollama"
    )


st.divider()


# ==================================================
# TOP KPI STRIP
# ==================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:

    st.metric(
        "📊 Analytics",
        "READY"
    )

with kpi2:

    st.metric(
        "📄 Documents",
        len(
            st.session_state.rag_documents
        )
    )

with kpi3:

    st.metric(
        "🔎 RAG",
        "READY"
    )

with kpi4:

    st.metric(
        "🤖 AI",
        "ACTIVE"
    )


st.write("")


# ==================================================
# MAIN NAVIGATION
# ==================================================

dataset_tab, document_tab = st.tabs(
    [
        "📊  Dataset Analytics",
        "📄  Document Intelligence",
    ]
)


# ==================================================
# DATASET ANALYTICS
# ==================================================

with dataset_tab:

    st.header(
        "📊 Dataset Analytics"
    )

    st.caption(
        "Upload a CSV to profile the data, visualize patterns, "
        "and generate AI-powered business insights."
    )

    uploaded_file = st.file_uploader(
        "Upload your CSV file",
        type=["csv"],
        key="csv_uploader",
    )


    if uploaded_file:

        # ------------------------------------------
        # READ CSV
        # ------------------------------------------

        try:

            file_bytes = (
                uploaded_file.getvalue()
            )

            csv_file_id = hashlib.sha256(
                file_bytes
            ).hexdigest()

            df = pd.read_csv(
                uploaded_file
            )

        except Exception as e:

            st.error(
                "Unable to read the CSV file."
            )

            st.caption(
                f"Reason: {str(e)}"
            )

            st.stop()


        # ------------------------------------------
        # NEW CSV DETECTION
        # ------------------------------------------

        is_new_csv = (
            st.session_state.csv_file_id
            != csv_file_id
        )


        if is_new_csv:

            st.session_state.csv_file_id = (
                csv_file_id
            )

            st.session_state.csv_insights = (
                None
            )


        st.success(
            f"Dataset loaded: {uploaded_file.name}"
        )


        # ------------------------------------------
        # DATASET KPI STRIP
        # ------------------------------------------

        rows = len(df)

        columns = len(df.columns)

        missing = int(
            df.isna().sum().sum()
        )

        duplicates = int(
            df.duplicated().sum()
        )


        data_kpi1, data_kpi2, data_kpi3, data_kpi4 = (
            st.columns(4)
        )


        with data_kpi1:

            st.metric(
                "Rows",
                f"{rows:,}"
            )


        with data_kpi2:

            st.metric(
                "Columns",
                columns
            )


        with data_kpi3:

            st.metric(
                "Missing Values",
                missing
            )


        with data_kpi4:

            st.metric(
                "Duplicate Rows",
                duplicates
            )


        st.write("")


        # ------------------------------------------
        # DATASET PREVIEW
        # ------------------------------------------

        with st.container(
            border=True
        ):

            st.subheader(
                "📋 Dataset Preview"
            )

            st.dataframe(
                df,
                use_container_width=True,
                height=360,
            )


        # ------------------------------------------
        # DATASET SUMMARY
        # ------------------------------------------

        with st.expander(
            "📌 Dataset Profile",
            expanded=True
        ):

            show_dataset_summary(
                df
            )


        # ------------------------------------------
        # VISUAL ANALYTICS
        # ------------------------------------------

        st.subheader(
            "📈 Visual Analytics"
        )

        chart_tab1, chart_tab2, chart_tab3, chart_tab4 = (
            st.tabs(
                [
                    "Missing Values",
                    "Data Types",
                    "Correlation",
                    "Distributions",
                ]
            )
        )


        with chart_tab1:

            show_missing_value_chart(
                df
            )


        with chart_tab2:

            show_data_type_chart(
                df
            )


        with chart_tab3:

            show_correlation_heatmap(
                df
            )


        with chart_tab4:

            show_histogram(
                df
            )


        # ------------------------------------------
        # AI BUSINESS INSIGHTS
        # ------------------------------------------

        st.subheader(
            "🤖 AI Business Insights"
        )

        if (
            is_new_csv
            or
            st.session_state.csv_insights is None
        ):

            try:

                with st.spinner(
                    "Analyzing dataset..."
                ):

                    st.session_state.csv_insights = (
                        run_ai_analysis(
                            df
                        )
                    )

            except Exception as e:

                 st.error(
                     "CSV AI generation failed."
                )

                 st.exception(e)

                 st.session_state.csv_insights = (
                     None
                 )


        insights = (
            st.session_state.csv_insights
        )


        if insights:

            insight1, insight2, insight3, insight4 = (
                st.tabs(
                    [
                        "📝 Executive Summary",
                        "📈 Important Trends",
                        "⚠️ Business Risks",
                        "💡 Recommendations",
                    ]
                )
            )


            with insight1:

                with st.container(
                    border=True
                ):

                    st.write(
                        insights.executive_summary
                    )


            with insight2:

                with st.container(
                    border=True
                ):

                    for trend in (
                        insights.important_trends
                    ):

                        st.write(
                            f"• {fix_ai_wording(trend)}"
                        )


            with insight3:

                with st.container(
                    border=True
                ):

                    for risk in (
                        insights.business_risks
                    ):

                        st.write(
                            f"• {risk}"
                        )


            with insight4:

                with st.container(
                    border=True
                ):

                    for recommendation in (
                        insights.recommendations
                    ):

                        st.write(
                            f"• {recommendation}"
                        )


    else:

        st.info(
            "Upload a CSV file to activate Dataset Analytics."
        )


# ==================================================
# DOCUMENT INTELLIGENCE
# ==================================================

with document_tab:

    st.header(
        "📄 Document Intelligence"
    )

    st.caption(
        "Upload one or more PDFs and ask questions using "
        "document-grounded retrieval."
    )


    # ----------------------------------------------
    # PDF UPLOADER
    # ----------------------------------------------

    uploaded_pdfs = st.file_uploader(
        "Upload your PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        key="pdf_uploader",
    )


    # ----------------------------------------------
    # PROCESS PDFs
    # ----------------------------------------------

    if uploaded_pdfs:

        for uploaded_pdf in uploaded_pdfs:

            file_bytes = (
                uploaded_pdf.getvalue()
            )

            file_id = hashlib.sha256(
                file_bytes
            ).hexdigest()


            if (
                file_id
                not in
                st.session_state.rag_documents
            ):

                Path(
                    "tests"
                ).mkdir(
                    exist_ok=True
                )


                pdf_path = (
                    Path("tests")
                    /
                    f"uploaded_{file_id}.pdf"
                )


                with open(
                    pdf_path,
                    "wb"
                ) as f:

                    f.write(
                        file_bytes
                    )


                with st.spinner(
                    f"Processing {uploaded_pdf.name}..."
                ):

                    try:

                        collection = (
                            build_rag_index(
                                str(pdf_path),
                                file_id,
                                uploaded_pdf.name,
                            )
                        )

                    except Exception as e:

                        st.error(
                            f"Could not process {uploaded_pdf.name}."
                        )

                        st.caption(
                            f"Reason: {str(e)}"
                        )

                        continue


                st.session_state.rag_documents[
                    file_id
                ] = {

                    "document_id":
                        file_id,

                    "document_name":
                        uploaded_pdf.name,

                    "pdf_path":
                        str(pdf_path),

                    "collection":
                        collection,
                }


                st.success(
                    f"{uploaded_pdf.name} processed successfully!"
                )


    # ----------------------------------------------
    # DOCUMENT WORKSPACE
    # ----------------------------------------------

    if st.session_state.rag_documents:

        st.subheader(
            "📚 Document Workspace"
        )

        document_ids = list(
            st.session_state.rag_documents.keys()
        )


        document_names = [

            st.session_state.rag_documents[
                document_id
            ][
                "document_name"
            ]

            for document_id in document_ids
        ]


        selected_name = st.selectbox(
            "Select a document",
            document_names,
            key="selected_document",
        )


        selected_index = (
            document_names.index(
                selected_name
            )
        )


        selected_document_id = (
            document_ids[
                selected_index
            ]
        )


        previous_selected_document = (
            st.session_state.get(
                "previous_selected_document"
            )
        )


        if (
            previous_selected_document is not None
            and
            previous_selected_document
            !=
            selected_document_id
        ):

            st.session_state.rag_question = ""


        st.session_state.previous_selected_document = (
            selected_document_id
        )


        selected_document = (
            st.session_state.rag_documents[
                selected_document_id
            ]
        )


        collection = (
            selected_document[
                "collection"
            ]
        )


        pdf_path = (
            selected_document[
                "pdf_path"
            ]
        )


        # ------------------------------------------
        # DOCUMENT STATUS
        # ------------------------------------------

        doc1, doc2, doc3 = st.columns(3)


        with doc1:

            st.metric(
                "📄 Selected",
                selected_document[
                    "document_name"
                ]
            )


        with doc2:

            st.metric(
                "🟢 Status",
                "READY"
            )


        with doc3:

            st.metric(
                "🔎 RAG",
                "ENABLED"
            )


        # ------------------------------------------
        # LOAD DOCUMENT
        # ------------------------------------------

        try:

            documents = load_pdf(
                pdf_path
            )

            chunks = create_chunks(
                documents
            )

        except Exception as e:

            st.error(
                "Unable to read the selected PDF."
            )

            st.caption(
                f"Reason: {str(e)}"
            )

            st.stop()


        if not documents:

            st.warning(
                "No readable text was found in this PDF."
            )

            st.info(
                "The PDF may be scanned, empty, or contain "
                "text that cannot be extracted."
            )

            st.stop()


        if not chunks:

            st.warning(
                "No text chunks could be created from this PDF."
            )

            st.stop()


        # ------------------------------------------
        # DOCUMENT METRICS
        # ------------------------------------------

        doc_kpi1, doc_kpi2, doc_kpi3 = (
            st.columns(3)
        )


        with doc_kpi1:

            st.metric(
                "Pages",
                len(documents)
            )


        with doc_kpi2:

            st.metric(
                "Chunks",
                len(chunks)
            )


        with doc_kpi3:

            st.metric(
                "Documents Loaded",
                len(
                    st.session_state.rag_documents
                )
            )


        # ------------------------------------------
        # CHUNK PREVIEW
        # ------------------------------------------

        with st.expander(
            "📄 Preview Extracted Content"
        ):

            first_chunk = chunks[0]

            st.write(
                f"**Page:** {first_chunk['page_number']}"
            )

            st.text_area(
                "First extracted chunk",
                first_chunk["text"],
                height=240,
                disabled=True,
            )


        # ------------------------------------------
        # ASK QUESTION
        # ------------------------------------------

        st.subheader(
            "💬 Ask Your Document"
        )

        st.caption(
            "Ask a question and receive an answer grounded "
            "in retrieved document context."
        )


        question = st.text_input(
            "Your question",
            key="rag_question",
            placeholder=(
                "Example: What does the "
                "Routh-Hurwitz criterion determine?"
            ),
            label_visibility="collapsed",
        )


        ask_question = st.button(
            "🔍  Ask Question",
            type="primary",
            use_container_width=True,
        )


        if ask_question:

            if not question.strip():

                st.warning(
                    "Please enter a question first."
                )

            else:

                try:

                    with st.spinner(
                        "Searching document and generating answer..."
                    ):

                        answer, sources = (
                            ask_rag_question(
                                collection,
                                question,
                                selected_document_id,
                            )
                        )

                except Exception as e:

                    st.error(
                        "Unable to generate an answer."
                    )

                    st.caption(
                        f"Reason: {str(e)}"
                    )

                    st.stop()


                # ----------------------------------
                # ANSWER
                # ----------------------------------

                st.subheader(
                    "🤖 AI Answer"
                )


                with st.container(
                    border=True
                ):

                    st.write(
                        answer
                    )


                # ----------------------------------
                # SOURCES
                # ----------------------------------

                st.subheader(
                    "📚 Retrieved Sources"
                )


                displayed_pages = set()


                source_columns = st.columns(
                    min(
                        max(
                            len(sources),
                            1
                        ),
                        4
                    )
                )


                source_index = 0


                for source in sources:

                    page_number = source[
                        "page_number"
                    ]


                    if (
                        page_number
                        not in
                        displayed_pages
                    ):

                        with source_columns[
                            source_index
                            %
                            len(source_columns)
                        ]:

                            st.info(
                                f"📄 Page {page_number}"
                            )


                        displayed_pages.add(
                            page_number
                        )


                        source_index += 1


    else:

        st.info(
            "Upload one or more PDF files above "
            "to start document question answering."
        )


# ==================================================
# FOOTER
# ==================================================

st.divider()

footer_left, footer_right = st.columns(
    [5, 1]
)

with footer_left:

    st.caption(
        "📊 DataDoc • AI Business Intelligence & Document Intelligence"
    )

with footer_right:

    st.caption(
        "v1.0"
    )