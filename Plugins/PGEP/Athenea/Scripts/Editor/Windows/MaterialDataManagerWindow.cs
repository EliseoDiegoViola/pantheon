using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using System.IO;
using System.Linq;
using Helios;
using SimpleJSON2;

namespace Athenea{
	public class MaterialDataManagerWindow : EditorWindow
	{

	    struct LocalMaterial
	    {
	        public Material mat;
	        public string matPath;
	        public GameMaterials.GameMaterial serverMat;
	    }

	    struct LocalTexture
	    {
	        public Texture tex;
	        public string texPath;
	        public List<LocalMaterial> localMatRefs;
        }

	    private GameMaterials.GameMaterial[] gameMaterials;
	    private LocalMaterial[] localMaterials;
	    private LocalTexture[] localTextures;

        private GUIStyle goodMaGuiStylet;
	    private GUIStyle badMGuiStyleat;

        private bool serverCheck;

	    private Vector2 materialsScrollPoss;
	    private Vector2 texturesScrollPoss;




        //static string[] shaderNames = new string[]{ "HDRenderPipeline/Unlit","HDRenderPipeline/Lit","HDRenderPipeline/Decal" };


  //      static MaterialDataManagerWindow window;
		//static MaterialDataManagerWindow Window
  //      {
		//	get{
		//		if(window == null){
		//			window = (MaterialDataManagerWindow)EditorWindow.GetWindow (typeof (MaterialDataManagerWindow));

		//		}
		//		return window;
		//	}
		//}

	    [MenuItem("Pantheon/Helios/Material Library")]
	    static void OpenMaterialManagetWindow()
	    {

	        MaterialDataManagerWindow window = (MaterialDataManagerWindow)EditorWindow.GetWindow(typeof(MaterialDataManagerWindow));
	        if (window != null)
	        {
	            window.gameMaterials =  GameMaterials.GetListGameMaterials_Sync();

	            string[] texIdsds = AssetDatabase.FindAssets("t:texture", new String[] { "Assets/ElementSpace/Artworks/ArtMasters" });
	            window.localTextures = new LocalTexture[texIdsds.Length];
	            for (int i = 0; i < texIdsds.Length; i++)
	            {
	                string assetPath = AssetDatabase.GUIDToAssetPath(texIdsds[i]);
	                window.localTextures[i] = new LocalTexture();
	                window.localTextures[i].tex = AssetDatabase.LoadAssetAtPath<Texture>(assetPath);
	                window.localTextures[i].texPath = assetPath;
	                window.localTextures[i].localMatRefs =  new List<LocalMaterial>();
	            }
	            window.localTextures = window.localTextures.OrderBy(lt => lt.tex.name).ToArray();

                string[] matsIds = AssetDatabase.FindAssets("t:material", new String[] { "Assets/ElementSpace/Artworks/ArtMasters" });
                window.localMaterials = new LocalMaterial[matsIds.Length];

                for (int i = 0; i < matsIds.Length; i++)
	            {
	                string assetPath = AssetDatabase.GUIDToAssetPath(matsIds[i]);
	                window.localMaterials[i] = new LocalMaterial();
	                window.localMaterials[i].mat = AssetDatabase.LoadAssetAtPath<Material>(assetPath);
	                window.localMaterials[i].matPath = assetPath;
	                window.localMaterials[i].serverMat =
	                    window.gameMaterials.FirstOrDefault(gm => gm.name.Equals(window.localMaterials[i].mat.name));

                    Shader shader = window.localMaterials[i].mat.shader;
                    for (int j = 0; j < ShaderUtil.GetPropertyCount(shader); j++)
                    {
                        if (ShaderUtil.GetPropertyType(shader, j) == ShaderUtil.ShaderPropertyType.TexEnv)
                        {
                            Texture texture = window.localMaterials[i].mat.GetTexture(ShaderUtil.GetPropertyName(shader, j));
                            if (texture != null)
                            {
                                LocalTexture localTex = window.localTextures.FirstOrDefault(lt => lt.tex.name.Equals(texture.name));
                                if (localTex.localMatRefs != null)
                                {
                                    localTex.localMatRefs.Add(window.localMaterials[i]);
                                }
                            }

                            
                        }
                    }
                }

                window.localMaterials = window.localMaterials.OrderBy(lm => lm.mat.name).ToArray();
	            window.badMGuiStyleat = new GUIStyle();
	            window.badMGuiStyleat.normal.textColor = Color.red;
	            window.goodMaGuiStylet = new GUIStyle();
	            window.goodMaGuiStylet.normal.textColor = Color.green;

                window.Show();
	        }
	    }



	    



