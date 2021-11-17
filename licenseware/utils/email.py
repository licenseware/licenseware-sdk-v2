import os, sys
import sendgrid
from sendgrid.helpers.mail import Mail
from jinja2 import Template

from .logger import log


def _load_template(html_template:str, html_template_vars:dict):
    
    resources_path = os.path.join(sys.path[0], f"app/resources/{html_template}")

    if not os.path.exists(resources_path):
        raise Exception("Email template not found in resources folder")
        
    with open(resources_path) as f:
        tmp = Template(f.read())
        
    if html_template_vars:
        html_content = tmp.render(**html_template_vars)
    else:
        html_content = tmp.render()
        
    return html_content
        
    


def send_email(
    to:str, 
    subject:str, 
    template:str, 
    **template_vars
):
    """
        to: email or list of emails of emails where the email needs to be sent
        subject: email subject
        template: the html template filename from app/resources ex: "software_request.html"
        template_vars: kwargs with template variables to be filled by Jinja2 
        ex: name='dan' will fill in the html template where `{{ name }}` is found 
        
        
        Usage:
        
        ```py
        
        send_email(
            to=some_email@gmail.com, 
            subject='SSC Catalog invite',
            template="email_template.html", 
            message="You've been invited as an admin to SCC Catalog."
        )
        
        ```
        
        The html template will be found in resources and it will contain jinja2 `{{ message }}` placeholder   
            
    """
    
    if os.getenv('ENVIRONMENT') in {'dev', 'local'}: return True
    
    try:
        
        html_content = _load_template(template, template_vars)
            
        mail_client = sendgrid.SendGridAPIClient(api_key=os.environ['SENDGRID_API_KEY'])
        mail = Mail(
            from_email=os.environ['SENDGRID_EMAIL_SENDER'],
            subject=subject,
            to_emails=to,
            html_content=html_content
        )

        response = mail_client.send(mail)
        log.info(response)

        return True

    except Exception as err:
        log.exception(err)
        return False
