from typing import Self
import zipfile
from pathlib import Path
from bs4 import BeautifulSoup
import msgspec
import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from markdownify import markdownify as md
import json

app = FastAPI()

class Section(msgspec.Struct):
    tag_name: str
    title: str
    content: str

    @classmethod
    def from_html(cls, tag_name: str, title: str, raw_content: str) -> Self:
        return cls(tag_name=tag_name, title=title, content=md(raw_content))


def chunk_epub(epub_path):
    sections = []
    temp_dir = "temp_epub"

    # Extract EPUB contents
    with zipfile.ZipFile(epub_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    # Find HTML files (including those in subdirectories)
    html_files = []
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if (
                    file.endswith(".html")
                    or file.endswith(".xhtml")
                    or file.endswith(".htm")
            ):
                html_files.append(os.path.join(root, file))

    for html_file in html_files:
        with open(html_file, "r", encoding="utf-8") as file:
            content = file.read()
            soup = BeautifulSoup(content, "html.parser")

            # Find all headings
            headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

            # todo: add a recursive layer to minimize the size of the chunks
            for heading in headings:
                tag_name = heading.name
                section_title = heading.get_text().strip()
                section_content = ""

                # Get all content until the next heading
                for sibling in heading.find_next_siblings():
                    if sibling.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                        break
                    section_content += str(sibling)

                # todo: need to remove the acknowledgment, About the Author, references, and other non-content sections
                # todo: or more simply - add a layer of removing the first and last few sections that are not content.
                if section_content != "":
                    sections.append(
                        Section.from_html(
                            tag_name=tag_name,
                            title=section_title,
                            raw_content=section_content,
                        )
                    )

    # Clean up temporary files
    shutil.rmtree(temp_dir)

    return sections


# @app.get("/process_epub/")
def process_epub(file_name: str):
    # ROOT_ = Path(os.path.expanduser(file_name)).parent
    # DATA_ = ROOT_ / "data"
    # epub_file_path = DATA_ / file_name
    epub_path = Path(os.path.expanduser(file_name))
    print ("epub_path: ", epub_path)

    if not epub_path.exists() or not epub_path.is_file() or not epub_path.suffix == '.epub':
        raise HTTPException(status_code=404, detail="File not found or not a valid EPUB file")

    try:
        sections = chunk_epub(epub_path)
        # Create the 'data' directory if it does not exist
        os.makedirs('data', exist_ok=True)
        response_content = [{"section_title": section.title, "content": section.content} for section in sections]
        json_file_path = 'data/' + epub_path.stem + '.json'
        with open(json_file_path, 'w') as f:
            json.dump(response_content, f)
        print("Full path of the JSON file:", os.path.abspath(json_file_path))

        # return JSONResponse(content=response_content)
        return json_file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# @app.post("/upload_and_chunk_epub")
# def process_epub(file: UploadFile = File(...)):
#     try:
#         UPLOAD_DIR = Path(__file__).parent / "uploaded_files"
#         UPLOAD_DIR.mkdir(exist_ok=True)

#         # Define the path to save the uploaded file
#         file_path = UPLOAD_DIR / file.filename

#         # Save the uploaded file
#         with file_path.open("wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
#         sections = chunk_epub(file_path)

#         return JSONResponse(
#             content=[{"section_title": section.title, "content": section.content} for section in sections])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    # import uvicorn

    # uvicorn.run(app, host="127.0.0.1", port=8000)
    process_epub("/Users/anjalee/Desktop/git/book-digest/book_to_chunks/data/4hr.epub")
