class state_transitions(object):
  def __init__(self, state, use_from_pv, use_from_grid, use_from_batt, charge_batt_from_grid, charge_batt_from_pv):
    self.state = state
    self.use_from_pv = use_from_pv
    self.use_from_grid = use_from_grid
    self.use_from_batt = use_from_batt
    self.charge_batt_from_grid = charge_batt_from_grid
    self.charge_batt_from_pv = charge_batt_from_pv

  def get_transition_cost(self):
    return (self.use_from_grid*self.state.grid_cost + self.use_from_batt*self.state.batt_cost + self.charge_batt_from_grid*self.state.grid_cost)

class state(object):
  """docstring for state"""
  def __init__(self, demand, grid_cost, pv, batt_cost, batt_charge_level):
    self.demand = demand
    self.grid_cost = grid_cost
    self.pv = pv
    self.batt_cost = batt_cost
    self.batt_charge_level = batt_charge_level

def main():
  first_state = state(2,.2,1,.15,.5)
  first_transition = state_transitions(first_state, 1,1,1,1,1)
  print first_transition.get_transition_cost()

if __name__ == '__main__':
  main()
