# -*- coding: utf-8 -*-
# tencentcloud-sdk-python

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tsf.v20180326 import tsf_client, models

import sys
import json

# 密钥参数，替换为用户的secret_id和secret_key
secret_id = "#"
secret_key = "#"

region = "ap-guangzhou"

endpoint = "tsf.tencentcloudapi.com"

client = None


def init_client():
    try:
        cred = credential.Credential(secret_id, secret_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = endpoint
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, region, clientProfile)
        return client
    except TencentCloudSDKException as err:
        print("client init error :" + err)
        assert TencentCloudSDKException


def describe_container_group_detail(group_id):
    req = models.DescribeContainerGroupDetailRequest()
    params = '{"GroupId":"' + group_id + '"}'
    req.from_json_string(params)

    resp = client.DescribeContainerGroupDetail(req)
    print(resp.to_json_string())
    return resp


def deploy_container_group(container_group_detail_resp, tag_name):
    params = dict(GroupId=container_group_detail_resp.Result.GroupId,
                  Server=container_group_detail_resp.Result.Server,
                  Reponame=container_group_detail_resp.Result.Reponame,
                  TagName=tag_name,
                  InstanceNum=container_group_detail_resp.Result.InstanceNum,
                  CpuRequest=container_group_detail_resp.Result.CpuRequest,
                  MemRequest=container_group_detail_resp.Result.MemRequest)
    """
    params = '{"GroupId":"group-zvw397wa",
            "Server":"ccr.ccs.tencentyun.com",
            "Reponame":"tsf_100011913960/zsf-tsf-docker",
            "TagName":"docker-consumer",
            "InstanceNum":1,
            "CpuRequest":"0.25",
            "MemRequest":"128"}'
    """
    req = models.DeployContainerGroupRequest()
    req.from_json_string(json.dumps(params))
    resp = client.DeployContainerGroup(req)
    print(resp.to_json_string())


if __name__ == '__main__':

    # 部署组ID
    group_id = sys.argv[1]
    # 镜像版本名称,如v1
    tag_name = sys.argv[2]

    client = init_client()
    container_group_detail_resp = describe_container_group_detail(group_id)
    deploy_container_group(container_group_detail_resp, tag_name)
