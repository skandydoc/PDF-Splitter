import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_path, output_folder, naming_scheme='output', max_pages=175):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        # Open the input PDF
        with open(input_path, 'rb') as file:
            try:
                pdf = PdfReader(file)
                
                # Check if PDF is encrypted
                if pdf.is_encrypted:
                    return {
                        'status': 'error',
                        'message': 'This PDF is encrypted/password-protected. Please provide a decrypted PDF file.',
                        'files': [],
                        'total_files': 0
                    }

                total_pages = len(pdf.pages)

                # Calculate the number of output PDFs
                num_output_pdfs = (total_pages + max_pages - 1) // max_pages
                
                split_files = []  # To store paths of created files

                for i in range(num_output_pdfs):
                    output = PdfWriter()
                    start_page = i * max_pages
                    end_page = min((i + 1) * max_pages, total_pages)

                    # Add pages to the output PDF
                    for page_num in range(start_page, end_page):
                        page = pdf.pages[page_num]
                        output.add_page(page)

                    # Add basic metadata
                    output.add_metadata({
                        '/Producer': 'PDF Splitter',
                        '/Creator': 'PDF Splitter'
                    })

                    # Save the output PDF with compression
                    output_path = os.path.join(output_folder, f'{naming_scheme}_{i + 1}.pdf')
                    with open(output_path, 'wb') as output_file:
                        output.write(output_file)
                    
                    split_files.append(output_path)

                return {
                    'status': 'success',
                    'message': f'Split complete. {num_output_pdfs} PDFs created in {output_folder}',
                    'files': split_files,
                    'total_files': num_output_pdfs
                }
            except Exception as e:
                if "encryption" in str(e).lower():
                    return {
                        'status': 'error',
                        'message': 'This PDF is encrypted/password-protected. Please provide a decrypted PDF file.',
                        'files': [],
                        'total_files': 0
                    }
                raise e
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}',
            'files': [],
            'total_files': 0
        }
