import os
import json
from datetime import datetime
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from text_anonymizer.core import anonymize, deanonymize

def get_llm_response(anthropic, prompt):
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
    
    original_text = """
    From: Sarah Johnson <sarah.johnson@techinnovate.com>
    To: Michael Chen <michael.chen@globex.com>
    Subject: Proposal for AI-driven Supply Chain Optimization

    Dear Michael,

    I hope this email finds you well. I'm reaching out to discuss an exciting opportunity for Globex Corporation to revolutionize its supply chain management using cutting-edge AI technology.

    Our team at TechInnovate Solutions has developed a state-of-the-art AI system that can significantly improve inventory forecasting, reduce logistics costs, and optimize warehouse operations. We believe this solution could save Globex up to 15% in annual supply chain expenses.

    Key benefits of our AI-driven system include:
    1. Real-time demand forecasting with 95% accuracy
    2. Automated inventory replenishment
    3. Dynamic route optimization for deliveries
    4. Predictive maintenance for warehouse equipment

    I'd love to schedule a meeting to discuss this further. Are you available next Tuesday at 2 PM EST for a video call? If not, please suggest a time that works better for you.

    Looking forward to potentially working together to transform Globex's supply chain operations.

    Best regards,
    Sarah Johnson
    Senior Solutions Architect
    TechInnovate Solutions
    Phone: +1 (555) 123-4567
    """

    anonymized_text, anonymization_map = anonymize(original_text)
    
    # Summarization task
    summary_prompt = f"{HUMAN_PROMPT} Please summarize the following text in 3-4 sentences: {original_text}{AI_PROMPT}"
    original_summary = get_llm_response(anthropic, summary_prompt)

    anonymized_summary_prompt = f"{HUMAN_PROMPT} Please summarize the following text in 3-4 sentences: {anonymized_text}{AI_PROMPT}"
    anonymized_summary = get_llm_response(anthropic, anonymized_summary_prompt)
    deanonymized_summary = deanonymize(anonymized_summary, anonymization_map)

    # Information retrieval task
    retrieval_questions = [
        "Who is the sender of the email?",
        "What company does the sender work for?",
        "Who is the recipient of the email?",
        "What company does the recipient work for?",
        "What is the main purpose of the email?",
        "What are the key benefits of the AI-driven system mentioned in the email?",
        "What is the proposed meeting time?",
    ]

    original_answers = []
    anonymized_answers = []

    for question in retrieval_questions:
        original_prompt = f"{HUMAN_PROMPT} Based on the following text, please answer this question: {question}\n\nText: {original_text}{AI_PROMPT}"
        original_answers.append(get_llm_response(anthropic, original_prompt))

        anonymized_prompt = f"{HUMAN_PROMPT} Based on the following text, please answer this question: {question}\n\nText: {anonymized_text}{AI_PROMPT}"
        anonymized_answers.append(get_llm_response(anthropic, anonymized_prompt))

    deanonymized_answers = [deanonymize(answer, anonymization_map) for answer in anonymized_answers]

    evaluation_results = {
        "original_text": original_text,
        "anonymized_text": anonymized_text,
        "original_summary": original_summary,
        "anonymized_summary": anonymized_summary,
        "deanonymized_summary": deanonymized_summary,
        "retrieval_questions": retrieval_questions,
        "original_answers": original_answers,
        "anonymized_answers": anonymized_answers,
        "deanonymized_answers": deanonymized_answers,
        "summary_length_difference": abs(len(original_summary) - len(deanonymized_summary)),
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
        print(f"Summary length difference: {results['summary_length_difference']} characters")
        print("\nRetrieval Quality Assessment:")
        for i, question in enumerate(results['retrieval_questions']):
            print(f"\nQuestion: {question}")
            print(f"Original Answer: {results['original_answers'][i]}")
            print(f"Deanonymized Answer: {results['deanonymized_answers'][i]}")
    except Exception as e:
        print(f"Error during evaluation: {str(e)}")

if __name__ == "__main__":
    run_evaluation()
