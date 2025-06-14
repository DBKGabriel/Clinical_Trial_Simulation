"""
Default parameter sets for clinical trial simulation.

This module provides default parameters based on reasonable estimates of industry-standards. 
"""
"""
Here, I am improving upon the prototype_extracted_defaults.py. 

**Architectural Rationale:**
I created the prototype with flat dictionaries that mixed data definitions with parameter values.
This made it difficult to validate, extend, and maintain. 

So I split it into 2 modules to support enterprise-grade parameter architecture:
-- defaults.py,
-- phases.py
In this module, I transform the working_prototype's simple dictionary-based 
parameters into a class architecture capable of supporting multiple therapeutic areas 
and business scenarios for clinical trial decision support via enterprise-grade parameter management.


**Evolution Rationale:**
In building the prototype, I used flat dictionaries with hardcoded values.
This presents several problems, which I address in this upgrade by implementing:
-- Object-oriented parameter architecture with proper data validation
-- Distinct parameter sets based on pharmaceutical industry-specific research insights (DiMasi studies, FDA data, anecdotal, etc.)
-- Therapeutic area specializations (oncology, rare disease) reflecting domain expertise
-- Business scenario support (conservative, optimistic) for strategic decision-making
-- Comprehensive market modeling with revenue projections and patent lifecycle
-- Enterprise-grade parameter management to support regulatory-quality simulations

**Direct Business Value:**
-- Enables portfolio optimization across different therapeutic areas
-- Supports risk-adjusted decision making with scenario analysis
-- Provides regulatory-quality parameter documentation and validation
-- Facilitates strategic planning with industry-benchmarked assumptions

**Key Transformations Made:**
-- Converted flat dictionary to sophisticated parameter creation functions
-- Added industry-benchmarked success rates and cost distributions
-- Implemented therapeutic area-specific parameter sets (oncology, rare disease)  
-- Included comprehensive market modeling with patent lifecycle
-- Added manufacturing and launch cost modeling
-- Converted from tuple-based to DistributionParams class usage
-- Changed time units from years to months for precision
-- Added business scenario planning capabilities (conservative, optimistic)

"""


import numpy as np
from .distributions import DistributionParams
from .phases import PhaseParams, MarketParams, SimulationParameters


def create_default_parameters() -> SimulationParameters:
    """
    Create a default parameter set based on industry benchmarks.

    Using my general knowledge of the industry and some publicly available data,
    I set these parameters with the following in mind:
    -- Phase I to approval has ~ 10 - 15% overall success rate
    -- Phase I is the cheapest phase and III is the most expensive
    -- DiMasi (2016) drug development studies reporting pharma economics
    -- FDA approval statistics and approval process timelines from their published reports for 510Ks and other submission standards

    Returns:
        SimulationParameters with industry-standard defaults
        
    Examples:
        -- params = create_default_parameters()
        -- simulator = ClinicalTrialSimulator(params)
        -- results = simulator.run_monte_carlo(n_simulations=1000)
    """
    # Phase I parameters
    phase_1 = PhaseParams(
        name="Phase_1",
        success_probability=0.63,
        cost_millions=DistributionParams(
                'triangular', # Using triangular since Phase I has less uncertainty
                {'low': 5, 'mode': 10, 'high': 15}
        ),
        duration_months=DistributionParams(
            'normal', 
            {'mean': 12, 'std': 2.4}
        )
    )
    
    # Phase II parameters  
    phase_2 = PhaseParams(
        name="Phase_2",
        success_probability=0.31,
        cost_millions=DistributionParams(
            'lognormal', # Using lognormal due to cost uncertainty in phase II
            {'mean': np.log(20), 'sigma': 0.3}  # Centered on prototype mode
        ),
        duration_months=DistributionParams(
            'normal',
            {'mean': 24, 'std': 3.6}
        )
    )
    
    # Phase III parameters
    phase_3 = PhaseParams(
        name="Phase_3",
        success_probability=0.58,
        cost_millions=DistributionParams(
            'lognormal', # Using lognormal due to cost uncertainty in phase III
            {'mean': np.log(100), 'sigma': 0.3}  # Centered on prototype mode
        ),
        duration_months=DistributionParams(
            'normal',
            {'mean': 36, 'std': 6.0} 
        )
    )
    
    # Regulatory review parameters
    regulatory = PhaseParams(
        name="Regulatory_Review",
        success_probability=0.85,
        cost_millions=DistributionParams(
            'triangular',
            {'low': 10, 'mode': 20, 'high': 30}
        ),
        duration_months=DistributionParams(
            'normal',
            {'mean': 12, 'std': 2.4}
        )
    )
    
    # Market parameters
    # Log-normal distribution for revenue reflects high uncertainty
    # Mean corresponds to ~$500M peak revenue with high variability
    market = MarketParams(
        peak_revenue_millions=DistributionParams(
            'lognormal', # lognormal due to revenue uncertainty
            {'mean': np.log(1500), 'sigma': 0.4}
        ),
        time_to_peak_years=DistributionParams(
            'triangular',
            {'low': 2, 'mode': 3, 'high': 5}
        ),
        patent_life_years=12
    )
    
    # Manufacturing and launch costs
    manufacturing_setup = DistributionParams(
        'uniform', # uniform because manufacturing should be a relatively known quantity
        {'low': 20, 'high': 100}
    )
    
    launch_cost = DistributionParams(
        'triangular',
        {'low': 30, 'mode': 75, 'high': 150}
    )
    
    return SimulationParameters(
        phase_1=phase_1,
        phase_2=phase_2,
        phase_3=phase_3,
        regulatory_review=regulatory,
        market=market,
        discount_rate=0.10,  # 10% annual discount rate
        tax_rate=0.25,       # 25% corporate tax rate
        manufacturing_setup_cost_millions=manufacturing_setup,
        launch_cost_millions=launch_cost
    )

