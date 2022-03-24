import os
import random
from types import ModuleType
from jinja2 import Template
from .templates import github_workflows_templates
from .templates import aws_cloud_formation_templates
import importlib.resources as pkg_resources


github_workflows_path = '.github/workflows'
aws_cloudformation_path = './cloudformation-templates'


class DevOpsCreator:
    
    def __init__(self, app_id: str):

        self.app_id = app_id
        app_idli = app_id.replace("-", "|").replace("_", "|").split("|")
        self.app_title = "".join([v.capitalize() for v in app_idli]) # odb-service => OdbService
        self.app_name = "-".join([v.lower() for v in app_idli]) # odb-service => odb-service


    def get_load_balancer_priority(self):
        return random.randint(10000, 99999)

    def create_file(self, filename: str, template_path: str, template_resource: ModuleType, template_filename: str = None, **template_vars):

        file_path = os.path.join(template_path, filename)
        if os.path.exists(file_path): return

        raw_contents = pkg_resources.read_text(template_resource, template_filename or filename + '.jinja')
        file_contents = Template(raw_contents, trim_blocks=True, lstrip_blocks=True).render(**template_vars)
        with open(file_path, 'w') as f:
            f.write(file_contents)


    def create_lint(self):
        self.create_file(
            filename='lint.yml', 
            template_path=github_workflows_path,
            template_resource=github_workflows_templates
        )

    def create_release_publish_notif(self):
        self.create_file(
            filename='release-publish-notif.yml', 
            template_path=github_workflows_path,
            template_resource=github_workflows_templates
        )


    def create_deploy_on_dev_workflow_file(self):
        
        self.create_file(
            filename="app_name.yml".replace("app_name", self.app_name), 
            template_filename="app_name.yml.jinja",
            template_path=github_workflows_path,
            template_resource=github_workflows_templates,
            app_title=self.app_title,
            app_name=self.app_name,
            load_balancer_priority=self.get_load_balancer_priority()
        )


    def create_deploy_on_prod_workflow_file(self):
        
        self.create_file(
            filename="app_name_prod.yml".replace("app_name", self.app_name), 
            template_filename="app_name_prod.yml.jinja",
            template_path=github_workflows_path,
            template_resource=github_workflows_templates,
            app_title=self.app_title,
            app_name=self.app_name,
            load_balancer_priority=self.get_load_balancer_priority()
        )


    def create_deploy_on_dev_cloudformation_file(self):

        self.create_file(
            filename="app_name_prod.yml".replace("app_name", self.app_name), 
            template_filename="app_name_prod.yml.jinja",
            template_path=github_workflows_path,
            template_resource=github_workflows_templates,
            app_title=self.app_title,
            app_name=self.app_name,
            load_balancer_priority=self.get_load_balancer_priority()
        )
    


    def create(self):
        
        if not os.path.exists(github_workflows_path): 
            os.makedirs(github_workflows_path)

        self.create_lint()
        self.create_release_publish_notif()

        self.create_deploy_on_dev_workflow_file()
        self.create_deploy_on_prod_workflow_file()
        
        self.create_deploy_on_dev_cloudformation_file()

