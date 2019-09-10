using UnityEngine;
using UnityEditor;
using System;
using System.Linq;
using System.IO;
using System.Collections.Generic;
using SimpleJSON2;
using Debug = UnityEngine.Debug;
using UnityEditorInternal;
using Helios;
using Hermes;

/// <summary>
///  For Athenea Exporter 1.24
///  
///  Retrompatibility:
///  > Asset Rename
/// </summary>

namespace Athenea
{

    public class ModelImporter {

		#region IMPORT TYPES
		public const string TYPE_CHARACTER= "Character";
		public const string TYPE_WEAPON= "Weapon";
		public const string TYPE_ANIMATION = "Animation";
		public const string TYPE_ENVIRONMENT = "Environment";
        public const string TYPE_PROP = "Prop";
        public const string TYPE_PIECE = "Piece";
        public const string TYPE_MODULE = "Module";
        #endregion

        #region PROP SUB TYPES
        public const string PROP_DOOR = "DOOR";
		public const string PROP_COVER = "COVER";
		#endregion

		#region PATHS
		//static string rootMotionCharsPath = Path.Combine(Application.dataPath,"ElementSpace/Artworks/Models/RootMotionCharacters/");
		//static string modelPath = Path.Combine(Application.dataPath,"ElementSpace/Artworks/Artmasters/");
		//static string animatorPath = Path.Combine(Application.dataPath,"ElementSpace/AnimationControllers/");
		//static string avatarListPath = Path.Combine(Application.dataPath,"Resources/ArtTools/avatarList.json");

		//static string artMasterRelativePath = "Assets/ElementSpace/Artworks/Artmasters/";

		//const string poolManagerPath = "Assets/ElementSpace/Prefabs/SceneManagers/PoolManager.prefab"; // TODO , change when the poolmanager is reworked.
		//const string avatarsPath = "Assets/ElementSpace/Prefabs/Avatars";
		//const string scnTestName= "SCN_Minimal";
		//const string animatorControllerBipedGeneric = "Assets/ElementSpace/AnimationControllers/AvatarControllerRootMotion_MidCharacter.controller";
		#endregion

		#region GUI
		//static JSONObject avatarSave;
		//static Vector2 modelScrollPosition;
		//private static List<string> modelNamesIncluded = new List<string>();
		//private static Color defaultColor = GUI.backgroundColor;
        #endregion
        //const string duplicatePostfix = "_Edited";


        [MenuItem("Assets/Debug/List Variables")]
        static void ListAllVariableMembers()
        {
            SkinnedMeshRenderer smr = (Selection.activeObject as GameObject).GetComponent<SkinnedMeshRenderer>();
            var props = smr.GetType().GetProperties();
            foreach (var prop in props)
            {

                Debug.Log(prop);
            }
        }

        [MenuItem("Assets/Debug/List Animation Variables")]
        static void AnimationVariables()
        {
            UnityEngine.Object[] objs = AssetDatabase.LoadAllAssetsAtPath(AssetDatabase.GetAssetPath(Selection.activeObject)).Where(x => (x is AnimationClip && !x.name.Contains("__preview__"))).ToArray();
            foreach (AnimationClip src in objs)
            {
                EditorCurveBinding[] curveDatas = AnimationUtility.GetCurveBindings(src);
                foreach (var curveData in curveDatas) {
                    Debug.Log(curveData.path + ":" + curveData.propertyName);
                }
            }
            
        }

        [MenuItem("Assets/Debug/Unlock ReadOnly Animation")]
        static void CopyClip()
        {
            //ImportUtilities.BlendShapeClipProcess(Selection.activeObject);
        }








