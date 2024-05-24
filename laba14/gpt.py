import requests

prompt = {
    "modelUri": "gpt://b1gev6kshr38q7ic83em/yandexgpt-lite",
    "completionOptions": {
        "stream": False,
        "temperature": 0.6,
        "maxTokens": "2000"
    },
    "messages": [
        {
            "role": "user",
            "text": "Как организовать успешное мероприятие? Опишите основные этапы и важные моменты, на которые нужно обратить внимание."
        }
    ]
}

url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Api-Key AQVNwk7qd42FkS8hStBsT1uslpgmWp-kIEdvDhub"
}

response = requests.post(url, headers=headers, json=prompt)
result = response.text
print(result)
