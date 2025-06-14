"""
Distribution parameter classes for clinical trial simulation.

This module defines classes for managing probability distributions
used throughout the simulation framework.
"""
"""
This is an evolution from the version extracted verbatim from Working_Prototype.py

**Evolution Rationale:**
To support more sophisticated risk modeling and simulation to support clinical trial decisions,
this version converts the prototype's tuple-based distribution sampling into a class.
This version builds upon the prototype to achieve the following:
-- Facilitates proper enterprise parameter management by establishing an object-oriented DistributionParams class
-- Expands distribution support by allowing for different shapes
-- Adds mathematical parameter validation ensuring statistical integrity
-- Includes built-in statistical methods (mean, std) enabling risk calculations in other modules
-- Supports scenario planning across different therapeutic areas by providing flexible distribution patterns of cost/timeline uncertainty
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Union


@dataclass
class DistributionParams:
    """
    Class to define probability distribution parameters.
    
    Supports common distributions used in pharmaceutical modeling:
    - triangular: For expert judgment with min/mode/max
    - normal: For symmetric uncertainty
    - lognormal: For multiplicative processes (revenues, costs)
    - uniform: For pure uncertainty within bounds
    - beta: For probabilities and percentages
    
    Attributes:
        dist_type: Type of distribution ('triangular', 'normal', 'lognormal', 'uniform', 'beta')
        params: Dictionary of distribution-specific parameters
        
     """
    
    dist_type: str
    params: Dict[str, float]
    
    def __post_init__(self):
        """Validate distribution parameters after initialization."""
        self._validate_params()
    
    def _validate_params(self) -> None:
        """Validate that required parameters are present for the distribution type."""
        required_params = {
            'triangular': ['low', 'mode', 'high'],
            'normal': ['mean', 'std'],
            'lognormal': ['mean', 'sigma'],
            'uniform': ['low', 'high'],
            'beta': ['alpha', 'beta']
        }
        
        if self.dist_type not in required_params:
            raise ValueError(f"Unsupported distribution type: {self.dist_type}")
        
        required = required_params[self.dist_type]
        missing = [param for param in required if param not in self.params]
        
        if missing:
            raise ValueError(
                f"Missing required parameters for {self.dist_type} distribution: {missing}"
            )
        
        # Additional validation for specific distributions
        if self.dist_type == 'triangular':
            low, mode, high = self.params['low'], self.params['mode'], self.params['high']
            if not (low <= mode <= high):
                raise ValueError(
                    f"Triangular distribution requires low <= mode <= high, "
                    f"got low={low}, mode={mode}, high={high}"
                )
        
        if self.dist_type == 'normal' and self.params['std'] <= 0:
            raise ValueError("Normal distribution standard deviation must be positive")
        
        if self.dist_type == 'lognormal' and self.params['sigma'] <= 0:
            raise ValueError("Lognormal distribution sigma must be positive")
        
        if self.dist_type == 'uniform':
            if self.params['low'] >= self.params['high']:
                raise ValueError("Uniform distribution requires low < high")
        
        if self.dist_type == 'beta':
            if self.params['alpha'] <= 0 or self.params['beta'] <= 0:
                raise ValueError("Beta distribution parameters must be positive")
    
    def sample(self, size: int = 1) -> np.ndarray:
        """
        Generate random samples from the distribution.
        
        Args:
            size: Number of samples to generate
            
        Returns:
            Array of random samples from the distribution
            
        Raises:
            ValueError: If distribution type is not supported
        """
        if self.dist_type == 'triangular':
            return np.random.triangular(
                self.params['low'], 
                self.params['mode'], 
                self.params['high'], 
                size
            )
        elif self.dist_type == 'normal':
            return np.random.normal(
                self.params['mean'], 
                self.params['std'], 
                size
            )
        elif self.dist_type == 'lognormal':
            return np.random.lognormal(
                self.params['mean'], 
                self.params['sigma'], 
                size
            )
        elif self.dist_type == 'uniform':
            return np.random.uniform(
                self.params['low'], 
                self.params['high'], 
                size
            )
        elif self.dist_type == 'beta':
            return np.random.beta(
                self.params['alpha'], 
                self.params['beta'], 
                size
            )
        else:
            raise ValueError(f"Unsupported distribution type: {self.dist_type}")
    
    def mean(self) -> float:
        """
        Calculates theoretical mean of the distribution.
        
        Returns:
            Expected value of the distribution
        """
        if self.dist_type == 'triangular':
            return (self.params['low'] + self.params['mode'] + self.params['high']) / 3
        elif self.dist_type == 'normal':
            return self.params['mean']
        elif self.dist_type == 'lognormal':
            return np.exp(self.params['mean'] + self.params['sigma']**2 / 2)
        elif self.dist_type == 'uniform':
            return (self.params['low'] + self.params['high']) / 2
        elif self.dist_type == 'beta':
            alpha, beta = self.params['alpha'], self.params['beta']
            return alpha / (alpha + beta)
        else:
            raise ValueError(f"Mean calculation not implemented for {self.dist_type}")
    
    def std(self) -> float:
        """
        Calculates the theoretical standard deviation of the distribution.
        
        It is necessary to build this custom std method rather than use the native np.std
        in order to ensure exact statistical properties and generate more precise risk calculations
        than would be easily available if I used numpy's random sampling method.

        Returns:
            distribution std
        """
        if self.dist_type == 'triangular':
            a, b, c = self.params['low'], self.params['mode'], self.params['high']
            return np.sqrt((a**2 + b**2 + c**2 - a*b - a*c - b*c) / 18)
        elif self.dist_type == 'normal':
            return self.params['std']
        elif self.dist_type == 'lognormal':
            sigma_sq = self.params['sigma']**2
            return np.sqrt((np.exp(sigma_sq) - 1) * np.exp(2*self.params['mean'] + sigma_sq))
        elif self.dist_type == 'uniform':
            return (self.params['high'] - self.params['low']) / np.sqrt(12)
        elif self.dist_type == 'beta':
            alpha, beta = self.params['alpha'], self.params['beta']
            return np.sqrt(alpha * beta / ((alpha + beta)**2 * (alpha + beta + 1)))
        else:
            raise ValueError(f"Std calculation not implemented for {self.dist_type}")
    
    def __repr__(self) -> str:
        """String representation of the distribution."""
        return f"DistributionParams('{self.dist_type}', {self.params})"