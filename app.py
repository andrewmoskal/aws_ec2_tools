import boto3
import os
import httpx

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


class AwsEc2:

    def __init__(self):
        self.__client = self.get_client(_type='ssm')

    def get_client(self, _region='eu-north-1', _type='ec2') -> boto3.client:

        return boto3.client(
            _type,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=_region
        )

    def get_region_name(self, _region):
        __client = self.get_client('eu-north-1', 'ssm')
        __name = f'/aws/service/global-infrastructure/regions/{_region}/longName'
        __response = self.__client.get_parameter(Name=__name)
        return __response.get('Parameter').get('Value')

    def get_regions(self) -> dict:
        __client = self.get_client()
        __response = __client.describe_regions()
        __regions = {}
        [__regions.update({x.get('RegionName'): self.get_region_name(x.get('RegionName'))}) for x in __response.get('Regions')]
        return __regions


if __name__ == '__main__':

    aws_ec2 = AwsEc2()

    _regions_map = aws_ec2.get_regions()

    for region in _regions_map.keys():

        client = aws_ec2.get_client(region)

        _response = client.describe_addresses()
        _addresses = _response.get('Addresses', [])

        if not _addresses:
            continue
        for _address in _addresses:
            _public_ip = _address.get('PublicIp')
            _instance_id = _address.get('InstanceId')
            _private_ip = _address.get('PrivateIpAddress')
            _net_group = _address.get('NetworkBorderGroup')
            print(_instance_id, _public_ip, _private_ip, _net_group, _regions_map.get(_net_group))
        print('--------------------------------------')
