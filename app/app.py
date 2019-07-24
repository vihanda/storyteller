from flask import Flask, request, jsonify
from video import VideoCreator

app = Flask(__name__)

@app.route('/')
def init():
  return 'Welcome to Storyteller service'

@app.route('/video', methods=['POST'])
def generateVideo():
    print(request.is_json)
    content = request.get_json()
    print(content)
    #VideoCreator.make_video(r"C:\Users\vihanda\dev\storyteller\images")
    return 'JSON posted'


if __name__ == '__main__':
  app.run(debug=True, port=12345)