def create_conservative_parameters() -> SimulationParameters:
    """
    Create a conservative parameter set with lower success rates and higher costs.
    
    This parameter set reflects more pessimistic assumptions suitable for
    risk-averse decision making or stress testing scenarios.
    
    Returns:
        SimulationParameters with conservative assumptions
    """
    params = create_default_parameters()
    
    # Reduce success probabilities by 15-20%
    params.phase_1.success_probability = 0.60
    params.phase_2.success_probability = 0.25
    params.phase_3.success_probability = 0.50
    params.regulatory_review.success_probability = 0.75
    
    # Increase costs by shifting distributions upward
    # Phase I costs: $3-15M (vs $2-10M default)
    
    params.phase_1.cost_millions = DistributionParams(
        'triangular', {'low': 7, 'mode': 12, 'high': 18}  # Higher than default's 5-10-15
    )
    
    # Phase II costs: (vs $20M centered default)
    params.phase_2.cost_millions = DistributionParams(
        'lognormal', {'mean': np.log(25), 'sigma': 0.4} 
    )
    
    # Phase III costs: (vs $100M centered default)
    params.phase_3.cost_millions = DistributionParams(
        'lognormal', {'mean': np.log(200), 'sigma': 0.4} 
    )
    
    # Significantly reduces peak revenue expectations from default
    params.market.peak_revenue_millions = DistributionParams(
        'lognormal', {'mean': np.log(300), 'sigma': 0.9}
    )
    
    return params

def create_optimistic_parameters() -> SimulationParameters:
    """
    Create an optimistic parameter set based on default's foundation.
 
    This parameter set reflects more hopeful assumptions suitable for
    risk-averse decision making or stress testing scenarios.
        
    Increases success rates and reduces costs relative to default's baseline.
    
    Returns:
        SimulationParameters with optimistic assumptions
    """
    params = create_default_parameters()
    
    # Increase success probabilities from default baseline
    params.phase_1.success_probability = 0.75  # Up from 0.63
    params.phase_2.success_probability = 0.45  # Up from 0.31
    params.phase_3.success_probability = 0.70  # Up from 0.58
    params.regulatory_review.success_probability = 0.90  # Up from 0.85
    
    # Reduce costs from default's baseline
    params.phase_1.cost_millions = DistributionParams(
        'triangular', {'low': 3, 'mode': 7, 'high': 12}
    )
    
    params.phase_2.cost_millions = DistributionParams(
        'lognormal', {'mean': np.log(15), 'sigma': 0.3}
    )
    
    params.phase_3.cost_millions = DistributionParams( # Presumes less likely exorbitant costs, and thus doesn't use lognormal dist
        'triangular', {'low': 40, 'mode': 75, 'high': 120}  # Lower than default
    )
    
    return params

def create_oncology_parameters() -> SimulationParameters:
    """
    Create parameters typical for oncology drug development.
    
    Oncology drugs typically have different risk/reward profiles based on
    specialized trial requirements and market potential.
    
    Returns:
        SimulationParameters tailored for oncology development
    """
    params = create_default_parameters()
    
    # Oncology-specific success rates (higher early phases, challenging late phases)
    params.phase_1.success_probability = 0.70  # Better than default due to dose-finding focus
    params.phase_2.success_probability = 0.40  # Better than default 0.31
    params.phase_3.success_probability = 0.50  # Lower than default due to survival endpoints
    params.regulatory_review.success_probability = 0.80  # Lower than default due to complexity
    
    # Higher costs due to specialized infrastructure
    params.phase_2.cost_millions = DistributionParams(
        'lognormal', {'mean': np.log(35), 'sigma': 0.4}
    )
    
    params.phase_3.cost_millions = DistributionParams(
        'triangular', {'low': 100, 'mode': 175, 'high': 300}
    )
    
    # Higher revenue potential for successful oncology drugs
    params.market.peak_revenue_millions = DistributionParams(
        'lognormal', {'mean': np.log(2000), 'sigma': 0.6}
    )
    
    return params

def create_rare_disease_parameters() -> SimulationParameters:
    """
    Create parameters typical for rare disease drug development.
    
    Rare disease drugs benefit from regulatory incentives but face
    unique challenges in trial design and market size.
    
    Returns:
        SimulationParameters tailored for rare disease development
    """
    params = create_default_parameters()
    
    # Regulatory advantages for rare diseases
    params.phase_1.success_probability = 0.50  # Lower than default, since rare diseases can be harder to get started treating
    params.phase_2.success_probability = 0.45  # Higher than default due to accelerated pathways
    params.phase_3.success_probability = 0.65  # Higher than default due to focused trials
    params.regulatory_review.success_probability = 0.90  # Higher than default due to orphan status
    
    # Lower and tight cost that default, since there are often specialized grant programs or funding incentives for these
    params.phase_1.cost_millions = DistributionParams(
        'normal', {'mean': 5, 'std': 1.5}  
    )

    # Reduced costs due to smaller trial sizes
    params.phase_2.cost_millions = DistributionParams(
        'lognormal', {'mean': np.log(12), 'sigma': 0.4}
    )
    
    params.phase_3.cost_millions = DistributionParams(
        'triangular', {'low': 30, 'mode': 60, 'high': 100}
    )
    
    # Lower absolute revenue but faster uptake
    params.market.peak_revenue_millions = DistributionParams(
        'lognormal', {'mean': np.log(800), 'sigma': 0.7}
    )
    
    # Faster peak than default, because of both high need urgency and low need population
    params.market.time_to_peak_years = DistributionParams(
        'triangular', {'low': 1, 'mode': 2, 'high': 3}  
    )
    
    return params
