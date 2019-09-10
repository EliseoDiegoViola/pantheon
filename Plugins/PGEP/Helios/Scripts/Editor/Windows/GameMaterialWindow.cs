using System;
using UnityEngine;
using UnityEditor;
using Athenea;
using SimpleJSON2;
using System.Linq;

namespace Helios
{
    public class GameMaterialWindow : EditorWindow
    {
        private ShaderDataDigest.MaterialDigest localMaterialObject;
        private JSONObject localMaterialData;
        private GameMaterials.GameMaterial remoteMaterialObject;

        private Action<string> OnActionSucceed;

        Vector2 propertyScrollPoss;
        
        public static void Init(JSONObject material)
        {
            // Get existing open window or if none, make a new one:
            GameMaterialWindow window = (GameMaterialWindow) EditorWindow.GetWindow(typeof(GameMaterialWindow));
            if (material != null)
            {
                window.localMaterialObject = ShaderDataDigest.MaterialDataDigest(material);
                window.localMaterialData = material;
                window.remoteMaterialObject = GameMaterials.GetGameMaterialByName_Sync(window.localMaterialObject.materialName);
                window.Show();
            }
        }

        void OnGUI()
        {

            EditorGUILayout.BeginVertical();

            EditorGUILayout.BeginHorizontal();
            GUILayout.FlexibleSpace();
            GUILayout.Label(String.Format("Working with {0} material", localMaterialObject.materialName),EditorStyles.boldLabel);
            GUILayout.FlexibleSpace();
            EditorGUILayout.EndHorizontal();

            EditorGUILayout.BeginHorizontal();
            if (!string.IsNullOrEmpty(remoteMaterialObject._id))
            {
                EditorGUILayout.BeginVertical();
                EditorGUILayout.BeginHorizontal();
                GUILayout.FlexibleSpace();
                GUILayout.Label(String.Format("↓↓↓↓ SERVER ↓↓↓↓ "), EditorStyles.boldLabel);
                GUILayout.FlexibleSpace();
                EditorGUILayout.EndHorizontal();
                    
                propertyScrollPoss = EditorGUILayout.BeginScrollView(propertyScrollPoss);
                EditorGUILayout.BeginHorizontal();
                GUILayout.Label(String.Format("{0}", "shader"),
                    EditorStyles.label);
                GUILayout.FlexibleSpace();
                GUILayout.Label(String.Format("{0}", remoteMaterialObject.shaderName),
                    EditorStyles.label);
                EditorGUILayout.EndHorizontal();

                foreach (var materialShaderProperty in localMaterialObject.shaderProperties)
                {
                    var remoteProp = remoteMaterialObject.properties.FirstOrDefault(p =>
                        p.propName.Equals(materialShaderProperty.propertyName));
                    EditorGUILayout.BeginHorizontal();
                    GUILayout.Label(String.Format("{0}", remoteProp.propName),
                        EditorStyles.label);
                    GUILayout.FlexibleSpace();
                    GUILayout.Label(String.Format("{0}", remoteProp.propValue),
                        EditorStyles.label);
                    EditorGUILayout.EndHorizontal();

                }

                EditorGUILayout.EndScrollView();
                EditorGUILayout.EndVertical();
            }
            



            EditorGUILayout.BeginVertical();
            EditorGUILayout.BeginHorizontal();
            GUILayout.FlexibleSpace();
            GUILayout.Label(String.Format("↓↓↓↓ LOCAL ↓↓↓↓ "), EditorStyles.boldLabel);
            GUILayout.FlexibleSpace();
            EditorGUILayout.EndHorizontal();
            propertyScrollPoss = EditorGUILayout.BeginScrollView(propertyScrollPoss);
            EditorGUILayout.BeginHorizontal();
            GUILayout.Label(String.Format("{0}", "shader"),
                EditorStyles.label);
            GUILayout.FlexibleSpace();
            GUILayout.Label(String.Format("{0}", localMaterialObject.shaderName),
                EditorStyles.label);
            EditorGUILayout.EndHorizontal();

            foreach (var materialShaderProperty in localMaterialObject.shaderProperties)
            {

                EditorGUILayout.BeginHorizontal();
                GUILayout.Label(String.Format("{0}", materialShaderProperty.propertyValue),
                    EditorStyles.label);
                GUILayout.FlexibleSpace();
                GUILayout.Label(String.Format("{0}", materialShaderProperty.propertyName),
                    EditorStyles.label);
                EditorGUILayout.EndHorizontal();

            }
            EditorGUILayout.EndScrollView();
            EditorGUILayout.EndVertical();

            EditorGUILayout.EndHorizontal();


            if (!string.IsNullOrEmpty(remoteMaterialObject._id))
            {
                if (GUILayout.Button("Modify"))
                {
                    if (EditorUtility.DisplayDialog(string.Format("Modify {0} material?", localMaterialObject.materialName),
                        "You can't undo it later", "Confirm", "Cancel"))
                    {
                            
                        var matUpdated = GameMaterials.ModifyMaterialData_Sync(remoteMaterialObject._id, localMaterialData.ToString());
                        if (!string.IsNullOrEmpty(matUpdated._id))
                        {
                            Debug.Log("Material Uploaded");
                            this.Close();
                            //EditorUtility.DisplayDialog("Material Uploaded", matUpdated.name, "OK");
                        }
                        else
                        {
                                
                            EditorUtility.DisplayDialog("OH NO!", "Something went wrong", ":(");
                        }

                        //GameMaterials.GetGameMaterialByID(remoteMaterialObject._id, MaterialUploadedSuccessful,MaterialUploadedFailed);
                    }
                }
            }
            else
            {
                if (GUILayout.Button("Upload"))
                {
                    if (EditorUtility.DisplayDialog(string.Format("Upload {0} material?", localMaterialObject.materialName),
                        "You can't delete it later", "Confirm", "Cancel"))
                    {
                        var matUpdated = GameMaterials.UploadMaterialData_Sync(localMaterialData.ToString());
                        if (!string.IsNullOrEmpty(matUpdated._id))
                        {
                            //EditorUtility.DisplayDialog("Material Uploaded", matUpdated.name, "OK");
                            Debug.Log("Material Uploaded");
                            this.Close();
                        }
                        else
                        {

                            EditorUtility.DisplayDialog("OH NO!", "Something went wrong", ":(");
                        }
                    }
                }
            }



            GUILayout.FlexibleSpace();

            EditorGUILayout.EndVertical();

        }

    }


}