        [MenuItem("Assets/Debug/Show Debug")]
        public static void ShowAssetPath()
        {

            //var test = GameMaterials.GetListGameMaterials();
            //Debug.Log(test);
            //UnityEngine.Object[] objs = AssetDatabase.LoadAllAssetsAtPath(AssetDatabase.GetAssetPath(Selection.activeObject));//.Where( x => (x is AnimationClip && !x.name.Contains("__preview__"))).ToArray();

            //UnityEditor.Animations.AnimatorController.CreateAnimatorControllerAtPath (AssetDatabase.GetAssetPath(Selection.activeObject) + "/" + "ASD" + ".overrideController");
            /*for(int i = 0; i < objs.Length; i++){
				UnityEditor.MonoScript a = objs[i] as UnityEditor.MonoScript;
				Debug.Log(objs[i].name + " __ " + UnityEditor.Unsupported.GetLocalIdentifierInFile(a.GetInstanceID()));

			}*/
            //Type t = (Selection.activeObject as UnityEditor.MonoScript).GetClass();
            //ElementSpace.AbilityButtonLinker a = new AbilityButtonLinker ();
            //Debug.Log ( t.AssemblyQualifiedName);

            //Apolo.ExportLogs.ExportLog eLog = new Apolo.ExportLogs.ExportLog();
            //eLog.user = "toOverWrite";
            //eLog.action = "toOverWrite";
            //eLog.command = "ModelImport";
            //eLog.filename = "ThisOne";
            //eLog.objects = new Apolo.ExportLogs.ExportData[] { new Apolo.ExportLogs.ExportData(name: "oName",exportType: "Piece",exportSubType:"Horizontal") };
            //Apolo.ExportLogs.CreateLogExport(eLog);
            /*if (objs [0] is GameObject) {
				GameObject go = objs [0] as GameObject;
				Animator a = go.GetComponent<Animator> ();
				//Debug.Log (a.runtimeAnimatorController);
				if (a != null) {

					AnimatorOverrideController aoc = new AnimatorOverrideController ();

					aoc.name = "DD";
					aoc.runtimeAnimatorController = AssetDatabase.LoadAssetAtPath<AnimatorController> ("Assets/TEST.controller");
					AnimationClipPair[] cls = new AnimationClipPair[1];
					cls [0] = new AnimationClipPair ();
					cls [0].originalClip = new AnimationClip ();
					cls [0].overrideClip = new AnimationClip ();
					cls [0].overrideClip.name = "AAASDDD";
					aoc.clips = cls;

					a.runtimeAnimatorController = aoc;
				}
			}*/
        }

        [MenuItem("Assets/Pantheon/Athenea/Force Step 2", validate = true)]
        public static bool IsValidToProcess()
        {
            for (int i = 0; i < Selection.objects.Length; i++)
            {
                if (!RawModelImporter.ValidateReimportObject(Selection.objects[i]))
                    return false;
            }
            return true;
        }

        [MenuItem("Assets/Pantheon/Athenea/Force Step 2", validate = false)]
        public static void ForceProcess()
        {
            for (int i = 0; i < Selection.objects.Length; i++)
            {
                ForceProcess(Selection.objects[i]);
            }
        }

