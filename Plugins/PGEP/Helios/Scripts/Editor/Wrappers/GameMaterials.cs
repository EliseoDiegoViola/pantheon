using System.IO;
using Debug = UnityEngine.Debug;
using System.Net;
using SimpleJSON2;
using UnityEditor;
using UnityEngine;
using Athenea;
using System;
using System.Text;

namespace Helios
{

    public class GameMaterials
    {
        public struct MaterialProperties
        {
            public string propName;
            public string propValue;
            public string propType;

            public MaterialProperties(string propName, string propValue, string propType)
            {
                this.propName = propName;
                this.propValue = propValue;
                this.propType = propType;
            }
        }

        public struct GameMaterial
        {
            public string _id;
            public string user;
            public string name;
            public string shaderName;
            public string project;
            public MaterialProperties[] properties;

            public GameMaterial(JSONObject gameMaterial)
            {
                if (gameMaterial != null)
                {
                    this._id = gameMaterial["id"].Value;
                    this.user = gameMaterial["user"].Value;
                    this.name = gameMaterial["name"].Value;
                    this.shaderName = gameMaterial["shaderName"].Value;
                    this.project = gameMaterial["project"].Value;
                    JSONArray props = gameMaterial["properties"].AsArray;
                    MaterialProperties[] matProps = new MaterialProperties[props.Count];
                    for (int i = 0; i < props.Count; i++)
                    {
                        matProps[i] = new MaterialProperties(props[i].AsObject["propName"].Value, props[i].AsObject["propValue"].Value, props[i].AsObject["propType"].Value);
                    }

                    this.properties = matProps;
                }
                else
                {
                    this._id = null;
                    this.user = null;
                    this.name = null;
                    this.shaderName = null;
                    this.project = null;
                    this.properties = new MaterialProperties[0];
                }
            }

            public GameMaterial(string json) : this(JSON.Parse(json).AsObject){

            }
        }
        
        public static GameMaterial[] GetListGameMaterials_Sync()
        {
            string baseUrl = ServerConfig.URL + ":" + ServerConfig.PORT + "/gameMaterials";


            var httpWebRequest = (HttpWebRequest)WebRequest.Create(baseUrl);
            httpWebRequest.Method = "GET";
            httpWebRequest.ContentType = "application/json";

            var httpResponse = (HttpWebResponse)httpWebRequest.GetResponse();
            if (httpResponse.StatusCode == HttpStatusCode.OK)
            {
                using (var streamReader = new StreamReader(httpResponse.GetResponseStream()))
                {
                    var result = streamReader.ReadToEnd();
                    JSONArray allMaterials = JSON.Parse(result).AsArray;
                    GameMaterial[] materials = new GameMaterial[allMaterials.Count];
                    for (int i = 0; i < allMaterials.Count; i++)
                    {
                        JSONObject gameterial = allMaterials[i].AsObject;
                        materials[i] = new GameMaterial(gameterial);
                    }

                    return materials;
                }
            }
            else
            {
                Debug.LogError(httpResponse.StatusCode.ToString());
                return null;
            }
        }

        public static GameMaterial UploadMaterialData_Sync(string matData)
        {
            string baseUrl = ServerConfig.URL + ":" + ServerConfig.PORT + "/gameMaterials";
            Debug.Log(matData);
            var data = Encoding.ASCII.GetBytes(matData);

            var httpWebRequest = (HttpWebRequest)WebRequest.Create(baseUrl);
            httpWebRequest.Method = "POST";
            httpWebRequest.ContentType = "application/json";
            httpWebRequest.ContentLength = data.Length;

            using (var stream = httpWebRequest.GetRequestStream())
            {
                stream.Write(data, 0, data.Length);
            }

            

            var httpResponse = (HttpWebResponse)httpWebRequest.GetResponse();
            if (httpResponse.StatusCode == HttpStatusCode.OK)
            {
                using (var streamReader = new StreamReader(httpResponse.GetResponseStream()))
                {
                    var result = streamReader.ReadToEnd();
                    GameMaterial gmat = new GameMaterial(result);
                    return gmat;
                }
            }
            else
            {
                Debug.LogError(httpResponse.StatusCode);
                return new GameMaterial();
            }

             

            
        }

