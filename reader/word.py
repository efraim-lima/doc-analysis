from docx import Document

class Reader:
    def __init__(self, file):
        self.file
        pass
    
    def read(self):
        try:
            
            # Load the document
            doc = Document(self.file)
            
            # Initialize results list
            table_contents = []
            
            # Iterate through all tables in document
            for table in doc.tables:
                table_data = []
                
                # Iterate through rows and cells
                for row in table.rows:
                    for cell in row.cells:
                        # Get text content of cell
                        text = cell.text.strip()
                        if text:  # Only include non-empty cells
                            table_data.append(text)
                
                # Add table data if not empty
                if table_data:
                    table_contents.append(table_data)
            
            return {
                "tables": table_contents
            }
            
        except Exception as e:
            return {"error": f"Failed to read Word document: {str(e)}"}


Reader.read("C:\Users\EfraimdeAlmeidaLima\OneDrive - Under Protection\Documentos\ATAS\ATA - CLIENTE - MOTIVO - D.A.TA.docx")