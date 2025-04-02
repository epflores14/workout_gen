import random
import csv
import matplotlib.pyplot as plt
import pandas as pd

def get_exercises(body_part_1, body_part_2, exercises, fitness_level):
    # Fetch exercises for the selected body parts
    #brackets added so code doesn't break if body part not found. 
    selected_exercises = exercises.get(body_part_1.lower(), []) + exercises.get(body_part_2.lower(), [])
    
    # Define rep and set ranges based on fitness level
    fitness_levels = {
        "beginner": {"reps": 10, "sets": 2},
        "intermediate": {"reps": 15, "sets": 3},
        "advanced": {"reps": 20, "sets": 3}
    }
    
    workout_plan = []
    
    if fitness_level in fitness_levels:
        level = fitness_levels[fitness_level]
        for exercise in selected_exercises:
            workout_plan.append(f"{exercise}: {level['reps']} reps, {level['sets']} sets")
    
    return workout_plan

def save_workout_to_csv(workout_data, filename="workout_history.csv"):
    """Saves workout session to CSV file"""
    try:
        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)

            # Write header if the file is empty
            if file.tell() == 0:
                writer.writerow(["Body Part 1", "Body Part 2", "Exercises", "Fitness Level", "Workout Location"])

            writer.writerow([workout_data["body_part_1"], workout_data["body_part_2"],
                             ", ".join(workout_data["exercises"]), workout_data["fitness_level"], workout_data["location"]])

        print("\nWorkout plan saved to CSV successfully!")
    
    except Exception as e:
        print(f"Error saving workout to CSV: {e}")

def random_branch(branches):
    return random.choice(branches)

def add_exercise(exercises):
    # Ask the user if they want to add an exercise
    add_exercise_choice = input("\nDo you want to add a custom exercise? (yes/no): ").strip().lower()
    
    if add_exercise_choice == "yes":
        body_part = input("Enter the body part this exercise targets: ").strip().lower()
        exercise_name = input("Enter the name of the exercise: ").strip()
        
        if body_part in exercises:
            exercises[body_part].append(exercise_name)
        else:
            exercises[body_part] = [exercise_name]
        
        print(f"Exercise '{exercise_name}' added to '{body_part}' successfully!")
    else:
        print("No exercise added.")

    return exercises

def manage_branches(branches):
    print("\nManage Branch List:")
    print("1. Add a branch.")
    print("2. Remove a branch.")
    print("3. View branches.")
    choice = input("Choose an option (1/2/3): ").strip()
    
    if choice == "1":
        new_branch = input("Enter the name of the branch you want to add: ").strip()
        branches.append(new_branch)
        print(f"Branch '{new_branch}' added successfully!")
    elif choice == "2":
        branch_to_remove = input("Enter the name of the branch you want to remove: ").strip()
        if branch_to_remove in branches:
            branches.remove(branch_to_remove)
            print(f"Branch '{branch_to_remove}' removed successfully!")
        else:
            print("Branch not found!")
    elif choice == "3":
        print("\nCurrent branch list:")
        for branch in branches:
            print("-", branch)
    else:
        print("Invalid choice!")
    return branches

def track_exercise_frequency(filename="workout_history.csv"):
    """Reads workout history and counts how often each body part is exercised."""
    try:
        # Load CSV file
        df = pd.read_csv(filename)

        # Count occurrences of each body part
        body_part_counts = {}
        for index, row in df.iterrows():
            body_parts = [row["Body Part 1"], row["Body Part 2"]]
            for part in body_parts:
                if part in body_part_counts:
                    body_part_counts[part] += 1
                else:
                    body_part_counts[part] = 1
        
        return body_part_counts
    except Exception as e:
        print(f"Error reading workout history: {e}")
        return {}

def visualize_exercise_frequency(body_part_counts):
    """Plots exercise frequency in a bar chart."""
    if body_part_counts:
        plt.figure(figsize=(8, 6))
        plt.bar(body_part_counts.keys(), body_part_counts.values(), color="skyblue")
        
        plt.xlabel("Body Parts")
        plt.ylabel("Workout Count")
        plt.title("Monthly Workout Frequency")
        plt.xticks(rotation=45)
        
        plt.show()
    else:
        print("No exercise data available for visualization.")

# Main program
exercises = {
    "arms": ["Bicep Curls", "Tricep Dips", "Push-Ups"],
    "legs": ["Squats", "Lunges", "Deadlifts"],
    "back": ["Pull-Ups", "Bent-Over Rows", "Lat Pulldowns"],
    "chest": ["Bench Press", "Push-Ups", "Chest Fly"],
    "shoulders": ["Shoulder Press", "Lateral Raises", "Front Raises"],
    "abs": ["Crunches", "Plank", "Russian Twists"]
}

branches = ["Otis", "Pedro Gil", "Ermita", "SM Manila", "Las Pinas", "Vito Cruz"]

print("Welcome to your personalized fitness program!")

branch = random_branch(branches)
print(f"\nToday's workout location: Anytime Fitness - {branch}")

branches = manage_branches(branches)
exercises = add_exercise(exercises)

body_part_1 = input("\nEnter the first body part you want to exercise today: ").strip()
body_part_2 = input("Enter the second body part you want to exercise today: ").strip()

fitness_level = input("\nEnter your fitness level (beginner/intermediate/advanced): ").strip().lower()

exercise_list = get_exercises(body_part_1, body_part_2, exercises, fitness_level)
if exercise_list:
    print(f"\nHere are your exercises for {body_part_1} and {body_part_2} at {branch}:")
    for exercise in exercise_list:
        print("-", exercise)
    
    # Save workout to CSV
    workout_data = {
        "body_part_1": body_part_1,
        "body_part_2": body_part_2,
        "exercises": exercise_list,
        "fitness_level": fitness_level,
        "location": branch
    }
    save_workout_to_csv(workout_data)
else:
    print("\nSorry, I don't have exercises listed for those body parts.")

# After saving workouts, generate the visualization
body_part_counts = track_exercise_frequency()
visualize_exercise_frequency(body_part_counts)