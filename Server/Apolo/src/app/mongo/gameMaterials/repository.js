const mongoose = require( "mongoose" );

const GameMaterial = mongoose.model( "gameMaterials" );

const saveGameMat = async ( data ) => {
    global.logger.info("Save game dat");
    try {
        const gameMat = new GameMaterial( data );
        const query = await gameMat.save();
        return query;
    } catch ( err ) { 
        return err; 
    }
};

const findGameMats = async () => {
    global.logger.info("Fetching gameterial list");
    const query = await GameMaterial.find( );
    return query;
};

const deleteGameMat = async (matId) => {
    global.logger.info("deleting " + matId);
	const query = await GameMaterial.find({ id:matId }).remove().exec();
	return query;
};

const findDetails = async (matId) => {
    global.logger.info("fetching details " + matId);
    const query = await GameMaterial.findById(matId);
    
    return query;
};

const findDetailsByName = async (matName) => {
    global.logger.info("fetching details " + matName);
    const query = await GameMaterial.findOne({ name:matName });
    return query;
};

const findByProject = async (projectName) => {
    global.logger.info("fetching materials from " + projectName);
    const query = await GameMaterial.find({ project:projectName });
    return query;
};

const update = async (matId,data) => {
    global.logger.info("update mat id "+matId);    
    const query = await GameMaterial.findOneAndUpdate({ _id:matId }, data, {upsert:false,new:true});
    return query; 
};

module.exports = {
    saveGameMat,
    findGameMats,
    deleteGameMat,
    findDetails,
    findDetailsByName,
    findByProject,
    update
};