from PyPDF2 import PdfReader
import re

class Reader:
    def __init__(self, file):
        self.file = file
    
    def read(self):
        try:
            # Add type checking for the file parameter
            if not isinstance(self.file, (str, bytes)):
                raise ValueError("File parameter must be a string path or bytes object")

            # Load the PDF file
            pdf = PdfReader(self.file)
            
            # Initialize results
            table_contents = []
            
            # Iterate through all pages
            for page in pdf.pages:
                text = page.extract_text()
                print(text)
                
                # Look for tabular data patterns
                # This is a simple approach - looks for text separated by multiple spaces
                # or text arranged in column-like format
                lines = text.split('\n')
                print (lines)
                for line in lines:
                    print(line)
                    # Split on multiple spaces to detect table-like data
                    cells = re.split(r'\s{2,}', line.strip())
                    
                    # Only include lines that appear to be table data
                    # (have multiple cells after splitting)
                    if len(cells) > 1:
                        table_contents.append([cell.strip() for cell in cells if cell.strip()])
            
            return {
                "tables": table_contents
            }
            
        except Exception as e:
            return {"error": f"Failed to read PDF document: {str(e)}"}

reader = Reader("C:\\Users\\EfraimdeAlmeidaLima\\OneDrive - Under Protection\\Documentos\\ATAS\\ATA - CLIENTE - MOTIVO - DATA.pdf")
result = reader.read()
print(result)