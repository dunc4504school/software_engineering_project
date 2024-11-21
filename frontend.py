import streamlit as st
import psycopg2
import pandas as pd
import sql_queries as sq

# Set page configuration
st.set_page_config(page_title="Movie System", page_icon="🎥")

# Initialize session state for page navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "welcome"

if "selected_movie_id" not in st.session_state:
    st.session_state["selected_movie_id"] = None


# Database connection function
def get_connection():
    return psycopg2.connect(
        host="localhost",       # Your database host
        database="cp317_final",    # Your database name
        user="heslip",       # Your database username
        password="pass123" # Your database password
    )

# Create connection and cursor for DB
conn = get_connection()
cur = conn.cursor()


# Welcome Page
def welcome_page():
    st.title("Welcome to Movie Recommendation System")
    st.subheader("Please choose an option to continue:")
    
    # Buttons for Signup and Login
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign Up"):
            st.session_state["current_page"] = "signup"
    with col2:
        if st.button("Login"):
            st.session_state["current_page"] = "login"


# Function to render the signup page
def signup_page():
    st.title("📝 Sign Up")
    
    # Collect user input
    name = st.text_input("Full Name")
    username = st.text_input("Username")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    
    if st.button("Create Account"):
        if not name or not username or not email or not phone or not password:
            st.error("Please fill out all fields.")
            return
        
        try:
             # Attempt to insert into the database
            cur.execute("INSERT INTO account (name, username, email, phone, password) VALUES (%s, %s, %s, %s, %s)", 
            (name, username, email, phone, password))
            conn.commit()

            # Check if the operation was successful
            if cur.rowcount > 0:
                st.success("Account created successfully! Redirecting to login...")
                st.session_state["current_page"] = "create_account"
                st.rerun()
            else:
                st.error("Failed to create account. Please try again.")
        
        finally:
            conn.close()


# Login verification function using attempt_login query
def verify_login(username, password):
    try:
        cur.execute(sq.attempt_login(), (username, password))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row is not None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False

# Streamlit Login Page
def login_page():
    st.title("Login Page")

    if st.button("⬅️ Back to Welcome Page"):
        st.session_state["current_page"] = "welcome"

    # User Input Fields
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Login")

    # Login Button Logic
    if login_button:
        if username and password:
            if verify_login(username, password):
                st.success("Login successful! Redirecting to homepage...")
                # Redirect to homepage
                st.session_state["current_page"] = "homepage"
            else:
                st.error("Invalid username or password. Please try again.")
        else:
            st.warning("Please enter both username and password.")



