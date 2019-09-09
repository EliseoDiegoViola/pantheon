var webClient = require('slack-terminalize').getWebClient();
/**
 * Wrapper function for postMessage from slack-client to handle formatting.
 * 
 * @param  { object } slack-client Channel boject
 * @param  { string } message to send to Slack channel
 * @param  { boolean } flag to indicate block formatting
 * @return { none }
 * 
 */

var debugLevel = {};
debugLevel.good = "#6dc066";
debugLevel.warning = "#fbd742";
debugLevel.bad = "#e62d5d";

var messageQueue = [];
var busy = false;

var postMessage = function (channel, response, level) {


    // more on this API here: https://api.slack.com/methods/chat.postMessage
    if(level === null) level = "good";
	attachments = {
			"as_user": true,
		  "attachments": [
		    {
		      "fallback": "Required plain-text summary of the attachment.",
		      "color": ""+debugLevel[level],
		      "text": ""+response
		    }
		  ],
		  "as_user": true
		};
	var message = {};
	message.ch = channel;
	message.att = attachments;
	message.level = level;
	messageQueue.push(message);
	if(messageQueue.length === 1){
		postQueueToSlack();
	}
	

};

var postQueueToSlack = function (){
	if(busy){ 
		console.log("BUSY!");
		return;
	}
	if(messageQueue.length === 0){
		console.log("done");
		return;
	}
	busy = true;
	var message = messageQueue.shift();
	
	webClient.chat.postMessage(message.ch, "", message.att,function(){
		busy = false;
		
		postQueueToSlack();
	});
}

var uploadFile = function (channel, file,filename) {
	opts = {
			"file": file,
		  	"filename" : filename,
		  	"title" : filename,
		  	"channels" : channel
		};
	webClient.files.upload(channel, opts);

};

exports.postMessage = postMessage;
exports.uploadFile = uploadFile;