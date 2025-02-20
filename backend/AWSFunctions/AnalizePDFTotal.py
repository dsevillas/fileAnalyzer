import boto3
import os
import PyPDF2

# Create a Textract client object
textract = boto3.client('textract')

# Load the image file into memory
# with open('/Users/sergio/Documents/School/fileAnalyzer/backend/AWSFunctions/factura.png', 'rb') as file:
#    image_data = file.read()
my_id = "1-1124-0589"
labels = [{"Query": "What is the total", "Text": "Total"},
          {"Query": "What is the date", "Text": "Date"},
          {"Query": "Whats is the cedula juridica or NIF", "Text": "NIF"},
          {"Query": "How much is on taxes or tributos or tributo", "Text": "Taxes"},
          {"Query": "What is the address or direccion", "Text": "Address"},
          {"Query": "What is the name", "Text": "Nombre"}]
labelsr = [
    {"Query": "Whats is the cedula juridica or NIF", "Text": "Address"}]
options = []
for label in labels:
    options.append({"Text": label["Query"], "Alias": label["Text"]+"Alias"})

print(options)
document_name = '/Users/sergio/Documents/School/fileAnalyzer/backend/AWSFunctions/factura.png'
# Open the file and read its contents
with open(document_name, 'rb') as document:
    # Call Amazon Textract to extract the text from the file
    response = textract.analyze_document(Document={'Bytes': document.read()}, FeatureTypes=[
                                         'QUERIES'], QueriesConfig={"Queries": options})
field_name = 'TOTAL'

# Search for the field you want to extract
total_value = 0
total_index = 0
return_str = "Entrante"

print(response['Blocks'])
for item in response['Blocks']:
    try:
        # print(item)

        if item['BlockType'] == 'QUERY_RESULT':

            # Get the value of the field
            # print(f"{field_name}' found")
            # print(f"{item}'")
            for sub_item in item:
                if sub_item == 'Text':
                    total_value = item.get('Text')
                    if item.get('Text') == my_id:
                        return_str = "Saliente"
                    print(
                        f"El {labels[total_index]['Text']} de esta factura es : {item.get('Text')}")

            # print(f"{response['Blocks'][total_index]}'")
            # total_value = item['Geometry']['BoundingBox']
            # break
            total_index = total_index+1
    except KeyError:
        print(f"{field_name}'s age is unknown.")


# Print the value of the field

print(return_str)
