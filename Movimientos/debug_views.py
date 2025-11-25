from django.http import HttpResponse
import os
from django.conf import settings

def debug_paths(request):
    base_dir = settings.BASE_DIR
    templates_dir = os.path.join(base_dir, "templates")
    files_in_templates = os.listdir(templates_dir) if os.path.exists(templates_dir) else "Templates directory not found"
    return HttpResponse(f"""
    <h2>Debug Paths</h2>
    <p>BASE_DIR: {base_dir}</p>
    <p>Templates Dir: {templates_dir}</p>
    <p>Files in templates dir: {files_in_templates}</p>
    """)
