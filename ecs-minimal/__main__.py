import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx


config = pulumi.Config()
environment             = config.require("environment")
cluster_base_name       = config.require("cluster_base_name")
td_name                 = config.get("task_definition_name", f"{environment}-td-default")
td_log_group_name       = f"/ecs/task-definition/{td_name}"
image                   = config.require("image")
container_port          = config.get_int("containerPort", 8080)
host_port               = config.get_int("host_port", 80)
cpu                     = config.get_int("cpu", 512)
memory                  = config.get_int("memory", 128)


td_log_group = aws.cloudwatch.LogGroup(td_log_group_name, retention_in_days=1)
td_log_group_id = td_log_group.id.apply(lambda id: id)


pulumi.export("task_definition_log_group", td_log_group_id)

#CONTINUE: Add references to the VPC project