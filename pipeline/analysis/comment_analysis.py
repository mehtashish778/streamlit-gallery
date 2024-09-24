import csv
import os
import json
from promptify import Prompter, OpenAI, Pipeline

# Define constants
API_KEY = 'api_key'
os.environ["OPENAI_API_KEY"] = API_KEY

MODEL_NAME = 'gpt-3.5-turbo'
TEMPLATE_PATH = 'multilabel_classification.jinja'

# Define label constants
SENTIMENT_LABELS = ["positive", "negative", "neutral"]
ENGAGEMENT_INTENT_LABELS = ["opinion", "question", "complaint", "informative"]
ENGAGEMENT_INTENSITY_LABELS = ["low", "medium", "high"]



import json




def parse_output(output_str):
    # Replace single quotes with double quotes to make it valid JSON
    print(output_str)
    output_str = output_str.replace("'", '"')

    
    try:
        # Parse the string into a list of dictionaries
        parsed_data = json.loads(output_str)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e} for output: {output_str}")
        return []  # Return an empty list on error
    
    # Extract and return the required fields
    result = [
        {
            'sentiment': item['sentiment'],
            'engagement_intent': item['engagement_intent'],
            'engagement_intensity': item['engagement_intensity']
        } 
        for item in parsed_data
    ]
    
    return result


def comment_analysis(comments: dict) -> dict:
    csv_file = 'data/comment_analysis.csv'  # Updated path
    create_csv_if_not_exists(csv_file)
    
    results = {}
    for comment_id, comment in comments.items():
        cached_result = get_cached_analysis(csv_file, comment_id)
        if cached_result:
            results[comment_id] = cached_result
            print(f"Using cached result for comment {comment_id}")
        else:
            print(f"Generating new analysis for comment {comment_id}")
            analysis = get_analysis(comment)
            # Parse the analysis to extract sentiment, intent, and intensity
            sentiment = analysis['sentiment']
            
            if analysis['engagement_intent'] ==[]:
                engagement_intent = 'none'
            else:
                engagement_intent = analysis['engagement_intent'][0]



            engagement_intensity = analysis['engagement_intensity']
            results[comment_id] = {'sentiment': sentiment, 'engagement_intent': engagement_intent, 'engagement_intensity': engagement_intensity}
            save_analysis_to_csv(csv_file, comment_id, comment, sentiment, engagement_intent, engagement_intensity)
    
    return results

def create_csv_if_not_exists(filename: str):
    """Create CSV file with headers if it doesn't exist."""
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)  # Ensure the data directory exists
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['comment_id', 'comment', 'sentiment', 'engagement_intent', 'engagement_intensity'])

def get_cached_analysis(filename: str, comment_id: str):
    """Retrieve cached analysis from CSV file if it exists."""
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if str(row['comment_id']) == str(comment_id):
                    print(f"Found cached analysis for comment {comment_id}")
                    return {
                        'sentiment': row['sentiment'],
                        'engagement_intent': row['engagement_intent'],
                        'engagement_intensity': row['engagement_intensity']
                    }  # Return as a dictionary
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    print(f"No cached analysis found for comment {comment_id}")
    return None

def save_analysis_to_csv(filename: str, comment_id: str, comment: str, sentiment: str, engagement_intent: list, engagement_intensity: str):
    """Save analysis results to CSV file in the new format."""
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([comment_id, comment, sentiment, engagement_intent, engagement_intensity])
        print(f"Saved analysis for comment {comment_id} to CSV")
    except Exception as e:
        print(f"Error saving to CSV file: {e}")





def get_analysis(comment: str):
    """Analyze a single comment using the OpenAI model and promptify pipeline."""
    # Initialize OpenAI model
    model = OpenAI(api_key=API_KEY, model=MODEL_NAME)

    # Create prompter and pipeline
    prompter = Prompter(TEMPLATE_PATH)
    pipe = Pipeline(prompter, model)
    comment =  comment.replace("'", '')   #remove all the "'" and '"' and ","
    
    output = pipe.fit(
        text_input=[comment],
        sentiment_labels=SENTIMENT_LABELS,
        engagement_intent_labels=ENGAGEMENT_INTENT_LABELS,
        engagement_intensity_labels=ENGAGEMENT_INTENSITY_LABELS
    )

    # Check if output is valid
    if output and isinstance(output, list) and len(output) > 0 and 'text' in output[0]:
        print(parse_output(output[0]['text'])[0])
        print(parse_output(output[0]['text']))

        return parse_output(output[0]['text'])[0]
    else:
        print(f"Error in model execution: {output}")
        return None  # Return None if output is invalid





# # Example usage:
# output = "[{'comment': 'This product is amazing! I love it.', 'sentiment': 'positive', 'engagement_intent': ['opinion'], 'engagement_intensity': 'high'}]"
# parsed_result = parse_output(output)
# print(parsed_result)

# print(type(parsed_result))

# print(parsed_result[0]['sentiment'])



# if __name__ == "__main__":
#     # Test comments
#     test_comments = {
#         "1": "This product is amazing! I love it."
#     }

#     # Run analysis
#     results = comment_analysis(test_comments)

#     # Print results
#     for comment_id, analysis in results.items():
#         print(f"Comment ID: {comment_id}")
#         print(f"Comment: {test_comments[comment_id]}")
#         print(f"Analysis: {analysis}")
#         print("-" * 50)

#     # Check if CSV file was created and populated
#     csv_file = 'comment_analysis.csv'
#     if os.path.exists(csv_file):
#         print(f"\nCSV file '{csv_file}' created successfully.")
#         with open(csv_file, 'r') as f:
#             print("CSV contents:")
#             print(f.read())
#     else:
#         print(f"\nError: CSV file '{csv_file}' was not created.")

