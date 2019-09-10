using System;
using System.Diagnostics;
using System.Linq;
using Hermes;
using UnityEditor;
using Debug = UnityEngine.Debug;

namespace Pantheon.Daedalus
{
    public class GameBuilder
    {
        //[MenuItem("Assets/CheckVersioning")]
        public static void CheckVersioning()
        {
            UpdateVersionFile("0");
        }

        public static void UpdateVersionFile(string versionNumber)
        {
             
                /*BuildVersioningData versioningData;
                BuildVersioningData[] datas = ErgoDataSerializer.Load<BuildVersioningData>(AppSettings.FilePath_BuildVersioning);

                if (datas == null)
                {
                    versioningData = new BuildVersioningData();
                }
                else
                {
                    versioningData = datas.FirstOrDefault();
                }

                if (versionNumber.Equals("0"))
                {
                    //SetVersionByGit(versioningData);
                    SetVersionByServer(versioningData);
                    
                }
                else
                {
                    int[] versions = versionNumber.Split('.').Select(int.Parse).ToArray();
                    versioningData.majorNumber = versions[0];
                    versioningData.minorNumber = versions[1];
                    versioningData.patchNumber = 0;
                }


            try
            {
                var procHash = new Process
                {
                    StartInfo = new ProcessStartInfo
                    {
                        FileName = "git",
                        Arguments = @"rev-parse HEAD",
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        CreateNoWindow = true
                    }
                };

                procHash.Start();
                while (!procHash.StandardOutput.EndOfStream)
                {
                    string commitHash = procHash.StandardOutput.ReadLine();
                    versioningData.commitHash = commitHash;
                }

            }
            catch (Exception e)
            {
                versioningData.commitHash = "error getting commit number";
                Debug.LogError(e.ToString());
            }



            HermesLogger.LogSlack(String.Format("Building version {0}.{1}.{2} from the commit {3}", versioningData.majorNumber, versioningData.minorNumber, versioningData.patchNumber, versioningData.commitHash), HermesLogger.ReportLevel.GOOD);


            //ErgoDataSerializer.Save(AppSettings.FilePath_BuildVersioning, versioningData);
            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();
           */
        }

        private static void SetVersionByGit()
        {
            /*var procCount = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "git",
                    Arguments = @"rev-list --count HEAD",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    CreateNoWindow = true
                }
            };

            procCount.Start();
            while (!procCount.StandardOutput.EndOfStream)
            {
                string commitCount = procCount.StandardOutput.ReadLine();

                int[] versions = commitCount.SplitInParts(2).Select(int.Parse).ToArray();
                versioningData.majorNumber = versions[0];
                versioningData.minorNumber = versions[1];
                versioningData.patchNumber = versions[2];
            }*/
        }

        private static void SetVersionByServer()
        {

            /*var version = Helios.Versioning.GetServerVersioning();
            if (version != null)
            {
                int[] versions = version.Split('.').Select(int.Parse).ToArray();
                versioningData.majorNumber = versions[0];
                versioningData.minorNumber = versions[1];
                versioningData.patchNumber = versions[2];
            }
            else
            {
                versioningData.majorNumber = -1;
                versioningData.minorNumber = -1;
                versioningData.patchNumber = -1;
            }*/


        }
    }
}


