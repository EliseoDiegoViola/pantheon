using UnityEngine;
using UnityEditor;
using System.Collections;
using System.Collections.Generic;
using System;
using System.Linq;
using System.IO;
using SimpleJSON2;
using System.Security.Cryptography;
using System.Text;
using Helios;
using Hermes;

namespace Athenea
{

    //EXPLORE SearchAndRemapMaterials
    public class RawModelImporter : AssetPostprocessor {

		class TextureAsset{
			public string texName;
			public string relativePath;
			public bool used;

            public TextureAsset(){
                texName = "";
				relativePath = "";
				used = false;
            }
		}

		class MaterialAsset{
			public string relativePath;
			public string matName;
			public bool used;

			public MaterialAsset (){
				matName = "";
				used = false;
				relativePath = "";
			}

		}
         
		const float ANIM_FPS = 30;
        //const string MATERIAL_POOL_PATH = "Assets/ElementSpace/Artworks/ArtMasters/Materials";
        //const string TEXTURE_POOL_PATH = "Assets/ElementSpace/Artworks/ArtMasters/Textures/";

        //		static void OnPostprocessAllAssets(string[] importedAssets, string[] deletedAssets, string[] movedAssets, string[] movedFromAssetPaths)
        //		{
        //			foreach (string str in importedAssets)
        //			{
        //				Debug.Log("Reimported Asset: " + str);
        //			}
        //			foreach (string str in deletedAssets)
        //			{
        //				Debug.Log("Deleted Asset: " + str);
        //			}
        //
        //			for (int i = 0; i < movedAssets.Length; i++)
        //			{
        //				Debug.Log("Moved Asset: " + movedAssets[i] + " from: " + movedFromAssetPaths[i]);
        //			}
        //			AssetDatabase.Refresh ();
        //		}



        void OnPreprocessModel()
        {

            UnityEditor.ModelImporter modelImporter = assetImporter as UnityEditor.ModelImporter;

            string importedAssetPath = modelImporter.assetPath.Replace("Assets", "");

            string modelFolderPath = modelImporter.assetPath.Remove(modelImporter.assetPath.LastIndexOf('/'), modelImporter.assetPath.Length - modelImporter.assetPath.LastIndexOf('/'));
            string[] files = Directory.GetFiles(Application.dataPath.Replace("Assets", "") + modelFolderPath + "/", Path.GetFileNameWithoutExtension(modelImporter.assetPath) + ".jsonMeta");

            if (files.Length >= 1)
            {
                string jsonMetaPath = files[0];

                HermesLogger.Log("-------------TRYING TO PREPROCESS-------------");
                HermesLogger.Log("-------------Processing (Character, Environment, Prop, Weapon, Piece)");

                JSONObject modelData = JSON.Parse(File.ReadAllText(jsonMetaPath)).AsObject;

                HermesLogger.Log("Processing model : " + importedAssetPath);

                if (!string.IsNullOrEmpty(modelImporter.userData))
                {
                    JSONObject userData = JSON.Parse(modelImporter.userData).AsObject;
                    if (userData != null)
                    {
                        HermesLogger.Log("-------------MODEL ALREADY IMPORTED, FOUND USER DATA IN META-------------");
                        if (userData["importStatus"]["status"].Value.Equals("DONE"))
                        {
                            string prevMD5 = userData["importStatus"]["md5"].Value;
                            string newMD5 = GetMD5(modelImporter);
                            Debug.Log("Prev: " + prevMD5 + " | New: " + newMD5);
                            if (prevMD5.Equals(newMD5))
                            {
                                HermesLogger.Log("UserData match| Import Already Done");
                                return;
                            }
                        }
                    }
                }

                PreProcessProcedure(modelImporter);                
            }
        }

        void OnPostprocessModel(object o)
        {
            UnityEditor.ModelImporter modelImporter = assetImporter as UnityEditor.ModelImporter;

            string importedAssetPath = modelImporter.assetPath.Replace("Assets","");

            string modelFolderPath = modelImporter.assetPath.Remove(modelImporter.assetPath.LastIndexOf('/'),modelImporter.assetPath.Length-modelImporter.assetPath.LastIndexOf('/'));
            string[] files = Directory.GetFiles(Application.dataPath.Replace("Assets","")+modelFolderPath+"/",Path.GetFileNameWithoutExtension(modelImporter.assetPath) +".jsonMeta");

            if (files.Length >= 1)
            {
                string jsonMetaPath = files[0];

                HermesLogger.Log("-------------TRYING TO POSTPROCESS-------------");
                HermesLogger.Log("-------------Processing (Animations)");

                JSONObject modelData = JSON.Parse(File.ReadAllText(jsonMetaPath)).AsObject;

                HermesLogger.Log("Processing model : " + importedAssetPath);

                if (!string.IsNullOrEmpty(modelImporter.userData))
                {
                    JSONObject userData = JSON.Parse(modelImporter.userData).AsObject;
                    if (userData != null)
                    {
                        HermesLogger.Log("-------------MODEL ALREADY IMPORTED, FOUND USER DATA IN META-------------");                        
                        if (userData["importStatus"]["status"].Value.Equals("DONE"))
                        {
                            string prevMD5 = userData["importStatus"]["md5"].Value;
                            string newMD5 = GetMD5(modelImporter);
                            //Debug.Log("Prev: " + prevMD5 + " | New: " + newMD5);
                            if (prevMD5.Equals(newMD5))
                            {
                                HermesLogger.Log("UserData | Import Already Done");
                                return;
                            }
                        }                        
                    }
                }

                PostProcessProcedure(modelImporter);

                string md5Str = GetMD5(modelImporter);
                JSONObject userDataToWrite = new JSONObject();
                JSONObject importStatusObj = new JSONObject
                    {
                        { "status", new JSONString("DONE") },
                        { "md5", new JSONString(md5Str) }
                    };
                userDataToWrite.Add("importStatus", importStatusObj);

                modelImporter.userData = userDataToWrite.ToString();
            }
        }



