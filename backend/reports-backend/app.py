import json

from flask import Flask, request, jsonify, render_template, send_from_directory
import os

import src.report as report_repo

app = Flask(__name__, static_folder="templates/assets")


@app.route('/api/reports', methods=['GET'])
def list_reports():
    return jsonify(report_repo.list())

@app.route('/videos', methods=['GET'])
def show_videos():
    video_files = os.listdir('videos')
    return render_template('videos.html', video_files=video_files, mimetype='video/mp4')

@app.route('/result', methods=['GET'])
def show_results():
    image_files = os.listdir('result')
    return render_template('results.html', image_files=image_files)

@app.route('/videos/<filename>')
def get_video(filename):
    return send_from_directory('videos', filename)


@app.route('/api/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No video part", 400
    file = request.files['video']
    if file.filename == '':
        return "No selected video", 400
    if file:
        filename = file.filename
        file.save(os.path.join('videos', filename))
        return "Video uploaded successfully", 200
    
@app.route('/api/start_post_process', methods=['POST'])
def start_post_process():
    data = request.json
    video = data.get('video')
    if not video:
        return jsonify({"error": "No video provided"}), 400
    # Assuming there's a function in report_repo to handle post processing
    # result = report_repo.start_post_process(video)
    print('Post processing video:', video)
    return jsonify({"success": True, "video": video}), 200

@app.route('/api/reports', methods=['POST'])
def add_report():
    report = request.json
    report_repo.add(json.dumps(report))
    return "OK"


@app.route("/reports", methods=['GET'])
def show_reports():
    reports = report_repo.list()
    return render_template('reports.html', reports=reports)


@app.route("/reports/<int:report_id>", methods=['GET'])
def show_report(report_id: int):
    report = report_repo.get(report_id)
    return render_template('report.html', report=report)


if __name__ == '__main__':
    report_repo.init_table()
    app.run(debug=True, host='', port=3002)
