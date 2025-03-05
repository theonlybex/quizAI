import openai
import json
from openai import OpenAI
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Set up your OpenAI API key
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key = ""
)
# Function to generate the quiz
def generate_quiz():
    material = text_input.get("1.0", tk.END).strip()
    num_questions = int(num_questions_var.get())
    question_type = question_type_var.get()

    if not material:
        messagebox.showwarning("Input Error", "Please provide the material for the quiz.")
        return

    messages = [
        {"role": "system", "content": "You are a helpful assistant that generates quizzes."},
        {"role": "user", "content": f"""
            Based on the following material, create a quiz with {num_questions} {question_type} questions:

            Material:
            {material}

            Format the output as follows:
            Q1. [Question]
                a. [Option 1]
                b. [Option 2]
                c. [Option 3]
                d. [Option 4]
            Answer: [Correct Option]
        """}
        
    ]
    

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=700  # Adjust as needed
        )

        
        # Check the structure step-by-step
        result = response #print the responce
        quiz_output.delete("1.0", tk.END)
        quiz_output.insert(tk.END, result)
    except Exception as e:
        messagebox.showerror("API Error", f"An error occurred: {e}")

# Function to save the quiz to a file
def save_quiz():
    quiz_content = quiz_output.get("1.0", tk.END).strip()
    if not quiz_content:
        messagebox.showwarning("Save Error", "No quiz content to save!")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(quiz_content)
        messagebox.showinfo("Save Successful", f"Quiz saved to {file_path}")

# Set up the main Tkinter window
root = tk.Tk()
root.title("Quiz Generator")
root.geometry("600x500")
root.configure(bg="#f9f9f9")  # Light background color for minimalism

# Light blue theme styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5, background="#81D4FA", foreground="black")
style.configure("TLabel", font=("Arial", 12), background="#E0F7FA", foreground="black")
style.configure("TEntry", font=("Arial", 12))
style.configure("TCombobox", font=("Arial", 12))

# Input Frame for Material and Parameters
input_frame = tk.Frame(root, bg="#E0F7FA")
input_frame.pack(pady=20, padx=20, fill="x")

# Input Frame for Material and Parameters
input_frame = tk.Frame(root, bg="#f9f9f9")
input_frame.pack(pady=20, padx=20, fill="x")

# Material Input
ttk.Label(input_frame, text="Material for Quiz:").grid(row=0, column=0, sticky="w", pady=5)
text_input = tk.Text(input_frame, height=5, width=50, wrap="word", font=("Arial", 11))
text_input.grid(row=1, column=0, columnspan=2, pady=5, padx=5)

# Parameters for Quiz
params_frame = tk.Frame(input_frame, bg="#f9f9f9")
params_frame.grid(row=2, column=0, columnspan=2, pady=10)

ttk.Label(params_frame, text="Number of Questions:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
num_questions_var = tk.StringVar(value="5")
num_questions_entry = ttk.Entry(params_frame, textvariable=num_questions_var, width=5)
num_questions_entry.grid(row=0, column=1, pady=5, padx=5)

ttk.Label(params_frame, text="Question Type:").grid(row=0, column=2, sticky="w", pady=5, padx=5)
question_type_var = tk.StringVar(value="multiple-choice")
question_type_menu = ttk.Combobox(params_frame, textvariable=question_type_var, values=["multiple-choice", "true/false"], width=15)
question_type_menu.grid(row=0, column=3, pady=5, padx=5)

# Buttons for Actions
action_frame = tk.Frame(root, bg="#f9f9f9")
action_frame.pack(pady=10)

generate_button = ttk.Button(action_frame, text="Generate Quiz", command=generate_quiz)
generate_button.grid(row=0, column=0, padx=10)

save_button = ttk.Button(action_frame, text="Save Quiz to File", command=save_quiz)
save_button.grid(row=0, column=1, padx=10)

# Output Area for Quiz
output_frame = tk.Frame(root, bg="#f9f9f9")
output_frame.pack(padx=20, pady=10, fill="both", expand=True)

ttk.Label(output_frame, text="Generated Quiz:").pack(anchor="w")
quiz_output = tk.Text(output_frame, height=10, wrap="word", font=("Arial", 11))
quiz_output.pack(fill="both", expand=True, padx=5, pady=5)

# Run the application
root.mainloop()
