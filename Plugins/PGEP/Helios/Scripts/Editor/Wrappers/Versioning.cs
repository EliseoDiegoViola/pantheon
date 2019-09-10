
using System.IO;
using System.Net;
using SimpleJSON2;
using UnityEngine;

namespace Helios
{
    public class Versioning
    {
        public static string GetServerVersioning()
        {

            string baseUrl = ServerConfig.URL + ":" + ServerConfig.PORT + "/tools/versioning/peek";

            var httpWebRequest = (HttpWebRequest)WebRequest.Create(baseUrl);
            httpWebRequest.Method = "GET";
            httpWebRequest.ContentType = "application/json";

            var httpResponse = (HttpWebResponse)httpWebRequest.GetResponse();
            if (httpResponse.StatusCode == HttpStatusCode.OK)
            {
                using (var streamReader = new StreamReader(httpResponse.GetResponseStream()))
                {
                    var result = streamReader.ReadToEnd();
                    JSONObject allMaterials = JSON.Parse(result).AsObject;

                    return allMaterials["version"].Value;
                }
            }
            else
            {
                Debug.LogError(httpResponse.StatusCode.ToString());
                return null;
            }
        }
    }
}