        static void PostProcessProcedure(UnityEditor.ModelImporter modelImporter)
        {
            string importedAssetPath = modelImporter.assetPath.Replace("Assets", "");

            string modelFolderPath = modelImporter.assetPath.Remove(modelImporter.assetPath.LastIndexOf('/'), modelImporter.assetPath.Length - modelImporter.assetPath.LastIndexOf('/'));
            string[] files = Directory.GetFiles(Application.dataPath.Replace("Assets", "") + modelFolderPath + "/", Path.GetFileNameWithoutExtension(modelImporter.assetPath) + ".jsonMeta");

            if (files.Length >= 1)
            {


                HermesLogger.Log("-------------POSTPROCESS PROCEDURE-------------");
                HermesLogger.Log("-------------Processing (Animations)");

                string jsonMetaPath = files[0];
                JSONObject modelData = JSON.Parse(File.ReadAllText(jsonMetaPath)).AsObject;

                var objJson = modelData["objects"].AsArray;
                var extraJson = objJson[0].AsObject["extraData"];
                var animsJson = extraJson.AsObject["objectAnimations"];
                var animations = animsJson.AsArray;




                int animationsCount = animations.Count;

                if (animationsCount > 0) {
                    modelImporter.importAnimation = true;
                    modelImporter.resampleCurves = false;
                    modelImporter.generateAnimations = ModelImporterGenerateAnimations.None;
                    modelImporter.animationCompression = ModelImporterAnimationCompression.Off;
                    modelImporter.animationType = ModelImporterAnimationType.Generic;

                    SerializedObject modelImporterObj = new SerializedObject(modelImporter);
                    SerializedProperty rootNodeProperty = modelImporterObj.FindProperty("m_HumanDescription.m_RootMotionBoneName");

                    ModelImporterClipAnimation[] clipAnimations = new ModelImporterClipAnimation[animationsCount];


                    for (int i = 0; i < clipAnimations.Length; i++)
                    {
                        clipAnimations[i] = new ModelImporterClipAnimation();



                        float startFrame = animations[i].AsObject["startFrame"].AsFloat;
                        float lastFrame = animations[i].AsObject["endFrame"].AsFloat;
                        JSONArray events = animations[i].AsObject["events"].AsArray;

                        clipAnimations[i] = new ModelImporterClipAnimation();

                        ModelImporterClipAnimation currentClipAnimation = (modelImporter.clipAnimations != null && i < modelImporter.clipAnimations.Length) ? modelImporter.clipAnimations[i] : (i < modelImporter.defaultClipAnimations.Length) ? modelImporter.defaultClipAnimations[i] : null;

                        if (currentClipAnimation == null)
                        {
                            Debug.LogError("IMPORT ANIMATION " + importedAssetPath + " FAILED , default clip animation is NULL for I= " + i);
                            currentClipAnimation = new ModelImporterClipAnimation();
                            currentClipAnimation.cycleOffset = 0;
                            currentClipAnimation.heightFromFeet = false;
                            currentClipAnimation.heightOffset = 0;
                            currentClipAnimation.keepOriginalOrientation = false;
                            currentClipAnimation.keepOriginalPositionXZ = false;
                            currentClipAnimation.keepOriginalPositionY = false;
                            currentClipAnimation.lockRootHeightY = false;
                            currentClipAnimation.lockRootPositionXZ = false;
                            currentClipAnimation.lockRootRotation = false;
                            currentClipAnimation.loopPose = false;
                            currentClipAnimation.maskSource = null;
                            currentClipAnimation.maskType = ClipAnimationMaskType.CreateFromThisModel;
                            currentClipAnimation.mirror = false;
                            currentClipAnimation.rotationOffset = 0;
                            currentClipAnimation.takeName = "DEFAULT";
                            currentClipAnimation.curves = new ClipAnimationInfoCurve[0];
                            currentClipAnimation.name = "DEFAULT NAME";
                            currentClipAnimation.firstFrame = 0;
                            currentClipAnimation.events = new AnimationEvent[0];
                            currentClipAnimation.lastFrame = 0;
                            currentClipAnimation.loop = false;
                            currentClipAnimation.loopTime = false;
                        }



                        clipAnimations[i].cycleOffset = currentClipAnimation.cycleOffset;
                        //clipAnimations[i].events = modelImporter.defaultClipAnimations[i].events;
                        clipAnimations[i].heightFromFeet = currentClipAnimation.heightFromFeet;
                        clipAnimations[i].heightOffset = currentClipAnimation.heightOffset;
                        clipAnimations[i].keepOriginalOrientation = currentClipAnimation.keepOriginalOrientation;
                        clipAnimations[i].keepOriginalPositionXZ = currentClipAnimation.keepOriginalPositionXZ;
                        clipAnimations[i].keepOriginalPositionY = currentClipAnimation.keepOriginalPositionY;
                        clipAnimations[i].lockRootHeightY = currentClipAnimation.lockRootHeightY;
                        clipAnimations[i].lockRootPositionXZ = currentClipAnimation.lockRootPositionXZ;
                        clipAnimations[i].lockRootRotation = currentClipAnimation.lockRootRotation;
                        clipAnimations[i].loopPose = currentClipAnimation.loopPose;
                        clipAnimations[i].maskSource = currentClipAnimation.maskSource;
                        clipAnimations[i].maskType = currentClipAnimation.maskType;
                        clipAnimations[i].mirror = currentClipAnimation.mirror;
                        clipAnimations[i].rotationOffset = currentClipAnimation.rotationOffset;
                        clipAnimations[i].takeName = currentClipAnimation.takeName;
                        clipAnimations[i].curves = currentClipAnimation.curves;


                        clipAnimations[i].name = animations[i].AsObject["clipName"].Value;
                        clipAnimations[i].takeName = animations[i].AsObject["clipName"].Value;

                        clipAnimations[i].firstFrame = startFrame ;
                        clipAnimations[i].lastFrame = lastFrame;

						//if (clipAnimations[i].firstFrame < 0)
						//{
						//	Debug.LogError("ATHENEA: " + clipAnimations[i].takeName + " first frame is < 0");
						//	clipAnimations[i].firstFrame = 0;
						//}
						//if (clipAnimations[i].lastFrame < 0)
						//{
						//	Debug.LogError("ATHENEA: " + clipAnimations[i].takeName + " last frame is < 0");
						//	clipAnimations[i].lastFrame = 0;
						//}

						clipAnimations[i].loop = animations[i].AsObject["isLoop"].AsBool;
                        clipAnimations[i].loopTime = animations[i].AsObject["isLoop"].AsBool;

                        if (clipAnimations[i].loop)
                        {
                            clipAnimations[i].wrapMode = WrapMode.Loop;
                        }
                        else
                        {
                            clipAnimations[i].wrapMode = WrapMode.Default;
                        }


                        List<AnimationEvent> evs = new List<AnimationEvent>();//clipAnimations[i].events.ToList();

                        var wiseEvents = currentClipAnimation.events.Where((ae) => ae.functionName.Equals("PlayWwiseEvent"));

                        evs.AddRange(wiseEvents);
                        for (int j = 0; j < events.Count; j++)
                        {
                            float keyEvent = events[j].AsObject["keyFrame"].AsFloat;
                            if (keyEvent <= lastFrame && keyEvent >= startFrame)
                            {
                                AnimationEvent ev = new AnimationEvent
                                {
                                    functionName = events[j].AsObject["eventName"].Value,
                                    time = (keyEvent - startFrame) / (lastFrame - startFrame),
                                    floatParameter = 0,
                                    intParameter = 0,
                                    stringParameter = "",
                                    objectReferenceParameter = null
                                };

                                evs.Add(ev);

                            }
                        }
                        clipAnimations[i].events = evs.ToArray();

                        if (animations[i].AsObject["isRootMotion"].AsBool)
                        {
                            modelImporter.motionNodeName = "Root";
                            rootNodeProperty.stringValue = "Root";
                        }
                        else
                        {
                            modelImporter.motionNodeName = "";
                            rootNodeProperty.stringValue = "";
                        }
                    }

                    modelImporterObj.ApplyModifiedPropertiesWithoutUndo();
                    modelImporter.clipAnimations = clipAnimations;
                }

                
                //modelImporter.resampleCurves = false;
                //modelImporter.generateAnimations = ModelImporterGenerateAnimations.None;
                //modelImporter.animationCompression = ModelImporterAnimationCompression.Off;
                //modelImporter.animationType = ModelImporterAnimationType.Generic;

                //SerializedObject modelImporterObj = new SerializedObject(modelImporter);
                //SerializedProperty rootNodeProperty = modelImporterObj.FindProperty("m_HumanDescription.m_RootMotionBoneName");



                //JSONArray animations = modelData["objects"].AsArray[0].AsObject["animations"].AsArray;
                //JSONArray events = modelData["objects"].AsArray[0].AsObject["events"].AsArray;

                //int animationsCount = animations.Count;
                //ModelImporterClipAnimation[] clipAnimations = new ModelImporterClipAnimation[animationsCount];

                    
                    





                HermesLogger.Log("Values Set for : " + importedAssetPath);
                AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);

                //HACK , REMOVE WHEN THE IMPORT IS DATA DRIVEN
                //var typee = modelData["objects"].AsArray[0].AsObject["type"].Value;
                //var stypee = modelData["objects"].AsArray[0].AsObject["subType"].Value;


                //if (typee.Equals(ModelImporter.TYPE_ANIMATION) && stypee.Equals("BlendShape"))
                //{
                //    ImportUtilities.BlendShapeClipProcess(modelImporter);
                //}

            }
        }

