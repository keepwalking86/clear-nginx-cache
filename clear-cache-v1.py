from flask import Flask, render_template, request
import hashlib
import shutil
import os

app = Flask(__name__)

# Define cache path and key
proxy_cache_path = "/path/to/cache"
proxy_cache_key = "http.example.com"

# Define usage function
def usage():
    return "Usage *url* as example: /audio/audio.mp3"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clear-cache', methods=['GET'])
#def clear_cache():
#    url = request.form.get('url')
#    if not url:
#        return usage()
def clear_cache():
    url = request.args.get('url')
    if not url:
        return usage()
    # Calculate cache path
    cache_path = hashlib.md5((proxy_cache_key + url).encode()).hexdigest()
    print(cache_path)
    cache_path = "{}/{}/{}/{}".format(proxy_cache_path, cache_path[-1], cache_path[-3:-1], cache_path)
    print(cache_path)

    # Check if cache path exists
    if not os.path.exists(cache_path):
        return "Cache not found for URL: {}".format(url)

    # Check if cache path is a file
    if not os.path.isfile(cache_path):
        return "Cache path is not a file: {}".format(url)

    # Remove cache file
    try:
        os.remove(cache_path)
    except Exception as e:
        return "Failed to clear cache for URL: {}. Error: {}".format(url, str(e))

    # Check if cache file still exists
    if os.path.exists(cache_path):
        return "Failed to clear cache for URL: {}".format(url)

    return "Cache cleared for URL: {}".format(url)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
