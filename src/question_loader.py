import os

class Question:
    def __init__(self, text, answer1_text, answer2_text, correct_answer_id):
        self.text = text
        self.answer1_text = answer1_text
        self.answer2_text = answer2_text
        self.correct_answer_id = correct_answer_id

    def __repr__(self):
        return (f"Question(text='{self.text}', "
                f"A1='{self.answer1_text}', "
                f"A2='{self.answer2_text}', "
                f"Correct='{self.correct_answer_id}')")

class QuestionLoader:
    def __init__(self):
        self.questions = []

    def load_questions(self, file_path):
        self.questions.clear()  # Clear previous questions

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: Question file not found at {file_path}")
            return False
        except IOError as e:
            print(f"Error: Could not read question file {file_path}. IOError: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred while opening/reading {file_path}: {e}")
            return False

        question_blocks = content.strip().split('---')
        
        for i, block in enumerate(question_blocks):
            block = block.strip()
            if not block:
                continue

            lines = block.split('\n')
            
            parsed_data = {}
            expected_prefixes = {
                "Q": "Q: ",
                "A1": "A1: ",
                "A2": "A2: ",
                "Correct": "Correct: "
            }

            for line in lines:
                line = line.strip()
                if line.startswith(expected_prefixes["Q"]):
                    parsed_data["text"] = line[len(expected_prefixes["Q"]):].strip()
                elif line.startswith(expected_prefixes["A1"]):
                    parsed_data["answer1_text"] = line[len(expected_prefixes["A1"]):].strip()
                elif line.startswith(expected_prefixes["A2"]):
                    parsed_data["answer2_text"] = line[len(expected_prefixes["A2"]):].strip()
                elif line.startswith(expected_prefixes["Correct"]):
                    parsed_data["correct_answer_id"] = line[len(expected_prefixes["Correct"]):].strip()
            
            # Validate required fields
            required_fields = ["text", "answer1_text", "answer2_text", "correct_answer_id"]
            all_fields_present = True
            for field in required_fields:
                if field not in parsed_data or not parsed_data[field]: # Check if field exists and is not empty
                    all_fields_present = False
                    break
            
            if all_fields_present:
                if parsed_data["correct_answer_id"] not in ["A1", "A2"]:
                    print(f"Warning: Malformed question block #{i+1} in {file_path}. Invalid Correct ID: '{parsed_data['correct_answer_id']}'. Skipping.")
                    continue

                question = Question(
                    text=parsed_data["text"],
                    answer1_text=parsed_data["answer1_text"],
                    answer2_text=parsed_data["answer2_text"],
                    correct_answer_id=parsed_data["correct_answer_id"]
                )
                self.questions.append(question)
            else:
                print(f"Warning: Malformed question block #{i+1} in {file_path}. Missing one or more parts. Skipping.")
                # print(f"Block content:\n{block}\nParsed data: {parsed_data}") # For debugging

        return True

    def get_question(self, index):
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None

    def get_total_questions(self):
        return len(self.questions)

if __name__ == '__main__':
    # This assumes the script is run from the project root (e.g., /app)
    # or that assets/questions/questions.txt is in a path relative to where the script is run.
    # For consistent testing, construct path from script's directory if needed,
    # but for now, direct relative path is used as per typical project structure.
    
    questions_file_path = os.path.join("assets", "questions", "questions.txt")
    
    # Verify the file exists before attempting to load
    if not os.path.exists(questions_file_path):
        print(f"Test Error: The question file was not found at the expected path: {os.path.abspath(questions_file_path)}")
        print("Make sure 'assets/questions/questions.txt' exists and is populated.")
        # Attempt to create a dummy file if it's missing, for basic loader testing
        # This is more for CI/testing environments than typical use.
        print("Attempting to create a dummy questions.txt for basic test continuity...")
        dummy_content = """Q: What is 1+1?
A1: 2
A2: 3
Correct: A1
---
Q: Is Python a snake?
A1: Yes
A2: No
Correct: A1
---
"""
        try:
            os.makedirs(os.path.dirname(questions_file_path), exist_ok=True)
            with open(questions_file_path, 'w', encoding='utf-8') as f_dummy:
                f_dummy.write(dummy_content)
            print(f"Dummy file created at {questions_file_path}")
        except Exception as e:
            print(f"Failed to create dummy file: {e}")
            # Exit if file cannot be found or created for test
            exit(1)


    loader = QuestionLoader()
    success = loader.load_questions(questions_file_path)

    if success:
        print(f"\nSuccessfully loaded {loader.get_total_questions()} questions:")
        for i in range(loader.get_total_questions()):
            q = loader.get_question(i)
            print(f"  {i+1}: {q}")
        
        if loader.get_total_questions() == 0:
            print("Warning: No questions were loaded. Check file content and format.")

    else:
        print("\nFailed to load questions.")

    print("\nTesting with a malformed block (should be skipped with a warning):")
    # Create a temporary malformed file for testing this specific case
    malformed_file_path = "assets/questions/temp_malformed_questions.txt"
    malformed_content = """Q: Correct Question?
A1: Yes
A2: No
Correct: A1
---
Q: Missing Answer 2
A1: Option 1
Correct: A1
---
Q: Invalid Correct ID
A1: Foo
A2: Bar
Correct: A3
"""
    try:
        with open(malformed_file_path, 'w', encoding='utf-8') as f_malformed:
            f_malformed.write(malformed_content)
        
        malformed_loader = QuestionLoader()
        malformed_loader.load_questions(malformed_file_path)
        print(f"Loaded {malformed_loader.get_total_questions()} questions from malformed file (expected 1).")
        for q in malformed_loader.questions:
            print(q)
        
        if os.path.exists(malformed_file_path):
            os.remove(malformed_file_path)

    except Exception as e:
        print(f"Error during malformed file test: {e}")

    print("\nQuestionLoader test finished.")