        static void PreProcessProcedure(UnityEditor.ModelImporter modelImporter)
        {
            string importedAssetPath = modelImporter.assetPath.Replace("Assets", "");
            string modelFolderPath = modelImporter.assetPath.Remove(modelImporter.assetPath.LastIndexOf('/'), modelImporter.assetPath.Length - modelImporter.assetPath.LastIndexOf('/'));
            string[] files = Directory.GetFiles(Application.dataPath.Replace("Assets", "") + modelFolderPath + "/", Path.GetFileNameWithoutExtension(modelImporter.assetPath) + ".jsonMeta");

            if (files.Length >= 1)
            {
                string jsonMetaPath = files[0];

                HermesLogger.Log("-------------PREPROCESS PROCEDURE-------------");
                HermesLogger.Log("-------------Processing (Character, Environment, Prop, Weapon, Piece)");

                JSONObject modelData = JSON.Parse(File.ReadAllText(jsonMetaPath)).AsObject;

                HermesLogger.Log("Processing model : " + importedAssetPath);

                Debug.Log("Model Type: " + modelData["objects"].AsArray[0].AsObject["type"].Value);
            if (modelData["objects"].AsArray[0].AsObject["type"].Value.Equals(ModelImporter.TYPE_CHARACTER))
            {
                HermesLogger.Log("Processing Character : " + importedAssetPath);

                modelImporter.importMaterials = false;
                modelImporter.importAnimation = false;
                modelImporter.animationType = ModelImporterAnimationType.Generic;
                modelImporter.motionNodeName = "Root";
                SerializedObject modelImporterObj = new SerializedObject(modelImporter);
                SerializedProperty rootNodeProperty = modelImporterObj.FindProperty("m_HumanDescription.m_RootMotionBoneName");
                rootNodeProperty.stringValue = "Root";
                modelImporterObj.ApplyModifiedProperties();
                FetchTexturesData(modelFolderPath, modelData);



            }
            else if (modelData["objects"].AsArray[0].AsObject["type"].Value.Equals(ModelImporter.TYPE_ANIMATION))
            {

                HermesLogger.Log("Processing Animation : " + importedAssetPath);

                modelImporter.importMaterials = false;
                modelImporter.importAnimation = true;
                modelImporter.importAnimatedCustomProperties = true;

            }
            else if (modelData["objects"].AsArray[0].AsObject["type"].Value.Equals(ModelImporter.TYPE_ENVIRONMENT))
            {
                HermesLogger.Log("Processing Environment : " + importedAssetPath);
                modelImporter.importMaterials = false;
                modelImporter.importAnimation = false;
                modelImporter.animationType = ModelImporterAnimationType.None;
                modelImporter.generateSecondaryUV = true;
				modelImporter.isReadable = true;
                FetchTexturesData(modelFolderPath, modelData);
            }
            else if (modelData["objects"].AsArray[0].AsObject["type"].Value.Equals(ModelImporter.TYPE_PROP))
            {
                HermesLogger.Log("Processing Prop : " + importedAssetPath);

                modelImporter.importMaterials = false;
                string propSubType = modelData["sub-type"].Value.ToUpper();

                if (propSubType.Equals(ModelImporter.PROP_DOOR))
                {
                    modelImporter.importAnimation = true;
                    modelImporter.animationType = ModelImporterAnimationType.Generic;
                }
                else if (propSubType.Equals(ModelImporter.PROP_COVER))
                {
                    modelImporter.importAnimation = false;
                    modelImporter.animationType = ModelImporterAnimationType.None;
                }
                modelImporter.importLights = false;
                modelImporter.importCameras = false;
                FetchTexturesData(modelFolderPath, modelData);

            }
            else if (modelData["objects"].AsArray[0].AsObject["type"].Value.Equals(ModelImporter.TYPE_WEAPON))
            {
                HermesLogger.Log("Processing Weapon : " + importedAssetPath);
                modelImporter.importMaterials = false;
                modelImporter.importAnimation = true;
                modelImporter.animationType = ModelImporterAnimationType.Generic;
                FetchTexturesData(modelFolderPath, modelData);


            }
            else if (modelData["objects"].AsArray[0].AsObject["type"].Value.Equals(ModelImporter.TYPE_PIECE))
            {
                HermesLogger.Log("Processing Piece : " + importedAssetPath);
                modelImporter.importMaterials = false;
                modelImporter.importAnimation = false;
                modelImporter.animationType = ModelImporterAnimationType.None;
                modelImporter.generateSecondaryUV = true;
                modelImporter.importLights = false;
                modelImporter.importCameras = false;
                FetchTexturesData(modelFolderPath, modelData);
            }
            else if (modelData["objects"].AsArray[0].AsObject["type"].Value.Equals(ModelImporter.TYPE_MODULE))
            {
                HermesLogger.Log("Processing Piece : " + importedAssetPath);
                modelImporter.importMaterials = false;
                modelImporter.importAnimation = false;
                modelImporter.animationType = ModelImporterAnimationType.None;
                modelImporter.generateSecondaryUV = true;
                modelImporter.importLights = false;
                modelImporter.importCameras = false;
                FetchTexturesData(modelFolderPath, modelData);
            }
                AssetDatabase.SaveAssets();
                Debug.Log("Finished pre process");
            }

        }
        

