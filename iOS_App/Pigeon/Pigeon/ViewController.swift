//
//  ViewController.swift
//  Pigeon
//
//  Created by Krish Iyengar on 10/28/22.
//

import UIKit
import GameKit
import FirebaseDatabase
import MapKit
import WebKit

class ViewController: UIViewController {
    
    let pigeonDatabaseReferenceControls = Database.database().reference().child("controls")
    let pigeonDatabaseReferenceLogs = Database.database().reference().child("logs")
    var pigeonVirtualController: GCVirtualController = {
        let pigeonVirtualControllerConfig = GCVirtualController.Configuration()
        let pigeonController = GCController()
        pigeonVirtualControllerConfig.elements = [GCInputLeftThumbstick, GCInputRightThumbstick]
        
        return GCVirtualController(configuration: pigeonVirtualControllerConfig)
        
    }()
    var pigeonLeftJoypadTimer = Timer()
    var pigeonRightJoypadTimer = Timer()
    var pigeonControls = [String:Any]()
    
    @IBOutlet weak var pigeonWebCam: WKWebView!
    
    
    @IBOutlet weak var pigeonActionButton: UIButton!
    @IBOutlet weak var deltaStackView: UIStackView!
    @IBOutlet weak var map: MKMapView!
    @IBOutlet weak var mode: UILabel!
    @IBOutlet weak var deltaAlt: UILabel!
    @IBOutlet weak var deltaZ: UILabel!
    @IBOutlet weak var deltaX: UILabel!
    @IBOutlet weak var groundspeed: UILabel!
    @IBOutlet weak var airspeed: UILabel!
    @IBOutlet weak var alt: UILabel!
    @IBOutlet weak var airspeedAltGSStackView: UIStackView!
    var pigeonActionButtonOptions = [PigeonActions]()
    
    enum PigeonActions: String {
        case takeoff = "Takeoff"
        case land = "Land"
        case returnToHome = "Return to Home"
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        
        self.pigeonDatabaseReferenceControls.getData { [self] pigeonError, pigeonDataSnapshot in
            if let pigeonDataSnapshot = pigeonDataSnapshot {
                pigeonControls = pigeonDataSnapshot.value as? [String:Any] ?? [:]
                
              
            }
        }
        
        pigeonDatabaseReferenceLogs.observe(.value) { [self] oneLogsSnapshot in
            guard let pigeonDroneDataObserved = oneLogsSnapshot.value as? [String:Any] else { return }
            guard let airspeedData = pigeonDroneDataObserved["airspeed"] as? Double else { return }
            guard let groundspeedData = pigeonDroneDataObserved["groundspeed"] as? Double else { return }
            guard let altitudeData = pigeonDroneDataObserved["altitude"] as? Double else { return }
            guard let modeData = pigeonDroneDataObserved["mode"] as? String else { return }
            guard let latData = pigeonDroneDataObserved["lat"] as? Double else { return }
            guard let longData = pigeonDroneDataObserved["long"] as? Double else { return }

            alt.text = "Altitude: \(String(format: "%.2f", altitudeData)) m"
            groundspeed.text = "Groundspeed: \(String(format: "%.2f", groundspeedData)) m/s"
            airspeed.text = "Airspeed: \(String(format: "%.2f", airspeedData)) m/s"
            mode.text = "Mode: \(modeData)"
            
            let pigeonDroneAnnotation = MKPointAnnotation()
            pigeonDroneAnnotation.coordinate = CLLocationCoordinate2D(latitude: latData, longitude: longData)
            pigeonDroneAnnotation.title = "Pigeon Drone"
            map.removeAnnotations(map.annotations)
            map.addAnnotation(pigeonDroneAnnotation)
            
            
            map.setCamera(MKMapCamera(lookingAtCenter: CLLocationCoordinate2D(latitude: latData + 0.0001, longitude: longData), fromDistance: altitudeData<=100 ? altitudeData*5:altitudeData, pitch: 0, heading: 0), animated: true)
            
            if altitudeData >= 2 {
                pigeonActionButtonOptions = [.land, .returnToHome]
                pigeonActionButton.setTitle("Options", for: .normal)

            }
            else {
                pigeonActionButtonOptions = [.takeoff]

                pigeonActionButton.setTitle("Takeoff", for: .normal)

            }
        }
        airspeedAltGSStackView.layer.cornerRadius = 10
        deltaStackView.layer.cornerRadius = 10
        
