using UnityEngine;
using UnityEditor;
using SimpleJSON2;

using Debug = UnityEngine.Debug;
using System.Collections.Generic;
using System.IO;

namespace Athenea
{
    public class ShaderDataDigest
    {

        public struct ShaderProperties
        {
            public string propertyName;
            public string properyType;
            public string propertyValue;
        }

        public struct MaterialDigest
        {
            public string id;
            public string materialName;
            public string shaderName;
            public ShaderProperties[] shaderProperties;
        }

        public static JSONObject ShaderToJson(Shader s)
        {
            JSONObject shaderItem = new JSONObject();
            shaderItem.Add("shaderName", new JSONString(s.name));
            int propertyCount = ShaderUtil.GetPropertyCount(s);
            JSONArray properties = new JSONArray();
            for (int j = 0; j < propertyCount; j++)
            {
                ShaderDataDigest.ShaderProperties sp = new ShaderDataDigest.ShaderProperties();
                sp.propertyName = ShaderUtil.GetPropertyName(s, j);
                sp.properyType = ShaderUtil.GetPropertyType(s, j).ToString();
                //Debug.Log(sp.properyType);
                //Debug.Log(sp.propertyName);
                //if(sp.properyType.Equals("TexEnv")){
                JSONObject propertyName = new JSONObject();

                propertyName.Add("propName", new JSONString(sp.propertyName));
                propertyName.Add("propType", new JSONString(sp.properyType));
                propertyName.Add("propValue", "");

                properties.Add(propertyName);
                //}
            }
            shaderItem.Add("properties", properties);
            return shaderItem;
        }

        public static JSONObject MaterialInstanceToJson(Material m)
        {
            JSONObject materialParsed = ShaderToJson(m.shader);
            materialParsed.Add("name", m.name);

            JSONArray materialProperties = materialParsed["properties"].AsArray;
            List<JSONNode> defaultValues = new List<JSONNode>();

            foreach (JSONNode materialProperty in materialProperties)
            {


                switch (materialProperty["propType"].Value)
                {
                    case "TexEnv":
                        if (string.IsNullOrEmpty(materialProperty["propName"].Value))
                        {
                            defaultValues.Add(materialProperty);
                            continue;
                        }
                        else
                        {
                            Texture tex = m.GetTexture(materialProperty["propName"].Value);

                            string extension = Path.GetExtension(AssetDatabase.GetAssetPath(tex));
                               
                            if (tex != null)
                            {
                                Debug.Log(tex.name + "." + extension);
                                materialProperty.Add("propValue", tex.name + extension);
                            }
                            else
                            {
                                materialProperty.Add("propValue", "");
                                defaultValues.Add(materialProperty);
                            }
                        }
                        break;
                    case "Color":
                        materialProperty.Add("propValue", m.GetColor(materialProperty["propName"].Value).ToString());
                        break;
                    case "Float":
                        materialProperty.Add("propValue", m.GetFloat(materialProperty["propName"].Value));
                        break;
                    case "Int":
                        materialProperty.Add("propValue", m.GetInt(materialProperty["propName"].Value));
                        break;
                    case "Range":
                        materialProperty.Add("propValue", m.GetFloat(materialProperty["propName"].Value));
                        break;
                    case "Vector":
                        materialProperty.Add("propValue", m.GetVector(materialProperty["propName"].Value).ToString());
                        break;
                    default:
                        materialProperty.Add("propValue", "");
                        break;
                }
            }

            foreach (JSONNode defaultValue in defaultValues)
            {
                materialProperties.Remove(defaultValue);

            }

            return materialParsed;

        }

        public static MaterialDigest MaterialDataDigest(JSONObject material)
        {
            JSONArray materialArray = new JSONArray();
            materialArray.Add(material);

            return MaterialDataDigest(materialArray)[0];

        }


        public static MaterialDigest[] MaterialDataDigest(JSONArray materials)
        {
            MaterialDigest[] allMaterials = new MaterialDigest[materials.Count];
            for (int i = 0; i < materials.Count; i++)
            {
                MaterialDigest matDig = new MaterialDigest();
                JSONObject materialItem = materials[i].AsObject;
                JSONArray materialProperties = materialItem["properties"].AsArray;

                matDig.id = materialItem["id"].Value;
                matDig.shaderName = materialItem["shaderName"].Value;
                matDig.materialName = materialItem["name"].Value;
                matDig.shaderProperties = new ShaderProperties[materialProperties.Count];
                for (int j = 0; j < materialProperties.Count; j++)
                {
                    JSONObject propertyItem = materialProperties[j].AsObject;
                    matDig.shaderProperties[j] = new ShaderProperties();
                    matDig.shaderProperties[j].propertyName = propertyItem["propName"].Value;
                    matDig.shaderProperties[j].propertyValue = propertyItem["propValue"].Value;
                    matDig.shaderProperties[j].properyType = propertyItem["propType"].Value;
                }
                allMaterials[i] = matDig;
            }
            return allMaterials;
        }

        public static string GetMaterialNameByID(JSONArray materials, string id)
        {
            for (int i = 0; i < materials.Count; i++)
            {
                if (materials[i].AsObject["id"].Value == id)
                {
                    return materials[i].AsObject["name"].Value;
                }
            }
            Debug.LogError("Material Not Found");
            return null;
        }
    }

}

