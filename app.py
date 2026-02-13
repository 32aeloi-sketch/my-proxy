from flask import Flask, request, Response
import requests

app = Flask(__name__)

# The destination for the proxy
TARGET_URL = "https://lite.duckduckgo.com"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    url = f"{TARGET_URL}{path}"
    
    # We tell DuckDuckGo we don't want compressed data (Gzip)
    headers = {key: value for (key, value) in request.headers if key != 'Host'}
    headers['Accept-Encoding'] = 'identity' 

    resp = requests.request(
        method=request.method,
        url=url,
        params=request.args,
        data=request.form,
        headers=headers,
        allow_redirects=True
    )

    # Send the clean text back to your browser
    return Response(resp.content, status=resp.status_code, content_type=resp.headers.get('Content-Type'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
