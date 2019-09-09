var natural = require('natural')
var classifier = new natural.BayesClassifier();
const exec = require('child_process').exec;
var slackTerminal 	= require('slack-terminalize'),
	commands 		= slackTerminal.getCommands(),
	util			= require('../util');
var nounInflector = new natural.NounInflector();
var ini = require('node-ini');
var fs = require('fs');



var ateneaScript = "..\\Atenea\\Atenea.py"
var iniFile = "..\\builder.ini"
var cfg = ini.parseSync(iniFile);

var _zipAll = function (channel) {
	var atenea = exec("python " + ateneaScript + " -z");
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

var _zipSpecific = function (channel,commands) {
	if(commands.length == 1){
		var com = commands[0];
		com = nounInflector.pluralize(com);

		if(com.toLowerCase() === "all"){
			return _zipAll(channel);
		}else{
			var atenea = exec("python " + ateneaScript + " -i " + com + " -z");
			atenea.stdout.on('data', function (data) {
				util.postMessage(channel, 'n: ' + data,"good");
			});

			atenea.stderr.on('data', function (data) {
				util.postMessage(channel, '*ERROR*: ' + data,"bad");
			});

			atenea.on('exit', function (code) {
				util.uploadFile(channel,'..\\'+cfg.Paths.ZipFilePath,"lastBuild.zip");
				util.postMessage(channel, 'I finished my job, code : ' + code,"good");

			});
		}
	}else if(commands.length == 2){
		commands[0] = nounInflector.pluralize(commands[0]);
		var atenea = exec("python " + ateneaScript + " -i " + commands[0] + " " +commands[1] + " -z");
			atenea.stdout.on('data', function (data) {
				util.postMessage(channel, 'n: ' + data,"good");
			});

			atenea.stderr.on('data', function (data) {
				util.postMessage(channel, '*ERROR*: ' + data,"bad");
			});

			atenea.on('exit', function (code) {

				util.uploadFile(channel,'..\\'+cfg.Paths.ZipFilePath,"lastBuild.zip");
				util.postMessage(channel, 'I finished my job, code : ' + code,"good");
			});
	}else{
		util.postMessage(channel,"Sorry Master I couldn't understand what you said, ask for *help* to learn more about me.","warning")
	
	}
};

module.exports = function (param) {
	var	channel		= param.channel;
	_zipSpecific(channel,param.args);

	
};