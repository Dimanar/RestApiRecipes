import psycopg2 as psql
import os
import json
import re

class Save_db:

    def __init__(self):
        self.__path = 'Data'
        self.__conn = psql.connect(
            dbname='recipes', user='postgres',
            password='31102000aA', host='localhost',
            port='5432')
        self.__curs = self.__conn.cursor()
        print('All is ready to save')

    def __delete__(self, instance):
        self.__curs.close()
        self.__conn.close()

    def save_to_db(self, debug=False):
        for root, dir, files in os.walk(self.__path):
            print('START')
            for i, file in enumerate(iter(files)):
                if i == 0:
                    continue
                path_tile = root + '/' + file
                if debug:
                    print(path_tile)
                with open(path_tile) as json_file:
                    recipes = json.load(json_file)
                    for recipe in recipes:
                        self.__query_to_save(recipe)


    def __query_to_save(self, recipe, debug=False):
        type, pack = recipe['type'], recipe['package']
        link, name = recipe['link'], recipe['name']
        summary, image = recipe['summary'], recipe['image']
        meta = [''.join(meta) for meta in recipe['meta']]
        meta = '<->'.join(meta)
        ingred = '<->'.join(recipe['ingredients'])
        direction, facts = '<->'.join(recipe['direction']), recipe['facts']
        postgres_insert_query = """ INSERT INTO food(id,type,pack,link,name,summary,image,meta,ingred,direction,facts ) 
                                    VALUES (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); """
        record_to_insert = (type, pack, link, name, summary, image, meta, ingred, direction, facts)
        self.__curs.execute(postgres_insert_query, record_to_insert)
        self.__conn.commit()
        count = self.__curs.rowcount
        if debug:
            print(count, "Record inserted successfully into mobile table")
