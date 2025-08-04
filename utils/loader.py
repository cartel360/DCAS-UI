import pandas as pd

def process_uploaded_files(profile_file, aguser_file, msg_code_file=None):
    # Read required CSVs
    profile_df = pd.read_csv(profile_file)
    aguser_df = pd.read_csv(aguser_file)

    dropped_rows = {}

    # Standardize column names
    aguser_df = aguser_df.rename(columns={
        'farmer_id': 'FarmerId',
        'planting_date': 'plantingDate',
        'growth_stage': 'growthStage',
        'message': 'message_1',
        'message_2': 'message_2',
        'message_3': 'message_3',
    })

    profile_df = profile_df.rename(columns={
        'farmer_id': 'FarmerId',
        'farmer_name': 'FarmerName',
        'farmer_mobile_number': 'FarmerMobileNumber',
        'county': 'County',
        'subcounty': 'Subcounty',
        'ward': 'Ward',
        'gender': 'Gender',
        'FinalLatitude': 'FinalLatitude',
        'Finallongitude': 'FinalLongitude'
    })

    # Drop AG user rows with missing FarmerId or all messages
    dropped_rows["AG User missing ID or message"] = aguser_df[
        aguser_df[['FarmerId', 'message_1', 'message_2', 'message_3']].isnull().all(axis=1) |
        aguser_df['FarmerId'].isnull()
    ]
    aguser_df = aguser_df.drop(dropped_rows["AG User missing ID or message"].index)

    # Drop Farmer profile rows with missing ID
    dropped_rows["Farmer Profile missing ID"] = profile_df[profile_df['FarmerId'].isnull()]
    profile_df = profile_df.dropna(subset=['FarmerId'])

    # Merge AG user with profile
    merged = pd.merge(aguser_df, profile_df, on='FarmerId', how='left')

    # Drop merged rows with critical missing fields
    key_cols = ['FarmerId', 'FarmerName', 'FarmerMobileNumber']
    dropped_rows["Final merged missing key profile fields"] = merged[
        merged[key_cols].isnull().any(axis=1)
    ]
    merged = merged.dropna(subset=key_cols)

    # If message code file provided, merge message translations
    if msg_code_file:
        try:
            msg_df = pd.read_csv(msg_code_file)
            msg_df = msg_df.drop_duplicates(subset='JUNE2024CODE')
            msg_df = msg_df[['JUNE2024CODE', 'Messages (English)']]

            for i in range(1, 4):
                merged = merged.merge(
                    msg_df,
                    left_on=f'message_{i}',
                    right_on='JUNE2024CODE',
                    how='left'
                ).rename(
                    columns={'Messages (English)': f'Message {i} (English)'}
                ).drop(columns=['JUNE2024CODE'])

        except Exception as e:
            print(f"Failed to read/merge message codes: {e}")

    return merged, dropped_rows
