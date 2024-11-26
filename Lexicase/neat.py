import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional
import random
import math
from pathlib import Path


class Gene:
    def __init__(self, input_node: int, output_node: int, weight: float, enabled: bool, innovation: int):
        self.input_node = input_node
        self.output_node = output_node
        self.weight = weight
        self.enabled = enabled
        self.innovation = innovation

class Genome:
    def __init__(self):
        self.genes: List[Gene] = []
        self.fitness: float = 0
        self.nodes: Dict[int, str] = {}  # node_id -> type ('input', 'hidden', 'output')
        
    def add_node(self, node_id: int, node_type: str):
        self.nodes[node_id] = node_type
        
    def add_gene(self, gene: Gene):
        self.genes.append(gene)

class NEATConfig:
    def __init__(self):
        self.population_size = 50
        self.weight_mutation_rate = 0.8
        self.weight_perturbation_range = 0.5
        self.add_node_rate = 0.03
        self.add_connection_rate = 0.05
        self.compatibility_threshold = 3.0
        self.c1 = 1.0  # Excess genes coefficient
        self.c2 = 1.0  # Disjoint genes coefficient
        self.c3 = 0.4  # Weight difference coefficient

class NEAT:
    def __init__(self, config: NEATConfig, input_size: int, output_size: int):
        self.config = config
        self.input_size = input_size
        self.output_size = output_size
        self.innovation_number = 0
        self.generation = 0
        self.population: List[Genome] = []
        self.species: List[List[Genome]] = []
        
        self.initialize_population()
    
    def initialize_population(self):
        for _ in range(self.config.population_size):
            genome = Genome()
            
            # Add input and output nodes
            for i in range(self.input_size):
                genome.add_node(i, 'input')
            for i in range(self.output_size):
                genome.add_node(self.input_size + i, 'output')
            
            # Create initial connections
            for i in range(self.input_size):
                for j in range(self.output_size):
                    weight = random.uniform(-1, 1)
                    gene = Gene(i, self.input_size + j, weight, True, self.get_innovation())
                    genome.add_gene(gene)
            
            self.population.append(genome)
    
    def get_innovation(self) -> int:
        self.innovation_number += 1
        return self.innovation_number
    
    def mutate_weight(self, gene: Gene):
        if random.random() < 0.1:  # 10% chance of complete weight reset
            gene.weight = random.uniform(-1, 1)
        else:
            gene.weight += random.uniform(-self.config.weight_perturbation_range, 
                                        self.config.weight_perturbation_range)
    
    def add_node_mutation(self, genome: Genome):
        if not genome.genes:
            return
        
        # Select a random connection to split
        gene = random.choice(genome.genes)
        gene.enabled = False
        
        # Add new node
        new_node_id = max(genome.nodes.keys()) + 1
        genome.add_node(new_node_id, 'hidden')
        
        # Add two new connections
        gene1 = Gene(gene.input_node, new_node_id, 1.0, True, self.get_innovation())
        gene2 = Gene(new_node_id, gene.output_node, gene.weight, True, self.get_innovation())
        
        genome.add_gene(gene1)
        genome.add_gene(gene2)
    
    def add_connection_mutation(self, genome: Genome):
        # Find all possible connections that don't exist yet
        existing_connections = {(g.input_node, g.output_node) for g in genome.genes}
        possible_connections = []
        
        for in_node in genome.nodes:
            for out_node in genome.nodes:
                if (genome.nodes[in_node] == 'output' and genome.nodes[out_node] == 'input'):
                    continue  # Prevent cycles
                if (in_node, out_node) not in existing_connections:
                    possible_connections.append((in_node, out_node))
        
        if possible_connections:
            in_node, out_node = random.choice(possible_connections)
            weight = random.uniform(-1, 1)
            new_gene = Gene(in_node, out_node, weight, True, self.get_innovation())
            genome.add_gene(new_gene)
    
    def mutate(self, genome: Genome):
        # Mutate weights
        if random.random() < self.config.weight_mutation_rate:
            for gene in genome.genes:
                if random.random() < self.config.weight_mutation_rate:
                    self.mutate_weight(gene)
        
        # Add node mutation
        if random.random() < self.config.add_node_rate:
            self.add_node_mutation(genome)
        
        # Add connection mutation
        if random.random() < self.config.add_connection_rate:
            self.add_connection_mutation(genome)
    
    def feed_forward(self, genome: Genome, inputs: List[float]) -> List[float]:
        if len(inputs) != self.input_size:
            raise ValueError(f"Expected {self.input_size} inputs, got {len(inputs)}")
        
        # Initialize node values
        node_values = {}
        
        # Set input values
        for i in range(self.input_size):
            node_values[i] = inputs[i]
            
        # Initialize hidden and output nodes to 0
        for node_id, node_type in genome.nodes.items():
            if node_type in ['hidden', 'output']:
                node_values[node_id] = 0
        
        # Sort genes by input node to ensure proper processing order
        sorted_genes = sorted(
            [g for g in genome.genes if g.enabled],
            key=lambda x: (x.input_node, x.output_node)
        )
        
        # Process each connection
        for gene in sorted_genes:
            node_values[gene.output_node] += node_values[gene.input_node] * gene.weight
            
            # Apply activation function after processing each node's inputs
            if genome.nodes[gene.output_node] in ['hidden', 'output']:
                node_values[gene.output_node] = 1 / (1 + math.exp(-node_values[gene.output_node]))
        
        # Collect outputs
        outputs = [node_values[self.input_size + i] for i in range(self.output_size)]
        return outputs

