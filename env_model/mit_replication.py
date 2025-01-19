## Cecelia Crumlish 
## December 29, 2024 

## mit_replication.py, currently in 

## replication of:  
# MIT energy Quantifying the financial value of building decarbonization technology
# under uncertainty: Integrating energy modeling and investment analysis

import pprint
from typing import Any, Dict
import random 
pp = pprint.PrettyPrinter(indent=4)

from collections import defaultdict

# all ranges from paper for EUI
GasEUI = (148,160)
elecEUI = (129,142)
flexElecEUI = (142, 161)

# static parameters 
static_data = {
    "Gross_floor_area": {"value": 85700, "units": "m^2", "source": "User"},
    "Percent_leasable_area": {"value": .65, "units": "%", "source": "User"},
    "EUI_electricity_gas_design_option": {"value": 78, "units": "%", "source": "PNNL"},
    "EUI_natural_gas_gas_design_option": {"value": 22, "units": "%", "source": "PNNL"},
    "EUI_electricity_fully_electric_option": {"value": 100, "units": "%", "source": "PNNL"},
    "EUI_natural_gas_fully_electric_option": {"value": 0, "units": "%", "source": "PNNL"},
    "EUI_electricity_flexible_electric_ready_option": {"value": 82, "units": "%", "source": "PNNL"},
    "EUI_natural_gas_flexible_electric_ready_option": {"value": 18, "units": "%", "source": "PNNL"},
    "Gas_price_year_zero": {"value": 0.05, "units": "$/kWh", "source": "EIA"},
    "Electricity_price_year_zero": {"value": 0.23, "units": "$/kWh", "source": "EIA"},
    "Natural_gas_emission_coefficient": {"value": 0.18, "units": "kgCO2/kWh", "source": "EPA"},
    "Electricity_emission_coefficient_year_zero": {"value": 0.29, "units": "kgCO2/kWh", "source": "EPA"},
    "Analysis_time_horizon": {"value": 30, "units": "years", "source": "User"}
}


def create_sim_params(btype: str):
    """generates model parameters and distrobutions used in a single simulation 

    Args:
        op_cost (int): cost of operation given a simulation  
        emissions (int): an energy usage intensity given from the model ran 
        btype (BuildingType): GAS | ELECTRIC | FLEXIBLE 

    Returns:
        Dict[str, Any] | Any: _description_
        0 if incorrectly formatted input
    """
    param_dictionary = defaultdict()
    
    #equipment lifespan
    param_dictionary["heatingLifespan"] =  round(random.weibullvariate(24.81, 2.3), 1)
    
    # Percent of leasable area lost due to heat pump equipment (Uniform distribution)
    param_dictionary["leasable_lost"] = round(random.uniform(.02, .05), 2)

    # Discount rate (Uniform distribution)
    param_dictionary["discount_rate"] = round(random.uniform(5, 10), 1)
    
    param_dictionary["hvac_fail_replacement"] = random.randint(323, 377)
    param_dictionary["LL97_emission_intensity"] = random.randint(753, 2260) / 100.0  # TODO check if this works for decimals 
    
    param_dictionary["rental_income"] = round(random.triangular(1066, 1088, 1109), 1)

    match btype: 
        case 'GAS':
            print("gas option chosen \n")
            # construction cost:           
            param_dictionary["btype"] = 'GAS'
            param_dictionary['construction_cost'] = random.randint(6405, 6512)
            param_dictionary['EUI'] = random.randint(GasEUI[0], GasEUI[1])
            #equipment replacement  cost 
            param_dictionary["replacement_cost"] = random.randint(323,355)
            #%eui attributed to nat gas use
            param_dictionary['nat_gas'] = 22
            param_dictionary['elec_EUI'] = 78
            #%eui energy use 
            #ASHP cost premmium when installed 
            param_dictionary['ASHP_prem'] = random.randint(65,108)
            
            # rental income rate 
            # param_dictionary["rental_income"] = random.triangular(1066, 1088, 1109)
            
        case 'ELECTRIC': 
            param_dictionary["btype"] = 'ELECTRIC'
            print("electric option chosen \n")
            #eqipment replacement cost 
            param_dictionary['construction_cost'] = random.randint(6631, 6674)
            param_dictionary['EUI'] = random.randint(elecEUI[0], elecEUI[1])
            param_dictionary["replacement_cost"] = random.randint(355,377)
            param_dictionary['nat_gas'] = 0
            param_dictionary['elecEUI'] = 100
            #ASHP cost premmium when installed 
            param_dictionary['ASHP_prem'] = random.randint(65, 108)
            
            param_dictionary["rental_premium"] = round(random.triangular(4.3, 6.1, 7.8), 1) 
            
            print("make electric params")
            
            
        case 'FLEXIBLE': 
            param_dictionary["btype"] = 'FLEXIBLE'
            print("flexible option chosen \n")
            param_dictionary['construction_cost'] = random.randint(6512, 6620)
            param_dictionary['EUI'] = random.randint(flexElecEUI[0], flexElecEUI[1])
            param_dictionary["gas_replacement_cost"] = random.randint(323,355)
            param_dictionary["elec_replacement_cost"] = random.randint(355,377)
            param_dictionary['nat_gas'] = 18
            param_dictionary['elec_EUI'] = 82
            param_dictionary['ASHP_prem'] = random.randint(129, 172)
            param_dictionary['rental_premium'] = round(random.triangular(3.8, 5.4, 6.9), 1) 
            
        case _: 
            print("please give a valid building typeof: GAS | ELECTRIC | FLEXIBLE")
            return 0
            
    return param_dictionary

