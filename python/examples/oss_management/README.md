# OSS Management Example

This example demonstrates how to use the OSS management features of the Wuying AgentBay SDK. It covers:

- Initializing the AgentBay client
- Setting up OSS environment
- Uploading files to OSS
- Uploading files anonymously
- Downloading files from OSS
- Downloading files anonymously
- Cleaning up sessions

This example is useful for understanding how to interact with OSS services in the AgentBay cloud environment.

---

## Prerequisites

- Python 3.12 or later
- Wuying AgentBay SDK installed:
  ```bash
  pip install wuying-agentbay-sdk
  ```

## Running the Example

```bash
cd oss_management
python main.py
```

Make sure you have set the `AGENTBAY_API_KEY` , `OSS_ACCESS_KEY_ID`, `OSS_ACCESS_KEY_SECRET`, `OSS_SECURITY_TOKEN`, `OSS_ENDPOINT`, `OSS_REGION`, `OSS_TEST_UPLOAD_URL`, `OSS_TEST_DOWNLOAD_URL` environment variable or replace the placeholder in the code with your actual API key.