import streamlit as st

# Set page configuration
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎥")

# Initialize session state for page navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "signup"

# Function to render the signup page
def signup_page():
    st.title("🎥 Movie Recommendation System")
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


def search_page():
    if st.button("⬅️ Back to Homepage"):
        st.session_state["current_page"] = "homepage"

    st.title("🔍 Search")
    st.subheader("Find Movies and TV Shows")
    st.write("Search our library for your favorite content or discover something new.")
    
    # Placeholder for search bar
    st.text_input("Search...", placeholder="Enter movie or TV show name")
    st.button("Search")
    st.markdown("**Search Results:**")
    st.write("🔎 Example Result: *The Dark Knight (2008)*")



# Navigation Block
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "signup"

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


