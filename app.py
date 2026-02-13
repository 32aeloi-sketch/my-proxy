from flask import Flask, request, Response
import requests

app = Flask(__name__)

# The destination for the proxy
TARGET = "https://lite.duckduckgo.com"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    # FIX: This ensures there is always a "/" between the host and the path
    url = f"{TARGET.rstrip('/')}/{path.lstrip('/')}"
    
    # We tell DuckDuckGo we don't want compressed data to avoid weird symbols
    headers = {k: v for k, v in request.headers if k.lower() not in ['host', 'accept-encoding']}
    headers['Accept-Encoding'] = 'identity' 
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

    try:
        resp = requests.request(
            method=request.method,
            url=url,
            params=request.args,
            data=request.form,
            headers=headers,
            allow_redirects=True
        )

        # Send the clean content back to your browser
        return Response(resp.content, status=resp.status_code, content_type=resp.headers.get('Content-Type'))
    
    except Exception as e:
        return f"Proxy Error: {str(e)}", 500

if __name__ == '__main__':
    # Run the server on Port 5000
    app.run(host='0.0.0.0', port=5000)
