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
        database="cp317_db",    # Your database name
        user="postgres",       # Your database username
        password="password" # Your database password
    )

# Create connection and cursor for DB
conn = get_connection()
cur = conn.cursor()



def get_symbol(val):
    if val > 0:
        return "✅"
    else:
        return "❗"
def scroll():
    st.markdown("""
    <script>
        window.scrollTo(0, 0);
    </script>
    """, unsafe_allow_html=True)


# Welcome Page (*)
def welcome_page():

    #Photo
    st.image("logo2.jpg", caption=None, width=600, use_container_width=False)
    col1, col2, col3 = st.columns([1, 1, 2]) 

    #Sign Up
    with col2: 
        if st.button("Sign Up", key="signup"):
            st.session_state["current_page"] = "signup"

    #Login
    with col3:
        if st.button("Login", key="login"):
            st.session_state["current_page"] = "login"
    
# SignUp Page (*)
def signup_page():
    st.title("📝 Sign Up")
    
    # Collect user input
    name = st.text_input("Full Name")
    username = st.text_input("Username")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    
    #Attempt To Create
    if st.button("Create Account"):
        #If Not All Info
        if not name or not username or not email or not phone or not password:
            st.error("Please fill out all fields.")
            return
        
        #Try To Create Account
        try:
            cur.execute(sq.add_account(), (name, username, email, phone, password))
            conn.commit()

            #If Successful
            if cur.rowcount > 0:
                st.success("Account created successfully! Redirecting to login...")
                st.session_state["current_page"] = "create_account"
                st.rerun()
            #If Unsuccessfull
            else:
                st.error("Failed to create account. Please try again.")
        
        except:
            st.error("Error Accessing Database")


# Login Page (*)
def login_page():
    st.title("Login Page")

    if st.button("⬅️ Back to Welcome Page"):
        st.session_state["current_page"] = "welcome"

    # User Input Fields
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Login")

    # Attempt To Login
    if login_button:
        #If Both Filled Out
        if username and password:

            #Check Database
            cur.execute(sq.attempt_login(), (username, password))
            user_id = cur.fetchone()

            #If Returns Valid Account
            if user_id:
                st.success("Login successful! Redirecting to homepage...")
                st.session_state["user_id"] = user_id
                st.session_state["username"] = username
                st.session_state["current_page"] = "homepage"
            #Fails
            else:
                st.error("Invalid username or password. Please try again.")
        else:
            st.warning("Please enter both username and password.")

# Create Account Page (*)
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

# Homepage
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
    col1, col2,col3 = st.columns(3)

    with col1:
        if st.button("👤 Manage Account", help="Manage your account settings and preferences."):
            st.session_state["current_page"] = "account"

        if st.button("🎥 Make Reviews", help="Check out reviews of movies and TV shows."):
            st.session_state["current_page"] = "reviews"
        

    with col2:
        if st.button("🤝 Social", help="See Peer Activity"):
            st.session_state["current_page"] = "social"
        if st.button("🔍 Search", help="Search For Media"):
            st.session_state["current_page"] = "search"

    with col3:
        if st.button("✍️ Reccomendations", help="Get Reccomendations"):
            st.session_state["current_page"] = "reccomendations"
        if st.button("❌ Logout"):
            del st.session_state["user_id"]
            st.session_state["current_page"] = "welcome"
            st.success("You have been logged out.")

    get_movie_recommendations(account_id)


#Reviews Page
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
    # Submit button logic
    if st.button("Submit Review"):
        if selected_movie_name:
            try:
                # Insert the review into the database
                conn = get_connection()
                cur = conn.cursor()
                sql = sq.add_review_frontend()
                cur.execute(sql, (account_id, selected_movie_name, rating, "None"))
                conn.commit()
                cur.close()
                conn.close()
                st.session_state["current_page"] = "account"
                return
            except Exception as e:
                st.error(f"An error occurred while submitting your review: {e}")
        else:
            st.warning("Please fill in all fields.")
        

