from .exportable import *
from .exportableMaterial import *





class exportableContent(exportable):

    

    represetationMaterials = []


    def __repr__(self):
        return self.localOverride.MiscUtilities.GetObjectName(self.objectRepresentation)  

    def __init__(self,contentNode,exportableParent,meshType):
        super(exportableContent,self).__init__(contentNode,exportableParent,meshType)   
        
        

    def getMaterials(self):
        materials = self.localOverride.MeshesUtilities.GetAllMaterialsFromObjects([self.objectRepresentation])
        # print "ORI!", len(materials) , " FROM " , str(self)

        self.represetationMaterials = [exportableMaterial(m,self,EXPORTABLE_TYPE.MATERIAL) for m in materials]
        # print "ABSTRACT!" ,self.represetationMaterials[0]
        # print (self.represetationMaterials)
        

    