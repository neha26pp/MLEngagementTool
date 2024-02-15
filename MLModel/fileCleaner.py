import csv
import os

# Specify the path to your CSV file
input_csv_file = "stimulus2.csv"

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Define the bounds for each column
column_bounds = {
    "start_of_record": {"min": 0, "max": float('inf')},
    "status": {"min": float('-inf'), "max": float('inf')},
    "overtime_count": {"min": 0, "max": float('inf')},
    "mark_value": {"min": float('-inf'), "max": float('inf')},
    "XDAT": {"min": float('-inf'), "max": float('inf')},
    "CU_video_field_num": {"min": float('-inf'), "max": float('inf')},
    "Gaze_LAOI": {"min": 0, "max": float('inf')},
    "LAOI_horz_gaze_coord": {"min": -1280, "max": 1280},
    "LAOI_vert_gaze_coord": {"min": -720, "max": 720},
    "left_pupil_pos_horz": {"min": 0, "max": 320},
    "right_pupil_pos_horz": {"min": 0, "max": 320},
    "left_pupil_pos_vert": {"min": 0, "max": 240},
    "right_pupil_pos_vert": {"min": 0, "max": 240},
    "left_pupil_diam": {"min": 0, "max": float('inf')},
    "right_pupil_diam": {"min": 0, "max": float('inf')},
    "left_pupil_height": {"min": 0, "max": float('inf')},
    "right_pupil_height": {"min": 0, "max": float('inf')},
    "left_ellipse_angle": {"min": -89.99, "max": 90},
    "right_ellipse_angle": {"min": -89.99, "max": 90},
    "left_eyelid_upper_vert": {"min": 0, "max": 239},
    "right_eyelid_upper_vert": {"min": 0, "max": 239},
    "left_eyelid_lower_vert": {"min": 0, "max": 239},
    "right_eyelid_lower_vert": {"min": 0, "max": 239},
    "left_blink_confidence": {"min": 0, "max": 100},
    "right_blink_confidence": {"min": 0, "max": 100},
    "left_cr_pos_horz": {"min": 0, "max": 320},
    "right_cr_pos_horz": {"min": 0, "max": 320},
    "left_cr_pos_vert": {"min": 0, "max": 240},
    "right_cr_pos_vert": {"min": 0, "max": 240},
    "left_cr_diam": {"min": 0, "max": float('inf')},
    "right_cr_diam": {"min": 0, "max": float('inf')},
    "left_cr2_pos_horz": {"min": 0, "max": 320},
    "right_cr2_pos_horz": {"min": 0, "max": 320},
    "left_cr2_pos_vert": {"min": 0, "max": 240},
    "right_cr2_pos_vert": {"min": 0, "max": 240},
    "left_cr2_diam": {"min": 0, "max": float('inf')},
    "right_cr2_diam": {"min": 0, "max": float('inf')},
    "horz_gaze_coord": {"min": -1280, "max": 1280},
    "vert_gaze_coord": {"min": -720, "max": 720},
    "horz_gaze_offset": {"min": float('-inf'), "max": float('inf')},
    "vert_gaze_offset": {"min": float('-inf'), "max": float('inf')},
    "vergence_angle": {"min": 0, "max": 360},
    "verg_gaze_coord_x": {"min": float('-inf'), "max": float('inf')},
    "verg_gaze_coord_y": {"min": float('-inf'), "max": float('inf')},
    "verg_gaze_coord_z": {"min": float('-inf'), "max": float('inf')},
    "left_eye_location_x": {"min": float('-inf'), "max": float('inf')},
    "right_eye_location_x": {"min": float('-inf'), "max": float('inf')},
    "left_eye_location_y": {"min": float('-inf'), "max": float('inf')},
    "right_eye_location_y": {"min": float('-inf'), "max": float('inf')},
    "left_eye_location_z": {"min": float('-inf'), "max": float('inf')},
    "right_eye_location_z": {"min": float('-inf'), "max": float('inf')},
    "left_gaze_dir_x": {"min": -1, "max": 1},
    "right_gaze_dir_x": {"min": -1, "max": 1},
    "left_gaze_dir_y": {"min": -1, "max": 1},
    "right_gaze_dir_y": {"min": -1, "max": 1},
    "left_gaze_dir_z": {"min": -1, "max": 1},
    "right_gaze_dir_z": {"min": -1, "max": 1},
}

exclude_columns = ["status"]
# Open the input CSV file
with open(input_csv_file, mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # Correctly read the header row

    # Prepare the output CSV file
    base_name = os.path.splitext(input_csv_file)[0]
    new_csv_file = f"{base_name}_cleaned.csv"

    with open(new_csv_file, mode='w', newline='') as new_file:
        writer = csv.writer(new_file)
        writer.writerow(header)  # Reiterate writing the header row to the new file

        failed_rows = []  # Use a list to keep track of failed row numbers for detailed reporting

        for i, row in enumerate(csv_reader, start=2):  # Enumeration starts at 2 due to header being the first row
            row_failed = False
            for index, value in enumerate(row):
                if index < len(header):  # Ensure index within header range
                    col_name = header[index]
                    if col_name in column_bounds and col_name not in exclude_columns:
                        # Proceed with bounds check if applicable
                        if not is_number(value) or not (column_bounds[col_name]["min"] <= float(value) <= column_bounds[col_name]["max"]):
                            failed_rows.append(i)  # Log failing row number
                            row_failed = True
                            break  # Stop checking further columns for this row

            if not row_failed:
                writer.writerow(row)  # Write to new file if row passes all checks

# After processing, report outcomes
if failed_rows:
    print(f"Rows that failed the checks: {sorted(set(failed_rows))}")
else:
    print("All rows passed the checks and were added to the new file.")