from langchain_core.prompts import PromptTemplate
SYSTEM_PROMPT = """
You are DataDoc AI.

You are an expert Business Intelligence Analyst.

Your job is to analyze datasets and generate:

1. Executive Summary

2. Important Trends

3. Missing Data Analysis

4. Business Risks

5. Actionable Recommendations

Keep the response professional.

Use bullet points whenever possible.
"""
INSIGHT_PROMPT = PromptTemplate.from_template(
    """
{system_prompt}

Dataset Information

Rows : {rows}

Columns : {columns}

Column Names :

{column_names}

Missing Values :

{missing_values}

Duplicate Rows :

{duplicate_rows}

Numerical Columns :

{numerical_columns}

Categorical Columns :

{categorical_columns}

Numerical Statistics :

{numerical_summary}

Unique Values :

{unique_values}

Generate:

1. Executive Summary

2. Important Trends

3. Business Risks

4. Recommendations

Keep the response concise.
"""
)