        private static void ForceProcess(UnityEngine.Object activeObject)
        {
            AssetImporter assetImporter = AssetImporter.GetAtPath(AssetDatabase.GetAssetPath(activeObject));
            UnityEditor.ModelImporter modelImporter = assetImporter as UnityEditor.ModelImporter;
            //string importedAssetPath = modelImporter.assetPath.Replace("Assets", "");
            string modelFolderPath = modelImporter.assetPath.Remove(modelImporter.assetPath.LastIndexOf('/'), modelImporter.assetPath.Length - modelImporter.assetPath.LastIndexOf('/'));
            string assetName = Path.GetFileNameWithoutExtension(modelImporter.assetPath);

            string[] pendingFiles = new string[1];
            pendingFiles[0] = Application.dataPath.Replace("Assets", "") + modelFolderPath + "/" + assetName + ".pending";
            RawModel[] models = CreateRawModelFromPending(pendingFiles);

            RawModel rawModel = models[0];
            try
            {

                if (ProcessObjects(rawModel))
                {
                    HermesLogger.Log("Processed FBX  " + rawModel.fbxName);
                    File.Delete(rawModel.pendingFile);
                    ExportLogs.ExportData[] exportedObjectDatas = new ExportLogs.ExportData[rawModel.objectData.Count];
                    for (int j = 0; j < rawModel.objectData.Count; j++)
                    {
                        exportedObjectDatas[j] = new ExportLogs.ExportData();

                        JSONObject importedObjectData = rawModel.objectData[j].AsObject;

                        string objectType = importedObjectData["type"].Value;
                        string objectSubType = importedObjectData["subType"].Value;
                        string objectName = importedObjectData["name"].Value;

                        exportedObjectDatas[j].name = objectName;
                        exportedObjectDatas[j].exportType = objectType;
                        exportedObjectDatas[j].exportSubType = objectSubType;
                    }
                    ExportLogs.ExportLog expLog = new ExportLogs.ExportLog();
                    expLog.filename = rawModel.fbxName;
                    expLog.command = "CreateAvatarFromPendingFiles";
                    expLog.objects = exportedObjectDatas;
                    ExportLogs.CreateLogExport(expLog);
                }
            }
            catch (Exception e)
            {
                //CLEAR PROGRESS BAR IF ERROR ENCOUNTERED;
                EditorUtility.ClearProgressBar();

                string errmorMsgSimple = "Cannot create prefab for " + rawModel.fbxPath;
                string errorMsgFull = errmorMsgSimple + "\n\n ----EXCEPTION : " + e.ToString();
                Debug.LogError(errorMsgFull);
                ErrorLogs.ErrorLog errLog = new ErrorLogs.ErrorLog();
                errLog.filename = rawModel.fbxName;
                errLog.level = "CRASH";
                errLog.errorMessage = errorMsgFull;
                errLog.errorCode = 100;
                ErrorLogs.CreateLogError(errLog);

                EditorUtility.DisplayDialog("Athenea Step 2 Error", errmorMsgSimple, "OK");
                //AteneaLogger.AddErrorToCache(errorMsg);
            }
        }
 
        [MenuItem ("Tools/Artists/Debug/Athenea Step 2")]
		public static void CreateAvatarFromPendingFiles(){
			HermesLogger.Log("-------------STARTING AVATAR CREATION PROCESS-------------");
			HermesLogger.Log("Loading all pending FBX");

			string[] pendingFiles = new string[0];
			try{
				pendingFiles = Directory.GetFiles(Pantheon.PantheonConfig.Local_Artmasters_Path,"*.pending",SearchOption.AllDirectories);	
			}catch(Exception e){
				HermesLogger.Log(e.Message);
			}


            RawModel[] models = CreateRawModelFromPending(pendingFiles);


            HermesLogger.Log("RawModels Created.");

            
			if(pendingFiles.Length > 0){
           
                for (int i = 0; i< models.Length; i++){
                    RawModel rawModel = models[i];
                    


                    
					try{
						if (ProcessObjects(rawModel)){
                            HermesLogger.Log("Processed FBX  "+rawModel.fbxName);
                            File.Delete(rawModel.pendingFile);
                            ExportLogs.ExportData[] exportedObjectDatas = new ExportLogs.ExportData[rawModel.objectData.Count];
                            for (int j = 0; j < rawModel.objectData.Count; j++) {
                                exportedObjectDatas[j] = new ExportLogs.ExportData();

                                JSONObject importedObjectData = rawModel.objectData[j].AsObject;

                                string objectType = importedObjectData["type"].Value;
                                string objectSubType = importedObjectData["subType"].Value;
                                string objectName = importedObjectData["name"].Value;

                                exportedObjectDatas[j].name = objectName;
                                exportedObjectDatas[j].exportType = objectType;
                                exportedObjectDatas[j].exportSubType = objectSubType;
                            }
                            ExportLogs.ExportLog expLog = new ExportLogs.ExportLog();
                            expLog.filename = rawModel.fbxName;
                            expLog.command = "CreateAvatarFromPendingFiles";
                            expLog.objects = exportedObjectDatas;
                            ExportLogs.CreateLogExport(expLog);
                        }
					}catch(Exception e){
                        string errorMsg = "Cannot create prefab for " + rawModel.fbxPath + "\n\n ----EXCEPTION : " + e.ToString();
                        Debug.LogError(errorMsg);
                        ErrorLogs.ErrorLog errLog = new ErrorLogs.ErrorLog();
                        errLog.filename = rawModel.fbxName;
                        errLog.level = "CRASH";
                        errLog.errorMessage = errorMsg;
                        errLog.errorCode = 100;
                        //AteneaLogger.AddErrorToCache(errorMsg);
                    }
				}
			}else{
				HermesLogger.Log("No Prefab Created, not a single fbx.pending file was found.");
			}
			HermesLogger.FlushErrors ();
            EditorUtility.ClearProgressBar();
		}