       [MenuItem("Assets/Pantheon/Athenea/Force Step 1", validate = true)]
        public static bool IsValidToReimport()
        {
            for (int i = 0; i < Selection.objects.Length; i++)
            {
                if (!ValidateReimportObject(Selection.objects[i]))
                    return false;
            }
            return true;
        }

        public static bool ValidateReimportObject(UnityEngine.Object activeObject)
        {
            AssetImporter assetImporter = AssetImporter.GetAtPath(AssetDatabase.GetAssetPath(activeObject));
            UnityEditor.ModelImporter modelImporter = assetImporter as UnityEditor.ModelImporter;
            if (modelImporter == null)
            {
                return false;
            }
            //string importedAssetPath = modelImporter.assetPath.Replace("Assets", "");
            string modelFolderPath = modelImporter.assetPath.Remove(modelImporter.assetPath.LastIndexOf('/'), modelImporter.assetPath.Length - modelImporter.assetPath.LastIndexOf('/'));
            string[] files = Directory.GetFiles(Application.dataPath.Replace("Assets", "") + modelFolderPath + "/", Path.GetFileNameWithoutExtension(modelImporter.assetPath) + ".jsonMeta");

            if (files.Length >= 1)
            {
                string jsonMetaPath = files[0];
                JSONObject modelData = JSON.Parse(File.ReadAllText(jsonMetaPath)).AsObject;
                if (modelData != null)
                {
                    return true;
                }
            }
            return false;
        }

