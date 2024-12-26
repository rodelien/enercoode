"""Module with functions to model and solve the problem"""
from typing import Union, List, Optional, Dict, Tuple
from pathlib import Path

import pandas as pd

import pyomo.environ as pyo
from pyomo.core.base.var import IndexedVar

import src.constants as cst


def compute_salary(
    *,
    profile: Union[dict, pd.Series],
    weights: Union[IndexedVar, pd.DataFrame],
) -> Union[float, pyo.Expression]:
    """Compute the salary of the given profile (pair of domain and level)
    
    Parameters
    ----------
    profile: pandas series
        series with th domains as index and the associated skill level as value
    weights: indexed variable or pandas dataframe
        the values given for each level of each skill"""
    
    domains = profile.index

    index, cols = {}, {}
    if isinstance(weights, pd.DataFrame):
        index, cols = weights.index, weights.columns
        # for indexation below
        weights = weights.stack()
    elif isinstance(weights, IndexedVar):
        index, cols = zip(*list(weights.index_set()))
    else:
        raise ValueError("weights must be a pandas dataframe or a pyomo variable")
    index, cols = set(index), set(cols)

    if set(domains) == cols:
        return sum(weights[(profile[skl], skl)] for skl in domains)
    elif set(domains) == set(index):
        return sum(weights[(skl, profile[skl])] for skl in domains)
    
    raise ValueError(f"Domains ({domains}) don't match weights index/columns")


def extract_gaps(weights_gap: IndexedVar) -> pd.Series:
    
    return pd.Series({idx: var.value for idx, var in weights_gap.items()})


def extract_weights(weights: IndexedVar) -> pd.DataFrame:

    return pd.Series({idx: var.value for idx, var in weights.items()}).unstack()


def solve_model(
    skills: pd.DataFrame,
    salaries: pd.Series,
    levels: List[str],
    ipopt_path: Union[Path, str],
    fix_gaps: Optional[Dict[str, float]] = None,
    fix_levels: Optional[Dict[str, float]] = None,
) -> Tuple[pd.DataFrame, float]:
    """Builds and solves the model
    
    Parameters
    ----------
    skills: pandas dataframe
        Table with people names as columns and domains as index.
    salaries: pandas series
        series with the people's salaries
    levels: list of strings
        the labels of the different levels
    ipopt_path: path
        the path to the correct ipopt executable ('ipopt.exe')
    fix_gaps: dict, optional
        if a dictionary is provided featuring domains names as keys and numerical values,
        imposes the given values to the corresponding domain gaps
    fix_levels: dict, optional
        if a dictionary is provided featuring (domain, level) tuples as keys and numerical values,
        imposes the given values to the corresponding (domain, level) pairs
        
    Return
    ------
    solutions: pandas datafarme
        the weights and weights gaps for each domain"""
    
    domains = skills.index

    model = pyo.ConcreteModel()
    model.weights = pyo.Var(domains, levels, within=pyo.NonNegativeReals)
    model.weights_gap = pyo.Var(domains, within=pyo.NonNegativeReals)

    # Main constraints imposing the gap between two successive levels values per domain
    skill_gaps = {}
    for dom in domains:
        for lv1, lv2 in zip(levels[:-1], levels[1:]):
            expr = model.weights[(dom, lv1)] - model.weights[(dom, lv2)] == model.weights_gap[dom]
            skill_gaps[(dom, lv1, lv2)] = expr

    model.skill_gaps_constraint = pyo.Constraint(skill_gaps.keys(), expr=skill_gaps)

    # Additional constraints if some values are preferred for the gaps
    if fix_gaps is not None:
        fixed_gaps = {}
        for domain, value in fix_gaps.items():
            fixed_gaps[domain] = model.weights_gap[domain] == value

        model.fixed_gaps_constraint = pyo.Constraint(fixed_gaps.keys(), expr=fixed_gaps)

    # Additional constraints if some values are preferred for sepcific domain/level combinations
    if fix_levels is not None:
        fixed_lvls = {}
        for (domain, level), value in fix_levels.items():
            fixed_lvls[domain] = model.weights[(domain, level)] == value

        model.fixed_lvls_constraint = pyo.Constraint(fixed_lvls.keys(), expr=fixed_lvls)


    # Objectif = somme des erreurs au carré
    objexpr = sum(
        (compute_salary(profile=val, weights=model.weights) - salaries[per]) ** 2
        for per, val in skills.items()
    )

    model.obj = pyo.Objective(expr=objexpr, sense=pyo.minimize)

    solver = pyo.SolverFactory("ipopt", executable=ipopt_path)
    solver.solve(model)
    obj = model.obj()

    weights_gap = extract_gaps(model.weights_gap)
    weights = extract_weights(model.weights)

    return pd.concat([weights, weights_gap.rename(cst.STEP)], axis=1), obj