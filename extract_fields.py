import torch
import os
import json
from transformers import T5Tokenizer, T5ForConditionalGeneration, AutoModelForSequenceClassification, AutoTokenizer
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", message="overflowing tokens are not returned for the setting you have chosen")

# Load pre-trained T5 model and tokenizer for QA
qa_tokenizer = T5Tokenizer.from_pretrained('t5-large')
qa_model = T5ForConditionalGeneration.from_pretrained('t5-large')

# Load pre-trained NLI model and tokenizer
nli_tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-mnli')
nli_model = AutoModelForSequenceClassification.from_pretrained('facebook/bart-large-mnli')

def load_text_file(file_path):
    # Load the content of a text file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def load_question_bank(file_path):
    # Load the question bank from a json file
    with open(file_path, 'r', encoding='utf-8') as file:
        question_bank = json.load(file)
    return question_bank

def save_question_bank(file_path, question_bank):
    # Save the question bank to a json file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(question_bank, file, indent=4, ensure_ascii=False)

def answer_question(question, context):
    # Generate an answer to a question based on the given context using a pre-trained T5 model
    input_text = f"question: {question} context: {context}"
    inputs = qa_tokenizer(input_text, return_tensors='pt', max_length=4096, truncation=True)
    with torch.no_grad():
        outputs = qa_model.generate(inputs['input_ids'], max_length=4096, num_beams=4, early_stopping=True)

    answer = qa_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

def validate_response(question, context, response):
    # Validate the response using NLI model
    nli_input = nli_tokenizer.encode_plus(context, response, return_tensors='pt', truncation=True)
    with torch.no_grad():
        logits = nli_model(**nli_input).logits
    probabilities = torch.softmax(logits, dim=-1)
    entailment_prob = probabilities[0][2].item()  # Entailment score
    return entailment_prob

def main():
    # Static file paths (Change accordingly)
    question_bank_path = r"./output.json"

    txtfilelist = []

    for root, dirs, filenames in os.walk(os.getcwd()):
        for f in filenames:
            if f.startswith("extracted_output"):
                txtfilelist.append(os.path.join(root, f))

    print(txtfilelist)

    # Load question bank
    question_bank = load_question_bank(question_bank_path)
    print("- qn bank loaded -")

    for question_data in question_bank:
        question_data['answer'] = []

    for i in range(0, len(txtfilelist), 1):
        
        context_path = r"%s" %txtfilelist[i]
        
        
        # Load context content
        context = load_text_file(context_path)
        print("- text file loaded -")

        # Extract only the file name from the context_path
        context_file_name = os.path.basename(context_path)
        
        # Update the file_location in question_bank with context_file_name
        for question_data in question_bank:
            question_data['file_location'] = context_file_name
            

        # Generate answers for all questions in the question bank based on the context
        for question_data in question_bank:

            # Skip updating if update is set to false
            if not question_data.get('update', True):
                continue

            question = question_data.get('question')
            answer = answer_question(question, context)
            entailment_prob = validate_response(question, context, answer)
            if entailment_prob > 0.5:
                if answer not in question_data["answer"]:
                    question_data["answer"].append(answer)
            else:
                print("-- ans validation failed --")
            print("- qn answered -")

        # Save the updated question bank
        save_question_bank(question_bank_path, question_bank)
        print("- qn and ans saved to json -")
        return True
    
if __name__ == "__main__":
    main()




# ========= NOTES =========
# main() --> main(txtfile)
# question_bank_path and context_path changed to path strings
## user input not necessary 
# perform os.walk()
    # for f in files:
    #     if f.startswith("pdf_output") and f.endswith(".txt"):
    #         main(f)