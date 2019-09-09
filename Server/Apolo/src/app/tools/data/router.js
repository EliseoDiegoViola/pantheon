const controller = require( "./controller" );

const express = require( "express" );

const router = express.Router( );

router.get( "/:jsonName", controller.list );

module.exports = router;
