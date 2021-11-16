import boto3
from botocore.exceptions import ClientError
import argparse
import sys

client = boto3.client('lambda')

parser = argparse.ArgumentParser()

parser.add_argument ("--account", type=str, required=True)
parser.add_argument ("--file", type=str, required=True)
parser.add_argument ("--type", type=str, required=True)

args = parser.parse_args()


def main(account_id,file,iamobjtype):
    try:
        count = 0
        with open(file) as fp:
            for line in fp:
                count += 1
                iamobj = line.strip()
                verify_iam_principal(account_id,iamobj,iamobjtype)
        print("All done!")
    except OSError:
        print ("Could not open/read file: " + file)
        sys.exit() 

def verify_iam_principal(account_id,iamobj,iamobjtype):
    try:
        if (iamobjtype=='user'):
            principal = 'arn:aws:iam::'+account_id+':user/'+iamobj
        elif (iamobjtype=='role'):
            principal = 'arn:aws:iam::'+account_id+':role/'+iamobj
        else:
            return ("Invalid IAM object type passed")
        response = client.add_permission(
            Action='lambda:ListTags',
            FunctionName='EnumLambda',
            Principal=principal,
            StatementId='enum'
        )
        if ("Statement" in response):
            cleanup()
            print("Found IAM principal: " + iamobj)
            return()
        else:
            return()
    except client.exceptions.InvalidParameterValueException as e:
        return()

def cleanup():
    try:
        response = client.remove_permission(
            FunctionName='EnumLambda',
            StatementId='enum'
        )
    except client.exceptions.ResourceNotFoundException as e:
        return()

if __name__=="__main__":
    main(args.account, args.file, args.type)
