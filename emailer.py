#!/usr/bin/env python

import smtplib
import sys
from ConfigParser import SafeConfigParser, NoSectionError, Error

def main():

    parser = SafeConfigParser()
    try:
        parser.read('settings.ini')
    except Error as e:
        print 'Error, settings.ini.', e
        sys.exit()

    try:
        settings = dict(parser.items('email'))
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


    try:
        subject = sys.argv[1]
    except IndexError:
        print 'Please provide a subject'
        sys.exit()

    try:
        to = (sys.argv[2]).split(',')
    except IndexError:
        print 'Please provide a destination e-mail address'
        sys.exit()

    if sys.stdin.isatty():
        msg = raw_input('Please enter your message >')
    else:
        msg = '<br>'.join(line for line in sys.stdin)

    headers = ['From: ' + user,
               'Subject: ' + subject,
               'To: ' + str(to),
               'MIME-Version: 1.0',
               'Content-Type: text/html']
    headers = '\r\n'.join(headers)

    session = smtplib.SMTP(smtp_server, smtp_port)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(user, password)

    try:
        session.sendmail(user, to, headers + '\r\n\r\n' + msg)
    except smtplib.SMTPException as e:
        print 'Error.'
        for key in e.args[0].keys():
            print key
            for msg in e.args[0][key]:
                print msg


    session.quit()

if __name__ == '__main__':
    main()
