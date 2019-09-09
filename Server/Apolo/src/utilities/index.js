

exports.extractObject = ( obj, keys ) => {
    const returnObj = { };
    keys.forEach( key => { returnObj[ key ] = obj[ key ]; } );

    return returnObj;
};

exports.validateMaterialName = (name) => {
	const regex = /\b(cs|fn|eb|es|gc|ko|su|gg|ms|mc|tt|me|sn|cos|in)_(foliage|fake|organic|glass|metal|concrete|wood|water|marble|stone|brick|holo|plastic|light|electronics|cloth|fabric|body|head|hair|ground|decal)_(trim|full|tile)_(.*)_(neat|old|cracked|rusty|moldy|dirty|base|rough)_(\d\d)/gmi;
	global.logger.info(name);
	let test = regex.exec(name);
	
	if( test ){
		return true;
	}else{
		return false;
	}
};
