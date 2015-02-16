#!/usr/bin/env python

math_ops = {'multiply': lambda x, y: x * y,
            'divide': lambda x, y: x / y,
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
           }


def usage():
    """ Explain the usage of calculator.py """

    usage_page = """<html>
    <head>
    <title>WSGI Calculator</title>
    </head>
    <body>

    The WSGI calculator supports the following operations:<br>
    Addition<br>
    Subtraction<br>
    Multiplication<br>
    Division<br>
    <br>
    Examples:<br>
    http://localhost:8080/multiply/3/5  => 15<br>
    http://localhost:8080/add/23/42     => 65<br>
    http://localhost:8080/divide/6/0    => HTTP "400 Bad Request"<br>

    </body>
    </html>"""

    return usage_page


def resolve_path(path):
    """ Resolve the path into an operator and its operands """

    parts = path.strip('/').split('/')
    if len(parts) != 3:
        raise NameError

    return parts[0], [int(i) for i in parts[1:]]


def math_func(operator, operands):
    """ Perform math operation specified by 'operator' on 'operands' """
    
    answer_page = """<html>
    <head>
    <title>WSGI Calculator</title>
    </head>
    <body>

    Answer: {}

    </body>
    </html>"""

    answer = math_ops[operator](operands[0], operands[1])
    return answer_page.format(answer)

    
def application(environ, start_response):
    """ A WSGI application for doing basic math via the url """

    import pprint
    pprint.pprint(environ)

    headers = [("Content-type", "text/html")]

    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError

        operator, operands = resolve_path(path)
        body = math_func(operator, operands)
        status = "200 OK"

    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
        body += usage()

    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        body += usage()

    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)

        return [body]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
