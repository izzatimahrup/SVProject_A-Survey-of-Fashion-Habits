# --- Load Data ---
@st.cache_data
def load_data():
    # Load your actual file here! 
    # If it's an Excel file, use pd.read_excel()
    try:
        data = pd.read_csv("https://raw.githubusercontent.com/izzatimahrup/SVProject_A-Survey-of-Fashion-Habits/refs/heads/main/Cleaned_FashionHabitGF%20(1).csv") 
        return data
    except FileNotFoundError:
        st.error("Data file not found. Please ensure the CSV is in the same folder as your script.")
        return None

# Now we call the function to define df globally
df = load_data()

# Only proceed if df was loaded successfully
if df is not None:
    # Define motivation questions
    motivation_questions = [
        'follow_for_updates_promotions',
        'follow_because_like_products',
        'follow_because_entertaining',
        'follow_because_discounts_contests',
        'follow_because_express_personality',
        'follow_because_online_community',
        'follow_because_support_loyalty'
    ]
    
    # ... (Rest of your Tab and Plotting code goes here) ...
