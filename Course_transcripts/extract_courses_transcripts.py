import os
import zipfile
import re
from pathlib import Path
from urllib.parse import unquote 

def extract_raw_text_from_srt(content):
    lines = content.splitlines()
    raw_text = []
    for line in lines:
        line = line.strip()
        if re.match(r"^\d+$", line):
            continue
        if re.match(r"\d{2}:\d{2}:\d{2},\d{3} -->", line):
            continue
        if line == "":
            continue
        raw_text.append(line)
    return " ".join(raw_text)

def clean_title(text):
    # Decode URL encoding and replace underscores/dashes
    title = unquote(Path(text).stem)
    title = title.replace("_", " ").replace("-", " ").strip()
    return title.title()

def process_english_transcripts(zip_folder_path, output_md_file='english_course_notes.md'):
    section_zips = sorted([f for f in os.listdir(zip_folder_path) if f.endswith('.zip')])

    with open(output_md_file, 'w', encoding='utf-8') as out:
        out.write("# 📘 English Course Notes (Lang En Vs Only)\n\n")

        for section_index, zip_filename in enumerate(section_zips, start=1):
            section_path = os.path.join(zip_folder_path, zip_filename)
            section_name = clean_title(zip_filename)
            out.write(f"# 🗂️ Section {section_index}: {section_name}\n\n")

            with zipfile.ZipFile(section_path, 'r') as zip_ref:
                srt_files = sorted([
                    f for f in zip_ref.namelist()
                    if f.endswith('.srt') and "lang_en_vs" in f
                ])

                for lesson_index, srt_file in enumerate(srt_files, start=1):
                    srt_data = zip_ref.read(srt_file).decode('utf-8', errors='ignore')
                    lesson_name = clean_title(srt_file)
                    raw_text = extract_raw_text_from_srt(srt_data)

                    out.write(f"## 📖 Lesson {lesson_index}: {lesson_name}\n\n")
                    out.write(f"{raw_text}\n\n")

    print(f"✅ Cleaned English-only Markdown notes created: {output_md_file}")

zip_folder = "Course_notes/"
process_english_transcripts(zip_folder)
