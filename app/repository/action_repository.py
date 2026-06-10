# =========================================================
# Action Repository
# Autonomous AI DBA Operations Platform
# =========================================================

import json
import os

from datetime import datetime

from app.audit.audit_logger import (
    write_audit_log
)

from app.common.error_handler import (
    handle_error
)


# =========================================================
# REPOSITORY FILE
# =========================================================

REPOSITORY_FILE = (
    "repository/actions.json"
)


# =========================================================
# SAVE ACTION
# =========================================================

def save_action(

    action_type,

    component,

    status,

    details

):

    """
    Save action to repository.
    """

    try:

        action_record = {

            "timestamp":
            str(datetime.now()),

            "action_type":
            action_type,

            "component":
            component,

            "status":
            status,

            "details":
            details

        }

        if os.path.exists(

            REPOSITORY_FILE

        ):

            with open(

                REPOSITORY_FILE,

                "r",

                encoding="utf-8"

            ) as file:

                actions = json.load(
                    file
                )

        else:

            actions = []

        actions.append(

            action_record

        )

        with open(

            REPOSITORY_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                actions,

                file,

                indent=4

            )

        write_audit_log(

            "ACTION SAVED TO REPOSITORY"

        )

        return True

    except Exception as error:

        return handle_error(

            "ACTION REPOSITORY",

            error

        )


# =========================================================
# LOAD ACTIONS
# =========================================================

def load_actions():

    """
    Load all actions.
    """

    try:

        if not os.path.exists(

            REPOSITORY_FILE

        ):

            return []

        with open(

            REPOSITORY_FILE,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(
                file
            )

    except Exception as error:

        return handle_error(

            "ACTION REPOSITORY",

            error

        )


# =========================================================
# GET ACTION COUNT
# =========================================================

def get_action_count():

    """
    Return total action count.
    """

    actions = load_actions()

    return len(
        actions
    )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    save_action(

        "RECOMMENDATION",

        "AGENT ENGINE",

        "SUCCESS",

        "Index rebuild recommendation generated."

    )

    print(

        f"\nTotal Actions: "
        f"{get_action_count()}"

    )