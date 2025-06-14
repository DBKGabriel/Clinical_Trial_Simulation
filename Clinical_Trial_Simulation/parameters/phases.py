"""
Classes for clinical trial phases and market parameters.

This module enables the sophisticated parameter creation functions in defaults.py
by providing the underlying data structures and validation logic used to organize parameters
according to each clinical trial phases, different market conditions/expectations, 
and overall simulation configuration.
"""
"""
Here, I begin evolving the prototype_extracted_defaults.py.
I extracted that module pretty much verbatim from the prototype. 
In extending and upgrading it, I realized it was getting needlessly long and 
I could foresee problems down the road arising from its inflexibility. 
For example, I wanted to add different distinct default parameter sets
that could be used when running the simulation. Adding that in alongside the phases,
I felt it was getting needlessly long. 

**Architectural Rationale:**
I created the prototype with flat dictionaries that mixed data definitions with parameter values.
This made it difficult to validate, extend, and maintain. 

So I split it into 2 modules to support enterprise-grade parameter architecture:
-- defaults.py,
-- phases.py

This NEW module (phases.py) defines 3 distinct classes: PhaseParams, MarketParams, and SimulationParameters.
This separates concerns by:
-- Creating dedicated classes to organize and validate parameters
-- Implementing business rule validation (probabilities 0-1, positive costs, etc.)
-- Enabling comprehensive parameter validation by using type hints and runtime checks to catch parameter errors early
-- Supporting complex parameter relationships and dependencies
-- Providing a foundation for therapeutic area-specific parameter sets
-- Supporting complex parameter relationships (phases, market conditions, financial assumptions)
-- Facilitating enterprise-grade parameter management with proper error handling

**Key Architectural Benefits:**
-- Separation of concerns: data structures vs. parameter values
-- Extensible design supporting new therapeutic areas and parameter types
-- Validation ensures parameter integrity for regulatory-quality simulations
-- Object-oriented design enables sophisticated parameter management
-- Clear interfaces for integration with simulation engines


*List of notable changes (non-exhaustive)*
-- Converted from tuple-based distributions to DistributionParams class usage
-- Added comprehensive parameter validation logic in __post_init__ methods
-- Added utility methods (get_all_phases, total_expected_cost, etc.) for parameter management
-- Changed the time arg in phases to months instead of years
-- Included market_penetration_rate parameter for future market modeling extensions

*Next steps*
-- I like my codes like I like my bills! Single issue! So I might extract marketparams and simulationparams into separate codes at some point.

"""

from dataclasses import dataclass, field
from typing import Optional
from .distributions import DistributionParams


@dataclass
class PhaseParams:
    """
    Parameters for a single clinical trial phase.
    
    Attributes:
        name: Phase identifier (e.g., "Phase_1", "Phase_2")
        success_probability: Historical probability of phase success (0.0 to 1.0)
        duration_months: Distribution of phase duration in months
        cost_millions: Distribution of phase cost in millions USD
        enrollment_time_months: Optional distribution for patient enrollment time
        
    Examples:
        -- phase1 = PhaseParams(
             name="Phase_1",
             success_probability=0.63,
             duration_months=DistributionParams('triangular', {'low': 8, 'mode': 12, 'high': 18}),
             cost_millions=DistributionParams('triangular', {'low': 2, 'mode': 5, 'high': 10})
            )
    """
    
    name: str
    success_probability: float
    duration_months: DistributionParams
    cost_millions: DistributionParams
    enrollment_time_months: Optional[DistributionParams] = None
    
    def __post_init__(self):
        """Validate parameters after initialization."""
        if not 0.0 <= self.success_probability <= 1.0:
            raise ValueError(
                f"Success probability must be between 0 and 1, got {self.success_probability}"
            )
        
        if not isinstance(self.duration_months, DistributionParams):
            raise TypeError("duration_months must be a DistributionParams instance")
        
        if not isinstance(self.cost_millions, DistributionParams):
            raise TypeError("cost_millions must be a DistributionParams instance")
        
        if (self.enrollment_time_months is not None and 
            not isinstance(self.enrollment_time_months, DistributionParams)):
            raise TypeError("enrollment_time_months must be a DistributionParams instance or None")


@dataclass
class MarketParams:
    """
    Parameters for market outcomes and revenue modeling.
    
    Attributes:
        peak_revenue_millions: Distribution of peak annual revenue in millions USD
        time_to_peak_years: Distribution of years to reach peak revenue
        patent_life_years: Total patent protection period in years
        market_penetration_rate: Optional distribution for market penetration dynamics
        
    Examples:
        -- market = MarketParams(
             peak_revenue_millions=DistributionParams('lognormal', {'mean': 6.2, 'sigma': 0.8}),
             time_to_peak_years=DistributionParams('triangular', {'low': 2, 'mode': 3, 'high': 5}),
             patent_life_years=12
            )
    """
    
    peak_revenue_millions: DistributionParams
    time_to_peak_years: DistributionParams
    patent_life_years: float = 12.0
    market_penetration_rate: Optional[DistributionParams] = None # Reserved for future implementation
    
    def __post_init__(self):
        """Validate parameters after initialization."""
        if not isinstance(self.peak_revenue_millions, DistributionParams):
            raise TypeError("peak_revenue_millions must be a DistributionParams instance")
        
        if not isinstance(self.time_to_peak_years, DistributionParams):
            raise TypeError("time_to_peak_years must be a DistributionParams instance")
        
        if self.patent_life_years <= 0:
            raise ValueError("Patent life must be positive")
        
        if (self.market_penetration_rate is not None and 
            not isinstance(self.market_penetration_rate, DistributionParams)):
            raise TypeError("market_penetration_rate must be a DistributionParams instance or None")


