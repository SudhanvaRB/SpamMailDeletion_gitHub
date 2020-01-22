import json
from imapclient import IMAPClient
import email
import os
import boto3
from base64 import b64decode
from Mailer_List import MailList

password = os.environ['psswd']
DECRYPTED = boto3.client('kms').decrypt(CiphertextBlob=b64decode(password))['Plaintext'].decode('utf-8')


def delete_mail(event, context):
    # TODO implement
    email_id = os.environ['Email_ID']
    mail_list = MailList()
    mail_list = mail_list.spam_mail_list
    obj = IMAPClient('imap.gmail.com', ssl=True)
    obj.login(email_id, DECRYPTED)
    select_info = obj.select_folder('Inbox')
    mails_before_deletion = select_info[b'EXISTS']
    print('%d mails in INBOX before deletion' % mails_before_deletion)
    for i in mail_list:
        msg_ids = obj.search(['FROM', i])
        if (len(msg_ids)) != 0:
            print('%d mails deleted from %s' % (len(msg_ids), i))
        obj.delete_messages(msg_ids)
    select_info1 = obj.select_folder('Inbox')
    mails_after_deletion = select_info1[b'EXISTS']
    print('%d mails in INBOX after deletion' % mails_after_deletion)
    print('Total number of mails deleted : %d' % (mails_before_deletion - mails_after_deletion))
    obj.expunge()
    obj.logout()
    return {
        'statusCode': 200,
        'body': msg_ids
    }