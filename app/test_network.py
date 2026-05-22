import requests

try:

    response = requests.get(
        "https://api.openai.com"
    )

    print("Status Code:", response.status_code)

except Exception as error:

    print("Network Error:")
    print(error)