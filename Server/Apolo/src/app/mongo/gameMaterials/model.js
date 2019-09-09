const mongoose = require( "mongoose" );

const Schema = mongoose.Schema;


const materialProperties = new Schema({
	propType: { type: String },
    propValue: { type: String, trim: true },
    propName: { type: String, trim: true }
 
} );

var materialsSchema = mongoose.Schema({
    	user : { type: String, required: true },
    	name : { type: String, required: true },
		shaderName : { type: String, required: true },
		thumbnail: { type: String, required: false },
		properties :  [materialProperties],
		project : { type: String, required: true }

}, {
    timestamps: true,
});

module.exports = mongoose.model( "gameMaterials", materialsSchema );
