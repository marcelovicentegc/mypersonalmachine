from flask import Flask, make_response
from clients.github import github_client

app = Flask(__name__)


@app.route('/merger/ht', methods=['GET'])
def healthcheck():
  resp = make_response('OK', 200)
  return resp

@app.route('/merger/lookup', methods=['POST'])
def pr_lookup():
  try:
    github_client.merge_prs()
    resp = make_response('OK', 200)
    return resp
  except Exception as error:
    resp = make_response('INTERNAL SERVER ERROR', 500)
    return resp
  