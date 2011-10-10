import imaplib
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('login@gmail.com', 'pss')
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox") # connect to inbox.

result, data = mail.search(None, "ALL")

ids = data[0] # data is a list.
id_list = ids.split() # ids is a space separated string
latest_email_id = id_list[-1] # get the latest

result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID

raw_email = data[0][1] # here's the body, which is raw text of the whole email
# including headers and alternate payloads

result, data = mail.uid('search', None, "ALL") # search and return uids instead
#result, data = mail.uid('search', None, "UnSeen") # search and return uids instead
latest_email_uid = data[0].split()[-1]
result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
raw_email = data[0][1]

import email
email_message = email.message_from_string(raw_email)

print email_message['To']

parsed = email.utils.parseaddr(email_message['From'])

from email import header as h

a = h.decode_header(parsed[0])
print a[0][0].decode('koi8-r')


print email_message['Subject']
print email_message['From']
# note that if you want to get text content (body) and the email contains
# multiple payloads (plaintext/ html), you must parse each message separately.
# use something like the following: (taken from a stackoverflow post)
def get_first_text_block(self, email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()
