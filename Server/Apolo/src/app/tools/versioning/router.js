const controller = require( "./controller" );
const express = require( "express" );

const router = express.Router( );
router.get( "/update/:version", controller.changeVersion );
router.get( "/get", controller.getNewVersion );
router.get( "/peek", controller.peekVersion );

module.exports = router;
