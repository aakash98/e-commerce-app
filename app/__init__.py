from app.instance.config import app, ES_CERT_PATH

if __name__ == '__main__':
    app.run(ssl_context=ES_CERT_PATH, debug=True)


@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'


@app.route('/about/')
def about():
    return '<h3>This is a Flask web application For e-commerce Website.</h3>'
