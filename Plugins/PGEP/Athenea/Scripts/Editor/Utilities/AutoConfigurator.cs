using UnityEngine;
using UnityEditor;
using SimpleJSON2;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using Hermes;
using Pantheon;

namespace Athenea
{
	public static class AutoConfigurator {

		#region Owners Keyworks
		private const string RootOwner = "__ROOT__";
		private const string TriggersOwner = "__TRIGGERS__";
		private const string CollidersOwner = "__COLLIDERS__";
		private const string RendererOwner = "__RENDERERS__";
		private const string StaticOwner = "__STATIC__";
        #endregion

        #region Parsing Tokens

	    private const char parsingDelemiter = '~';
	    private const char all = '*';
	    private const char not = '$';
	    private const char contains = '^';

        #endregion

        private static ImportedObject imp; //FIXME The workaround to allow bad code structures (from other people)!

		public struct ComponentProperty
		{
			public string propertyName;
            public JSONNode propertyValue;
			public string propertyType;
		}

		public struct ProcessArgument
		{
			public string argumentName;
            public JSONNode argumentValue;
			public string argumentType;
		}


//		public static void ConfigureObject(GameObject obj,string Otyp){
//			ConfigureObject (obj, Otyp, "");
//		}

		private static JSONObject  Parse(string data){
			return JSON.Parse (data).AsObject;
		}

		private static JSONObject LoadData(string dataName){
			string data = PathsBuilder.GetData (dataName);
			JSONObject jsonClass = JSONObject.Parse (data).AsObject;
			return jsonClass;
		}

        public static void PostProcess(ImportedObject impObj)
        {
            imp = impObj;

            string dataName = string.IsNullOrEmpty(imp.SubTyp) ? imp.Typ : imp.Typ + "_" + imp.SubTyp;

            JSONObject parsedData = LoadData(dataName);
            JSONArray reqPost = parsedData["postProcess"].AsArray;

            for (int i = 0; i < reqPost.Count; i++)
            {
                JSONObject processToRun = reqPost[i].AsObject;

                string nspace = processToRun["namespace"].Value;
                string nscript = processToRun["scriptName"].Value;
                string dll = processToRun["dll"].Value;
                string method = processToRun["methodName"].Value;
                string owner = ParseRelativeData(processToRun["owner"]).Value;

                JSONArray argumentsData = processToRun["arguments"].AsArray;
                ProcessArgument[] arguments = new ProcessArgument[argumentsData.Count];
                for (int j = 0; j < argumentsData.Count; j++)
                {
                    arguments[j] = new ProcessArgument();
                    arguments[j].argumentType = argumentsData[j]["argType"].Value;
                    arguments[j].argumentValue = ParseRelativeData(argumentsData[j]["argValue"]);
                    arguments[j].argumentName = argumentsData[j]["argName"].Value;
                }

                ParseRequiredProcesses(imp.ObjectRoot, dll, nspace, nscript, method, owner, arguments);
            }

            imp = null;
        }