	    void OnGUI()
	    {

            EditorGUILayout.BeginVertical();
            EditorGUILayout.BeginHorizontal();
            if (serverCheck)
            {
                EditorGUILayout.BeginVertical();
                EditorGUILayout.BeginHorizontal();
                GUILayout.FlexibleSpace();
                GUILayout.Label(String.Format("↓↓↓↓ MATERIALS ↓↓↓↓ "), EditorStyles.boldLabel);
                GUILayout.FlexibleSpace();
                EditorGUILayout.EndHorizontal();
                materialsScrollPoss = EditorGUILayout.BeginScrollView(materialsScrollPoss);
                foreach (var localMaterial in localMaterials)
                {
                    //var remoteProp = remoteMaterialObject.properties.FirstOrDefault(p =>
                    //    p.propName.Equals(materialShaderProperty.propertyName));
                    if (localMaterial.mat != null)
                    {
                        EditorGUILayout.BeginHorizontal();

                        if (!string.IsNullOrEmpty(localMaterial.serverMat._id))
                        {
                            GUILayout.Label(String.Format("{0}", localMaterial.mat.name), goodMaGuiStylet);
                        }
                        else
                        {
                            GUILayout.Label(String.Format("{0}", localMaterial.mat.name), badMGuiStyleat);
                        }


                        EditorGUILayout.EndHorizontal();
                    }

                    

                }
                EditorGUILayout.EndScrollView();
                EditorGUILayout.EndVertical();

                EditorGUILayout.BeginVertical();
                EditorGUILayout.BeginHorizontal();
                GUILayout.FlexibleSpace();
                GUILayout.Label(String.Format("↓↓↓↓ TEXTURES ↓↓↓↓ "), EditorStyles.boldLabel);
                GUILayout.FlexibleSpace();
                EditorGUILayout.EndHorizontal();
                texturesScrollPoss = EditorGUILayout.BeginScrollView(texturesScrollPoss);
                foreach (var localTexture in localTextures)
                {
                    //var remoteProp = remoteMaterialObject.properties.FirstOrDefault(p =>
                    //    p.propName.Equals(materialShaderProperty.propertyName));
                    if (localTexture.tex != null)
                    {
                        EditorGUILayout.BeginHorizontal();
                        if ((localTexture.localMatRefs.Count > 0))
                        {
                            GUILayout.Label(String.Format("{0}", localTexture.tex.name), goodMaGuiStylet);
                        }
                        else
                        {
                            GUILayout.Label(String.Format("{0}", localTexture.tex.name), badMGuiStyleat);
                        }


                        EditorGUILayout.EndHorizontal();
                    }


                    

                }
                EditorGUILayout.EndScrollView();
                EditorGUILayout.EndVertical();

               

                
            }
            else
            {
                EditorUtility.DisplayProgressBar("Connecting to server", "Loading Server Materials", 0.35f);
            }



            EditorGUILayout.EndHorizontal();
	        if (GUILayout.Button("DELETE BAD MATERIALS"))
	        {
	            RemoveBadMaterials();
	        }

	        if (GUILayout.Button("DELETE ORPHAN TEXTURES"))
	        {
	            RemoveOrphans();
	        }
            EditorGUILayout.EndVertical();
        }

	    void OnGetMaterialsSuccess(GameMaterials.GameMaterial[] gameMats)
	    {
	        gameMaterials = gameMats;
	        serverCheck = true;


	    }

	    void OnRequestFailed(string code)
	    {
            Debug.LogError("REQUEST FAILED "+ code);
	        serverCheck = true;

	    }

	    void RemoveBadMaterials()
	    {
	        foreach (var localMaterial in localMaterials)
	        {
	            if (string.IsNullOrEmpty(localMaterial.serverMat._id))
	            {
	                AssetDatabase.DeleteAsset(localMaterial.matPath);
	            }

	        }
	    }

	    void RemoveOrphans()
	    {
	        foreach (var localTexture in localTextures)
	        {
	            if (localTexture.localMatRefs == null || localTexture.localMatRefs.Count == 0)
	            {
	                AssetDatabase.DeleteAsset(localTexture.texPath);
	            }

	        }
	    }


    }
}
