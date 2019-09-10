using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Helios;
using UnityEditor;
using System.Linq;
using UnityEditor.SceneManagement;
using SimpleJSON2;
using System.IO;

public class MaterialLibraryTracker
{

    public struct MaterialRef
    {
        public string matPath;
        public Material mat;
        public List<GameObject> fileReferences;
        public List<string> sceneReferences;
    }

    //Debug.ClearDeveloperConsole();

    public static MaterialRef[] AnalyzeArtMasterMaterials()
    {
        EditorUtility.DisplayProgressBar("Analyzing artmasters", "", 0);
        string[] materialsPath = AssetDatabase.FindAssets("t:material", new string[] { "Assets/ElementSpace/Artworks/ArtMasters" });
        MaterialRef[] materialReferences = new MaterialRef[materialsPath.Length];
        for (int i = 0; i < materialReferences.Length; i++)
        {
            EditorUtility.DisplayProgressBar("Parsing materials", AssetDatabase.GUIDToAssetPath(materialsPath[i]), (float)i / (float)materialReferences.Length);
            materialReferences[i] = new MaterialRef
            {
                matPath = AssetDatabase.GUIDToAssetPath(materialsPath[i]),
                mat = AssetDatabase.LoadAssetAtPath<Material>(AssetDatabase.GUIDToAssetPath(materialsPath[i])),
                fileReferences = new List<GameObject>(),
                sceneReferences = new List<string>()
                
            };
        }

        string[] prefabPaths = AssetDatabase.FindAssets("t:prefab", new string[] { "Assets/ElementSpace/Artworks/ArtMasters" });
        for (int i = 0; i < prefabPaths.Length; i++)
        {
            EditorUtility.DisplayProgressBar("Parsing Prefabs", AssetDatabase.GUIDToAssetPath(prefabPaths[i]), (float)i / (float)prefabPaths.Length);

            GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(AssetDatabase.GUIDToAssetPath(prefabPaths[i]));
            Renderer[] prefabsRends = prefab.GetComponentsInChildren<Renderer>();
            if (prefabsRends != null && prefabsRends.Length > 0)
            {
                for (int j = 0; j < prefabsRends.Length; j++)
                {
                    Renderer r = prefabsRends[j];
                    Material[] renMaterials = r.sharedMaterials;
                    for (int k = 0; k < renMaterials.Length; k++)
                    {
                        MaterialRef matRef = materialReferences.FirstOrDefault(matr => matr.mat == renMaterials[k]);
                        if (matRef.mat != null) matRef.fileReferences.Add(prefab);
                    }

                }
            }
        }

        string[] scenePaths = AssetDatabase.FindAssets("t:scene", new string[] { "Assets/ElementSpace_NewFolder/Scenes" });
        EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);

        for (int i = 0; i < scenePaths.Length; i++)
        {
            EditorUtility.DisplayProgressBar("Parsing Scenes", AssetDatabase.GUIDToAssetPath(scenePaths[i]), (float)i / (float)scenePaths.Length);

            //SceneAsset scene = AssetDatabase.LoadAssetAtPath<SceneAsset>(AssetDatabase.GUIDToAssetPath(scenePaths[i]));
            EditorSceneManager.OpenScene(AssetDatabase.GUIDToAssetPath(scenePaths[i]), OpenSceneMode.Single);

            Renderer[] sceneRends = GameObject.FindObjectsOfType<Renderer>();
            if (sceneRends != null && sceneRends.Length > 0)
            {
                for (int j = 0; j < sceneRends.Length; j++)
                {
                    Renderer r = sceneRends[j];
                    Material[] renMaterials = r.sharedMaterials;
                    for (int k = 0; k < renMaterials.Length; k++)
                    {
                        MaterialRef matRef = materialReferences.FirstOrDefault(matr => matr.mat == renMaterials[k]);
                        if (matRef.mat != null)
                        {                            
                            matRef.sceneReferences.Add(r.gameObject.name + " ______ " + AssetDatabase.GUIDToAssetPath(scenePaths[i]));

                        }
                    }

                }
            }
        }


        EditorUtility.ClearProgressBar();
        return materialReferences;
    }



    public static void ReportRefs(MaterialRef[] refs) {
        JSONObject parent = new JSONObject();
        parent.Add("SAFE", new JSONArray());
        parent.Add("OK", new JSONArray());
        parent.Add("INNECESARY", new JSONArray());
        parent.Add("WRONG", new JSONArray());
        for (int i = 0; i < refs.Length; i++)
        {
            MaterialRef r = refs[i];
            JSONObject matReport = new JSONObject();
            matReport.Add("matName", r.matPath);
            matReport.Add("fileReferences", new JSONArray());
            matReport.Add("sceneReferences", new JSONArray());

            foreach (var fr in r.fileReferences) matReport["fileReferences"].AsArray.Add(fr.name);
            foreach (var sr in r.sceneReferences) matReport["sceneReferences"].AsArray.Add(sr);

            if (r.fileReferences.Count > 0 && r.sceneReferences.Count == 0) //Have prefabs and is NOT in use ( INNECESARY ASSET)
            {
                
                Debug.LogFormat(refs[i].mat, "{0} ----- {1} ----- <color=orange>INNECESARY ASSET</color>", r.matPath, r.sceneReferences.Count);
                parent["INNECESARY"].Add(matReport);
            }

            else if (r.fileReferences.Count == 0 && r.sceneReferences.Count > 0) //Have NO prefabs and is in use ( SOMEONE'S HEAD MUST ROLL)
            {
                Debug.LogFormat(refs[i].mat, "{0} ----- {1} ----- <color=maroon>SOMEONE'S HEAD MUST ROLL</color>", r.matPath, r.sceneReferences.Count);
                parent["WRONG"].Add(matReport);
            }

            else if (r.fileReferences.Count > 0 && r.sceneReferences.Count > 0) //Have prefabs and is in use (OK CASE)
            {
                Debug.LogFormat(refs[i].mat, "{0} ----- <color=green>OK CASE</color>", r.matPath);
                parent["OK"].Add(matReport);
            }

            else if (r.fileReferences.Count == 0 && r.sceneReferences.Count == 0) //Have NO prefabs and is NOT in use (SAFE CLEAN)
            {
                Debug.LogFormat(refs[i].mat, "{0} ----- <color=teal>SAFE CLEAN</color>", r.matPath);
                parent["SAFE"].Add(matReport);
            }
        }
        File.WriteAllText(Application.dataPath.Replace("Assets", "WorngMaterials.json"), parent.ToString());
    }



    [MenuItem("Assets/TESTING/Analyze")]
    static void InvestigateNonProceduralParticles()
    {
        var refs = AnalyzeArtMasterMaterials();
        ReportRefs(refs);
    }
}
