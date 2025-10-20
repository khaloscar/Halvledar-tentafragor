import random
import os
from pathlib import Path

class Question:
    def __init__(self, prompt, answer, suggestions, explanation="", image_ref=""):
        self.prompt = prompt
        self.answer = answer.strip()
        self.suggestions = [s.strip() for s in suggestions]
        self.explanation = explanation.strip()
        self.image_ref = image_ref.strip()

    def print_question(self):
        print(self.prompt)
        for idx, s in enumerate(self.suggestions, 1):
            print(f"{idx}: {s}")

    def ask_and_check(self):
        # Randomize answer order
        random.shuffle(self.suggestions)

        self.print_question()
        num_options = len(self.suggestions)

        # Ask user
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

        # Show explanation + image link
        if self.explanation:
            print(f"💡 Explanation: {self.explanation}")

        if self.image_ref:
            link_text = clickable("CTRL + Click to view image", self.image_ref)
            print(f"🖼️  {link_text}")       # clickable words
            # optional: also print the raw path/URL as a fallback
            # print(os.path.abspath(self.image_ref))

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
                image_ref = lines[4] if len(lines) >= 5 else ""
                questions.append(Question(prompt, answer, suggestions, explanation, image_ref))
    return questions

def clickable(label: str, ref: str) -> str:
    """
    Make OSC-8 hyperlink for VS Code terminal.
    Accepts http(s) URLs or local file paths. Returns clickable label text.
    """
    esc = "\x1b"
    # If it's not already a URL, convert local path -> file URI
    if not (ref.startswith("http://") or ref.startswith("https://") or ref.startswith("file://")):
        p = Path(ref).expanduser().resolve()
        # as_uri() percent-encodes spaces and uses forward slashes
        ref = p.as_uri()   # e.g., file:///G:/Random%20stuff/.../NVM_schematic.png

    return f"{esc}]8;;{ref}{esc}\\{label}{esc}]8;;{esc}\\"

def main():
    questions = load_questions_from_file("questions.txt")
    random.shuffle(questions)

    score = 0
    for q in questions:
        if q.ask_and_check():
            score += 1

    total = len(questions)
    pct = (score / total * 100) if total else 0
    print(f"You got {score}/{total} correct ({pct:.0f}%).")


if __name__ == "__main__":
    main()