import vk_api
import numpy as np
import datetime

def get_friends(user_id, fields):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    vk_session = vk_api.VkApi(
        token='vk1.a.kw7mUqA--zdyrE7lxA5RhTuV2VKeLgaKorV__he55I18H5cMzoXxL-Y81KkAQ8ynyBMwcBJQoq7oUpHDkfCtPGzm_pxsJo6mdJLYXHQ7XK42dCWrRDuXQOBWMEln384G5h86YWojArP0zAlPQSm1dN2ofwTVoVZjy0aO8jOCHdgFki5xsjpJBqTr-Tw14staGf56jYyE2rdlQFaiQcmcmQ')
    vk = vk_session.get_api()

    friends = vk.friends.get(user_id=user_id, fields=fields)
    return friends['items']

def predict_age(user_id):
    friends = get_friends(user_id, 'bdate')
    current_year = datetime.datetime.now().year
    ages = []

    for friend in friends:
        if 'bdate' in friend:
            bdate = friend['bdate']
            parts = bdate.split('.')
            if len(parts) == 3:
                day, month, year = parts
                try:
                    year = int(year)
                    age = current_year - year
                    ages.append(age)
                except ValueError:
                    continue

    if ages:
        predicted_age = np.mean(ages)
        print(f"Прогнозируевый возраст {user_id} - {predicted_age} основанный на {len(ages)} друзьях, у которых указан возраст")
        return predicted_age
    else:
        print(f"У пользователя нет действительных дат рождения друзей {user_id}.")
        return None


user_id = 122036099
predicted_age = predict_age(user_id)

