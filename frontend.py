import streamlit as st
import psycopg2
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎥")

# Initialize session state for page navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "signup"

# Function to render the signup page
def signup_page():
    st.title("🎥 Movie System")
    st.subheader("Signup Page")

    # Unique form key
    with st.form(key="signup_form_unique"):
        username = st.text_input("Username", placeholder="Enter your username")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        submit_button = st.form_submit_button("Sign Up")

    if submit_button:
        if password != confirm_password:
            st.error("Passwords do not match!")
        elif not username or not email or not password:
            st.error("All fields are required!")
        else:
            st.session_state["username"] = username
            st.session_state["email"] = email
            st.session_state["current_page"] = "create_account"

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
        use_column_width=True,
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


# Updated search page
def search_page():
    if st.button("⬅️ Back to Homepage"):
        st.session_state["current_page"] = "homepage"

    st.title("🔍 Search")
    st.subheader("Find Movies and TV Shows")
    st.write("Search our library for your favorite content or discover something new.")
    
    # Search input
    query = st.text_input("Search Movies:")
    if query:
        search_movies(query)

# Database connection function
def get_connection():
    return psycopg2.connect(
        host="localhost",       # Your database host
        database="movie_db",    # Your database name
        user="heslip",       # Your database username
        password="GavinLeafs2003!" # Your database password
    )

def get_movie_details(movie_id):
    """
    Retrieve detailed information about a specific movie.
    """
    conn = get_connection()
    cur = conn.cursor()
    sql = """
        SELECT media.id, media.name, type.name AS type, genre.name AS genre, media.date_released, media.full_average, media.total_reviews
        FROM media
        JOIN type ON media.type = type.id
        JOIN genre ON media.genre = genre.id
        WHERE media.id = %s
    """
    cur.execute(sql, (movie_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result


def search_movies(query):
    """
    Search for movies based on the query and display them as clickable links.
    """
    conn = get_connection()
    cur = conn.cursor()

    sql = """
        SELECT media.id, media.name, type.name AS type, genre.name AS genre, media.date_released
        FROM media
        JOIN type ON media.type = type.id
        JOIN genre ON media.genre = genre.id
        WHERE 
            LOWER(media.name) LIKE %s OR
            LOWER(type.name) LIKE %s OR
            LOWER(genre.name) LIKE %s OR
            TO_CHAR(media.date_released, 'YYYY-MM-DD') LIKE %s
    """
    search_term = f"%{query.lower()}%"
    cur.execute(sql, (search_term, search_term, search_term, search_term))
    results = cur.fetchall()
    cur.close()
    conn.close()

    if not results:
        st.write("No results found")
        return

    df = pd.DataFrame(results, columns=["ID", "Name", "Type", "Genre", "Release Date"])
    df['Release Date'] = pd.to_datetime(df['Release Date']).dt.strftime('%B %d, %Y')  # Format date

    for _, row in df.iterrows():
        st.markdown(
            f"[{row['Name']}](#)",
            unsafe_allow_html=True,
            key=f"movie_{row['ID']}",
            on_click=lambda movie_id=row['ID']: open_movie_profile(movie_id)
        )


def open_movie_profile(movie_id):
    """
    Open the profile page for a specific movie.
    """
    st.session_state.page = "profile"
    st.session_state.selected_movie_id = movie_id


def movie_profile_page():
    """
    Display the profile page for a selected movie.
    """
    movie_id = st.session_state.selected_movie_id
    movie = get_movie_details(movie_id)

    if not movie:
        st.write("Movie not found")
        return

    st.markdown(f"## {movie[1]}")
    st.write(f"**Type:** {movie[2]}")
    st.write(f"**Genre:** {movie[3]}")
    st.write(f"**Release Date:** {pd.to_datetime(movie[4]).strftime('%B %d, %Y')}")
    st.write(f"**Average Rating:** {movie[5]}")
    st.write(f"**Total Reviews:** {movie[6]}")

    # Back button to go to search
    if st.button("Back to Search"):
        st.session_state.page = "search"
        st.session_state.selected_movie_id = None


def main():
    """
    Main function to handle navigation and rendering.
    """
    if st.session_state.page == "search":
        st.title("Movie Search")
        query = st.text_input("Search for movies:")
        if st.button("Search"):
            search_movies(query)
    elif st.session_state.page == "profile":
        movie_profile_page()

        # Convert results to a pandas DataFrame for better display
        df = pd.DataFrame(results, columns=["ID", "Name", "Type", "Genre", "Release Date"])

        # Check if the DataFrame is empty
        if df.empty:
            st.write("No results found")
            return None

        # Format columns for better display
        df['Release Date'] = pd.to_datetime(df['Release Date']).dt.strftime('%B %d, %Y')  # Format date
        df = df.set_index("ID")  # Set movie ID as the index for cleaner output

        # Generate HTML output
        movie_html = ""
        for index, row in df.iterrows():
            movie_html += f"""
                <p><b>{row['Name']}</b> <i>{row['Type']}</i> <u>{row['Genre']}</u> <font color='blue'>{row['Release Date']}</font></p>
            """

        # Display the HTML formatted results using st.markdown
        st.markdown(movie_html, unsafe_allow_html=True)

    try:
        # Code that might raise an exception
        conn = get_connection()
        cur = conn.cursor()
        # Your SQL logic or other code here
        cur.close()
        conn.close()
    except Exception as e:
        st.write(f"An error occurred: {e}")


# Navigation Block
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "signup"  # Default page

if st.session_state["current_page"] == "signup":
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



