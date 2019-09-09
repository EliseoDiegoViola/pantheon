var Slack = require('slack-node');
var template = '['+
        '{'+
            '"fallback": "Required plain-text summary of the attachment.",'+
            '"color": "good",'+
            '"author_name": "Bobby Tables",'+
            '"title_link": "https://api.slack.com/",'+
            '"text": "Optional text that appears within the attachment"'+
        '}'+
    ']';


exports.sendMessage = function(req,res){
	var data = req.body;
	var message = "";
	if("msg" in data){
		message = data["msg"];
		this.webhookUri = "https://hooks.slack.com/services/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"
		slack = new Slack();
		slack.setWebhook(this.webhookUri);

		slack.webhook({
		  channel: "#hermes",
		  username: "Hermes",
		  icon_emoji: ":email:",
		  text: message
		}, function(err, response) {
		  global.logger.info(response);
		  res.send(response);
		});
	}else{
		global.logger.error("Cannot parse message body");
		global.logger.debug(data);
		
	}
	
}


exports.reportAction = function(req,res){
	var data = req.body;
	var message = "";
	if("msg" in data){
		var obj = JSON.parse(template);
	
		var colorLevel = "none"
		if(data["level"] == 0){
			colorLevel = "good";
		}else if(data["level"] == 1){
			colorLevel = "warning";
		}else if(data["level"] == 2){
			colorLevel = "danger";
		}
		
		this.webhookUri = "https://hooks.slack.com/services/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"
		slack = new Slack();
		slack.setWebhook(this.webhookUri);

		slack.webhook({
		  channel: "#hermes",
		  username: "Hermes",
		  icon_emoji: ":email:",
		  attachments:[
			  {
			  	"fallback":data["msg"],
			  	"color":colorLevel,
			  	"author_name":data["author"],
			  	"text":data["msg"],
			  	"ts":data["ts"]
			  }
		  ]
		}, function(err, response) {
		  global.logger.info(response);
		  res.send(response);
		});
	}else{
		global.logger.error("Cannot parse message body");
		global.logger.debug(data);
		
	}
	
}

exports.checkHermes = function(req,res){
		res.send("Hermes Is Alive")
}