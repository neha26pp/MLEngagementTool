def read_and_process_emotions(file_path):
    """
    Reads emotions from a text file and processes them to a weighted 1D array of size 100.
    Each line in the file represents one emotion for a single student.
    """
    # Define the weights for each emotion
    emotion_weights = {
        'surprise': 0.9,
        'angry': 0.8,
        'neutral': 0.7,
        'sad': 0.6,
        'happy': 0.4,
        'disgust': 0.2,
        'fear': 0.1
    }

    # Read the emotions from the text file, one emotion per line
    with open(file_path, 'r') as file:
        emotions = file.read().splitlines()
    
    # Count each emotion
    emotion_counts = {emotion: emotions.count(emotion) for emotion in set(emotions)}
    total_emotions = sum(emotion_counts.values())
    
    # Normalize counts to sum up to 100 and apply weights
    normalized_weighted_counts = []
    for emotion, count in emotion_counts.items():
        normalized_count = round((count / total_emotions) * 100)
        weight = emotion_weights.get(emotion, 0)
        for _ in range(normalized_count):
            normalized_weighted_counts.append(weight)
    
    print(len(normalized_weighted_counts))
    return normalized_weighted_counts

# Process emotions for students
student_file_paths = ["emotions.txt"]  # Add paths to student files
all_students_features = [read_and_process_emotions(file_path) for file_path in student_file_paths]
# Now, `all_students_features` contains a 1D array of size 100 for each student, representing their weighted emotions
