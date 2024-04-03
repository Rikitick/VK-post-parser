try:
    import time
    import requests
    import os
    import shutil
    from datetime import datetime
    import time

    def parser(i):
        if 'attachments' in posts[i]:
            photos = posts[i]['attachments']
            for j in range(len(photos)):
                try:
                    if photos[j]['type'] == 'photo':
                        if not os.path.exists(f'{user1}/Пост {i + 1}'):
                            os.mkdir(f'{user1}/Пост {i + 1}')
                        photo = [i for i in photos[j]['photo']['sizes'] if 'dict' in str(type(i))][-1]['url']
                        with open(f'{user1}/Пост {i + 1}/Фотка {j + 1}.png', 'wb') as file:
                            file.write(requests.get(photo).content)
                        if len(photos[j]['photo']['text']) != 0:
                            with open(f'{user1}/Пост {i + 1}/Описание к Фоткам.txt', 'a', encoding='utf8') as file:
                                file.write(
                                    f'<<< Описание к Фотке {j + 1} >>>\n' + photos[j]['photo']['text'] + '\n\n\n\n')
                except Exception as er:
                    print(f'Не удалось собрать фото! Причина: {er}')

                try:
                    if photos[j]['type'] == 'video':
                        try:
                            key = '_' + photos[j]["video"]["access_key"]
                        except:
                            key = ''
                        if not os.path.exists(f'{user1}/Пост {i + 1}'):
                            os.mkdir(f'{user1}/Пост {i + 1}')
                        video = f'https://api.vk.com/method/video.get?videos={photos[j]["video"]["owner_id"]}_{photos[j]["video"]["id"]}{key}&access_token={token}&v=5.131'
                        resp = requests.get(video).json()
                        
                except Exception as er:
                    print(f'Не удалось скачать видео: {er}')

        if len(posts[i]['text']) != 0:
            if not os.path.exists(f'{user1}/Пост {i + 1}'):
                os.mkdir(f'{user1}/Пост {i + 1}')
            with open(f'{user1}/Пост {i + 1}/Текст поста.txt', 'w', encoding='utf8') as file:
                file.write(posts[i]['text'])

        print(f'Собрал пост №{i + 1}')

    # Ваш токен от аккаунта
    token = ''
    url = None
    count = None
    counter = 1
    date = None
    numbers = []

    user = input('Укажите ID или домен пользователя или группы (Например: id295619472 или sjbody): ')
    if os.path.exists(f'{user}'):
        quest = input('Вы хотите обновить данные по этой группе (1 - ДА, 2 - НЕТ): ')
        if quest == '1':
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), user)
            shutil.rmtree(path)
            user1 = user
            os.mkdir(user1)
        else:
            while os.path.exists(user + '-' + str(counter)):
                counter += 1
            user1 = user + '-' + str(counter)
            os.mkdir(user1)
    else:
        user1 = user
        os.mkdir(user)

    filter1 = input('Как собирать посты (1 - по количеству, 2 - по дате): ')
    if filter1 == '1':
        count = int(input('Укажите число постов (максимум - 100): '))
    else:
        date = input('Укажите дату и промежуток дат (5.10.2022 или 12.10.2022-15.10.2022): ').split('-')

    f = input(
        'Напишите номера постов, которые нужно собрать БЕЗ ЗАПЯТЫХ (1 2 4 5-8 10 13-15 или 0 - все подряд): ').split()
    if f[0] != '0':
        for i in f:
            if '-' in i:
                for j in range(int(i.split('-')[0]), int(i.split('-')[-1]) + 1):
                    numbers.append(int(j))
            else:
                numbers.append(int(i))

    if user[2:].isdigit() and len(user[2:]) == 9:
        if count is not None:
            url = f'https://api.vk.com/method/wall.get?owner_id={user[2:]}&count={count}&access_token={token}&v=5.131'
        else:
            url = f'https://api.vk.com/method/wall.get?owner_id={user[2:]}&count=100&access_token={token}&v=5.131'
    else:
        if count is not None:
            url = f'https://api.vk.com/method/wall.get?domain={user}&count={count}&access_token={token}&v=5.131'
        else:
            url = f'https://api.vk.com/method/wall.get?domain={user}&count=100&access_token={token}&v=5.131'

    print(url)
    req = requests.get(url).json()

    posts = req['response']['items']

    if date is not None:
        if len(date) == 1:
            for i in range(len(posts)):
                if len(numbers) != 0:
                    if i + 1 in numbers:
                        if int(posts[i]['date']) + 7200 > int(
                                datetime.strptime(f'{"-".join(date[0].split(".")[::-1])} 00:00:00',
                                                  '%Y-%m-%d %H:%M:%S').timestamp()):
                            parser(i)

                else:
                    if int(posts[i]['date']) + 7200 > int(
                            datetime.strptime(f'{"-".join(date[0].split(".")[::-1])} 00:00:00',
                                              '%Y-%m-%d %H:%M:%S').timestamp()):
                        parser(i)


        else:
            print('Ищу посты, ожидайте...')
            for i in range(len(posts)):
                if len(numbers) != 0:
                    if i + 1 in numbers:
                        if int(datetime.strptime(f'{"-".join(date[-1].split(".")[::-1])} 00:00:00',
                                                 '%Y-%m-%d %H:%M:%S').timestamp()) > int(posts[i]['date']) + 7200 > int(
                            datetime.strptime(f'{"-".join(date[0].split(".")[::-1])} 00:00:00',
                                              '%Y-%m-%d %H:%M:%S').timestamp()):
                            parser(i)
                else:
                    if int(datetime.strptime(f'{"-".join(date[-1].split(".")[::-1])} 00:00:00',
                                             '%Y-%m-%d %H:%M:%S').timestamp()) > int(posts[i]['date']) + 7200 > int(
                        datetime.strptime(f'{"-".join(date[0].split(".")[::-1])} 00:00:00',
                                          '%Y-%m-%d %H:%M:%S').timestamp()):
                        parser(i)

    else:
        for i in range(len(posts)):
            if len(numbers) != 0:
                if i + 1 in numbers:
                    parser(i)
            else:
                parser(i)




except Exception as er:
    print(f'ОШИБКА: {er}')
    time.sleep(10)