using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SimpleJSON2;


namespace Athenea
{
	public abstract class ImportedObject{


		protected string assetName;
		protected string relativePathToAsset;
		protected string absolutePathToAsset;

		protected GameObject objectRoot;
		protected string typ = "";
		protected string subTyp = "";
        protected JSONObject extraData;

        public string Typ
        {
            get
            {
                return this.typ;
            }
        }

        public string SubTyp
        {
            get
            {
                return this.subTyp;
            }
        }

        public GameObject ObjectRoot
        {
            get
            {
                return this.objectRoot;
            }
         
        }

        public JSONObject ExtraData
        {
            get
            {
                return this.extraData;
            }

        }


        public ImportedObject (string assetName, string relativePathToAsset, string absolutePathToAsset, GameObject objectRoot, string typ, string subTyp, JSONObject eData)
		{
			this.assetName = assetName;
			this.relativePathToAsset = relativePathToAsset;
			this.absolutePathToAsset = absolutePathToAsset;
			this.objectRoot = objectRoot;
			this.typ = typ;
			this.subTyp = subTyp;
            this.extraData = eData;
		}
		
        public void PreProcessObject(){
            AutoConfigurator.ConfigureObject (this);
        }
        public void PostProcessObject() {
            AutoConfigurator.PostProcess(this);
        }
		
	}
}
