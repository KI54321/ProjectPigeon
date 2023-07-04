using System.Collections;
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using OVRTouchSample;
using TMPro;
using Firebase;
using Firebase.Database;
using Mapbox.Platform.Cache;
using Mapbox.Unity.Map.Interfaces;
using Mapbox.Unity.Map.Strategies;
using Mapbox.Unity.Map.TileProviders;
using Mapbox.Utils;
using System.Linq;
using Mapbox.Unity.Utilities;
using UnityEngine;
using Mapbox.Map;
using Mapbox.Unity.MeshGeneration.Factories;
using Mapbox.Unity.MeshGeneration.Data;
using System.Globalization;

public class PigeonFirebase : MonoBehaviour
{
    private FirebaseDatabase firPigeonDatabase;
    private DatabaseReference pigeonDatabaseControls;
    private DatabaseReference pigeonDatabaseLogs;

    public Text airspeedLabel;
    public Text groundSpeedLabel;
    public Text modeLabel;
    public Text altitudeLabel;
    public Text deltaXLabel;
    public Text deltaYLabel;
    public Text deltaZLabel;
    public Text deltaYawLabel;

    private string airspeedData;
    private string groundspeedData;
    private string modeData;
    private string altitudeData;
    private double pigeonLat;
    private double pigeonLong;
    
    private Quaternion pigeonLocalRightRotation;
    private float pigeonLocalIndexTriggerUp;
    private float pigeonLocalHandTriggerDown;
    private Vector2 pigeonLocalThumbstick;

    public WebViewObject pigeonCameraWebview;
    public Mapbox.Unity.Map.AbstractMap pigeonMapbox;

    private bool isPigeonFirebaseLoaded = false;
    // Start is called before the first frame update
    void Start()
    {

// Only works with Arm_64 OS
        Firebase.FirebaseApp.CheckAndFixDependenciesAsync().ContinueWith(pigeonFirebaseInitTask => {
            if (pigeonFirebaseInitTask.Result == Firebase.DependencyStatus.Available) {

                
                firPigeonDatabase = FirebaseDatabase.DefaultInstance;
                pigeonDatabaseControls = FirebaseDatabase.DefaultInstance.RootReference.Child("controls");
                pigeonDatabaseLogs = FirebaseDatabase.DefaultInstance.RootReference.Child("logs");

                pigeonDatabaseLogs.ValueChanged += PigeonLogsUpdated;
                
                isPigeonFirebaseLoaded = true;

            }
            else {
                Debug.Log("ERROR");
                Debug.Log(pigeonFirebaseInitTask.Result);
            }
        });

        // This is the web cam stream for Pigeon Drone
                pigeonCameraWebview.Init();
                pigeonCameraWebview.SetMargins(Screen.width/4, 60, Screen.width/4, (int) (Screen.height / 1.5));
                pigeonCameraWebview.SetVisibility(true);
                pigeonCameraWebview.LoadURL("XXXX");

    }

    void PigeonLogsUpdated(object pigeonUpdate, ValueChangedEventArgs pigeonValueChanged) {
        if (pigeonValueChanged.DatabaseError != null) { return; }
        pigeonDatabaseLogs.GetValueAsync().ContinueWith(pigeonDataTask => {
            if (pigeonDataTask.IsCompleted) {
                DataSnapshot pigeonResultSnapshot = pigeonDataTask.Result;
                // Debug.Log(pigeonResultSnapshot.Children.Count);
                foreach (var pigeonResultItem in pigeonResultSnapshot.Children) {

                
                string pigeonValueChangedKey = pigeonResultItem.Key.ToString();
                string pigeonValueChangedValue = pigeonResultItem.Value.ToString();
                Debug.Log(pigeonValueChangedKey);
                    if (pigeonValueChangedKey == "airspeed") {
                        airspeedData = "Airspeed: " + pigeonValueChangedValue.ToString() + " m/s";
                    }
                    else if (pigeonValueChangedKey == "groundspeed") {

                        groundspeedData = "Groundspeed: " + pigeonValueChangedValue.ToString() + " m/s";
                    }
                    else if (pigeonValueChangedKey == "mode") {

                        modeData = "Mode: " + pigeonValueChangedValue.ToString();
                    }
                    else if (pigeonValueChangedKey == "altitude") {

                        altitudeData = "Altitude: " + pigeonValueChangedValue.ToString() + " m";
                    }
                    else if (pigeonValueChangedKey == "lat") {
                        pigeonLat = (double) pigeonResultItem.Value;
                    }
                    else if (pigeonValueChangedKey == "long") {
                        pigeonLong = (double) pigeonResultItem.Value;

                    }
                }
                 
            }
        });

    }

