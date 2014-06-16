import argparse

from api import create_app

app = create_app()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0', help='host to bind to [%(default)s]')
    parser.add_argument('--port', type=int, default=app.config['SERVER_PORT'], help='port to listen [%(default)s]')
    parser.add_argument('--nodebug', action='store_true', default=False, help='no debug mode? [%(default)s]')
    args = parser.parse_args()
    app.run(debug=not args.nodebug, host=args.host, port=args.port)
