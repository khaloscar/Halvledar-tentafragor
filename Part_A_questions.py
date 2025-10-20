import random

class Question:
    def __init__(self, prompt, answer, suggestions, explanation=""):
        self.prompt = prompt
        self.answer = answer.strip()
        self.suggestions = [s.strip() for s in suggestions]
        self.explanation = explanation.strip()

    def print_question(self):
        print(self.prompt)
        for idx, s in enumerate(self.suggestions, 1):
            print(f"{idx}: {s}")

    def ask_and_check(self):
        # Shuffle the order of the suggestions for this question
        random.shuffle(self.suggestions)

        self.print_question()
        num_options = len(self.suggestions)

        # Ask user for numeric answer
        while True:
            user_input = input(f"Choose 1-{num_options}: ").strip()
            if user_input.isdigit():
                choice = int(user_input)
                if 1 <= choice <= num_options:
                    break
            print(f"Please enter a number between 1 and {num_options}.")

        picked = self.suggestions[choice - 1]
        correct = picked.lower() == self.answer.lower()

        if correct:
            print("✅ Correct!")
        else:
            print(f"❌ Wrong! The correct answer was: {self.answer}")

        if self.explanation:
            print(f"💡 Explanation: {self.explanation}\n")
        else:
            print()

        return correct


def load_questions_from_file(filename):
    questions = []
    with open(filename, "r", encoding="utf-8") as f:
        blocks = f.read().strip().split("\n\n")
        for block in blocks:
            lines = [ln.strip() for ln in block.strip().split("\n") if ln.strip()]
            if len(lines) >= 3:
                prompt = lines[0]
                answer = lines[1]
                suggestions = [s.strip() for s in lines[2].split(",")]
                explanation = lines[3] if len(lines) >= 4 else ""
                questions.append(Question(prompt, answer, suggestions, explanation))
    return questions


def main():
    questions = load_questions_from_file("questions.txt")
    random.shuffle(questions)  # Randomize question order

    score = 0
    for q in questions:
        if q.ask_and_check():
            score += 1

    print(f"You got {score}/{len(questions)} correct.")


if __name__ == "__main__":
    main()