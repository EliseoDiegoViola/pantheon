const mongoose = require( "mongoose" );

const Schema = mongoose.Schema;

var projectSchema = mongoose.Schema({
    	name : { type: String, required: true },
}, {
    timestamps: true,
});

module.exports = mongoose.model( "gameProjects", projectSchema );
