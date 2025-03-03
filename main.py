from datetime import datetime, timedelta
import time
from models import TransportSimulation

def main():
    # Initialize simulation
    sim = TransportSimulation()
    
    # Add terminals (Port maritime et terminaux fluviaux)
    terminal_le_havre = sim.add_terminal("Le Havre", capacity=2000)
    terminal_rouen = sim.add_terminal("Rouen", capacity=1500)
    terminal_paris = sim.add_terminal("Paris", capacity=1800)
    terminal_gennevilliers = sim.add_terminal("Gennevilliers", capacity=1200)
    terminal_bonneuil = sim.add_terminal("Bonneuil", capacity=1000)
    
    # Current time for scheduling
    start_time = datetime.now()
    
    # Add services
    # Service Le Havre -> Rouen (4 fois par jour)
    schedule_hr = [
        start_time + timedelta(hours=i*6)
        for i in range(4)  # 24 hours of schedule
    ]
    service_hr = sim.add_service(
        origin=terminal_le_havre,
        destination=terminal_rouen,
        capacity=200,
        duration=timedelta(hours=3),
        schedule=schedule_hr
    )
    
    # Service Rouen -> Paris (3 fois par jour)
    schedule_rp = [
        start_time + timedelta(hours=i*8)
        for i in range(3)
    ]
    service_rp = sim.add_service(
        origin=terminal_rouen,
        destination=terminal_paris,
        capacity=150,
        duration=timedelta(hours=4),
        schedule=schedule_rp
    )
    
    # Service Paris -> Gennevilliers (6 fois par jour)
    schedule_pg = [
        start_time + timedelta(hours=i*4)
        for i in range(6)
    ]
    service_pg = sim.add_service(
        origin=terminal_paris,
        destination=terminal_gennevilliers,
        capacity=100,
        duration=timedelta(hours=1),
        schedule=schedule_pg
    )
    
    # Service Paris -> Bonneuil (4 fois par jour)
    schedule_pb = [
        start_time + timedelta(hours=i*6)
        for i in range(4)
    ]
    service_pb = sim.add_service(
        origin=terminal_paris,
        destination=terminal_bonneuil,
        capacity=120,
        duration=timedelta(hours=2),
        schedule=schedule_pb
    )
    
    # Add barges with different capacities
    barge1 = sim.add_barge(capacity=100, terminal_id=terminal_le_havre)  # Grande barge maritime
    barge2 = sim.add_barge(capacity=80, terminal_id=terminal_le_havre)   # Barge maritime moyenne
    barge3 = sim.add_barge(capacity=60, terminal_id=terminal_rouen)      # Barge fluviale moyenne
    barge4 = sim.add_barge(capacity=40, terminal_id=terminal_paris)      # Petite barge fluviale
    barge5 = sim.add_barge(capacity=40, terminal_id=terminal_paris)      # Petite barge fluviale
    
    # Add container requests
    # Containers from Le Havre to Paris (import maritime)
    for i in range(10):
        sim.add_container_request(
            type="TEU",
            origin=terminal_le_havre,
            destination=terminal_paris,
            available_date=start_time + timedelta(hours=i),
            due_date=start_time + timedelta(hours=24),
            priority=2  # High priority for maritime imports
        )
    
    # Containers from Le Havre to Gennevilliers
    for i in range(8):
        sim.add_container_request(
            type="TEU",
            origin=terminal_le_havre,
            destination=terminal_gennevilliers,
            available_date=start_time + timedelta(hours=i*2),
            due_date=start_time + timedelta(hours=36),
            priority=1
        )
    
    # Containers from Rouen to Bonneuil
    for i in range(6):
        sim.add_container_request(
            type="TEU",
            origin=terminal_rouen,
            destination=terminal_bonneuil,
            available_date=start_time + timedelta(hours=i*3),
            due_date=start_time + timedelta(hours=48),
            priority=1
        )
    
    print("Starting simulation...")
    print("Press Ctrl+C to stop the simulation")
    
    try:
        # Run simulation for 24 hours with 30-minute steps
        simulation_duration = timedelta(hours=24)
        end_time = start_time + simulation_duration
        
        while sim.current_time < end_time:
            sim.step()
            sim.print_status()
            time.sleep(1)  # Wait 1 second between updates
            
    except KeyboardInterrupt:
        print("\nSimulation stopped by user")
    
    # Print final statistics
    print("\nFinal Statistics:")
    metrics = sim.get_performance_metrics()
    print(f"Total containers processed: {metrics['total_containers']}")
    print(f"Containers delivered: {metrics['delivered']}")
    print(f"Containers in transit: {metrics['in_transit']}")
    print(f"Containers waiting: {metrics['waiting']}")
    print("\nTerminal Utilization:")
    for terminal, utilization in metrics['terminal_utilization'].items():
        print(f"{terminal}: {utilization*100:.1f}%")

if __name__ == "__main__":
    main()
