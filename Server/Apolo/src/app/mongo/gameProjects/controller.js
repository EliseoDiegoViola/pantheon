const utilities = require( "../../../utilities" );
const repository = require( "./repository" );

exports.create = ( req, res ) => {
	try{

        repository.saveGameProject( req.body ).then( savedShader => res.send( utilities.extractObject(savedShader,["name"] ) ) );
	}catch(e){
		res.status(400).send({"error":"invalid json body for game material creation"}); 
	}
};

// exports.update = ( req, res ) => {
//     res.send( );
// };

exports.delete = ( req, res ) => {
    repository.deleteGameProject(req.params["id"])
        .then(returnCode => res.send(returnCode))
        .catch(err => res.send(err));
};

exports.list = ( req, res ) => {
	global.logger.info("Loading game projects...");
    repository.findGameProjects()
        .then( gameProject => res.send( gameProject ))
        .catch( err => res.send( err ) );
};

exports.detail = ( req, res ) => {	
    repository.findDetails(req.params.id )
        .then( gameProject => res.send( gameProject ) )
        .catch( err => res.send( err ) );
};
    
exports.detailByName = ( req, res ) => {
    repository.findDetailsByName( req.params.name )
        .then( gameProject => res.send( gameProject ) )
        .catch( err => res.send( err ) );
};

exports.update = (req, res) => {
    repository.update( req.params.id,req.body ).then( gameProject => res.send( gameProject ) ).catch( err => res.send( err ) );    

    
};
