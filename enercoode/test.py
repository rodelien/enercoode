from pathlib import Path

import pandas as pd

from src.path import DATA_PATH, IPOPT_PATH
import src.constants as cst
import src.model as mod


if __name__ == "__main__":

    profiles = pd.read_excel(DATA_PATH / "test_data.xlsx", index_col=0)

    skills = profiles.loc[cst.SKILLS]
    salaries = profiles.loc[cst.SLRY]

    sol, obj = mod.solve_model(
        skills=skills,
        salaries=salaries,
        levels=cst.LEVELS,
        ipopt_path=IPOPT_PATH,
    )
    
    from_sol = pd.Series(
        {per: mod.compute_salary(profile=val, weights=sol) for per, val in skills.items()}
    )

    slry_err = (from_sol - salaries).abs()

    print(f"Total Error is {obj}")
    print(f"Max Error is {slry_err.max()}\n")

    print("Step values are:")
    print(sol[cst.STEP])