	    public static RawModel[] CreateRawModelFromPending(string[] pendingFiles)
        {
            RawModel[] models = new RawModel[pendingFiles.Length];
            for (int i = 0; i < models.Length; i++)
            {
                try
                {
                    models[i] = new RawModel();
                    models[i].pendingFile = pendingFiles[i];

                    string fileName = Path.GetFileNameWithoutExtension(pendingFiles[i]);
                    //Debug.Log(Directory.GetParent(pendingFiles[i]).GetFiles(fileName+".jsonMeta")[0]);
                    JSONObject jsonData = JSONObject.Parse(File.ReadAllText(Directory.GetParent(pendingFiles[i]).GetFiles(fileName + ".jsonMeta")[0].FullName.Replace("\\", "/"))).AsObject;

                    models[i].objectData = jsonData["objects"].AsArray;
                    models[i].materialsData = jsonData["materials"].AsArray;

                    string fbxPath = Directory.GetParent(pendingFiles[i]).GetFiles(fileName + ".fbx")[0].FullName.Replace("\\", "/");
                    //Debug.Log(Directory.GetParent(pendingFiles[i]).GetFiles("*.fbx")[0]);
                    //Debug.LogError(Directory.GetParent(pendingFiles[i]).GetFiles("*.fbx")[0].FullName);
                    models[i].relativeDirectory = "Assets" + Directory.GetParent(pendingFiles[i]).FullName.Replace("\\", "/").Replace(Application.dataPath, "");
                    models[i].fbxPath = "Assets" + fbxPath.Replace(Application.dataPath, "");
                    models[i].fbxName = Path.GetFileNameWithoutExtension(fbxPath);

                }
                catch (Exception e)
                {
                    HermesLogger.Log(e.Message);

                }
            }
            return models;
        }


        public static bool ProcessObjects(RawModel model){
			EditorUtility.DisplayProgressBar("Creating Prefab","Loading Fbx",0);
			HermesLogger.Log("Loading Fbx " + model.fbxPath);
            JSONArray importedObjects = model.objectData;
            JSONArray importedMaterials = model.materialsData;
            //JSONArray materialData = model.materialsData;

            //importData["objects"].AsArray;

            for(int i = 0; i < importedObjects.Count; i++)
            {
                //JSONClass objectData = model.objectData;
                JSONObject importedObjectData = importedObjects[i].AsObject;
                ProcessObject(model, importedObjectData, importedMaterials);

            }

            AssetDatabase.SaveAssets();
			EditorUtility.ClearProgressBar();
			HermesLogger.Log("Refreshing AssetDataBase");
			AssetDatabase.Refresh();
			return true;
		}

