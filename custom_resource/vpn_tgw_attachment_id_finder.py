"""
Find TGW attachment ID for VPN and tag it
"""
import boto3

import cfnresponse


def lambda_handler(event, context):
    """
    Lambda handler
    """
    print(event)
    response_data = {}
    response_status = cfnresponse.SUCCESS
    try:
        if event["RequestType"] in ("Create", "Update"):
            vpn_id = event["ResourceProperties"]["vpn_id"]
            attachment_name = event["ResourceProperties"]["attachment_name"]

            ec2 = boto3.client("ec2")
            response = ec2.describe_transit_gateway_attachments(
                Filters=[
                    {"Name": "resource-id", "Values": [vpn_id]},
                ],
            )
            attachment_id = response["TransitGatewayAttachments"][0][
                "TransitGatewayAttachmentId"
            ]
            tags = [{"Key": "Name", "Value": f"TGW-{attachment_name}"}]
            ec2.create_tags(Resources=[attachment_id], Tags=tags)
            response_data["TransitGatewayAttachmentId"] = attachment_id
    except Exception as err:
        response_data["error"] = str(err)
        response_status = cfnresponse.FAILED

    print(f"response status: {response_status}, response data: {response_data}")
    cfnresponse.send(event, context, response_status, response_data)
