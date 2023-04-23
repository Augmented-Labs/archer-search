import requests
import json


def test_endpoint():
    linkedins = [
        ""http://www.linkedin.com/in / brad-bjelke-80579a3",
        ""http://www.linkedin.com/in / ryan-gellert-2a36086",
        ""http://www.linkedin.com/in / trip-brock-b441653",
        ""http://www.linkedin.com/in / davidjkennedy",
        ""http://www.linkedin.com/in / joaquin-quintas",
        ""http://www.linkedin.com/in / angie-klein-501a4",
        ""http://www.linkedin.com/in / gurushyam",
        ""http://www.linkedin.com/in / randall-k-davis",
        ""http://www.linkedin.com/in / alexeck",
        ""http://www.linkedin.com/in / bryanchristiansen",
        ""http://www.linkedin.com/in / ericpliner",
        ""http://www.linkedin.com/in / larry-williamson-754a7368",
        ""http://www.linkedin.com/in / sunel53",
        ""http://www.linkedin.com/in / markgershburg",
        ""http://www.linkedin.com/in / eric-peterman-89b91a6",
        ""http://www.linkedin.com/in / ron-calhoun-905b59139",
        ""http://www.linkedin.com/in / vishal-kapoor-ceng",
        ""http://www.linkedin.com/in / tonicunningham",
        ""http://www.linkedin.com/in / robertkarlseng",
        ""http://www.linkedin.com/in / racardozo",
        ""http://www.linkedin.com/in / runenterprises",
        ""http://www.linkedin.com/in / jim-harrington-09777310",
        ""http://www.linkedin.com/in / vincentramelli",
        ""http://www.linkedin.com/in / yasserbashir",
        ""http://www.linkedin.com/in / seth-morgan-5b878a1",
        ""http://www.linkedin.com/in / ankurgopal",
        ""http://www.linkedin.com/in / john-tallent-44a85a8",
        ""http://www.linkedin.com/in / steve-schinhofen-84a24423",
        ""http://www.linkedin.com/in / hashim-zaibak-82a6473a",
        ""http://www.linkedin.com/in / simeon-george-b2707985",
        ""http://www.linkedin.com/in / bostonpads",
        ""http://www.linkedin.com/in / nehaparikh",
        ""http://www.linkedin.com/in / joepelayo",
        ""http://www.linkedin.com/in / michael-buckley-ab060011",
        ""http://www.linkedin.com/in / maziar-minovi-5a008818",
        ""http://www.linkedin.com/in / douglasjwatts",
        ""http://www.linkedin.com/in / john-ambrose-432b6410",
        ""http://www.linkedin.com/in / pafournier",
        ""http://www.linkedin.com/in / alltite",
        ""http://www.linkedin.com/in / etropper",
        ""http://www.linkedin.com/in / toby-mulligan-jd-2a91bb4",
        ""http://www.linkedin.com/in / robert-caruso-23b6a896",
        ""http://www.linkedin.com/in / bryanmurphy2",
        ""http://www.linkedin.com/in / dale-dodson-b3029a11",
        ""http://www.linkedin.com/in / tainabrack",
        ""http://www.linkedin.com/in / holmen",
    ]

    output_list = []
    for i in linkedins:
        try:
            output_list.append({"data": get_data_from_endpoint(i), "url": i})
        except Exception as e:
            output_list.append({'error_linkedin_url': i})
            raise e
    w = {'output': output_list}
    with open('myfile.txt', mode='w') as f:
        # Write the data to the file.
        f.write(json.dumps(w))


def get_data_from_endpoint(url):
    """
    Retrieves data from the specified endpoint URL.

    Args:
        endpoint_url (str): The URL of the endpoint to retrieve data from.

    Returns:
        list: A list of data retrieved from the endpoint.
    """
    try:
        response = requests.post('"http://127.0.0.1:8000/relevancy',
                                 json={'linkedin_url': url, 'problem': 'svb'})

        # If the request was successful, add the data to the list.
        if response.status_code == 200:
            return response.json()
        else:
            # Print the error message if the request was not successful.
            print(f"Error {response.status_code}: {response.content}")
            return None
    except Exception as e:
        # Print the exception if an error occurred.
        print(f"Error: {e}")
        return None


test_endpoint()
