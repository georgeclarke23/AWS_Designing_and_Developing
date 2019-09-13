from __future__ import print_function, unicode_literals


from pprint import pprint
from PyInquirer import (Token, prompt, style_from_dict)
from pyfiglet import figlet_format
from ec2.ec2_instance import EC2Insance
import boto3
import six

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})


def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(string, font=font), color))
    else:
        six.print_(string)


def number_of_instances_(instances):
    number_of_instances = 0
    if instances:
        for reservation in instances["Reservations"]:
            for instance in reservation["Instances"]:
                number_of_instances += 1
    return str(number_of_instances)


def dashboard_option():
    questions = [{'type': 'list',
                  'name': 'dashboard',
                  'message': 'Dashboard:',
                  'choices': ['ec2', 'Security groups', 'Key Pair'],
                  'filter': lambda val: val.lower()
                  }]

    return prompt(questions)


def main():

    ec2 = EC2Insance()
    instances = ec2.get_instances()
    security_groups = ec2.get_security_group()
    my_session = boto3.session.Session()
    my_region = my_session.region_name
    profile_name = my_session.profile_name

    pprint(instances)
    log('EC2 Instances', color="blue", figlet=True)
    log("Welcome to EC2 Instances", "green")
    print("Profile Name: {}".format(colored(profile_name, "blue")))
    print("Region: {}".format(colored(my_region, "blue")))
    print("Instances: {}".format(colored(number_of_instances_(instances), "blue")))
    #pprint(security_groups)

    dashboard = dashboard_option()


if __name__ == "__main__":
    main()