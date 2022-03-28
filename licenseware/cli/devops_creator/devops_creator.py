import os
import random
from licenseware.cli.base_creator import BaseCreator

from .templates import github_workflows_templates
from .templates import aws_cloud_formation_templates
from .templates import deploy_templates
from .templates import root_templates


paths = dict(
    github_workflows = '.github/workflows',
    aws_cloudformation = './cloudformation-templates',
    deploy_folder = './deploy',
    deploy_jupyter_folder = './deploy/jupyter',
    root = "./"
)


class DevOpsCreator(BaseCreator):
    
    def __init__(self, app_id: str):
        super().__init__(app_id)

    def get_random_int(self):
        return random.randint(10000, 99999)

    def create_lint(self):
        self.create_file(
            filename='lint.yml', 
            filepath=paths['github_workflows'],
            template_resource=github_workflows_templates
        )

    def create_release_publish_notif(self):
        self.create_file(
            filename='release-publish-notif.yml', 
            filepath=paths['github_workflows'],
            template_resource=github_workflows_templates
        )

    def create_deploy_on_dev_workflow_file(self):
        
        self.create_file(
            filename="app-dash.yml".replace("app-dash", self.app_dash), 
            filepath=paths['github_workflows'],
            template_filename="app-dash.yml.jinja",
            template_resource=github_workflows_templates,
            load_balancer_priority=self.get_random_int()
        )


    def create_deploy_on_prod_workflow_file(self):
        
        self.create_file(
            filename="app-dash-prod.yml".replace("app-dash", self.app_dash), 
            filepath=paths['github_workflows'],
            template_filename="app-dash-prod.yml.jinja",
            template_resource=github_workflows_templates,
            load_balancer_priority=self.get_random_int()
        )


    def create_deploy_on_dev_cloudformation_file(self):

        self.create_file(
            filename="app-dash-api.yml".replace("app-dash", self.app_dash), 
            filepath=paths['aws_cloudformation'],
            template_filename="app-dash-api.yml.jinja",
            template_resource=aws_cloud_formation_templates
        )


    def create_deploy_on_prod_cloudformation_file(self):

        self.create_file(
            filename="app-dash-api-prod.yml".replace("app-dash", self.app_dash), 
            filepath=paths['aws_cloudformation'],
            template_filename="app-dash-api-prod.yml.jinja",
            template_resource=aws_cloud_formation_templates
        )


    def create_deploy_envs_files(self):

        self.create_file(
            filename=".env.app_title".replace("app_title", self.app_title), 
            filepath=paths['deploy_folder'],
            template_filename="env.app_title.jinja",
            template_resource=deploy_templates,
            redis_db = self.get_random_int()
        )

        self.create_file(
            filename=".env.debug",
            filepath=paths['deploy_folder'],
            template_filename="env.app_title.jinja",
            template_resource=deploy_templates,
            redis_db = self.get_random_int()
        )


    def create_deploy_jupyter_files(self):

        self.create_file(
            filename="docker-compose.yml", 
            filepath=paths['deploy_jupyter_folder'],
            template_resource=deploy_templates,
            redis_db = self.get_random_int()
        )

        self.create_file(
            filename="requirements.txt",
            filepath=paths['deploy_jupyter_folder'],
            template_resource=deploy_templates,
            redis_db = self.get_random_int()
        )

    def create_devops_root_files(self):

        for file in ['docker-compose.yml', 'docker-entrypoint.sh', "Dockerfile", 
        "Dockerfile.stack", "makefile", "pre-commit-config.yaml", 
        "Procfile", "Procfile.stack"]:
            self.create_file(
                filename=file,
                filepath=paths['root'],
                template_resource=root_templates
            )

        self.create_file(
            filename=".dockerignore",
            filepath=paths['root'],
            template_filename="dockerignore.jinja",
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

