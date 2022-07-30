from email.policy import default
import json
import rich_click as click
import requests
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class Sublimation():
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def sublimation(self):
        self.token = self.get_token()
        parsed_json = json.dumps(self.network_objects(), indent=4, sort_keys=True)
        self.all_files(parsed_json)

    def get_token(self):
        access_token = None
        requests.packages.urllib3.disable_warnings()
        payload = f'{{"grant_type": "password", "username": "{ self.username }", "password": "{ self.password }" }}'
        auth_headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response = requests.post(f"{ self.url }/api/fdm/latest/fdm/token",
                                data=payload, headers=auth_headers, verify=False)
        access_token = response.json().get('access_token')
        return(access_token)

    def network_objects(self):
        self.url = f"{ self.url }/api/fdm/latest/object/networks"
        headers = { 
            "Accept": "application/json",
            "Authorization": f"Bearer { self.token }"
        }
        response = requests.request("GET", self.url, headers=headers, verify=False)
        print(f"<Network Objects Status Code { response.status_code } for { self.url }")
        response_dict = response.json()
        return(response_dict)

    def json_file(self, parsed_json):
        if "networks" in self.url:
            with open('Network Objects/JSON/Network Objects.json', 'w') as f:
                f.write(parsed_json)

    def yaml_file(self, parsed_json):
        clean_yaml = yaml.dump(json.loads(parsed_json), default_flow_style=False)
        if "networks" in self.url:
            with open('Network Objects/YAML/Network Objects.yaml', 'w') as f:
                f.write(clean_yaml)

    def csv_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        csv_template = env.get_template('ftd_csv.j2')
        csv_output = csv_template.render(api = self.url,
                                        data_to_template = json.loads(parsed_json))
        if "networks" in self.url:
            with open('Network Objects/CSV/Network Objects.csv', 'w') as f:
                f.write(csv_output)

    def markdown_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        markdown_template = env.get_template('ftd_markdown.j2')
        markdown_output = markdown_template.render(api = self.url,
                                        data_to_template = json.loads(parsed_json))
        if "networks" in self.url:
            with open('Network Objects/Markdown/Network Objects.md', 'w') as f:
                f.write(markdown_output)

    def html_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        html_template = env.get_template('ftd_html.j2')
        html_output = html_template.render(api = self.url,
                                        data_to_template = json.loads(parsed_json))
        if "networks" in self.url:
            with open('Network Objects/HTML/Network Objects.html', 'w') as f:
                f.write(html_output)

    def mindmap_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        mindmap_template = env.get_template('ftd_mindmap.j2')
        mindmap_output = mindmap_template.render(api = self.url,
                                        data_to_template = json.loads(parsed_json))
        if "networks" in self.url:
            with open('Network Objects/Mindmap/Network Objects.md', 'w') as f:
                f.write(mindmap_output)

    def all_files(self, parsed_json):
        self.json_file(parsed_json)
        self.yaml_file(parsed_json)
        self.csv_file(parsed_json)
        self.markdown_file(parsed_json)
        self.html_file(parsed_json)
        self.mindmap_file(parsed_json)

@click.command()
@click.option('--url',
    prompt='FTD URL',
    help=('The FTD URL'),
    required=True,
    envvar='URL')
@click.option('--username',
    prompt='FTD Username',
    help=('The FTD Username'),
    required=True,
    envvar='USERNAME')
@click.option('--password',
    prompt='FTD Password',
    help=('The FTD Password'),
    required=True,
    envvar='PASSWORD',
    hide_input=True)
def cli(url, username, password):
    invoke_class = Sublimation(url, username, password)
    invoke_class.sublimation()

if __name__ == '__main__':
    cli()