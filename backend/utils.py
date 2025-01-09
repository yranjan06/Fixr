def validate_file(file):
    """Validate uploaded file"""
    import magic
    
    if not file:
        raise ValueError("No file provided")
        
    # Check if filename is safe
    filename = secure_filename(file.filename)
    if not filename:
        raise ValueError("Invalid filename")
        
    # Check file extension
    if not ('.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'):
        raise ValueError("Only PDF files are allowed")
        
    # Check MIME type
    mime = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)  # Reset file pointer
    
    if mime != 'application/pdf':
        raise ValueError("Invalid file type")
        
    return filename