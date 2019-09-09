const mongoose = require( "mongoose" );

const ErrorLog = mongoose.model( "errorLog" );

const saveError = async (data ) => {
    try {
        const error = new ErrorLog( data );
        const query = await error.save();
        return query;
    } catch ( err ) { return err; }
};

const findErrors = async () => {
    const query = await ErrorLog.find( );
    return query;
};

module.exports = {
    saveError,
    findErrors,
};