        public static void ConfigureObject(ImportedObject impObj){
            imp = impObj;

            string dataName = string.IsNullOrEmpty (imp.SubTyp) ? imp.Typ: imp.Typ + "_" + imp.SubTyp;

            JSONObject parsedData =  LoadData (dataName);
			JSONArray reqComps = parsedData ["requiredComponents"].AsArray;
			JSONArray reqProc = parsedData ["requiredProcess"].AsArray;

			for (int i = 0; i < reqComps.Count; i++) {
				JSONObject componentToAdd = reqComps [i].AsObject;

				string nspace = componentToAdd ["namespace"].Value;
				string nscript = componentToAdd ["scriptName"].Value;
				string dll = componentToAdd ["dll"].Value;
				string owner = ParseRelativeData(componentToAdd ["owner"]).Value;

				JSONArray propertiesData = componentToAdd ["properties"].AsArray;
				ComponentProperty[] properties = new ComponentProperty[propertiesData.Count];
				for (int j = 0; j < propertiesData.Count; j++) {
					properties [j] = new ComponentProperty ();
					properties [j].propertyType = propertiesData[j] ["propertyType"].Value;
                    properties [j].propertyValue = ParseRelativeData(propertiesData[j]["propertyValue"]);
					properties [j].propertyName = propertiesData[j]  ["propertyName"].Value;	 
				} 

                ParseRequiredProperties (imp.ObjectRoot,dll, nspace, nscript, owner, properties);
			}

			for (int i = 0; i < reqProc.Count; i++) {
				JSONObject processToRun = reqProc [i].AsObject;

				string nspace = processToRun ["namespace"].Value;
				string nscript = processToRun ["scriptName"].Value;
				string dll = processToRun ["dll"].Value;
				string method = processToRun ["methodName"].Value;
				string owner = ParseRelativeData(processToRun["owner"]).Value;

                JSONArray argumentsData = processToRun ["arguments"].AsArray;
				ProcessArgument[] arguments = new ProcessArgument[argumentsData.Count];
				for (int j = 0; j < argumentsData.Count; j++) {
					arguments [j] = new ProcessArgument ();
					arguments [j].argumentType = argumentsData[j] ["argType"].Value;
                    arguments [j].argumentValue = ParseRelativeData(argumentsData[j]["argValue"]);
                    arguments [j].argumentName = argumentsData[j]  ["argName"].Value;	 
				} 

                ParseRequiredProcesses (imp.ObjectRoot,dll, nspace, nscript,method, owner, arguments);
			}

            imp = null;
		}
			

		#region Process
		private static void ParseRequiredProcesses(GameObject rootObject,string dll,string nspace,string nscript,string methodName, string owner, ProcessArgument[] properties){
			Type compToAdd = Type.GetType (nspace + "." + nscript + "," + dll);

            if (compToAdd != null)
            {
                Debug.Log("Component Found in " + nspace + "." + nscript + "," + dll);
            }
            else
            {
                Debug.LogError("Component NOT Found in " + nspace + "." + nscript + "," + dll);
            }

			if (owner.Equals(RootOwner)) {
				RunRequiredInstanceProcess (rootObject, compToAdd,methodName, properties);
			} else if (owner.Equals(StaticOwner)) {
				RunRequiredStaticProcess (rootObject, compToAdd,methodName, properties);
			}  else{
				GameObject newOwner =  rootObject.transform.FindDeepChild (owner).gameObject;
				if (newOwner != null) {
					RunRequiredInstanceProcess (newOwner, compToAdd,methodName, properties);
				} else {
					Debug.LogError ("owner " + owner + " does not exist in " + rootObject.name);
				}

			}
		}


		private static void RunRequiredStaticProcess(GameObject obj,Type compToAdd,string methodName,ProcessArgument[] arguments){
			object[] parameters = new object[arguments.Length];
			for (int i = 0; i < arguments.Length; i++) {
				ProcessArgument argument = arguments [i];

                MethodInfo parserMethod =  typeof(AutoConfigurator).GetMethod (argument.argumentType, BindingFlags.Static |
                    BindingFlags.NonPublic |
                    BindingFlags.Public |
                    BindingFlags.FlattenHierarchy);

                if (parserMethod != null) {
                    Debug.Log ("Running method  " + argument.argumentType);
                    object valueObject = parserMethod.Invoke (null, new object[]{argument.argumentValue});
                    parameters [i] = valueObject;
                } else {
                    Debug.LogError (" Does not contains method " + argument.argumentType);
                }
                  
				
			}
			MethodInfo method = compToAdd.GetMethod (methodName, BindingFlags.Static |
				BindingFlags.NonPublic |
				BindingFlags.Public |
				BindingFlags.FlattenHierarchy);

			if (method != null) {
				Debug.Log ("Running method  " + methodName + " for component " + obj.name);
				method.Invoke (null, parameters);
			} else {
				Debug.LogError (compToAdd.ToString() + " Does not contains method " + methodName);
			}

		}

