import cv2
import pytesseract
import numpy as np
import pandas as pd

class TableExtractor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        self.gray = None
        self.thresh = None
        self.vertical_lines = None
        self.horizontal_lines = None
        self.table_structure = None
        self.contours = None
        self.rows = []
        self.data = []

    def preprocess_image(self):
        # Load the image
        self.image = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
        # Convert to grayscale
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # Apply binary thresholding
        _, self.thresh = cv2.threshold(self.gray, 150, 255, cv2.THRESH_BINARY_INV)

    def detect_lines(self):
        # Define kernel lengths
        kernel_len_ver = np.array(self.image).shape[1] // 100
        kernel_len_hor = np.array(self.image).shape[0] // 100

        # Create vertical kernel
        ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len_ver))
        # Create horizontal kernel
        hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len_hor, 1))

        # Detect vertical lines
        image_1 = cv2.erode(self.thresh, ver_kernel, iterations=3)
        self.vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)

        # Detect horizontal lines
        image_2 = cv2.erode(self.thresh, hor_kernel, iterations=3)
        self.horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)

    def combine_lines(self):
        self.table_structure = cv2.addWeighted(self.vertical_lines, 0.5, self.horizontal_lines, 0.5, 0.0)
        # Invert the image
        self.table_structure = cv2.bitwise_not(self.table_structure)

    def find_contours(self):
        # Find contours
        contours, hierarchy = cv2.findContours(self.table_structure, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Sort contours top to bottom
        bounding_boxes = [cv2.boundingRect(c) for c in contours]
        (contours, bounding_boxes) = zip(*sorted(zip(contours, bounding_boxes), key=lambda b: b[1][1]))
        self.contours = contours
        self.bounding_boxes = bounding_boxes

    def sort_contours(self):
        margin = 10  # Adjust as necessary
        row = []
        prev_y = -margin * 2

        for c in self.contours:
            x, y, w, h = cv2.boundingRect(c)
            if abs(y - prev_y) > margin and row:
                # Sort cells in the row by x-coordinate
                row = sorted(row, key=lambda b: b[0])
                self.rows.append(row)
                row = []
            row.append((x, y, w, h))
            prev_y = y

        if row:
            row = sorted(row, key=lambda b: b[0])
            self.rows.append(row)

    def extract_cells(self):
        custom_config = r'--oem 3 --psm 6'
        for row in self.rows:
            row_data = []
            for box in row:
                x, y, w, h = box
                cell = self.image[y:y+h, x:x+w]
                # Preprocess cell image if necessary
                cell_gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
                cell_thresh = cv2.threshold(cell_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                # OCR on the cell
                text = pytesseract.image_to_string(cell_thresh, config=custom_config).strip()
                row_data.append(text)
            self.data.append(row_data)

    def extract_table(self):
        self.preprocess_image()
        self.detect_lines()
        self.combine_lines()
        self.find_contours()
        self.sort_contours()
        self.extract_cells()
        return self.data

    def to_dataframe(self):
        df = pd.DataFrame(self.data)
        return df

# # Usage example
# if __name__ == "__main__":
#     extractor = TableExtractor('table_image.png')
#     data = extractor.extract_table()
#     df = extractor.to_dataframe()
#     print(df)
