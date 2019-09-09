const utilities = require( "../../../utilities" );
const repository = require( "./repository" );

exports.create = ( req, res ) => {
	try{

        repository.saveGameShader( req.body ).then( savedShader => res.send( utilities.extractObject(savedShader,[ "user","name", "shaderName","id","properties"] ) ) );
	}catch(e){
		res.status(400).send({"error":"invalid json body for game material creation"}); 
	}
};

// exports.update = ( req, res ) => {
//     res.send( );
// };

exports.delete = ( req, res ) => {
    repository.deleteGameShader(req.params["id"])
        .then(returnCode => res.send(returnCode))
        .catch(err => res.send(err));
};

exports.list = ( req, res ) => {
	global.logger.info("Loading game materials...");
    repository.findGameShaders()
        .then( gameShaders => res.send( gameShaders ))
        .catch( err => res.send( err ) );
};

exports.detail = ( req, res ) => {	
    repository.findDetails(req.params.id )
        .then( gameShader => res.send( gameShader ) )
        .catch( err => res.send( err ) );
};
    
exports.detailByName = ( req, res ) => {
    repository.findDetailsByName( req.params.name )
        .then( gameShader => res.send( gameShader ) )
        .catch( err => res.send( err ) );
};

exports.listByProject = ( req, res ) => {
    repository.findByProject( req.params.name )
        .then( gameShader => res.send( gameShader ) )
        .catch( err => res.send( err ) );
};

exports.update = (req, res) => {
    repository.update( req.params.id,req.body ).then( gameShader => res.send( gameShader ) ).catch( err => res.send( err ) );    

    
};
