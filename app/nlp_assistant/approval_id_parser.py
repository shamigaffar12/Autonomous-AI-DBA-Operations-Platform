# =========================================================
# NLP Approval ID Parser
# Autonomous AI DBA Operations Platform
# =========================================================

import re


# =========================================================
# EXTRACT APPROVAL ID
# =========================================================

def extract_approval_id(
    user_query
):
    """
    Extract UUID approval ID from natural language command.
    """

    if not user_query:

        return None

    approval_id_pattern = (
        r"[0-9a-fA-F]{8}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{12}"
    )

    match = re.search(
        approval_id_pattern,
        user_query
    )

    if match:

        return match.group(
            0
        )

    return None