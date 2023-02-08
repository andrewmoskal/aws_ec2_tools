import boto3
import os

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


def get_client(_region, _type='ec2') -> boto3.client:
    return boto3.client(
        _type,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=_region
    )


def get_region_name(_region):
    __client = get_client('eu-north-1', 'ssm')
    __name = f'/aws/service/global-infrastructure/regions/{_region}/longName'
    __response = __client.get_parameter(Name=__name)
    return __response.get('Parameter').get('Value')


def get_regions() -> dict:
    __client = get_client('eu-north-1')
    __response = __client.describe_regions()
    __regions = {}
    [__regions.update({x.get('RegionName'): get_region_name(x.get('RegionName'))}) for x in __response.get('Regions')]
    return __regions


if __name__ == '__main__':

    _regions_map = get_regions()

    for region in _regions_map.keys():

        client = get_client(region)

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
