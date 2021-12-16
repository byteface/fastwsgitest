import fastwsgi
from http_router import Router
from domonic import html, head, body, h1

router = Router(trim_last_slash=True)


@router.route('/')
def index():
    return str(html(head(), body(h1("Hello World!!!!"))))


@router.route('/page2')
def page2():
    return str(html(head(), body(h1("Hello World 22222!!!!"))))


class Application:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        try:
            p = router(self.environ.get('PATH_INFO'), method="GET")
            body = str.encode(str(p.target()))
        except Exception as e:
            # print(e)
            body = b'404!\n'

        status = '200 OK'
        headers = [('Content-type', 'text/html')]
        self.start_response(status, headers)
        yield body


if __name__ == '__main__':
    fastwsgi.run(wsgi_app=Application, host='0.0.0.0', port=5000)
