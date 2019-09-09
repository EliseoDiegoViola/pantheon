var fs = require('fs');

exports.changeVersion = function(req,res){
	var versionTxt = req.params.version;
	var versionParts = versionTxt.split(".");
	if(updateVersionFile(versionParts)){
		res.send("New Version "+versionTxt+" saved");
	}else{
		res.send("Update failed: version format must be in the form 'x.x.x' and x must be a number ");
	}
	
	
}

exports.getNewVersion = function(req,res){
	var versionData = fs.readFileSync('versionFile.json');
	var versionParsed = JSON.parse(versionData);
	var versionParts = versionParsed["version"].split(".");
	versionParts[2] = (parseInt(versionParts[2])+1).toString();
	if(updateVersionFile(versionParts)){
		res.send(versionParsed)
	}else{
		res.send("Get failed");
	}
	

	
}

exports.peekVersion = function(req,res){
	var versionData = fs.readFileSync('versionFile.json');
	var versionParsed = JSON.parse(versionData);
	res.send(versionParsed)
}

function updateVersionFile(versionsArray){
	if(versionsArray.length !== 3){
		global.logger.info("Error, version format must be in the form 'x.x.x'");
		return false;
	}

	var major = versionsArray[0];

	if (major != parseInt(major)){
	    global.logger.info("Error, major version must be an int");
		return false;
	}


	var minor = versionsArray[1];
	if (minor != parseInt(minor)){
		global.logger.info("Error, minor version must be an int");
		return false;
	}

	var patch = versionsArray[2];
	if (patch != parseInt(patch)){
		global.logger.info("Error, patch version must ve an int");
		return false;
	}

	var version = {};
	version["version"] = major+"."+minor+"."+patch;
	var data = JSON.stringify(version,null,2)
	fs.writeFile('versionFile.json',data,function(err) {
	  global.logger.info(err);
	});
	return true
}


