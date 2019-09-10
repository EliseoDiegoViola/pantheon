//using System.IO;
//using ElementSpace;
//using SimpleJSON2;
//using UnityEngine;
//using UnityEditor;
//using JSONArray = SimpleJSON2.JSONArray;

//public class WeaponFD{

//    [MenuItem ("Assets/Weapon/List Weapons")]
//    public static JSONObject ListWeapons(){
//        JSONObject jsonBase = new JSONObject();
//        JSONArray shaderArray = new JSONArray();
//        string[] allPrefabs = AssetDatabase.FindAssets("t:Prefab");
//        JSONObject weapons = new JSONObject();
//        int i;
//        for (i = 0; i < allPrefabs.Length; i++)
//        {
//            string assetPath =  AssetDatabase.GUIDToAssetPath(allPrefabs[i]);
            
            
//            GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(assetPath);
//            if(prefab.name.Equals("Weapon_Turret")) continue;

//            if (prefab.GetComponentInChildren<MeleeWeapon>() || prefab.GetComponentInChildren<FireWeapon>())
//            {
//                Debug.Log(assetPath);
//                JSONObject prefabData = new JSONObject();
//                prefabData.Add("prefab", assetPath);
//                MeshFilter[] meshFilters = prefab.GetComponentsInChildren<MeshFilter>();
//                JSONArray meshReferences = new JSONArray();
//                prefabData.Add("meshReferences",meshReferences);
//                foreach (MeshFilter meshFilter in meshFilters)
//                {
//                    string meshPath = AssetDatabase.GetAssetPath(meshFilter.sharedMesh);
//                    if (!string.IsNullOrEmpty(meshPath) && meshPath.Split('/')[0].Equals("Assets"))
//                    {
//                        meshReferences.Add(meshPath);
//                    }
//                }
                 
//                MeshRenderer[] renderers = prefab.GetComponentsInChildren<MeshRenderer>();
//                JSONArray rendererReferences = new JSONArray();
//                prefabData.Add("rendererReferences", rendererReferences);
//                foreach (MeshRenderer meshRenderer in renderers)
//                {
//                    foreach (Material rendererMaterial in meshRenderer.sharedMaterials)
//                    {
//                        string matPath = AssetDatabase.GetAssetPath(rendererMaterial);
//                        if (!string.IsNullOrEmpty(matPath) && matPath.Split('/')[0].Equals("Assets"))
//                        {
//                            rendererReferences.Add(matPath);
//                            Shader shader = rendererMaterial.shader;
//                            int shaderPropCount = ShaderUtil.GetPropertyCount(shader);
//                            for (int j = 0; j < shaderPropCount; j++)
//                            {
//                                if (ShaderUtil.GetPropertyType(shader, j) == ShaderUtil.ShaderPropertyType.TexEnv)
//                                {
//                                    Texture texture = rendererMaterial.GetTexture(ShaderUtil.GetPropertyName(shader, j));
//                                    if (texture != null)
//                                    {
//                                        rendererReferences.Add(AssetDatabase.GetAssetPath(texture));
//                                    }


//                                }
//                            }
//                        }
                        

                      
                        
//                    }
//                }
//                weapons.Add(prefab.name, prefabData);
//            }
//        }
//        File.WriteAllText(Application.dataPath.Replace("Assets", "Weapons.json"), weapons.ToString());
//        return weapons;
//    }

//    [MenuItem ("Assets/Weapon/Destroy Weapons")]
//    public static void DestroyWeapons()
//    {
//        JSONObject weapons = ListWeapons();
//        for (int i = 0; i < weapons.Count; i++)
//        {
//            JSONObject weapon = weapons[i].AsObject;

//            AssetDatabase.DeleteAsset(weapon["prefab"].Value);

//            //DELETE Meshes
//            foreach (JSONNode meshRef in weapon["meshReferences"].AsArray)
//            {
//                AssetDatabase.DeleteAsset(meshRef.Value);
//            }

//            //DELETE Materials and textures
//            foreach (JSONNode rendRef in weapon["rendererReferences"].AsArray)
//            {
//                AssetDatabase.DeleteAsset(rendRef.Value);
                
//            }
//        }

//    }
        
//}