class SolarSiteOptimizer:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.neat = NEAT(
            NEATConfig(),
            input_size=2,  # yearly_sunlight_kwh_kw_threshold_avg, carbon_offset_metric_tons
            output_size=1  # selection score
        )
    
    def evaluate_genome(self, genome: Genome) -> float:
        total_fitness = 0
        
        for _, row in self.data.iterrows():
            inputs = [
                row['yearly_sunlight_kwh_kw_threshold_avg'] / 1000,  # Normalize sunlight
                row['carbon_offset_metric_tons'] / 100000  # Normalize carbon offset
            ]
            
            outputs = self.neat.feed_forward(genome, inputs)
            selection_score = outputs[0]
            
            # Calculate fitness based on energy generation and carbon offset optimization
            fitness_contribution = (
                selection_score * 
                (row['yearly_sunlight_kwh_kw_threshold_avg'] * 0.7 +  # Weight sunlight more heavily
                 row['carbon_offset_metric_tons'] * 0.3)              # Consider carbon offset
            )
            
            total_fitness += fitness_contribution
        
        return total_fitness
    
    def train(self, generations: int):
        for generation in range(generations):
            # Evaluate all genomes
            for genome in self.neat.population:
                genome.fitness = self.evaluate_genome(genome)
            
            # Sort population by fitness
            self.neat.population.sort(key=lambda x: x.fitness, reverse=True)
            
            # Print progress
            best_fitness = self.neat.population[0].fitness
            print(f"Generation {generation}: Best Fitness = {best_fitness}")
            
            # Create next generation
            new_population = []
            
            # Keep top performers
            elite_size = int(self.neat.config.population_size * 0.1)
            new_population.extend(self.neat.population[:elite_size])
            
            # Create offspring through mutation and crossover
            while len(new_population) < self.neat.config.population_size:
                parent = random.choice(self.neat.population[:int(self.neat.config.population_size * 0.2)])
                offspring = Genome()
                offspring.nodes = parent.nodes.copy()
                offspring.genes = [Gene(g.input_node, g.output_node, g.weight, g.enabled, g.innovation) 
                                 for g in parent.genes]
                
                self.neat.mutate(offspring)
                new_population.append(offspring)
            
            self.neat.population = new_population
            self.neat.generation += 1
    
    def get_best_zip_codes(self, top_n: int = 10) -> List[Tuple[str, float]]:
        best_genome = max(self.neat.population, key=lambda x: x.fitness)
        zip_scores = []
        
        for _, row in self.data.iterrows():
            inputs = [
                row['yearly_sunlight_kwh_kw_threshold_avg'] / 1000,
                row['carbon_offset_metric_tons'] / 100000
            ]
            
            outputs = self.neat.feed_forward(best_genome, inputs)
            zip_scores.append((row['zip_code'], outputs[0]))
        
        return sorted(zip_scores, key=lambda x: x[1], reverse=True)[:top_n]

if __name__ == "__main__":
    # Load and prepare data
    filepath = Path("Visualization") / "Clean_Data" / "data_by_zip.csv"
    data = pd.read_csv(filepath)
    optimizer = SolarSiteOptimizer(data)
    
    # Train the model
    optimizer.train(generations=50)
    
    # Get best zip codes
    best_zips = optimizer.get_best_zip_codes(top_n=10)
    print("\nTop 10 recommended zip codes:")
    for zip_code, score in best_zips:
        print(f"ZIP: {zip_code}, Score: {score:.4f}")