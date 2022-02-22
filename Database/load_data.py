import pandas as pd
#from tqdm import tqdm

from Database.database import db
from tables.professors import Professors
from tables.projects import Projects
from tables.users import Users


def return_none_if_nan(value):
    if pd.isna(value):
        return None

    return value


# Script runs with the assumption data loading has not occurred yet
# If the database is already populated, this script will fail
def load_data():

    professor_data='2020-2021 Professor Interests'

    profs = pd.read_excel(professor_data, sheetname=0, header=0, index_col=False, keep_default_na=True)

    profs.head()

    
    # Insert just course data, skipping prerequisites for now
    # to avoid issues with graph cycles
    print("Inserting courses...")
    for course, row in tqdm(df_processed.iterrows()):
        new_course = Course(
            code=course,
            name=row["Name"],
            level=row["Course Level"],
            division=row["Division"],
            department=row["Department"],
            description=return_none_if_nan(row["Course Description"]),
            campus=row["Campus"],
            utsc_breadth=return_none_if_nan(row["UTSC Breadth"]),
            as_breadth=return_none_if_nan(row["Arts and Science Breadth"]),
            as_distribution=return_none_if_nan(row["Arts and Science Distribution"]),
            apsc_electives=return_none_if_nan(row["APSC Electives"]),
            utm_distribution=return_none_if_nan(row["UTM Distribution"]),
            fase_available=row["FASEAvailable"],
            maybe_restricted=row["MaybeRestricted"],
        )
        db.session.add(new_course) 

        offerings = set(row["Term"])
        for term in offerings:
            new_offering = Offering(
                course=course,
                term=term,
            )
            db.session.add(new_offering)

        major_outcomes = set(row["MajorsOutcomes"])
        for major_outcome in major_outcomes:
            new_major_outcome = MajorOutcome(
                course=course,
                major=major_outcome,
            )
            db.session.add(new_major_outcome)  

        minor_outcomes = set(row["MinorsOutcomes"])
        for minor_outcome in minor_outcomes:
            new_minor_outcome = MinorOutcome(
                course=course,
                minor=minor_outcome,
            )
            db.session.add(new_minor_outcome)

        db.session.commit()

    # Process prerequisites after all courses inserted
    print("Inserting prerequisites...")
    for course, row in tqdm(df_processed.iterrows()):
        prerequisites = set(row["Pre-requisites"])
        for prerequisite in prerequisites:
            new_prerequisite = Prerequisite(
                course=course,
                prereq=prerequisite,
            )
            db.session.add(new_prerequisite)

        corequisites = set(row["Corequisite"])
        for corequisite in corequisites:
            new_corequisite = Corequisite(
                course=course,
                coreq=corequisite,
            )
            db.session.add(new_corequisite)

        exclusions = set(row["Exclusion"])
        for exclusion in exclusions:
            new_exclusion = Exclusion(
                course=course,
                exclusion=exclusion,
            )
            db.session.add(new_exclusion)

        preparations = set(row["Recommended Preparation"])
        for preparation in preparations:
            new_preparation = Preparation(
                course=course,
                recommended_preparation=preparation,
            )
            db.session.add(new_preparation)

        smart_prerequisites = set(row["AIPreReqs"])
        for smart_prerequisite in smart_prerequisites:
            new_smart_prerequisite = SmartPrerequisite(
                course=course,
                prereq=smart_prerequisite,
            )
            db.session.add(new_smart_prerequisite)

        db.session.commit()