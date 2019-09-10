using System;
using System.ComponentModel;
using System.IO;
using System.Net;

namespace Helios
{

    public class FTPService
    {
        private const string ftpUser = "apolo";
        private const string ftpPass = "sixthvowel2018";
        private const string ftpServer = "sv-server";

        public static void UploadFileSync(FileInfo fi, string savePath)
        {
            try
            {

                if (!FtpDirectoryExists(string.Format(@"ftp://{0}/ftp/files/{1}/", ftpServer, savePath)))
                {
                    FtpCreateDirectory(string.Format(@"ftp://{0}/ftp/files/{1}", ftpServer, savePath));
                }

                FtpWebRequest request =
                    WebRequest.Create(new Uri(string.Format(@"ftp://{0}/ftp/files/{1}/{2}", ftpServer, savePath, fi.Name))) as
                        FtpWebRequest;
                request.Method = WebRequestMethods.Ftp.UploadFile;
                request.UseBinary = true;
                request.UsePassive = true;
                request.KeepAlive = true;
                request.Credentials = new NetworkCredential(ftpUser, ftpPass);
                //request.ConnectionGroupName = "group";


                using (FileStream fs = File.OpenRead(fi.FullName))
                {
                    byte[] buffer = new byte[fs.Length];
                    fs.Read(buffer, 0, buffer.Length);
                    fs.Close();
                    Stream requestStream = request.GetRequestStream();
                    requestStream.Write(buffer, 0, buffer.Length);
                    requestStream.Flush();
                    requestStream.Close();
                }
            }
            catch (Exception ex)
            {
                Console.Write(ex.ToString());
                Console.WriteLine(string.Format("Error on FTPService: message:{0} \n exception:{1}", ex.Message, ex.StackTrace));
            }
        }

        private static void UploadCompleted(object sender, UploadFileCompletedEventArgs e)
        {
            Console.WriteLine(string.Format("{0} FINISHED", e.ToString()));
        }

        private static void UploadProgress(object sender, UploadProgressChangedEventArgs e)
        {
            Console.WriteLine(string.Format("Upload progress is {0}", e.ProgressPercentage));
        }

        public static FileInfo DownloadFileSync(string filename, string folder, DirectoryInfo storageFolder)
        {
            if (!Directory.Exists(storageFolder.FullName))
            {
                Directory.CreateDirectory(storageFolder.FullName);
            }
            using (WebClient client = new WebClient())
            {
                client.Credentials = new NetworkCredential(ftpUser, ftpPass);
                client.DownloadFileCompleted += DownloadCompleted;
                client.DownloadProgressChanged += DownloadProgress;
                client.DownloadFile(string.Format(@"ftp://{0}/ftp/files/{1}/{2}", ftpServer, folder, filename), storageFolder.FullName + "/" + filename);
            }
            return new FileInfo(storageFolder.FullName + "/" + filename);
        }

        private static void DownloadProgress(object sender, DownloadProgressChangedEventArgs e)
        {
            Console.WriteLine(string.Format("Download progress is {0}", e.ProgressPercentage));

        }

        private static void DownloadCompleted(object sender, AsyncCompletedEventArgs e)
        {
            Console.WriteLine(string.Format("{0} FINISHED", e.ToString()));
        }

        private static bool FtpDirectoryExists(string directoryPath)
        {
            bool IsExists = true;
            try
            {
                FtpWebRequest request = (FtpWebRequest)WebRequest.Create(directoryPath);
                request.Credentials = new NetworkCredential(ftpUser, ftpPass);
                request.Method = WebRequestMethods.Ftp.PrintWorkingDirectory;

                using (var response = (FtpWebResponse)request.GetResponse())
                {
                    Console.WriteLine(response.StatusCode);
                }
            }
            catch (WebException ex)
            {
                Console.Write(ex.ToString());
                IsExists = false;
            }
            return IsExists;
        }

        private static string FtpCreateDirectory(string directoryPath)
        {
            FtpWebRequest request = (FtpWebRequest)WebRequest.Create(directoryPath);
            request.Method = WebRequestMethods.Ftp.MakeDirectory;
            request.Credentials = new NetworkCredential(ftpUser, ftpPass);
            using (var resp = (FtpWebResponse)request.GetResponse())
            {
                Console.WriteLine(resp.StatusCode);
            }

            return directoryPath;

        }

    }

}
