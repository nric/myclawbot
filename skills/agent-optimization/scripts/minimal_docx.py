#!/usr/bin/env python3
"""
Minimal DOCX generator without external dependencies
DOCX is a ZIP file with XML content
"""

import zipfile
import io
from datetime import datetime

def create_minimal_docx(title, author, date, content_paragraphs, output_path):
    """Create a minimal valid DOCX file"""
    
    # Create a BytesIO buffer for the ZIP
    buffer = io.BytesIO()
    
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        # [Content_Types].xml
        content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>'''
        zf.writestr('[Content_Types].xml', content_types)
        
        # _rels/.rels
        rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''
        zf.writestr('_rels/.rels', rels)
        
        # word/_rels/document.xml.rels
        doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>'''
        zf.writestr('word/_rels/document.xml.rels', doc_rels)
        
        # Build document.xml content
        body_content = []
        
        # Title
        body_content.append(f'<w:p><w:pPr><w:pStyle w:val="Title"/></w:pPr><w:r><w:t>{escape_xml(title)}</w:t></w:r></w:p>')
        
        # Author and date
        body_content.append(f'<w:p><w:pPr><w:pStyle w:val="Subtitle"/></w:pPr><w:r><w:rPr><w:b/></w:rPr><w:t>von {escape_xml(author)}</w:t></w:r></w:p>')
        body_content.append(f'<w:p><w:pPr><w:pStyle w:val="Subtitle"/></w:pPr><w:r><w:t>Reflexion vom {escape_xml(date)}</w:t></w:r></w:p>')
        body_content.append('<w:p><w:r><w:t></w:t></w:r></w:p>')  # Empty line
        
        # Content paragraphs
        for para in content_paragraphs:
            if para.strip():
                body_content.append(f'<w:p><w:pPr><w:pStyle w:val="Normal"/></w:pPr><w:r><w:t>{escape_xml(para.strip())}</w:t></w:r></w:p>')
        
        # Footer
        body_content.append('<w:p><w:r><w:t></w:t></w:r></w:p>')
        body_content.append(f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:t>—</w:t></w:r></w:p>')
        body_content.append(f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:t>Philosophische Bibliothek 100 | Tägliche Reflexion</w:t></w:r></w:p>')
        
        # word/document.xml
        document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:body>
        {''.join(body_content)}
    </w:body>
</w:document>'''
        zf.writestr('word/document.xml', document_xml)
    
    # Write to file
    with open(output_path, 'wb') as f:
        f.write(buffer.getvalue())
    
    print(f"✓ DOCX erstellt: {output_path}")
    return True

def escape_xml(text):
    """Escape XML special characters"""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 5:
        print("Usage: python minimal_docx.py 'Title' 'Author' 'Date' 'Content' output.docx")
        sys.exit(1)
    
    title = sys.argv[1]
    author = sys.argv[2]
    date = sys.argv[3]
    content = sys.argv[4]
    output = sys.argv[5]
    
    paragraphs = content.split('\n\n')
    create_minimal_docx(title, author, date, paragraphs, output)
