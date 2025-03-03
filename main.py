from datetime import datetime, timedelta
import pygame
from models import TransportSimulation
from visualization import SimulationVisualizer

def main():
    # Initialize simulation
    sim = TransportSimulation()
    
    # Add terminals
    terminal_a = sim.add_terminal("Terminal A", capacity=1000)
    terminal_b = sim.add_terminal("Terminal B", capacity=800)
    terminal_c = sim.add_terminal("Terminal C", capacity=1200)
    
    # Add services
    # Service from A to B, every 4 hours
    schedule_ab = [
        datetime.now() + timedelta(hours=i*4)
        for i in range(6)  # 24 hours of schedule
    ]
    service_ab = sim.add_service(
        origin=terminal_a,
        destination=terminal_b,
        capacity=100,
        duration=timedelta(hours=2),
        schedule=schedule_ab
    )
    
    # Service from B to C, every 6 hours
    schedule_bc = [
        datetime.now() + timedelta(hours=i*6)
        for i in range(4)  # 24 hours of schedule
    ]
    service_bc = sim.add_service(
        origin=terminal_b,
        destination=terminal_c,
        capacity=150,
        duration=timedelta(hours=3),
        schedule=schedule_bc
    )
    
    # Add barges
    barge1 = sim.add_barge(capacity=50, terminal_id=terminal_a)
    barge2 = sim.add_barge(capacity=75, terminal_id=terminal_b)
    
    # Add some container requests
    for i in range(5):
        sim.add_container_request(
            type="TEU",
            origin=terminal_a,
            destination=terminal_c,
            available_date=datetime.now() + timedelta(hours=i),
            due_date=datetime.now() + timedelta(hours=24),
            priority=1
        )
    
    # Initialize visualizer
    viz = SimulationVisualizer(sim)
    
    # Main simulation loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update simulation
        sim.step()
        
        # Update visualization
        viz.draw()
        
        # Control frame rate
        clock.tick(60)
        
        # Every 100 steps, show metrics
        if sim.current_time.minute % 100 == 0:
            metrics = sim.get_performance_metrics()
            viz.plot_metrics(metrics)
    
    pygame.quit()

if __name__ == "__main__":
    main()
