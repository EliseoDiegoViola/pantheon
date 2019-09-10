using System.Linq;
using Apollo;
using Hermes;
using UnityEngine;

namespace Pantheon.Daedalus
{
    public class CommandRunner 
    {

        public static void RunBuildFromCommand()
        {

            string presetName = null;
            bool loadAllBakes = false;
            string versionNumber = "0";

            HermesLogger.LogSlack("Started remote Building process", HermesLogger.ReportLevel.GOOD);
            string[] commands = System.Environment.GetCommandLineArgs();
            string presetNameCommand = commands.FirstOrDefault(com => com.Contains("presetName="));
            if (presetNameCommand != null)
            {
                presetName = presetNameCommand.Replace("presetName=", "");
                if (!string.IsNullOrEmpty(presetName))
                {
                    presetName = presetName.Trim();
                }
            }

            string loadBakes = commands.FirstOrDefault(com => com.Contains("loadBakes="));
            if (loadBakes != null)
            {
                string bakesFlag = loadBakes.Replace("loadBakes=", "");
                if (!string.IsNullOrEmpty(bakesFlag))
                {
                    loadAllBakes = bool.Parse(bakesFlag.Trim().ToLower());
                }
            }

            string versionCommand = commands.FirstOrDefault(com => com.Contains("versionCommand="));
            if (versionCommand != null)
            {
                string vesionNumberValue = versionCommand.Replace("versionCommand=", "");
                if (!string.IsNullOrEmpty(vesionNumberValue))
                {
                    versionNumber = vesionNumberValue.Trim();
                }
            }

            if (presetName == null)
            {
                HermesLogger.LogSlack("Cant Build game without 'presetname' parameter",HermesLogger.ReportLevel.ERROR);
                return;
            }


            if (loadAllBakes)
            {
                ApolloRunner.ApplyAllJobsAndSave();
            }

            GameBuilder.UpdateVersionFile(versionNumber);
            //BuildPresetEditorWindow.BuildByPresetName(presetName);

            HermesLogger.LogSlack("Finished remote Building process", HermesLogger.ReportLevel.GOOD);
            Application.Quit();
        }
    }

}

