# https://api.qualtrics.com/5e86e383167d5-getting-survey-responses-via-the-new-export-ap-is
import io
import os
import re
import sys
import zipfile
import requests
from dotenv import load_dotenv


def exportSurvey(apiToken, surveyId, dataCenter, fileFormat):
    surveyId = surveyId
    fileFormat = fileFormat
    dataCenter = dataCenter

    # Setting static parameters
    requestCheckProgress = 0.0
    progressStatus = "inProgress"
    baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(dataCenter, surveyId)
    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
    }

    # Step 1: Creating Data Export
    downloadRequestUrl = baseUrl
    downloadRequestPayload = '{"format":"' + fileFormat + '"}'
    downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
    progressId = downloadRequestResponse.json()["result"]["progressId"]
    print(downloadRequestResponse.text)

    # Step 2: Checking on Data Export Progress and waiting until export is ready
    while progressStatus != "complete" and progressStatus != "failed":
        print("progressStatus=", progressStatus)
        requestCheckUrl = baseUrl + progressId
        requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
        requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
        print("Download is " + str(requestCheckProgress) + " complete")
        progressStatus = requestCheckResponse.json()["result"]["status"]

    # step 2.1: Check for error
    if progressStatus == "failed":
        raise Exception("export failed")

    fileId = requestCheckResponse.json()["result"]["fileId"]

    # Step 3: Downloading file
    requestDownloadUrl = baseUrl + fileId + '/file'
    requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

    # Step 4: Unzipping the file
    zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall("MyQualtricsDownload")
    print('Complete')


def main():
    try:
        # Get env vars from .env
        load_dotenv()
        apiToken = os.getenv('APIKEY')
        dataCenter = os.getenv('DATACENTER')
    except KeyError:
        print("set environment variables APIKEY and DATACENTER")
        sys.exit(2)

    # Set export file format
    fileFormat = "csv"

    # Read survey ids
    post_surveys = {}
    with open('.env', 'r') as file:
        for line in file:
            line = line.strip()  # remove whitespaces
            if line.startswith('P'):  # if not line break or comment
                survey_name, survey_id = line.split('=', 1)  # split key and value

                # Check servey id format
                regex = re.compile('^SV_.*')
                match = regex.match(survey_id)
                if not match:
                    print(f"survey Id must match ^SV_.*: {survey_name}={survey_id}")
                    sys.exit(2)
                post_surveys[survey_name] = survey_id

    # Export post surveys
    for surveyName, surveyId in post_surveys.items():
        print(f'{surveyName}: {surveyId}')
        exportSurvey(apiToken, surveyId, dataCenter, fileFormat)


if __name__ == "__main__":
    main()
