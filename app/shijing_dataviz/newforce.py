import json
import pymysql

def make_forcejson():
    db = pymysql.connect(host="localhost", user="root", password='liu123456',
                         database="chinese_poetry", charset='utf8')
    cursor = db.cursor()
    cursor.execute("select * from the_book_of_songs")
    rs = cursor.fetchall()
    print(rs[0])

    themes = {}
    for item in rs:
        if item[5] not in themes:
            themes[item[5]] = 1
        else:
            themes[item[5]] += 1
    print(themes)
    nodes = []
    links = []
    emotion = {}
    emotion_type = []
    emotion_value = []
    for item in rs:
        e_list = item[6].split('、')
        for e in e_list:
            if e not in emotion:
                emotion[e] = 1
            else:
                emotion[e] += 1
    emotion=sorted(emotion.items(),key=lambda x: x[1], reverse=True)
    for item in emotion:
        emotion_type.append(item[0])
        emotion_value.append(item[1])
    value_sum = sum(emotion_value)
    for i in range(len(emotion_value)):
        emotion_value[i] = round(emotion_value[i] / value_sum, 4)

    nodes.append({'name': '诗经', 'num': 305, 'emotion_type': emotion_type, 'emotion_value': emotion_value})
    all_emotion=['思', '喜', '忧', '悲', '其他', '怒', '恐']
    for it in themes:
        # print(it)

        cursor = db.cursor()
        sql = "select * from the_book_of_songs where theme=%s"
        cursor.execute(sql, it)
        r = cursor.fetchall()

        r_emotion = {}
        r_emotion_type = []
        r_emotion_value = []
        print(r)
        for item1 in r:
            e_list = item1[6].split('、')
            for e in e_list:
                if e not in r_emotion:
                    r_emotion[e] = 1
                else:
                    r_emotion[e] += 1
        r_emotion=sorted(r_emotion.items(),key=lambda x: x[1], reverse=True)
        for item2 in r_emotion:
            r_emotion_type.append(item2[0])
            r_emotion_value.append(item2[1])
        r_value_sum = sum(r_emotion_value)
        for i in range(len(r_emotion_value)):
            r_emotion_value[i] = round(r_emotion_value[i] / r_value_sum, 4)
        for item3 in all_emotion:
            if item3 not in r_emotion_type:
                r_emotion_type.append(item3)
                r_emotion_value.append(0)
        # print(r_emotion_type)
        # print(r_emotion_value)
        # print(nodes)
        # print('fenjiexian')
        # print(it)
        # print(themes[it])
        nodes.append({'name': it, 'num': themes[it], 'emotion_type': r_emotion_type, 'emotion_value': r_emotion_value})

    for i in range(1, len(themes) + 1):
        links.append({'source': 0, 'target': i, 'num': nodes[i]['num']})

    forcejson = json.dumps({'nodes': nodes, 'links': links}, ensure_ascii=False, indent=1)
    # print(forcejson)
    url = 'app/static/jsondata/newforce.json'
    f = open(url, 'w', encoding='utf-8')
    f.write(forcejson)
    f.close()
    return 'static/jsondata/newforce.json'
