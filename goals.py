import mysql.connector
from datetime import date

# Function to establish database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="finance_db"
    )

# Function to add a new financial goal
def add_goal(user_id, goal_name, target_amount, deadline):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Check if the goal already exists for the user
        check_query = "SELECT COUNT(*) FROM goals WHERE user_id = %s AND goal_name = %s"
        cursor.execute(check_query, (user_id,goal_name))
        (goal_exists,)=cursor.fetchone()
        if goal_exists > 0:
            print(f"‼️ Goal '{goal_name}' already exists! Duplicate goals are not allowed.")
        else:
            #insert new goal if it is unique or new
            query="""
            INSERT INTO goals (user_id, goal_name, target_amount, deadline)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, goal_name, target_amount, deadline))
            conn.commit()

            print(f"✅ Goal Added: {goal_name} | Target: ₹{target_amount} | Deadline: {deadline}")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to view all goals
def view_goals(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        query="SELECT id, goal_name, target_amount, saved_amount, deadline FROM goals WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        goals = cursor.fetchall()
        if not goals:
            print("❌ No Financial Goals Found!")
        else:
            print("\n 🎯 Your Financial Goals:")
            for goal in goals:
                goal_id, goal_name, target_amount, saved_amount, deadline = goal
                progress = (saved_amount / target_amount) * 100 if target_amount > 0 else 0
                print(f"🆔 {goal_id} | {goal_name} | 💰 Saved: ₹{saved_amount}/₹{target_amount} | 📅 Target: {deadline} | 📊Progress {progress:.2f}")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to update saved amount for a goal
def update_goal_progress(goal_id, amount):
    conn=get_db_connection()
    try:
        cursor=conn.cursor()

        query = "UPDATE goals SET saved_amount = saved_amount + %s WHERE id = %s"
        cursor.execute(query,(amount, goal_id))
        conn.commit()
        print(f"✅ Goal Process Updated! Added ₹{amount} to Goal ID: {goal_id}")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

#Function to delete a Goal
def delete_goal(goal_id):
    conn=get_db_connection()
    try:
        cursor=conn.cursor()

        query = "DELETE FROM goals WHERE id =  %s"
        cursor.execute(query, (goal_id,))
        conn.commit()
        print(f"❌ Goal ID {goal_id} Deleted Successfully!")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

#Example usage
if __name__=="__main__":
    user_id = 1   # Replace with dynamic user input

    add_goal(user_id, "Buy a Car", 500000, "2026-12-02")
    add_goal(user_id,"Australia Trip",200000, "2027-12-02")

    view_goals(user_id)

    update_goal_progress(1,20000)

    delete_goal(0) #replace id with your desired goal id to delete it

    view_goals(user_id)


