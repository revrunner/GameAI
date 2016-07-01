# Program 4: Behavior Trees for Planet Wars
# Program Authors: Nirav Agrawal and Jacob Preston

# checks if planet is neutral
def if_neutral_planet_available(state):
  return any(state.neutral_planets())

# checks if friendly fleet is bigger or smaller
# than enemy fleet
def have_largest_fleet(state):
  return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def default_true(state):
  return True
             
# def neutral_planet_with_largest_fleet(state):
  # temp = state.neutral_planets()[0].num_ships
  # for planet in state.neutral_planets():
    # if planet.num_ships > temp:
      # temp = planet.num_ships
  # pass
  
# 
def find_closest_neutral_planet(state):
  pass
