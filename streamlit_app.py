import streamlit as st
import json
from pprint import pformat

from annotated_text import annotated_text
import random
import re

def text2words(text):
    words = re.findall(r'\b\w+\b', text)
    return words

# Function to format JSON content for proper Markdown rendering
def format_json_content(value):
    try:
        # Ensure the value is a string
        if isinstance(value, dict) or isinstance(value, list):
            formatted_string = json.dumps(value, indent=4, ensure_ascii=False)
        else:
            formatted_string = str(value)

        # Convert `\n` to `\n\n` for Markdown paragraph separation
        formatted_string = formatted_string.replace("\n", "\n\n")

        return formatted_string
    except Exception as e:
        return f"Error in formatting: {e}"

def random_light_shorthand_hex():
    r = random.choice(['C', 'D', 'E', 'F'])  # High Red
    g = random.choice(['8', '9', 'A', 'B', 'C', 'D', 'E', 'F'])  # Medium to High Green
    b = random.choice(['8', '9', 'A', 'B', 'C', 'D', 'E', 'F'])  # Medium to High Blue
    return f"#{r}{g}{b}"


def highlightAll(text, spans, types):
    # color = ["#F6B"]
    #### generate a color dictionary based on the set of types
    color_dict = {key: random_light_shorthand_hex() for key in set(types)}
    my_text = []
    current_index = 0
    for spanindex, span in enumerate(spans):
        start = span[0]
        end = span [1]
        # Append the text before the current span
        my_text += {text[current_index:start]}
        # st.text(text[current_index:start])

        # Wrap the highlighted span with the specified color
        ############# need to do this word by word #########
        # st.text ('below is text')
        # st.text(text[start:end])
        words_list = text2words(text[start:end])
        for itemindex, item in enumerate(words_list):
            # st.write(item)
            # if (spanindex == len(spans) - 1) & (itemindex == len(words_list)-1):
            #     my_text += [(item, "", color)]
            if (itemindex == len(words_list)-1):
                my_text += [(item, types[spanindex], color_dict[types[spanindex]])]
            else:
                my_text += [(item, "", color_dict[types[spanindex]])]
            # st.text(my_text)
        # Update the current index
        current_index = end
    
    # Append the remaining text after the last span
    my_text += {text[current_index:-1]}
    # st.write(highlighted_text)
    annotated_text(my_text) 




st.title("Ransomware Incidents Annotation Visualization App")
st.subheader("First, upload an annotation file of a ransomware incident (format: .json)")
# Upload the .json file
uploaded_file = st.file_uploader("Choose a JSON file", type="json")

if uploaded_file is not None:
    # Load the content of the file
    dataall = json.load(uploaded_file)
    st.subheader(f"There are {len(dataall)} incidents")
    user_input = st.number_input("Enter the index of the incident (starting from 0)", min_value=0, step=1, format="%d")
    data = dataall[user_input]
    content = data['content']
    with st.expander(f'Show the whole file:'):
            # Display the formatted and decoded string
            st.markdown(data)
    with st.expander(f'Show the Content of the ransomware incident'):
            # Display the formatted and decoded string
            st.markdown(format_json_content(content))

    #### extract all the annotations and spans ######
    attribute_list = data['attributes']
    type_list = []
    span_list = []
    for index, value in enumerate(attribute_list):
        # print(f"Annotation {index+1}")
        type_list = type_list + value['attribute-types']
        span_list = span_list + value['spans']
    with st.expander(f'Show all the annotations'):
        highlightAll(content, span_list, type_list)
# st.title("🎈 My new app")
# st.write(
#     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# )
