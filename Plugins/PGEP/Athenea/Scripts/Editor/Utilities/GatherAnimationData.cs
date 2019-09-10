using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SimpleJSON2;
using UnityEditor;
using System;
using System.IO;

public class GatherAnimationData : MonoBehaviour {


	[MenuItem("Assets/Gather Infor")]
	private static void GatherInformation(){//
		

		//UnityEngine.Object[] allObjects =  AssetDatabase.LoadAllAssetsAtPath (AssetDatabase.GetAssetPath (Selection.activeObject)+"/");
		string[] anims = AssetDatabase.FindAssets ("t:Animation", new string[]{AssetDatabase.GetAssetPath (Selection.activeObject)} );




		JSONObject data = new JSONObject ();

		for (int i = 0; i < anims.Length; i++) {
			string absolutePath = Application.dataPath.Replace ("Assets", "") +  AssetDatabase.GUIDToAssetPath (anims [i]);
			//Debug.Log (Directory.GetParent (absolutePath));
			JSONObject jsonData = JSON.Parse (File.ReadAllText (Directory.GetParent (absolutePath).GetFiles ("*.jsonMeta") [0].FullName.Replace ("\\", "/"))).AsObject;
			Debug.Log (jsonData.ToString());

			JSONObject animdata = new JSONObject ();	
			ModelImporter mi = (ModelImporter)ModelImporter.GetAtPath (AssetDatabase.GUIDToAssetPath (anims [i]));
			if (mi.clipAnimations.Length != 0) {
				Debug.Log ("YAAAAY!!!!? " + AssetDatabase.GUIDToAssetPath (anims [i]));
				for (int j = 0; j < mi.clipAnimations.Length; j++) {
					JSONObject clipData = new JSONObject ();
					clipData.Add ("clipName", mi.clipAnimations [j].name);
					clipData.Add ("clipLoop", mi.clipAnimations [j].loopTime);
					clipData.Add ("clipRoot", !string.IsNullOrEmpty (mi.motionNodeName));
					JSONArray events = new JSONArray ();
					for (int k = 0; k < mi.clipAnimations [j].events.Length; k++) {
						JSONObject animEvent = new JSONObject ();
						animEvent.Add ("clipKeyEvent", mi.clipAnimations [j].events [k].functionName);
						int eventKey = (int)(mi.clipAnimations [j].events [k].time * (mi.clipAnimations [j].lastFrame - mi.clipAnimations [j].firstFrame));
						animEvent.Add ("clipKeyFrame", eventKey);
						animEvent.Add("clipKeyEventStringParameter", mi.clipAnimations[j].events[k].stringParameter);
						events.Add (animEvent);
					}
					clipData.Add ("events", events);
					animdata.Add (""+j , clipData);
				}
			} else {
				
				for (int j = 0; j < mi.defaultClipAnimations.Length; j++) {
					JSONObject clipData = new JSONObject ();
					clipData.Add ("clipName", mi.defaultClipAnimations [j].name);
					clipData.Add ("clipLoop", mi.defaultClipAnimations [j].loopTime);
					clipData.Add ("clipRoot", !string.IsNullOrEmpty (mi.motionNodeName));
					JSONArray events = new JSONArray ();
					for (int k = 0; k < mi.defaultClipAnimations [j].events.Length; k++) {
						JSONObject animEvent = new JSONObject ();
						animEvent.Add ("clipKeyEvent", mi.defaultClipAnimations [j].events [k].functionName);
						int eventKey = (int)(mi.defaultClipAnimations [j].events [k].time * (mi.defaultClipAnimations [j].lastFrame - mi.defaultClipAnimations [j].firstFrame));
						animEvent.Add ("clipKeyFrame", eventKey);
						animEvent.Add("clipKeyEventStringParameter", mi.defaultClipAnimations[j].events[k].stringParameter);
						events.Add (animEvent);
					}
					clipData.Add ("events", events);
					animdata.Add (""+j, clipData);


				}
			}

			data.Add (Path.GetFileNameWithoutExtension(AssetDatabase.GUIDToAssetPath (anims [i])) , animdata);
		}//"C:\\Users\\Programming-Tools\\Documents\\AnimDump.json"
		File.WriteAllText(System.Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + "/AnimDump.json",data.ToString ());

	}
}
