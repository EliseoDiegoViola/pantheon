const mongoose = require( "mongoose" );

const Schema = mongoose.Schema;


const shaderProperties = new Schema({
	propType: { type: String },
    propValue: { type: String, trim: true },
    propName: { type: String, trim: true }
 
} );

var shadersSchema = mongoose.Schema({
    	user : { type: String, required: true },
    	name : { type: String, required: true },
		shaderName : { type: String, required: true },
		properties :  [shaderProperties],
		project : { type: String, required: true }

}, {
    timestamps: true,
});

module.exports = mongoose.model( "gameShaders", shadersSchema );
