const controller = require( "./controller" );
const express = require( "express" );

const router = express.Router( );
router.post( "/message", controller.sendMessage );
router.post( "/report", controller.reportAction );
router.get( "/isAlive", controller.checkHermes );

module.exports = router;
