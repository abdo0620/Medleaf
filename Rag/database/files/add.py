import requests, json
import os
from path import Path 
PARENT_DIR=Path(__file__).parent 
total_saved = 0
os.makedirs(PARENT_DIR / "drug_json_files", exist_ok=True)
os.makedirs(PARENT_DIR / "drug_text_files", exist_ok=True)




url = f"https://api.fda.gov/drug/label.json?search=openfda.product_type:HUMAN+PRESCRIPTION+DRUG&limit=1000&skip=0"
r = requests.get(url)
results = r.json().get("results", [])
if r.status_code != 200:
    raise Exception(f"FDA API returned status {r.status_code}")



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
        spl_text         = drug.get("spl_product_data_elements", [""])[0]


        if any([indications, warnings, dosage, adverse, description]):

            header = f"""DRUG NAME: {brand_name}
GENERIC NAME: {generic_name}
MANUFACTURER: {manufacturer}
ROUTE: {route}"""
 
            sections = [
                ("ACTIVE INGREDIENT", active_ingr),
                ("INACTIVE INGREDIENTS", inactive_ingr),
                ("DESCRIPTION", description),
                ("CLINICAL PHARMACOLOGY", clinical_pharm),
                ("MECHANISM OF ACTION", mechanism),
                ("INDICATIONS AND USAGE", indications),
                ("CONTRAINDICATIONS", contraindic),
                ("BOXED WARNING", boxed_warning),
                ("WARNINGS", warnings),
                ("DO NOT USE", do_not_use),
                ("ASK A DOCTOR BEFORE USE", ask_doctor),
                ("PRECAUTIONS", precautions),
                ("DOSAGE AND ADMINISTRATION", dosage),
                ("ADVERSE REACTIONS", adverse),
                ("DRUG INTERACTIONS", interactions),
                ("USE IN PREGNANCY", pregnancy),
                ("NURSING MOTHERS", nursing),
                ("PEDIATRIC USE", pediatric),
                ("GERIATRIC USE", geriatric),
                ("OVERDOSAGE", overdosage),
                ("STOP USE IF", stop_use),
                ("CLINICAL STUDIES", clinical_studies),
                ("STORAGE AND HANDLING", storage),
                ("SPL TEXT", spl_text),
            ]
 
            # Only keep sections that actually have content (non-empty after stripping)
            body_parts = [
                f"{label}:\n{value.strip()}"
                for label, value in sections
                if value and value.strip()
            ]
 
            text = header + "\n\n" + "\n\n".join(body_parts)
            text = text.strip()
 
        

        meta_data=dict()

        safe_name = brand_name.replace(" ", "_").replace("/", "_")[:50]
        safe_spl=spl_text.replace(" ", "_").replace("/", "_")[:200]
        filename = PARENT_DIR / "drug_text_files" / f"drug_{total_saved:04d}_{safe_name}.txt"
        filename_json = PARENT_DIR / "drug_json_files" / f"drug_{total_saved:04d}_{safe_name}.json"
        meta_json=open(filename_json,"w")


        with open(filename, "w", encoding="utf-8",) as f:
                f.write(text)
        meta_data["safe_name"]=safe_name
        meta_data["safe_spl"]=safe_spl
        jsmeta=json.dumps(meta_data,indent=2)
        meta_json.write(jsmeta)
        total_saved += 1
        meta_json.close()


print("Done! Total saved:", total_saved)