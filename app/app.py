from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def init():
  return 'Welcome to Storyteller service'

@app.route('/video', methods=['POST'])
def generateVideo():
    json_ = request.json
    print(json_)
    return json_

def parseInput(text):
  #pass


if __name__ == '__main__':
  app.run(debug=True, port=12345)