        private static void ProcessObject(RawModel model, JSONObject importedObjectData, JSONArray importedMaterials)
        {
            UnityEngine.Object fbxGo = AssetDatabase.LoadAssetAtPath<UnityEngine.Object>(model.fbxPath); //TODO LOAD THE OBJECT TO SPAWN NO THE ENTIRE FBX
            GameObject fbxInstance = (GameObject)PrefabUtility.InstantiatePrefab(fbxGo);

            

            string objectType = importedObjectData["type"].Value;
            string objectSubType = importedObjectData["subType"].Value;
            string objectName = importedObjectData["name"].Value;


            //Retrocompatibility ---------
            GameObject OLD_oldPrefab = (AssetDatabase.LoadAssetAtPath<GameObject>(model.relativeDirectory + "/" + objectType + "_" + objectName + ".prefab"));
            if (OLD_oldPrefab != null)
            {
                AssetDatabase.RenameAsset(model.relativeDirectory + "/" + objectType + "_" + objectName + ".prefab", objectName + ".prefab");
            }
            //Retrocompatibility ---------



            GameObject oldPrefab = (AssetDatabase.LoadAssetAtPath<GameObject>(model.relativeDirectory + "/" + objectName + ".prefab"));
            if (oldPrefab != null)
            {
                GameObject newRoot = PrefabUtility.InstantiatePrefab(oldPrefab) as GameObject;
                int cc = newRoot.transform.childCount;

                for (int j = cc - 1; j >= 0; j--)
                {
                    //Debug.Log ("DELETING " + i);
                    GameObject.DestroyImmediate(newRoot.transform.GetChild(j).gameObject);
                }

                Component[] oldComponents = newRoot.GetComponents<Component>().Where(c =>
                !(c is Transform) &&
                !(c is Animator) &&
                !(c is MeshFilter) &&
                !(c is MeshRenderer)).OrderByDescending(c => c.CanDestroy()).ToArray();

                for (int j = 0; j < oldComponents.Length; j++)
                {
                    GameObject.DestroyImmediate(oldComponents[j]);
                }

                //int compIndex = 0;
                //while (oldComponents.All(c => c != null)) {
                //    compIndex++;
                //    if (oldComponents[compIndex].CanDestroy())
                //    {
                //        GameObject.DestroyImmediate(oldComponents[compIndex]);
                //        compIndex--;
                //    }
                //}
                //for (int j = 0; j < oldComponents.Length; j++) {
                //    if (!(oldComponents [j] is Transform) && !(oldComponents [j] is GameObject) && !(oldComponents [j] is Animator) && !(oldComponents [j] is MeshFilter) && !(oldComponents [j] is MeshRenderer)) {
                //        GameObject.DestroyImmediate(oldComponents[j]);
                //    }
                //}

                //CHECK IF THE FBXINSTANCE HAS A MESH RENDERER AND MESH FILTER IN ROOT, IF NOT, THEN REMOVE THE
                //MESH RENDERER AND FILTER FROM THE OLD PREFAB
                if (fbxInstance.GetComponent<Renderer>() != null &&
                fbxInstance.GetComponent<MeshFilter>() != null)
                {
                    //CHECK IF THE NEW ROOT ALSO HAS A MESHRENDERER, TO AVOID NULL REFERENCES
                    if (newRoot.GetComponent<Renderer>() != null &&
                        newRoot.GetComponent<MeshFilter>() != null)
                    {
                        if (ComponentUtility.CopyComponent(fbxInstance.GetComponent<Renderer>()))
                            ComponentUtility.PasteComponentValues(newRoot.GetComponent<Renderer>());
                        if (ComponentUtility.CopyComponent(fbxInstance.GetComponent<MeshFilter>()))
                            ComponentUtility.PasteComponentValues(newRoot.GetComponent<MeshFilter>());
                    }

                }
                else
                {
                    //IF THE FBX INSTANCE DOESN'T HAVE A MESH RENDERER OR MESH FILTER THEN REMOVE IT FROM THE OLDPREFAB
                    GameObject.DestroyImmediate(newRoot.GetComponent<Renderer>());
                    GameObject.DestroyImmediate(newRoot.GetComponent<MeshFilter>());
                }


                Vector3 oldPrefabPos = newRoot.transform.position;
                Quaternion oldPrefabRot = newRoot.transform.rotation;

                //REPOSITION BEFORE REPARENTING
                newRoot.transform.position = fbxInstance.transform.position;
                newRoot.transform.rotation = fbxInstance.transform.rotation;

                cc = fbxInstance.transform.childCount;
                for (int j = 0; j < cc; j++)
                {
                    fbxInstance.transform.GetChild(0).SetParent(newRoot.transform);
                }
                GameObject.DestroyImmediate(fbxInstance);
                fbxInstance = newRoot;
                fbxInstance.name = fbxGo.name;

                // APPLY OLD TRANSFORMS BACK
                fbxInstance.transform.rotation = oldPrefabRot;
                fbxInstance.transform.position = oldPrefabPos;
            }
            //Debug.LogError(PrefabUtility.GetPrefabParent(fbxInstance));

            if (fbxInstance.GetComponent<MeshFilter>() != null) fbxInstance.transform.name = fbxInstance.GetComponent<MeshFilter>().sharedMesh.name;

            JSONObject extraData = importedObjectData["extraData"].AsObject;
            ImportedObject importedObject = new ImportedGeneric(objectName, model.relativeDirectory, model.fbxPath, fbxInstance, objectType, objectSubType, extraData); ;
            importedObject.PreProcessObject();



            JSONArray meshesArray = importedObjectData["meshes"].AsArray;
            for (int j = 0; j < meshesArray.Count; j++)
            {
                JSONObject mesh = meshesArray[j].AsObject;
                Transform meshGO = fbxInstance.transform.FindDeepChild(mesh["meshName"].Value);
                //Debug.Log(mesh["meshName"].Value);
                //Debug.Log("-----" + fbxInstance.name);
                if (meshGO)
                {
                    Renderer ren = meshGO.GetComponent<Renderer>();
                    JSONArray materialIds = mesh["materialIds"].AsArray;
                    Material[] mats = new Material[materialIds.Count];
                    for (int k = 0; k < materialIds.Count; k++)
                    {
                        JSONObject materialIdItem = materialIds[k].AsObject;
                        //int o = materialIdItem["materialId"].AsInt;
                        //long l = (long)materialIdItem["materialId"].AsDouble;
                        string materialName = ShaderDataDigest.GetMaterialNameByID(importedMaterials, materialIdItem["materialId"].Value);
                        var matUFile = ImportUtilities.FindFileInParents<Material>(materialName + ".mat", model.relativeDirectory, "/Materials");


                        Material mat = matUFile.file;
                        if (mat)
                        {
                            mats[k] = mat;
                        }
                        else
                        {
                            Debug.LogError(materialName + " NOT FOUND");
                        }

                    }


                    if (ren != null)
                    {
                        ren.sharedMaterials = mats;
                    }
                    else
                    {
                        for (int k = 0; k < meshGO.transform.childCount; k++)
                        {
                            Transform dividedMeshPart = meshGO.transform.GetChild(k);
                            if (dividedMeshPart.name.Contains("MeshPart"))
                            {
                                dividedMeshPart.GetComponent<Renderer>().sharedMaterials = mats;
                            }
                        }
                    }

                }
                else
                {
                    HermesLogger.Log(mesh["meshName"].Value + " NOT FOUND ON HIERARCHY");
                }

            }


            fbxInstance.name = objectName;

            if (oldPrefab != null)
            {
                PrefabUtility.ReplacePrefab(fbxInstance, oldPrefab, ReplacePrefabOptions.ReplaceNameBased);
            }
            else
            {
                PrefabUtility.CreatePrefab(model.relativeDirectory + "/" + objectName + ".prefab", fbxInstance);
            }

            importedObject.PostProcessObject();

            GameObject.DestroyImmediate(fbxInstance);
        }

