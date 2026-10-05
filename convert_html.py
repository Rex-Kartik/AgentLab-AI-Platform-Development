import re
import os

def html_to_jsx(html_str):
    # Extract body content
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html_str, re.DOTALL | re.IGNORECASE)
    if not body_match:
        return ""
    content = body_match.group(1)

    # Convert class to className
    content = re.sub(r'\bclass=', 'className=', content)
    # Convert for to htmlFor
    content = re.sub(r'\bfor=', 'htmlFor=', content)
    
    # Close self-closing tags (br, hr, input, img, meta, link)
    for tag in ['br', 'hr', 'input', 'img', 'meta', 'link']:
        content = re.sub(r'(<'+tag+r'\b[^>]*?)(?<!/)>', r'\1 />', content, flags=re.IGNORECASE)
        
    # Convert SVG attributes to camelCase
    svg_attrs = {
        'stroke-width': 'strokeWidth',
        'stroke-linecap': 'strokeLinecap',
        'stroke-linejoin': 'strokeLinejoin',
        'fill-rule': 'fillRule',
        'clip-rule': 'clipRule',
        'stroke-dasharray': 'strokeDasharray',
        'stroke-dashoffset': 'strokeDashoffset'
    }
    for old, new in svg_attrs.items():
        content = content.replace(old, new)

    return content.strip()

def process_file(html_path, tsx_path, component_name):
    if not os.path.exists(html_path):
        print(f"Not found: {html_path}")
        return
        
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    jsx = html_to_jsx(html)
    
    # Wrap in React component
    template = f"""import React from 'react';
import {{ useNavigate }} from 'react-router-dom';

export default function {component_name}() {{
  const navigate = useNavigate();
  return (
    <>
      {{/* Note: You may need to wire up interactive elements like onClick={{() => navigate('/workspace')}} manually */}}
      {jsx}
    </>
  );
}}
"""
    with open(tsx_path, 'w', encoding='utf-8') as f:
        f.write(template)
    print(f"Processed {component_name}")

import glob

base_dir = r"D:\Ai agents\tools_project\stich_designs"
out_dir = r"D:\Ai agents\tools_project\frontend\src\pages"

landing = glob.glob(os.path.join(base_dir, "*Landing Page.html"))
workspace = glob.glob(os.path.join(base_dir, "*Workspace.html"))

if landing:
    process_file(landing[0], os.path.join(out_dir, "LandingPage.tsx"), "LandingPage")
if workspace:
    process_file(workspace[0], os.path.join(out_dir, "WorkspacePage.tsx"), "WorkspacePage")
