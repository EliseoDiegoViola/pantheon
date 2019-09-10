using System.IO;
using Debug = UnityEngine.Debug;
using System.Net;
using SimpleJSON2;

namespace Helios {
    public class ErrorLogs
    {


        public struct ErrorLog
        {
            public string user;
            public string level;
            public string action;
            public string filename;
            public int errorCode;
            public string errorMessage;
        }

        public static void CreateLogError(ErrorLog log)
        {
            log.user = System.Security.Principal.WindowsIdentity.GetCurrent().Name;
            log.action = "Import";
            string baseUrl = ServerConfig.URL + ":" + ServerConfig.PORT + "/errorLogs";


            var httpWebRequest = (HttpWebRequest)WebRequest.Create(baseUrl);
            httpWebRequest.ContentType = "application/json";
            httpWebRequest.Method = "POST";

            using (var streamWriter = new StreamWriter(httpWebRequest.GetRequestStream()))
            {
                JSONObject logJson = new JSONObject();
                logJson.Add("user", log.user);
                logJson.Add("filename", log.filename);
                logJson.Add("action", log.action);
                logJson.Add("level", log.level);
                logJson.Add("errorCode", log.errorCode);
                logJson.Add("errorMessage", log.errorMessage);

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

        public static string GetListErrorLog()
        {
            string baseUrl = ServerConfig.URL + ":" + ServerConfig.PORT + "/errorLogs";


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