        /*[MenuItem ("Tools/Artists/Fbx Importer")]
    static void Init () {

        // Get existing open window or if none, make a new one:

        RefreshModels();
        Window.Show();
    }

    void OnGUI () {
        GUILayout.BeginVertical();

        GUILayout.BeginHorizontal();
        GUILayout.Label("Choose a model");
        if(GUILayout.Button("Refresh")){
            RefreshModels();
        }
        GUILayout.EndHorizontal();

        GUILayout.Space(25);
        modelScrollPosition = GUILayout.BeginScrollView(modelScrollPosition);
        GUILayout.BeginVertical();
        for(int i = 0; i< models.Length; i++){
            GUILayout.BeginHorizontal();
            RawModel rawModel = models[i];
            //GUILayout.Label(rawModel.friendlyName);

            if(modelNamesIncluded.Contains(rawModel.friendlyName)){
                GUI.backgroundColor = Color.red;
                if(GUILayout.Button("Remove Avatar - " + rawModel.friendlyName,GUILayout.Width(350))){
                    RemoveAvatar(rawModel);
                    return;
                }
                GUI.backgroundColor = defaultColor;
            }else{
                GUI.backgroundColor = Color.green;
                if(GUILayout.Button("Create Avatar- " + rawModel.friendlyName,GUILayout.Width(350))){
                    CreatePrefab(rawModel);
                    return;
                }	
                GUI.backgroundColor = defaultColor;
            }

            GUILayout.EndHorizontal();
        }
        GUILayout.EndScrollView();
        GUILayout.EndVertical();

        GUILayout.Space(25);
        GUILayout.BeginHorizontal();

        if(GUILayout.Button("Test")){
            TestAvatars();
        }
        GUILayout.EndHorizontal();

        GUILayout.EndVertical();
    }

    static void TestAvatars(){
        EditorSceneManager.OpenScene(scnTestName);
        EditorApplication.isPlaying = true;
    }

    static void RefreshModels(){
        string[] modelFiles = new string[0];
        try{
            modelFiles = Directory.GetFiles(rootMotionCharsPath,"*.fbx",SearchOption.AllDirectories);	
        }catch(Exception e){
            AteneaLogger.Log(e.Message);
        }

    models = new RawModel[modelFiles.Length];
    for(int i = 0; i< models.Length; i++){
        RawModel newRawModel = new RawModel();
        newRawModel.fbxPath = "Assets"+modelFiles[i].Replace(Application.dataPath,"");
        newRawModel.friendlyName = Path.GetFileNameWithoutExtension(modelFiles[i]);

        models[i] =newRawModel;
    }
    if(avatarSave == null){
        if(File.Exists(avatarListPath)){
            avatarSave = JSONClass.LoadFromFile(avatarListPath).AsObject;
            foreach(JSONNode node in avatarSave["avatarList"].AsArray){
                modelNamesIncluded.Add(node["name"].Value);
            }
        }else{
            avatarSave = new JSONClass();
            JSONArray avatarArray = new JSONArray();
            avatarArray.Add("avatarList",avatarArray);
        }
    }
}

        static void RemoveAvatar(RawModel model){

            if(File.Exists(Path.Combine(Application.dataPath,"ElementSpace/Prefabs/Avatars/")+"/avatar_"+model.friendlyName+".prefab")){
                AssetDatabase.DeleteAsset("Assets/ElementSpace/Prefabs/Avatars/"+"avatar_"+model.friendlyName+".prefab");
                //File.Delete(Path.Combine(Application.dataPath,");
            }else{
                Debug.LogWarning("Prefab doesnt exist , trying to delete poolmanager entry...");
            }
            GameObject poolManagerGO = AssetDatabase.LoadAssetAtPath<GameObject>(poolManagerPath);
            if(poolManagerGO != null ){
                EditorUtility.SetDirty(poolManagerGO);
                PoolManager poolManager = poolManagerGO.GetComponent<PoolManager>();
                GameObjectPoolData oldData = poolManager.poolDatas.FirstOrDefault( x => x != null && x.name.Equals(model.friendlyName));
                if(oldData != null){
                    poolManager.poolDatas = poolManager.poolDatas.Where(x => (x != null && !x.name.Equals(model.friendlyName))).ToArray();
                    AssetDatabase.SaveAssets();
                }else{
                    Debug.LogWarning("PoolManager reference doesnt exist.");
                }
            }


            JSONClass avatarItem = new JSONClass();
            avatarItem.Add("name", model.friendlyName);
            avatarItem.Add("path", model.fbxPath);
            avatarSave["avatarList"].AsArray.Remove(modelNamesIncluded.IndexOf(model.friendlyName));
            modelNamesIncluded.Remove(model.friendlyName);
            avatarSave.SaveToFile(avatarListPath);


            AssetDatabase.Refresh();
        }*/



