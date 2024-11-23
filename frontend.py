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
        database="cp317_final2",    # Your database name
        user="heslip",       # Your database username
        password="pass123" # Your database password
    )

# Create connection and cursor for DB
conn = get_connection()
cur = conn.cursor()


# Welcome Page
def welcome_page():
    # Centered image using st.image
    st.image("logo2.jpg", caption=None, width=600, use_container_width=False)

    # Buttons for Signup and Login
    col1, col2, col3 = st.columns([1, 1, 2])  # Outer columns create spacing
    with col2:  # Center column for buttons
        signup = st.button("Sign Up", key="signup")
    with col3:
        login = st.button("Login", key="login")
    
    # Handle button clicks
    if signup:
        st.session_state["current_page"] = "signup"
    if login:
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
    conn = get_connection()
    cur = conn.cursor()
    sql = sq.attempt_login()
    cur.execute(sql, (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user[0] if user else None

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
            user_id = verify_login(username, password)
            if user_id:  # Assuming `verify_login` returns `user_id` on success
                st.success("Login successful! Redirecting to homepage...")
                # Set the session for the logged-in user
                st.session_state["user_id"] = user_id
                st.session_state["username"] = username
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
            st.session_state["current_page"] = "login"

# Function to render the homepage
def homepage():
    account_id = st.session_state.get("user_id")
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

        # Logout Option
        st.markdown("### Logout")
        if st.button("Logout"):
            del st.session_state["user_id"]
            st.session_state["current_page"] = "welcome"
            st.success("You have been logged out.")

    with col2:
        if st.button("🤝 Social", help="Connect with friends and see what they're watching."):
            st.session_state["current_page"] = "social"
        if st.button("🔍 Search", help="Search our library for movies and TV shows."):
            st.session_state["current_page"] = "search"

    get_movie_recommendations(account_id)

def reviews_page():
    # Ensure account_id is retrieved from session state
    account_id = st.session_state.get("user_id")

    if st.button("⬅️ Back to Homepage"):
        st.session_state["current_page"] = "homepage"

    # Check if the user is logged in
    if account_id is None:
        st.warning("You need to log in to access the reviews page.")
        return

    st.title("🎥 Reviews")
    st.subheader("Explore Movie and TV Show Reviews")
    st.write("Here, you can browse through reviews or add your own.")

    # Media selection list
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM media ORDER BY name;")
    media_list = [row[0] for row in cur.fetchall()]
    conn.close()

    # Dropdown for movie name
    selected_movie_name = st.selectbox("Select a Movie/TV Show", media_list)

    # User input for review
    rating = st.slider("Rating", min_value=0.0, max_value=10.0, step=0.1)
    review_text = st.text_area("Write your review here...", placeholder="What did you think about the movie?")

    # Submit button logic
    if st.button("Submit Review"):
        if selected_movie_name and review_text:
            try:
                # Insert the review into the database
                conn = get_connection()
                cur = conn.cursor()
                sql = sq.add_review_frontend()
                cur.execute(sql, (account_id, selected_movie_name, rating, review_text))
                conn.commit()
                cur.close()
                conn.close()
                st.success(f"Review submitted successfully for **{selected_movie_name}**!")
            except Exception as e:
                st.error(f"An error occurred while submitting your review: {e}")
        else:
            st.warning("Please fill in all fields.")

    # Display latest reviews
    st.markdown("**Latest Reviews:**")
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = sq.get_recent_reviews()
        cur.execute(sql, (account_id,))
        reviews = cur.fetchall()
        cur.close()
        conn.close()

        if reviews:
            for review in reviews:
                st.write(f"🎬 **{review[3]}** - {review[1]}⭐")
                st.write(f"_Reviewed on {review[2]}:_ {review[0]}")
                st.markdown("---")
        else:
            st.info("You haven't reviewed any movies yet.")
    except Exception as e:
        st.error(f"An error occurred while fetching reviews: {e}")


def account_page():
    if st.button("⬅️ Back to Homepage"):
        st.session_state["current_page"] = "homepage"

    st.title("👤 Account Page")
    st.subheader("Manage Your Account and Preferences")

    account_id =  st.session_state.get("user_id")
    if account_id is None:
        st.warning("You need to log in to access the account page.")
        return

    # Database connection
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Fetch account details
        cur.execute(sq.get_self_summary(), (account_id,))
        user_details = cur.fetchone()

        if not user_details:
            st.error("Could not fetch account details.")
            return

        st.markdown("### Account Information")
        st.write(f"**Name:** {user_details[1]}")
        st.write(f"**Username:** {user_details[2]}")
        st.write(f"**Email:** {user_details[4]}")
        st.write(f"**Phone Number:** {user_details[3]}")
        st.write(f"**Total Reviews:** {user_details[5]}")
        st.write(f"**Followers:** {user_details[6]}")
        st.write(f"**Following:** {user_details[7]}")

        # Update Profile Section
        st.markdown("### Update Your Profile")
        with st.form(key="update_profile_form"):
            new_name = st.text_input("Full Name", value=user_details[1])
            new_username = st.text_input("Username", value=user_details[2])
            new_phone = st.text_input("Phone Number", value=user_details[3])
            new_email = st.text_input("Email", value=user_details[4])
            submit_update = st.form_submit_button("Save Changes")

        if submit_update:
            try:
                cur.execute(
                    """
                    UPDATE account 
                    SET name = %s, username = %s, phone = %s, email = %s
                    WHERE id = %s
                    """,
                    (new_name, new_username, new_phone, new_email, account_id),
                )
                conn.commit()
                st.success("Profile updated successfully!")
            except Exception as e:
                st.error(f"Error updating profile: {e}")

        # Account Reviews Section
        st.markdown("### Your Reviews")
        cur.execute(sq.get_account_review(), (account_id,))
        reviews = cur.fetchall()

        if reviews:
            for review in reviews:
                st.write(f"🎬 **{review[0]}** ({review[5]}) - Rated {review[1]}/10")
                st.write(f"_Review: {review[3]}_")
        else:
            st.write("You have not reviewed any movies yet.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()


def social_page():
    if st.button("⬅️ Back to Homepage"):
        st.session_state["current_page"] = "homepage"

    # Check navigation state
    if st.session_state.get("view_profile", False):
        # If viewing a profile, call view_profile_page
        user_id = st.session_state.get("selected_user_id")
        if st.button("⬅️ Back to Social Page"):
            st.session_state["view_profile"] = False
            st.rerun()
        view_profile_page(user_id)
        return

    st.title("🤝 Social Page")
    st.subheader("Stay Connected and Discover Movies")

    account_id =  st.session_state.get("user_id")
    if account_id is None:
        st.warning("You need to log in to access the social page.")
        return

    # Database connection
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Fetch followers and following
        cur.execute(sq.get_account_follows(), (account_id,))
        followers = cur.fetchall()

        cur.execute(sq.get_account_following(), (account_id,))
        following = cur.fetchall()

        st.markdown("### Connections")
        st.write(f"**Followers:** {len(followers)}")
        st.write(f"**Following:** {len(following)}")

        # Display follower and following details
        if followers:
            st.markdown("#### Followers")
            for follower in followers:
                st.write(f"👤 {follower[1]} - Reviews: {follower[2]} - Following: {follower[3]}")

        if following:
            st.markdown("#### Following")
            for follow in following:
                st.write(f"👤 {follow[1]} - Reviews: {follow[2]} - Following: {follow[3]}")

        # Manage connections
        st.markdown("### Manage Connections")
        col1, col2 = st.columns(2)

        # fetch all accounts for dropdown
        cur.execute(sq.get_all_accounts(), (account_id,))
        all_accounts = cur.fetchall()
        account_names = [acc[1] for acc in all_accounts] 

        with col1:
            new_follower = st.selectbox("Select a user to add as follower", options= ["Search for a friend..."] + account_names, index=0)  # Assuming account_names contains a list of usernames
            if st.button("Add Follower"):
                try:
                    # Trim any extra spaces in the input username
                    new_follower = new_follower.strip()
                    
                    # Check if the new_follower exists in the account table
                    cur.execute("SELECT id FROM account WHERE LOWER(name) = LOWER(%s)", (new_follower,))
                    result = cur.fetchone()
                    
                    if result:
                        new_follower_id = result[0]  # Get the account_id for the selected user
                        
                        # Check if the current user is already following the new_follower
                        cur.execute("SELECT 1 FROM following WHERE account_id = %s AND follows_id = %s", (account_id, new_follower_id))
                        already_following = cur.fetchone()
                        
                        if already_following:
                            st.warning(f"You are already following {new_follower}.")
                        else:
                            # Insert the follow relationship into the following table
                            cur.execute(sq.add_following(), (account_id, new_follower_id))
                            conn.commit()
                            
                            st.success(f"Added {new_follower} as a follower!")
                    else:
                        st.error(f"User {new_follower} not found!")
                        
                except Exception as e:
                    st.error(f"Error adding follower: {e}")



        with col2:
            unfollow = st.selectbox(
        "Select a user to unfollow", 
        options=[""] + account_names, 
        format_func=lambda x: "Search for a friend..." if x == "" else x, 
        index=0
        )   
            if st.button("Remove Following"):
                try:
                    # Trim any extra spaces in the input username
                    unfollow = unfollow.strip()
                    
                    # Check if the unfollow user exists in the account table
                    cur.execute("SELECT id FROM account WHERE LOWER(name) = LOWER(%s)", (unfollow,))
                    result = cur.fetchone()
                    
                    if result:
                        unfollow_id = result[0]  # Get the account_id for the user to unfollow
                        
                        # Check if the current user is following the user to unfollow
                        cur.execute("SELECT 1 FROM following WHERE account_id = %s AND follows_id = %s", (account_id, unfollow_id))
                        following_exists = cur.fetchone()
                        
                        if following_exists:
                            # Remove the follow relationship from the following table
                            cur.execute(sq.delete_following(), (account_id, unfollow_id))
                            conn.commit()
                            
                            st.success(f"Removed {unfollow} from following list!")
                        else:
                            st.warning(f"You are not following {unfollow}.")
                    else:
                        st.error(f"User {unfollow} not found!")
                        
                except Exception as e:
                    st.error(f"Error removing following: {e}")


        # Friends' activities
        st.markdown("### Friends' Recent Activities")
        cur.execute(sq.get_account_recent(), (account_id,))
        activities = cur.fetchall()

        if activities:
            for activity in activities:
                st.write(f"🎥 {activity[5]} watched {activity[4]} ({activity[1]}, {activity[2]}, {activity[3]}) and rated it {activity[6]}/10.")
        else:
            st.write("No recent activities from your connections.")

        # Add View Profile Navigation
        st.markdown("### View a Friend's Profile")
        selected_friend = st.selectbox(
            "Select a friend to view their profile:",
            options=[""] + [f[1] for f in following],  # Extract usernames from `following`
            format_func=lambda x: "Select a friend..." if x == "" else x,
        )
        if st.button("View Profile"):
            # Set navigation state and selected user ID
            for f in following:
                if f[1] == selected_friend:
                    st.session_state["view_profile"] = True
                    st.session_state["selected_user_id"] = f[0]
                    st.rerun()

        # Recommendations
        st.markdown("### Personalized Recommendations")
        if activities:
            st.write("Based on your followers' recent activities, we recommend:")
            for activity in activities[:5]:  # Show up to 5 recommendations
                st.write(f"🎬 {activity[2]} - Recommended by {activity[3]}")
        else:
            st.write("Start following people to get personalized recommendations!")

    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()


def view_profile_page(user_id):
    st.title("👤 View User Profile")

    # Fetch and display profile details
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(sq.get_account_summary(), (user_id,))
        profile = cur.fetchone()

        if profile:
            user_id, name, username, total_reviews, total_followers, total_following, avg_rating = profile

            # Display profile information
            st.markdown(f"### **{name}**")
            st.markdown(f"- **Username:** {username}")
            st.markdown(f"- **Total Reviews:** {total_reviews}")
            st.markdown(f"- **Followers:** {total_followers}")
            st.markdown(f"- **Following:** {total_following}")
            st.markdown(f"- **Average Rating:** {avg_rating:.1f}" if avg_rating else "- **Average Rating:** N/A")

            # Fetch and display reviews
            cur.execute(sq.get_account_review(), (user_id,))
            reviews = cur.fetchall()

            if reviews:
                st.markdown("### Reviews:")
                for review in reviews:
                    movie_name, rating, diff, description, genre_name, type_name = review
                    st.markdown(f"- 🎬 **{movie_name}** ({genre_name}, {type_name}) - Rated: {rating}/10")
                    st.markdown(f"  _Review: {description}_")
            else:
                st.info("No reviews found.")
        else:
            st.error("User not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()


def search_page():
    st.title("🔍 Search for Movies")

    if st.button("Back to Homepage"):
        st.session_state["current_page"] = "homepage"
        st.rerun()

    account_id =  st.session_state.get("user_id")
    if account_id is None:
        st.warning("You need to log in to access the account page.")
        return
    
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
    get_movie_recommendations(account_id)

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
    movie_id = st.session_state.get("selected_movie_id")  # Retrieve selected movie ID from session state
    movie = get_movie_details(movie_id)  # Function to fetch movie details based on ID

    # Back to Search Button
    if st.button("⬅️ Back to Search"):
        st.session_state["current_page"] = "search"
        st.rerun()

    # Display Movie Details
    if movie:  # Ensure movie is not None
        st.title(movie['Name'])  # Use the dictionary key 'Name'

        # Display other movie details
        st.write(f"🎥 **Type**: {movie['Type']}")
        st.write(f"🎭 **Genres**: {movie['Genres']}")
        st.write(f"📅 **Release Date**: {movie['Release']}")
        st.write(f"⭐ **Average Rating**: {movie['Average Rating']:.1f}")
        st.write(f"👥 **Total Reviews**: {movie['Total Reviews']}")
        st.write(f"🎬 **Studio**: {movie['Studio']}")
        st.write(f"🎞️ **Producer**: {movie['Producer']}")

        # Write a Review Button
        if st.button("✍️ Write a Review"):
            st.session_state["current_page"] = "reviews"  # Redirect to review page
            st.session_state["selected_media_name"] = movie['Name']            
            st.rerun()

        # Divider
        st.markdown("---")

        # Fetch and Display Recent Reviews
        st.subheader("📝 Recent Reviews")
        try:
            conn = get_connection()  # Establish database connection
            cur = conn.cursor()

            # SQL to fetch recent reviews for the movie
            sql = sq.get_specific_reviews()
            cur.execute(sql, (movie_id,))
            reviews = cur.fetchall()
            cur.close()
            conn.close()

            if reviews:
                # Display each review
                for review in reviews:
                    st.markdown(f"**{review[3]}** rated it **{review[1]}⭐**")
                    st.markdown(f"_Reviewed on {review[2]}:_ {review[0]}")
                    st.markdown("---")
            else:
                st.info("No reviews yet for this movie.")
        except Exception as e:
            st.error(f"An error occurred while fetching reviews: {e}")
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
            studio = result[9]
            producer = result[10]
            
            return {
                "ID": movie,
                "Name": movie_name,
                "Type": movie_type,
                "Genres": movie_genres,
                "Release": release_date,
                "Average Rating": avg_rating,
                "Total Reviews": total_reviews,
                "Studio": studio,
                "Producer": producer
            }
        return None
    except Exception as e:
        st.error(f"Error fetching movie details: {e}")
        return None


import streamlit as st

def get_movie_recommendations(user_id):
    try:
        # SQL Query to get 5 movie recommendations based on user preferences
        recommendation_query = """
        SELECT DISTINCT 
            m.id, 
            m.name, 
            g.name AS genre1, 
            g2.name AS genre2, 
            g3.name AS genre3, 
            t.name AS type_name, 
            m.full_average, 
            m.date_released
        FROM media m
        LEFT JOIN genre g ON m.genre = g.id
        LEFT JOIN genre g2 ON m.genre2 = g2.id
        LEFT JOIN genre g3 ON m.genre3 = g3.id
        JOIN type t ON m.type = t.id
        WHERE (
            m.genre IN (
                SELECT m.genre FROM review r
                JOIN media m ON r.media_id = m.id
                WHERE r.account_id = %s
                GROUP BY m.genre
                ORDER BY AVG(r.rating) DESC
                LIMIT 3
            )
            OR m.genre2 IN (
                SELECT m.genre2 FROM review r
                JOIN media m ON r.media_id = m.id
                WHERE r.account_id = %s
                GROUP BY m.genre2
                ORDER BY AVG(r.rating) DESC
                LIMIT 3
            )
            OR m.genre3 IN (
                SELECT m.genre3 FROM review r
                JOIN media m ON r.media_id = m.id
                WHERE r.account_id = %s
                GROUP BY m.genre3
                ORDER BY AVG(r.rating) DESC
                LIMIT 3
            )
        )
        AND m.id NOT IN (
            SELECT media_id FROM review WHERE account_id = %s
        )
        ORDER BY m.full_average DESC, m.date_released DESC
        LIMIT 5;
        """

        # Execute the query
        cur.execute(recommendation_query, (user_id, user_id, user_id, user_id))
        recommendations = cur.fetchall()

        # Display the recommendations horizontally
        st.markdown("""
            <div style="
                background: #f1f1f1;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
                padding: 20px;
            ">
                <h4 style='color: #333;'>Here are some movies recommended globally:</h4>
            </div>
        """, unsafe_allow_html=True)

        if recommendations:
            # Create columns for displaying movies horizontally
            columns = st.columns(5)  # Create 5 columns for 5 movies

            for idx, movie in enumerate(recommendations):
                movie_id, movie_name, genre1, genre2, genre3, type_name, full_average, date_released = movie
                genres = ", ".join([g for g in [genre1, genre2, genre3] if g])

                # Display each movie in the corresponding column
                with columns[idx]:
                    st.markdown(f"""
                        <div style="
                            background: white;
                            border-radius: 10px;
                            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
                            margin-bottom: 15px;
                            padding: 15px;
                        ">
                            <h5 style='color: #222;'>{movie_name}</h5>
                            <p style='color: #555;'>🎭 Genres: {genres}</p>
                            <p style='color: #555;'>📺 Type: {type_name}</p>
                            <p style='color: #555;'>⭐ Average Rating: {full_average:.2f}</p>
                            <p style='color: #555;'>📅 Released: {date_released.strftime('%Y-%m-%d')}</p>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
                    padding: 15px;
                ">
                    <p style='color: #555;'>No recommendations available at the moment.</p>
                </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred while fetching recommendations: {e}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()




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