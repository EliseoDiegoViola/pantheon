using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using Helios;
using Hermes;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using SimpleJSON2;
using UnityEngine.Rendering;
using Object = UnityEngine.Object;

namespace Apollo
{
    public class ApolloJob : ScriptableObject
    {
        public enum BakeResult
        {
            ERROR,
            COMPLETED
        }
        private const string lightProbesSuffix = "_LIGHTPROBES_DATA.json";

        [SerializeField]
        private SceneAsset[] scenes;
        [SerializeField]
        private SceneAsset bakeScene;
        [SerializeField]
        private ApolloLightmapSettings settings;
        [SerializeField]
        private String[] gameobjectsToDisable;

        private JSONObject manifest;
        public string BakeFolder
        {
            get { return Path.Combine(Application.dataPath, Directory.GetParent(AssetDatabase.GetAssetPath(bakeScene)).FullName); }
        }


        public SceneAsset BakeScene
        {
            get { return bakeScene; }
        }

        //private Dictionary<string, object> manifest;

        public Action<BakeResult, FileInfo[], ApolloJob> OnBakeCompleted;
        public Action<BakeResult, Exception> OnBakeFailed;

        public void Start()
        {
            manifest = new JSONObject();
            EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            if (!CheckOpenedScenes())
            {
                SetupScenes();
            }
            BakeScenes();
        }

        public void Stop()
        {
            if (Lightmapping.isRunning)
            {
                Lightmapping.Cancel();
                OnBakeFailed(BakeResult.ERROR, new Exception("Canceled"));
            }
            else
            {
                Debug.LogError("Trying to stop a Job which is not running");
            }
        }



        private bool CheckOpenedScenes()
        {
            if (scenes.Length == 0) return false;
            if (EditorSceneManager.loadedSceneCount != scenes.Length) return false;

            for (int i = 0; i < scenes.Length; i++)
            {
                var scene = EditorSceneManager.GetSceneByName(scenes[i].name);
                if (!scene.name.Equals(scenes[i].name))
                {
                    return false;
                }
            }

            EditorSceneManager.SetActiveScene(EditorSceneManager.GetSceneByName(bakeScene.name));
            return true;
        }

        private void SetupScenes()
        {
            if (scenes.Length == 0) return;
            if (!scenes.Contains(bakeScene)) return;
            EditorSceneManager.OpenScene(AssetDatabase.GetAssetPath(scenes[0]), OpenSceneMode.Single);

            for (int i = 1; i < scenes.Length; i++)
            {
                string scenePath = AssetDatabase.GetAssetPath(scenes[i]);
                EditorSceneManager.OpenScene(scenePath, OpenSceneMode.Additive);
            }

            EditorSceneManager.SetActiveScene(EditorSceneManager.GetSceneByName(bakeScene.name));

            if (gameobjectsToDisable != null) {
                for (int i = 0; i < gameobjectsToDisable.Length; i++)
                {
                    GameObject.Find(gameobjectsToDisable[i]).SetActive(false);
                }
            }
            
        }

        private void BakeScenes()
        {
            try
            {
                Lightmapping.Clear();

                MethodInfo GetLightmapSettingsMethod = null;
                Type type = typeof(LightmapEditorSettings);
                MethodInfo method = type.GetMethod("GetLightmapSettings", BindingFlags.NonPublic | BindingFlags.Static);
                if (method != null) GetLightmapSettingsMethod = method;


                var m_LightmapSettings = GetLightmapSettingsMethod.Invoke(null, null) as UnityEngine.Object;
                var m_LightmapSettingsSO = new SerializedObject(m_LightmapSettings);

               // Debug.Log(settings.lightmapResolution);
                //Debug.Log(LightmapEditorSettings.bakeResolution);
                
                //LightmapEditorSettings.finalGatherRays
                //Debug.Log(LightmapEditorSettings.bakeResolution);
                SerializedProperty m_LightmapParameters = m_LightmapSettingsSO.FindProperty("m_LightmapEditorSettings.m_LightmapParameters");
                SerializedProperty m_EnableRealtimeGI = m_LightmapSettingsSO.FindProperty("m_GISettings.m_EnableRealtimeLightmaps");
                SerializedProperty m_AmbientOcclusion = m_LightmapSettingsSO.FindProperty("m_LightmapEditorSettings.m_AO");
                SerializedProperty m_AOMaxDistance = m_LightmapSettingsSO.FindProperty("m_LightmapEditorSettings.m_AOMaxDistance");
                SerializedProperty m_CompAOExponent = m_LightmapSettingsSO.FindProperty("m_LightmapEditorSettings.m_CompAOExponent");
                SerializedProperty m_CompAOExponentDirect = m_LightmapSettingsSO.FindProperty("m_LightmapEditorSettings.m_CompAOExponentDirect");

                m_LightmapParameters.objectReferenceValue = settings.lightmapParameters;
                m_EnableRealtimeGI.boolValue = false;
                m_AmbientOcclusion.boolValue = true;
                m_AOMaxDistance.floatValue = 2;
                m_CompAOExponent.floatValue = 2;
                m_CompAOExponentDirect.floatValue = 1;

                //Debug.Log(LightmapEditorSettings.bakeResolution);
                m_LightmapSettingsSO.ApplyModifiedProperties();
                //Debug.Log(LightmapEditorSettings.bakeResolution);
                LightmapEditorSettings.bakeResolution = settings.lightmapResolution;
                LightmapEditorSettings.padding = settings.lightmapPadding;
                LightmapEditorSettings.realtimeResolution = settings.indirectResolution;
                LightmapEditorSettings.maxAtlasSize =
                    ApolloLightmapSettings.LightmapSizeValues[(int)settings.lightmapSize];

                //Debug.Log(LightmapEditorSettings.bakeResolution);
                Lightmapping.completed = BakeCompleted;
                
                Lightmapping.Bake();

            }
            catch (Exception e)
            {
                OnBakeFailed(BakeResult.ERROR, e);
                Debug.LogError(e.Message);
            }
        }

