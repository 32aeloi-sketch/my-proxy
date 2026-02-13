from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Target for the proxy
TARGET = "https://lite.duckduckgo.com"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    url = f"{TARGET}{path}"
    
    # Copy headers but skip 'Host' to avoid security errors
    headers = {key: value for (key, value) in request.headers if key != 'Host'}

    # Fetch the page from DuckDuckGo
    resp = requests.request(
        method=request.method,
        url=url,
        params=request.args,
        data=request.form,
        headers=headers,
        allow_redirects=True
    )

    # CRITICAL FIX: Use .text instead of .content. 
    # This forces the 'requests' library to unzip the data for us automatically.
    return Response(resp.text, status=resp.status_code, content_type=resp.headers.get('Content-Type'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
