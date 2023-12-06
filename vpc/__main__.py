"""An AWS Python Pulumi program"""
import pulumi
# import pulumi_aws as aws
import pulumi_awsx as awsx


config = pulumi.Config()
vpc_base_name = config.get("vpc_base_name", "dev-vpc")


vpc = awsx.ec2.Vpc(vpc_base_name,
        number_of_availability_zones=2, #NOTE Reduce to save on cost; Min: 2
        cidr_block="172.16.0.0/20", #NOTE Set custom CIDR block; Default: 10.0.0.0/16
        # subnet_specs=[ #NOTE Enable to override defaults; Default: 1 public + 1 private subnet per availability zone
        #     awsx.ec2.SubnetSpecArgs(
        #         type=awsx.ec2.SubnetType.PRIVATE,
        #         cidr_mask=20,
        #         name="your_private_subnet_name_01"
        #     ),
        #     awsx.ec2.SubnetSpecArgs(
        #         type=awsx.ec2.SubnetType.PUBLIC,
        #         cidr_mask=22,
        #         name="your_public_subnet_name_01"
        #     )
        # ],
        nat_gateways=awsx.ec2.NatGatewayConfigurationArgs(strategy=awsx.ec2.NatGatewayStrategy.NONE) #NOTE Set to NONE to save on cost
    )

vpc_name = vpc.vpc.tags.apply(lambda tags: f"{tags['Name']}") #NOTE Example of the convertion of the resource output into string


pulumi.export("vpcName", vpc_name)
pulumi.export("vpcId", vpc.vpc_id)
pulumi.export("publicSubnetIds", vpc.public_subnet_ids)
pulumi.export("privateSubnetIds", vpc.private_subnet_ids)
