"""
Забираем всю информацию из контейнеров и на её основе создаем таски в CTFd
"""
import os
import json
import requests
import yaml

from CTFd import create_app

app = create_app()

host = input("Please input your url in format http://<host>: ")

access_token = input("Please input your admin access token: ")

game_host = input("Please input game host without port: ")

def generate_session():
    s = requests.Session()
    s.headers.update({"Authorization": f"Token {access_token}"})
    return s

def get_flag(compose_data):
    if "FLAG" in compose_data['environment']:
        return compose_data['environment']['FLAG']

    if "FLAG" in compose_data.get('build', {}).get('args', False):
        return compose_data['build']['args']['FLAG']

    return 'SUPERSECRETFLAG'


if __name__ == "__main__":
    with app.app_context():
        db = app.db

        # Generating Challenges
        print("GENERATING CHALLENGES")
        print(os.listdir('../'))

        s = generate_session()
        service = []
        print("Read docker-compose.yml file")
        with open("../docker-compose.yml", 'r') as stream:
            try:
                services = yaml.safe_load(stream)['services']
            except yaml.YAMLError as exc:
                print(exc)

        for task in os.listdir("../"):
            json_file = f"../{task}/to_import.json"
            if not os.path.exists(json_file):
                continue

            with open(json_file, "r") as file:
                data = json.loads(file.read())
                print(data)

                print(services[task])
                to_read = ""
                for l in data['links']:
                    to_read += f"<a href='{l}'>Ссылка</a>\n<br />"

                port = services[task]['ports'][0].split(':')[0]
                description = f"{data['description']} <br /> <a href='{game_host}:{port}'>Ссылка на задание</a>"

                print({"name": data['name'], "category": data['category'],
                                         "description": description, "value": data['value'],
                                         "state": "visible", "type": "standard", "to_read": to_read})

                challenge = s.post(url=f"{host}/api/v1/challenges",
                                   json={"name": data['name'], "category": data['category'],
                                         "description": description, "value": data['value'],
                                         "state": "visible", "type": "standard", "to_read": to_read},
                                   )

                response = challenge.json()['data']

                flag = get_flag(services[task])
                print(flag)
                data = {"content": flag, "type": "static", "challenge": response['id']}
                r = s.post(url=f"{host}/api/v1/flags", json=data)
                r.raise_for_status()