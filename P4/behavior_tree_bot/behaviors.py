# Program 4: Behavior Trees for Planet Wars
# Program Authors: Nirav Agrawal and Jacob Preston

import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

# Spreads to the weakest closest planets    
def spread_to_weakest_closest_neutral_planet(state):
  
  if len(state.my_fleets()) >= 1: 
    return False
  strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
  weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

  if not strongest_planet or not weakest_planet:
    return False
  
  main_distance = state.distance(strongest_planet.ID, weakest_planet.ID)
  new_time = main_distance
  difference = main_distance 
  for planet in state.neutral_planets():
    new_distance = state.distance(strongest_planet.ID, planet.ID)
    if (planet.num_ships > strongest_planet.num_ships):
      difference = planet.num_ships - strongest_planet.num_ships + (strongest_planet.num_ships / 2)
      new_time = difference / strongest_planet.growth_rate
      new_time += new_distance  
    if (planet.num_ships < (1.5 * strongest_planet.num_ships)):
      new_time = new_distance
    if (new_time < main_distance):
      main_distance = new_time
      weakest_planet = planet
  return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
    
def attack_same_planet_as_enemy(state):
  if len(state.my_fleets()) >= 1:
    return False
  
  # temporary closest planet till we find one
  closest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
  weakest_fleet = min(state.enemy_fleets(), key=lambda f: f.num_ships, default=None)
  
  if not closest_planet or not weakest_fleet:
    return False
  
  min_dist = float('inf')
  destination = weakest_fleet.destination_planet
  numberOfShips = weakest_fleet.num_ships
  for planet in state.my_planets():
    if planet == destination:
      return False
    new_distance = state.distance(planet.ID, destination)
    if (planet.num_ships - 20) > weakest_fleet.num_ships and new_distance < min_dist:
      min_dist = new_distance
      closest_planet = planet
  
  required_ships = weakest_fleet.num_ships + 20
  return issue_order(state, closest_planet.ID, destination, required_ships)
  
def best_spread(state):
  my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))
  enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
  enemy_planets.sort(key=lambda p: p.num_ships)
  target_planets = iter(enemy_planets)
  try:
    my_planet = next(my_planets)
    target_planet = next(target_planets)
    while True:
        required_ships = target_planet.num_ships + \
                            state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1
        if my_planet.num_ships > required_ships:
          issue_order(state, my_planet.ID, target_planet.ID, required_ships)
          my_planet = next(my_planets)
          target_planet = next(target_planets)
        else:
          my_planet = next(my_planets)

  except StopIteration:
    return
    