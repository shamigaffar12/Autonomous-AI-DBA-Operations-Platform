# =========================================================
# NLP DBA Assistant
# Autonomous AI DBA Operations Platform
# =========================================================

from app.nlp_assistant.intent_classifier import (
    classify_dba_intent
)

from app.nlp_assistant.nlp_response_engine import (
    build_nlp_response
)


# =========================================================
# HANDLE DBA QUERY
# =========================================================

def handle_dba_query(
    user_query
):
    """
    Handle natural language DBA query.
    """

    intent_result = classify_dba_intent(
        user_query
    )

    response = build_nlp_response(
        user_query=user_query,
        intent_result=intent_result
    )

    return {
        "user_query": user_query,
        "intent": intent_result.get(
            "intent"
        ),
        "confidence": intent_result.get(
            "confidence"
        ),
        "risk_level": intent_result.get(
            "risk_level"
        ),
        "assistant_response": response.get(
            "assistant_response"
        ),
        "summary": response.get(
            "summary"
        ),
        "recommended_next_action": response.get(
            "recommended_next_action"
        )
    }