using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using System;
using System.Text;
using Hermes;

namespace Athenea
{
	public class AnimationValidator : MonoBehaviour {

		class ValidationResult{
			public string errorMsg;
			public bool valid = true;

		}

		class ValidationItem{
			Func<KeyValuePair<AnimationClip,AnimationClip>,ValidationResult> isValid;
			//public string lastErrorMsg;

			public ValidationItem (Func<KeyValuePair<AnimationClip,AnimationClip>, ValidationResult> isValid)
			{
				this.isValid = isValid;
			}

			public ValidationResult IsValid (KeyValuePair<AnimationClip,AnimationClip> clip){ 
					return isValid (clip);
			}


		}

		static List<StringBuilder> sbs = new List<StringBuilder> ();
		static StringBuilder sb;
		private static void CacheMessage(string msg){
			if (sbs == null)
				sbs = new List<StringBuilder> ();
			if (sbs.Count == 0)
				sbs.Add (new StringBuilder ());
			if (sbs [sbs.Count - 1].Length > 31000) {
				sbs.Add (new StringBuilder ());
			}
			sbs [sbs.Count - 1].AppendLine (msg);
		}

		[MenuItem("Assets/Validate Animation Overrides")]
		public static void ValidateAnimations(){
			
			AnimationValidator.sbs = new List<StringBuilder> ();
			//UnityEngine.Object[] allObjects =  AssetDatabase.LoadAllAssetsAtPath (AssetDatabase.GetAssetPath (Selection.activeObject)+"/");
			string[] animControllers = AssetDatabase.FindAssets ("t:AnimatorOverrideController", new string[]{AssetDatabase.GetAssetPath (Selection.activeObject)} );
			Debug.Log ("STARTING VALIDATING PROCESS!");
			//StringBuilder sb = new StringBuilder ();
			for (int i = 0; i < animControllers.Length; i++) {
				
				AnimatorOverrideController aoc = AssetDatabase.LoadAssetAtPath<AnimatorOverrideController> (AssetDatabase.GUIDToAssetPath (animControllers [i]));
				
				List<KeyValuePair<AnimationClip,AnimationClip>> allClips = new List<KeyValuePair<AnimationClip, AnimationClip>>();
				aoc.GetOverrides(allClips);

				StringBuilder aocSb = new StringBuilder ();
				foreach (var acp in allClips) {
					if (acp.Value != null) {
						string oriName = acp.Key.name;
						string oveName = acp.Value.name;
						if (oriName.Equals (oveName)) {
							//Debug.Log (aoc.name + " : " + oriName + " NO overrided");
						} else {
							//Debug.Log (aoc.name + " : " + oriName + " overrided , Validating");
							ValidationResult vr = ValidateAnimation (acp);

							if (vr.valid) {
								//Debug.Log ("All good");
							} else {
								
								aocSb.AppendLine (acp.Key.name + " using override ("+acp.Value.name+") problem -> " + vr.errorMsg);
								//Debug.Log ("PROBLEM WITH " + aoc.name + " IN " + acp.originalClip.name);
							}
							//Debug.Log (acp.originalClip.name + " ---- " + acp.overrideClip.name);
						}


					} else {
						CacheMessage ("*CONTROLLER : " + aoc.name+"*");
						CacheMessage (acp.Key.name + " problem -> HAS A NULL CLIP OVERRIDED");
					}

				}
				if(!string.IsNullOrEmpty(aocSb.ToString())){
					CacheMessage ("*CONTROLLER : " + aoc.name+"*");
					CacheMessage (aocSb.ToString());
				}
			}
			Debug.Log ("FINISHING VALIDATING PROCESS!");
			if (AnimationValidator.sbs.Count == 1) {
				HermesLogger.LogSlack(AnimationValidator.sbs[0].ToString ());
			} else {
				for (int i = 0; i < AnimationValidator.sbs.Count; i++) {
					HermesLogger.LogSlack ("LOG PART " + (i + 1).ToString () + " OF " + AnimationValidator.sbs.Count);
					HermesLogger.LogSlack(AnimationValidator.sbs[i].ToString ());
				}
			}


		}

