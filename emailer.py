#!/usr/bin/env python

from ConfigParser import SafeConfigParser, NoSectionError, Error
import argparse
import os
import smtplib
import re
import sys


def main():

    argument_parser = argparse.ArgumentParser(prog='mail')
    argument_parser.add_argument('subject', help='The subject of the email')
    argument_parser.add_argument('to', help='The destination email address')
    args = argument_parser.parse_args()

    if not re.match(r'.*@.*', args.to):
        print args.to, ' is not a vialid email address.'
        sys.exit()

    path = os.path.split(os.path.realpath(__file__))[0]

    config_parser = SafeConfigParser()
    try:
        config_parser.read(os.path.join(path, 'settings.ini'))
    except Error as e:
        print 'Error, settings.ini.', e
        sys.exit()

    try:
        settings = dict(config_parser.items('email'))
    except NoSectionError as e:
        print 'Error settings.ini.', e
        sys.exit()

    try:
        smtp_server = settings['smtp_server']
        smtp_port = settings['smtp_port']
        user = settings['user']
        password = settings['password']
    except KeyError as e:
        print e
        sys.exit()

    if sys.stdin.isatty():
        msg = raw_input('Please enter your message >')
    else:
        msg = '<br>'.join(line for line in sys.stdin)

    headers = ['From: ' + user,
               'Subject: ' + args.subject,
               'To: ' + args.to,
               'MIME-Version: 1.0',
               'Content-Type: text/html']
    headers = '\r\n'.join(headers)

    session = smtplib.SMTP(smtp_server, smtp_port)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(user, password)

    try:
        session.sendmail(user, args.to, headers + '\r\n\r\n' + msg)
    except smtplib.SMTPException as e:
        print 'Error.'
        for key in e.args[0].keys():
            print key
            for msg in e.args[0][key]:
                print msg

    session.quit()

if __name__ == '__main__':
    main()
