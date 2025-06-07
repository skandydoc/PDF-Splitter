import os
from PyPDF2 import PdfReader, PdfWriter
import logging

def split_pdf(input_path, output_folder, naming_scheme='output', max_pages=175):
    """
    Split a PDF file into smaller files with a maximum number of pages.
    
    Args:
        input_path (str): Path to the input PDF file
        output_folder (str): Directory to save the split PDF files
        naming_scheme (str): Base name for output files
        max_pages (int): Maximum pages per output file
    
    Returns:
        dict: Status information with success/error details
    """
    # Validate inputs
    if not input_path or not os.path.exists(input_path):
        return {
            'status': 'error',
            'message': 'Input PDF file not found or path is invalid.',
            'files': [],
            'total_files': 0
        }
    
    if max_pages <= 0:
        return {
            'status': 'error',
            'message': 'Maximum pages must be a positive number.',
            'files': [],
            'total_files': 0
        }
    
    # Sanitize naming scheme
    naming_scheme = "".join(c for c in naming_scheme if c.isalnum() or c in (' ', '-', '_')).strip()
    if not naming_scheme:
        naming_scheme = 'output'
    
    # Create output folder if it doesn't exist
    try:
        os.makedirs(output_folder, exist_ok=True)
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Cannot create output directory: {str(e)}',
            'files': [],
            'total_files': 0
        }
    
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
                
                # Check if PDF has any pages
                if total_pages == 0:
                    return {
                        'status': 'error',
                        'message': 'The PDF file appears to be empty (no pages found).',
                        'files': [],
                        'total_files': 0
                    }

                # Calculate the number of output PDFs
                num_output_pdfs = (total_pages + max_pages - 1) // max_pages
                
                split_files = []  # To store paths of created files

                for i in range(num_output_pdfs):
                    try:
                        output = PdfWriter()
                        start_page = i * max_pages
                        end_page = min((i + 1) * max_pages, total_pages)

                        # Add pages to the output PDF
                        for page_num in range(start_page, end_page):
                            try:
                                page = pdf.pages[page_num]
                                output.add_page(page)
                            except Exception as e:
                                logging.warning(f"Could not process page {page_num + 1}: {str(e)}")
                                continue

                        # Add basic metadata
                        try:
                            output.add_metadata({
                                '/Producer': 'PDF Splitter',
                                '/Creator': 'PDF Splitter',
                                '/Title': f'{naming_scheme}_{i + 1}'
                            })
                        except Exception:
                            # Metadata is optional, continue without it
                            pass

                        # Save the output PDF
                        output_path = os.path.join(output_folder, f'{naming_scheme}_{i + 1}.pdf')
                        with open(output_path, 'wb') as output_file:
                            output.write(output_file)
                        
                        split_files.append(output_path)
                        
                    except Exception as e:
                        logging.error(f"Error creating split file {i + 1}: {str(e)}")
                        continue

                if not split_files:
                    return {
                        'status': 'error',
                        'message': 'Failed to create any split files. The PDF may be corrupted.',
                        'files': [],
                        'total_files': 0
                    }

                return {
                    'status': 'success',
                    'message': f'Split complete. {len(split_files)} PDFs created from {total_pages} pages',
                    'files': split_files,
                    'total_files': len(split_files)
                }
                
            except Exception as e:
                error_msg = str(e).lower()
                if "encryption" in error_msg or "password" in error_msg:
                    return {
                        'status': 'error',
                        'message': 'This PDF is encrypted/password-protected. Please provide a decrypted PDF file.',
                        'files': [],
                        'total_files': 0
                    }
                elif "invalid" in error_msg or "corrupt" in error_msg:
                    return {
                        'status': 'error',
                        'message': 'The PDF file appears to be corrupted or invalid.',
                        'files': [],
                        'total_files': 0
                    }
                else:
                    return {
                        'status': 'error',
                        'message': f'Error processing PDF: {str(e)}',
                        'files': [],
                        'total_files': 0
                    }
                    
    except FileNotFoundError:
        return {
            'status': 'error',
            'message': 'PDF file not found. Please check the file path.',
            'files': [],
            'total_files': 0
        }
    except PermissionError:
        return {
            'status': 'error',
            'message': 'Permission denied. Cannot read the PDF file.',
            'files': [],
            'total_files': 0
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Unexpected error: {str(e)}',
            'files': [],
            'total_files': 0
        }
