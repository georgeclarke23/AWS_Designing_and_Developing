import boto3
from pprint import pprint



class EC2Insance:

    def __init__(self):
        self.client = boto3.client('ec2')

    def create_security_group(self, group_name, description, vpc_id=""):
        """Creates a new security group

        Arguments:
            group_name: (string) --[REQUIRED]
                        The name of the security group.

            description: (string) --[REQUIRED]
                         A description for the security group

            vpc_id: (string) --[OPTIONAL]
                    The ID of the VPC
        Returns:
            security-group-ID: (dict)
                                {
                                    'GroupId': 'string'
                                }
        """
        return self.client.create_security_group(Description=description,
                                                 GroupName=group_name,
                                                 VpcId=vpc_id)

    def add_security_group_rules(self, group_id, ip_permissions):
        return self.client.authorize_security_group_ingress(GroupId=group_id,
                                                            IpPermissions=ip_permissions)

    def create_key_pair(self, name):
        return self.client.create_key_pair(
            KeyName=name,
        )

    def create_instance(self, ami, key_pair):
        return self.client.create_instances(ImageId=ami,
                                            MinCount=1,
                                            MaxCount=1,
                                            InstanceType='t2.micro',
                                            KeyName=key_pair)

    def get_security_group(self):
        return self.client.describe_security_groups()

    def get_instances(self):
        self.client.describe_instances()


def main():

    params = [{'IpProtocol': 'tcp',
               'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'Everyone'}],
               'FromPort': 80,
               'ToPort': 80},
              {'IpProtocol': 'tcp',
               'IpRanges': [{'CidrIp': '79.69.235.218/32', 'Description': 'My_House'}],
               'FromPort': 22,
               'ToPort': 22}]

    try:
        ec2 = EC2Insance()

        sg = ec2.create_security_group('george', 'example')
        pprint(sg)

        sg_rules = ec2.add_security_group_rules(sg['GroupId'], params)
        pprint(sg_rules)

        key_pair = ec2.create_key_pair('Admin_access')
        pprint(key_pair)

        ec2_instance = ec2.run_instance('ami-0ce71448843cb18a1', key_pair)
        pprint(ec2_instance)
    except Exception as error:
        pprint(error)


if __name__ == "__main__":
    main()




