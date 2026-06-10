# =========================================================
# Action Search
# Autonomous AI DBA Operations Platform
# =========================================================

from app.repository.action_repository import (
    load_actions
)


# =========================================================
# SEARCH BY STATUS
# =========================================================

def search_by_status(

    status

):

    """
    Search actions by status.
    """

    actions = load_actions()

    results = [

        action

        for action in actions

        if action["status"].upper()

        == status.upper()

    ]

    return results


# =========================================================
# SEARCH BY COMPONENT
# =========================================================

def search_by_component(

    component

):

    """
    Search actions by component.
    """

    actions = load_actions()

    results = [

        action

        for action in actions

        if action["component"].upper()

        == component.upper()

    ]

    return results


# =========================================================
# GET LATEST ACTION
# =========================================================

def get_latest_action():

    """
    Return latest action.
    """

    actions = load_actions()

    if not actions:

        return None

    return actions[-1]


# =========================================================
# GET ACTION BY INDEX
# =========================================================

def get_action_by_index(

    index

):

    """
    Return action by index.
    """

    actions = load_actions()

    if not actions:

        return None

    if index < 0:

        return None

    if index >= len(actions):

        return None

    return actions[index]


# =========================================================
# GET ALL ACTIONS
# =========================================================

def get_all_actions():

    """
    Return all actions.
    """

    return load_actions()


# =========================================================
# DISPLAY ACTIONS
# =========================================================

def display_actions(

    actions

):

    """
    Display action results.
    """

    print("\n========================================")

    print(" ACTION SEARCH RESULTS ")

    print("========================================\n")

    if not actions:

        print(

            "No actions found."

        )

        return

    for action in actions:

        print(

            f"Timestamp      : "
            f"{action['timestamp']}"

        )

        print(

            f"Action Type    : "
            f"{action['action_type']}"

        )

        print(

            f"Component      : "
            f"{action['component']}"

        )

        print(

            f"Status         : "
            f"{action['status']}"

        )

        print(

            f"Details        : "
            f"{action['details']}"

        )

        print(

            "----------------------------------------"

        )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    successful_actions = search_by_status(

        "SUCCESS"

    )

    display_actions(

        successful_actions

    )

    print("\nLatest Action:\n")

    print(

        get_latest_action()

    )

    print("\nAction By Index:\n")

    print(

        get_action_by_index(

            0

        )

    )