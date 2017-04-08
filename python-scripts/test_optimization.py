import pytest
import optimization

def test_battery_creation():
  test_battery = optimization.battery(.5, .15, 60, 6000)
  assert test_battery.c_rate == .5
  assert test_battery.charge_level == 1
  assert test_battery.cost == .15
  assert test_battery.max_capacity == 60

def test_state_creation():
  test_state = optimization.state('2014-01-01 00:00:00', 2, .2, 1)
  assert test_state.demand == 2
  assert test_state.grid_cost == .2
  assert test_state.pv == 1

def test_transition_creation():
  test_battery = optimization.battery(.5, .15, 60, 6000)
  test_state = optimization.state('2014-01-01 00:00:00', 2,.2,1)
  test_transition = optimization.state_transitions(test_state, test_battery,1,1,1,1,1)
  assert test_transition.transpile_transition_to_json() == {'timestamp': '2014-01-01 00:00:00', 'building_use_from_pv' : 1, 'building_use_from_grid' : 1, 'building_use_from_batt' : 1, 'charge_batt_from_grid' : 1, 'charge_batt_from_pv' : 1 }
  assert test_transition.get_transition_cost() == .55

def test_naive_model():
  test_battery = optimization.battery(.5, .15, 60, 6000)
  test_state = optimization.state('2014-01-01 00:00:00', 2,.2,1)
  naive_model_transition = optimization.evaluate_naive_model(test_state, test_battery)
  assert naive_model_transition.get_transition_cost() == 0.15

def test_naive_model_states_2_3_4():
  bat0 = optimization.battery(1.0, .15, 60.0, 6000)
  state0 = optimization.state('2014-01-01 00:00:00', 10.0, 0.2, 13.0)
  state1 = optimization.state('2014-01-01 00:00:00', 10.0, 0.13, 5.0)
  state2 = optimization.state('2014-01-01 00:00:00', 10.0, 0.2, 5.0)
  state3 = optimization.state('2014-01-01 00:00:00', 50.0, 0.2, 5.0)

  transition2 = optimization.evaluate_naive_model(state0,bat0)
  transition3 = optimization.evaluate_naive_model(state1,bat0)
  transition4 = optimization.evaluate_naive_model(state2,bat0)
  assert transition2.building_use_from_grid == -3
  assert transition2.building_use_from_pv == 10
  assert transition3.building_use_from_grid == 5
  assert transition3.building_use_from_pv == 5
  assert transition4.building_use_from_batt == 5
  assert transition4.building_use_from_pv == 5

def test_naive_model_states_1_5():
  bat1 = optimization.battery(1.0, .15, 60.0, 6000)
  bat1.update_charge_level(.2)
  state0 = optimization.state('2014-01-01 00:00:00', 10.0, 0.2, 13.0)
  state3 = optimization.state('2014-01-01 00:00:00', 50.0, 0.2, 1.0)

  transition1 = optimization.evaluate_naive_model(state0,bat1)
  transition5 = optimization.evaluate_naive_model(state3,bat1)
  assert bat1.charge_level == .8
  assert transition1.building_use_from_pv == 10
  assert transition1.charge_batt_from_pv == 3
  assert transition5.building_use_from_batt == 48
  assert transition5.building_use_from_grid == 1
  assert transition5.building_use_from_pv == 1