		private static void RunRequiredInstanceProcess(GameObject obj,Type compToAdd,string methodName, ProcessArgument[] arguments){
			Component c = obj.GetComponent (compToAdd);
			if (c != null) {
				object[] parameters = new object[arguments.Length];
				for (int i = 0; i < arguments.Length; i++) {
					ProcessArgument argument = arguments [i];

                    MethodInfo parserMethod = typeof(AutoConfigurator).GetMethod (argument.argumentType, BindingFlags.Static |
                        BindingFlags.NonPublic |
                        BindingFlags.Public |
                        BindingFlags.FlattenHierarchy);

                    if (parserMethod != null) {
                        Debug.Log ("Running method  " + argument.argumentType);
                        object valueObject = parserMethod.Invoke (null, new object[]{argument.argumentValue});
                        parameters [i] = valueObject;
                    } else {
                        Debug.LogError (" I dont have the parser " + argument.argumentType);
                    }

				}
				MethodInfo method = compToAdd.GetMethod (methodName, BindingFlags.Instance |
					BindingFlags.NonPublic |
					BindingFlags.Public |
					BindingFlags.FlattenHierarchy);

				if (method != null) {
					
					try{
                        Debug.Log ("Running method  " + methodName + " for component " + obj.name);
						method.Invoke (c, parameters);
					}catch(Exception e){
						Debug.LogError (methodName + " | " + e.Message + " | " + obj.name);
					}

				} else {
					Debug.LogError (compToAdd.ToString() + " Does not contains method " + methodName);
				}

			} else {
				Debug.LogError (obj.name + " Does not contains component " + compToAdd.Name);
			}

		}
		#endregion

		#region Properties and fields
		private static void ParseRequiredProperties(GameObject rootObject,string dll,string nspace,string nscript, string owner, ComponentProperty[] properties){
			Type compToAdd = Type.GetType (nspace + "." + nscript + "," + dll);

		    var objectsToApply = ParseOwnership(rootObject, owner);
		    foreach (GameObject go in objectsToApply)
		    {
		        //MeshRenderer r = go.GetComponent<MeshRenderer>();

                //so.FindProperty("m_ScaleInLightmap").floatValue = 0;
                //so.ApplyModifiedProperties();
		        //SerializedObject so = new SerializedObject(r);
                //Debug.Log(so.FindProperty("m_ScaleInLightmap").floatValue);
                AssignPropertiesToObject(go, compToAdd, properties);
		        //Debug.Log(so.FindProperty("m_ScaleInLightmap").floatValue);
                //Debug.Log(go.name);
            }
            

		    //         if (owner.Equals(RootOwner)) {
		    //	AssignPropertiesToObject (rootObject, compToAdd, properties);
		    //} else if (owner.Equals(TriggersOwner)) {
		    //	Collider[] trigs = rootObject.GetComponentsInChildren<Collider> (true);
		    //	if (trigs != null) {
		    //		for(int j = 0; j < trigs.Length; j++){
		    //			if (trigs [j].isTrigger) {
		    //				AssignPropertiesToObject (trigs[j].gameObject, compToAdd, properties);
		    //			}

		    //		}
		    //	}
		    //} else if (owner.Equals(CollidersOwner)) {
		    //	Collider[] trigs = rootObject.GetComponentsInChildren<Collider> (true);
		    //	if (trigs != null) {
		    //		for(int j = 0; j < trigs.Length; j++){
		    //			if (!trigs [j].isTrigger) {
		    //				AssignPropertiesToObject (trigs[j].gameObject, compToAdd, properties);
		    //			}

		    //		}
		    //	}
		    //} else if (owner.Equals(RendererOwner)) {
		    //	Renderer[] rends = rootObject.GetComponentsInChildren<Renderer> (true);
		    //	if (rends != null) {
		    //		for(int j = 0; j < rends.Length; j++){
		    //			AssignPropertiesToObject (rends[j].gameObject, compToAdd, properties);
		    //		}
		    //	}
		    //} else{
		    //	GameObject newOwner =  rootObject.transform.FindDeepChild (owner).gameObject;
		    //	if (newOwner != null) {
		    //		AssignPropertiesToObject (newOwner, compToAdd, properties);
		    //	} else {
		    //		Debug.LogError ("owner " + owner + " does not exist in " + rootObject.name);
		    //	}

		    //}
		}

