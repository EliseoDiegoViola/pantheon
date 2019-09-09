const utilities = require( "../../../utilities" );
const repository = require( "./repository" );

exports.create = ( req, res ) => {
	try{
		repository.saveExport( req.body )
        .then( savedExport => res.send( utilities.extractObject(
            savedExport,
            [ "user", "level", "action","filename","id" ] ) ) );
	}catch(e){
		res.status(400).send({"error":"invalid json body for export log creation"}); 
	}

};




exports.update = ( req, res ) => {
    res.send( );
};

exports.delete = ( req, res ) => {
    res.send( );
};
//res.send( exportLogs );
exports.list = ( req, res ) => {
	global.logger.info("Loading exports...");
    repository.findExports()
        .then( exportLogs => res.send( exportLogs ))
        .catch( err => res.send( err ) );
};

// exports.detail = ( req, res ) => {
//     repository.findDetails( req.params.id )
//         .then( article => res.success( article ) )
//         .catch( err => res.send( err ) );
// };
