# PDF Splitter

A simple, efficient application for splitting large PDF files into smaller ones with a maximum page count.

## Features

- **User-Friendly Interface**: Built with Streamlit for a clean, intuitive user experience
- **Batch Processing**: Split multiple PDF files at once
- **Customizable Output**: Set the maximum pages per output file and customize naming for each input file
- **Real-time Feedback**: Clear status updates during processing
- **Local Storage**: All files are processed locally with output saved to a dedicated folder

## Use Cases

- Splitting large documents for email attachments
- Breaking books or manuals into smaller sections
- Creating separate files for different chapters or sections
- Processing files that are too large for certain viewing applications

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/skandydoc/PDF-Splitter.git
   cd PDF-Splitter
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run app.py
   ```

## Usage

1. Open the application in your web browser (typically http://localhost:8501)
2. Set the maximum number of pages per output file
3. Upload one or more PDF files using the file selector
4. Customize the output name template for each file
5. Click "Split All PDFs" to process the files
6. Output files will be saved to the "Output Files" folder in the application directory

## Limitations

- The application cannot process encrypted or password-protected PDF files
- Very large PDF files may require additional processing time
- Some PDF features like embedded forms might not be preserved in the split files

## Technologies Used

- [Streamlit](https://streamlit.io/): Front-end interface
- [PyPDF2](https://pypi.org/project/PyPDF2/): PDF manipulation library
- [Python](https://www.python.org/): Core programming language

## License

This project is available as open source under the terms of the MIT License.

## Acknowledgements

- All processing happens locally - your files never leave your computer
- No data is collected or transmitted to external services 