		private static void AssignPropertiesToObject(GameObject obj,Type compToAdd, ComponentProperty[] properties){
			Component c = null;
			if ((c = obj.GetComponent (compToAdd)) == null) {
                Debug.Log(string.Format("Component {0} not found , adding...", compToAdd));
				c =  obj.AddComponent (compToAdd);
			}


			for (int i = 0; i < properties.Length; i++) {
				ComponentProperty propData = properties [i];

                //JSONNode valueToParse = impObj.ExtraData.ContainsKey(argument.argumentValue.Value) ? impObj.ExtraData[argument.argumentValue.Value] : argument.argumentValue ;
                object valueObject = null;
                Debug.Log(propData.propertyType);
                MethodInfo parserMethod = typeof(AutoConfigurator).GetMethod (propData.propertyType, BindingFlags.Static |
                    BindingFlags.NonPublic |
                    BindingFlags.Public |
                    BindingFlags.FlattenHierarchy);

                if (parserMethod != null) {
                    Debug.Log ("Running method  " + parserMethod.Name);
                    valueObject = parserMethod.Invoke (null, new object[]{propData.propertyValue});

                } else {
                    Debug.LogError (" Does not contains method " + propData.propertyType);
                }
                    
				/*BindingFlags bindingFlags = BindingFlags.Instance |
				                            BindingFlags.Static |
				                            BindingFlags.NonPublic |
				                            BindingFlags.Public |
				                            BindingFlags.FlattenHierarchy;*/
				
				FieldInfo field = compToAdd.GetField (propData.propertyName);
				PropertyInfo property = compToAdd.GetProperty (propData.propertyName);
			    SerializedObject so = new SerializedObject(c);
			    SerializedProperty sp = so.FindProperty(propData.propertyName);

			    if (field != null)
			    {
			        Debug.Log("Setting value " + compToAdd.ToString() + " for field " + field + " for component " +
			                  compToAdd.ToString());
			        field.SetValue(c, valueObject);
			    }
			    else if (property != null)
			    {
			        try
			        {
			            Debug.Log("Setting value " + compToAdd.ToString() + " for property " + property + " for component " +
			                      compToAdd.ToString() + " with value " + valueObject);
			            property.SetValue(c, valueObject, null);


			        }
			        catch (Exception e)
			        {
			            Debug.LogError(e.Message);
			        }
			    }
			    else if(sp != null)
			    {
                    // mmm..... arrays?
			        sp.SetValue(valueObject, parserMethod.ReturnType);
			        so.ApplyModifiedProperties();
			    }

			}
		}
        #endregion

        #region Parsers

        private static JSONNode ParseRelativeData(JSONNode variable) {
            if (string.IsNullOrEmpty(variable.Value))
            {
                return variable;
            }
            string value = variable.Value;
            string[] valueParts = value.Split('.');
            JSONObject whereToSearch = imp.ExtraData;
            JSONNode foundValue = null;
            if (whereToSearch.ContainsKey(valueParts[0])) {
                for (int i = 0; i < valueParts.Length; i++)
                {
                    if (whereToSearch.ContainsKey(valueParts[i]))
                    {
                        if (i < valueParts.Length - 1)
                        {
                            whereToSearch = whereToSearch[valueParts[i]].AsObject;
                        }
                        else
                        {
                            foundValue = whereToSearch[valueParts[i]];
                        }

                    }
                    else
                    {
                        throw new Exception("Wrong data search " + value);
                    }
                }
            }
            else {
                foundValue = value;
            }
            return foundValue;
        }
        

        private static string AtnParseToString(JSONNode val){
            return val.Value;
        }

        private static float AtnParseToFloat(JSONNode val){
            return float.Parse (val.Value);
        }

        private static int AtnParseToInt(JSONNode val){
            return int.Parse(val.Value);
        }

        private static bool AtnParseToBool(JSONNode val){
            bool result = false;
            bool.TryParse(val.Value, out result);
            return result;
            //return bool.Parse(val.Value);
        }

        private static object AtnParseToEnum(JSONNode val){
            string[] parts = val.Value.Split ('.');
            object value = null;
            if (parts.Length < 2) {
                Debug.LogError ("Invalid enum data " + val.Value);
            }else if (parts.Length >= 2) {
                string enumValue = parts [parts.Length-1];
                string type = String.Join(".",parts.Take (parts.Length - 1).ToArray());
                Type typ = Type.GetType (type +",Assembly-CSharp");
                value =  Convert.ChangeType(Enum.Parse (typ, enumValue),typ);
            }
            return value;
        }

