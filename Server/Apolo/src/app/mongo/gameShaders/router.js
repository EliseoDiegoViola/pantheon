require( "./model" );
const controller = require( "./controller" );

const express = require( "express" );

const router = express.Router( );


/**
*    @apiGroup exportLogs
*    @api {delete} /:id Deleting an existing game shader.
*/
router.delete( "/:id", controller.delete );

/**
*    @apiGroup exportLogs
*    @api {update} /:id Deleting an existing game shader.
*/
router.post( "/:id", controller.update );

/**
*    @apiGroup exportLogs
*    @api {post} / creates new game shader.
*/
router.post( "/", controller.create );

/**
*    @apiGroup exportLogs
*    @api {get} /:id Displaying details of an existing game shader.
*/
router.get( "/:id", controller.detail );

/**
*    @apiGroup exportLogs
*    @api {get} /:name Displaying details of an existing game shader.
*/
router.get( "/filterBy/name/:name", controller.detailByName );

/**
*    @apiGroup exportLogs
*    @api {get} /:name Displaying details of an existing game shader.
*/
router.get( "/filterBy/project/:name", controller.listByProject );

/**
*    @apiGroup exportLogs
*    @api {get} / Displaying the list with existing game shader.
*/
router.get( "/", controller.list );



module.exports = router;
