# =========================================================
# Action Repository
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime


ACTION_HISTORY = []


def save_action(

    sql_action,

    validation_result,

    execution_result

):

    record = {

        "timestamp":

        datetime.now()

        .strftime(

            "%Y-%m-%d %H:%M:%S"

        ),

        "action_type":

        sql_action[
            "action_type"
        ],

        "sql":

        sql_action[
            "sql"
        ],

        "validation":

        validation_result,

        "execution":

        execution_result

    }

    ACTION_HISTORY.append(

        record

    )

    return record


def get_action_history():

    return ACTION_HISTORY


if __name__ == "__main__":

    print(

        get_action_history()

    )