tell application "Terminal"
    -- Prevent Terminal from opening a new window
    do script "cd /Users/sb/Desktop/projects_master/PDFSplitter && streamlit run app.py"
    
    -- Wait a moment for the server to start
    delay 2
    
    -- Hide Terminal
    set visible of front window to false
end tell

-- Open the default browser to the Streamlit app
do shell script "open http://localhost:8501" 