        airspeedAltGSStackView.layer.opacity = 0.7
        deltaStackView.layer.opacity = 0.7
        
        guard let pigeonWebURL = URL(string: "http://10.0.0.147:5000") else { return }

        pigeonWebCam.load(URLRequest(url: pigeonWebURL))
    }
    
    @IBAction func pigeonAction(_ sender: UIButton) {
        
        if pigeonActionButtonOptions.count > 1 {
            let pigeonActionAlert = UIAlertController(title: "Pigeon Actions", message: "Choose an option", preferredStyle: .actionSheet)
            pigeonActionAlert.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: { [self] onePigeonActionAlert in
                self.dismiss(animated: true)
            }))
            for eachPigeonAction in pigeonActionButtonOptions {
                pigeonActionAlert.addAction(UIAlertAction(title: eachPigeonAction.rawValue, style: .default, handler: { [self] onePigeonActionAlert in
                    pigeonActionButtonHandler(pigeonAction: eachPigeonAction)
                }))
            }
            
            present(pigeonActionAlert, animated: true)
        }
        else if pigeonActionButtonOptions.count == 1 {
            pigeonActionButtonHandler(pigeonAction: pigeonActionButtonOptions[0])
        }
    }
    
    func pigeonActionButtonHandler(pigeonAction: PigeonActions) {
        pigeonDatabaseReferenceControls.updateChildValues(["action":pigeonAction.rawValue])

        pigeonActionButtonOptions.removeAll()
        
    }
    override func viewDidAppear(_ animated: Bool) {
        
        pigeonVirtualController.connect { [self] pigeonConnectVirtualControllerError in
            
            pigeonLeftJoypadTimer = Timer.scheduledTimer(withTimeInterval: 0.05, repeats: true, block: { [self] pigeonLeftJoyTimer in
                
                guard let pigeonControllerX = pigeonVirtualController.controller?.extendedGamepad?.leftThumbstick.xAxis.value else { return }
                guard let pigeonControllerY = pigeonVirtualController.controller?.extendedGamepad?.leftThumbstick.yAxis.value else { return }
            
                    pigeonControls["x_vel"] = Double(pigeonControllerX)
                    self.pigeonDatabaseReferenceControls.updateChildValues(["x_vel": pigeonControls["x_vel"]])
                    
                deltaX.text = "Δ X: \(String(format: "%.2f", Double(pigeonControllerX))) m/s"

                
                    pigeonControls["y_vel"] = Double(pigeonControllerY)
                    self.pigeonDatabaseReferenceControls.updateChildValues(["y_vel": pigeonControls["y_vel"]])
            deltaAlt.text = "Δ Y: \(String(format: "%.2f", Double(pigeonControllerY))) m/s"

                
            })
                
                
            
            pigeonRightJoypadTimer = Timer.scheduledTimer(withTimeInterval: 0.05, repeats: true, block: { [self] pigeonRightJoyTimer in
                guard let pigeonControllerY = pigeonVirtualController.controller?.extendedGamepad?.rightThumbstick.yAxis.value else { return }
                
                    pigeonControls["z_vel"] = Double(pigeonControllerY)
                    self.pigeonDatabaseReferenceControls.updateChildValues(["z_vel": pigeonControls["z_vel"]])
                   
                deltaZ.text = "Δ Z: \(String(format: "%.2f", Double(pigeonControllerY))) m/s"

                // This is for turning the drone
                guard let pigeonControllerX = pigeonVirtualController.controller?.extendedGamepad?.rightThumbstick.xAxis.value else { return }
                
                    pigeonControls["yaw"] = Double(pigeonControllerX)
                    self.pigeonDatabaseReferenceControls.updateChildValues(["yaw": pigeonControls["yaw"]])
                   

                
                
                

            })
         
        }
        
    }

}

