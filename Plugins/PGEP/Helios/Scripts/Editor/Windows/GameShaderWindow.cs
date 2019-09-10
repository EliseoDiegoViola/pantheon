using System;
using UnityEngine;
using UnityEditor;
using Athenea;
using SimpleJSON2;
using System.Linq;
using System.Collections.Generic;

namespace Helios
{
	public class GameShaderWindow : EditorWindow {

		Helios.GameShaders.GameShader shaderData;

		bool[] selectedProperties;
		Vector2 propertyScrollPoss;

		public static void Init(Helios.GameShaders.GameShader shader)
			{
				// Get existing open window or if none, make a new one:
				GameShaderWindow window = (GameShaderWindow) EditorWindow.GetWindow(typeof(GameShaderWindow));
				window.shaderData = shader;
				window.selectedProperties = new bool[shader.properties.Length];
				window.Show();
			}
		
		void OnGUI()
        {
			EditorGUILayout.BeginVertical();

            EditorGUILayout.BeginHorizontal();
            GUILayout.FlexibleSpace();
			EditorGUILayout.BeginHorizontal();
            GUILayout.Label(String.Format("Uploading Shader "),EditorStyles.boldLabel);
			shaderData.name = GUILayout.TextField(shaderData.name);
			GUILayout.Label(String.Format("with shader {0} , select desired fields",shaderData.shaderName),EditorStyles.boldLabel);
			EditorGUILayout.EndHorizontal();
            GUILayout.FlexibleSpace();
            EditorGUILayout.EndHorizontal();


			propertyScrollPoss = EditorGUILayout.BeginScrollView(propertyScrollPoss);
			for (int i = 0; i < shaderData.properties.Length; i++)
			{
				var item = shaderData.properties[i];
			
				EditorGUILayout.BeginHorizontal();
				selectedProperties[i] = GUILayout.Toggle(selectedProperties[i],String.Format("{0}", item.propName));
                GUILayout.FlexibleSpace();
                GUILayout.Label(String.Format("{0}", item.propType), EditorStyles.label);
				GUILayout.FlexibleSpace();
                GUILayout.Label(String.Format("{0}", item.propValue), EditorStyles.label);
                EditorGUILayout.EndHorizontal();
			}
			EditorGUILayout.EndScrollView();

			if(GUILayout.Button("Upload Shader")){
				List<Helios.GameShaders.ShaderProperties> props = new List<Helios.GameShaders.ShaderProperties>();
				for (int i = 0; i < selectedProperties.Length; i++)
				{
					if(selectedProperties[i]){
						props.Add( shaderData.properties[i]);
					}
				}
				shaderData.properties = props.ToArray();

				GameShaders.UploadShaderData_Sync(shaderData.ToJson().ToString());
				this.Close();
				//Debug.Log(shaderData.ToJson());
			}

			EditorGUILayout.EndVertical();
		}
	}
}
