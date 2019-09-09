const utilities = require( "../../../utilities" );
const repository = require( "./repository" );

exports.create = ( req, res ) => {
	try{
		repository.saveError( req.body )
        .then( savedError => res.send( utilities.extractObject(
            savedError,
            [ "user", "level", "action","filename","id"] ) ) );
	}catch(e){
		res.status(400).send({"error":"invalid json body for errorLog creation"}); 
	}
    
};

// exports.update = ( req, res ) => {
//     res.send( );
// };

exports.delete = ( req, res ) => {
    res.send( );
};

exports.list = ( req, res ) => {
    repository.findErrors()
        .then( errorLogs => res.send( errorLogs ) )
        .catch( err => res.send( err ) );
};

// exports.detail = ( req, res ) => {
//     repository.findDetails( req.params.id )
//         .then( article => res.success( article ) )
//         .catch( err => res.send( err ) );
// };
