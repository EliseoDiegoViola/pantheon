const jsonRouter = require( "./data/router" );
const hermesRouter = require( "./hermes/router" );
const versioningRouter = require( "./versioning/router" );

module.exports = ( app ) => {
    app.use( "/tools/data", jsonRouter );
    app.use( "/tools/hermes", hermesRouter );
    app.use( "/tools/versioning", versioningRouter );
};