#Account Page (Our)
def account_page():
    scroll()
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

        # Update Profile Section
        st.markdown("### Your Profile/Info")
        with st.form(key="update_profile_form"):
            new_name = st.text_input("Full Name(shown)", value=user_details[1])
            new_username = st.text_input("Username(shown)", value=user_details[2])
            new_phone = st.text_input("Phone Number(not shown)", value=user_details[3])
            new_email = st.text_input("Email(not shown)", value=user_details[4])
            st.write(f"**Total Reviews:** {user_details[5]}")
            st.write(f"**Followers:** {user_details[6]}")
            st.write(f"**Following:** {user_details[7]}")
            submit_update = st.form_submit_button("Save Changes")

        #Commit Update
        if submit_update:
            try:
                cur.execute(""" UPDATE account 
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
        st.markdown("### Your Reviews (expand)")
        cur.execute(sq.get_account_review(), (account_id,))
        print_account_reviews(cur.fetchall())

    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()

#Prints List Of Reviews For Account
def print_account_reviews(reviews):
    if reviews:
        with st.expander(f"Date, Name, Rating, (Difference From Global)"):
            for review in reviews:
                if st.button(f"🎬{review[7]} - **{review[0]}**({review[4]}) - Rated {review[1]}/10 ({round(review[2],1)}{get_symbol(review[2])})"):
                    st.session_state["current_page"] = "movie_profile"
                    st.session_state["selected_movie_id"] = review[6]
    else:
            st.write("No reviews yet.")

#Account Page (Other)
def other_account_page():
    scroll()
    st.title("👤 View User Profile")

    # Fetch and display profile details
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(sq.get_account_summary(), (st.session_state["selected_account_id"],))
        profile = cur.fetchone()

        if profile:
            user_id, name, username, total_reviews, total_followers, total_following, avg_rating, delta = profile
            st.markdown("### Profile/Info")
            # Display profile information
            st.markdown(f"- **Name:** {name}")
            st.markdown(f"- **Username:** {username}")
            st.markdown(f"- **Total Reviews:** {total_reviews}")
            st.markdown(f"- **Followers:** {total_followers}")
            st.markdown(f"- **Following:** {total_following}")
            if avg_rating: 
                st.markdown(f"- **Average Rating:** {avg_rating:.1f} ({round(delta,1)}{get_symbol(delta)})")
            else: st.markdown(f"- **Average Rating:** N/A")
            
            # Fetch and display reviews
            st.markdown("### Reviews (expand)")
            cur.execute(sq.get_account_review(), (st.session_state["selected_account_id"],))
            print_account_reviews(cur.fetchall())
            
        else:
            st.error("User not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()

#Media Page
def media_page():
    scroll()
    movie = get_movie_details(st.session_state["selected_movie_id"])  

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

        # Fetch and Display Recent Reviews
        st.subheader("📝 Recent Reviews By Following (expand)")
        try:
            conn = get_connection()  # Establish database connection
            cur = conn.cursor()

            cur.execute(sq.get_media_reviews(), (st.session_state["selected_movie_id"],st.session_state["user_id"]))
            print_media_reviews(cur.fetchall())

            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"An error occurred while fetching reviews: {e}")
    else:
        st.error(f"Movie details not found.")

#Prints List Of Media Reviews (From Following)
def print_media_reviews(reviews):
    if reviews:
         with st.expander(f"Date, Account, Rating, (Difference From Global)"):
            for review in reviews:
                if st.button(f"🧑‍🧒 {review[1]} - {review[2]} - Rated {review[0]}/10 ({round(review[3],1)}{get_symbol(review[3])})"):
                    st.session_state["current_page"] = "account_profile"
                    st.session_state["selected_account_id"] = review[4]

def print_following(following, name, f):
    with st.expander(f"{name} ({len(following)})"):
        for foll in following:
            col11, col22 = st.columns([2, 1])

            with col11:
                if st.button(f"{foll[1]} ({foll[2]}) - {foll[3]}", key=f"{f}{foll[0]}"):
                    st.session_state["current_page"] = "account_profile"
                    st.session_state["selected_account_id"] = foll[0]
            with col22:
                if st.button(f"Remove:{foll[0]}", key=f"{f}{foll[0]}R"):
                    if name == "Following":
                        cur.execute(sq.delete_following(), (st.session_state["user_id"], foll[0]))
                    else:
                        cur.execute(sq.delete_following(), (foll[0], st.session_state["user_id"]))
                    conn.commit()
                    st.session_state["current_page"] = "social"


#SOCIAL PAGE
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


    conn = get_connection()
    cur = conn.cursor()

    st.write("## Discover Accounts")
    query = st.text_input("Search Account:")
    if query:
        cur.execute(sq.get_searched_account(), (st.session_state["user_id"], f"%{query.lower()}%"))
        
        matchs = cur.fetchall()
        if not matchs:
            st.write("No results found.")
        else:
            with st.expander(f"Matchs"):
                for row in matchs:
                    col11, col22 = st.columns([2, 1])

                    with col11:
                        if st.button(f"{row[1]} ({row[2]})"):
                            st.session_state["current_page"] = "account_profile"
                            st.session_state["selected_account_id"] = row[0]
                    
                    with col22:
                        if row[3] == 1 :
                            st.write("Already Followed")
                        else:
                            if st.button(f" Follow: {row[2]}"):
                                cur.execute(sq.add_following(), (st.session_state["user_id"], row[0]))
                                conn.commit()
                                st.rerun()
                        
                            
    
    st.write("## Your Following")
    cur.execute(sq.get_account_following(), (account_id,))
    print_following(cur.fetchall(), "Following", "F")
    
    cur.execute(sq.get_account_follows(), (account_id,))
    print_following(cur.fetchall(), "Followers", "f")



#SEARCH PAGE
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
            
            for _, row in movies.iterrows():
                if st.button(f"{row['Name']} ({row['Type']})  -  -  -  {row['Genres']}"):
                    st.session_state["selected_movie_id"] = row["ID"]
                    st.session_state["current_page"] = "movie_profile"
                    st.rerun()

    # Global Recommendations Section
    get_movie_recommendations(account_id)


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
        LIMIT 3;
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
                <h4 style='color: #333;'>Here are some uniquely recommended films :</h4>
            </div>
        """, unsafe_allow_html=True)

        if recommendations:
            # Create columns for displaying movies horizontally
            columns = st.columns(3)  # Create 5 columns for 5 movies

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



#Welcome Page
if st.session_state["current_page"] == "welcome":
    welcome_page()

#Login Page
elif st.session_state["current_page"] == "login":
    login_page()

#Sign Up Page
elif st.session_state["current_page"] == "signup":
    signup_page()

#Create Account Page
elif st.session_state["current_page"] == "create_account":
    create_account_page()

#HomePage
elif st.session_state["current_page"] == "homepage":
    homepage()

#Add Review
elif st.session_state["current_page"] == "reviews":
    reviews_page()

#Account Details
elif st.session_state["current_page"] == "account":
    account_page()

#Reccomendations
elif st.session_state["current_page"] == "recommendation":
    recommendation_page()

#Social
elif st.session_state["current_page"] == "social":
    social_page()

#Search
elif st.session_state["current_page"] == "search":
    search_page()

#Movie Profile
elif st.session_state["current_page"] == "movie_profile":
    media_page()

#Other Account
elif st.session_state["current_page"] == "account_profile":
    other_account_page()