        public static GameMaterial GetGameMaterialByID_Sync(string uuid)
        {
            string baseUrl = String.Format("{0}:{1}/gameMaterials/{2}",ServerConfig.URL,ServerConfig.PORT, uuid);


            var httpWebRequest = (HttpWebRequest)WebRequest.Create(baseUrl);
            httpWebRequest.Method = "GET";
            httpWebRequest.ContentType = "application/json";


            var httpResponse = (HttpWebResponse)httpWebRequest.GetResponse();
            if (httpResponse.StatusCode == HttpStatusCode.OK)
            {
                using (var streamReader = new StreamReader(httpResponse.GetResponseStream()))
                {
                    var result = streamReader.ReadToEnd();
                    GameMaterial gmat = new GameMaterial(result);
                    return gmat;
                }
            }
            else
            {
                Debug.LogError(httpResponse.StatusCode);
                return new GameMaterial();
            }
        }

        public static GameMaterial GetGameMaterialByName_Sync(string name)
        {
            string baseUrl = String.Format("{0}:{1}/gamematerials/filterby/name/{2}", ServerConfig.URL, ServerConfig.PORT, name);
            Debug.Log(baseUrl);

            var httpWebRequest = (HttpWebRequest)WebRequest.Create(baseUrl);
            httpWebRequest.Method = "GET";
            httpWebRequest.ContentType = "application/json";


            var httpResponse = (HttpWebResponse)httpWebRequest.GetResponse();
            if (httpResponse.StatusCode == HttpStatusCode.OK)
            {
                using (var streamReader = new StreamReader(httpResponse.GetResponseStream()))
                {
                    var result = streamReader.ReadToEnd();
                    if (string.IsNullOrEmpty(result))
                    {
                        return new GameMaterial();
                    }
                    else
                    {
                        GameMaterial gmat = new GameMaterial(result);
                        return gmat;
                    }

                    
                }
            }
            else
            {
                Debug.LogError(httpResponse.StatusCode);
                return new GameMaterial();
            }
        }



        public static GameMaterial ModifyMaterialData_Sync(string uuid, string matData)
        {
            string baseUrl = String.Format("{0}:{1}/gameMaterials/{2}", ServerConfig.URL, ServerConfig.PORT, uuid);

            var data = Encoding.ASCII.GetBytes(matData);

            var httpWebRequest = (HttpWebRequest)WebRequest.Create(baseUrl);
            httpWebRequest.Method = "POST";
            httpWebRequest.ContentType = "application/json";
            httpWebRequest.ContentLength = data.Length;

            using (var stream = httpWebRequest.GetRequestStream())
            {
                stream.Write(data, 0, data.Length);
            }

            var httpResponse = (HttpWebResponse)httpWebRequest.GetResponse();
            if (httpResponse.StatusCode == HttpStatusCode.OK)
            {
                using (var streamReader = new StreamReader(httpResponse.GetResponseStream()))
                {
                    var result = streamReader.ReadToEnd();
                    GameMaterial gmat = new GameMaterial(result);
                    return gmat;
                }
            }
            else
            {
                Debug.LogError(httpResponse.StatusCode);
                return new GameMaterial();
            }
        }

        [MenuItem("Assets/Pantheon/Helios/Upload Material", validate = true)]
        public static bool IsValidMaterial()
        {
            for (int i = 0; i < Selection.objects.Length; i++)
            {
                if (!(Selection.objects[i] is Material))
                    return false;
            }
            return true;
        }

        [MenuItem("Assets/Pantheon/Helios/Upload Material", validate = false)]
        public static void GetMaterialInformation()
        {
            for (int i = 0; i < Selection.objects.Length; i++)
            {

                var matJson = CollectMaterialData(Selection.objects[i] as Material);
                //Debug.Log(matJson.ToString());
                GameMaterialWindow.Init(matJson);
                //File.WriteAllText(Application.dataPath.Replace("Assets", "ShaderExport.json"), matJson.ToString());
                //UploadMaterialData(matJson.ToString(), (s) => Debug.Log(s), () => Debug.LogError("WRONG"));
            }
            
        }

        public static JSONObject CollectMaterialData(Material m)
        {
            var matJson = ShaderDataDigest.MaterialInstanceToJson(m);
            matJson.Add("user", System.Environment.MachineName);
            matJson.Add("project", Pantheon.PantheonConfig.Project);
            var texturePreview = AssetPreview.GetAssetPreview(m);
            var thumbnailBytes = texturePreview.EncodeToPNG();
            if(thumbnailBytes != null){
                string basee64ThumbnailEncoded = System.Convert.ToBase64String(thumbnailBytes);
                matJson.Add("thumbnail", basee64ThumbnailEncoded);
            }else{
                matJson.Add("thumbnail", "");
            }

            return matJson;
        }




    }
}
