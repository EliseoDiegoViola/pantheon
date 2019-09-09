const mongoose = require( "mongoose" );

const ExportLog = mongoose.model( "exportLog" );

const saveExport = async ( data ) => {
    try {
        const exportLog = new ExportLog( data );
        const query = await exportLog.save();
        return query;
    } catch ( err ) { return err; }
};

const findExports = async () => {
    const query = await ExportLog.find( );
    return query;
};

module.exports = {
    saveExport,
    findExports,
};