        [MenuItem("Assets/Pantheon/Athenea/Force Step 1", validate =false)]
        public static void ForceReimport()
        {
            for (int i = 0; i < Selection.objects.Length; i++)
            {
                ForceReimport(Selection.objects[i]);
            }            
        }
		[MenuItem("Assets/Force Reimport Animations (Athenea)", validate = false)]
		public static void ForceReimportAnimations()
		{
			for (int i = 0; i < Selection.objects.Length; i++)
			{
				if (Selection.objects[i].name.StartsWith("Mid_") || Selection.objects[i].name.StartsWith("Fem_") || Selection.objects[i].name.StartsWith("Big_"))
					ForceReimport(Selection.objects[i]);

			}
		}
		private static void ForceReimport(UnityEngine.Object activeObject)
        {
            AssetImporter assetImporter = AssetImporter.GetAtPath(AssetDatabase.GetAssetPath(activeObject));
            UnityEditor.ModelImporter modelImporter = assetImporter as UnityEditor.ModelImporter;

            PreProcessProcedure(modelImporter);
            PostProcessProcedure(modelImporter);
			//AssetDatabase.SaveAssets();
			assetImporter.SaveAndReimport();

		}

        string GetMD5(UnityEditor.ModelImporter modelImporter)
        {
            MD5 md5Hash = MD5.Create();
            string modelPath = Application.dataPath.Replace("Assets", "") + modelImporter.assetPath;
            byte[] data = md5Hash.ComputeHash(File.ReadAllBytes(modelPath));
            StringBuilder sBuilder = new StringBuilder(data.Length * 2);
            for (int i = 0; i < data.Length; ++i)
                sBuilder.Append(data[i].ToString("x2"));
            return sBuilder.ToString();
        }