        private static GameObject AtnParseToGameObject(JSONNode val){
            GameObject value = null;
            if (val.Value.Equals (RootOwner)) {
                value = imp.ObjectRoot;
            } else {
                Transform child = imp.ObjectRoot.transform.FindDeepChild(val.Value);
                if (child != null)
                {
                    value = imp.ObjectRoot.transform.FindDeepChild(val.Value).gameObject;
                }
            }
            return value;
        }

        private static UnityEngine.Object AtnParseToPath(JSONNode val){
            string path = PathsBuilder.GetPathToFile(val.Value);
            UnityEngine.Object value = AssetDatabase.LoadAssetAtPath<UnityEngine.Object>(path);
            return value;
        }

        private static Vector3 AtnParseToVector3(JSONNode val){
            string sVector = "-1000,-1000,-1000";
            // Remove the parentheses
            if (val.Value.StartsWith ("(") && val.Value.EndsWith (")")) {
                sVector = val.Value.Substring(1, val.Value.Length-2);
            }

            // split the items
            Debug.Log(val.Value);
            string[] sArray = sVector.Split(',');

            // store as a Vector3
            Vector3 result = new Vector3(
                float.Parse(sArray[0]),
                float.Parse(sArray[1]),
                float.Parse(sArray[2]));

            return result;
        }

        private static string[] AtnParseToArray_String(JSONNode val)
        {
            JSONArray jarr = val.AsArray;
            string[] arr = new string[jarr.Count];
            for (int i = 0; i < arr.Length; i++)
            {
                arr[i] = jarr[i].Value;
            }
            return arr;
        }

        private static GameObject[] AtnParseToArray_GameObject(JSONNode val)
        {
            JSONArray jarr = val.AsArray;
            GameObject[] arr = new GameObject[jarr.Count];
            for (int i = 0; i < arr.Length; i++)
            {
                string meshName = jarr[i].Value;
                GameObject value = null;
                if (meshName.Equals(RootOwner))
                {
                    value = imp.ObjectRoot;
                }
                else
                {
                    Transform child = imp.ObjectRoot.transform.FindDeepChild(meshName);
                    if (child != null)
                    {
                        value = child.gameObject;
                    }
                }
                arr[i] = value;
            }
            return arr;
        }
        #endregion

        #region Special Objects
        private static object AtnParseToArray_SeeThrough(JSONNode val)
        {

            JSONArray colArray = val.AsArray;
            if (colArray != null)
            {
                SeeThroughGroup[] seeThroughGrps = new SeeThroughGroup[colArray.Count];
                for (int j = 0; j < seeThroughGrps.Count(); j++)
                {
                    seeThroughGrps[j] = new SeeThroughGroup();
                    
                    seeThroughGrps[j].id = colArray[j].AsObject["id"].Value;
                    

                    JSONArray boxes = colArray[j].AsObject["seeThroughs"].AsArray;
                    seeThroughGrps[j].boxes = new SeeThroughBox[boxes.Count];
                    for (int i = 0; i < boxes.Count; i++)
                    {

                        seeThroughGrps[j].boxes[i] = new SeeThroughBox();
                        string lostChild = boxes[i].AsObject["node"].Value;

                        seeThroughGrps[j].boxes[i].box = imp.ObjectRoot.transform.FindDeepChild(lostChild).gameObject;
                        seeThroughGrps[j].boxes[i].colType = (ColliderType)Enum.Parse(typeof(ColliderType), boxes[i]["colType"].Value.ToUpper());
                         
                    }


                    
                }
                return seeThroughGrps;
            }
            else
            {
                HermesLogger.Log("SeeThough boxes is not setted for this object -- " + imp.ObjectRoot.name);
                return null;
            }

        }

        private static object AtnParseToArray_DynamicObject(JSONNode val)
        {

