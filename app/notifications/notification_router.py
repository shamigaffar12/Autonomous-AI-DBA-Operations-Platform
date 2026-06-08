# =========================================================
# Notification Router
# Autonomous AI DBA Operations Platform
# =========================================================


# =========================================================
# GET NOTIFICATION ROUTE
# =========================================================

def get_notification_route(

    severity

):

    """
    Route notifications based
    on incident severity.
    """

    severity = severity.upper()

    if severity == "CRITICAL":

        return {

            "send_email": True,

            "send_teams": True,

            "escalation_required": True

        }

    elif severity == "HIGH":

        return {

            "send_email": True,

            "send_teams": True,

            "escalation_required": False

        }

    elif severity == "MEDIUM":

        return {

            "send_email": True,

            "send_teams": False,

            "escalation_required": False

        }

    return {

        "send_email": False,

        "send_teams": False,

        "escalation_required": False

    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    print(

        get_notification_route(

            "HIGH"

        )

    )