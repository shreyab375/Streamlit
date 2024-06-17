# Import Packages
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from PIL import Image
import os

# Function to load images and their captions from a directory
def load_images_and_captions(directory):
    images = []
    captions = []
    # List all files in the directory
    files = os.listdir(directory)
    # Filter out only image files (assuming they have .jpg extension)
    image_files = [f for f in files if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]
    # Sort image files by filename if necessary
    image_files.sort()

    for img_file in image_files:
        images.append(os.path.join(directory, img_file))
        captions.append(f' {img_file}')

    return images, captions

# Directory where images are stored
image_directory = '1954_jpg'

# Load images and captions from the directory
images, captions = load_images_and_captions(image_directory)

# Initialize session state if not already done
if 'img_index' not in st.session_state:
    st.session_state.img_index = 0

if 'page' not in st.session_state:
    st.session_state.page = 1  # Initialize page number

# Navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])

if col1.button('Previous'):
    if st.session_state.img_index > 0:
        st.session_state.img_index -= 1

if col3.button('Next'):
    if st.session_state.img_index < len(images) - 1:
        st.session_state.img_index += 1
        st.session_state.page += 1  # Increment page number for next image

# Display current image and caption
current_img_path = images[st.session_state.img_index]
current_caption = captions[st.session_state.img_index]

image = Image.open(current_img_path)
st.image(image, caption=current_caption, use_column_width=True)

# Function to convert DataFrame to CSV bytes
def convert_df_to_csv_bytes(df):
    return df.to_csv(index=False).encode('utf-8')

# Function to save DataFrame to CSV file with image name
def save_dataframe_as_csv(df, img_path):
    img_name = os.path.splitext(os.path.basename(img_path))[0]
    csv_filename = f"{img_name}_table.csv"
    df.to_csv(csv_filename, index=False)
    st.success(f"Table saved as {csv_filename}")


# Function to create a sample DataFrame (you can replace this with your actual data loading logic)
def create_sample_dataframe(page):
    data = [
        {"Page": f"p00{page+ 1}.jpg", "Date": i, "g.f-1": "", "k-1": "", "g.f-2": "", "k-2": "",
         "g.f-3": "", "k-3": "", "g.f-4": "", "k-4": "", "g.f-5": "", "k-5": "", "g.f-6": "", "k-6": "",
         "g.f-7": "", "k-7": "", "g.f-8": "", "k-8": "", "g.f-9": "", "k-9": "", "g.f-10": "", "k-10": "",
         "g.f-11": "", "k-11": "", "g.f-12": "", "k-12": ""}
        for i in range(1, 32)  # Example: 31 dates
    ]
    return pd.DataFrame(data)

# Sample DataFrame creation based on the current image page
df = create_sample_dataframe(st.session_state.page)

# Display DataFrame
st.subheader("Transcribed Table")

with st.form("Transcribed Table"):
    # Display AgGrid with the DataFrame
    response = AgGrid(df,
                      editable=True,
                      allow_unsafe_jscode=True,
                      theme='balham',
                      height=400,
                      width=800,
                      fit_columns_on_grid_load=True)

    # Submit button
    submit_button = st.form_submit_button("Confirm")

# Display the DataFrame output (for debugging purposes)
st.write(response["data"])

# Save CSV file and set download button when form is submitted
if submit_button:
    # Save CSV file with image name
    save_dataframe_as_csv(response['data'], current_img_path)

    # Download button to save DataFrame as CSV
    csv_bytes = convert_df_to_csv_bytes(response['data'])
    st.download_button(
        label=f"Download {os.path.basename(current_img_path)} Table 🗳️",
        data=csv_bytes,
        file_name=f"{os.path.splitext(os.path.basename(current_img_path))[0]}_table.csv",
        mime="text/csv",
        key='download-csv'
    )