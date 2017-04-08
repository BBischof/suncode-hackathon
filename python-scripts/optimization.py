import pandas as pd

STEPS_PER_HOUR = 4

class state_transitions(object):
  """decision values for state"""
  def __init__(self, state, battery, building_use_from_pv, building_use_from_grid, building_use_from_batt, charge_batt_from_grid, charge_batt_from_pv):
    self.state = state
    self.battery = battery
    self.building_use_from_pv = building_use_from_pv
    self.building_use_from_grid = building_use_from_grid
    self.building_use_from_batt = building_use_from_batt
    self.charge_batt_from_grid = charge_batt_from_grid
    self.charge_batt_from_pv = charge_batt_from_pv

  def get_transition_cost(self):
    return (self.building_use_from_grid*self.state.grid_cost + self.building_use_from_batt*self.battery.cost + self.charge_batt_from_grid*self.state.grid_cost)

  def transpile_transition_to_json(self):
    return {
        'building_use_from_pv' : self.building_use_from_pv,
        'building_use_from_grid' : self.building_use_from_grid,
        'building_use_from_batt' : self.building_use_from_batt,
        'charge_batt_from_grid' : self.charge_batt_from_grid,
        'charge_batt_from_pv' : self.charge_batt_from_pv
    }

class battery(object):
  """docstring for battery"""
  def __init__(self, c_rate, cost, max_capacity):
    self.c_rate = c_rate
    self.charge_level = 1
    self.cost = cost
    self.max_capacity = max_capacity


class state(object):
  """variable values for state"""
  def __init__(self, demand, grid_cost, pv):
    self.demand = demand
    self.grid_cost = grid_cost
    self.pv = pv
    self.STEPS_PER_HOUR = STEPS_PER_HOUR

def convert_to_charge_rate(kwh, battery):
  return (kwh/float(battery.max_capacity))

def evaluate_naive_model(state, battery):
  delta_pv_less_demand = (state.pv - state.demand)
  if delta_pv_less_demand > 0:
    if batt_charge_level < 1:
      charge_batt_from_pv = delta_pv_less_demand if (convert_to_charge_rate(delta_pv_less_demand, battery) <= battery.c_rate) else (battery.max_capacity*battery.c_rate)
      building_use_from_pv = state.demand
      building_use_from_grid, building_use_from_batt, charge_batt_from_grid = 0,0,0
      return state_transitions(state, battery, building_use_from_pv, building_use_from_grid, building_use_from_batt, charge_batt_from_grid, charge_batt_from_pv)
    else:
      building_use_from_pv = state.demand
      building_use_from_grid = -delta_pv_less_demand
      charge_batt_from_pv, building_use_from_batt, charge_batt_from_grid = 0,0,0
      return state_transitions(state, battery, building_use_from_pv, building_use_from_grid, building_use_from_batt, charge_batt_from_grid, charge_batt_from_pv)
  else:
    cost_delta_batt_less_grid = (battery.cost - state.grid_cost)
    if cost_delta_batt_less_grid > 0:
      building_use_from_pv = state.pv
      building_use_from_grid = -delta_pv_less_demand
      charge_batt_from_pv, building_use_from_batt, charge_batt_from_grid = 0,0,0
      return state_transitions(state, battery, building_use_from_pv, building_use_from_grid, building_use_from_batt, charge_batt_from_grid, charge_batt_from_pv)
    else:
      if state.demand<(battery.max_capacity*battery.charge_level):
        building_use_from_pv = state.pv
        building_use_from_batt = -delta_pv_less_demand
        charge_batt_from_pv, building_use_from_grid, charge_batt_from_grid = 0,0,0
        return state_transitions(state, battery, building_use_from_pv, building_use_from_grid, building_use_from_batt, charge_batt_from_grid, charge_batt_from_pv)
      else:
        building_use_from_pv = state.pv
        building_use_from_batt = battery.max_capacity*battery.charge_level
        building_use_from_grid = delta_pv_less_demand - (battery.max_capacity*battery.charge_level)
        charge_batt_from_pv, charge_batt_from_grid = 0,0
        return state_transitions(state, battery, building_use_from_pv, building_use_from_grid, building_use_from_batt, charge_batt_from_grid, charge_batt_from_pv)


def convert_usage_demand_to_kwh(dataframe, data_column):
  dataframe[data_column] = dataframe[data_column].apply(lambda x: x/4.0)

def main():
  first_battery = battery(.5, .15, 60)
  first_state = state(2,.2,1)
  first_transition = state_transitions(first_state, first_battery,1,1,1,1,1)
  print first_transition.transpile_transition_to_json()
  print first_transition.get_transition_cost()

if __name__ == '__main__':
  main()
