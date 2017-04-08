import pytest
import optimization

def test_battery_creation():
  test_battery = optimization.battery(.5, .15, 60)
  assert test_battery.c_rate == .5
  assert test_battery.charge_level == 1
  assert test_battery.cost == .15
  assert test_battery.max_capacity == 60

def test_state_creation():
  test_state = optimization.state(2, .2, 1)
  assert test_state.demand == 2
  assert test_state.grid_cost == .2
  assert test_state.pv == 1

def test_transition_creation():
  test_battery = optimization.battery(.5, .15, 60)
  test_state = optimization.state(2,.2,1)
  test_transition = optimization.state_transitions(test_state, test_battery,1,1,1,1,1)
  assert test_transition.transpile_transition_to_json() == {'building_use_from_pv' : 1, 'building_use_from_grid' : 1, 'building_use_from_batt' : 1, 'charge_batt_from_grid' : 1, 'charge_batt_from_pv' : 1 }
  assert test_transition.get_transition_cost() == .55

def test_naive_model():
  test_battery = optimization.battery(.5, .15, 60)
  test_state = optimization.state(2,.2,1)
  naive_model_transition = optimization.evaluate_naive_model(test_state, test_battery)
  assert naive_model_transition.get_transition_cost() == 0.15

