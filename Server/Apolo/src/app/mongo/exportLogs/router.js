require( "./model" );
const controller = require( "./controller" );

const express = require( "express" );

const router = express.Router( );

/**
*    @apiGroup exportLogs
*    @api {post} / Creating new exportLog.
*    @apiParam {String} name  The exported object's name is required.
*	 @apiParam {String} exportType  The exported object's type is required.
*    @apiParam {String} exportSubType  The exported object's sub type is required.
*
*    @apiParam {String} user  The export's user is required.
*	 @apiParam {String} filename  The export's filename is required.
*	 @apiParam {String} action  The export's action is required.
*	 @apiParam {String} command  The export's command is required.
*	 @apiParam {String} objects  The export's objects is NOT required.
*    @apiExample {response} Example response:
*       {
*         "exportLog": {
*            "user": "3DModeles-03",
*            "filename": "local/file/path/filename.max",
*            "action": "export",
*            "command": "3ds.max filename execute command"
*           }
*      }
*/
router.post( "/", controller.create );

/**
*    @apiGroup exportLogs
*    @api {delete} /:id Deleting an existing exportLog.
*/
router.delete( "/:id", controller.delete );


/**
*    @apiGroup exportLogs
*    @api {get} / Displaying the list with existing exportLog.
*/
router.get( "/", controller.list );

/**
*    @apiGroup exportLogs
*    @api {get} /:id Displaying details of an existing exportLog.
*/
// router.get( "/:id", controller.detail );

module.exports = router;
