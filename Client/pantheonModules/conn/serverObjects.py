class MongoObject(object):

    def __init__(self, mongoId = 0):
        self.mongoId = mongoId

    def toDict(self):
        return todict(self)

    @classmethod
    def initFromJsonObject(cls, jsonObj):
        print("initFromJsonObject NOT IMPLEMENTED")
        return None

class MongoData():

    def toDict(self):
        return todict(self)

class ErrorLogs(MongoObject):

    def __init__(self,user,level,action,filename,errorCode,errorMessage,mongoId = None):
        super(ErrorLogs,self).__init__(mongoId)   
        self.user = user
        self.level = level
        self.action = action
        self.filename = filename
        self.errorCode = errorCode
        self.errorMessage = errorMessage

    @classmethod
    def initFromJsonObject(cls, jsonObj):
        # "Initialize MyData from a file"
        return cls(user=jsonObj["user"],
            level=jsonObj["user"],
            action=jsonObj["action"],
            filename=jsonObj["filename"],
            errorCode=jsonObj["errorCode"],
            errorMessage=jsonObj["errorMessage"],
            mongoId = jsonObj["_id"])

class ExportData(MongoData):

    def __init__(self,name,exportType,exportSubType):
        self.name = name
        self.exportType = exportType
        self.exportSubType = exportSubType

    @classmethod
    def initFromJsonObject(cls, jsonObj):
        # "Initialize MyData from a file"
        return cls(name=jsonObj["name"],
            exportType=jsonObj["exportType"],
            exportSubType=jsonObj["exportSubType"])

class ExportLogs(MongoObject):

    def __init__(self,user,filename,action,command,objects,mongoId = None):
        super(ExportLogs,self).__init__(mongoId)   
        self.user = user
        self.filename = filename
        self.action = action
        self.command = command
        self.objects = objects


    @classmethod
    def initFromJsonObject(cls, jsonObj):
        
        objects = []
        for obj in jsonObj["objects"]:
            exportData = ExportData.initFromJsonObject(obj)
            objects.append(exportData)

        return cls(user=jsonObj["user"],
            filename=jsonObj["filename"],
            action=jsonObj["action"],
            command=jsonObj["command"],
            objects=objects,
            mongoId=jsonObj["_id"])

class GameProjects(MongoObject):

    def __init__(self,name,mongoId = None):
        super(GameProjects,self).__init__(mongoId)   
        self.name = name

    @classmethod
    def initFromJsonObject(cls, jsonObj):
        return cls(name=jsonObj["name"],
            mongoId=jsonObj["_id"])

class MaterialProperties(MongoData):

    def __init__(self,propType,propValue,propName):
        self.propType = propType
        self.propValue = propValue
        self.propName = propName

    @classmethod
    def initFromJsonObject(cls, jsonObj):
        # "Initialize MyData from a file"
        return cls(propType=jsonObj["propType"],
            propValue=jsonObj["propValue"],
            propName=jsonObj["propName"])

class GameMaterials(MongoObject):

    def __init__(self,user,name,shaderName,properties,project,mongoId = None, thumbnail = None):
        super(GameMaterials,self).__init__(mongoId)   
        self.user = user
        self.name = name
        self.shaderName = shaderName
        self.properties = properties
        self.thumbnail = thumbnail
        self.project = project


    @classmethod
    def initFromJsonObject(cls, jsonObj):
        
        properties = []
        for obj in jsonObj["properties"]:
            matProp = MaterialProperties.initFromJsonObject(obj)
            properties.append(matProp)

        thumbnail = None
        if "thumbnail" in jsonObj:
            thumbnail = jsonObj["thumbnail"] 

        return cls(user=jsonObj["user"],
            name=jsonObj["name"],
            shaderName=jsonObj["shaderName"],
            properties=properties,
            project=jsonObj["project"],
            mongoId=jsonObj["_id"],
            thumbnail= thumbnail)

class ShaderProperties(MongoData):

    def __init__(self,propType,propValue,propName):
        self.propType = propType
        self.propValue = propValue
        self.propName = propName

    @classmethod
    def initFromJsonObject(cls, jsonObj):
        # "Initialize MyData from a file"
        return cls(propType=jsonObj["propType"],
            propValue=jsonObj["propValue"],
            propName=jsonObj["propName"])

class GameShaders(MongoObject):

    def __init__(self,user,name,shaderName,properties,project,mongoId = None, thumbnail = None):
        super(GameShaders,self).__init__(mongoId)   
        self.user = user
        self.name = name
        self.shaderName = shaderName
        self.properties = properties
        self.thumbnail = thumbnail
        self.project = project


    @classmethod
    def initFromJsonObject(cls, jsonObj):
        
        properties = []
        for obj in jsonObj["properties"]:
            matProp = ShaderProperties.initFromJsonObject(obj)
            properties.append(matProp)

        thumbnail = None
        if "thumbnail" in jsonObj:
            thumbnail = jsonObj["thumbnail"] 

        return cls(user=jsonObj["user"],
            name=jsonObj["name"],
            shaderName=jsonObj["shaderName"],
            properties=properties,
            project=jsonObj["project"],
            mongoId=jsonObj["_id"],
            thumbnail= thumbnail)

def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey)) 
            for key, value in obj.__dict__.items()
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj
