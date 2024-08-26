import json
from usra import generation_chain



def main():

    with open(r'C:\Users\OYaghi\Desktop\UsraWise_backend\myvenv\Scripts\project\core\UsraWise\response.json', 'r') as file:
        RESPONSE_JSON = json.load(file)

    
    
    
    # Create a GenerationChain object

    response = generation_chain(
{
    "age": 9,
    "grade_level": "4th",
    "gender": "Female",
    "learning_style": "Kinesthetic",
    "hobbies": ["Playing Piano", "Swimming"],
    "education_level": "High School Diploma",
    "occupation": "Teacher",
    "parenting_style": "Supportive",
    "overall_performance_level": "Average",
    "standardized_test_scores": {
        "Math": "70th percentile",
        "Reading": "65th percentile",
        "Science": "72nd percentile"
    },
    "behavioral_challenges": "Struggles with organization, occasionally disruptive in class, needs encouragement to participate",
    "response_json": json.dumps(RESPONSE_JSON)
})
    
    # Save the JSON data to an external file
    output_path = r'C:\Users\OYaghi\Desktop\UsraWise_backend\myvenv\Scripts\project\core\UsraWise\output.json'  # Change to your desired path

    output = json.loads(response['response'])

    with open(output_path, 'w') as file:
        json.dump(output, file, indent=4)

    print("JSON data has been saved to 'output.json'")


if __name__ == '__main__':
    main()