import argparse
import pandas as pd
from tcia_utils import nbia




COLLECTION = "Duke-Breast-Cancer-MRI"
TARGET_DESC = "ax dyn 1st pass"

def get_target_series():

    all_series = nbia.getSeries(collection= COLLECTION, format = "df")

    if all_series is None or len(all_series) == 0:
        raise SystemExit("No series returned. check your internet connection")
    

    desc_col = "SeriesDescription" if "SeriesDescription" in all_series.columns else None

    if desc_col is None:
        SystemExit("Could not find SeriesDescription column in returned data. check your internet connection")

    
    mask = all_series[desc_col].str.strip().str.lower()  == TARGET_DESC.lower()

    target = all_series[mask].copy()

    all_patients  = all_series["PatientID"].unique()
    target_patients = target["PatientID"].unique()

    missing = set(all_patients) - set(target_patients)

    if missing:

        print(f"Warning: {len(missing)} patients are missing from the target series. This may be due to differences in SeriesDescription formatting. Missing patients: {missing}")

    return target




def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("--inspect", action="store_true", help="Inspect the target series and exit")

    ap.add_argument("--download", action="store_true", help="Download the target series")

    ap.add_argument("--path", default="duke_nri_raw", help="Path to save downloaded data")


    args = ap.parse_args()

    target = get_target_series()

    target.to_csv("duke_1st_pass_series.csv", index=False)


    if args.download:
        
        nbia.downloadSeries(target, input_type="df", path=args.path, max_workers=4)
        print("\ndownload complete")

    
    else:
        est_gb = len(target) * 0.062

        print(f"Estimated download size: {est_gb:.2f} GB")
        print("Use --download to download the target series")



if __name__ == "__main__":
    main()