#!/usr/bin/ node

const express = require( "express" );
const bodyParser = require( "body-parser" );

const config = require( "./config" );
// const customResponses = require( "./middlewares/customResponses" );
global.logger = require( "./utilities/logger" );

const app = express( );
const port = process.env.PORT || config.port;
const ENV = process.env.NODE_ENV || config.env;

app.set( "env", ENV );
app.use( bodyParser.json( ));
// app.use( customResponses );

require( "./config/mongoose" )( app );
require( "./app/mongo" )( app );
require( "./app/tools" )( app );

// app.use( ( req, res ) => {
//     res.notFound( );
// } );

// app.get('/', function (req, res) {
//    res.send('Hello World');
// })



app.listen( port, ( ) => {
    global.logger.info( `Listening on port ${ port }` );
} );
