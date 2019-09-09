require( "./model" );
const controller = require( "./controller" );

const express = require( "express" );

const router = express.Router( );

/**
*    @apiGroup errorLogs
*    @api {post} / Creating new errorLog.
*    @apiParam {String} user  The error's user is required.
*	 @apiParam {String} level  The error's level is required.
*    @apiParam {String} action  The error's action is required.
*    @apiParam {String} filename  The error's filename is required.
*	 @apiParam {String} errorCode  The error's errorCode is NOT required.
*	 @apiParam {String} errorMessage  The error's errorMessage is NOT required.
*    @apiExample {response} Example response:
*       {
*         "errorLog": {
*            "user": "3DModeles-03",
*            "level": "CRASH",
*            "action": "export",
*            "filename": "local/file/path/filename.max"
*           }
*      }
*/
router.post( "/", controller.create );

/**
*    @apiGroup errorLogs
*    @api {delete} /:id Deleting an existing errorLog.
*/
router.delete( "/:id", controller.delete );


/**
*    @apiGroup errorLogs
*    @api {get} / Displaying the list with existing errorLog.
*/
router.get( "/", controller.list );

/**
*    @apiGroup errorLogs
*    @api {get} /:id Displaying details of an existing errorLog.
*/
// router.get( "/:id", controller.detail );



module.exports = router;