@dataclass
class SimulationParameters:
    """
    Complete parameter set for clinical trial simulation.
    
    This class aggregates all parameters needed for a complete simulation run,
    including clinical phase parameters, market conditions, and financial assumptions.
    
    Attributes:
        phase_1: Phase I trial parameters
        phase_2: Phase II trial parameters  
        phase_3: Phase III trial parameters
        regulatory_review: Regulatory approval parameters
        market: Market outcome parameters
        discount_rate: Annual discount rate for NPV calculations (default: 0.10)
        tax_rate: Corporate tax rate (default: 0.25)
        manufacturing_setup_cost_millions: Optional manufacturing setup costs
        launch_cost_millions: Optional product launch costs
        
    Examples:
        -- params = SimulationParameters(
             phase_1=phase1_params,
             phase_2=phase2_params,
             phase_3=phase3_params,
             regulatory_review=regulatory_params,
             market=market_params,
             discount_rate=0.12,
             tax_rate=0.25
             )
    """
    
    # Clinical phases (required)
    phase_1: PhaseParams
    phase_2: PhaseParams
    phase_3: PhaseParams
    regulatory_review: PhaseParams
    
    # Market parameters (required)
    market: MarketParams
    
    # Financial parameters
    discount_rate: float = 0.10
    tax_rate: float = 0.25
    
    # Additional cost parameters (optional)
    manufacturing_setup_cost_millions: Optional[DistributionParams] = None
    launch_cost_millions: Optional[DistributionParams] = None
    
    def __post_init__(self):
        """Validate parameters after initialization."""
        # Validate required phase parameters
        required_phases = [
            ('phase_1', self.phase_1),
            ('phase_2', self.phase_2), 
            ('phase_3', self.phase_3),
            ('regulatory_review', self.regulatory_review)
        ]
        
        for name, phase in required_phases:
            if not isinstance(phase, PhaseParams):
                raise TypeError(f"{name} must be a PhaseParams instance")
        
        # Validate market parameters
        if not isinstance(self.market, MarketParams):
            raise TypeError("market must be a MarketParams instance")
        
        # Validate financial parameters
        if not 0.0 <= self.discount_rate <= 1.0:
            raise ValueError("Discount rate must be between 0 and 1")
        
        if not 0.0 <= self.tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0 and 1")
        
        # Validate optional cost parameters
        optional_costs = [
            ('manufacturing_setup_cost_millions', self.manufacturing_setup_cost_millions),
            ('launch_cost_millions', self.launch_cost_millions)
        ]
        
        for name, cost_param in optional_costs:
            if cost_param is not None and not isinstance(cost_param, DistributionParams):
                raise TypeError(f"{name} must be a DistributionParams instance or None")
    
    def get_all_phases(self) -> list[PhaseParams]:
        """
        Get all clinical trial phases in order.
        
        Returns:
            List of PhaseParams in order of execution
        """
        return [self.phase_1, self.phase_2, self.phase_3, self.regulatory_review]
    
    def get_phase_by_name(self, phase_name: str) -> Optional[PhaseParams]:
        """
        Get a specific phase by name.
        
        Args:
            phase_name: Name of the phase to retrieve
            
        Returns:
            PhaseParams instance if found, None otherwise
        """
        for phase in self.get_all_phases():
            if phase.name == phase_name:
                return phase
        return None
    
    def total_expected_cost(self) -> float:
        """
        Calculate total expected development cost.
        
        Returns:
            Expected total cost in millions USD
        """
        total = 0.0
        
        # Add expected costs from all phases
        for phase in self.get_all_phases():
            total += phase.cost_millions.mean()
        
        # Add optional costs if specified
        if self.manufacturing_setup_cost_millions:
            total += self.manufacturing_setup_cost_millions.mean()
        
        if self.launch_cost_millions:
            total += self.launch_cost_millions.mean()
        
        return total
    
    def total_expected_time(self) -> float:
        """
        Calculate total expected development time.
        
        Returns:
            Expected total time in months
        """
        return sum(phase.duration_months.mean() for phase in self.get_all_phases())
    
    def overall_success_probability(self) -> float:
        """
        Calculate overall probability of success through all phases.
        
        Returns:
            Combined probability of success (0.0 to 1.0)
        """
        prob = 1.0
        for phase in self.get_all_phases():
            prob *= phase.success_probability
        return prob