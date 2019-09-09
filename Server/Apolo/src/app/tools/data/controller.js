const fs = require('fs');
const path = require('path');

exports.list = ( req, res ) => {
	try{
		var jsonPath = path.join(__dirname, 'json', req.params["jsonName"]+'.json');
		var jsonString = fs.readFileSync(jsonPath, 'utf8');
		var jsonData = JSON.parse(jsonString);
		res.send( jsonData );	
	}catch (e){
		res.status(400).send({"error":"invalid json"}); 
	}

};
