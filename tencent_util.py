import argparse
import base64
import json
import os
import time

import pandas as pd
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import \
    TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.iai.v20180301 import iai_client, models

from tencent_secret import CLIENT_ID, CLIENT_KEY


def create_group():
    try:
        cred = credential.Credential(CLIENT_ID, CLIENT_KEY)
        client = iai_client.IaiClient(cred, "ap-beijing")

        req = models.CreateGroupRequest()

        request_body = {"GroupName": "wyy_19", "GroupId": "wyy_19"}

        req.from_json_string(json.dumps(request_body))
        resp = client.CreateGroup(req)

        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)


def add_person(name, studentID, picture_path):
    try:
        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法(默认为HmacSHA256)

        cred = credential.Credential(CLIENT_ID, CLIENT_KEY)
        client = iai_client.IaiClient(cred, "ap-beijing", clientProfile)

    except TencentCloudSDKException:
        raise TencentCloudSDKException

    try:

        req = models.CreatePersonRequest()

        with open(picture_path, "rb") as FILE:
            request_body = {
                "GroupId": 'wyy_19',
                "PersonName": name,
                "PersonId": str(studentID),
                "Image": base64.encodestring(FILE.read()).decode('utf-8')
            }

        req.from_json_string(json.dumps(request_body))
        resp = client.CreatePerson(req)

        print(resp.to_json_string())
    except TencentCloudSDKException as err:
        print(studentID)
        print(err)


def add_persen_op(args):
    add_person(args.name, args.studentID, args.path)


def get_person_list(group_id):
    try:
        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法(默认为HmacSHA256)

        cred = credential.Credential(CLIENT_ID, CLIENT_KEY)
        client = iai_client.IaiClient(cred, "ap-beijing", clientProfile)

        req = models.GetPersonListRequest()
        request_body = {"GroupId": group_id, "Limit": 1000}
        req.from_json_string(json.dumps(request_body))
        resp = client.GetPersonList(req)

        return json.loads(resp.to_json_string())

    except TencentCloudSDKException as err:
        raise TencentCloudSDKException


def load_person_batch(image_dir, namelist_path):
    added_person_list = get_person_list('wyy_19')
    print(added_person_list)

    added_student_ID_list = [
        student['PersonId'] for student in added_person_list["PersonInfos"]
    ]

    print(added_student_ID_list)
    # print(added_student_ID_list)
    image_list = os.listdir(image_dir)
    namelist = pd.read_excel(namelist_path)
    for index, person in namelist.iterrows():
        if str(person['学号']) in added_student_ID_list:
            print(f"{person['姓名']} {person['学号']} has been added, skip")
            continue
        time.sleep(1)
        try:
            image_path = filter(
                lambda file_name: file_name.startswith(str(person["学号"])),
                image_list).__next__()
            image_path = os.path.join(image_dir, image_path)
            add_person(person["姓名"], person["学号"], image_path)
        except StopIteration:
            print(f'no picture corresponding to {person["学号"]}')


def load_person_batch_op(args):
    load_person_batch(args.image_dir, args.namelist_path)


def search_person(picture):
    try:
        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法(默认为HmacSHA256)

        cred = credential.Credential(CLIENT_ID, CLIENT_KEY)
        client = iai_client.IaiClient(cred, "ap-beijing", clientProfile)

        req = models.SearchFacesRequest()
        request_body = {
            "GroupIds": ['wyy_19'],
            "Image": picture,
            "MaxFaceNum": 1,
            "MaxPersonNum": 1,
            "NeedPersonInfo": 1
        }
        req.from_json_string(json.dumps(request_body))
        resp = client.SearchFaces(req)

        return json.loads(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Command Line Tool to manage person library')
    subparsers = parser.add_subparsers(help='command to execute')

    add_person_parser = subparsers.add_parser("add_person")

    add_person_parser.add_argument("--name",
                                   required=True,
                                   help='name of the student added')
    add_person_parser.add_argument("--studentID",
                                   required=True,
                                   help='student ID of the student added')
    add_person_parser.add_argument("--path",
                                   required=True,
                                   help='path to picture of the student added')
    add_person_parser.set_defaults(func=add_persen_op)

    load_person_parser = subparsers.add_parser("load_person")
    load_person_parser.add_argument("--image_dir", required=True)
    load_person_parser.add_argument("--namelist_path", required=True)
    load_person_parser.set_defaults(func=load_person_batch_op)

    args = parser.parse_args()
    args.func(args)

# python .\tencent_util.py load_person --image_dir img --namelist_path namelist.xlsx
