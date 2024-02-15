import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

#start_of_record,status,overtime_count,mark_value,XDAT,CU_video_field_num,Gaze_LAOI,LAOI_horz_gaze_coord,LAOI_vert_gaze_coord,left_pupil_pos_horz,right_pupil_pos_horz,left_pupil_pos_vert,right_pupil_pos_vert,left_pupil_diam,right_pupil_diam,left_pupil_height,right_pupil_height,left_ellipse_angle,right_ellipse_angle,left_eyelid_upper_vert,right_eyelid_upper_vert,left_eyelid_lower_vert,right_eyelid_lower_vert,left_blink_confidence,right_blink_confidence,left_cr_pos_horz,right_cr_pos_horz,left_cr_pos_vert,right_cr_pos_vert,left_cr_diam,right_cr_diam,left_cr2_pos_horz,right_cr2_pos_horz,left_cr2_pos_vert,right_cr2_pos_vert,left_cr2_diam,right_cr2_diam,horz_gaze_coord,vert_gaze_coord,horz_gaze_offset,vert_gaze_offset,vergence_angle,verg_gaze_coord_x,verg_gaze_coord_y,verg_gaze_coord_z,left_eye_location_x,right_eye_location_x,left_eye_location_y,right_eye_location_y,left_eye_location_z,right_eye_location_z,left_gaze_dir_x,right_gaze_dir_x,left_gaze_dir_y,right_gaze_dir_y,left_gaze_dir_z,right_gaze_dir_z

#skip 2 rows
dataset = pd.read_csv("Stimulus1.csv", skiprows=2)
#place in a 2d array
with open('Stimulus1.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))
#remove first 2 rows
data = data[2:]
#convert to numpy array
data = np.array(data)
#remove first column
data = data[:,1:]
#remove last 3 columns
data = data[:,:-3]
#convert to dataframe
df = pd.DataFrame(data)
#remove first column
df = df.drop(df.columns[0], axis=1)
#convert to numpy array
data = df.to_numpy()
#convert to float
data = data.astype(float)
#split into input and output
X = data[:,:-1]
y = data[:,-1]
#scale input
scaler = StandardScaler()
X = scaler.fit_transform(X)
#fit the model
model = SVR()
model.fit(X, y)

