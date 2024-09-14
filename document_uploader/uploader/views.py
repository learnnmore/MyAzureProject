# uploader/views.py
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# Allowed file types (PDF, DOC, DOCX)
ALLOWED_FILE_TYPES = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']

# def document_upload(request):
#     if request.method == 'POST':
#         # Get the uploaded file and metadata
#         uploaded_file = request.FILES.get('document')
#         document_type = request.POST.get('document_type')
#         tags = request.POST.get('tags')
#         user_id = request.POST.get('user_id')
#
#         # Validate the file type
#         if uploaded_file and uploaded_file.content_type not in ALLOWED_FILE_TYPES:
#             return render(request, 'uploader/upload.html', {
#                 'error_message': 'Invalid file type. Please upload a PDF or Word document.'
#             })
#
#         # Save the file if valid
#         if uploaded_file:
#             fs = FileSystemStorage()
#             filename = fs.save(uploaded_file.name, uploaded_file)
#             file_url = fs.url(filename)
#
#             # Success message
#             return render(request, 'uploader/upload.html', {
#                 'success_message': f'File uploaded successfully! File URL: {file_url}'
#             })
#
#     # Default return (GET request)
#     return render(request, 'uploader/upload.html')

# uploader/views.py
# from django.shortcuts import render
# from .azure_blob_service import AzureBlobService
#
# # Allowed file types (PDF, DOC, DOCX)
# #ALLOWED_FILE_TYPES = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
#
# def document_upload(request):
#     if request.method == 'POST':
#         # Get the uploaded file and metadata
#         uploaded_file = request.FILES.get('document')
#         document_type = request.POST.get('document_type')
#         tags = request.POST.get('tags')
#         user_id = request.POST.get('user_id')
#
#         # Validate the file type
#         if uploaded_file and uploaded_file.content_type not in ALLOWED_FILE_TYPES:
#             return render(request, 'uploader/upload.html', {
#                 'error_message': 'Invalid file type. Please upload a PDF or Word document.'
#             })
#
#         # Upload the file to Azure Blob Storage if valid
#         if uploaded_file:
#             azure_service = AzureBlobService()
#             file_name = uploaded_file.name  # You can modify the name as needed (e.g., add a timestamp or user ID)
#             file_url = azure_service.upload_file(uploaded_file, file_name)
#
#             # If upload is successful, return the file URL
#             if file_url:
#                 return render(request, 'uploader/upload.html', {
#                     'success_message': f'File uploaded successfully! File URL: {file_url}'
#                 })
#             else:
#                 return render(request, 'uploader/upload.html', {
#                     'error_message': 'Failed to upload the file to Azure.'
#                 })
#
#     # Default return (GET request)
#     return render(request, 'uploader/upload.html')


# uploader/views.py
from django.shortcuts import render
from .azure_blob_service import AzureBlobService
from .cosmos_service import CosmosDBService
#
# # Allowed file types (PDF, DOC, DOCX)
# #ALLOWED_FILE_TYPES = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
#
# def document_upload(request):
#     if request.method == 'POST':
#         # Get the uploaded file and metadata
#         uploaded_file = request.FILES.get('document')
#         document_type = request.POST.get('document_type')
#         tags = request.POST.get('tags')
#         user_id = request.POST.get('user_id')
#
#         # Validate the file type
#         if uploaded_file and uploaded_file.content_type not in ALLOWED_FILE_TYPES:
#             return render(request, 'uploader/upload.html', {
#                 'error_message': 'Invalid file type. Please upload a PDF or Word document.'
#             })
#
#         # Upload the file to Azure Blob Storage if valid
#         if uploaded_file:
#             azure_service = AzureBlobService()
#             file_name = uploaded_file.name  # You can modify the name as needed (e.g., add a timestamp or user ID)
#             file_url = azure_service.upload_file(uploaded_file, file_name)
#
#             # If upload is successful, store metadata in Azure Cosmos DB
#             if file_url:
#                 # Metadata to store
#                 metadata = {
#                     'file_name': file_name,
#                     'file_url': file_url,
#                     'document_type': document_type,
#                     'tags': tags.split(','),
#                     'user_id': user_id,
#                     'upload_date': None,  # This will be added by the CosmosDBService
#                 }
#
#                 # Store metadata in Cosmos DB
#                 cosmos_service = CosmosDBService()
#                 cosmos_service.store_metadata(metadata)
#
#                 # Render success message with file URL
#                 return render(request, 'uploader/upload.html', {
#                     'success_message': f'File uploaded successfully! File URL: {file_url}'
#                 })
#             else:
#                 return render(request, 'uploader/upload.html', {
#                     'error_message': 'Failed to upload the file to Azure.'
#                 })
#
#     # Default return (GET request)
#     return render(request, 'uploader/upload.html')




