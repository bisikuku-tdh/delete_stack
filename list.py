import boto3
import functools
import re

###### Info about code ##########
# List stacks
# Basic assumption here is that you have permissions to access the AWS resources.
# You can use the AWS CLI to check the permissions.
# You can use the AWS CloudFormation console to check the stack status.
# boto3 is used to access the AWS resources and needs to be installed.
# Please be free to use it in your own projects and feel free to modify it, improve it and share it. 
#################################

# Get the list of activated or already 'opt in' regions.
def get_region_names():
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_regions()
    regions = response['Regions']
    return [region['RegionName'] for region in regions] 

regions = get_region_names()

# Get the list of stacks in all regions and their corresponding stacts and delete them.
for region in regions:
    client = boto3.client('cloudformation', region_name=region)
    paginator = client.get_paginator('list_stacks')
    status_filter = ['CREATE_COMPLETE', 'UPDATE_COMPLETE', 'ROLLBACK_COMPLETE', 'CREATE_IN_PROGRESS', 'UPDATE_IN_PROGRESS', 'ROLLBACK_IN_PROGRESS']

    response_iterator = paginator.paginate(
    StackStatusFilter=status_filter
    )
    stacks = []
    for response in response_iterator:
        stacks += [stack['StackName'] for stack in response['StackSummaries']]
    # adding this to get the stacks that have the string 'pattern' in them, this is a hacky way to get the stacks that we want to delete
    def get_stacksList():
        return [st for st in stacks if any(sub in st for sub in ['StackSet-AWSControlTower', 'StackSet-Densify', 'StackSet-Infose'])]
    stacks = (get_stacksList())
    print("Region/Stacks " + region, stacks)
