import json
import pymysql


def make_treejson():
    db = pymysql.connect(host="localhost", user="root", password='liu123456',
                         database="chinese_poetry", charset='utf8')
    cursor = db.cursor()
    cursor.execute("select * from the_book_of_songs")
    rs = cursor.fetchall()
    print(rs[0])

    booksong = {}
    booksong['name'] = '诗经'
    booksong['children'] = []
    booksong['theme'] = 'none'

    section_list = []
    section_index = []

    chapter_list = []
    chapter_index = []

    for item in rs:
        if item[3] not in section_index:
            section_index.append(item[3])
            section_list.append({'name': item[3], 'children': [], 'theme': 'none'})
        section_list[section_index.index(item[3])]['children'].append(
            {'id': item[0], 'title': item[1], 'content': item[4], 'theme': item[5]})

    for item in rs:
        if item[2] not in chapter_index:
            chapter_index.append(item[2])
            chapter_list.append({'name': item[2], 'children': [], 'theme': 'none'})
        if section_list[section_index.index(item[3])] not in chapter_list[chapter_index.index(item[2])]['children']:
            chapter_list[chapter_index.index(item[2])]['children'].append(section_list[section_index.index(item[3])])

    fys_list = []
    fys_index = []
    for item in rs:
        key = list(item[2])[1]
        if key not in fys_index:
            fys_index.append(key)
            fys_list.append({'name': key, 'children': [], 'theme': 'none'})
        if chapter_list[chapter_index.index(item[2])] not in fys_list[fys_index.index(key)]['children']:
            fys_list[fys_index.index(key)]['children'].append(chapter_list[chapter_index.index(item[2])])

    for item in fys_list:
        booksong['children'].append(item)

    treejson = json.dumps(booksong, ensure_ascii=False, indent=1)
    # print(treejson)
    url = 'app/static/jsondata/treemap.json'
    f = open(url, 'w', encoding='utf-8')
    f.write(treejson)
    f.close()
    return 'static/jsondata/treemap.json'
