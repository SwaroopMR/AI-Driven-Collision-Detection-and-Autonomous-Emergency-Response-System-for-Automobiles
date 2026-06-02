"""
Emergency Response Handler for Collision Detection System
Manages notifications based on collision severity levels
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime
import json


class CollisionSeverity(Enum):
    """Collision severity levels"""
    NORMAL = "normal"
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"


@dataclass
class Location:
    """Vehicle location information"""
    latitude: float
    longitude: float
    address: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address
        }


@dataclass
class EmergencyContact:
    """Emergency contact information"""
    name: str
    phone: str
    email: str
    relationship: str


class EmergencyResponseSystem:
    """
    Handles emergency responses based on collision severity
    """
    
    def __init__(self, vehicle_id: str, driver_info: Dict[str, str]):
        """
        Initialize the emergency response system
        
        Args:
            vehicle_id: Unique vehicle identifier
            driver_info: Dictionary containing driver details (name, phone, email)
        """
        self.vehicle_id = vehicle_id
        self.driver_info = driver_info
        self.emergency_contacts: List[EmergencyContact] = []
        self.accident_log: List[Dict[str, Any]] = []
        
    def register_emergency_contact(self, contact: EmergencyContact) -> None:
        """Register a family member or emergency contact"""
        self.emergency_contacts.append(contact)
        print(f"✓ Registered emergency contact: {contact.name} ({contact.relationship})")
    
    def notify_driver(self, severity: CollisionSeverity, location: Location, 
                     collision_data: Dict[str, Any]) -> None:
        """Send alert to driver"""
        message = self._generate_driver_alert(severity, collision_data)
        print(f"\n🚨 DRIVER ALERT ({severity.value.upper()}):")
        print(f"   {message}")
        print(f"   Location: {location.address} (Lat: {location.latitude}, Lon: {location.longitude})")
    
    def notify_family_members(self, severity: CollisionSeverity, location: Location) -> None:
        """Send notifications to registered family members"""
        if severity == CollisionSeverity.NORMAL:
            return
            
        print(f"\n📞 NOTIFYING FAMILY MEMBERS:")
        for contact in self.emergency_contacts:
            notification = {
                "type": "SMS/EMAIL",
                "recipient": contact.name,
                "phone": contact.phone,
                "email": contact.email,
                "message": f"Emergency Alert: {contact.name}, there has been a {severity.value} collision involving your family member at {location.address}. Emergency services have been contacted.",
                "timestamp": datetime.now().isoformat()
            }
            print(f"   ✓ Notified {contact.name} ({contact.relationship}) via SMS and Email")
            print(f"     Phone: {contact.phone} | Email: {contact.email}")
    
    def notify_hospital(self, severity: CollisionSeverity, location: Location,
                       collision_data: Dict[str, Any]) -> None:
        """Send emergency request to nearby hospital"""
        if severity in [CollisionSeverity.MINOR, CollisionSeverity.MODERATE, CollisionSeverity.NORMAL]:
            return
        
        if severity == CollisionSeverity.MAJOR:
            ambulance_request = {
                "request_type": "EMERGENCY_AMBULANCE",
                "severity": severity.value,
                "location": location.to_dict(),
                "vehicle_id": self.vehicle_id,
                "driver_info": self.driver_info,
                "collision_data": collision_data,
                "timestamp": datetime.now().isoformat(),
                "urgency": "CRITICAL"
            }
            print(f"\n🏥 HOSPITAL ALERT (AMBULANCE REQUEST):")
            print(f"   ✓ Emergency ambulance requested")
            print(f"   Location: {location.address}")
            print(f"   Urgency: CRITICAL")
            print(f"   ETA: Dispatch to location immediately")
    
    def notify_police(self, severity: CollisionSeverity, location: Location,
                     collision_data: Dict[str, Any]) -> None:
        """Send notification to police station"""
        if severity in [CollisionSeverity.MINOR, CollisionSeverity.NORMAL]:
            return
        
        if severity in [CollisionSeverity.MODERATE, CollisionSeverity.MAJOR]:
            police_report = {
                "report_type": "ACCIDENT_NOTIFICATION",
                "severity": severity.value,
                "location": location.to_dict(),
                "vehicle_id": self.vehicle_id,
                "driver_info": self.driver_info,
                "collision_data": collision_data,
                "timestamp": datetime.now().isoformat(),
                "requires_inspection": True
            }
            print(f"\n🚔 POLICE NOTIFICATION:")
            print(f"   ✓ Police station notified of {severity.value} accident")
            print(f"   Location: {location.address}")
            print(f"   Vehicle ID: {self.vehicle_id}")
            print(f"   Status: Officers dispatched to inspect scene")
    
    def log_accident(self, severity: CollisionSeverity, location: Location,
                    collision_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create accident log entry"""
        accident_entry = {
            "timestamp": datetime.now().isoformat(),
            "vehicle_id": self.vehicle_id,
            "severity": severity.value,
            "location": location.to_dict(),
            "driver_info": self.driver_info,
            "collision_data": collision_data,
            "responses_triggered": self._get_responses_for_severity(severity)
        }
        self.accident_log.append(accident_entry)
        
        print(f"\n📋 ACCIDENT LOGGED:")
        print(f"   Log Entry: {len(self.accident_log)}")
        print(f"   Severity: {severity.value.upper()}")
        print(f"   Time: {accident_entry['timestamp']}")
        
        return accident_entry
    
    def handle_collision(self, severity: CollisionSeverity, location: Location,
                        collision_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main handler for collision events - triggers appropriate emergency responses
        
        Args:
            severity: Collision severity level
            location: Vehicle location
            collision_data: Collision detection data (speed, impact force, etc.)
            
        Returns:
            Summary of actions taken
        """
        print("\n" + "="*60)
        print("COLLISION DETECTION SYSTEM - EMERGENCY RESPONSE ACTIVATED")
        print("="*60)
        
        # Always log the accident
        accident_log = self.log_accident(severity, location, collision_data)
        
        # Always notify driver
        self.notify_driver(severity, location, collision_data)
        
        # Trigger responses based on severity
        if severity == CollisionSeverity.MAJOR:
            print("\n⚠️  MAJOR COLLISION DETECTED - FULL EMERGENCY RESPONSE")
            self.notify_family_members(severity, location)
            self.notify_hospital(severity, location, collision_data)
            self.notify_police(severity, location, collision_data)
            
        elif severity == CollisionSeverity.MODERATE:
            print("\n⚠️  MODERATE COLLISION DETECTED - PARTIAL EMERGENCY RESPONSE")
            self.notify_family_members(severity, location)
            self.notify_police(severity, location, collision_data)
            # Hospital and ambulance NOT notified
            
        elif severity == CollisionSeverity.MINOR:
            print("\n⚠️  MINOR COLLISION DETECTED - LIMITED RESPONSE")
            self.notify_family_members(severity, location)
            # Hospital, ambulance, and police NOT notified
            
        else:  # NORMAL - no emergency
            print("\n✓ SYSTEM IN MONITORING STATE - No emergency response required")
        
        print("\n" + "="*60)
        
        return {
            "collision_severity": severity.value,
            "accident_log_entry": accident_log,
            "responses_triggered": self._get_responses_for_severity(severity)
        }
    
    def _generate_driver_alert(self, severity: CollisionSeverity, 
                              collision_data: Dict[str, Any]) -> str:
        """Generate appropriate alert message for driver"""
        messages = {
            CollisionSeverity.MAJOR: "MAJOR COLLISION DETECTED! Emergency services have been contacted. Remain in vehicle, activate hazard lights.",
            CollisionSeverity.MODERATE: "MODERATE COLLISION DETECTED! Check for injuries. Move to safety if possible.",
            CollisionSeverity.MINOR: "MINOR COLLISION DETECTED. Check vehicle for damage.",
            CollisionSeverity.NORMAL: "System monitoring in progress. All clear."
        }
        return messages.get(severity, "Unknown collision event")
    
    def _get_responses_for_severity(self, severity: CollisionSeverity) -> List[str]:
        """Get list of responses triggered for severity level"""
        responses = {
            CollisionSeverity.MAJOR: ["driver_alert", "family_notification", "hospital_ambulance", "police_notification", "accident_logging"],
            CollisionSeverity.MODERATE: ["driver_alert", "family_notification", "police_notification", "accident_logging"],
            CollisionSeverity.MINOR: ["driver_alert", "family_notification", "accident_logging"],
            CollisionSeverity.NORMAL: ["monitoring"]
        }
        return responses.get(severity, [])
    
    def get_accident_history(self) -> List[Dict[str, Any]]:
        """Retrieve accident log history"""
        return self.accident_log
    
    def export_accident_log(self, filename: str = "accident_log.json") -> None:
        """Export accident log to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.accident_log, f, indent=2)
        print(f"✓ Accident log exported to {filename}")
