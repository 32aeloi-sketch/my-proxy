from flask import Flask, request, Response
import requests

app = Flask(__name__)
TARGET = "https://lite.duckduckgo.com"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    url = f"{TARGET}{path}"
    
    # We tell DuckDuckGo: "Do not send me zipped/compressed data"
    headers = {k: v for k, v in request.headers if k.lower() not in ['host', 'accept-encoding']}
    headers['Accept-Encoding'] = 'identity'

    resp = requests.request(
        method=request.method,
        url=url,
        params=request.args,
        data=request.form,
        headers=headers,
        allow_redirects=True
    )

    # Use 'content' to keep images and icons working
    return Response(resp.content, status=resp.status_code, content_type=resp.headers.get('Content-Type'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
