import os
from celery import Celery
from collector.microsoft.api import Microsoft
from collector.zeev.api import Zeev
from reader.word import WordReader
from reader.excell import ExcelReader
from reader.pdf import PDFReader

# Get Redis URL from environment variable
CELERY_BROKER_URL = os.getenv('BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('RESULT_BACKEND', 'redis://localhost:6379/0')

# Initialize Celery
celery_app = Celery('document_processor',
                    broker=CELERY_BROKER_URL,
                    backend=CELERY_RESULT_BACKEND)

# Load Celery configuration
celery_app.config_from_object('celeryconfig')

class DocumentManager:
    def __init__(self):
        self.microsoft = Microsoft()
        self.zeev = Zeev()
        self.word_reader = WordReader()
        self.excel_reader = ExcelReader()
        self.pdf_reader = PDFReader()

@celery_app.task(name='tasks.collect_microsoft_data')
def collect_microsoft_data():
    """
    Async task to collect Microsoft data
    """
    try:
        microsoft = Microsoft()
        response = microsoft.get()
        return response.get_json() if response else None
    except Exception as e:
        return {"status": "Error", "message": str(e)}

@celery_app.task(name='tasks.collect_zeev_data')
def collect_zeev_data():
    """
    Async task to collect Zeev data
    """
    try:
        zeev = Zeev()
        response = zeev.get()
        return response.get_json() if response else None
    except Exception as e:
        return {"status": "Error", "message": str(e)}

@celery_app.task(name='tasks.process_document')
def process_document(document_type, file_path):
    """
    Async task to process a document
    """
    try:
        manager = DocumentManager()
        
        if document_type == 'word':
            result = manager.word_reader.read_document(file_path)
        elif document_type == 'excel':
            result = manager.excel_reader.read_workbook(file_path)
        elif document_type == 'pdf':
            result = manager.pdf_reader.read_pdf(file_path)
        else:
            return {"status": "Error", "message": "Invalid document type"}
        
        return {
            "status": "Success",
            "document_type": document_type,
            "result": result
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}

@celery_app.task(name='tasks.process_all_sources')
def process_all_sources():
    """
    Async task to process data from all sources
    """
    try:
        # Create async tasks for each source
        microsoft_task = collect_microsoft_data.delay()
        zeev_task = collect_zeev_data.delay()
        
        # Wait for results
        microsoft_result = microsoft_task.get(timeout=300)  # 5 minutes timeout
        zeev_result = zeev_task.get(timeout=300)
        
        # Combine results
        return {
            "status": "Success",
            "data": {
                "microsoft": microsoft_result.get('data', []) if microsoft_result else [],
                "zeev": zeev_result.get('data', []) if zeev_result else []
            }
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}

# Example of how to chain tasks
@celery_app.task(name='tasks.complete_workflow')
def complete_workflow(file_paths):
    """
    Chain multiple tasks together
    """
    try:
        # First collect data from all sources
        sources_data = process_all_sources.delay()
        sources_result = sources_data.get(timeout=300)
        
        # Then process each document
        document_tasks = []
        for file_path in file_paths:
            # Determine document type from file extension
            if file_path.endswith('.docx'):
                task = process_document.delay('word', file_path)
            elif file_path.endswith('.xlsx'):
                task = process_document.delay('excel', file_path)
            elif file_path.endswith('.pdf'):
                task = process_document.delay('pdf', file_path)
            document_tasks.append(task)
        
        # Collect all document processing results
        document_results = [task.get(timeout=300) for task in document_tasks]
        
        return {
            "status": "Success",
            "sources_data": sources_result,
            "processed_documents": document_results
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}

if __name__ == '__main__':
    # Example usage
    file_paths = [
        'document1.docx',
        'spreadsheet.xlsx',
        'document.pdf'
    ]
    
    # Start a complete workflow
    workflow = complete_workflow.delay(file_paths)
    
    # Get the results (with timeout)
    try:
        result = workflow.get(timeout=600)  # 10 minutes timeout
        print("Workflow completed:", result)
    except Exception as e:
        print("Error in workflow:", str(e)) 