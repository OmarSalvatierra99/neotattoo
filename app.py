#!/usr/bin/env python3
"""
neotatto - Flask Application
Created: 2026-01-27
"""

import os
from urllib.parse import quote_plus

from flask import Flask, render_template, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'


@app.route('/')
def index():
    maps_key = os.environ.get('GOOGLE_MAPS_EMBED_KEY', '').strip()
    maps_query = os.environ.get(
        'NEOTATTO_MAPS_QUERY',
        '90400 Blvd. Francisco I. Madero 304, Centro, 90300, 90400 Cdad. de Apizaco, Tlax.',
    )
    maps_lat = os.environ.get('NEOTATTO_MAPS_LAT', '').strip()
    maps_lng = os.environ.get('NEOTATTO_MAPS_LNG', '').strip()
    if maps_lat and maps_lng:
        maps_query = f"{maps_lat},{maps_lng}"
    maps_query_encoded = quote_plus(maps_query)
    if maps_key:
        maps_embed_url = (
            "https://www.google.com/maps/embed/v1/place"
            f"?key={maps_key}&q={maps_query_encoded}"
        )
    else:
        maps_embed_url = (
            "https://www.google.com/maps"
            f"?q={maps_query_encoded}&output=embed"
        )

    return render_template('index.html', maps_embed_url=maps_embed_url)


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'service': 'neotatto'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5016))
    app.run(host='0.0.0.0', port=port, debug=True)
