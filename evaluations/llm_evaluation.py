import os
import json
from datetime import datetime
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from text_anonymizer.core import anonymize, deanonymize

def get_llm_response(anthropic, text):
    prompt = f"{HUMAN_PROMPT} Please summarize the following text: {text}{AI_PROMPT}"
    response = anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=300,
        prompt=prompt
    )
    return response.completion.strip()

def evaluate_anonymization_effect():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Anthropic API key not set in environment variables")

    anthropic = Anthropic(api_key=api_key)
    
    original_text = "John Doe from Acme Corp in New York is working on a new project. His email is john.doe@acme.com."
    anonymized_text, anonymization_map = anonymize(original_text)
    
    original_response = get_llm_response(anthropic, original_text)
    anonymized_response = get_llm_response(anthropic, anonymized_text)
    deanonymized_response = deanonymize(anonymized_response, anonymization_map)
    
    evaluation_results = {
        "original_text": original_text,
        "anonymized_text": anonymized_text,
        "original_response": original_response,
        "anonymized_response": anonymized_response,
        "deanonymized_response": deanonymized_response,
        "key_info_preserved": all(
            info in deanonymized_response
            for info in ["John Doe", "Acme Corp", "New York"]
        ),
        "response_length_difference": abs(len(original_response) - len(deanonymized_response)),
    }
    
    return evaluation_results

def run_evaluation():
    try:
        results = evaluate_anonymization_effect()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"llm_evaluation_report_{timestamp}.json"
        
        with open(report_filename, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"Evaluation complete. Report saved to {report_filename}")
        print("\nSummary:")
        print(f"Key information preserved: {results['key_info_preserved']}")
        print(f"Response length difference: {results['response_length_difference']} characters")
    except Exception as e:
        print(f"Error during evaluation: {str(e)}")

if __name__ == "__main__":
    run_evaluation()
