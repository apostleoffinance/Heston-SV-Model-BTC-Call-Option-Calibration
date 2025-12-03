"""
Heston Model Implementation
============================
This module contains the implementation of the Heston stochastic volatility model.
The Heston model is used for pricing options and simulating asset price paths
with stochastic volatility.
"""

import numpy as np
from scipy.integrate import quad
from typing import Tuple


class HestonModel:
    """
    Implementation of the Heston stochastic volatility model.
    
    The Heston model describes the evolution of asset prices with stochastic volatility:
    - dS_t = μS_t dt + √V_t S_t dW^S_t
    - dV_t = κ(θ - V_t)dt + σ√V_t dW^V_t
    
    where W^S and W^V are correlated Brownian motions with correlation ρ.
    """
    
    def __init__(self, S0: float, r: float, kappa: float, theta: float, 
                 sigma: float, rho: float, v0: float):
        """
        Initialize the Heston Model.
        
        Parameters:
        -----------
        S0 : float
            Initial stock/asset price
        r : float
            Risk-free interest rate
        kappa : float
            Mean reversion rate of volatility
        theta : float
            Long-term average volatility
        sigma : float
            Volatility of volatility (vol of vol)
        rho : float
            Correlation between asset returns and volatility
        v0 : float
            Initial volatility
        """
        self.S0 = S0
        self.r = r
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma
        self.rho = rho
        self.v0 = v0
    
    def heston_characteristic_function(self, phi: complex, T: float) -> complex:
        """
        Compute the Heston Model characteristic function.
        
        The characteristic function is used in the semi-analytical pricing formula.
        
        Parameters:
        -----------
        phi : complex
            Frequency parameter for characteristic function
        T : float
            Time to maturity
        
        Returns:
        --------
        complex
            Value of the characteristic function
        """
        tau = T
        i = complex(0, 1)
        
        # Compute intermediate terms
        M = np.sqrt((self.rho * self.sigma * i * phi - self.kappa)**2 + 
                   self.sigma**2 * (i * phi + phi**2))
        N = ((self.rho * self.sigma * i * phi - self.kappa - M) / 
             (self.rho * self.sigma * i * phi - self.kappa + M))
        
        # Compute A, B, C components
        A = (self.r * i * phi * tau + 
             (self.kappa * self.theta / self.sigma**2) * (
                 -(self.rho * self.sigma * i * phi - self.kappa - M) * tau - 
                 2 * np.log((1 - N * np.exp(M * tau)) / (1 - N))
             ))
        B = 0
        C = (((np.exp(M * tau) - 1) * 
              (self.rho * self.sigma * i * phi - self.kappa - M)) / 
             (self.sigma**2 * (1 - N * np.exp(M * tau))))
        
        # Characteristic function
        f = np.exp(A + B * np.log(self.S0) + C * self.v0 + i * phi * np.log(self.S0))
        return f
    
    def integrand(self, phi: float, K: float, T: float, flag: int) -> float:
        """
        Integrand for the Heston option price formula.
        
        Parameters:
        -----------
        phi : float
            Integration variable
        K : float
            Strike price
        T : float
            Time to maturity
        flag : int
            Flag for which integral (1 or 2)
        
        Returns:
        --------
        float
            Real part of the integrand
        """
        i = complex(0, 1)
        if flag == 1:
            f = self.heston_characteristic_function(phi - i, T)
            return np.real((K**(-i * phi) * f) / (i * phi))
        else:
            f = self.heston_characteristic_function(phi, T)
            return np.real((K**(-i * phi) * f) / (i * phi))
    
    def heston_option_price(self, K: float, T: float) -> float:
        """
        Compute European call option price using Heston model semi-analytical formula.
        
        Parameters:
        -----------
        K : float
            Strike price
        T : float
            Time to maturity in years
        
        Returns:
        --------
        float
            Call option price
        """
        # Compute the two integrals using numerical integration
        integral1, _ = quad(self.integrand, 0, 100, args=(K, T, 1))
        integral2, _ = quad(self.integrand, 0, 100, args=(K, T, 2))
        
        # Option price formula
        C = (0.5 * self.S0 + 
             (np.exp(-self.r * T) / np.pi) * integral1 - 
             K * np.exp(-self.r * T) * (0.5 + (1 / np.pi) * integral2))
        return C
    
    def heston_monte_carlo(self, T: float, N: int, mu: float, 
                          num_sims: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        """
        Monte Carlo simulation of the Heston Model.
        
        Uses the Euler-Maruyama discretization scheme with full truncation
        to ensure volatility stays positive.
        
        Parameters:
        -----------
        T : float
            Time horizon for simulation (in years)
        N : int
            Number of time steps
        mu : float
            Drift term (typically the risk-free rate)
        num_sims : int
            Number of simulation paths (default: 500)
        
        Returns:
        --------
        tuple
            (S, V) where:
            - S: ndarray of shape (num_sims, N+1) with stock price paths
            - V: ndarray of shape (num_sims, N+1) with volatility paths
        """
        dt = T / N  # Time step size
        
        # Generate correlated Brownian motions for all simulations
        dW2 = np.random.normal(0, 1, size=(num_sims, N))
        dW1 = (self.rho * dW2 + 
               np.sqrt(1 - self.rho**2) * np.random.normal(0, 1, size=(num_sims, N)))
        
        # Initialize arrays for stock prices and volatilities
        S = np.zeros((num_sims, N + 1))
        V = np.zeros((num_sims, N + 1))
        S[:, 0] = self.S0
        V[:, 0] = self.v0
        
        # Vectorized Euler-Maruyama method
        for i in range(N):
            # Update volatility with full truncation scheme
            V[:, i+1] = (V[:, i] + 
                        self.kappa * (self.theta - np.maximum(V[:, i], 0)) * dt + 
                        self.sigma * np.sqrt(np.maximum(V[:, i], 0)) * dW2[:, i] * np.sqrt(dt))
            V[:, i+1] = np.maximum(V[:, i+1], 0)
            
            # Update stock price
            S[:, i+1] = S[:, i] * (1 + mu * dt + 
                                   np.sqrt(V[:, i]) * dW1[:, i] * np.sqrt(dt))
        
        return S, V
