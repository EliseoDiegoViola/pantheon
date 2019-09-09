const mongoose = require( "mongoose" );

const GameProject = mongoose.model( "gameProjects" );

const saveGameProject = async ( data ) => {
    global.logger.info("Save game Project");
    try {
        const gameProject = new GameProject( data );
        global.logger.info(JSON.stringify(data));
        const query = await gameProject.save();
        global.logger.info(query);
        return query;
    } catch ( err ) { 
        global.logger.info(err);
        return err; 

    }
};

const findGameProjects = async () => {
    global.logger.info("Fetching gameProjects list");
    const query = await GameProject.find( );
    global.logger.info(query);
    return query;
};

const deleteGameProject = async (projectId) => {
    global.logger.info("deleting game project " + projectId);
	const query = await GameProject.find({ id:projectId }).remove().exec();
	return query;
};

const findDetails = async (projectId) => {
    global.logger.info("fetching details " + projectId);
    const query = await GameProject.findById(projectId);
    
    return query;
};

const findDetailsByName = async (pName) => {
    global.logger.info("fetching details " + pName);
    const query = await GameProject.findOne({ name:pName });
    return query;
};

const update = async (projectId,data) => {
    global.logger.info("update game project id "+projectId);    
    const query = await GameProject.findOneAndUpdate({ _id:projectId }, data, {upsert:false,new:true});
    return query; 
};

module.exports = {
    saveGameProject,
    findGameProjects,
    deleteGameProject,
    findDetails,
    findDetailsByName,
    update
};