            JSONArray gosArray = val.AsArray;
            if (gosArray != null)
            {
                GameObject[] gos = new GameObject[gosArray.Count];
                for (int j = 0; j < gos.Count(); j++)
                {
                    string lostChild = gosArray[j].AsObject["node"].Value;
                    gos[j] = imp.ObjectRoot.transform.FindDeepChild(lostChild).gameObject;
                }
                return gos;
            }
            else
            {
                HermesLogger.Log("Dynamic objects is not setted for this object -- " + imp.ObjectRoot.name);
                return null;
            }

        }

        private static object AtnParseToArray_ColliderData(JSONNode val)
        {
            JSONArray colArray = val.AsArray;
            if (colArray != null)
            {
                ColliderData[] colliders = new ColliderData[colArray.Count];
                for (int j = 0; j < colliders.Count(); j++)
                {
                    colliders[j] = new ColliderData();
                    colliders[j].meshName = colArray[j].AsObject["node"].Value;
                    colliders[j].colType = (ColliderType)Enum.Parse(typeof(ColliderType), colArray[j].AsObject["colType"].Value.ToUpper());
                }
                return colliders;
            }
            else
            {
                HermesLogger.Log("Colliders is not setted for this object -- " + imp.ObjectRoot.name);
                return null;
            }

        }

        private static object AtnParseToArray_RoomData(JSONNode val)
        {

            JSONArray colArray = val.AsArray;
            if (colArray != null)
            {
                ImportedRoom[] iRooms = new ImportedRoom[colArray.Count];
                for (int j = 0; j < iRooms.Count(); j++)
                {
                    iRooms[j] = new ImportedRoom();
                    string lostChild = colArray[j].AsObject["node"].Value;
                    iRooms[j].box = imp.ObjectRoot.transform.FindDeepChild(lostChild).gameObject;
                    iRooms[j].id = colArray[j].AsObject["roomId"].Value;
                }
                return iRooms;
            }
            else
            {
                HermesLogger.Log("RoomData is not setted for this object -- " + imp.ObjectRoot.name);
                return null;
            }

        }

        private static object AtnParseToArray_LayerData(JSONNode val)
        {
            JSONArray layArray = val.AsArray;
            if(layArray != null) {
                LayerData[] layers = new LayerData[layArray.Count];
                for (int j = 0; j < layers.Count(); j++)
                {
                    layers[j] = new LayerData();
                    layers[j].meshName = layArray[j].AsObject["node"].Value;
                    layers[j].layer = LayerMask.NameToLayer(layArray[j].AsObject["layer"].Value);
                }
                return layers;
            }
            else
            {
                HermesLogger.Log("Layers is not setted for this object -- " + imp.ObjectRoot.name);
                return null;
            }
            
        }

        private static object AtnParseToArray_StaticFlagData(JSONNode val)
        {
            //Debug.Log(val);
            JSONArray staticFlagArray = val.AsArray;
            if (staticFlagArray != null) {
                StaticFlagData[] staticData = new StaticFlagData[staticFlagArray.Count];
                for (int j = 0; j < staticData.Count(); j++)
                {
                    staticData[j] = new StaticFlagData();
                    staticData[j].meshName = staticFlagArray[j].AsObject["node"].Value;
                    staticData[j].batchingStatic = staticFlagArray[j].AsObject["batchingStatic"].AsBool;
                    staticData[j].lightmapStatic = staticFlagArray[j].AsObject["lightmapStatic"].AsBool;
                    staticData[j].navigationStatic = staticFlagArray[j].AsObject["navigationStatic"].AsBool;
                    staticData[j].occluderStatic = staticFlagArray[j].AsObject["occluderStatic"].AsBool;
                    staticData[j].occludeeStatic = staticFlagArray[j].AsObject["occludeeStatic"].AsBool;
                    staticData[j].offMeshLinkGeneration = staticFlagArray[j].AsObject["offMeshLinkGeneration"].AsBool;
                    staticData[j].reflectionProbeStatic = staticFlagArray[j].AsObject["reflectionProbeStatic"].AsBool;
                }
                return staticData;
            }
            else
            {
                HermesLogger.Log("Static Flags is not setted for this object -- " + imp.ObjectRoot.name);
                return null;
            }
            
        }

