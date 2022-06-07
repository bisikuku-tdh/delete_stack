import boto3
boto3.set_stream_logger('botocore', level='DEBUG')

######--this code is to get list of cidr for all
######  provisioned vpcs in all regions in a specific account

profiles = ['sandbox1']

def all_account(profiles):
    accounts = []
    for profile in profiles:
        session = boto3.Session(profile_name=profile)
        accounts.append(session.profile_name)
    return accounts
       

accounts = all_account(profiles)

def main():
    for _ in accounts:
        def get_region_names():
            ec2_client = boto3.client('ec2')
            response = ec2_client.describe_regions()
            regions = response['Regions']
            return [region['RegionName'] for region in regions] 

        regions = get_region_names()

        for region in regions:
            client = boto3.client('ec2', region_name=region)
            subnets = client.describe_subnets()['Subnets']
            vpcs = client.describe_vpcs()['Vpcs']
            cidr_sub = []
            cidr_vpc = []
            for subnet in subnets:
                for vpc in vpcs:
                    if subnet['VpcId'] == vpc['VpcId']:
                        cidr_sub.append(subnet['CidrBlock'])
                        cidr_vpc.append(vpc['CidrBlock'])
            print(region, cidr_sub, sep='\n', end='\n\n')

main()
      