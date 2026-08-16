from src.llm.llm_router import (
    generate_structured_with_fallback
)

from src.llm.prompts import (
    SYSTEM_PROMPT,
    INSIGHT_PROMPT
)

from src.data_processing.dataset_profiler import (
    profile_dataset
)

from src.llm.output_schema import (
    BusinessInsight
)


# ==================================================
# GENERATE AI BUSINESS INSIGHTS
# ==================================================

def generate_ai_insights(df):

    # ----------------------------------------------
    # Profile dataset
    # ----------------------------------------------

    dataset_profile = profile_dataset(
        df
    )


    # ----------------------------------------------
    # Build prompt
    # ----------------------------------------------

    prompt = INSIGHT_PROMPT.format(

        system_prompt=SYSTEM_PROMPT,

        rows=dataset_profile[
            "rows"
        ],

        columns=dataset_profile[
            "columns"
        ],

        column_names=dataset_profile[
            "column_names"
        ],

        missing_values=dataset_profile[
            "missing_values"
        ],

        duplicate_rows=dataset_profile[
            "duplicate_rows"
        ],

        numerical_columns=dataset_profile[
            "numerical_columns"
        ],

        categorical_columns=dataset_profile[
            "categorical_columns"
        ],

        numerical_summary=dataset_profile[
            "numerical_summary"
        ],

        unique_values=dataset_profile[
            "unique_values"
        ]

    )


    # ----------------------------------------------
    # Gemini → Ollama fallback
    # ----------------------------------------------

    response = generate_structured_with_fallback(

        prompt,

        BusinessInsight

    )


    # ----------------------------------------------
    # Validate response
    # ----------------------------------------------

    if not isinstance(
        response,
        BusinessInsight
    ):

        raise RuntimeError(
            "The LLM returned an invalid "
            "BusinessInsight response."
        )


    return response