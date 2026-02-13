from flask import Flask, request, Response
import requests

app = Flask(__name__)

# This tells the proxy where to go
TARGET = "https://lite.duckduckgo.com"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    # Forwards your search query to DuckDuckGo
    url = f"{TARGET}{path}"
    resp = requests.request(
        method=request.method,
        url=url,
        params=request.args,
        data=request.form,
        headers={key: value for (key, value) in request.headers if key != 'Host'}
    )
    
    # Sends the search results back to your screen
    return Response(resp.content, status=resp.status_code, content_type=resp.headers['content-type'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
