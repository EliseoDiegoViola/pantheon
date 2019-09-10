using System.IO;
using Debug = UnityEngine.Debug;
using System.Net;
using SimpleJSON2;

namespace Helios
{
    public class ExportLogs
    {

        //const string serverUrl = "http://sv-server:13370/";

        public struct ExportData {
            public string name;
            public string exportType;
            public string exportSubType;

            public ExportData(string name, string exportType, string exportSubType)
            {
                this.name = name;
                this.exportType = exportType;
                this.exportSubType = exportSubType;
            }
        }

        public struct ExportLog {
            public string user;
            public string filename;
            public string action;
            public string command;
            public ExportData[] objects;
        }

        public static void CreateLogExport(ExportLog log)
        {
            log.user = System.Security.Principal.WindowsIdentity.GetCurrent().Name;
            log.action = "Import";
            string baseUrl = ServerConfig.URL + ":" + ServerConfig.PORT + "/exportLogs";


            var httpWebRequest = (HttpWebRequest)WebRequest.Create(baseUrl);
            httpWebRequest.ContentType = "application/json";
            httpWebRequest.Method = "POST";

            using (var streamWriter = new StreamWriter(httpWebRequest.GetRequestStream()))
            {
                JSONObject logJson = new JSONObject();
                logJson.Add("user", log.user);
                logJson.Add("filename", log.filename);
                logJson.Add("action", log.action);
                logJson.Add("command", log.command);
                JSONArray objects = new JSONArray();
                foreach (var logData in log.objects) {
                    JSONObject logDataJson = new JSONObject();
                    logDataJson.Add("name", logData.name);
                    logDataJson.Add("exportType", logData.exportType);
                    logDataJson.Add("exportSubType", logData.exportSubType);
                    objects.Add(logDataJson);
                }
                logJson.Add("objects", objects);
                streamWriter.Write(logJson.ToString());
                streamWriter.Flush();
                streamWriter.Close();
     
            }

            var httpResponse = (HttpWebResponse)httpWebRequest.GetResponse();
            using (var streamReader = new StreamReader(httpResponse.GetResponseStream()))
            {
                var result = streamReader.ReadToEnd();
                Debug.Log(result);
            }
        }

        public static string GetListExportLog()
        {
            string baseUrl = ServerConfig.URL + ":" + ServerConfig.PORT + "/exportLogs";


            var httpWebRequest = (HttpWebRequest)WebRequest.Create(baseUrl);
            httpWebRequest.Method = "GET";

            var httpResponse = (HttpWebResponse)httpWebRequest.GetResponse();
            using (var streamReader = new StreamReader(httpResponse.GetResponseStream()))
            {
                var result = streamReader.ReadToEnd();
                return result;
            }
        }
    }

    
}