        private void BakeCompleted()
        {
            List<FileInfo> files = new List<FileInfo>();
            JSONArray sceneNameList = new JSONArray();



            foreach (var scene in scenes)
            {
                JSONObject sceneData = new JSONObject();
                EditorSceneManager.SetActiveScene(EditorSceneManager.GetSceneByName(scene.name));
                sceneData.Add("name", scene.name);
                sceneData.Add("lightingAsset", Lightmapping.lightingDataAsset.name);
                sceneNameList.Add(sceneData);


                DirectoryInfo bakePath =
                    Directory.GetParent(Path.Combine(Directory.GetParent(Application.dataPath).FullName,
                        AssetDatabase.GetAssetPath(scene)));
                if (Directory.Exists(bakePath.FullName + "/" + scene.name + "/"))
                {
                    string[] bakeFiles = Directory
                        .GetFiles(bakePath.FullName + "/" + scene.name + "/", "*.*", SearchOption.TopDirectoryOnly)
                        .Where(s => s.EndsWith(".asset") || s.EndsWith(".meta") || s.EndsWith(".png") || s.EndsWith(".exr"))
                        .ToArray();

                    foreach (var bakedFile in bakeFiles)
                    {
                        FileInfo fi = new FileInfo(bakedFile);
                        files.Add(fi);
                    }
                }
            }

            EditorSceneManager.SetActiveScene(EditorSceneManager.GetSceneByName(bakeScene.name));

            JSONArray bakedFileList = new JSONArray();
            for (int i = 0; i < LightmapSettings.lightmaps.Length; i++){
                var lightmap = LightmapSettings.lightmaps[i];

                JSONObject lightmapData = new JSONObject();
                if (lightmap.lightmapDir != null)
                {
                    lightmapData.Add("dir", lightmap.lightmapDir.name + ".png");
                }
                else
                {
                    //HermesLogger.LogSlack(string.Format("{0} Job dont have a lightmapDir baked on the lightmap {1} ", BakeScene.ToString(), i), HermesLogger.ReportLevel.WARN);
                }

                if(lightmap.lightmapColor != null)
                {
                    lightmapData.Add("light", lightmap.lightmapColor.name + ".exr");
                }
                else
                {
                    //HermesLogger.LogSlack(string.Format("{0} Job dont have a lightmapColor baked on the lightmap {1} ", BakeScene.ToString(), i), HermesLogger.ReportLevel.WARN);
                }

                if(lightmap.shadowMask != null)
                {
                    lightmapData.Add("mask", lightmap.shadowMask.name + ".png");
                }
                else
                {
                    //HermesLogger.LogSlack(string.Format("{0} Job dont have a shadowMask baked on the lightmap {1} ", BakeScene.ToString(), i), HermesLogger.ReportLevel.WARN);
                }

                
                
                bakedFileList.Add(lightmapData);
            }

            JSONArray reflectionProbesList = new JSONArray();
            ReflectionProbe[] reflectionProbes = GameObject.FindObjectsOfType<ReflectionProbe>();
            foreach (ReflectionProbe reflectionProbe in reflectionProbes)
            {
                if (reflectionProbe.mode == ReflectionProbeMode.Baked)
                {


                    JSONObject refData = new JSONObject();
                    refData.Add("gameObjectName", reflectionProbe.gameObject.name);
                    if (reflectionProbe.bakedTexture != null)
                    {
                        refData.Add("exr", reflectionProbe.bakedTexture.name + ".exr");
                    }
                    else
                    {
                        HermesLogger.LogSlack(string.Format("{0} reflection probe problem on {1}", reflectionProbe.gameObject.name, BakeScene.ToString()), HermesLogger.ReportLevel.ERROR);
                    }
                    reflectionProbesList.Add(refData);
                }

                
            }




            JSONArray bakedRenderers = new JSONArray();
            Renderer[] renderersInScene = EditorSceneManager.GetActiveScene().GetRootGameObjects()
                .SelectMany(go => go.GetComponentsInChildren<Renderer>(true)).ToArray();
            foreach (Renderer renderer in renderersInScene)
            {
                JSONObject bakedRendererData = new JSONObject();
                bakedRendererData.Add("gameObjectName", renderer.gameObject.name);
                bakedRendererData.Add("lightIndex", renderer.lightmapIndex);
                JSONObject offset = new JSONObject();
                offset.Add("x", renderer.lightmapScaleOffset.x);
                offset.Add("y", renderer.lightmapScaleOffset.y);
                offset.Add("z", renderer.lightmapScaleOffset.z);
                offset.Add("w", renderer.lightmapScaleOffset.w);
                bakedRendererData.Add("staticOffset", offset);
                bakedRenderers.Add(bakedRendererData);
            }

            manifest.Add("timestamp", DateTime.Now.ToLongDateString());
            manifest.Add("scenes", sceneNameList);
            manifest.Add("bakedFiles", bakedFileList);
            manifest.Add("reflectionProbes", reflectionProbesList);
            manifest.Add("bakedRenderers", bakedRenderers);
            manifest.Add("lightingData", "LightingData.asset");


            string manifestPath = BakeFolder + "/" + bakeScene.name + ApolloRunner.manifestSuffix;
            File.WriteAllText(manifestPath, manifest.ToString());
            files.Add(new FileInfo(manifestPath));

            if (OnBakeCompleted != null) {
                OnBakeCompleted(BakeResult.COMPLETED, files.ToArray(), this);
            }
            
        }

