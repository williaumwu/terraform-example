def run(stackargs):

    import json

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="vpc_name")
    stack.parse.add_required(key="gcloud_project")

    # this will set the GOOGLE_APPLICATION_CREDENTIALS environment variable relative to the shared docker volume
    stack.parse.add_required(key="google_application_credentials",default="/var/tmp/share/.creds/gcloud.json")

    # docker image to execute terraform with
    stack.parse.add_optional(key="docker_exec_env",default="elasticdev/terraform-run-env")

    # initialize variables
    stack.init_variables()

    # declare execution groups
    stack.add_execgroup("elasticdev:::gcloud::base williaumwu:::terraform-example::vpc","vpc")

    # initialize exegroups for introspection and dependencies
    stack.init_execgroups()

    # CREATE EMPTY VPC
    vpc_state_id = stack.random_id(size=8)

    env_vars = {"NAME":stack.vpc_name}
    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["GCLOUD_PROJECT"] = stack.gcloud_project
    env_vars["GOOGLE_APPLICATION_CREDENTIALS"] = stack.google_application_credentials
    env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env
    env_vars["USE_DOCKER"] = True
    env_vars["METHOD"] = "create"

    env_vars["TERRAFORM_RESOURCE_TYPE"] = "google_compute_network"
    env_vars["RESOURCE_TYPE"] = "vpc"
    env_vars["RESOURCE_TAGS"] = [ "vpc", stack.vpc_name ]
    #env_vars["RESOURCE_PARENT"] = True

    # determine what env vars to pass to 
    # the docker execution container
    docker_env_fields_keys = env_vars.keys()
    docker_env_fields_keys.remove("METHOD")
    env_vars["DOCKER_ENV_FIELDS"] = ",".join(docker_env_fields_keys)
    env_vars["OS_TEMPLATE_VARS"] = "GCLOUD_PROJECT,VPC_NAME" 
    env_vars["DESTROY_EXECGROUP"] = "elasticdev:::gcloud::base {}".format(stack.credential_group)
    env_vars["DESTROY_ENV_VARS"] = json.dumps({"GOOGLE_APPLICATION_CREDENTIALS":stack.google_application_credentials})

    inputargs = {"name":stack.vpc_name}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["stateful_id"] = vpc_state_id
    stack.vpc.insert(**inputargs)

    return stack.get_results()
