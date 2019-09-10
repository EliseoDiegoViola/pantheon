using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System;
using System.IO;
using SimpleJSON2;

namespace Pantheon
{
	public static class PathsBuilder{
		private const string RelativeDataPathDirectory = "/Data/";

		private const string ObjectsDataDirectory = "/Objects/";
		private const string ProjectsDataDirectory = "/Project/";


		private const string AteneaDataExtension = ".atnd";
		private const string PathsFile = "athenea.paths";

		private static string artmastersPath = null;
		public static string ArtmastersPath {
			get{
				
				if(string.IsNullOrEmpty(artmastersPath)){
					InitializePaths();
				}
				return artmastersPath;
			}
		}
		 
		private static Dictionary<string,string> paths;

		private static string ateneaRoot = "";
		private static string AteneaRoot {
			get{ 
				if (string.IsNullOrEmpty (ateneaRoot)) {
					string[] paths = Directory.GetFiles (Application.dataPath, "Athenea.root", SearchOption.AllDirectories);
					if (paths.Length == 1) {
						ateneaRoot = Path.GetDirectoryName(paths [0]);
					} else {
						Debug.LogError ("Multiple Athenea installations found?");
						for (int i = 0; i < paths.Length; i++) {
							Debug.LogError (paths [i]);
						}
					}
				}

				return ateneaRoot;
			}
		}

		private static string PathCombine(string path1, string path2)
		{
			if (Path.IsPathRooted(path2))
			{
				path2 = path2.TrimStart(Path.DirectorySeparatorChar);
				path2 = path2.TrimStart(Path.AltDirectorySeparatorChar);
			}

			return Path.Combine(path1, path2);
		}

		private static string PathCombine(params string[] paths )
		{
			string finalPath = "";
			for (int i = 0; i < paths.Length; i++) {
				finalPath = PathCombine (finalPath, paths [i]);
			}
			return finalPath;
		}



		public static string GetData(string dataName){
			string pathToData = GetPathToData (dataName);
			return File.ReadAllText (pathToData);
		}

		public static string GetPathToData(string dataName){
			string pathToData = PathCombine (AteneaRoot, RelativeDataPathDirectory, ObjectsDataDirectory, dataName + AteneaDataExtension);
			return pathToData;
		}

		private static void InitializePaths(){
			string pathToData = PathCombine (AteneaRoot, RelativeDataPathDirectory, ProjectsDataDirectory,PathsFile);

			if (File.Exists (pathToData)) {
				string data = File.ReadAllText (pathToData);
				JSONObject rootFile = JSONObject.Parse (data).AsObject;

				JSONArray pathsArray = rootFile ["paths"].AsArray;
				paths = new Dictionary<string, string> ();
				artmastersPath = rootFile ["artmaster"].Value;
				for (int i = 0; i < pathsArray.Count; i++) {
					JSONObject pathData = pathsArray [i].AsObject;
					paths.Add (pathData ["dataName"], pathData["dataValue"]);
				}
			} else {
				Debug.LogError ("No paths file");
			}


		}

		public static string GetPathToFile(string name){
			if (paths == null) {
				InitializePaths ();
			}
			return paths [name];
		}

	
	
	}
}
