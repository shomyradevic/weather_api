from json import load, dumps, dump
from time import perf_counter
from os import path, makedirs, stat
from pathlib import Path

#f = open(file='city.json', mode='rb')
#for something in bp(file=f):
    #print(something)


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
    conf = open(file='config.json', mode='r')
    json = load(conf)
    mapped = json['DIR_LET']
    root = json['JSON_DIR']
    create_directories()
    conf.close()
    cur_fol = ''
    for city in cities:
        name = city['name']
        if name:
            if name.find('/', 0, len(name)) >= 0:
                name = name.replace('/', '-')
            for key in mapped:
                if name[0].lower() in mapped[key]:
                    cur_fol = key
                    print(name[0].lower(), end='')
            if not cur_fol:
                cur_fol = 'dir10' # u dir10 ide sve ostalo
            file = path.join(path.join(root, cur_fol), name + '.json')
            with open(file=file, mode='w', encoding='utf-8') as f:
                dump(city, f)
                f.close()


t1 = perf_counter()

f = open(file='city.json', mode='r', encoding='utf-8')
json = load(f)
f.close()
create_files(json)

t2 = perf_counter()
print('Runtime: {0:.2f}'.format(t2-t1))