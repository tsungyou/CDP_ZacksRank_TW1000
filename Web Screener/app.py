from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/snapshot')
def snapshot():
    return {
        "code": "success",
        "sucess": True,
        "message": "localhost:5000",
        "status": "200"
    }


print("a")
app.run(debug=True)
print("b")
