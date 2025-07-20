from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/extract', methods=['GET'])
def extract():
    url = request.args.get('url')
    if not url:
        return jsonify({"error":"No URL provided"}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # pick the first video/audio format URL
    formats = info.get('formats') or []
    best = formats[-1] if formats else info
    return jsonify({
        'title': info.get('title'),
        'media_url': best.get('url'),
        'ext': best.get('ext')
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