		static void FetchTexturesData(string modelFolderPath, JSONObject modelData ){
            string materialsFolder = "/Materials";
            string texturesFolder = "/Textures";

			ShaderDataDigest.MaterialDigest[] allMaterials = new ShaderDataDigest.MaterialDigest[0];
			MaterialAsset[] matAssets = new MaterialAsset[0];

			try{
				JSONArray materials = modelData["materials"].AsArray;
				allMaterials =  ShaderDataDigest.MaterialDataDigest(materials);


			    if (!AssetDatabase.IsValidFolder(Pantheon.PathsBuilder.ArtmastersPath + materialsFolder))
			    {
			        AssetDatabase.CreateFolder(Pantheon.PathsBuilder.ArtmastersPath, "Materials");
			    }

			    //if (!AssetDatabase.IsValidFolder(modelFolderPath + materialsFolder))
			    //{
			    //    AssetDatabase.CreateFolder(modelFolderPath, "Materials");
			    //}
                
               matAssets = new MaterialAsset[materials.Count];

				HermesLogger.Log("Fetching Materials");
				for(int i = 0; i< matAssets.Length; i++){
					matAssets[i] = new MaterialAsset();
					matAssets[i].matName = materials[i].AsObject["name"].Value;
                    matAssets[i].relativePath = modelFolderPath+materialsFolder+"/"+matAssets[i].matName+".mat";
				}
			}catch(Exception e){
				HermesLogger.Log("Error fetching data ----EXCEPTION : " + e.ToString());
			}



			//try{
				for(int i = 0; i < allMaterials.Length; i++){
					ShaderDataDigest.MaterialDigest matData = allMaterials[i];
                    Debug.Log(matData.materialName);

					if(matAssets.Length > 0 && matAssets.Any(x => x.matName.Equals(matData.materialName))){
						MaterialAsset matAsset = matAssets.First( x => x.matName.Equals(matData.materialName));
						matAsset.used = true;
					}



					Material mat;
					bool newMaterial = false;

                    var materialUFile = ImportUtilities.FindFileInParents<Material>(allMaterials[i].materialName + ".mat", modelFolderPath, materialsFolder); //AssetDatabase.LoadAssetAtPath<Material>(modelFolderPath+materialsFolder+"/"+allMaterials[i].materialName+".mat");
                    mat = materialUFile.file;



				    if (mat == null){
                        
                        newMaterial = true;
                        mat = new Material(Shader.Find(matData.shaderName)){
                            name = allMaterials[i].materialName
                        };
                        materialUFile.path = Pantheon.PathsBuilder.ArtmastersPath + "/Materials/" +allMaterials[i].materialName + ".mat"; //modelFolderPath + materialsFolder + "/" + allMaterials[i].materialName + ".mat";
                        HermesLogger.Log("Creating new material " + mat.name + " in " + materialUFile.path);
                        AssetDatabase.CreateAsset(mat, materialUFile.path);
                        materialUFile.file = AssetDatabase.LoadAssetAtPath<Material>(materialUFile.path);
                    }
                    else{
                        mat.shader = Shader.Find(matData.shaderName);

                        EditorUtility.SetDirty(mat);
					}

                    Shader shader = mat.shader;
					mat.name = matData.materialName; 
					bool useTex = false;
				    string mostInnerFolder = Pantheon.PathsBuilder.ArtmastersPath; // modelFolderPath;

                    foreach (ShaderDataDigest.ShaderProperties prop in matData.shaderProperties){
						if(prop.properyType.Equals("TexEnv")){
							useTex = true;

                            //var texUFile = ImportUtilities.FindFileInParents<Texture2D>(prop.propertyValue,modelFolderPath,texturesFolder);
						    var texUFile = ImportUtilities.FindFileInParents<Texture2D>(prop.propertyValue, Pantheon.PathsBuilder.ArtmastersPath, texturesFolder);
                            Texture2D tex = texUFile.file;

                            if (tex != null){
								mat.SetTexture(prop.propertyName,tex);
								mat.SetColor(prop.propertyName, Color.white);
                                string texParentFolder = texUFile.path.Substring(0, texUFile.path.IndexOf(texturesFolder));
                                mostInnerFolder = mostInnerFolder.Split('/').Length > texParentFolder.Split('/').Length ? mostInnerFolder : texParentFolder;

                            }

                            if (prop.propertyName.Equals("_BumpMap") && !mat.IsKeywordEnabled("_NORMALMAP"))
                                mat.EnableKeyword("_NORMALMAP");
                            if (prop.propertyName.Equals("_EmissionMap") && !mat.IsKeywordEnabled("_EMISSION"))
                                mat.EnableKeyword("_EMISSION");
						    if (prop.propertyName.Equals("_MetallicGlossMap") && !mat.IsKeywordEnabled("_METALLICGLOSSMAP"))
						        mat.EnableKeyword("_METALLICGLOSSMAP");

                        }
                        else if(prop.properyType.Equals("Color") && newMaterial && !useTex){
							string[] colVals = prop.propertyValue.Split('/');
							Color newColor = new Color(
								float.Parse(colVals[0]),
								float.Parse(colVals[1]),
								float.Parse(colVals[2]),
								float.Parse(colVals[3])
							);

							mat.SetColor(prop.propertyName,newColor);
						}else if(prop.properyType.Equals("Float") && newMaterial) //FINISH
                        {

                            string[] colVals = prop.propertyValue.Split('/');
                            Color newColor = new Color(
                                float.Parse(colVals[0]),
                                float.Parse(colVals[1]),
                                float.Parse(colVals[2]),
                                float.Parse(colVals[3])
                            );

                            mat.SetColor(prop.propertyName, newColor);
                        }
                    }
                    HermesLogger.Log("Updating material " + mat.name + " in " + mostInnerFolder+ materialsFolder+"/"+ mat.name+".mat");
                    if (!AssetDatabase.IsValidFolder(mostInnerFolder + materialsFolder))
                    {
                        HermesLogger.Log("Creating Materials Folder in: " + mostInnerFolder);
                        AssetDatabase.CreateFolder(mostInnerFolder, materialsFolder.Replace("/",""));
                    }

                    AssetDatabase.MoveAsset(materialUFile.path, mostInnerFolder + materialsFolder + "/" + mat.name + ".mat");
                    AssetDatabase.SaveAssets();

                    //Upload updated data to server
				    JSONObject gameMaterial = GameMaterials.CollectMaterialData(mat);
				    GameMaterials.GameMaterial serverMaterial = GameMaterials.GetGameMaterialByName_Sync(mat.name);
				    if (!string.IsNullOrEmpty(serverMaterial._id))
				    {
				        GameMaterials.ModifyMaterialData_Sync(serverMaterial._id, gameMaterial.ToString());

				    }

				    
				}
                

			//}catch(Exception e){
				//HermesLogger.Log("Error Creating assets ----EXCEPTION : " + e.ToString());
			//}

//			GeneralCleanUp(matAssets,texAssets);
		}

