# hlcupdocs


## Запуск стрельбы в yandex-tank

Сначала нужно склонировать репозиторий:

```
git clone https://github.com/sat2707/hlcupdocs.git
cd hlcupdocs
```

Запуск стрельбы:

```bash
for i in {1..3}; do
    docker run -v $(pwd):/var/loadtest --net host -it --rm direvius/yandex-tank -c load/load_$i.ini
done
```

Ваш сервис должен быть доступен при обращении к http://127.0.0.1:80.

Для отслеживания процесса и просмотра результатов стрельб можно воспользоваться
сервисом https://overload.yandex.net. Нужно зарегистрироваться и получить токен
(нужно кликнуть по аватарке справа вверху).

```bash
# запишем полученный токен в token.txt рядом с load.ini
echo ВАШ_ТОКЕН > token.txt

# раскомментируем плагин overload
sed -i s/\#plugin_uploader/plugin_uploader/ load/load_*.ini
```
