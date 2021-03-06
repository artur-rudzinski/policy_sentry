#!/usr/bin/env python
from policy_sentry.shared.database import connect_db
from policy_sentry.writing.template import get_crud_template_dict, get_actions_template_dict
from policy_sentry.command.write_policy import write_policy_with_access_levels, write_policy_with_actions
import json


if __name__ == '__main__':
    db_session = connect_db('bundled')
    crud_template = get_crud_template_dict()
    wildcard_actions_to_add = ["kms:createcustomkeystore", "cloudhsm:describeclusters"]

    crud_template['policy_with_crud_levels'][0]['name'] = "MyPolicy"
    crud_template['policy_with_crud_levels'][0]['description'] = "Description"
    crud_template['policy_with_crud_levels'][0]['role_arn'] = "somearn"
    crud_template['policy_with_crud_levels'][0]['read'].append(
        "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret")
    crud_template['policy_with_crud_levels'][0]['write'].append(
        "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret")
    crud_template['policy_with_crud_levels'][0]['list'].append("arn:aws:s3:::example-org-sbx-vmimport/stuff")
    crud_template['policy_with_crud_levels'][0]['permissions-management'].append(
        "arn:aws:kms:us-east-1:123456789012:key/123456")
    crud_template['policy_with_crud_levels'][0]['wildcard'].extend(wildcard_actions_to_add)
    crud_template['policy_with_crud_levels'][0]['tagging'].append("arn:aws:ssm:us-east-1:123456789012:parameter/test")

    policy = write_policy_with_access_levels(db_session, crud_template, None)
    print(json.dumps(policy, indent=4))

"""
Output:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "MultMultNone",
            "Effect": "Allow",
            "Action": [
                "kms:createcustomkeystore"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "SecretsmanagerReadSecret",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:describesecret",
                "secretsmanager:getresourcepolicy",
                "secretsmanager:getsecretvalue",
                "secretsmanager:listsecretversionids"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
            ]
        },
        {
            "Sid": "SecretsmanagerWriteSecret",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:cancelrotatesecret",
                "secretsmanager:deletesecret",
                "secretsmanager:putsecretvalue",
                "secretsmanager:restoresecret",
                "secretsmanager:rotatesecret",
                "secretsmanager:updatesecret",
                "secretsmanager:updatesecretversionstage"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
            ]
        },
        {
            "Sid": "KmsPermissionsmanagementKmskey",
            "Effect": "Allow",
            "Action": [
                "kms:creategrant",
                "kms:putkeypolicy",
                "kms:retiregrant",
                "kms:revokegrant"
            ],
            "Resource": [
                "arn:aws:kms:us-east-1:123456789012:key/123456"
            ]
        }
    ]
}
"""
