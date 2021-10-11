import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, make_response
from clients.github import github_client
from config.env import SENTRY_DSN

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.8
)

app = Flask(__name__)


@app.route('/merger/ht', methods=['GET'])
def healthcheck():
  resp = make_response('OK', 200)
  return resp

@app.route('/merger/debug-sentry')
def trigger_error():
  return 1 / 0

@app.route('/merger/lookup', methods=['POST'])
def pr_lookup():
  try:
    github_client.merge_prs()
    resp = make_response('OK', 200)
    return resp
  except Exception as error:
    resp = make_response('INTERNAL SERVER ERROR', 500)
    return resp
