from src.llm.insight_generator import generate_ai_insights


def run_ai_analysis(df):

    insights = generate_ai_insights(df)

    return insights