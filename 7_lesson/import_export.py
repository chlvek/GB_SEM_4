import csv
import json

def import_csv(path):
    records = {}
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for record in reader:
            lastname, name, phone, info = record
            records[(lastname, name)] = {'phone': phone, 'info': info}
    return records


def import_json(path):
    records = {}
    with open(path, 'r') as f:
        data = json.load(f)
        for record in data.values():
            lastname = record['lastname']
            name = record['name']
            phone = record['phone']
            info = record['info']
            records[(lastname, name)] = {'phone': phone, 'info': info}
    return records


def import_txt(path):
    records = {}
    with open(path, 'r') as f:
        data = f.readlines()
    for i in range(0, len(data), 4):
        lastname = data[i+0].strip()
        name = data[i+1].strip()
        phone = data[i+2].strip()
        info = data[i+3].strip()
        records[(lastname, name)] = {'phone': phone, 'info': info}
    return records


def export_csv(data, path):
    with open(path, 'w') as f:
        writer = csv.writer(f)
        for person, params in data.items():
            lastname, name = person
            phone = params['phone']
            info = params['info']
            writer.writerow((lastname, name, phone, info))


def export_json(data, path):
    wdata = {}
    for i, ((lastname, name), d) in enumerate(data.items()):
        wdata[i] = {
            'lastname': lastname, 
            'name': name, 
            'phone': d['phone'], 
            'info': d['info']
        }
    with open(path, 'w') as f:
        f.write(json.dumps(wdata, indent=4))


def export_txt(data, path):
    with open(path, 'w') as f:
        for (lastname, name), d in data.items():
            phone = d['phone']
            info = d['info']
            f.write('\n'.join([lastname, name, phone, info]) + '\n')

