import vk_api
import datetime
import matplotlib.pyplot as plt

def messages_get_history(user_id, offset=0, count=20):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "offset must be non-negative integer"
    assert isinstance(count, int), "count must be positive integer"
    assert count > 0, "count must be positive integer"

    vk_session = vk_api.VkApi(
        token='vk1.a.kw7mUqA--zdyrE7lxA5RhTuV2VKeLgaKorV__he55I18H5cMzoXxL-Y81KkAQ8ynyBMwcBJQoq7oUpHDkfCtPGzm_pxsJo6mdJLYXHQ7XK42dCWrRDuXQOBWMEln384G5h86YWojArP0zAlPQSm1dN2ofwTVoVZjy0aO8jOCHdgFki5xsjpJBqTr-Tw14staGf56jYyE2rdlQFaiQcmcmQ')
    vk = vk_session.get_api()

    history = vk.messages.getHistory(user_id=user_id, offset=offset, count=count)
    return history['items']

user_id = 183716165
messages = messages_get_history(user_id, count=200)

def plot_message_frequency(user_id, count=200):
    messages = messages_get_history(user_id, count=count)

    dates = [datetime.datetime.fromtimestamp(message['date']) for message in messages]

    date_counts = {}
    for date in dates:
        date_str = date.strftime('%Y-%m-%d')
        if date_str in date_counts:
            date_counts[date_str] += 1
        else:
            date_counts[date_str] = 1


    sorted_dates = sorted(date_counts.items())

    dates, counts = zip(*sorted_dates)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, counts, marker='o')
    plt.xlabel('Дата')
    plt.ylabel('Количество сообщений')
    plt.title(f'Частота сообщений с пользователем {user_id}')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

user_id = 183716165
plot_message_frequency(user_id, count=200)