        private static object AtnParseToArray_NavMeshLayerData(JSONNode val)
        {
            //Debug.Log(val);
            JSONArray navmeshLayerArray = val.AsArray;
            if (navmeshLayerArray != null)
            {
                NavMeshLayerData[] navmeshData = new NavMeshLayerData[navmeshLayerArray.Count];
                for (int j = 0; j < navmeshData.Count(); j++)
                {
                    navmeshData[j] = new NavMeshLayerData();
                    navmeshData[j].meshName = navmeshLayerArray[j].AsObject["node"].Value;
                    navmeshData[j].navmeshLayer = GameObjectUtility.GetNavMeshAreaFromName(navmeshLayerArray[j].AsObject["navmesh"].Value);
                }
                return navmeshData;
            }
            else
            {
                HermesLogger.Log("Colliders is not setted for this object -- " + imp.ObjectRoot.name);
                return null;
            }

            
        }
        #endregion

	    #region Parsing

	    private static GameObject[] ParseOwnership(GameObject rootObject, string ownership)
	    {

            List< GameObject > objectOwners = new List<GameObject>();

	        if (ownership.Equals(RootOwner))
	        {
	            objectOwners.Add(rootObject);

            }
	        else if (ownership.Equals(TriggersOwner))
	        {
	            Collider[] trigs = rootObject.GetComponentsInChildren<Collider>(true);
	            objectOwners.AddRange(trigs.Select(t => t.gameObject));
	        }
	        else if (ownership.Equals(CollidersOwner))
	        {
	            Collider[] cols = rootObject.GetComponentsInChildren<Collider>(true);
	            objectOwners.AddRange(cols.Select(t => t.gameObject));
            }
	        else if (ownership.Equals(RendererOwner))
	        {
	            Renderer[] rends = rootObject.GetComponentsInChildren<Renderer>(true);
	            objectOwners.AddRange(rends.Select(t => t.gameObject));
            }
	        else
	        {
                //NEEDS TO BE REWORKED FROM SCRATCH https://jack-vanlightly.com/blog/2016/2/3/creating-a-simple-tokenizer-lexer-in-c
                string[] tokens = ownership.Split(parsingDelemiter);
	            string owner = ownership;

                if (tokens.Length > 1)
                {
                    owner = tokens[1];
                    bool negate = false;
                    bool all= false;
                    bool contains = false;

                    for (int i = 0; i < tokens[0].Length; i++)
                    {
                        char token = tokens[0][i];
                        switch (token)
                        {
                            case AutoConfigurator.not:
                                negate = !negate;
                                break;
                            case AutoConfigurator.all:
                                all = true;
                                break;
                            case AutoConfigurator.contains:
                                contains = true;
                                break;
                                
                        }
                    }
                    if (negate)
                    {
                        if (all)
                        {
                            if (contains)
                            {
                                objectOwners.AddRange(rootObject.transform.FindInnerChildsNotContains(owner));
                            }
                            else
                            {
                                objectOwners.AddRange(rootObject.transform.FindInnerChildsNot(owner));
                            }
                        }
                        else
                        {
                            if (contains)
                            {
                                objectOwners.Add(rootObject.transform.FindInnerChildNotContains(owner));
                            }
                            else
                            {
                                objectOwners.Add(rootObject.transform.FindInnerChildNot(owner));
                            }
                        }
                    }
                    else
                    {
                        if (all)
                        {
                            if (contains)
                            {
                                objectOwners.AddRange(rootObject.transform.FindInnerChildsContains(owner));
                            }
                            else
                            {
                                objectOwners.AddRange(rootObject.transform.FindInnerChilds(owner));
                            }
                        }
                        else
                        {
                            if (contains)
                            {
                                objectOwners.Add(rootObject.transform.FindInnerChildContains(owner));
                            }
                            else
                            {
                                objectOwners.Add(rootObject.transform.FindInnerChild(owner));
                            }
                        }
                    }
                }
	            else
	            {
	                GameObject newOwner = rootObject.transform.FindDeepChild(owner).gameObject;
	                if (newOwner != null)
	                {
	                    objectOwners.Add(newOwner);
	                }
	                else
	                {
	                    Debug.LogError("owner " + owner + " does not exist in " + rootObject.name);
	                }
                }

	            

	        }

	        return objectOwners.ToArray();
	    }


	    #endregion
    }

}
