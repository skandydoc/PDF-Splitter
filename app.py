import streamlit as st
import os
from pdf_splitter import split_pdf
import tempfile
from pathlib import Path

# Health check for Cloud Run
if st.query_params.get("health") == "check":
    st.write("OK")
    st.stop()

# Disable Streamlit's default menu
st.set_page_config(
    page_title="PDF Splitter",
    page_icon="📄",
    layout="centered",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Create Output Files directory next to app.py
output_directory = Path(os.path.dirname(os.path.abspath(__file__))) / "Output Files"
output_directory.mkdir(exist_ok=True)

# Styling remains the same
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .stButton>button {
        background-color: #007AFF;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .success-message {
        padding: 1rem;
        border-radius: 8px;
        background-color: #E8F5E9;
        color: #1B5E20;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        border-radius: 8px;
        background-color: #FFEBEE;
        color: #B71C1C;
        margin: 1rem 0;
    }
    .file-status {
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        background-color: #F5F5F5;
    }
    .file-config {
        padding: 1rem;
        border-radius: 8px;
        background-color: #F8F9FA;
        margin: 1rem 0;
        border: 1px solid #E9ECEF;
    }
    </style>
    """, unsafe_allow_html=True)

# App header
st.title("PDF Splitter")
st.markdown("Split multiple PDF files into smaller ones with ease.")

# Get max pages upfront
max_pages = st.number_input(
    "Maximum pages per file",
    min_value=1,
    value=175,
    help="Maximum number of pages in each split PDF"
)

# Multiple file uploader
uploaded_files = st.file_uploader(
    "Choose PDF files",
    type=['pdf'],
    accept_multiple_files=True,
    help="You can select multiple PDF files by holding Ctrl/Cmd while selecting"
)

if uploaded_files:
    st.info(f"Selected {len(uploaded_files)} file(s)")
    
    # Dictionary to store output names for each file
    if 'output_names' not in st.session_state:
        st.session_state.output_names = {}
    
    # Create input fields for each file's output name
    st.subheader("Configure Output Names")
    
    for uploaded_file in uploaded_files:
        file_id = uploaded_file.name
        file_base_name = os.path.splitext(uploaded_file.name)[0]
        
        # Initialize default name if not already set
        if file_id not in st.session_state.output_names:
            st.session_state.output_names[file_id] = file_base_name
        
        st.markdown(f"""
            <div class="file-config">
            """, unsafe_allow_html=True)
        
        # Show file name and size
        file_size_mb = uploaded_file.size / (1024 * 1024)
        st.markdown(f"**{uploaded_file.name}** ({file_size_mb:.1f} MB)")
        
        # Input for output name
        st.session_state.output_names[file_id] = st.text_input(
            "Output name template",
            value=st.session_state.output_names[file_id],
            key=f"name_{file_id}",
            help="Base name for the split PDF files. Each file will be suffixed with _1, _2, etc."
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Process PDF button
    if st.button("Split All PDFs"):
        overall_success = True
        
        for idx, uploaded_file in enumerate(uploaded_files, 1):
            with st.spinner(f"Processing {uploaded_file.name} ({idx}/{len(uploaded_files)})..."):
                file_id = uploaded_file.name
                output_name = st.session_state.output_names[file_id]
                
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_input = tmp_file.name
                    
                    # Process the PDF - now using output_directory directly
                    result = split_pdf(temp_input, str(output_directory), output_name, max_pages)
                    
                    # Clean up temporary input file
                    os.unlink(temp_input)
                    
                    # Display individual file results
                    if result['status'] == 'success':
                        st.markdown(f"""
                            <div class="file-status">
                                ✅ {uploaded_file.name}: {result['message']}
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        overall_success = False
                        st.markdown(f"""
                            <div class="error-message">
                                ❌ {uploaded_file.name}: {result['message']}
                            </div>
                        """, unsafe_allow_html=True)
        
        # Show final status
        if overall_success:
            st.markdown(f"""
                <div class="success-message">
                    All files processed successfully!<br>
                    Files have been saved to: {output_directory}
                </div>
            """, unsafe_allow_html=True)
            
            # Show file listing - modified to show flat structure
            st.subheader("Processed Files")
            for pdf_file in output_directory.glob("*.pdf"):
                st.text(f"↳ {pdf_file.name}")
        else:
            st.warning("Some files could not be processed. Check the errors above.")

# Add footer
st.markdown("---")
st.markdown("Files are automatically saved to the 'Output Files' folder")