        /*GameObject oldPrefabInstance = GameObject.Instantiate(oldPrefab);

            int cc = oldPrefabInstance.transform.childCount;

            for(int i = cc-1; i >= 0; i--){
                DestroyImmediate(oldPrefabInstance.transform.GetChild(0).gameObject);
            }
            for (int i = 0; i < fbxInstance.transform.childCount; i++) {
                fbxInstance.transform.GetChild (0).SetParent (oldPrefabInstance.transform);
                Debug.Log (i);
            }
            Component[] newComponents = fbxInstance.GetComponents<Component> ();
            Component[] oldComponents = oldPrefabInstance.GetComponents<Component> ();

            for (int i = 0; i < oldComponents.Length; i++) {
                Debug.Log (oldComponents [i]);
                if (!(oldComponents [i] is Transform) && !(oldComponents [i] is GameObject)) {
                    Debug.Log ("DELETE!!! " +oldComponents [i]);
                    DestroyImmediate (oldComponents [i]);
                }
            }

            for (int i = 0; i < newComponents.Length; i++) {
                if (ComponentUtility.CopyComponent (newComponents [i])) {
                    ComponentUtility.PasteComponentAsNew (oldPrefabInstance);
                }
            }*/


        /*EditorUtility.DisplayProgressBar("Creating Avatar","Updating PoolManager",0.75f);
        Log("Updating PoolManager");
        GameObject poolManagerGO = AssetDatabase.LoadAssetAtPath<GameObject>(poolManagerPath);
        if(poolManagerGO != null ){
            EditorUtility.SetDirty(poolManagerGO);
            PoolManager poolManager = poolManagerGO.GetComponent<PoolManager>();
            GameObjectPoolData oldData = poolManager.poolDatas.FirstOrDefault( x => x != null && x.name.Equals(model.friendlyName));


            if(oldData == null){
                GameObjectPoolData gop = new GameObjectPoolData();
                gop.prefab = avatarPrefab;
                gop.name = model.friendlyName;
                gop.defaultPoolCount = 10;
                gop.defaultStoragePosition = new Vector3(10000,10000,10000);
                gop.keepActive = false;
                gop.spawnBehaviour = PoolSpawnBehavior.AddNew;
                GameObjectPoolData[] poolDatas = new GameObjectPoolData[poolManager.poolDatas.Length+1];
                Array.Copy(poolManager.poolDatas,poolDatas,poolManager.poolDatas.Length);
                poolDatas[poolDatas.Length-1] = gop;
                poolManager.poolDatas = poolDatas;

                JSONClass avatarItem = new JSONClass();
                avatarItem.Add("name", model.friendlyName);
                avatarItem.Add("path", model.fbxPath);
                avatarSave["avatarList"].AsArray.Add(avatarItem);
                modelNamesIncluded.Add(model.friendlyName);
                avatarSave.SaveToFile(avatarListPath);
            }else{
                Debug.LogWarning("This avatar is already in the poolManager, re-wiring");
                oldData.prefab = avatarPrefab;
                oldData.defaultPoolCount = 10;
                oldData.defaultStoragePosition = new Vector3(10000,10000,10000);
                oldData.keepActive = false;
                oldData.spawnBehaviour = PoolSpawnBehavior.AddNew;
            }
        }*/




        //		static void ConfigureAvatar(ElementSpace.BipedController bipedController, RigTypes rigType){
        //            bipedController.SetupAvatar(rigType);
        //
        //            ElementSpaceRagdollBuilder.CreateRagdoll(bipedController.gameObject);
        //            /*
        //            RagdollBuilder builder = ScriptableObject.CreateInstance<RagdollBuilder>();
        //            if (builder != null)
        //            {
        //                FullBodyBipedIK ik = bipedController.GetComponent<FullBodyBipedIK>();
        //                builder.CreateRagdollUsingIKReferences(ik);
        //            } else
        //            {1
        //                Debug.LogError("Failed to create ragdoll wizzard");
        //            }*/
        //
        //            bipedController.PostSetup();
        //        }




    }


}
