import requests
import pandas as pd
from tqdm import tqdm

COUNTRY_URL = "https://sweetgum.nybg.org/science/api/v1/countries"
INSTITUTIONS_URL = "https://sweetgum.nybg.org/science/api/v1/institutions/search"
COLUMNS = [
    "irn",
    "organization",
    "code",
    "division",
    "department",
    "cites",
    "specimenTotal",
    "currentStatus",
    "dateFounded",
    "taxonomicCoverage",
    "geography",
    "address_physicalStreet",
    "address_physicalCity",
    "address_physicalState",
    "address_physicalZipCode",
    "address_physicalCountry",
    "address_postalStreet",
    "address_postalCity",
    "address_postalState",
    "address_postalZipCode",
    "address_postalCountry",
    "contact_phone",
    "contact_email",
    "contact_webUrl",
    "location_lat",
    "location_lon",
    "collectionsSummary_numAlgae",
    "collectionsSummary_numAlgaeDatabased",
    "collectionsSummary_numAlgaeImaged",
    "collectionsSummary_numBryos",
    "collectionsSummary_numBryosDatabased",
    "collectionsSummary_numBryosImaged",
    "collectionsSummary_numFungi",
    "collectionsSummary_numFungiDatabased",
    "collectionsSummary_numFungiImaged",
    "collectionsSummary_numPteridos",
    "collectionsSummary_numPteridosDatabased",
    "collectionsSummary_numPteridosImaged",
    "collectionsSummary_numSeedPl",
    "collectionsSummary_numSeedPlDatabased",
    "collectionsSummary_numSeedPlImaged",
    "incorporatedHerbaria",
    "importantCollectors",
    "notes",
    "dateModified",
]


def get_countries():
    return requests.get(COUNTRY_URL).json()["data"]


def get_institutions(country):
    params = {"country": country}
    return requests.get(INSTITUTIONS_URL, params).json()["data"]


def flatten_institution(d, parent_key="", sep="_"):
    items = [
        (
            f"{parent_key}{sep}{k}" if parent_key else k,
            ";".join(v) if isinstance(v, list) else v,
        )
        for k, v in d.items()
    ]
    return {
        k: v
        for item in items
        for k, v in (
            flatten_institution(item[1], item[0], sep=sep).items()
            if isinstance(item[1], dict)
            else [item]
        )
    }


def main():
    rows_list = []

    for country in tqdm(get_countries(), ascii=True):
        data = get_institutions(country)

        for item in data:
            row = flatten_institution(item)
            rows_list.append(row)

    df = pd.DataFrame(rows_list, columns=COLUMNS)
    df.to_excel("ih_output.xlsx", index=False)


if __name__ == "__main__":
    main()
