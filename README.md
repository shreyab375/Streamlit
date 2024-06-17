# Image and Table Transcription App

This repository contains a Streamlit app for displaying images from a directory, transcribing data into a table, and saving the transcribed data as CSV files named after the corresponding images. The app allows users to navigate through images, edit table data, and download the data in CSV format.

## Features

- **Image Navigation**: Navigate through images in a specified directory using "Previous" and "Next" buttons.
- **Image Display**: Display the current image with a caption.
- **Data Transcription**: Edit a sample data table corresponding to the current image.
- **Save and Download**: Save the transcribed table as a CSV file with a filename matching the current image and download it.

## Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/shreyab37/Streamlit.git
    cd your-repo-name
    ```

2. **Install Dependencies**:
    Ensure you have Python installed. Then, install the required packages:
    ```sh
    pip install streamlit pandas Pillow streamlit-aggrid
    ```

3. **Prepare the Image Directory**:
    Place your images in a directory named `1954_jpg` in the same folder as the script.

## Usage

Run the Streamlit app:
```sh
streamlit run app.py
```

## Code Explanation

### Import Packages

```python
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from PIL import Image
import os
```

### Load Images and Captions

Function to load images and their captions from a directory:
```python
def load_images_and_captions(directory):
    images = []
    captions = []
    files = os.listdir(directory)
    image_files = [f for f in files if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]
    image_files.sort()

    for img_file in image_files:
        images.append(os.path.join(directory, img_file))
        captions.append(f' {img_file}')

    return images, captions

image_directory = '1954_jpg'
images, captions = load_images_and_captions(image_directory)
```

### Initialize Session State

Initialize session state variables for image index and page number:
```python
if 'img_index' not in st.session_state:
    st.session_state.img_index = 0

if 'page' not in st.session_state:
    st.session_state.page = 1
```

### Navigation Buttons

Buttons to navigate through the images:
```python
col1, col2, col3 = st.columns([1, 2, 1])

if col1.button('Previous'):
    if st.session_state.img_index > 0:
        st.session_state.img_index -= 1

if col3.button('Next'):
    if st.session_state.img_index < len(images) - 1:
        st.session_state.img_index += 1
        st.session_state.page += 1
```

### Display Current Image

Display the current image and its caption:
```python
current_img_path = images[st.session_state.img_index]
current_caption = captions[st.session_state.img_index]

image = Image.open(current_img_path)
st.image(image, caption=current_caption, use_column_width=True)
```

### Convert DataFrame to CSV

Function to convert a DataFrame to CSV bytes:
```python
def convert_df_to_csv_bytes(df):
    return df.to_csv(index=False).encode('utf-8')
```

### Save DataFrame as CSV

Function to save the DataFrame to a CSV file with the image name:
```python
def save_dataframe_as_csv(df, img_path):
    img_name = os.path.splitext(os.path.basename(img_path))[0]
    csv_filename = f"{img_name}_table.csv"
    df.to_csv(csv_filename, index=False)
    st.success(f"Table saved as {csv_filename}")
```

### Create Sample DataFrame

Function to create a sample DataFrame:
```python
def create_sample_dataframe(page):
    data = [
        {"Page": f"p00{page+ 1}.jpg", "Date": i, "g.f-1": "", "k-1": "", "g.f-2": "", "k-2": "",
         "g.f-3": "", "k-3": "", "g.f-4": "", "k-4": "", "g.f-5": "", "k-5": "", "g.f-6": "", "k-6": "",
         "g.f-7": "", "k-7": "", "g.f-8": "", "k-8": "", "g.f-9": "", "k-9": "", "g.f-10": "", "k-10": "",
         "g.f-11": "", "k-11": "", "g.f-12": "", "k-12": ""}
        for i in range(1, 32)
    ]
    return pd.DataFrame(data)

df = create_sample_dataframe(st.session_state.page)
```

### Display DataFrame

Display the transcribed table:
```python
st.subheader("Transcribed Table")

with st.form("Transcribed Table"):
    response = AgGrid(df,
                      editable=True,
                      allow_unsafe_jscode=True,
                      theme='balham',
                      height=400,
                      width=800,
                      fit_columns_on_grid_load=True)

    submit_button = st.form_submit_button("Confirm")
```

### Save and Download CSV

Save the CSV file and display the download button upon form submission:
```python
if submit_button:
    save_dataframe_as_csv(response['data'], current_img_path)

    csv_bytes = convert_df_to_csv_bytes(response['data'])
    st.download_button(
        label=f"Download {os.path.basename(current_img_path)} Table 🗳️",
        data=csv_bytes,
        file_name=f"{os.path.splitext(os.path.basename(current_img_path))[0]}_table.csv",
        mime="text/csv",
        key='download-csv'
    )
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