    // Update is called once per frame
    void Update()
    {
        pigeonLocalRightRotation = OVRInput.GetLocalControllerRotation(OVRInput.Controller.RTouch);
        pigeonLocalIndexTriggerUp = OVRInput.Get(OVRInput.RawAxis1D.RIndexTrigger);
        pigeonLocalHandTriggerDown = OVRInput.Get(OVRInput.RawAxis1D.RHandTrigger);
        pigeonLocalThumbstick = OVRInput.Get(OVRInput.RawAxis2D.RThumbstick);

        float shouldActivateX = 0.00f; // Straight/Back
        float shouldActivateY = 0.00f; // Right/Left
        float shouldActivateZ = 0.00f; // Up/Down
        float shouldActivateYaw = 0.00f; // Rotate


        if (isPigeonFirebaseLoaded) {
   

             Debug.Log("x");


        if (Math.Abs(pigeonLocalRightRotation.z) >= 0.1 && (pigeonLocalHandTriggerDown > 0.1 || pigeonLocalIndexTriggerUp > 0.1)) {
            shouldActivateX = (float) pigeonLocalRightRotation.z;
                if (pigeonLocalRightRotation.y > 0) {
                    shouldActivateX -= 0.1f;
                }
                else {
                    shouldActivateX += 0.1f;
                }
        }
        if (Math.Abs(pigeonLocalRightRotation.x) >= 0.1 && (pigeonLocalHandTriggerDown > 0.1 || pigeonLocalIndexTriggerUp > 0.1)) {
            shouldActivateY = (float) pigeonLocalRightRotation.x;
                if (pigeonLocalRightRotation.y > 0) {
                    shouldActivateY -= 0.1f;
                }
                else {
                    shouldActivateY += 0.1f;
                }
        }
        if (pigeonLocalIndexTriggerUp > 0.1) {
            shouldActivateZ = (float) pigeonLocalIndexTriggerUp;
       }
       else if (pigeonLocalHandTriggerDown > 0.1) {
            shouldActivateZ = (float) -pigeonLocalHandTriggerDown;
       }

            shouldActivateYaw = (float) pigeonLocalThumbstick.x;
            
     
        Debug.Log(pigeonDatabaseControls);
        pigeonDatabaseControls.Child("x_vel").SetValueAsync(shouldActivateX);
        pigeonDatabaseControls.Child("y_vel").SetValueAsync(shouldActivateY);
        pigeonDatabaseControls.Child("z_vel").SetValueAsync(shouldActivateZ);
        pigeonDatabaseControls.Child("yaw").SetValueAsync(shouldActivateYaw);
        }
        deltaXLabel.text = "Δ x: " + System.Math.Round(shouldActivateX, 2).ToString() + " m/s";
        deltaYLabel.text = "Δ y: " + System.Math.Round(shouldActivateY, 2).ToString() + " m/s";
        deltaZLabel.text = "Δ z: " + System.Math.Round(shouldActivateZ, 2).ToString() + " m/s";
        deltaYawLabel.text = "Δ yaw: " + System.Math.Round(shouldActivateYaw, 2).ToString() + " m/s";

        // Index clicked
        // go up change z

        // index clicked +
        pigeonMapbox.UpdateMap(new Vector2d(pigeonLat, pigeonLong));
 

    }
    // Called at a specific rate
    void FixedUpdate() {
        airspeedLabel.text = airspeedData;
        groundSpeedLabel.text = groundspeedData;
        modeLabel.text = modeData;
        altitudeLabel.text = altitudeData;
    }
}
