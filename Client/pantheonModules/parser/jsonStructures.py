import os
import sys
import json
from pantheonModules.versioning import requests
#from pantheonModules.jsonschema import validate
from ..jsonschema import validate
from ..jsonschema.exceptions import ValidationError




def getDataOrDefault(data,key,defaultValue):
    try: returnData = data[key] 
    except KeyError: returnData = defaultValue
    return returnData


class MayaParser():
    animationVersion0Schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "definitions": {},
        "id": "http://example.com/example.json",
        "properties": {
            "animations": {
                "id": "/properties/animations",
                "items": {
                    "id": "/properties/animations/items",
                    "properties": {
                        "clipEnd": {
                            "id": "/properties/animations/items/prop erties/clipEnd",
                            "type": "number"
                        },
                        "clipName": {
                            "id": "/properties/animations/items/properties/clipName",
                            "type": "string"
                        },
                        "clipStart": {
                            "id": "/properties/animations/items/properties/clipStart",
                            "type": "number"
                        }
                    },
                    "required": [
                        "clipStart",
                        "clipEnd",
                        "clipName"
                    ],
                    "type": "object"
                },
                "type": "array"
            }
        },
        "additionalProperties" : False,
        "required": [
            "animations"
        ],
        "type": "object"
    }

    animationVersion1Schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "definitions": {},
        "id": "http://example.com/example.json",
        "properties": {
            "animations": {
                "id": "/properties/animations",
                "items": {
                    "id": "/properties/animations/items",
                    "properties": {
                        "clipEnd": {
                            "id": "/properties/animations/items/properties/clipEnd",
                            "type": "number"
                        },
                        "clipName": {
                            "id": "/properties/animations/items/properties/clipName",
                            "type": "string"
                        },
                        "clipStart": {
                            "id": "/properties/animations/items/properties/clipStart",
                            "type": "number"
                        }
                    },
                    "required": [
                        "clipStart",
                        "clipEnd",
                        "clipName"
                    ],
                    "type": "object"
                },
                "type": "array"
            },
            "rootMotion": {
                "id": "/properties/rootMotion",
                "type": "boolean"
            }
        
        },
        "additionalProperties" : False,
        "required": [
            "rootMotion",
            "animations"
        ],
        "type": "object"
    }

    animationVersion2Schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "definitions": {},
        "id": "http://example.com/example.json",
        "properties": {
            "animations": {
                "id": "/properties/animations",
                "items": {
                    "id": "/properties/animations/items",
                    "properties": {
                        "clipEnd": {
                            "id": "/properties/animations/items/properties/clipEnd",
                            "type": "number"
                        },
                        "clipLoop": {
                            "id": "/properties/animations/items/properties/clipLoop",
                            "type": "boolean"
                        },
                        "clipName": {
                            "id": "/properties/animations/items/properties/clipName",
                            "type": "string"
                        },
                        "clipStart": {
                            "id": "/properties/animations/items/properties/clipStart",
                            "type": "number"
                        }
                    },
                    "required": [
                        "clipStart",
                        "clipLoop",
                        "clipEnd",
                        "clipName"
                    ],
                    "type": "object"
                },
                "type": "array"
            },
            "events": {
                "id": "/properties/events",
                "items": {},
                "type": "array"
            },
            "rootMotion": {
                "id": "/properties/rootMotion",
                "type": "boolean"
            }
        },
        "additionalProperties" : False,
        "required": [
            "rootMotion",
            "events",
            "animations"
        ],
        "type": "object"
    }


    animationVersion10Schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "definitions": {},
        "id": "http://example.com/example.json",
        "properties": {
            "animations": {
                "id": "/properties/animations",
                "items": {
                    "id": "/properties/animations/items",
                    "properties": {
                        "clipEnd": {
                            "id": "/properties/animations/items/properties/clipEnd",
                            "type": "number"
                        },
                        "clipLoop": {
                            "id": "/properties/animations/items/properties/clipLoop",
                            "type": "boolean"
                        },
                        "clipName": {
                            "id": "/properties/animations/items/properties/clipName",
                            "type": "string"
                        },
                        "clipRoot": {
                            "id": "/properties/animations/items/properties/clipRoot",
                            "type": "boolean"
                        },
                        "clipStart": {
                            "id": "/properties/animations/items/properties/clipStart",
                            "type": "number"
                        }
                    },
                    "required": [
                        "clipStart",
                        "clipLoop",
                        "clipEnd",
                        "clipRoot",
                        "clipName"
                    ],
                    "type": "object"
                },
                "type": "array"
            },
            "events": {
                "id": "/properties/events",
                "items": {
                    "id": "/properties/events/items",
                    "properties": {
                        "clipKeyEvent": {
                            "id": "/properties/events/items/properties/clipKeyEvent",
                            "type": "string"
                        },
                        "clipKeyFrame": {
                            "id": "/properties/events/items/properties/clipKeyFrame",
                            "type": "number"
                        }
                    },
                    "required": [
                        "clipKeyEvent",
                        "clipKeyFrame"
                    ],
                    "type": "object"
                },
                "type": "array"
            },
            "version": {
                "id": "/properties/version",
                "type": "number"
            }
        },
        "additionalProperties" : False,
        "required": [
            "version",
            "events",
            "animations"
        ],
        "type": "object"
    }

    materialsVersion1Schema = {
        "type" : "object",
        "patternProperties" : {
            "^.*$": {
                "type" : "object",
                "properties" : {
                    "shaderName" : {"type" : "string"},
                    "properties" : {
                        "type" : "array",
                        "items" : {
                            "type" : "object", 
                            "properties" : {
                                "propType" : {"type" : "string"},
                                "propName" : {"type" : "string"},
                                "propValue" : {"type" : "string"},
                            }
                        }
                    }
                }
            },   
        },
        "properties" : {
            "version" : {"type" : "number"}
        }
    }

    animationVersion0Data = {
        "tool" : "Maya_EzAnims",
        "versionNumber" : 0,
        "schema" : animationVersion0Schema
    }

    animationVersion1Data = {
        "tool" : "Maya_EzAnims",
        "versionNumber" : 1,
        "schema" : animationVersion1Schema
    }

    animationVersion2Data = {
        "tool" : "Maya_EzAnims",
        "versionNumber" : 2,
        "schema" : animationVersion2Schema
    }

    animationVersion10Data = {
        "tool" : "Maya_EzAnims",
        "versionNumber" : 10,
        "schema" : animationVersion10Schema
    }


    materialVersion1Data = {
        "tool" : "Maya_EzMaterials",
        "versionNumber" : 1,
        "schema" : materialsVersion1Schema
    }

    versions = []

    def __init__(self):
        self.versions = [self.animationVersion10Data,self.animationVersion2Data,self.animationVersion1Data,self.animationVersion0Data,self.materialVersion1Data]

    def getVersion(self, data):
        for version in self.versions:
            try:
                result = True
                validate(data, version["schema"])
            except ValidationError as e:
                
                result = False
            if result:
                #print("Data is a valid json of " + version["tool"])
                return version["versionNumber"]
            else:
                result = False
                #print("Data is invalid for " + version["tool"])
        return -1

    def validateData(self, data):
        result = self.getVersion(data)
        if result != -1:
            return True
        else:
            return False