from core.UsraWise.configuration import llm
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate



TEMPLATE = """

*** Problem ***:

Parents often struggle to effectively support their children’s education due to a lack of personalized guidance, relevant resources, and understanding of their child’s unique learning needs.
This gap can lead to missed opportunities for academic and personal growth, particularly for children with diverse learning styles and educational challenges.
Parents may be overwhelmed by the complexity of tailoring support and accessing relevant information.

*** Data Collection ***

We will gather the following data to tailor our guidance effectively:

- **Child Data**:
    - Age: {age}
    - Grade Level: {grade_level}
    - Gender: {gender}
    - Learning Style: {learning_style}
    - Hobbies: {hobbies}

- **Parent's Information**:
    - Education Level: {education_level}
    - Occupation: {occupation}
    - Parenting Style: {parenting_style}

- **Child's Academic Information**:
    - Overall Performance Level: {overall_performance_level}
    - Standardized Test Scores: {standardized_test_scores}
    - Behavioral Challenges (if any): {behavioral_challenges}

*** Idea ***

Develop "Usra Wise," a comprehensive AI-driven platform designed to empower parents with personalized guidance, tools, and resources to support their children’s educational journey.
"Usra Wise" will deliver tailored learning plans, provide access to curated educational resources, and offer real-time feedback.

The platform will include:

- **Personalized Learning Resources**: Diagnostic assessments, customized learning plans, supplementary materials, study skills workshops, and regular progress monitoring tools.
- **Tailored Parenting Advice**: Strategies for creating consistent routines, encouraging a growth mindset, providing emotional support, engaging with teachers, and setting realistic goals.
- **Communication Tools**: Templates for effective communication with educators and tools for tracking academic progress.


*** Objective ***

Our objective is to develop a generative AI solution that delivers personalized, data-driven guidance to empower parents in supporting their child's educational journey.

The AI will:

- Provide tailored learning plans and resource recommendations.
- Offer real-time feedback based on continuous monitoring of the child's progress.
- Integrate diagnostic assessments, customized learning plans, supplementary materials, study skills workshops, and progress tracking tools.
- Include communication templates and tools for effective interaction with educators.

By combining these elements, "Usra Wise" will bridge the gap between parents and their children’s learning needs, ensuring comprehensive support for both academic and personal growth.

### Note

The platform should offer clear explanations for all recommendations and present the final output in a user-friendly format, such as a personalized action plan.

### I want the output in this format {response_json}
"""


##############################################################################################################################################

generation_prompt = PromptTemplate(
    input_variables=[
        "age",
        "grade_level",
        "gender",
        "learning_style",
        "hobbies",
        "education_level",
        "occupation",
        "parenting_style",
        "overall_performance_level",
        "standardized_test_scores",
        "behavioral_challenges",
    ],
    template=TEMPLATE,
)

#################################################################################################################################################



generation_chain = LLMChain(llm=llm, prompt=generation_prompt, output_key="response", verbose=True)