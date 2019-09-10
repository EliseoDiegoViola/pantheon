using System.IO;
using UnityEditor;
using UnityEngine;
using Pantheon;

class AteneaModelWatcher : AssetPostprocessor
{
    static bool HasPath(string path, string[] paths)
    {
        for (int i = 0; i < paths.Length; i++)
        {
            if (paths[i].ToLower().Equals(path.ToLower()))
                return true;
        }
        return false;
    }
 
    static void OnPostprocessAllAssets(string[] importedAssets, string[] deletedAssets, string[] movedAssets, string[] movedFromAssetPaths)
    {
        string artmastersPath = PathsBuilder.ArtmastersPath.Replace('\\','/');
        for (int i = 0; i < importedAssets.Length; i++)
        {

            //Debug.Log("Imported Asset: " + importedAssets[i]);
            string assetPath = importedAssets[i];      
            

                  
            if (assetPath.ToLower().Contains(artmastersPath.ToLower()) &&
                assetPath.ToLower().EndsWith(".jsonmeta"))
            {
                
                string fbxPath = assetPath.Replace(".jsonmeta", ".fbx");
                if (!HasPath(fbxPath, importedAssets))
                {
                    AssetDatabase.ImportAsset(fbxPath, ImportAssetOptions.Default);
                }
            }
        }

        for (int i = 0; i < movedAssets.Length; i++)
        {
            //Debug.Log("Moved Asset: " + movedAssets[i] + " from: " + movedFromAssetPaths[i]);
            string assetPath = movedAssets[i];
            string modelFolderPath = assetPath.Remove(assetPath.LastIndexOf('/'), assetPath.Length - assetPath.LastIndexOf('/'));
            string[] files;
            if (assetPath.ToLower().Contains(artmastersPath.ToLower()) &&
                assetPath.ToLower().EndsWith(".fbx")) {

                files = Directory.GetFiles(Application.dataPath.Replace("Assets", "") + modelFolderPath + "/", Path.GetFileNameWithoutExtension(assetPath) + ".jsonMeta");
                if (files.Length >= 1)
                {
                    AssetDatabase.ImportAsset(assetPath, ImportAssetOptions.Default);
                }
            } else if (assetPath.ToLower().Contains(artmastersPath.ToLower()) &&
                assetPath.ToLower().EndsWith(".jsonmeta")) {

                files = Directory.GetFiles(Application.dataPath.Replace("Assets", "") + modelFolderPath + "/", Path.GetFileNameWithoutExtension(assetPath) + ".fbx");
                if (files.Length >= 1)
                {
                    string fbxPath = files[0].Replace(Application.dataPath, "Assets");
                    AssetDatabase.ImportAsset(fbxPath, ImportAssetOptions.Default);
                }
            }
        }
    }
}
