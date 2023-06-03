# csv_API
HTTP сервис для работы с файлами в формате .csv. Поддерживает загрузку файлов в базу данных, получение информации о колонках всех файлов, получение полной информации из определенного файла по его имени (доступна фильтрация по определенным колонкам), удаление файлов по их имени. Написан на python.

Чтобы развернуть сервис на своем компьютере, вам необходимо:

1. Прописать в терминал следующие команды для установки необходимых библиотек:

        pip install flask_restful
    
        pip install requests
    
        pip install pandas
    
        pip install psycopg2
    
2. Создать на своем локальном сервере базу данных PostgreSQL с названием csv_api_db (user must be postgres, password must be 2524590).
3. Запустить файл main.py для начала работы локального сервера, который будет обрабатывать HTTP запросы.

# Опции взаимодействия с HTTP сервисом csv_API:

1. Загрузка csv файла. Загрузка файла осуществляется с помощью метода: 

        url = http://127.0.0.1:5000/csv_api
        files = {'file': open('your_file_name.csv', 'rb')}
        requests.post(url, files=files)        
                       
2. Получение информации о колонках всех файлов, находящихся в базе данных сервиса. Для получения этой информации используется метод:
        
        url = http://127.0.0.1:5000/csv_api
        params = {'file_name': 'all'}
        requests.get(url, params=params)
          
3. Получение информации о файле, загруженном в базу данных по его имени с опциональной фильтрацией по определенным колонкам. Для получения этой информации используется метод:

       url = http://127.0.0.1:5000/csv_api
       params = {
        'file_name': 'your_file_name.csv',
        'filter': 'true',
        'filter_columns': json.dumps(filter_columns_list)
        }
       requests.get(url, params=params)

4. Удаление файла из базы данных сервиса по его имени. Для этого используется метод:
        
        url = 'http://127.0.0.1:5000/csv_api'
        params = {'file_name': 'your_file_name.csv'}
        requests.delete(url, params=params)
     