# currently performs 1 simulation will be soon to perform 0 - n 
def run_simulations(years: int, params: Dict[str, Any]) -> list[int]:
    """run_simulations
    
    runs the simulations from the paper, and returns a list of npv's run over 1000 simulations 

    Args:
        years (int): time horizon between 0 and n 
        params (Dict[str, Any]): GAS | ELECTRIC | ELECTRIC_FLEXIBLE
        simulations (int, optional): Defaults to 10000.

    Returns:
        list[int]: list of net 
    """
    # discount rate: r
    r = random.randint(5,10) 
    cashflows_sum = 0 
    
    capital_costs = get_capitalcosts(params)
         
    for t in range(1, years): 
        print("hello world")
        if t == years: 
            get_resaleval(params) / ((1 + r) ^ (years + 1)) 

    

            # cashflows_sum = get_rentalIncome(params) - get_operating_costs(params) get_regulatory_costs(params, t)
    
    # npv = (Capital costs @ t =0) + (sum from t-1 to n of ((rentalIncome_t - Operating Costst - Regulatory Costs_t) / (1 + r)^t)) + (ResaleValue / (1 + r)^n+1)
    
    pass

def get_capitalcosts(params: dict[str, float]) -> float: 
    """get capital costs 

    Args:
        params dict[str: float]: a parameter dictionary for a building 

    Returns:
        float: calculated capital cost for that building at time = 0
    notes: 
        assumes that the construction cost is per m^2 and the area is also in m^2
    """
    # TODO: determine if labor and permitting are included in construciton cost, in the paper this is unclear 
    return params['construction_cost'] * static_data["Gross_floor_area"]["value"]
    


def fucked_up_heating(params): 
    # gives you the cost of correcting the heating 
    pass


def get_rentalIncome(params): 
    # leasable area * $m^2 * rental rate per year 

    match params['btype']:
        case "ELECTRIC": 
            # find percentage leasable 
            leasable = static_data["Percent_leasable_area"]["value"] - params["leasable_lost"]
            sqf_leasable = leasable * static_data["Gross_floor_area"]["value"]
            print(leasable)

            # find square feet leasable 
            return sqf_leasable * params["rental_income"]
        
        case "FLEXIBLE: ": 
            return 0 
        
        case "GAS":
            return 0 

        case _ : 
            print(f"incorrectly typed simulation model of")
            return 0 
        
        
    
        
        

    pass

def get_operating_costs(params): 
    pass

def get_regulatory_costs(params): 
    return 1

def get_resaleval(params): 
    return 1


def main(): 
    """simulation driver, for now runs one simulation at a time 
    """
    print("hello world")
    electric_building = create_sim_params(btype= "ELECTRIC")
    pp.pprint(electric_building)
    print(get_rentalIncome(electric_building)) 
    # pp.pprint(create_sim_params(btype='ELECTRIC'))
    # pp.pprint(create_sim_params(btype='FLEXIBLE'))
     # regulatory costs: LL97 penalty, emisisons 
     
if __name__ == "__main__": 
    main()
    
    



## takes a list of simulation results from the energyplus modeller 
## and then runs 