# Function to render the create account page
def create_account_page():
    st.title("🎬 Welcome to Movie Recommendation System!")
    st.subheader("Create Your Account")

    username = st.session_state.get("username", "User")
    email = st.session_state.get("email", "N/A")

    st.write(f"Hello, **{username}**!")
    st.write(f"We've recorded your email as **{email}**.")

    # Unique form key
    with st.form(key="profile_form_unique"):
        favorite_genre = st.selectbox("What's your favorite movie genre?", 
                                      ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance"])
        age = st.number_input("Your Age", min_value=10, max_value=100, step=1)
        agree_terms = st.checkbox("I agree to the terms and conditions.")
        submit_button = st.form_submit_button("Complete Registration")

    if submit_button:
        if not agree_terms:
            st.error("You must agree to the terms and conditions.")
        else:
            st.success("Account creation successful!")
            st.session_state["current_page"] = "homepage"

# Function to render the homepage
def homepage():
    # Add a title with an icon
    st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #4CAF50; font-size: 3rem;">🎉 Welcome to Your Homepage!</h1>
        <p style="font-size: 1.2rem; color: #555;">Navigate through our features and find what you're looking for.</p>
    </div>
    """, unsafe_allow_html=True)

    # Add an image banner
    st.image(
        "https://via.placeholder.com/800x200.png?text=Your+Movie+Recommendation+System",
        use_container_width=True,
        caption="Explore Reviews, Manage Your Account, Connect Socially, and Search for Movies!"
    )

    # Display the four options as buttons in a grid layout
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎥 Reviews", help="Check out reviews of movies and TV shows."):
            st.session_state["current_page"] = "reviews"
        if st.button("👤 Account", help="Manage your account settings and preferences."):
            st.session_state["current_page"] = "account"

    with col2:
        if st.button("🤝 Social", help="Connect with friends and see what they're watching."):
            st.session_state["current_page"] = "social"
        if st.button("🔍 Search", help="Search our library for movies and TV shows."):
            st.session_state["current_page"] = "search"

    # Footer message
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;">
        <p style="color: #888;">© 2024 Movie Recommendation System. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

def reviews_page():
    if st.button("⬅️ Back to Homepage"):
        st.session_state["current_page"] = "homepage"

    st.title("🎥 Reviews")
    st.subheader("Explore Movie and TV Show Reviews")
    st.write("Here, you can browse through reviews or add your own.")
    
    # Placeholder for reviews
    st.text_area("Write your review here...", placeholder="What did you think about the movie?")
    st.button("Submit Review")
    st.markdown("**Latest Reviews:**")
    st.write("🚀 Example Review: *This movie was fantastic!*")


def account_page():
    if st.button("⬅️ Back to Homepage"):
        st.session_state["current_page"] = "homepage"

    st.title("👤 Account")
    st.subheader("Manage Your Account Settings")
    st.write("Update your personal information, change your password, or view your account activity.")
    
    # Placeholder for account settings
    st.text_input("Username", value="User123", help="Update your username.")
    st.text_input("Email", value="user@example.com", help="Update your email address.")
    st.button("Save Changes")


def social_page():
    if st.button("⬅️ Back to Homepage"):
        st.session_state["current_page"] = "homepage"

    st.title("🤝 Social")
    st.subheader("Connect With Friends and Share Recommendations")
    st.write("See what your friends are watching or share your favorites with them.")
    
    # Placeholder for social features
    st.text_input("Search for friends", placeholder="Enter a friend's username...")
    st.button("Add Friend")
    st.markdown("**Friend Activity:**")
    st.write("🎬 *Alex just watched Inception!*")


def search_page():
    st.title("🔍 Search for Movies")

    if st.button("Back to Homepage"):
        st.session_state["current_page"] = "homepage"
        st.rerun()
    
    # Search bar
    query = st.text_input("Search Movies:")
    if query:
        movies = search_movies(query)
        if movies.empty:
            st.write("No results found.")
        else:
            # Loop through the DataFrame and display each movie in a styled card
            for _, row in movies.iterrows():
                # Display movie info as a styled card
                st.markdown(f"""
                <div style='
                    background: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                    margin-bottom: 20px;
                    padding: 20px;
                '>
                    <h3 style='color: #333;'>{row['Name']}</h3>
                    <p><b>Type:</b> {row['Type']}</p>
                    <p><b>Genre:</b> {row['Genres']}</p>
                    <p><b>Release Date:</b> {row['Release']}</p>
                </div>
                """, unsafe_allow_html=True)

                # Create a Streamlit button for viewing details
                if st.button(f"View Details for {row['Name']}"):
                    st.session_state["selected_movie_id"] = row["ID"]
                    st.session_state["current_page"] = "movie_profile"
                    st.rerun()

    # Global Recommendations Section
    st.subheader("🌍 Global Recommendations")
    # Placeholder for global recommendations (e.g., most popular movies globally)
    st.markdown("""
    <div style="
        background: #f1f1f1;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        padding: 20px;
    ">
        <h4 style='color: #333;'>Here are some movies recommended globally:</h4>
        <ul>
            <li><b>Movie 1</b> - Genre: Action, Rating: 9.0/10</li>
            <li><b>Movie 2</b> - Genre: Drama, Rating: 8.7/10</li>
            <li><b>Movie 3</b> - Genre: Comedy, Rating: 8.5/10</li>
            <li><b>Movie 4</b> - Genre: Thriller, Rating: 8.3/10</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Friends' Recommendations Section
    st.subheader("👫 Friends' Recommendations")
    # Placeholder for friends' recommendations (e.g., movies recommended by friends)
    st.markdown("""
    <div style="
        background: #f1f1f1;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        padding: 20px;
    ">
        <h4 style='color: #333;'>Here are some movies recommended by your friends:</h4>
        <ul>
            <li><b>Movie A</b> - Genre: Romance, Rating: 8.8/10</li>
            <li><b>Movie B</b> - Genre: Sci-Fi, Rating: 8.6/10</li>
            <li><b>Movie C</b> - Genre: Action, Rating: 8.4/10</li>
            <li><b>Movie D</b> - Genre: Horror, Rating: 8.2/10</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


def search_movies(query):
    sql = sq.search_movies_by_attributes()
    search_term = f"%{query.lower()}%"
    conn = get_connection()  # Ensure a valid DB connection
    cur = conn.cursor()
    cur.execute(sql, (search_term, search_term, search_term, search_term, search_term, search_term))
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    if not results:
        return pd.DataFrame()
    
    return pd.DataFrame(results, columns=["ID", "Name", "Type", "Genres", "Release"])



def movie_profile_page():
    movie_id = st.session_state.get("selected_movie_id") # Or the actual movie ID you are retrieving
    movie = get_movie_details(movie_id)

    if st.button("Back to Search"):
        st.session_state["current_page"] = "search"
        st.rerun()
    
    if movie:  # Ensure movie is not None
        st.title(movie['Name'])  # Use the dictionary key 'Name' instead of movie[1]
        
        # Display other movie details
        st.write(f"Type: {movie['Type']}")
        st.write(f"Genres: {movie['Genres']}")
        st.write(f"Release Date: {movie['Release']}")
        st.write(f"Average Rating: {movie['Average Rating']}")
        st.write(f"Total Reviews: {movie['Total Reviews']}")

    else:
        st.error("Movie details not found.")

# Function to fetch movie details
def get_movie_details(movie_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = sq.get_media_genre_names()
        cur.execute(sql, (movie_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
         
        if result:
            movie = result[0]  # ID
            movie_name = result[1]  # Name
            movie_type = result[2]  # Type
            movie_genres = ', '.join([str(result[i]) for i in range(3, 6) if result[i]])  # Join all non-null genres
            release_date = pd.to_datetime(result[6]).strftime('%B %d, %Y')
            avg_rating = result[7]  # Average Rating
            total_reviews = result[8]  # Total Reviews
            
            return {
                "ID": movie,
                "Name": movie_name,
                "Type": movie_type,
                "Genres": movie_genres,
                "Release": release_date,
                "Average Rating": avg_rating,
                "Total Reviews": total_reviews
            }
        return None
    except Exception as e:
        st.error(f"Error fetching movie details: {e}")
        return None


# Add custom CSS for background and buttons
st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
        color: #444;
    }
    button {
        background-color: #ff7f50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }
    button:hover {
        background-color: grey;
    }
    </style>
    """, unsafe_allow_html=True)

# Navigation Block
if st.session_state["current_page"] == "welcome":
    welcome_page()

elif st.session_state["current_page"] == "login":
    login_page()

elif st.session_state["current_page"] == "signup":
    signup_page()

elif st.session_state["current_page"] == "create_account":
    create_account_page()

elif st.session_state["current_page"] == "homepage":
    homepage()

elif st.session_state["current_page"] == "reviews":
    reviews_page()

elif st.session_state["current_page"] == "account":
    account_page()

elif st.session_state["current_page"] == "social":
    social_page()

elif st.session_state["current_page"] == "search":
    search_page()

elif st.session_state["current_page"] == "movie_profile":
    movie_profile_page()