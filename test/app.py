class App(object):
    def __init__(self, hook_func=None):
        self.hook_func = hook_func

    def __call__(self, environ, start_response):
        html = """<html>
        <body><table>{0}</table></body>
        </html>"""

        def _get_env(k, v):
            return """<tr><td>{0}</td><td>{1}</td></tr>""".format(k, v)

        env_table = ''.join( [_get_env(k, v) for k, v in sorted(environ.items())] )
        html = html.format(env_table)

        status = '200 OK'
        headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(html)))
        ]

        start_response(status, headers)
        if self.hook_func:
            self.hook_func()
        return [html]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = App()
    server = make_server('127.0.0.1', 8000, app)
    server.handle_request()
