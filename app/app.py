from google import genai
import os

# -----------------------------
# CONNECT TO GEMINI
# -----------------------------

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("API key not found!")
    exit()

client = genai.Client(
    api_key=api_key,
    http_options={"timeout": 30000}
)

chat = client.chats.create(
    model="gemini-2.5-flash"
)

# -----------------------------
# BCA SUBJECTS
# -----------------------------

subjects = [
    "Programming",
    "Data Structures",
    "Database Management",
    "Operating Systems",
    "Computer Networks",
    "Java",
    "Python",
    "Web Development",
    "Software Engineering",
    "Artificial Intelligence",
    "Machine Learning",
    "Data Science",
    "Cybersecurity",
    "Cloud Computing"
]

# -----------------------------
# FUNCTIONS
# -----------------------------

def show_subjects():
    print("\n========== BCA SUBJECTS ==========\n")

    for i, subject in enumerate(subjects, 1):
        print(f"{i}. {subject}")

    print()


def ask_ai():
    print("\n========== AI STUDY ASSISTANT ==========")
    print("Ask any BCA question.")
    print("Type 'back' to return to menu.\n")

    while True:

        question = input("You: ")

        if question.lower() == "back":
            break

        if not question.strip():
            continue

        prompt = f"""
You are a friendly BCA Study Assistant.

Student question:
{question}

Give the answer in simple language.

Include:
1. Definition
2. Explanation
3. Example
4. Important points
5. Code example if relevant

Make the answer useful for a BCA student.
"""

        try:
            print("\nAssistant is thinking...\n")

            response = chat.send_message(prompt)

            print("Assistant:")
            print(response.text)
            print()

        except Exception as e:
            print("Error:", e)


def study_subject():
    show_subjects()

    choice = input("Choose a subject number: ")

    try:
        number = int(choice)

        if number < 1 or number > len(subjects):
            print("Invalid choice.")
            return

        subject = subjects[number - 1]

        print(f"\n📚 Selected: {subject}")
        print("Ask me anything about this subject.")
        print("Type 'back' to return.\n")

        while True:

            question = input(f"{subject}: ")

            if question.lower() == "back":
                break

            prompt = f"""
You are a BCA Study Assistant.

Subject: {subject}

Student question:
{question}

Explain clearly for a BCA student.

Give:
- Definition
- Simple explanation
- Example
- Important points
- Code/example if useful
"""

            try:
                response = chat.send_message(prompt)

                print("\nAssistant:")
                print(response.text)
                print()

            except Exception as e:
                print("Error:", e)

    except ValueError:
        print("Please enter a number.")


def quiz():

    print("\n========== BCA QUIZ ==========\n")

    show_subjects()

    choice = input("Choose subject number: ")

    try:
        number = int(choice)

        if number < 1 or number > len(subjects):
            print("Invalid choice.")
            return

        subject = subjects[number - 1]

        print(f"\nQuiz Topic: {subject}")
        print("You will get 5 questions.")
        print("Answer with A, B, C or D.\n")

        score = 0

        for i in range(1, 6):

            prompt = f"""
Create ONE multiple-choice question about {subject}
for a BCA student.

Return EXACTLY in this format:

QUESTION:
<question>

A. <option>
B. <option>
C. <option>
D. <option>

ANSWER:
<correct letter>

EXPLANATION:
<short explanation>
"""

            response = chat.send_message(prompt)

            text = response.text

            print(f"\nQuestion {i}")
            print(text)

            answer = input("\nYour answer: ").upper().strip()

            if f"ANSWER:\n{answer}" in text:
                print("✅ Correct!")
                score += 1
            else:
                print("❌ Incorrect.")

        print("\n========== QUIZ RESULT ==========")
        print(f"Your score: {score}/5")

        if score == 5:
            print("🏆 Excellent!")
        elif score >= 3:
            print("👏 Good job!")
        else:
            print("📚 Keep studying and try again!")

    except ValueError:
        print("Please enter a number.")


# -----------------------------
# MAIN PROGRAM
# -----------------------------

print("==========================================")
print("       BCA AI STUDY ASSISTANT")
print("==========================================")

name = input("\nWhat is your name? ")

print(f"\nHello {name}! 👋")
print("Your personal BCA AI Study Assistant is ready!")

while True:

    print("\n========== MAIN MENU ==========")
    print("1. 📚 Study a Subject")
    print("2. 🤖 Ask AI Anything")
    print("3. 📝 Take a Quiz")
    print("4. 📖 View Subjects")
    print("5. 🚪 Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        study_subject()

    elif choice == "2":
        ask_ai()

    elif choice == "3":
        quiz()

    elif choice == "4":
        show_subjects()

    elif choice == "5":
        print(f"\nGoodbye {name}! Keep learning! 🚀")
        break

    else:
        print("Please choose 1, 2, 3, 4 or 5.")