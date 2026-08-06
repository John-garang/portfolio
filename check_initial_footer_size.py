import subprocess

# Get the previous version of styles.css before our changes
result = subprocess.run(
    ['git', 'show', 'HEAD:templates/static/styles.css'],
    capture_output=True,
    text=True,
    cwd='c:\\Portfolio'
)

if result.returncode == 0:
    content = result.stdout
    
    # Find footer-related font-size declarations
    lines = content.split('\n')
    in_footer_section = False
    footer_context = []
    
    for i, line in enumerate(lines):
        if '.footer' in line and '{' in line:
            in_footer_section = True
            start_idx = i
        
        if in_footer_section:
            footer_context.append(f"{i+1}: {line}")
            
        if in_footer_section and '}' in line and i > start_idx:
            in_footer_section = False
    
    # Print footer section
    print("=== FOOTER SECTION FROM PREVIOUS VERSION ===")
    for line in footer_context[:100]:  # First 100 lines of footer
        print(line)
    
    # Search for font-size in footer context
    print("\n=== FONT-SIZE DECLARATIONS IN FOOTER ===")
    for i, line in enumerate(lines):
        if 'footer' in line.lower() or (in_footer_section and 'font-size' in line):
            if 'font-size' in line:
                print(f"{i+1}: {line}")
else:
    print(f"Error: {result.stderr}")