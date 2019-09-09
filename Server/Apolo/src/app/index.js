const mongoData = require( "./mongo" );
const toolsData = require( "./tools" );

module.exports = ( app ) => {
    mongoData(app);
    toolsData(app);
};
