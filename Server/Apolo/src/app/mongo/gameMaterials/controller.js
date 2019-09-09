const utilities = require( "../../../utilities" );
const repository = require( "./repository" );

exports.create = ( req, res ) => {
	try{
        let matName = req.body.name;
        if(!utilities.validateMaterialName(matName)){
            global.logger.info("BAD NAME...");           
            res.status(400).send({"error":"Invalid Material Name : " + matName }); 
        }else{
            global.logger.info("GOOD NAME...");
            repository.saveGameMat( req.body ).then( savedMat => res.send( utilities.extractObject(savedMat,[ "user", "name", "shaderName","id","properties" ,"thumbnail"] ) ) );
        }
	}catch(e){
		res.status(400).send({"error":"invalid json body for game material creation"}); 
	}

};

// exports.update = ( req, res ) => {
//     res.send( );
// };

exports.delete = ( req, res ) => {
    repository.deleteGameMat(req.params["id"])
        .then(returnCode => res.send(returnCode))
        .catch(err => res.send(err));

};

exports.list = ( req, res ) => {
	global.logger.info("Loading game materials...");
    repository.findGameMats()
        .then( gameMats => res.send( gameMats ))
        .catch( err => res.send( err ) );
};

exports.detail = ( req, res ) => {	
    repository.findDetails(req.params.id )
        .then( gameMat => res.send( gameMat ) )
        .catch( err => res.send( err ) );
};
    
exports.detailByName = ( req, res ) => {
    repository.findDetailsByName( req.params.name )
        .then( gameMat => res.send( gameMat ) )
        .catch( err => res.send( err ) );
};

exports.listByProject = ( req, res ) => {
    repository.findByProject( req.params.name )
        .then( gameMat => res.send( gameMat ) )
        .catch( err => res.send( err ) );
};

exports.update = (req, res) => {
    let matName = req.body.name;
    if(! utilities.validateMaterialName(matName)){
            res.status(400).send({"error":"Invalid Material Name : " + matName}); 
    }else{
        repository.update( req.params.id,req.body ).then( gameMat => res.send( gameMat ) ).catch( err => res.send( err ) );    
    }

    
};
