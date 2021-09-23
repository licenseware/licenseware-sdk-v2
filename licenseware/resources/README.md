# Quickstart 

Here are the steps needed for local development of an app:

- Install the sdk : `pip3 install git+https://git@github.com/licenseware/licenseware-sdk-python3.git`;
- Clone the repo for your service;
- CD in the cloned repo locally;
- Create a new app : `licenseware new-app odb`;
- Create a new uploader: `licenseware new-uploader lms_options`;
- Update modules `validator.py` `worker.py` as per processing requirements needs for `lms_options` uploader_id. Modules created will be found here: `app/uploaders/lms_options`
- Open the first terminal start the mock-server : `licenseware start-mock-server`;
- Open the second terminal start the redis background worker: `licenseware start-background-worker`;
- Open the third terminal start the development server: `licenseware start-dev-server`;
- Copy `docker-compose.yml` file to `Documents` folder start the databases with:

```
docker-compose up
```

You will have mongoexpress running at: `http://localhost:8081/`


See more licenseware docs [here](https://licenseware.github.io/licenseware-sdk-python3/)