        public void ApplyJobData()
        {
            if (!CheckOpenedScenes())
            {
                SetupScenes();
            }

            if (!Directory.Exists(Path.Combine(BakeFolder, "PRE-BAKE")))
            {
                Directory.CreateDirectory(Path.Combine(BakeFolder, "PRE-BAKE"));
            }
            DirectoryInfo storageFolder = new DirectoryInfo(Path.Combine(BakeFolder, "PRE-BAKE"));
            FileInfo manifestFile = FTPService.DownloadFileSync(BakeScene.name + ApolloRunner.manifestSuffix, BakeScene.name, storageFolder);
            JSONObject manifest = JSON.Parse(File.ReadAllText(manifestFile.FullName)).AsObject;


            //LightProbes
            /*var lights = new LightProbes();
            lights.name = "asaasd";
            Debug.Log(lights);
            TextAsset lightProbeAsset = DownloadAndImportFile<TextAsset>(manifest["lightProbeFile"].Value, storageFolder);
            EditorJsonUtility.FromJsonOverwrite(lightProbeAsset.text, LightmapSettings.lightProbes);*/

            //LightingAsset
            Object lightingParentAsset = DownloadAndImportFile<Object>(manifest["lightingData"].Value, storageFolder, withMeta: true);
            Object[] lightingDataAssets = AssetDatabase.LoadAllAssetsAtPath(AssetDatabase.GetAssetPath(lightingParentAsset));
            for (int i = 0; i < manifest["scenes"].AsArray.Count; i++)
            {
                JSONObject sceneData = manifest["scenes"].AsArray[i].AsObject;
                EditorSceneManager.SetActiveScene(EditorSceneManager.GetSceneByName(sceneData["name"].Value));
                Lightmapping.lightingDataAsset = lightingDataAssets.FirstOrDefault(ass => ass.name.Equals(sceneData["lightingAsset"].Value)) as LightingDataAsset;
            }
            EditorSceneManager.SetActiveScene(EditorSceneManager.GetSceneByName(bakeScene.name));


            //LightMaps
            LightmapData[] lightmaps = new LightmapData[manifest["bakedFiles"].AsArray.Count];
            for (var i = 0; i < manifest["bakedFiles"].AsArray.Count; i++)
            {
                JSONObject bakedFile = manifest["bakedFiles"].AsArray[i].AsObject;
                lightmaps[i] = new LightmapData();

                Texture2D mapDirTexture = DownloadAndImportFile<Texture2D>(bakedFile["dir"].Value, storageFolder, withMeta: true);
                lightmaps[i].lightmapDir = mapDirTexture;

                Texture2D mapLightTexture = DownloadAndImportFile<Texture2D>(bakedFile["light"].Value, storageFolder, withMeta: true);
                lightmaps[i].lightmapColor = mapLightTexture;

                Texture2D mapShadowTexture = DownloadAndImportFile<Texture2D>(bakedFile["mask"].Value, storageFolder, withMeta: true);
                lightmaps[i].shadowMask = mapShadowTexture;
            }
            LightmapSettings.lightmaps = lightmaps;



            //ReflectionProbes
            for (int i = 0; i < manifest["reflectionProbes"].AsArray.Count; i++)
            {
                JSONObject refData = manifest["reflectionProbes"].AsArray[i].AsObject;
                Cubemap reflectionTexture = DownloadAndImportFile<Cubemap>(refData["exr"].Value, storageFolder, withMeta: true);
                GameObject reflectionProbeGO = GameObject.Find(refData["gameObjectName"].Value); ;
                if (reflectionProbeGO != null)
                {
                    
                    var refProbe = reflectionProbeGO.GetComponent<ReflectionProbe>();
                    if (refProbe != null)
                    {
                        reflectionProbeGO.GetComponent<ReflectionProbe>().bakedTexture = reflectionTexture;
                    }
                    else
                    {
                        HermesLogger.LogSlack(string.Format("{0}: {1} reflection probe MUST have unique names!",BakeScene.ToString(), refData["gameObjectName"].Value), HermesLogger.ReportLevel.ERROR);
                    }
                }
                else
                {
                    Debug.LogError("REFLECTION PROBE NOT FOUND");
                }
            }

            //BakedRenderers
            for (int i = 0; i < manifest["bakedRenderers"].AsArray.Count; i++)
            {
                JSONObject bakedRendRef = manifest["bakedRenderers"].AsArray[i].AsObject;
                GameObject bakedGO =  GameObject.Find(bakedRendRef["gameObjectName"].Value);
                if (bakedGO != null)
                {
                    var rendererGO = bakedGO.GetComponent<Renderer>();
                    if (rendererGO != null)
                    {
                        bakedGO.GetComponent<Renderer>().lightmapIndex = bakedRendRef["lightIndex"].AsInt;
                        Vector4 offset = new Vector4();
                        offset.x = bakedRendRef["staticOffset"].AsObject["x"].AsFloat;
                        offset.y = bakedRendRef["staticOffset"].AsObject["y"].AsFloat;
                        offset.z = bakedRendRef["staticOffset"].AsObject["z"].AsFloat;
                        offset.w = bakedRendRef["staticOffset"].AsObject["w"].AsFloat;
                        bakedGO.GetComponent<Renderer>().lightmapScaleOffset = offset;
                    }
                    else
                    {
                        Debug.LogError(bakedRendRef["gameObjectName"].Value + " RENDERER NOT FOUND");
                    }
                }
                else
                {
                    Debug.LogError(bakedRendRef["gameObjectName"].Value + " BAKED GAMEOBJECT NOT FOUND");
                }
            }


        }


