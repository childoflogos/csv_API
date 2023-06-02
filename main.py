import json
from threading import Thread
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import requests
import pandas as pd
import time
import database

db = database.Database()

class CsvApi(Resource):
    def __init__(self):
        pass

    def post(self):
        file = request.files['file']
        data = pd.read_csv(file)
        file_name = file.filename
        db.add_file(file_name, data)
        return f'File {file_name} added to the database'

    def get(self):
        file_name = request.args.get('file_name')
        if file_name == "all":
            files = db.get_all_files()
            ret = []
            for file in files:
                name = file[0]
                columns = file[1].split('\n')[0].split(' ')
                cleaned_columns = []
                for col in columns:
                    if col != '':
                        cleaned_columns.append(col)
                ret.append([name, cleaned_columns])
            return ret
        elif file_name is not None:
            data = db.get_file(file_name)
            if data:
                data = data[0].split(' ')
                cleaned_data = []
                for element in data:
                    if element != '':
                        cleaned_data.append(element)
                rows = split_list(cleaned_data)
                if request.args.get('filter') == 'true':
                    return filter_table(rows, request.args.get('filter_columns'))
            else:
                return 'There is no such file'
        else:
            return 'Please provide file_name parameter.'

    def delete(self):
        file_name = request.args.get('file_name')
        if file_name is not None:
            db.delete_file(file_name)
            return f'File {file_name} deleted from the database'
        else:
            return 'Please provide file_name parameter.'

def filter_table(table, filter_columns):
    unfiltered_columns = table[0]
    filter_columns = json.loads(filter_columns)
    if unfiltered_columns == filter_columns:
        return table
    indexes = []
    for col in filter_columns:
        indexes.append(unfiltered_columns.index(col))
    filtered_table = []
    for row in table:
        new_row = []
        for idx in indexes:
            new_row.append(row[idx])
        filtered_table.append(new_row)
    return filtered_table

def split_list(lst):
    sublists = []
    sublist = []
    for item in lst:
        if '\n' in item:
            sublist.append(item.split('\n')[0])
            sublists.append(sublist)
            sublist = []
        else:
            sublist.append(item)
    sublists.append(sublist)
    return sublists

def test():
    time.sleep(1)
    url = 'http://127.0.0.1:5000/csv_api'
    params = {'file_name': 'data.csv'}
    response = requests.delete(url, params=params)
    print(response.text)
    files = {'file': open('data.csv', 'rb')}
    response = requests.post(url, files=files)
    print(response.text)
    params = {
        'file_name': 'data.csv',
        'filter': 'true',
        'filter_columns': json.dumps(['ETH', 'USDT'])
    }
    response = requests.get(url, params=params)
    print(response.text)

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(CsvApi, '/csv_api', '/csv_api/')
    th = Thread(target=test)
    th.start()
    app.run()
