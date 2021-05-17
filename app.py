from flask import Flask, jsonify, abort, make_response
from config import DIR
from business_logic import *

app = Flask(__name__)


@app.route("/api/folder", methods=["GET"])
def get_folder_info():
    folder = group_folder_info(DIR)
    return json.dumps({"folder": folder}, ensure_ascii=False)


@app.route("/api/file/<string:file_name>", methods=["GET"])
def get_file_info(file_name):
    all_files = get_names_of_files(DIR)["names_of_files"]
    if file_name not in all_files:
        abort(404)
    path_to_file = get_path_for_filename(file_name)
    file = group_file_info(path_to_file)
    return json.dumps({"file": file}, ensure_ascii=False)


@app.route("/api/word/<string:word>", methods=["GET"])
def get_word_info(word):
    all_words = get_list_of_all_words(DIR)
    if word not in all_words:
        abort(404)
    word_info = group_word_info(word)
    return jsonify({"word": word_info})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error 404": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7070)
