from flask import Flask, request

app = Flask(__name__, static_url_path='/static')

#### Backend
@app.route('/test')
def test():
    path = request.args.get('path')
    #checker = checkers.GDALChecker(path)
    return path

#### Frontend
@app.route('/')
def root():
    return app.send_static_file('index.html')

if __name__ == '__main__':

    app.run(port=5000)
    #app.run(host="0.0.0.0", port=5000)
