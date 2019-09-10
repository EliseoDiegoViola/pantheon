//using System;
//using System.Linq;
//using System.Collections;
//using System.Collections.Generic;
//using UnityEditor;
//using UnityEngine;
//using System.IO;

//public class MaterialDuplicateReferences : MonoBehaviour
//{

//    [MenuItem("Assets/Pantheon/HARDCODED/Check ArtMasters Materials")]
//    static void CheckMaterialReferences()
//    {

//        string[] coverPrefabs = AssetDatabase.FindAssets("t:Prefab", new string[] {"Assets/ElementSpace/Prefabs/Covers"});
//        Debug.Log(coverPrefabs.Length);

//        string[] materialsAll = AssetDatabase.FindAssets("t:Material", new string[] { "Assets/ElementSpace/Artworks/ArtMasters" });
//        string[] prefabsAll = AssetDatabase.FindAssets("t:Prefab", new string[] { "Assets/ElementSpace/Artworks/ArtMasters" }).Concat(coverPrefabs).ToArray();
//        string[] materialsGood = AssetDatabase.FindAssets("t:Material", new string[] { "Assets/ElementSpace/Artworks/ArtMasters/Materials" });
//        string[] materialsDuplicated = materialsAll.Where(s => !materialsGood.Contains(s)).ToArray();

//        string[] materialsGoodAssets = materialsGood.Select(AssetDatabase.GUIDToAssetPath).ToArray();
//        string[] materialsDuplicatedAssets = materialsDuplicated.Select(AssetDatabase.GUIDToAssetPath).ToArray();

//        GameObject[] prefabsGO = new GameObject[prefabsAll.Length];
//        Material[] duplicatedAssets = new Material[materialsDuplicated.Length];

//        for (int i = 0; i < prefabsAll.Length; i++)
//        {
//            prefabsGO[i] = AssetDatabase.LoadAssetAtPath<GameObject>(AssetDatabase.GUIDToAssetPath(prefabsAll[i]));
//            Renderer[] renderers = prefabsGO[i].GetComponentsInChildren<Renderer>();
//            foreach (var renderer in renderers)
//            {
//                for (int j = 0; j < renderer.sharedMaterials.Length; j++)
//                {
//                    string materialPath = AssetDatabase.GetAssetPath(renderer.sharedMaterials[j]);
//                    if (materialsDuplicatedAssets.Contains(materialPath))
//                    {
//                        string materialName = Path.GetFileName(materialPath);
//                        string goodMaterialPath = materialsGoodAssets.FirstOrDefault(mg => Path.GetFileName(mg).ToLower().Equals(materialName.ToLower()));
//                        if (string.IsNullOrEmpty(goodMaterialPath))
//                        {
//                            Debug.LogError("THE OBJECT " + prefabsGO[i].name + " mat: " + materialPath + " WAS NOT FOUND IN GOOD!?");
//                            AssetDatabase.MoveAsset(materialPath,
//                                "Assets/ElementSpace/Artworks/ArtMasters/Materials/" + Path.GetFileName(materialPath));
//                        }
//                        else
//                        {
//                            Material[] sharedMaterials = renderer.sharedMaterials;
//                            sharedMaterials[j] = AssetDatabase.LoadAssetAtPath<Material>(goodMaterialPath);
//                            renderer.sharedMaterials = sharedMaterials;
//                            Debug.Log("THE OBJECT " + prefabsGO[i].name + " SHOULD HAVE " + goodMaterialPath + " IN " + j + " THE RENDERER " + renderer.name);
//                        }
//                    }
//                }
//            }
//        }
//        Debug.Log("EVERYTHING IS FINE");
//        for (int i = 0; i < materialsDuplicated.Length; i++)
//        {
//            Debug.LogWarning(AssetDatabase.GUIDToAssetPath(materialsDuplicated[i]));
//            AssetDatabase.DeleteAsset(AssetDatabase.GUIDToAssetPath(materialsDuplicated[i]));
//        }
//        AssetDatabase.Refresh();
//    }

//    [MenuItem("Assets/Pantheon/HARDCODED/Check ArtMasters Textures")]
//    static void CheckTextureReferences()
//    {
//        string[] texturesAll = AssetDatabase.FindAssets("t:Texture", new string[] { "Assets/ElementSpace/Artworks/ArtMasters" });
//        string[] materialsAll = AssetDatabase.FindAssets("t:Material", new string[] { "Assets/ElementSpace/Artworks/ArtMasters/Materials" });
//        string[] texturesGood = AssetDatabase.FindAssets("t:Texture", new string[] { "Assets/ElementSpace/Artworks/ArtMasters/Textures" });
//        string[] texturesDuplicated = texturesAll.Where(s => !texturesGood.Contains(s)).ToArray();

//        string[] texturesGoodAssets = texturesGood.Select(AssetDatabase.GUIDToAssetPath).ToArray();
//        string[] texturesDuplicatedAssets = texturesDuplicated.Select(AssetDatabase.GUIDToAssetPath).ToArray();

//        Material[] materials = new Material[materialsAll.Length];
//        Material[] duplicatedAssets = new Material[texturesDuplicated.Length];

//        for (int i = 0; i < materialsAll.Length; i++)
//        {
//            materials[i] = AssetDatabase.LoadAssetAtPath<Material>(AssetDatabase.GUIDToAssetPath(materialsAll[i]));


//            for (int j = 0; j < ShaderUtil.GetPropertyCount(materials[i].shader); j++)
//            {
//                if (ShaderUtil.GetPropertyType(materials[i].shader, j) == ShaderUtil.ShaderPropertyType.TexEnv)
//                {
//                    string propName = ShaderUtil.GetPropertyName(materials[i].shader,j);
//                    Texture matTex = materials[i].GetTexture(propName);
//                    string texturePath = AssetDatabase.GetAssetPath(matTex);
//                    if (texturesDuplicatedAssets.Contains(texturePath))
//                    {
//                        string textureName = Path.GetFileName(texturePath);
//                        string goodTexturePath = texturesGoodAssets.FirstOrDefault(mg => Path.GetFileName(mg).ToLower().Equals(textureName.ToLower()));
//                        if (string.IsNullOrEmpty(goodTexturePath))
//                        {
//                            Debug.LogError("THE MATERIAL " + materials[i].name + " texture: " + texturePath + " WAS NOT FOUND IN GOOD!?");
//                            AssetDatabase.MoveAsset(texturePath,
//                                "Assets/ElementSpace/Artworks/ArtMasters/Textures/" + Path.GetFileName(texturePath));
//                        }
//                        else
//                        {
//                            Texture goodTexture = AssetDatabase.LoadAssetAtPath<Texture>(goodTexturePath);
//                            Debug.Log("THE MATERIAL  " + materials[i].name + " SHOULD HAVE " + goodTexturePath);
//                            //Debug.Log("SETTING " + goodTexture.name);
//                            materials[i].SetTexture(propName, goodTexture);
//                        }
//                    }
//                }
//            }

//            //foreach (var texture in textures)
//            //{
                
//            //}
//        }
//        Debug.Log("EVERYTHING IS FINE");
//        for (int i = 0; i < texturesDuplicated.Length; i++)
//        {
//            Debug.LogWarning(AssetDatabase.GUIDToAssetPath(texturesDuplicated[i]));
//            AssetDatabase.DeleteAsset(AssetDatabase.GUIDToAssetPath(texturesDuplicated[i]));
//        }
//        AssetDatabase.Refresh();

//    }
//}
