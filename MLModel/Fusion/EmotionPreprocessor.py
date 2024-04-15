import os

def normalize_emotions(emotions_count, total_emotions):
    # Normalize each emotion count to a fraction of the total count of emotions, avoiding division by zero
    normalized_emotions = {emotion: (count / total_emotions if total_emotions > 0 else 0) for emotion, count in emotions_count.items()}
    return list(normalized_emotions.values())

def EmotionPreprocess(base_path):
    # This will be a 2D array to hold the normalized emotions from each set
    all_normalized_emotions = []

    # Define the emotions dictionary template
    emotions_template = {
        'surprise': 0.9,
        'angry': 0.8,
        'neutral': 0.7,
        'sad': 0.6,
        'happy': 0.4,
        'disgust': 0.2,
        'fearf': 0.1
    }

    if not os.path.isdir(base_path):
        print(f"Error: {base_path} is not a directory")
        return all_normalized_emotions
    
    for subdir in os.listdir(base_path):
        subdir_path = os.path.join(base_path, subdir)
        if os.path.isdir(subdir_path):
            for file in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, file)
                if file_path.endswith('.txt'):
                    try:
                        with open(file_path, 'r') as f:
                            # Reset emotions_count for each file
                            emotions_count = emotions_template.copy()
                            total_emotions = 0
                            
                            content = f.read()
                            emotions = content.replace('\n', ' ').split()
                            for emotion in emotions:
                                if emotion.lower() in emotions_count:
                                    emotions_count[emotion.lower()] += 1
                                    total_emotions += 1
                            
                            # Normalize the emotions for this file and add to the 2D array
                            normalized_emotions_array = normalize_emotions(emotions_count, total_emotions)
                            all_normalized_emotions.append(normalized_emotions_array)
                    except IOError as e:
                        print(f"Could not read file {file_path}: {e}")

    return all_normalized_emotions
