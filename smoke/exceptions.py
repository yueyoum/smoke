# -*- coding: utf-8 -*-


import sys
import traceback

class ExceptionMiddleware(object):
    def __init__(self, wrap_app, smoke_html=False):
        self.wrap_app = wrap_app
        self.smoke_html = smoke_html

    def __call__(self, environ, start_response):
        try:
            return self.wrap_app(environ, start_response)
        except:
            tb_exc = traceback.format_exc()
            exc_info = sys.exc_info()
            self.handle_exception(tb_exc, exc_info)
            if not self.smoke_html:
                raise

            status = '500 Internal Server Error'
            start_response(
                status,
                [('Content-Type', 'text/html')],
                exc_info
            )
            tb_exc = tb_exc.replace('\n', '<br/>').replace(' ', '&nbsp;')
            html = """<html>
            <head><title>%s</title></head>
            <body>
                <h1>%s</h1>
                <p>%s</p>
            </body>
            </html>
            """ % (status, status, tb_exc)
            return [html]

    def handle_exception(self, tb_exc, exc_info):
        raise NotImplementedError



class EmailExceptionMiddleware(ExceptionMiddleware):
    """This is an Example, In production, It's better not send emails in sync mode.
    Because sending emails maybe slow, this will block your web app.
    So, the best practices is write your own EmailExceptionMiddleware,
    In this class, It's handle_exception method not send mail directly,
    You shoul use MQ, or something else.
    """
    def __init__(self,
                 wrap_app,
                 smoke_html=False,
                 from_address=None,
                 to_address=None,
                 smtp_server=None,
                 smtp_port=25,
                 smtp_username=None,
                 smtp_password=None,
                 mail_subject_prefix=None,
                 mail_template=None):
        assert isinstance(to_address, (list, tuple)) and smtp_server is not None, "Email Config Error"
        self.from_address = from_address
        self.to_address = to_address
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.mail_subject_prefix = mail_subject_prefix
        self.mail_template = mail_template

        super(EmailExceptionMiddleware, self).__init__(wrap_app, smoke_html=smoke_html)


    def handle_exception(self, tb_exc, exc_info):
        from smoke.functional import send_mail
        send_mail(
            self.smtp_server,
            self.smtp_port,
            self.smtp_username,
            self.smtp_password,
            self.from_address,
            self.to_address,
            '{0} Error Occurred'.format(self.mail_subject_prefix if self.mail_subject_prefix else ''),
            tb_exc,
            'html'
        )

