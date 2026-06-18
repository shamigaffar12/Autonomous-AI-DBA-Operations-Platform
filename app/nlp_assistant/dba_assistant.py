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

from app.nlp_assistant.workflow_router import (
    route_nlp_workflow
)


# =========================================================
# WORKFLOW ROUTING INTENTS
# =========================================================

WORKFLOW_ROUTING_INTENTS = [
    "START_MONITORING",
    "STOP_MONITORING",
    "RUN_HEALTH_CHECK",
    "RUN_FULL_DBA_WORKFLOW",
    "DEADLOCK_ANALYSIS",
    "BACKUP_STATUS",
    "BACKUP_REQUEST",
    "FULL_BACKUP_REQUEST",
    "DIFFERENTIAL_BACKUP_REQUEST",
    "LOG_BACKUP_REQUEST",
    "CREATE_APPROVAL_REQUEST",
    "EXECUTE_APPROVED_REMEDIATION"
]


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

    workflow_result = None

    if intent_result.get(
        "intent"
    ) in WORKFLOW_ROUTING_INTENTS:

        workflow_result = route_nlp_workflow(
            user_query=user_query,
            intent=intent_result.get(
                "intent"
            ),
            risk_level=intent_result.get(
                "risk_level"
            )
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
        ),
        "workflow_result": workflow_result
    }