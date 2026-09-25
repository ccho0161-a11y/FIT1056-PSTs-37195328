import streamlit as st
 
 
def show_search_page(manager):
    """Renders a universal search page for students, teachers, and courses."""
    st.header("Search")
 
    with st.form("search_form"):
        search_type = st.selectbox("Search by", ["Name", "ID", "Course"])
        search_term = st.text_input("Search term")
        search_submitted = st.form_submit_button("Search")
 
        if search_submitted:
            if search_term.strip():
                results = manager.search_database(search_type, search_term.strip())
                if results:
                    for r in results:
                        st.write(r)
                else:
                    st.info("No matches found.")
            else:
                st.warning("Please enter a search term.")
 
    st.divider()