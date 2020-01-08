from pyomo.environ import *


model = ConcreteModel()

MAX_LEV=56
GLCAP=100
NGLCAP=20

# weights
STOR_WT=1/75
IMPLANT_COUNT_WT=1/10
REGEN_WT=3

PWR_FROM_MGT=4
model.S = Set(initialize=[x for x in range(51,MAX_LEV+1)], doc='levels')
#implant_data structure
# key: implant name
#  0: control requirement
#  1: power storage
#  2: power regeneration
#  3: implant Power Grid requirement
#  4: requires lack of Power Grid
#  5: implant limit
#  6: hard caps at which the implant will not be installed
implant_data = {
        'Advanced Flywheel':        [1.50,    75, 0,  0, -1,  2, NGLCAP],
        'Battery Grid Pack':        [0.50,    50, 0, -1,  0,101,  GLCAP],
        'Battery Pack':             [0.50,    25, 0,  0, -1,  2, NGLCAP],
        'Cold Fusion Grid Pack':    [1.00,     0, 8, -1,  0,101,  GLCAP],
        'Efficiency Coprocessor':   [1.50,     0, 0,  0,  0,  1,    100],
        'Flywheel Grid Pack':       [1.50,   150, 0, -1,  0,101,  GLCAP],
        'Nuclear Reactor Grid Pack':[0.50,     0, 4, -1,  0,101,  GLCAP],
        'Power Grid':               [2.00,     0, 0,100,  0, 1,   GLCAP],
        'Power Management System':  [1.50,     0, 0,  0,  0,  1,    100],
        'Solar Cell Grid Pack':     [0.25,     0, 2, -1,  0,101,  GLCAP],
        'Solar Cells':              [0.25,     0, 1,  0, -1,  2, NGLCAP],
        'Ultracapacitor Chain':     [1.00,    50, 0,  0, -1,  2, NGLCAP],
        'Ultracapacitor Grid Pack': [1.00,   100, 0, -1,  0,101,  GLCAP]}
model.I = Set(initialize=implant_data.keys(), doc='implants')

def init_implants_levels(model):
        return ((k,i) for k in model.S for i in model.I)
model.implants_levels=Set(dimen=2,initialize=init_implants_levels)

def zeros(model, x, y):
   return 0
def xBounds(model, x, y):
   if y == 'Efficiency Coprocessor' and x >= 25:
     return (1, 1)

   if implant_data[y][6] <= x:
     return (0, 0)

   return (0, implant_data[y][5])

model.x = Var(model.implants_levels, within=NonNegativeIntegers, initialize=zeros, bounds=xBounds) 
model.value = Objective(
        expr = sum( -model.x[k,i]*IMPLANT_COUNT_WT + ((implant_data[i][1]*STOR_WT)+implant_data[i][2])*model.x[k,i]*REGEN_WT for k in model.S for i in model.I )+sum( model.x[k, 'Power Management System']*PWR_FROM_MGT*k*STOR_WT for k in model.S ),
        sense = maximize )

def control_limit_rule(model, k):
  
    return sum(model.x[k,i]*implant_data[i][0] for i in model.I) <= k
model.control_limit = Constraint(model.S, rule=control_limit_rule)

def power_control_limit_rule(model, k):
   
    return sum(model.x[k,i]*implant_data[i][0] for i in model.I) <= k*0.25
model.power_control = Constraint(model.S, rule=power_control_limit_rule)
def storage_requirements_rule(model, k):
    
    #you must have 50 storage for each 1 regen
    total_storage = sum(model.x[k,i]*implant_data[i][1] for i in model.I)
    total_regen   = sum(model.x[k,i]*implant_data[i][2] for i in model.I)
    special_storage = PWR_FROM_MGT*k*model.x[k,'Power Management System']

    return (total_storage+special_storage) >= (total_regen * 50)
model.storage_requirements = Constraint(model.S, rule=storage_requirements_rule)

def grid_requirement_rule(model, k):

    #you must have the power grid installed if you have at least 1 grid implant
    grid_sum = sum(model.x[k,i]*implant_data[i][3] for i in model.I)

    return 0 <= grid_sum <= 100

model.grid_requirements = Constraint(model.S, rule=grid_requirement_rule)
def nongrid_requirement_rule(model, k):

    #if the implant is non-grid it must not have power grid installed
    power_grid = model.x[k,'Power Grid']*implant_data['Power Grid'][3]
    nongrid = sum(implant_data[i][4]*model.x[k,i] for i in model.I)

    return -100 <= nongrid - power_grid <= 0
model.nongrid_requirements = Constraint(model.S, rule=nongrid_requirement_rule)