        static void GeneralCleanUp(MaterialAsset[] matAssets, TextureAsset[] texAssets){
			matAssets.Where( mat => !mat.used).ToList().ForEach( mat => AssetDatabase.DeleteAsset(mat.relativePath));
			texAssets.Where( tex => !tex.used).ToList().ForEach( tex => AssetDatabase.DeleteAsset(tex.relativePath));
		}

        //struct UnityFile<T> where T : UnityEngine.Object
        //{
        //    public T file;
        //    public string path;
        //}

        //static UnityFile<T> FindFileInParents<T>(string fileName, string startDirectory, string subFolder = "") where T : UnityEngine.Object
        //{

        //    string directoryCache = startDirectory;
        //    string searchPatttern = directoryCache + subFolder;
        //    UnityFile<T> uFile = new UnityFile<T>();

        //    T foundFile = AssetDatabase.LoadAssetAtPath<T>(searchPatttern + "/" + fileName);
        //    if (foundFile != null)
        //    {
        //        uFile.file = foundFile;
        //        uFile.path = searchPatttern + "/" + fileName;
        //        return uFile;
        //    }

        //    while ((foundFile == null) && !(GetParentFolder(directoryCache).Equals(directoryCache)))
        //    {
        //        directoryCache = GetParentFolder(directoryCache);
        //        searchPatttern = directoryCache + subFolder;
        //        foundFile = AssetDatabase.LoadAssetAtPath<T>(searchPatttern + "/" + fileName);

        //        if (foundFile != null)
        //        {
        //            uFile.file = foundFile;
        //            uFile.path = searchPatttern + "/" + fileName;
        //            return uFile;
        //        }
        //    }

        //    uFile.file = null;
        //    uFile.path = "";
        //    return uFile;
        //}

