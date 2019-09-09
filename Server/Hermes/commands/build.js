var natural = require('natural')
var classifier = new natural.BayesClassifier();
const exec = require('child_process').exec;
var slackTerminal 	= require('slack-terminalize'),
	commands 		= slackTerminal.getCommands(),
	util			= require('../util');
var nounInflector = new natural.NounInflector();


var ateneaScript = "..\\Atenea\\Atenea.py"


var _buildAll = function (channel) {
	var atenea = exec("python " + ateneaScript);
	atenea.stdout.on('data', function (data) {
		util.postMessage(channel, 'n: ' + data,"good");
	});

	atenea.stderr.on('data', function (data) {
		util.postMessage(channel, '*ERROR*: ' + data,"bad");
	});

	atenea.on('exit', function (code) {
		util.postMessage(channel, 'I finished my job, code : ' + code,"good");
	});
};

var _buildSpecific = function (channel,commands) {
	if(commands.length == 1){
		var com = commands[0];
		com = nounInflector.pluralize(com);

		if(com.toLowerCase() === "all"){
			return _buildAll(channel);
		}else{
			util.postMessage(channel, "Buiding... please wait...","good");
			var atenea = exec("python " + ateneaScript + " -i " + com);
			atenea.stdout.on('data', function (data) {
				util.postMessage(channel, 'n: ' + data,"good");
			});

			atenea.stderr.on('data', function (data) {
				util.postMessage(channel, '*ERROR*: ' + data,"bad");
			});

			atenea.on('exit', function (code) {
				util.postMessage(channel, 'I finished my job, code : ' + code,"good");
			});
		}
	}else if(commands.length == 2){
		commands[0] = nounInflector.pluralize(commands[0]);
		util.postMessage(channel, "Buiding... please wait...","good");

		var atenea = exec("python " + ateneaScript + " -i " + commands[0] + " " +commands[1]);
			atenea.stdout.on('data', function (data) {
				util.postMessage(channel, 'n: ' + data,"good");
			});

			atenea.stderr.on('data', function (data) {
				util.postMessage(channel, '*ERROR*: ' + data,"bad");
			});

			atenea.on('exit', function (code) {
				util.postMessage(channel, 'I finished my job, code : ' + code,"good");
			});
	}else{
		var stepSpecify = commands.indexOf("step");
		if(stepSpecify > -1){
			commands[0] = nounInflector.pluralize(commands[0]);
			var stepNumber = commands[stepSpecify+1];
			var commVals = []
			for (i = 0; i < commands.length; i++) {
				if(i === stepSpecify || i === stepSpecify+1){
					continue;
				}else{
					commVals.push(commands[i]);
				}
		   	 	
			}
			util.postMessage(channel, "Buiding... please wait...","good");

			var atenea = exec("python " + ateneaScript + " -i " + commands[0] + " "+ commands[1] +" -s "+ stepNumber);
			atenea.stdout.on('data', function (data) {
				util.postMessage(channel, 'n: ' + data,"good");
			});

			atenea.stderr.on('data', function (data) {
				util.postMessage(channel, '*ERROR*: ' + data,"bad");
			});

			atenea.on('exit', function (code) {
				util.postMessage(channel, 'I finished my job, code : ' + code,"good");
			});

		}else{
			util.postMessage(channel,"Sorry Master I couldn't understand what you said, ask for *help* to learn more about me.","warning")
		}
	}
};

module.exports = function (param) {
	var	channel		= param.channel;
	_buildSpecific(channel,param.args);

	
};