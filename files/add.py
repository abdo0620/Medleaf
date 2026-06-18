import requests, os

os.makedirs("leaflets", exist_ok=True)
total_saved = 0

for skip in range(0,1):
    url = f"https://api.fda.gov/drug/label.json?search=openfda.product_type:HUMAN+PRESCRIPTION+DRUG&limit=1000&skip={skip}"
    r = requests.get(url)
    results = r.json().get("results", [])

    if not results:
        break

    for drug in results:
        brand_name   = drug.get("openfda", {}).get("brand_name", ["Unknown"])[0]
        generic_name = drug.get("openfda", {}).get("generic_name", [""])[0]
        manufacturer = drug.get("openfda", {}).get("manufacturer_name", [""])[0]
        route        = drug.get("openfda", {}).get("route", [""])[0]

        description      = drug.get("description", [""])[0]
        mechanism        = drug.get("mechanism_of_action", [""])[0]
        indications      = drug.get("indications_and_usage", [""])[0]
        contraindic      = drug.get("contraindications", [""])[0]
        warnings         = drug.get("warnings", [""])[0]
        boxed_warning    = drug.get("boxed_warning", [""])[0]
        precautions      = drug.get("precautions", [""])[0]
        dosage           = drug.get("dosage_and_administration", [""])[0]
        adverse          = drug.get("adverse_reactions", [""])[0]
        interactions     = drug.get("drug_interactions", [""])[0]
        pregnancy        = drug.get("pregnancy", [""])[0]
        nursing          = drug.get("nursing_mothers", [""])[0]
        pediatric        = drug.get("pediatric_use", [""])[0]
        geriatric        = drug.get("geriatric_use", [""])[0]
        overdosage       = drug.get("overdosage", [""])[0]
        storage          = drug.get("storage_and_handling", [""])[0]
        clinical_pharm   = drug.get("clinical_pharmacology", [""])[0]
        clinical_studies = drug.get("clinical_studies", [""])[0]
        active_ingr      = drug.get("active_ingredient", [""])[0]
        inactive_ingr    = drug.get("inactive_ingredient", [""])[0]
        stop_use         = drug.get("stop_use", [""])[0]
        do_not_use       = drug.get("do_not_use", [""])[0]
        ask_doctor       = drug.get("ask_doctor", [""])[0]

        if any([indications, warnings, dosage, adverse, description]):

            text = f"""
DRUG NAME: {brand_name}
GENERIC NAME: {generic_name}
MANUFACTURER: {manufacturer}
ROUTE: {route}

ACTIVE INGREDIENT:
{active_ingr}

INACTIVE INGREDIENTS:
{inactive_ingr}

DESCRIPTION:
{description}

CLINICAL PHARMACOLOGY:
{clinical_pharm}

MECHANISM OF ACTION:
{mechanism}

INDICATIONS AND USAGE:
{indications}

CONTRAINDICATIONS:
{contraindic}

BOXED WARNING:
{boxed_warning}

WARNINGS:
{warnings}

DO NOT USE:
{do_not_use}

ASK A DOCTOR BEFORE USE:
{ask_doctor}

PRECAUTIONS:
{precautions}

DOSAGE AND ADMINISTRATION:
{dosage}

ADVERSE REACTIONS:
{adverse}

DRUG INTERACTIONS:
{interactions}

USE IN PREGNANCY:
{pregnancy}

NURSING MOTHERS:
{nursing}

PEDIATRIC USE:
{pediatric}

GERIATRIC USE:
{geriatric}

OVERDOSAGE:
{overdosage}

STOP USE IF:
{stop_use}

CLINICAL STUDIES:
{clinical_studies}

STORAGE AND HANDLING:
{storage}
""".strip()

            safe_name = brand_name.replace(" ", "_").replace("/", "_")[:50]
            filename = f"files/drug_text_files/drug_{total_saved:04d}_{safe_name}.txt"

            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)

            total_saved += 1

    print(f"Saved {total_saved} drugs so far...")

print("Done! Total saved:", total_saved)