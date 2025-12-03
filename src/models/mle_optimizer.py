"""
MLE Optimizer Module
====================
This module implements Maximum Likelihood Estimation (MLE) for calibrating
Heston model parameters from historical data.
"""

import numpy as np
import warnings
from scipy.optimize import minimize
from typing import Dict, List


class MLEOptimizer:
    """
    Maximum Likelihood Estimation optimizer for Heston model parameters.
    
    This class estimates the Heston model parameters (kappa, theta, sigma, rho)
    by maximizing the likelihood function based on observed asset returns and volatilities.
    """
    
    def __init__(self, Q: List[float], V: List[float], r: float, 
                 n_guesses: int = 10):
        """
        Initialize MLEOptimizer.
        
        Parameters:
        -----------
        Q : list of float
            Vector of change in asset returns
        V : list of float
            Vector of rolling volatility values
        r : float
            Risk-free interest rate
        n_guesses : int
            Number of random initial guesses for optimization (default: 10)
        """
        self.Q = np.array(Q)
        self.V = np.array(V)
        self.r = r
        self.n_guesses = n_guesses
    
    def transform_parameters(self, x: np.ndarray) -> np.ndarray:
        """
        Transform unconstrained optimization variables to constrained Heston parameters.
        
        This transformation ensures parameters stay within valid bounds:
        - kappa (κ): [0.5, 5] - mean reversion rate
        - theta (θ): [0, 1] - long-term volatility
        - sigma (σ): [0, 5] - volatility of volatility
        - rho (ρ): [-1, 0] - correlation (typically negative)
        
        Parameters:
        -----------
        x : np.ndarray
            Unconstrained optimization variables [x1, x2, x3, x4]
        
        Returns:
        --------
        np.ndarray
            Constrained Heston parameters [kappa, theta, sigma, rho]
        """
        x1, x2, x3, x4 = x
        k     = 0.5 + 4.5 * (1 / (1 + np.exp(-x1)))
        theta = 1   / (1 + np.exp(-x2))
        sigma = 5   / (1 + np.exp(-x3))
        rho   = -1  / (1 + np.exp(-x4))
        return np.array([k, theta, sigma, rho])
    
    def transform_parameters_inverse(self, params: np.ndarray) -> np.ndarray:
        """
        Inverse transformation from constrained parameters to unconstrained variables.
        
        Parameters:
        -----------
        params : np.ndarray
            Constrained Heston parameters [kappa, theta, sigma, rho]
        
        Returns:
        --------
        np.ndarray
            Unconstrained optimization variables [x1, x2, x3, x4]
        """
        k, theta, sigma, rho = params
        try:
            x1 = -np.log((4.5 / (k - 0.5)) - 1)
            x2 = -np.log((1 / theta) - 1)
            x3 = -np.log((5 / sigma) - 1)
            x4 = -np.log((-1 / rho) - 1)
            return np.array([x1, x2, x3, x4])
        except Exception:
            return np.full(4, np.nan)
    
    def log_likelihood_transformed(self, x: np.ndarray) -> float:
        """
        Calculate negative log-likelihood for transformed parameters.
        
        The log-likelihood is based on the joint distribution of asset returns
        and volatility under the Heston model dynamics.
        
        Parameters:
        -----------
        x : np.ndarray
            Unconstrained optimization variables
        
        Returns:
        --------
        float
            Negative log-likelihood value (to be minimized)
        """
        params = self.transform_parameters(x)
        k, θ, σ, ρ = params
        Q, V, r = self.Q, self.V, self.r
        n = len(V) - 1
        ll = 0.0
        
        try:
            for t in range(n):
                # Log-likelihood components
                term1 = -np.log(2 * np.pi) - np.log(σ) - np.log(V[t])
                term2 = -0.5 * np.log(1 - ρ**2)
                
                # Increments
                ΔQ = Q[t + 1] - 1 - r
                ΔV = V[t + 1] - V[t] - θ * k + k * V[t]
                
                # Likelihood terms
                frac1 = -ΔQ**2 / (2 * V[t] * (1 - ρ**2))
                frac2 = ρ * ΔQ * ΔV / (V[t] * σ * (1 - ρ**2))
                frac3 = -ΔV**2 / (2 * σ**2 * V[t] * (1 - ρ**2))
                
                ll += term1 + term2 + frac1 + frac2 + frac3
        except:
            return np.inf  # Return large value if calculation fails
        
        return -ll  # Return negative for minimization
    
    def generate_initial_guesses(self) -> List[List[float]]:
        """
        Generate random initial guesses for optimization.
        
        Returns:
        --------
        list
            List of initial parameter guesses [kappa, theta, sigma, rho]
        """
        eps = 1e-6
        guesses = []
        
        for _ in range(self.n_guesses):
            k = np.random.uniform(0.5 + eps, 5 - eps)
            θ = np.random.uniform(0 + eps, 1 - eps)
            σ = np.random.uniform(0 + eps, 5 - eps)
            ρ = np.random.uniform(-1 + eps, 0 - eps)
            guesses.append([k, θ, σ, ρ])
        
        return guesses
    
    def estimate_parameters_robust(self) -> Dict:
        """
        Robustly estimate Heston parameters using multiple initial guesses and methods.
        
        This method tries multiple optimization algorithms with different starting points
        to find the global maximum of the likelihood function.
        
        Returns:
        --------
        dict
            Dictionary containing:
            - 'k' (kappa): Mean reversion rate
            - 'theta': Long-term volatility
            - 'sigma': Volatility of volatility
            - 'rho': Correlation coefficient
            - 'log_likelihood': Maximum log-likelihood value
            - 'method': Optimization method used
            - 'initial_guess': Best initial guess
            - 'message': Optimization message
        
        Raises:
        -------
        ValueError
            If all optimization attempts fail
        """
        initial_guesses = self.generate_initial_guesses()
        best = {'likelihood': -np.inf, 'result': None}
        methods = ['L-BFGS-B', 'SLSQP', 'TNC']
        
        for guess in initial_guesses:
            x0 = self.transform_parameters_inverse(guess)
            if not np.isfinite(x0).all():
                continue
            
            for m in methods:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    res = minimize(
                        self.log_likelihood_transformed,
                        x0,
                        method=m,
                        options={'maxiter': 1000, 'ftol': 1e-8, 'gtol': 1e-8}
                    )
                
                if res.success:
                    ll = -res.fun
                    if ll > best['likelihood']:
                        best = {
                            'likelihood': ll,
                            'result': res,
                            'method': m,
                            'initial': guess
                        }
        
        if best['result'] is None:
            raise ValueError("Optimization failed for all attempts")
        
        params = self.transform_parameters(best['result'].x)
        
        return {
            'k': params[0],
            'theta': params[1],
            'sigma': params[2],
            'rho': params[3],
            'log_likelihood': best['likelihood'],
            'method': best['method'],
            'initial_guess': best['initial'],
            'message': best['result'].message
        }
    
    def print_estimation_results(self, results: Dict) -> None:
        """
        Print formatted estimation results.
        
        Parameters:
        -----------
        results : dict
            Dictionary of estimation results from estimate_parameters_robust()
        """
        print("\n" + "="*60)
        print("HESTON MODEL PARAMETER ESTIMATION RESULTS")
        print("="*60)
        print(f"\nEstimated Parameters:")
        print(f"  κ (kappa):  {results['k']:.6f}  - Mean reversion rate")
        print(f"  θ (theta):  {results['theta']:.6f}  - Long-term volatility")
        print(f"  σ (sigma):  {results['sigma']:.6f}  - Volatility of volatility")
        print(f"  ρ (rho):    {results['rho']:.6f}  - Correlation coefficient")
        print(f"\nOptimization Details:")
        print(f"  Log-likelihood: {results['log_likelihood']:.2f}")
        print(f"  Method used:    {results['method']}")
        print(f"  Status:         {results['message']}")
        print("="*60 + "\n")
