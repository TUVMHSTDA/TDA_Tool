import pymupdf
import re
import os

# Function to extract all plain text and text in tables from pdf/word documents
def pdf_extract_text(input_file):

    pages_text = []
    
    for page_num in range(len(input_file)):

        pages_text.append(f"\n--------Page:{page_num + 1} of {len(input_file)}--------\n")

        page = input_file.load_page(page_num)

        # Only extract pdf content outside of headers and footers
        page_rect = page.rect  # Get page dimensions
        page_width = page_rect.width
        page_height = page_rect.height


        header_height = 50
        footer_height = 55

        content_area = pymupdf.Rect(0, header_height, page_width, page_height - footer_height)

        text = page.get_text("text", clip=content_area)

        # Remove all non printable characters except for \n
        text = re.sub(r'[^\x20-\x7E\n\xA0-\xFF]', '', text, flags=re.DOTALL)
        

        pages_text.append(text)

        # Find and extract data from tables
        table = page.find_tables()

        if table.tables:

            headers = table[0].extract()[0]
            data = table[0].extract()[1: ]


            if table is not None:
                pages_text.append(f"-----------\nTable\n-----------\n")

            for idx, row in enumerate(data):
                if all(cell is not None for cell in row):
                    idx += 1
                    pages_text.append(f"\n---------\nRow {idx}\n---------")

                    for header, value in zip(headers, row):
                        pages_text.append(str(f"\n{header}: \n{value}\n"))
                else:
                    pages_text.append("Unable to retrieve table contents.\n")
                      

    return pages_text

                

# Function to write extracted data to text
def write_to_file(output_file, pages_text):
    
    with open(output_file, 'w', encoding="utf-8") as file:
        for text in pages_text:
            file.write(text)


    file.close()
    

# list parameter - loops through list of paths
def extract_txt_list(pathlist):
    
    for i in range(0, len(pathlist), 1):
        if pathlist[i].endswith(".pdf") or pathlist[i].endswith(".docx"):
            input_file = pymupdf.open(pathlist[i])
            output_file = f"extracted_output{i}.txt"


            pages_text = pdf_extract_text(input_file)
            print(f"extracted_output{i}.txt extracted")

            write_to_file(output_file, pages_text)
                        





if __name__ == "__main__":
    files = ["C:/Users/chin-yu/Desktop/research/AI_MDA0315_TDAR/Project 3/107250_MED_T_09.64_mylife Software_final.pdf",
             "C:/Users/chin-yu/Desktop/research/AI_MDA0315_TDAR/Project 3/11202_MED_T_09.28_DR_mylife Software_v3_final.pdf"
             ]
    extract_txt_list(files)


# ========= NOTES =========
# main() --> main(list)
# main() now takes in list, outputs as multiple txt files
# directory can be changed later


