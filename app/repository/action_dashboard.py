# =========================================================
# Action Dashboard Data
# Autonomous AI DBA Operations Platform
# =========================================================

from app.repository.action_repository import (
    load_actions
)


# =========================================================
# GET ACTION DASHBOARD DATA
# =========================================================

def get_action_dashboard_data():

    """
    Return action repository data.
    """

    actions = load_actions()

    return {

        "total_actions":
        len(actions),

        "actions":
        list(

            reversed(

                actions

            )

        )

    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    data = get_action_dashboard_data()

    print(

        f"\nTotal Actions: "
        f"{data['total_actions']}"

    )