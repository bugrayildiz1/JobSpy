from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from jobspy import scrape_jobs
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for dev; restrict in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/jobs")
def get_jobs(
    search_term: str = '"graduate program" OR internship OR "early career"',
    location: str = "Amsterdam, Netherlands",
    results: int = 20,
    hours_old: int = 48,
    country_indeed: Optional[str] = "Netherlands",
    site_name: Optional[List[str]] = Query(default=["linkedin", "indeed"]),
    job_type: Optional[str] = None,
    is_remote: Optional[bool] = None,
    easy_apply: Optional[bool] = None,
    enforce_annual_salary: Optional[bool] = False,
    linkedin_fetch_description: Optional[bool] = True,
    company_industry: Optional[str] = None,
    job_level: Optional[str] = None,
):
    try:
        jobs = scrape_jobs(
            site_name=site_name,
            search_term=search_term,
            location=location,
            results_wanted=results,
            hours_old=hours_old,
            country_indeed=country_indeed,
            job_type=job_type,
            is_remote=is_remote,
            easy_apply=easy_apply,
            enforce_annual_salary=enforce_annual_salary,
            linkedin_fetch_description=linkedin_fetch_description,
            verbose=1,
        )

        df = jobs

        if job_level:
            df = df[df['job_level'].str.contains(job_level, na=False, case=False)]
        if company_industry:
            df = df[df['company_industry'].str.contains(company_industry, na=False, case=False)]

        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}
