import csv

def invert_negative_question_score(score):
    """Inverts the score for a negative question."""
    try:
        return str(10 - int(score))
    except ValueError:
        return score  # Returns the original score if conversion fails

def calculate_quiz_score(quiz_responses, correct_answers):
    """Calculates the quiz score based on correct responses."""
    quiz_score = 0
    for response, correct_answer in zip(quiz_responses, correct_answers):
        if response == correct_answer:
            quiz_score += 10  # Assuming a perfect score for each correct answer
    return quiz_score

def calculate_engagement_percentage(responses, negative_indices, quiz_responses, correct_answers):
    """Calculates the engagement score as a percentage, considering both interest and quiz responses."""
    total_score = calculate_quiz_score(quiz_responses, correct_answers)
    for i, response in enumerate(responses):
        if i in negative_indices:
            response = invert_negative_question_score(response)
        try:
            total_score += int(response)
        except ValueError:
            pass  # Ignores the score if it's not an integer
    # Total possible score is adjusted to include quiz questions
    total_possible_score = (len(responses) + len(quiz_responses)) * 10
    # Calculate percentage
    engagement_percentage = (total_score / total_possible_score) * 100
    return engagement_percentage

def read_and_calculate_engagement_percentages(csv_file_path):
    correct_answers = ['2', '3', '2', '3', '', '1', '1', '1']  # Correct answers for the quiz
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            first_name = row[17]  # Adjusting for zero-based indexing
            last_name = row[18]
            responses = row[19:54]  # Includes responses to the interest questions
            quiz_responses = row[55:62]  # Adjust for zero-based indexing and includes quiz responses
            # Indices of negative questions, adjusted for zero-based index and offset in responses slice
            negative_indices = [i - 20 for i in range(26, 32)] + [i - 20 for i in range(50, 52)]
            engagement_percentage = calculate_engagement_percentage(responses, negative_indices, quiz_responses, correct_answers)
            print(f"Student: {first_name} {last_name}, Engagement Percentage: {engagement_percentage:.2f}%")

# Replace 'path/to/your/survey_data.csv' with the actual path to your CSV file
print("TOPIC 1 TEXT\n")
topic1_text_path = 'topic 1 text.csv'
read_and_calculate_engagement_percentages(topic1_text_path)
print("\nTOPIC 1 VIDEO\n")
topic1_video_path = 'topic 1 video.csv'
read_and_calculate_engagement_percentages(topic1_video_path)


