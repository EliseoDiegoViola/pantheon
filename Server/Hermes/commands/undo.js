var natural = require('natural')
var classifier = new natural.BayesClassifier();
const exec = require('child_process').exec;
var slackTerminal 	= require('slack-terminalize'),
	commands 		= slackTerminal.getCommands(),
	util			= require('../util');
var nounInflector = new natural.NounInflector();
var ini = require('node-ini');
var fs = require('fs');



var iniFile = "..\\builder.ini"
var cfg = ini.parseSync(iniFile);
var paths = {};
paths["ArtMasters"] = cfg.Paths.ArtistsPlaticPath;
paths["ElementSpace"] = cfg.Paths.ArtistsPlaticPath;

var _undoSpecific = function (channel,commands) {
	if(commands.length == 1){
		var com = commands[0];
		console.log(paths['ArtMasters']);

		var atenea = exec("cm undochange " + paths[com] + " -R");
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
};

module.exports = function (param) {
	var	channel		= param.channel;
	_undoSpecific(channel,param.args);
};