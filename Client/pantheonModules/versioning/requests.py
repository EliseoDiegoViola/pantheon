import json
try:
    from urllib import request as url
except ImportError:
    print("Using Python 2.x URL module")
    import urllib2 as url


SVurl = "http://sv-server:13370/tools/data/version"

class Requests():

    def __init__(self):
        self.serverVersions = self.loadToolVersions()

    def loadToolVersions(self):
        versions = json.loads(url.urlopen(SVurl).read().decode("utf-8"))
        return versions

    def validateVersions(self,fileVersions):
        data = {}
        data["keys"] = {}
        for key in fileVersions:
            if key in self.serverVersions["Versions"]:
                minVersion = self.serverVersions["Versions"][key]["minVersion"]
                expectedVersion = self.serverVersions["Versions"][key]["version"]
                if fileVersions[key] < minVersion:
                    data["result"] = 1
                    data["keys"][key] = {}
                    data["keys"][key]["error"] = {}
                    data["keys"][key]["error"]["code"] = 110
                    data["keys"][key]["error"]["message"] = "ERROR : " + key + " version is lower than the minimal version required - " + str(fileVersions[key]) +" // " +  str(minVersion)
                    return data
                elif fileVersions[key] < expectedVersion:
                    data["keys"][key] = {}
                    data["keys"][key]["error"] = {}
                    data["keys"][key]["error"]["code"] = 200
                    data["keys"][key]["error"]["message"] = "WARNING : " + key + " version is lower than the expected version - " + str(fileVersions[key]) +" // " +  str(expectedVersion)
            else:
                data["result"] = 1
                data["keys"][key] = {}
                data["keys"][key]["error"] = {}
                data["keys"][key]["error"]["code"] = 100
                data["keys"][key]["error"]["message"] = "ERROR : " + key + " is not versioned in the server"
                return data
        
        data["result"] = 0
        return data