        //static string GetParentFolder(string folder)
        //{
        //    int slashIndex = folder.LastIndexOf("/");
        //    folder = slashIndex < 0 ? folder : folder.Remove(slashIndex);
        //    int backslashIndex = folder.LastIndexOf("\\");
        //    folder = backslashIndex < 0 ? folder : folder.Remove(backslashIndex);
        //    return folder;
        //}

    }
}
//                else if (modelData ["objects"].AsArray[0].AsObject["type"].Value.Equals(ModelImporter.TYPE_ANIMATION))
//                {
//					
//                    AteneaLogger.Log("Processing Animation : " + importedAssetPath);
//
//                    modelImporter.importMaterials = false;
//                    modelImporter.importAnimation = true;
//                    modelImporter.resampleCurves = false;
//                    modelImporter.generateAnimations =  ModelImporterGenerateAnimations.None;
//                    modelImporter.animationCompression = ModelImporterAnimationCompression.Off;
//                    modelImporter.animationType = ModelImporterAnimationType.Generic;
//					
//                    SerializedObject modelImporterObj = new SerializedObject(modelImporter);
//                    SerializedProperty rootNodeProperty = modelImporterObj.FindProperty("m_HumanDescription.m_RootMotionBoneName");
//
//
//
//                    JSONArray animations = modelData ["objects"].AsArray[0].AsObject["animations"].AsArray;
//                    JSONArray events = modelData ["objects"].AsArray[0].AsObject["events"].AsArray;
//
//                    int animationsCount = animations.Count;
//                    ModelImporterClipAnimation[] clipAnimations = new ModelImporterClipAnimation[animationsCount];
//
//                    for (int i = 0; i < clipAnimations.Length; i++)
//                    {
//                        clipAnimations[i] = new ModelImporterClipAnimation();
//
//
//
//                        float startFrame = animations[i].AsObject["animStart"].AsFloat;
//
//                        float lastFrame = animations[i].AsObject["animEnd"].AsFloat;
//
//
//                        clipAnimations[i] = new ModelImporterClipAnimation();
//
//                        ModelImporterClipAnimation currentClipAnimation = (modelImporter.clipAnimations != null && i < modelImporter.clipAnimations.Length) ? modelImporter.clipAnimations[i] : (i < modelImporter.defaultClipAnimations.Length) ? modelImporter.defaultClipAnimations[i] : null;
//
//                        if (currentClipAnimation == null)
//                        {
//                            Debug.LogError("IMPORT ANIMATION " + importedAssetPath + " FAILED , default clip animation is NULL for I= " + i);
//                            currentClipAnimation = new ModelImporterClipAnimation();
//                            currentClipAnimation.cycleOffset = 0;
//                            currentClipAnimation.heightFromFeet = false;
//                            currentClipAnimation.heightOffset = 0;
//                            currentClipAnimation.keepOriginalOrientation = false;
//                            currentClipAnimation.keepOriginalPositionXZ = false;
//                            currentClipAnimation.keepOriginalPositionY = false;
//                            currentClipAnimation.lockRootHeightY = false;
//                            currentClipAnimation.lockRootPositionXZ = false;
//                            currentClipAnimation.lockRootRotation = false;
//                            currentClipAnimation.loopPose = false;
//                            currentClipAnimation.maskSource = null ;
//                            currentClipAnimation.maskType = ClipAnimationMaskType.CreateFromThisModel;
//                            currentClipAnimation.mirror = false;
//                            currentClipAnimation.rotationOffset = 0;
//                            currentClipAnimation.takeName = "DEFAULT";
//                            currentClipAnimation.curves = new ClipAnimationInfoCurve[0];
//                            currentClipAnimation.name = "DEFAULT NAME";
//                            currentClipAnimation.firstFrame = 0;
//                            currentClipAnimation.events = new AnimationEvent[0];
//                            currentClipAnimation.lastFrame = 0;
//                            currentClipAnimation.loop = false;
//                            currentClipAnimation.loopTime = false;
//                        }
//
//
//
//                        clipAnimations[i].cycleOffset = currentClipAnimation.cycleOffset;
//                        //clipAnimations[i].events = modelImporter.defaultClipAnimations[i].events;
//                        clipAnimations[i].heightFromFeet = currentClipAnimation.heightFromFeet;
//                        clipAnimations[i].heightOffset = currentClipAnimation.heightOffset;
//                        clipAnimations[i].keepOriginalOrientation = currentClipAnimation.keepOriginalOrientation;
//                        clipAnimations[i].keepOriginalPositionXZ = currentClipAnimation.keepOriginalPositionXZ;
//                        clipAnimations[i].keepOriginalPositionY = currentClipAnimation.keepOriginalPositionY;
//                        clipAnimations[i].lockRootHeightY = currentClipAnimation.lockRootHeightY;
//                        clipAnimations[i].lockRootPositionXZ = currentClipAnimation.lockRootPositionXZ;
//                        clipAnimations[i].lockRootRotation = currentClipAnimation.lockRootRotation;
//                        clipAnimations[i].loopPose = currentClipAnimation.loopPose;
//                        clipAnimations[i].maskSource = currentClipAnimation.maskSource;
//                        clipAnimations[i].maskType = currentClipAnimation.maskType;
//                        clipAnimations[i].mirror = currentClipAnimation.mirror;
//                        clipAnimations[i].rotationOffset = currentClipAnimation.rotationOffset;
//                        clipAnimations[i].takeName = currentClipAnimation.takeName;
//                        clipAnimations[i].curves = currentClipAnimation.curves;
//
//                        //FIXME DONE
//                        /*if (animations [i].AsObject ["animName"].Value.Equals ("MyClip") || string.IsNullOrEmpty (animations [i].AsObject ["animName"].Value)) {
//							string[] splitName = Path.GetFileNameWithoutExtension (modelImporter.assetPath).Split ('@');
//							if (splitName.Length == 2) {
//								clipAnimations [i].name = splitName[splitName.Length-1];
//							} else {
//								clipAnimations[i].name = modelImporter.name;
//							}
//						} else {
//							clipAnimations[i].name = animations[i].AsObject["animName"].Value;
//						}*/
//                        clipAnimations[i].name = animations[i].AsObject["animName"].Value;
//
//
//                        clipAnimations[i].firstFrame = startFrame;
//                        clipAnimations[i].lastFrame = lastFrame;
//                        clipAnimations[i].loop = animations[i].AsObject["animLoop"].AsBool;
//                        clipAnimations[i].loopTime = animations[i].AsObject["animLoop"].AsBool;
//
//                        if (clipAnimations[i].loop)
//                        {
//                            clipAnimations[i].wrapMode = WrapMode.Loop;	
//                        }
//                        else
//                        {
//                            clipAnimations[i].wrapMode = WrapMode.Default;
//                        }
//
//
//                        List<AnimationEvent> evs = new List<AnimationEvent>();//clipAnimations[i].events.ToList();
//
//                        var wiseEvents = currentClipAnimation.events.Where((ae) => ae.functionName.Equals("PlayWwiseEvent"));
//
//                        evs.AddRange(wiseEvents);
//
//                        for (int j = 0; j < events.Count; j++)
//                        {
//                            float keyEvent = events[j].AsObject["eventKey"].AsFloat;
//                            if (keyEvent <= lastFrame && keyEvent >= startFrame)
//                            {
//                                AnimationEvent ev = new AnimationEvent();
//                                ev.functionName = events[j].AsObject["eventName"].Value;
//                                ev.time = keyEvent / (lastFrame - startFrame);
//                                ev.floatParameter = 0;
//                                ev.intParameter = 0;
//                                ev.stringParameter = "";
//                                ev.objectReferenceParameter = null;
//
//                                evs.Add(ev);
//
//                            }
//                        }
//                        clipAnimations[i].events = evs.ToArray();
//
//                        if (animations[i].AsObject["animRoot"].AsBool)
//                        {
//                            modelImporter.motionNodeName = "Root";
//                            rootNodeProperty.stringValue = "Root";	
//                        }
//                        else
//                        {
//                            modelImporter.motionNodeName = "";
//                            rootNodeProperty.stringValue = "";
//                        }
//                    }
//
//                    modelImporter.clipAnimations = clipAnimations;
//                    modelImporterObj.ApplyModifiedProperties();
//
//
//
//
//                    AteneaLogger.Log("Values Set for : " + importedAssetPath);
//
//
//                }