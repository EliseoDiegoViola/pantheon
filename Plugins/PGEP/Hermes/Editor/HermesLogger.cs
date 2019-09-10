using System;
using System.IO;
using System.Collections.Generic;
using System.Diagnostics;
using Debug = UnityEngine.Debug;
using System.Net;
using System.Text;
using Helios;
using SimpleJSON2;

namespace Hermes
{
    public class HermesLogger
    {

        public enum ReportLevel
        {
            GOOD = 0,
            WARN = 1,
            ERROR = 2
        };
		const string serverUrl = "http://sv-server:13370/";
		private static List<PantheonException> errors = new List<PantheonException>();

		class PantheonException{

			public string message;
			public StackFrame sf;

			public PantheonException(string message,StackFrame sf){
				this.message = message;
				this.sf = sf;
			}
		}

		public static void Log(string message){
			Debug.Log(message);
			System.Text.StringBuilder sb = new System.Text.StringBuilder("-");
			sb.Append("-");
			Console.WriteLine(sb.ToString() + message);
			string myDocsPath = System.Environment.GetFolderPath(System.Environment.SpecialFolder.MyDocuments);
			string finalMessage = System.DateTime.Now.ToString() + "----" +sb.ToString() + message+"\n";
			File.AppendAllText(myDocsPath+"/Athenea.log",finalMessage);
		}
 
        public static void LogSlack(string message)
        {
            try
            {
                string baseUrl = String.Format("{0}:{1}/tools/hermes/message", ServerConfig.URL, ServerConfig.PORT);

                string header = System.Security.Principal.WindowsIdentity.GetCurrent().Name + " -- " + System.DateTime.Now.ToString();
                string fullMessage = header + "  : \n" + message;

                JSONObject jsonMessage = new JSONObject();
                jsonMessage.Add("msg", fullMessage);

                var data = Encoding.ASCII.GetBytes(jsonMessage.ToString());

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
                    }
                }
                else
                {
                    Debug.LogError(httpResponse.StatusCode);
                }
            }
            catch (Exception e)
            {
                Debug.LogError(e.ToString());
            }
        }

        public static void LogSlack(string message, ReportLevel level)
        {
            try
            {
                string baseUrl = String.Format("{0}:{1}/tools/hermes/report", ServerConfig.URL, ServerConfig.PORT);


                JSONObject jsonMessage = new JSONObject();
                jsonMessage.Add("msg", message);
                jsonMessage.Add("level", (int)level);
                jsonMessage.Add("author", Environment.MachineName);
                jsonMessage.Add("ts", System.DateTime.Now.ToLocalTime().AddHours(3).ToUnixTime());

                var data = Encoding.ASCII.GetBytes(jsonMessage.ToString());

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
                    }
                }
                else
                {
                    Debug.LogError(httpResponse.StatusCode);
                }
            }
            catch(Exception e) {
                Debug.LogError(e.ToString());
            }
        }

        public static void AddErrorToCache(string message){
			StackTrace st = new StackTrace (true);
			PantheonException ae = new PantheonException (message, st.GetFrame (1));
			errors.Add (ae);
		}

        public static string GetErrorsMsg()
        {
            if (errors.Count > 0)
            {
                StringBuilder sbMsgs = new StringBuilder();
                StringBuilder sbSts = new StringBuilder();
                for (int i = 0; i < errors.Count; i++)
                {
                    PantheonException ae = errors[i];
                    sbMsgs.AppendLine("*" + ae.message + "*");
                    sbSts.AppendLine(ae.sf.GetMethod() + "IN LINE " + ae.sf.GetFileLineNumber());
                }
                return sbMsgs.ToString() + "\n\n\n\n" + sbSts.ToString();
            }
            return "";
        }

		public static void FlushErrors(){
			if (errors.Count > 0) {                
				LogSlack (GetErrorsMsg());
			} else {
				Log ("No errors Found");
			}
			errors.Clear ();
		}



	}

}
