def clean_html_text(html_text):
    '''
    Takes in html text as string, removes tags and special characters and returns string as a result. 
    '''
    import re
    cleaner = re.compile('(?<=&lt;).*(?=&gt;)|<.*?>|{.*?}|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    clean_text = re.sub(cleaner, ' ', html_text)
    clean_text = clean_text.lower()
    
    # Remove html text before innitial statement 
    statement = "united states securities and exchange commission"
    statement_regex = r'\s+'.join(statement.split())
    pattern = re.compile(statement_regex, re.IGNORECASE)
    match = pattern.search(clean_text)
    if match:
        clean_text = clean_text[match.start():]

    return clean_text


def clean_html_text_files(input_dir, dest_dir):
    '''
    Takes raw 10-q files in input folder, performs text cleaning and writes them to destination folder. 
    '''
    from pathlib import Path 
    for file in input_dir.iterdir():
        if file.suffix == '.html':
            with open(file, 'r', encoding = 'utf-8') as f: 
                    text = f.read()
                    clean_text = clean_html_text(text)
                    file_name = str(file.name).replace('.html', '')
                    with open(f"{dest_dir}/{file_name}.txt", "w", encoding='utf-8') as f:
                            f.write(clean_text)