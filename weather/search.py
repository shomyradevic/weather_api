from json import load, dump
from os import path, makedirs, listdir
from pathlib import Path


def append_item(o: list, filename: str, directory='dir10'):
    new = list(o)
    with open(file=path.join(path.join('json_files', directory), filename),
              mode='r',
              encoding='utf-8') as f:
        js = load(f)
        f.close()
        new.append(dict({'id': js['id'], 'name': js['name'] + ", " + js["country"]}))
    return new


def search_query(query: str):
    found, fol = [], 'dir10' # dict list
    q = query.lower()
    first_letter = str(q)
    if len(q) > 1:
        first_letter = q[0]
    with open(file='config.json', mode='r', encoding='utf-8') as f:
        js = load(f)
        f.close()
        dir_let = js['DIR_LET']
        for key in dir_let:
            if first_letter in dir_let[key]:
                fol = key
                for file in listdir(path.join('json_files', fol)):
                    if len(found) == 6:
                        return found
                    if len(q) > 1:
                        if file.lower().find(q, 0, len(file)) >= 0:
                            found = append_item(o=found, filename=file, directory=fol)
                    else:
                        if file.lower()[0] == q:
                            found = append_item(o=found, filename=file, directory=fol)
        if fol == 'dir10':
            for file in listdir(path.join('json_files', 'dir10')):
                if len(found) == 6:
                    return found
                if len(q) > 1:
                    if file.lower().find(q, 0, len(file)) >= 0:
                        found = append_item(o=found, filename=file)
                else:
                    if file.lower()[0] == q:
                        found = append_item(o=found, filename=file)
    return found


def alphanumeric(cityname: str):
    l = list(cityname)
    flag = False
    for i in reversed(range(len(l))):
        if flag:
            flag = False
            i -= 0
        if l[i] != ' ':
            if not l[i].isalpha():
                l.pop(i)
                flag = True
    return ''.join(l)


def create_directories():
    conf = open(file='config.json', mode='r', encoding='utf-8')
    json = load(conf)
    root = json['JSON_DIR']
    conf.close()
    if not Path(root).is_dir():
        makedirs(root)
    for i in range(1, 11):
        makedirs(path.join('json_files', 'dir' + str(i)))


def create_files(cities):
    conf = open(file='config.json', mode='r', encoding='utf-8')
    json = load(conf)
    mapped = json['DIR_LET']
    root = json['JSON_DIR']
    create_directories()
    conf.close()
    for city in cities:
        cur_fol = 'dir10'
        name = city['name']
        if name:
            new_name = alphanumeric(name)
            if not new_name:
                new_name = name
            for key in mapped:
                if new_name[0].lower() in mapped[key]:
                    cur_fol = key
            file = path.join(path.join(root, cur_fol), new_name + ", " + city["country"] + '.json')
            with open(file=file, mode='w', encoding='utf-8') as f:
                dump(city, f)
                f.close()
