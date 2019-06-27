#
from flask import Flask, render_template, jsonify, request, make_response

import json,os

from ACevaluator import ACevaluator
# from UniqueTester import UniqueTester
# from InspTester2 import InspTester

# inspTester = InspTester()
# uniqueTester = UniqueTester()
ac = ACevaluator()

app = Flask(__name__)


def evaluate_insp(text):
	return inspTester.is_inspiring(text)

def evaluate_uniqueness(new,previous):
	return uniqueTester.is_unique(new,previous)


@app.route("/get", methods=["GET"])
def get_bot_response():
	poem = request.args.get('poem')
	return jsonify(ac.evaluate(poem))


@app.route('/', methods=['GET', 'POST'])
def main():
	resp = make_response(render_template("game.html"))
	return resp


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
