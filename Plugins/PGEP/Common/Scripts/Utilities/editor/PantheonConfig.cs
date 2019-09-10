using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using UnityEditor.Callbacks;
using SimpleJSON2;
using System.IO;

namespace Pantheon{

	[InitializeOnLoadAttribute]
	public class PantheonConfig{

		public static string Project = "";
		public static string Local_Artmasters_Path = "";


		static PantheonConfig(){
			//Debug.Log("Project");
			
			var settingsFile = new StreamReader(Application.dataPath+"/Pantheon/Project.settings");
			
			JSONObject settings = JSON.Parse(settingsFile.ReadToEnd()).AsObject;
			Project = settings["project_name"];
			Local_Artmasters_Path = settings["local_artmasters_path"];
			//Debug.Log(Project);

			settingsFile.Close(); 
		} 
	}
}