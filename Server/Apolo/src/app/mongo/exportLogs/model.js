const mongoose = require( "mongoose" );

const Schema = mongoose.Schema;

const exportData = new Schema({
	name: { type: String },
    exportType: { type: String, lowercase: true, trim: true },
    exportSubType: { type: String, lowercase: true, trim: true }
 
} );


var exportsSchema = mongoose.Schema({
    	user : { type: String, required: true },
    	filename : { type: String, required: true },
		action : { type: String, required: true },
		command : { type: String, required: true },
		objects : [exportData]
}, {
    timestamps: true,
});

module.exports = mongoose.model( "exportLog", exportsSchema );
