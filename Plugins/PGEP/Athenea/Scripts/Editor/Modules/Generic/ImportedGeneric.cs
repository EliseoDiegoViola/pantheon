using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Athenea
{
    public class ImportedGeneric : ImportedObject {

        public ImportedGeneric(string assetName, string relativePathToAsset, string absolutePathToAsset, GameObject objectRoot, string typ, string subTyp, SimpleJSON2.JSONObject eData) : base(assetName, relativePathToAsset, absolutePathToAsset, objectRoot, typ, subTyp,eData)
        {
        }
        
    	
    }
}