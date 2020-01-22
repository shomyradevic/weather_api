try:
    from json import load
    from weather.search import create_files
    try:
        with open(file='city.json', mode='r', encoding='utf-8') as f:
            j = load(f)
            f.close()
            create_files(j)
    except FileNotFoundError as n:
        print(n)
except ImportError as i:
    print(i)