        //Move From Here
        private T DownloadAndImportFile<T>(string fileName, DirectoryInfo folder, bool withMeta = false) where T : UnityEngine.Object
        {
            if (withMeta)
            {
                //FileInfo metaFile = 
                FTPService.DownloadFileSync(fileName + ".meta", BakeScene.name, folder);
            }


            FileInfo downloadedFile = FTPService.DownloadFileSync(fileName, BakeScene.name, folder);
            //AssetDatabase.Refresh(ImportAssetOptions.Default);
            AssetDatabase.ImportAsset(downloadedFile.FullName.Replace(Application.dataPath.Replace("/", "\\"), "Assets"), ImportAssetOptions.Default);
            T loadedAsset = AssetDatabase.LoadAssetAtPath<T>(downloadedFile.FullName.Replace(Application.dataPath.Replace("/", "\\"), "Assets"));
            return loadedAsset;
        }


        [MenuItem("Assets/Create/Apollo/Apollo Job")]
        public static void CreateMyAsset()
        {
            ApolloJob asset = ScriptableObject.CreateInstance<ApolloJob>();

            AssetDatabase.CreateAsset(asset, AssetDatabase.GetAssetPath(Selection.objects[0]) + "/NewApolloJob.asset");
            AssetDatabase.SaveAssets();

            EditorUtility.FocusProjectWindow();

            Selection.activeObject = asset;
        }

        /*[MenuItem("Assets/DebugAsset")]
        public static void DebugAsset()
        {
            Debug.Log(Selection.activeObject.name);
            //Debug.Log(Lightmapping.lightingDataAsset.name);
        }*/
    }


}
