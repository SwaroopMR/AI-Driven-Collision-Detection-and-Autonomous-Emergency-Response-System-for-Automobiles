"""
Example usage of the Emergency Response System
Demonstrates collision detection at different severity levels
"""

from emergency_response import (
    EmergencyResponseSystem,
    CollisionSeverity,
    Location,
    EmergencyContact
)


def main():
    """Demonstrate emergency response system functionality"""
    
    # Initialize the system
    print("\n🚗 VEHICLE EMERGENCY RESPONSE SYSTEM - INITIALIZATION")
    print("="*60)
    
    driver_info = {
        "name": "John Doe",
        "phone": "+1-555-0101",
        "email": "john.doe@example.com",
        "license": "DL12345678"
    }
    
    vehicle_id = "VEHICLE_ABC_12345"
    system = EmergencyResponseSystem(vehicle_id, driver_info)
    
    # Register emergency contacts
    print("\n📋 REGISTERING EMERGENCY CONTACTS")
    print("="*60)
    
    family_contacts = [
        EmergencyContact(
            name="Jane Doe",
            phone="+1-555-0102",
            email="jane.doe@example.com",
            relationship="Spouse"
        ),
        EmergencyContact(
            name="Robert Doe",
            phone="+1-555-0103",
            email="robert.doe@example.com",
            relationship="Son"
        ),
        EmergencyContact(
            name="Sarah Smith",
            phone="+1-555-0104",
            email="sarah.smith@example.com",
            relationship="Sister"
        )
    ]
    
    for contact in family_contacts:
        system.register_emergency_contact(contact)
    
    # Test Case 1: MAJOR COLLISION
    print("\n\n" + "#"*60)
    print("TEST CASE 1: MAJOR COLLISION DETECTED")
    print("#"*60)
    
    major_location = Location(
        latitude=40.7128,
        longitude=-74.0060,
        address="5th Avenue and 34th Street, Manhattan, NY"
    )
    
    major_collision_data = {
        "impact_force": 85.5,  # kN (kilonewtons)
        "vehicle_speed": 65,  # mph
        "deceleration": 0.8,  # g-force
        "airbags_deployed": True,
        "seat_belts_engaged": True,
        "confidence": 0.98
    }
    
    major_result = system.handle_collision(
        CollisionSeverity.MAJOR,
        major_location,
        major_collision_data
    )
    
    # Test Case 2: MODERATE COLLISION
    print("\n\n" + "#"*60)
    print("TEST CASE 2: MODERATE COLLISION DETECTED")
    print("#"*60)
    
    moderate_location = Location(
        latitude=40.7200,
        longitude=-74.0150,
        address="Broadway and 42nd Street, Manhattan, NY"
    )
    
    moderate_collision_data = {
        "impact_force": 45.2,
        "vehicle_speed": 35,
        "deceleration": 0.4,
        "airbags_deployed": True,
        "seat_belts_engaged": True,
        "confidence": 0.92
    }
    
    moderate_result = system.handle_collision(
        CollisionSeverity.MODERATE,
        moderate_location,
        moderate_collision_data
    )
    
    # Test Case 3: MINOR COLLISION
    print("\n\n" + "#"*60)
    print("TEST CASE 3: MINOR COLLISION DETECTED")
    print("#"*60)
    
    minor_location = Location(
        latitude=40.7300,
        longitude=-74.0250,
        address="Park Avenue and 52nd Street, Manhattan, NY"
    )
    
    minor_collision_data = {
        "impact_force": 15.8,
        "vehicle_speed": 15,
        "deceleration": 0.2,
        "airbags_deployed": False,
        "seat_belts_engaged": True,
        "confidence": 0.87
    }
    
    minor_result = system.handle_collision(
        CollisionSeverity.MINOR,
        minor_location,
        minor_collision_data
    )
    
    # Test Case 4: NORMAL/NO COLLISION
    print("\n\n" + "#"*60)
    print("TEST CASE 4: NORMAL STATE - NO COLLISION")
    print("#"*60)
    
    normal_location = Location(
        latitude=40.7400,
        longitude=-74.0350,
        address="Central Park West, Manhattan, NY"
    )
    
    normal_data = {
        "impact_force": 0,
        "vehicle_speed": 25,
        "deceleration": 0,
        "airbags_deployed": False,
        "seat_belts_engaged": True,
        "confidence": 1.0
    }
    
    normal_result = system.handle_collision(
        CollisionSeverity.NORMAL,
        normal_location,
        normal_data
    )
    
    # Display accident history
    print("\n\n" + "="*60)
    print("ACCIDENT HISTORY SUMMARY")
    print("="*60)
    
    history = system.get_accident_history()
    for idx, entry in enumerate(history, 1):
        print(f"\n{idx}. Collision Severity: {entry['severity'].upper()}")
        print(f"   Timestamp: {entry['timestamp']}")
        print(f"   Location: {entry['location']['address']}")
        print(f"   Responses: {', '.join(entry['responses_triggered'])}")
    
    # Export accident log
    print("\n" + "="*60)
    system.export_accident_log("accident_log.json")
    print("="*60)


if __name__ == "__main__":
    main()
