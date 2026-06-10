# =========================================================
# Action Repository Manager
# Autonomous AI DBA Operations Platform
# =========================================================

from app.repository.action_repository import (
    load_actions,
    get_action_count
)


# =========================================================
# GET ACTION REPOSITORY STATUS
# =========================================================

def get_action_repository_status():

    """
    Return action repository status.
    """

    return {

        "status": "ACTIVE",

        "total_actions":
        get_action_count()

    }


# =========================================================
# DISPLAY ACTION SUMMARY
# =========================================================

def display_action_summary():

    """
    Display action repository summary.
    """

    actions = load_actions()

    print("\n========================================")

    print(" ACTION REPOSITORY ")

    print("========================================\n")

    print(

        f"Total Actions : {len(actions)}"

    )

    if actions:

        latest_action = actions[-1]

        print(

            f"Latest Action : "
            f"{latest_action['action_type']}"

        )

        print(

            f"Latest Status : "
            f"{latest_action['status']}"

        )

        print(

            f"Component     : "
            f"{latest_action['component']}"

        )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    display_action_summary()

    print("\nRepository Status:\n")

    print(

        get_action_repository_status()

    )