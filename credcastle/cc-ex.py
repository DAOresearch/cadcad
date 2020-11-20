# CRED CASTLE EXPERIMENTS

# Imports
import numpy as np

from cadCAD.configuration.utils import config_sim
from cadCAD.configuration import Experiment
from cadCAD import configs

from cadCAD.engine import ExecutionMode, ExecutionContext
from cadCAD.engine import Executor

# Params
genesis_states = {
    # the castle
    'castle': 0,
    # the difficulty of building the castle
    'difficulty': 100,
    # the folks in the village
    'village_population': 100
}

sim_config_dict = {
    # days
    'T': range(30),
    # months
    'N': 1,
    #'M': {}
}

# Policies
def p_working_villagers(params, step, sH, s):
    working_villagers = np.random.randint(0, s['village_population'])
    return ({'working_villagers': working_villagers})

def p_villager_effort(params, step, sH, s):
    villager_effort = np.random.randint(0, 10)
    return ({'villager_effort': villager_effort})

# State Update Functions
def s_build_castle(params, step, sH, s, _input):
    y = 'castle'
    x = s[y]
    add_to_castle = round(_input['working_villagers'] * _input['villager_effort'] / s['difficulty'])
    x += add_to_castle
    return (y, x)

# State Update Blocks
partial_state_update_blocks = [
    {
        # policies represent the behavior of agents that interact with components of the system
        'policies': {
            'villager_effort': p_villager_effort,
            'working_villagers': p_working_villagers
        },
        # state variables that will be updated
        'variables': {
            'castle': s_build_castle
        }
    }
]

# Building The Model
exp = Experiment()
c = config_sim(sim_config_dict)
del configs[:]
exp.append_configs(initial_state=genesis_states,
                    partial_state_update_blocks=partial_state_update_blocks,
                    sim_configs=c)

# Running The Engine
exec_mode = ExecutionMode()
local_mode_ctx = ExecutionContext(exec_mode.local_mode)
simulation = Executor(exec_context=local_mode_ctx, configs=configs)
raw_system_events, tensor_field, sessions = simulation.execute()

# Data Viz
import pandas as pd
simulation_result = pd.DataFrame(raw_system_events)
simulation_result.set_index(['subset', 'run', 'timestep', 'substep'])
simulation_result.plot('timestep', ['castle', 'village_population'], grid=True,
        colormap = 'gist_rainbow',
        xticks=list(simulation_result['timestep'].drop_duplicates()),
        yticks=list(range(1+(simulation_result['castle']+simulation_result['village_population']).max())))