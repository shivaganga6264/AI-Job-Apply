import os
import json

from datetime import datetime

from dotenv import load_dotenv

from playwright.sync_api import sync_playwright

# Load .env variables
load_dotenv()


def apply_jobs():

    # Secure Credentials
    EMAIL = os.getenv("EMAIL")

    PASSWORD = os.getenv("PASSWORD")

    # Job Roles
    JOB_ROLES = [

        "full stack developer",

        "frontend developer",

        "software engineer",

        "python developer",

        "backend developer",

        "data analyst"
    ]

    # Store Applied Jobs
    applied_jobs = set()

    # Total Applied Counter
    total_applied = 0

    with sync_playwright() as p:

        # Launch Browser
        browser = p.chromium.launch(
            headless=False
        )

        # Create Main Page
        page = browser.new_page()

        # Open Login Page
        page.goto(
            "https://www.naukri.com/nlogin/login"
        )

        # Enter Email
        page.fill(
            'input[placeholder="Enter Email ID / Username"]',
            EMAIL
        )

        # Enter Password
        page.fill(
            'input[placeholder="Enter Password"]',
            PASSWORD
        )

        # Click Login
        page.click(
            'button[type="submit"]'
        )

        print("Logging In...")

        # Wait After Login
        page.wait_for_timeout(5000)

        # Close Popup If Present
        try:

            page.click(
                'svg[data-title="cross"]'
            )

            print("Popup Closed")

        except:

            print("No Popup Found")

        # Search All Roles
        for role in JOB_ROLES:

            print(f"\nSearching Jobs For: {role}")

            # Open Search Page
            page.goto(
                f"https://www.naukri.com/{role.replace(' ', '-')}-jobs"
            )

            # Wait For Page Load
            page.wait_for_timeout(5000)

            # Extract Job Cards
            jobs = page.query_selector_all(
                "div.srp-jobtuple-wrapper"
            )

            print(f"Total Jobs Found: {len(jobs)}")

            # Check First 3 Jobs
            for job in jobs[:3]:

                try:

                    # Extract Elements
                    title_element = job.query_selector(
                        "a.title"
                    )

                    company_element = job.query_selector(
                        "a.comp-name"
                    )

                    experience_element = job.query_selector(
                        "span.expwdth"
                    )

                    # Skip Missing Title
                    if not title_element:

                        print("Title Missing")

                        continue

                    # Skip Missing Company
                    if not company_element:

                        print("Company Missing")

                        continue

                    # Extract Text
                    title = title_element.inner_text()

                    company = company_element.inner_text()

                    experience = (
                        experience_element.inner_text()
                        if experience_element
                        else "Not Mentioned"
                    )

                    print("\n----------------")
                    print("Job Title:", title)
                    print("Company:", company)
                    print("Experience:", experience)

                    # Get Job Link
                    job_link = title_element.get_attribute(
                        "href"
                    )

                    # Skip Missing Link
                    if not job_link:

                        print("Job Link Missing")

                        continue

                    # Skip Already Applied
                    if job_link in applied_jobs:

                        print("Already Applied")

                        continue

                    print("Opening Job...")

                    # Open New Job Tab
                    job_page = browser.new_page()

                    # Open Job Page Safely
                    job_page.goto(

                        job_link,

                        wait_until="domcontentloaded",

                        timeout=60000
                    )

                    # Wait For Page
                    job_page.wait_for_timeout(3000)

                    # Apply Job
                    try:

                        apply_button = job_page.query_selector(
                            'button:has-text("Apply")'
                        )

                        if apply_button:

                            # Wait Until Page Loads
                            job_page.wait_for_load_state(
                                "domcontentloaded"
                            )

                            # Click Apply
                            apply_button.click()

                            # Wait After Apply
                            job_page.wait_for_timeout(3000)

                            print(
                                f"Applied Successfully: {title} ✅"
                            )

                            # Save Applied Job
                            applied_jobs.add(job_link)

                            # Increase Counter
                            total_applied += 1

                            # Save History
                            job_data = {

                                "title": title,

                                "company": company,

                                "role": role,

                                "time": datetime.now().strftime(
                                    "%d-%m-%Y %H:%M:%S"
                                )
                            }

                            # Read Existing History
                            try:

                                with open(
                                    "backend/history.json",
                                    "r"
                                ) as file:

                                    history = json.load(file)

                            except:

                                history = []

                            # Add New Job
                            history.append(job_data)

                            # Save Updated History
                            with open(
                                "backend/history.json",
                                "w"
                            ) as file:

                                json.dump(
                                    history,
                                    file,
                                    indent=4
                                )

                        else:

                            print("Apply Button Not Found")

                    except Exception as e:

                        print("Apply Error:", e)

                    # Close Job Tab
                    try:

                        job_page.close()

                    except:
                        pass

                except Exception as e:

                    print("Job Processing Error:", e)

        # Close Main Page
        try:

            page.close()

        except:
            pass

        # Close Browser
        try:

            browser.close()

        except:
            pass

    # Return API Response
    return {

        "status": "success",

        "total_applied": total_applied
    }