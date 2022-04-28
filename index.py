import boto3
import botocore

ec2_resource = boto3.resource('ec2',region_name='us-east-1')

def list_instance():
    instance_id_list = []
    for instance in ec2_resource.instances.all():
        instance_id_list.append(instance)
    
    return instance_id_list

def prepare_tags_for_iterface(instance_tags):
    interface_tags = []

    if instance_tags != None:
        for each_tag in instance_tags:
            temp_each_tags = {}
            if each_tag['Key'].lower() == "name":
                temp_each_tags['Key'] = each_tag['Key']
                temp_each_tags['Value'] = each_tag['Value'] + "-interface"
                interface_tags.append(temp_each_tags)
            else:
                temp_each_tags['Key'] = each_tag['Key']
                temp_each_tags['Value'] = each_tag['Value']
                interface_tags.append(temp_each_tags)

    return interface_tags

def attach_tags_to_interface(instance,interface_tags):
    for each_interface in instance.network_interfaces:

        if each_interface.tag_set == None:
            print("here")
            response = each_interface.create_tags(
                DryRun=True,
                Tags=interface_tags
            )
            print(response)

def ec2_tags_to_interface(instance_list):
    for instance in instance_list:
        interface_tags = prepare_tags_for_iterface(instance.tags)
        if len(interface_tags) > 0:
            attach_tags_to_interface(instance,interface_tags)
        else:
            print("{instance_id} has to no tags to attach to network interface".format(instance_id = instance.id))

def main():
    instance_list = list_instance()
    ec2_tags_to_interface(instance_list)

if __name__ == "__main__":
    main()