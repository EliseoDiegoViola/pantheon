import json
import os

from app import app 
from flask import url_for,abort,request

from slackclient import SlackClient

#DATAS
@app.route('/tools/data/<filename>')
def showTool(filename):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'jsons/{0}.json'.format(filename))
    if os.path.isfile(file_path):
        with open(file_path, 'r') as fi:
            json_response = json.load(fi)
            return str(json_response)
    else:
        abort(404)



#SLACK
slack_message_template = [{
    "fallback" : "Required plain-text summary of the attachment.",
    "color": "good",
    "author_name": "Eliseo Viola",
    "title_link": "https://api.slack.com/",
    "text": "Optional text that appears within the attachment"
}]


@app.route('/tools/hermes/message', methods=['POST'])
def sendMessage():
    data = request.form
    message = ""
    if "msg" in data:
        slack_token = os.environ["SLACK_API_TOKEN"]
        message = data["msg"]
        sc = SlackClient(slack_token)
        this.webhookUri = "https://hooks.slack.com/services/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"
        slack = new Slack();
        slack.setWebhook(this.webhookUri);

        sc.api_call(
          "chat.postMessage",
          channel="#hermes",
          text=message,
          user="Hermes",
          icon_emoji=":email:"
        )
    else:
        abort(200)
        
    







