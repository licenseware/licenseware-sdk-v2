import os
import random
from types import ModuleType
from jinja2 import Template
from .templates import github_workflows_templates
from .templates import aws_cloud_formation_templates
from .templates import deploy_templates
from .templates import root_templates
import importlib.resources as pkg_resources


paths = dict(
    github_workflows = '.github/workflows',
    aws_cloudformation = './cloudformation-templates',
    deploy_folder = './deploy',
    deploy_jupyter_folder = './deploy/jupyter',
    root = "./"
)



class DevOpsCreator:
    
    def __init__(self, app_id: str):
        app_idli = app_id.replace("-", "|").replace("_", "|").split("|")
        self.app_title = "".join([v.capitalize() for v in app_idli]) # odb-service => OdbService
        self.app_dash = "-".join([v.lower() for v in app_idli]) # odb-service => odb-service
        self.app_dash_upper = "-".join([v.upper() for v in app_idli]) # odb-service => ODB-SERVICE
        self.app_underscore = "_".join([v.lower() for v in app_idli]) # odb-service => odb_service
        self.app_underscore_upper = "_".join([v.upper() for v in app_idli]) # odb-service => ODB_SERVICE

    def get_random_int(self):
        return random.randint(10000, 99999)

    def create_file(self, filename: str, template_path: str, template_resource: ModuleType, template_filename: str = None, **template_vars):

        file_path = os.path.join(template_path, filename)
        if os.path.exists(file_path): return

        raw_contents = pkg_resources.read_text(template_resource, template_filename or filename + '.jinja')
        file_contents = Template(raw_contents).render(
            **{
                'app_title': self.app_title, 
                'app_dash': self.app_dash,
                'app_dash_upper': self.app_dash_upper,
                'app_underscore': self.app_underscore,
                'app_underscore_upper': self.app_underscore_upper
            }, **template_vars
        )

        with open(file_path, 'w') as f:
            f.write(file_contents)


    def create_lint(self):
        self.create_file(
            filename='lint.yml', 
            template_path=paths['github_workflows'],
            template_resource=github_workflows_templates
        )

    def create_release_publish_notif(self):
        self.create_file(
            filename='release-publish-notif.yml', 
            template_path=paths['github_workflows'],
            template_resource=github_workflows_templates
        )


    def create_deploy_on_dev_workflow_file(self):
        
        self.create_file(
            filename="app-dash.yml".replace("app-dash", self.app_dash), 
            template_filename="app-dash.yml.jinja",
            template_path=paths['github_workflows'],
            template_resource=github_workflows_templates,
            load_balancer_priority=self.get_random_int()
        )


    def create_deploy_on_prod_workflow_file(self):
        
        self.create_file(
            filename="app-dash-prod.yml".replace("app-dash", self.app_dash), 
            template_filename="app-dash-prod.yml.jinja",
            template_path=paths['github_workflows'],
            template_resource=github_workflows_templates,
            load_balancer_priority=self.get_random_int()
        )


    def create_deploy_on_dev_cloudformation_file(self):

        self.create_file(
            filename="app-dash-api.yml".replace("app-dash", self.app_dash), 
            template_filename="app-dash-api.yml.jinja",
            template_path=paths['aws_cloudformation'],
            template_resource=aws_cloud_formation_templates
        )


    def create_deploy_on_prod_cloudformation_file(self):

        self.create_file(
            filename="app-dash-api-prod.yml".replace("app-dash", self.app_dash), 
            template_filename="app-dash-api-prod.yml.jinja",
            template_path=paths['aws_cloudformation'],
            template_resource=aws_cloud_formation_templates
        )


    def create_deploy_envs_files(self):

        self.create_file(
            filename=".env.app_title".replace("app_title", self.app_title), 
            template_filename="env.app_title.jinja",
            template_path=paths['deploy_folder'],
            template_resource=deploy_templates,
            redis_db = self.get_random_int()
        )

        self.create_file(
            filename=".env.debug",
            template_filename="env.app_title.jinja",
            template_path=paths['deploy_folder'],
            template_resource=deploy_templates,
            redis_db = self.get_random_int()
        )


    def create_deploy_jupyter_files(self):

        self.create_file(
            filename="docker-compose.yml", 
            template_path=paths['deploy_jupyter_folder'],
            template_resource=deploy_templates,
            redis_db = self.get_random_int()
        )

        self.create_file(
            filename="requirements.txt",
            template_path=paths['deploy_jupyter_folder'],
            template_resource=deploy_templates,
            redis_db = self.get_random_int()
        )

    def create_devops_root_files(self):

        for file in ['docker-compose.yml', 'docker-entrypoint.sh', "Dockerfile", 
        "Dockerfile.stack", "makefile", "pre-commit-config.yaml", 
        "Procfile", "Procfile.stack"]:
            self.create_file(
                filename=file,
                template_path=paths['root'],
                template_resource=root_templates
            )

        self.create_file(
            filename=".dockerignore",
            template_filename="dockerignore.jinja",
            template_path=paths['root'],
            template_resource=root_templates
        )


    def create(self):

        for _, path in paths.items():
            if not os.path.exists(path): os.makedirs(path)

        self.create_lint()
        self.create_release_publish_notif()

        self.create_deploy_on_dev_workflow_file()
        self.create_deploy_on_prod_workflow_file()
        
        self.create_deploy_on_dev_cloudformation_file()
        self.create_deploy_on_prod_cloudformation_file()

        self.create_deploy_envs_files()
        self.create_deploy_jupyter_files()

        self.create_devops_root_files()

