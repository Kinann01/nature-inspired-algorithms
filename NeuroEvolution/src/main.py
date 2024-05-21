import argparse
import gymnasium as gym
import neat
import numpy as np
import visualizer

def _evaluateGenomes(genomes, config, environment, numEpisodes, episodeDuration):
    env = gym.make(environment)
    for _, genome in genomes:
        genome.fitness = 0
        for _ in range(numEpisodes):
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            observation, _ = env.reset()
            totalReward = 0.0
            for _ in range(episodeDuration):
                action = np.argmax(net.activate(observation))
                observation, reward, terminated, truncated, _ = env.step(action)
                totalReward += reward
                if terminated or truncated:
                    break
            genome.fitness += totalReward
        genome.fitness /= numEpisodes

def _demonstrateWinner(genome, config, environment):
    env = gym.make(environment, render_mode="human")
    winnerNet = neat.nn.FeedForwardNetwork.create(genome, config)
    observation, _ = env.reset()
    done = False
    while not done:
        env.render()
        action = np.argmax(winnerNet.activate(observation))
        observation, _, terminated, truncated, _ = env.step(action)
        if terminated or truncated:
            break
    env.close()

def runNeat(configPath, environment, numGenerations, episodeDuration, numEpisodes):
    config = neat.Config(neat.DefaultGenome, 
                         neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, 
                         neat.DefaultStagnation,
                         configPath)
    
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    def _evaluateGenomesWrapper(genomes, config):
        _evaluateGenomes(genomes, config, environment, numEpisodes, episodeDuration)

    winner = population.run(_evaluateGenomesWrapper, numGenerations)
    print('\nBest genome:\n{!s}'.format(winner))
    _demonstrateWinner(winner, config, environment)
    
    visualizer.plot_stats(stats, ylog=False, view=True)

def main():

    parser = argparse.ArgumentParser(description="Run NEAT algorithm on a specified game environment.")
    parser.add_argument('--env', type=str, default="CartPole-v1", help="The game environment to use.")
    parser.add_argument('--generations', type=int, default=100, help="Number of generations to run.")
    parser.add_argument('--episodeDuration', type=int, default=500, help="Duration of each episode.")
    parser.add_argument('--numEpisodes', type=int, default=5, help="Number of episodes to average fitness over.")
    parser.add_argument('--configPath', type=str, default="", help="Path to the NEAT configuration file.", required=False)

    args = parser.parse_args()
    print(f"Running NEAT for {args.env}")

    POLE_ENV = "../config-pole"
    MOUNTAINCAR_ENV = "../config-mountainCar"

    temp = POLE_ENV if args.env == "CartPole-v1" else MOUNTAINCAR_ENV
    if (not args.configPath):
        runNeat(temp, args.env, args.generations, args.episodeDuration, args.numEpisodes)
    else:
        runNeat(args.configPath, args.env, args.generations, args.episodeDuration, args.numEpisodes)

if __name__ == "__main__":
    main()


# Submit your solution via email, which should include:
# List of environments you tried
# Description of the algorithm along with its settings (hyperparameters, etc.)
# Algorithm code + instructions for running it
# Graphs showing the performance of the best individual over generations

# The NEAT (NeuroEvolution of Augmenting Topologies) algorithm is used for evolving neural networks. NEAT evolves both the weights and the topology of the networks. 
# The key hyperparameters for NEAT in this implementation are:

# Population Size: The number of genomes in each generation.
# Mutation Rates: The rates at which weights and structures are mutated.
# Number of Generations: The number of iterations for the evolutionary process.
# Fitness Function: The reward obtained from the environment used to evaluate the performance of each genome.