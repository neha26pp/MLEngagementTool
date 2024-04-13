import pandas as pd
from datetime import datetime
from Scripts.database import add_to_sessions
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
files = [
        'C:\\Users\\NEHA\\Downloads\\MLEngagementTool\\Scripts\\QualtricsDownload\\Post Survey_Engagement Project - Text - Topic 1.csv',
        'C:\\Users\\NEHA\\Downloads\\MLEngagementTool\\Scripts\\QualtricsDownload\\Post Survey_Engagement Project - Text - Topic 2.csv',
        'C:\\Users\\NEHA\\Downloads\\MLEngagementTool\\Scripts\\QualtricsDownload\\Post Survey_Engagement Project - Video - Topic 1.csv',
        'C:\\Users\\NEHA\\Downloads\\MLEngagementTool\\Scripts\\QualtricsDownload\\Post Survey_Engagement Project - Video - Topic 2.csv'
    ]
# Function to shorten the stimulus name
def shorten_stimulus_name(stimulus):
    parts = stimulus.split(' - ')
    if len(parts) > 3:
        return f"{parts[2]} {parts[3]}"
    return stimulus  # Return original if the expected format is not met

# Function to process files and update the database
def process_files():
    all_data = {}

    # Process each file
    for file in files:
        stimulus = file.split("\\")[-1].split('.')[0]  # Extract filename without extension
        if("text" in stimulus.lower() and "topic 1" in stimulus.lower()):
            stimulus = "Topic 1 Text"
        if("text" in stimulus.lower() and "topic 2" in stimulus.lower()):
            stimulus = "Topic 1 Text"
        if("video" in stimulus.lower() and "topic 1" in stimulus.lower()):
            stimulus = "Topic 1 Video"
        if("video" in stimulus.lower() and "topic 2" in stimulus.lower()):
            stimulus = "Topic 2 Video"
        # Load the CSV file
        df = pd.read_csv(file, usecols=[0, 17, 18])

        for row in df.itertuples(index=False):
            start_date_str, first_name, last_name = row
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                continue

            # Filtering criteria
            if any(keyword in str(first_name).lower() or keyword in str(last_name).lower()
                   for keyword in ['test', 'hello', 'why']) or len(str(first_name)) == 1 or is_float(first_name) or is_float(last_name):
                continue

            # Create a full name key
            full_name = f"{first_name} {last_name}".strip()

            if full_name not in all_data:
                all_data[full_name] = []

            all_data[full_name].append((start_date, stimulus))

    # Sort the stimuli for each person by date and assign to stimulus1 and stimulus2
    for name, data in all_data.items():
        data.sort(key=lambda x: x[0])  # Sort by datetime
        stimuli = [entry[1] for entry in data]  # Extract the stimuli
        stimulus1 = stimuli[0] if len(stimuli) > 0 else " "
        stimulus2 = stimuli[1] if len(stimuli) > 1 else " "
        print(name, stimulus1, stimulus2)
        add_to_sessions(name, stimulus1, stimulus2)

# Run the processing function
# process_files()
