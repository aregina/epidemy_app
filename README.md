Back-end for mobile app, based on Django REST framework.

1. Скачать PostreSQL
2. Создать базу
3. Командой psql -d [yourdatabase] -c "CREATE EXTENSION postgis;" установить дополнение для базы, нужно для хранения и работы с геоданными
4. Восстановить из дампа базу эпидемии (Mysql)
5. В папке epidemy созадать файл local_settings.py в котором прописать параметры подключения к базам
6. Чтобы проверить работу