# uploader/views.py
def document_upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('document')
        document_type = request.POST.get('document_type')
        tags = request.POST.get('tags')
        user_id = request.POST.get('user_id')

        # Validate the file type
        if uploaded_file and uploaded_file.content_type not in ALLOWED_FILE_TYPES:
            return render(request, 'uploader/upload.html', {
                'error_message': 'Invalid file type. Please upload a PDF or Word document.'
            })

        if uploaded_file:
            azure_service = AzureBlobService()
            file_name = uploaded_file.name
            file_url = azure_service.upload_file(uploaded_file, file_name)

            if file_url:
                metadata = {
                    'file_name': file_name,
                    'file_url': file_url,
                    'document_type': document_type,
                    'tags': tags.split(','),
                    'user_id': user_id,
                    'upload_date': None
                }

                cosmos_service = CosmosDBService()
                cosmos_service.store_metadata(metadata)

                return render(request, 'uploader/upload.html', {
                    'success_message': f'File uploaded successfully! File URL: {file_url}'
                })
            else:
                return render(request, 'uploader/upload.html', {
                    'error_message': 'Failed to upload the file to Azure.'
                })

    return render(request, 'uploader/upload.html')


import requests
from django.conf import settings
from django.shortcuts import render

def generate_expiring_url(document_reference, expiration_in_minutes=60):
    """
    Calls Azure Function to generate a unique download URL with an expiration date.
    :param document_reference: The reference (name) of the document in Blob Storage.
    :param expiration_in_minutes: Expiration time in minutes.
    :return: The generated download URL if successful, or None.
    """
    try:
        function_url = 'https://<your-function-app-name>.azurewebsites.net/api/expiring_url_function'
        params = {
            'document_reference': document_reference,
            'expiration_in_minutes': expiration_in_minutes
        }
        response = requests.get(function_url, params=params)

        if response.status_code == 200:
            return response.json().get('download_url')
        else:
            print(f"Failed to generate expiring URL: {response.text}")
            return None
    except Exception as e:
        print(f"Error generating expiring URL: {str(e)}")
        return None

# def document_download(request, document_reference):
#     expiration_in_minutes = request.GET.get('expiration_in_minutes', 60)
#     download_url = generate_expiring_url(document_reference, int(expiration_in_minutes))
#
#     if download_url:
#         return render(request, 'uploader/download.html', {
#             'download_url': download_url
#         })
#     else:
#         return render(request, 'uploader/download.html', {
#             'error_message': 'Failed to generate download URL.'
#         })


from django.shortcuts import render
from django.http import JsonResponse
from .tasks import generate_and_store_url


def document_download(request, document_reference):
    expiration_in_minutes = int(request.GET.get('expiration_in_minutes', 60))

    # Trigger the Celery task
    task = generate_and_store_url.delay(document_reference, expiration_in_minutes)

    # Optionally: wait for the task to complete and return the URL
    # In production, you may want to use a frontend polling mechanism or a task result store
    download_url = task.get(timeout=10)  # Wait up to 10 seconds for the result

    if download_url:
        return render(request, 'uploader/download.html', {'download_url': download_url})
    else:
        return render(request, 'uploader/download.html', {'error_message': 'Failed to generate download URL.'})

