const mongoose = require( "mongoose" );

const GameShader = mongoose.model( "gameShaders" );

const saveGameShader = async ( data ) => {
    global.logger.info("Save game shader");
    try {
        const gameShader = new GameShader( data );
        global.logger.info(JSON.stringify(data));
        const query = await gameShader.save();
        global.logger.info(query);
        return query;
    } catch ( err ) { 
        global.logger.info(err);
        return err; 

    }
};

const findGameShaders = async () => {
    global.logger.info("Fetching gameterial list");
    const query = await GameShader.find( );
    return query;
};

const deleteGameShader = async (shaderId) => {
    global.logger.info("deleting shader " + shaderId);
	const query = await GameShader.find({ id:shaderId }).remove().exec();
	return query;
};

const findDetails = async (shaderId) => {
    global.logger.info("fetching details " + shaderId);
    const query = await GameShader.findById(shaderId);
    
    return query;
};

const findDetailsByName = async (sName) => {
    global.logger.info("fetching details " + sName);
    const query = await GameShader.findOne({ shaderName:sName });
    return query;
};

const findByProject = async (sProject) => {
    global.logger.info("fetching shaders from " + sProject);
    const query = await GameShader.find({ project:sProject });
    return query;
};

const update = async (shaderId,data) => {
    global.logger.info("update shader id "+shaderId);    
    const query = await GameShader.findOneAndUpdate({ _id:shaderId }, data, {upsert:false,new:true});
    return query; 
};

module.exports = {
    saveGameShader,
    findGameShaders,
    deleteGameShader,
    findDetails,
    findDetailsByName,
    findByProject,
    update
};