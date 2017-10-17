import poplib
from email.parser import Parser
from email.header import decode_header
from envelopes import Envelope
import Global


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def Get_info(msg):
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            return Get_info(part)
    if not msg.is_multipart():
        content_type = msg.get_content_type()
        if content_type == 'text/plain':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            return content


def SentEmail(message, subject,imgpath):
    envelope = Envelope(
        from_addr=(Global.useremail, u'Train'),
        to_addr=(Global.toemail, u'FierceX'),
        subject=subject,
        text_body=message
    )
    if imgpath is not None:
        envelope.add_attachment(imgpath)

    envelope.send(Global.smtphost, login=Global.useremail,
                  password=Global.password, tls=True)


def ReEmail():
    try:
        pp = poplib.POP3(Global.pophost)
        pp.user(Global.useremail)
        pp.pass_(Global.password)
        resp, mails, octets = pp.list()
        index = len(mails)
        if index > 0:
            resp, lines, octets = pp.retr(index)
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            pp.dele(index)
            pp.quit()
            msg = Parser().parsestr(msg_content)
            message = Get_info(msg)
            subject = msg.get('Subject')
            date = msg.get('Date')
            return message, subject, date
    except ConnectionResetError as e:
        print('ConnectionResetError')
    return None, None, None
