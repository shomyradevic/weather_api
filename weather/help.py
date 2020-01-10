from datetime import datetime, timedelta


def process_data(data: dict):
    date_and_time = datetime.utcfromtimestamp(data["json"]["sys"]["sunrise"])
    just_time = date_and_time.strftime("%H:%M:%S")
    data["json"]["sys"]["sunrise"] = just_time 
    date_and_time = datetime.utcfromtimestamp(data["json"]["sys"]["sunset"])
    just_time = date_and_time.strftime("%H:%M:%S")
    data["json"]["sys"]["sunset"] = just_time
    data = timezone(data=data)
    return data


def timezone(data: dict):
    offset = data["json"]["timezone"]
    sr = datetime.strptime(data["json"]["sys"]["sunrise"], "%H:%M:%S") + timedelta(seconds=offset)
    ss = datetime.strptime(data["json"]["sys"]["sunset"], "%H:%M:%S") + timedelta(seconds=offset)
    data["json"]["sys"]["sunrise"] = sr.strftime("%H:%M:%S")
    data["json"]["sys"]["sunset"] = ss.strftime("%H:%M:%S")
    return data


def log(value: str):
    with open(file="log.log", mode="a", encoding="utf-8") as f:
        f.write(str(datetime.now()) + " - " + value + "\n")
        f.close()