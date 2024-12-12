import fitz  # PyMuPDF
import cv2
import pytesseract
import numpy as np
import json
import re
import os

class PDFTableExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pages = []
        self.tables = []

    def load_pdf(self):
        """
        Load PDF using pymupdf and render pages to images.
        """
        try:
            doc = fitz.open(self.pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                img_data = pix.tobytes()
                img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
                self.pages.append(img)
            print(f"Loaded {len(self.pages)} pages from PDF.")
        except Exception as e:
            print(f"Error loading PDF: {e}")

    def process_pages(self):
        """
        Process each page to detect and extract tables.
        """
        for idx, img in enumerate(self.pages):
            print(f"Processing page {idx + 1}/{len(self.pages)}...")
            tables = self.detect_tables(img)
            print(f"Found {len(tables)} tables on page {idx + 1}.")
            for table_idx, table in enumerate(tables):
                # Extract table data
                table_data = self.extract_table_data(table)
                self.tables.append({
                    "page": idx + 1,
                    "table_index": table_idx + 1,
                    "data": table_data
                })

    def detect_tables(self, img):
        """
        Detect tables in an image using OpenCV.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(~gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,-2)
        # Detect horizontal and vertical lines
        horizontal = thresh.copy()
        vertical = thresh.copy()

        # Horizontal lines
        h_scale = 15  # Adjust this value for your images
        h_size = int(horizontal.shape[1]/h_scale)
        h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (h_size,1))
        horizontal = cv2.erode(horizontal, h_kernel, iterations=1)
        horizontal = cv2.dilate(horizontal, h_kernel, iterations=1)

        # Vertical lines
        v_scale = 15  # Adjust this value for your images
        v_size = int(vertical.shape[0]/v_scale)
        v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,v_size))
        vertical = cv2.erode(vertical, v_kernel, iterations=1)
        vertical = cv2.dilate(vertical, v_kernel, iterations=1)

        # Combine horizontal and vertical lines
        mask = horizontal + vertical

        # Find contours of tables
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        tables = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # Filter out small contours that are unlikely to be tables
            if w > 50 and h > 50:
                table_img = img[y:y+h, x:x+w]
                tables.append((x, y, w, h, table_img))
        return tables

    def extract_table_data(self, table_info):
        """
        Extract data from a detected table image.
        """
        x, y, w, h, table_img = table_info
        # Preprocess table image
        gray = cv2.cvtColor(table_img, cv2.COLOR_BGR2GRAY)
        # Thresholding
        thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # Invert image
        thresh = 255 - thresh
        # Find contours (cells)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Build a list of cell bounding boxes
        cells = []
        for cnt in contours:
            x_cell, y_cell, w_cell, h_cell = cv2.boundingRect(cnt)
            # Filter cells by size (eliminate noise)
            if w_cell > 20 and h_cell > 20 and w_cell < w and h_cell < h:
                cells.append((x_cell, y_cell, w_cell, h_cell))
        # Remove duplicates and sort cells
        cells = list(set(cells))
        cells = sorted(cells, key=lambda b: (b[1], b[0]))
        # Group cells into rows
        rows = self.group_cells_into_rows(cells)
        # Extract text from each cell
        table_data = []
        for row in rows:
            row_data = []
            for cell in row:
                x_cell, y_cell, w_cell, h_cell = cell
                # Extract cell image
                cell_img = table_img[y_cell:y_cell+h_cell, x_cell:x_cell+w_cell]
                # OCR the cell image
                text = self.ocr_cell(cell_img)
                row_data.append(text)
            table_data.append(row_data)
        return table_data

    def group_cells_into_rows(self, cells):
        """
        Group cells into rows based on their vertical positions.
        """
        rows = []
        current_row = []
        current_y = -1
        for cell in cells:
            x, y, w, h = cell
            if current_y == -1:
                current_y = y
            if abs(y - current_y) < h / 2:
                current_row.append(cell)
            else:
                # Sort current row cells by x coordinate
                current_row = sorted(current_row, key=lambda b: b[0])
                rows.append(current_row)
                current_row = [cell]
                current_y = y
        if current_row:
            current_row = sorted(current_row, key=lambda b: b[0])
            rows.append(current_row)
        return rows

    def ocr_cell(self, cell_img):
        """
        Perform OCR on a cell image, handling rotated text.
        """
        # Resize image for better OCR accuracy
        cell_img = cv2.resize(cell_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        # Convert to grayscale
        gray = cv2.cvtColor(cell_img, cv2.COLOR_BGR2GRAY)
        # Thresholding
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # Detect orientation
        try:
            osd = pytesseract.image_to_osd(thresh)
            angle = int(re.search('(?<=Rotate: )\d+', osd).group(0))
            script = re.search('(?<=Script: )\w+', osd).group(0)
        except:
            angle = 0
            script = 'Unknown'
        if angle != 0:
            # Rotate image to correct orientation
            thresh = self.rotate_image(thresh, angle)
        # OCR
        config = '--psm 6'  # Assume a single uniform block of text
        text = pytesseract.image_to_string(thresh, config=config)
        return text.strip()

    def rotate_image(self, image, angle):
        """
        Rotate image by the given angle.
        """
        angle = 360 - angle  # Adjust angle for OpenCV rotation
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    def output_as_json(self):
        """
        Convert extracted table data to JSON.
        """
        return json.dumps(self.tables, indent=2)

    def run(self):
        """
        Run the extraction process and return JSON data.
        """
        self.load_pdf()
        if not self.pages:
            print("No pages to process.")
            return None
        self.process_pages()
        return self.output_as_json()
