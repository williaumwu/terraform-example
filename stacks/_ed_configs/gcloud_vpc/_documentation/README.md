**Description**

  - This stack creates a VPC on gcp

**Required**

| argument      | description                            | var type | default      |
| ------------- | -------------------------------------- | -------- | ------------ |
| vpc_name   | name of the vpc                 | string   | None         |
| gcloud_project      | the project id in gclouod from      | string   | None         |
| google_application_credentials      | the location for the json file gcp      | string     | /tmp/.credentials.json         |

**Optional**

| *argument*           | *description*                            | *var type* |  *default*      |
| ------------- | -------------------------------------- | -------- | ------------ |
| routing_mode      | routing mode for vpc    | string   | global         |
| docker_exec_env      | docker container to execute terraform templates    | string   | elasticdev/terraform-run-env         |

**Sample entry:**
```
infrastructure:
  vpc:
    stack_name: williaumwu:::gcloud_vpc
    arguments:
      vpc_name: project1
      gcloud_project: project1-288907
