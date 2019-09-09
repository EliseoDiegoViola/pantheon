const mongoose = require( "mongoose" );

const Schema = mongoose.Schema;

const errorsSchema = new Schema({
    	user : { type: String, required: true },
		level : { type: String, required: true },
		action : { type: String, required: true },
		filename : { type: String, required: true },
		errorCode : Number,
		errorMessage : String
}, {
    timestamps: true,
} );

module.exports = mongoose.model( "errorLog", errorsSchema );
