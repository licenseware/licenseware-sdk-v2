import os
import random
from jinja2 import Template
from .templates import github_workflows_templates
import importlib.resources as pkg_resources


github_workflows_path = '.github/workflows'



class DevOpsCreator:
    
    def __init__(self, app_id: str):

        self.app_id = app_id
        app_idli = app_id.replace("-", "|").replace("_", "|").split("|")
        self.app_title = "".join([v.capitalize() for v in app_idli]) # odb-service => OdbService
        self.app_name = "-".join([v.lower() for v in app_idli]) # odb-service => odb-service
        self.load_balancer_priority = random.randint(10000, 99999)

    def create_file(self, filename: str, template_filename: str, **template_vars):

        file_path = os.path.join(github_workflows_path, filename)
        if os.path.exists(file_path): return

        raw_contents = pkg_resources.read_text(github_workflows_templates, template_filename)
        file_contents = Template(raw_contents).render(**template_vars)
        with open(file_path, 'w') as f:
            f.write(file_contents)


    def create_lint(self):
        self.create_file(filename='lint.yml', template_filename='lint.yml.jinja')

    def create_release_publish_notif(self):
        self.create_file(filename='release-publish-notif.yml', template_filename='release-publish-notif.yml.jinja')


    def create_deploy_on_test_workflow_file(self):
        
        self.create_file(
            filename="app_name.yml.jinja".replace("app_name", self.app_name), 
            template_filename="app_name.yml.jinja",
            app_title=self.app_title,
            app_name=self.app_name,
            load_balancer_priority=self.load_balancer_priority
        )

    
    def create(self):
        
        if not os.path.exists(github_workflows_path): 
            os.makedirs(github_workflows_path)

        self.create_lint()
        self.create_release_publish_notif()
        self.create_deploy_on_test_workflow_file()