		private static ValidationResult ValidateAnimation(KeyValuePair<AnimationClip,AnimationClip> acp){
			ValidationResult stacked = new ValidationResult ();
			for (int i = 0; i < validators.Length; i++) {
				ValidationResult vr = validators [i].IsValid (acp);
				if (!vr.valid) {
					stacked.errorMsg = vr.errorMsg + "\n";
				}
				stacked.valid = stacked.valid  && vr.valid;
			}
			return stacked;

		}


		 


		static ValidationItem[] validators = new ValidationItem[] {
			new ValidationItem ((clip) => { // AimWeight Anim
				ValidationResult vr = new ValidationResult();
				if (clip.Key.name.ToUpper().Contains ("AIM")) {
					EditorCurveBinding[] curves = AnimationUtility.GetCurveBindings (clip.Value);
					for (int i = 0; i < curves.Length; i++) {
						if(curves [i].propertyName.Equals("AimWeight")){
							vr.valid = true;
							return vr;	
						}
					}
					vr.errorMsg = "DOES NOT CONTAIN AimWeight curve";
					vr.valid = false;
					return vr;

				}
				vr.valid = true;
				return vr;
			}),//
			new ValidationItem((clip) => { //WeaponToggle
				ValidationResult vr = new ValidationResult();
				if (clip.Key.name.ToUpper().Contains ("SWITCHWEAPON")) {
					AnimationEvent[] events = clip.Value.events;
					for(int i = 0; i < events.Length; i++){
						if(events[i].functionName.Equals("WeaponToggle")){
							vr.valid = true;
							return vr;	
						}
					}
					vr.errorMsg = "DOES NOT CONTAIN WeaponToggle event";
					vr.valid = false;
					return vr;

				}
				vr.valid = true;
				return vr;

			}),//
			new ValidationItem((clip) => { //MeleeCombo Events
				ValidationResult vr = new ValidationResult();
				if(clip.Key.name.ToUpper().Contains("MELEECOMBO")){
					AnimationEvent[] events = clip.Value.events;
					for(int i = 0; i < events.Length; i++){
						if(events[i].functionName.Equals("MeleeAttack")){
							vr.valid = true;
							return vr;	
						}
					}
					vr.errorMsg = "DOES NOT CONTAIN MeleeAttack event";
					vr.valid = false;
					return vr;

				}
				vr.valid = true;
				return vr;
			}),
			new ValidationItem((clip) => { // Idle, Walking, Standing, Running Loop events
				string orNameUpper = clip.Key.name.ToUpper();
				ValidationResult vr = new ValidationResult();
				if(orNameUpper.Contains("IDLE") || orNameUpper.Contains("WALKING") || orNameUpper.Contains("STANDING") || orNameUpper.Contains("RUNNING") && ( !orNameUpper.Contains("EXIT") && !orNameUpper.Contains("ENTER")) ){

					if(clip.Value.isLooping){
						vr.valid = true;
						return vr;
					}else{
						vr.errorMsg = "IS NOT LOOPING!";
						vr.valid = false;
						return vr;
					}
				}
				vr.valid = true;
				return vr;
			}),
			new ValidationItem((clip) => { // EXIT , ENTER Loop Validation
				string orNameUpper = clip.Key.name.ToUpper();
				ValidationResult vr = new ValidationResult();
				if(orNameUpper.Contains("EXIT") || orNameUpper.Contains("ENTER")){

					if(!clip.Value.isLooping){
						vr.valid = true;
						return vr;
					}else{
						vr.errorMsg = "IS LOOPING!";
						vr.valid = false;
						return vr;
					}
				}
				vr.valid = true;
				return vr;
			}),
			new ValidationItem ((clip) => { // AIM Anim name
				ValidationResult vr = new ValidationResult();
				if (clip.Key.name.ToUpper().Contains ("AIM")) {
					if(clip.Value.name.ToUpper().Contains("AIM")){
						vr.valid = true;
						return vr;
					}else{
						vr.errorMsg = "FUNNY NAME! DOES NOT CONTAIN 'AIM'";
						vr.valid = false;
						return vr;
					}
				}
				vr.valid = true;
				return vr;
			})


		};
	}
		
}
