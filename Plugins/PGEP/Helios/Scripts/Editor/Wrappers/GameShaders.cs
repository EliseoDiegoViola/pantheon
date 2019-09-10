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

    public class GameShaders
    {
        public struct ShaderProperties
        {
            public string propName;
            public string propValue;
            public string propType;

            public ShaderProperties(string propName, string propValue, string propType)
            {
                this.propName = propName;
                this.propValue = propValue;
                this.propType = propType;
            }

            public JSONObject ToJson(){
                JSONObject property = new JSONObject();
                property.Add("propName",propName);
                property.Add("propValue",propValue);
                property.Add("propType",propType);
                return property;
            }
        }

        public struct GameShader
        {
            public string _id;
            public string user;
            public string shaderName;
            public string project;
            public string name;
            public ShaderProperties[] properties;

            public GameShader(JSONObject gameShader)
            {
                if (gameShader != null)
                {
                    this._id = gameShader["_id"].Value;
                    this.user = gameShader["user"].Value;
                    this.shaderName = gameShader["shaderName"].Value;
                    this.project = gameShader["project"].Value;
                    this.name = gameShader["name"].Value;
                    JSONArray props = gameShader["properties"].AsArray;
                    ShaderProperties[] matProps = new ShaderProperties[props.Count];
                    for (int i = 0; i < props.Count; i++)
                    {
                        matProps[i] = new ShaderProperties(props[i].AsObject["propName"].Value, props[i].AsObject["propValue"].Value, props[i].AsObject["propType"].Value);
                    }

                    this.properties = matProps;
                }
                else
                {
                    this._id = null;
                    this.user = null;
                    this.shaderName = null;
                    this.project = null;
                    this.name = null;
                    this.properties = new ShaderProperties[0];
                }
            }

            public JSONObject ToJson(){
                JSONObject shaderJson = new JSONObject();
                shaderJson.Add("user",user);
                shaderJson.Add("shaderName",shaderName);
                shaderJson.Add("project",project);
                shaderJson.Add("name",name);
                shaderJson.Add("properties",new JSONArray());
                for (int i = 0; i < properties.Length; i++)
                {
                    
                    shaderJson["properties"].Add(properties[i].ToJson());
                }
                return shaderJson;
            }

            public GameShader(string json) : this(JSON.Parse(json).AsObject){

            }
        }
        public static GameShader[] GetListGameShaderss_Sync()
        {
            
            string baseUrl = ServerConfig.URL + ":" + ServerConfig.PORT + "/gameShaderss";


            var httpWebRequest = (HttpWebRequest)WebRequest.Create(baseUrl);
            httpWebRequest.Method = "GET";
            httpWebRequest.ContentType = "application/json";

            var httpResponse = (HttpWebResponse)httpWebRequest.GetResponse();
            if (httpResponse.StatusCode == HttpStatusCode.OK)
            {
                using (var streamReader = new StreamReader(httpResponse.GetResponseStream()))
                {
                    var result = streamReader.ReadToEnd();
                    JSONArray allShaders = JSON.Parse(result).AsArray;
                    GameShader[] shaders = new GameShader[allShaders.Count];
                    for (int i = 0; i < allShaders.Count; i++)
                    {
                        JSONObject gameterial = allShaders[i].AsObject;
                        shaders[i] = new GameShader(gameterial);
                    }

                    return shaders;
                }
            }
            else
            {
                Debug.LogError(httpResponse.StatusCode.ToString());
                return null;
            }
        }

        public static GameShader UploadShaderData_Sync(string sData)
        {
            string baseUrl = ServerConfig.URL + ":" + ServerConfig.PORT + "/gameShaders";

            var data = Encoding.ASCII.GetBytes(sData);

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
                    Debug.Log(result);
                    GameShader gShader = new GameShader(result);
                    return gShader;
                }
            }
            else
            {
                Debug.LogError(httpResponse.StatusCode);
                return new GameShader();
            }

            

            
        }

        public static GameShader GetGameShaderByID_Sync(string uuid)
        {
            string baseUrl = String.Format("{0}:{1}/gameShaders/{2}",ServerConfig.URL,ServerConfig.PORT, uuid);


            var httpWebRequest = (HttpWebRequest)WebRequest.Create(baseUrl);
            httpWebRequest.Method = "GET";
            httpWebRequest.ContentType = "application/json";


            var httpResponse = (HttpWebResponse)httpWebRequest.GetResponse();
            if (httpResponse.StatusCode == HttpStatusCode.OK)
            {
                using (var streamReader = new StreamReader(httpResponse.GetResponseStream()))
                {
                    var result = streamReader.ReadToEnd();
                    GameShader gmat = new GameShader(result);
                    return gmat;
                }
            }
            else
            {
                Debug.LogError(httpResponse.StatusCode);
                return new GameShader();
            }
        }

        public static GameShader[] GetGameShaderByProject_Sync(string name)
        {
            string baseUrl = String.Format("{0}:{1}/gameShaders/filterby/project/{2}", ServerConfig.URL, ServerConfig.PORT, name);
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
                    JSONArray allShaders = JSON.Parse(result).AsArray;
                    GameShader[] shaders = new GameShader[allShaders.Count];
                    for (int i = 0; i < allShaders.Count; i++)
                    {
                        JSONObject gameterial = allShaders[i].AsObject;
                        shaders[i] = new GameShader(gameterial);
                    }
                    return shaders;
                }
            }
            else
            {
                Debug.LogError(httpResponse.StatusCode);
                return new GameShader[0];
            }
        }

        public static GameShader GetGameShaderByName_Sync(string name)
        {
            string baseUrl = String.Format("{0}:{1}/gameShaders/filterby/name/{2}", ServerConfig.URL, ServerConfig.PORT, name);
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
                        return new GameShader();
                    }
                    else
                    {
                        GameShader gmat = new GameShader(result);
                        return gmat;
                    }

                    
                }
            }
            else
            {
                Debug.LogError(httpResponse.StatusCode);
                return new GameShader();
            }
        }



        public static GameShader ModifyMaterialData_Sync(string uuid, string matData)
        {
            string baseUrl = String.Format("{0}:{1}/gameShaders/{2}", ServerConfig.URL, ServerConfig.PORT, uuid);

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
                    GameShader gmat = new GameShader(result);
                    return gmat;
                }
            }
            else
            {
                Debug.LogError(httpResponse.StatusCode);
                return new GameShader();
            }
        }

        [MenuItem("Assets/Pantheon/Helios/Upload Shader", validate = true)]
        public static bool IsValidMaterial()
        {
            for (int i = 0; i < Selection.objects.Length; i++)
            {
                if (!(Selection.objects[i] is Shader))
                    return false;
            }
            return true;
        }


        [MenuItem("Assets/Pantheon/Helios/Upload Shader", validate = false)]
        public static void GetMaterialInformation()
        {
            for (int i = 0; i < Selection.objects.Length; i++)
            {        
                Shader shader = Selection.objects[i] as Shader;        
                JSONObject shaderItem = ShaderDataDigest.ShaderToJson(shader);
                shaderItem.Add("user", System.Environment.MachineName);
                shaderItem.Add("name", "NewShader");
                shaderItem.Add("project", Pantheon.PantheonConfig.Project);
                //Debug.Log(shaderItem);
                
                GameShaderWindow.Init(new GameShader(shaderItem));
                //GameShader gShader = new GameShader(shaderItem);
                //UploadShaderData_Sync(shaderItem.ToString());
            }
            
        }
    }
}
