const errorsLogRouter = require( "./errorLogs/router" );
const exportsLogRouter = require( "./exportLogs/router" );
const materialsRouter = require( "./gameMaterials/router" );
const shadersRouter = require( "./gameShaders/router" );
const projectsRouter = require( "./gameProjects/router" );

module.exports = ( app ) => {
	global.logger.info('Seetting mongos');
    app.use( "/errorLogs", errorsLogRouter );
    app.use( "/exportLogs", exportsLogRouter );
    app.use( "/gameMaterials", materialsRouter );
    app.use( "/gameShaders", shadersRouter );
    app.use( "/gameProjects", projectsRouter );
};
