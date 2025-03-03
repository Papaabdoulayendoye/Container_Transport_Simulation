import pygame
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict
from models import TransportSimulation

class SimulationVisualizer:
    def __init__(self, simulation: TransportSimulation):
        self.simulation = simulation
        pygame.init()
        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Container Transport Simulation")
        
        # Colors
        self.COLORS = {
            "background": (255, 255, 255),
            "terminal": (100, 100, 100),
            "barge": (0, 0, 255),
            "text": (0, 0, 0)
        }
        
        # Terminal positions (will be calculated based on network layout)
        self.terminal_positions = {}
        self._calculate_terminal_positions()
        
    def _calculate_terminal_positions(self):
        """Calculate terminal positions using networkx layout"""
        G = nx.Graph()
        
        # Add terminals as nodes
        for terminal_id in self.simulation.terminals:
            G.add_node(terminal_id)
            
        # Add services as edges
        for service in self.simulation.services.values():
            G.add_edge(service.origin, service.destination)
            
        # Calculate layout
        layout = nx.spring_layout(G)
        
        # Convert networkx coordinates to screen coordinates
        margin = 100
        for terminal_id, pos in layout.items():
            x = int(pos[0] * (self.width - 2 * margin)) + margin
            y = int(pos[1] * (self.height - 2 * margin)) + margin
            self.terminal_positions[terminal_id] = (x, y)
    
    def draw(self):
        """Draw the current state of the simulation"""
        # Clear screen
        self.screen.fill(self.COLORS["background"])
        
        # Draw services (routes)
        for service in self.simulation.services.values():
            start_pos = self.terminal_positions[service.origin]
            end_pos = self.terminal_positions[service.destination]
            pygame.draw.line(self.screen, (200, 200, 200), start_pos, end_pos, 2)
        
        # Draw terminals
        for terminal_id, terminal in self.simulation.terminals.items():
            pos = self.terminal_positions[terminal_id]
            pygame.draw.circle(self.screen, self.COLORS["terminal"], pos, 20)
            
            # Draw terminal name
            font = pygame.font.Font(None, 24)
            text = font.render(terminal.name, True, self.COLORS["text"])
            self.screen.blit(text, (pos[0] - 30, pos[1] - 40))
        
        # Draw barges
        for barge in self.simulation.barges.values():
            if barge.current_terminal:
                pos = self.terminal_positions[barge.current_terminal]
                pygame.draw.circle(self.screen, self.COLORS["barge"], pos, 10)
        
        # Update display
        pygame.display.flip()
    
    def plot_metrics(self, metrics: Dict):
        """Plot performance metrics using matplotlib"""
        plt.figure(figsize=(10, 6))
        
        # Terminal utilization bar chart
        utilization = metrics["terminal_utilization"]
        plt.bar(utilization.keys(), utilization.values())
        plt.title("Terminal Utilization")
        plt.xlabel("Terminal")
        plt.ylabel("Utilization (%)")
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show()
