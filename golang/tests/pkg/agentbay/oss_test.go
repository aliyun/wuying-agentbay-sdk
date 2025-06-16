package agentbay_test

import (
	"fmt"
	"os"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// Helper function to get OSS credentials from environment variables or use defaults
func getOssCredentials(t *testing.T) (string, string, string, string, string) {
	accessKeyId := os.Getenv("OSS_ACCESS_KEY_ID")
	if accessKeyId == "" {
		t.Log("OSS_ACCESS_KEY_ID environment variable not set, using default value")
		accessKeyId = "test-access-key-id"
	}

	accessKeySecret := os.Getenv("OSS_ACCESS_KEY_SECRET")
	if accessKeySecret == "" {
		t.Log("OSS_ACCESS_KEY_SECRET environment variable not set, using default value")
		accessKeySecret = "test-access-key-secret"
	}

	securityToken := os.Getenv("OSS_SECURITY_TOKEN")
	if securityToken == "" {
		t.Log("OSS_SECURITY_TOKEN environment variable not set, using default value")
		securityToken = "test-security-token"
	}

	endpoint := os.Getenv("OSS_ENDPOINT")
	if endpoint == "" {
		t.Log("OSS_ENDPOINT environment variable not set, using default value")
		endpoint = "https://oss-cn-hangzhou.aliyuncs.com"
	}

	region := os.Getenv("OSS_REGION")
	if region == "" {
		t.Log("OSS_REGION environment variable not set, using default value")
		region = "cn-hangzhou"
	}

	return accessKeyId, accessKeySecret, securityToken, endpoint, region
}

func TestOss_EnvInit(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for OSS testing...")
	sessionParams := agentbay.NewCreateSessionParams().WithImageId("code_latest")
	session, err := agentBay.Create(sessionParams)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Log("Session successfully deleted")
		}
	}()

	// Test OSS EnvInit
	if session.Oss != nil {
		// Get OSS credentials from environment variables
		accessKeyId, accessKeySecret, securityToken, endpoint, region := getOssCredentials(t)

		fmt.Println("Initializing OSS environment...")
		result, err := session.Oss.EnvInit(accessKeyId, accessKeySecret, securityToken, endpoint, region)
		t.Logf("EnvInit result: %s, err=%v", result, err)
		if err != nil {
			t.Errorf("OSS environment initialization failed: %v", err)
		} else {
			t.Log("OSS environment initialization successful")

			// Check if response contains "tool not found"
			if containsToolNotFound(result) {
				t.Errorf("Oss.EnvInit returned 'tool not found'")
			}
		}
	} else {
		t.Logf("Note: OSS interface is nil, skipping OSS test")
	}
}

func TestOss_Upload(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for OSS testing...")
	sessionParams := agentbay.NewCreateSessionParams().WithImageId("code_latest")
	session, err := agentBay.Create(sessionParams)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Log("Session successfully deleted")
		}
	}()

	// Test OSS Upload
	if session.Oss != nil {
		// First initialize the OSS environment
		accessKeyId, accessKeySecret, securityToken, endpoint, region := getOssCredentials(t)
		_, err := session.Oss.EnvInit(accessKeyId, accessKeySecret, securityToken, endpoint, region)
		if err != nil {
			t.Fatalf("Failed to initialize OSS environment: %v", err)
		}

		// Create a test file to upload
		testContent := "This is a test file for OSS upload."
		testFilePath := "/tmp/test_oss_upload.txt"
		if session.FileSystem != nil {
			_, err = session.FileSystem.WriteFile(testFilePath, testContent, "overwrite")
			if err != nil {
				t.Fatalf("Failed to create test file for upload: %v", err)
			}
		} else {
			t.Skip("FileSystem interface is nil, skipping upload test")
		}

		fmt.Println("Uploading file to OSS...")
		bucket := os.Getenv("OSS_TEST_BUCKET")
		if bucket == "" {
			bucket = "test-bucket"
		}
		objectKey := "test-object.txt"
		result, err := session.Oss.Upload(bucket, objectKey, testFilePath)
		t.Logf("Upload result: %s, err=%v", result, err)
		if err != nil {
			t.Errorf("OSS upload failed: %v", err)
		} else {
			t.Log("OSS upload successful")

			// Check if response contains "tool not found"
			if containsToolNotFound(result) {
				t.Errorf("Oss.Upload returned 'tool not found'")
			}
		}
	} else {
		t.Logf("Note: OSS interface is nil, skipping OSS test")
	}
}

func TestOss_UploadAnonymous(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for OSS testing...")
	sessionParams := agentbay.NewCreateSessionParams().WithImageId("code_latest")
	session, err := agentBay.Create(sessionParams)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Log("Session successfully deleted")
		}
	}()

	// Test OSS UploadAnonymous
	if session.Oss != nil {
		// Create a test file to upload
		testContent := "This is a test file for OSS anonymous upload."
		testFilePath := "/tmp/test_oss_upload_anon.txt"
		if session.FileSystem != nil {
			_, err = session.FileSystem.WriteFile(testFilePath, testContent, "overwrite")
			if err != nil {
				t.Fatalf("Failed to create test file for anonymous upload: %v", err)
			}
		} else {
			t.Skip("FileSystem interface is nil, skipping anonymous upload test")
		}

		fmt.Println("Uploading file anonymously...")
		uploadUrl := os.Getenv("OSS_TEST_UPLOAD_URL")
		if uploadUrl == "" {
			uploadUrl = "https://example.com/upload"
		}
		result, err := session.Oss.UploadAnonymous(uploadUrl, testFilePath)
		t.Logf("UploadAnonymous result: %s, err=%v", result, err)
		if err != nil {
			t.Errorf("OSS anonymous upload failed: %v", err)
		} else {
			t.Log("OSS anonymous upload successful")

			// Check if response contains "tool not found"
			if containsToolNotFound(result) {
				t.Errorf("Oss.UploadAnonymous returned 'tool not found'")
			}
		}
	} else {
		t.Logf("Note: OSS interface is nil, skipping OSS test")
	}
}

func TestOss_Download(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for OSS testing...")
	sessionParams := agentbay.NewCreateSessionParams().WithImageId("code_latest")
	session, err := agentBay.Create(sessionParams)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Log("Session successfully deleted")
		}
	}()

	// Test OSS Download
	if session.Oss != nil {
		// First initialize the OSS environment
		accessKeyId, accessKeySecret, securityToken, endpoint, region := getOssCredentials(t)
		_, err := session.Oss.EnvInit(accessKeyId, accessKeySecret, securityToken, endpoint, region)
		if err != nil {
			t.Fatalf("Failed to initialize OSS environment: %v", err)
		}

		fmt.Println("Downloading file from OSS...")
		bucket := os.Getenv("OSS_TEST_BUCKET")
		if bucket == "" {
			bucket = "test-bucket"
		}
		objectKey := "test-object.txt"
		downloadPath := "/tmp/test_oss_download.txt"
		result, err := session.Oss.Download(bucket, objectKey, downloadPath)
		t.Logf("Download result: %s, err=%v", result, err)
		if err != nil {
			t.Errorf("OSS download failed: %v", err)
		} else {
			t.Log("OSS download successful")

			// Check if response contains "tool not found"
			if containsToolNotFound(result) {
				t.Errorf("Oss.Download returned 'tool not found'")
			}

			// Verify the downloaded file exists
			if session.FileSystem != nil {
				fileInfo, err := session.FileSystem.GetFileInfo(downloadPath)
				if err != nil {
					t.Errorf("Failed to get info for downloaded file: %v", err)
				} else {
					t.Logf("Downloaded file info: %v", fileInfo)
				}
			}
		}
	} else {
		t.Logf("Note: OSS interface is nil, skipping OSS test")
	}
}

func TestOss_DownloadAnonymous(t *testing.T) {
	// Initialize AgentBay client
	apiKey := getTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session
	fmt.Println("Creating a new session for OSS testing...")
	sessionParams := agentbay.NewCreateSessionParams().WithImageId("code_latest")
	session, err := agentBay.Create(sessionParams)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	t.Logf("Session created with ID: %s", session.SessionID)

	// IMPORTANT: Ensure cleanup of the session after test
	defer func() {
		fmt.Println("Cleaning up: Deleting the session...")
		err := agentBay.Delete(session)
		if err != nil {
			t.Logf("Warning: Error deleting session: %v", err)
		} else {
			t.Log("Session successfully deleted")
		}
	}()

	// Test OSS DownloadAnonymous
	if session.Oss != nil {
		fmt.Println("Downloading file anonymously...")
		downloadUrl := os.Getenv("OSS_TEST_DOWNLOAD_URL")
		if downloadUrl == "" {
			downloadUrl = "https://example.com/download/test-file.txt"
		}
		downloadPath := "/tmp/test_oss_download_anon.txt"
		result, err := session.Oss.DownloadAnonymous(downloadUrl, downloadPath)
		t.Logf("DownloadAnonymous result: %s, err=%v", result, err)
		if err != nil {
			t.Errorf("OSS anonymous download failed: %v", err)
		} else {
			t.Log("OSS anonymous download successful")

			// Check if response contains "tool not found"
			if containsToolNotFound(result) {
				t.Errorf("Oss.DownloadAnonymous returned 'tool not found'")
			}

			// Verify the downloaded file exists
			if session.FileSystem != nil {
				fileInfo, err := session.FileSystem.GetFileInfo(downloadPath)
				if err != nil {
					t.Errorf("Failed to get info for downloaded file: %v", err)
				} else {
					t.Logf("Downloaded file info: %v", fileInfo)
				}
			}
		}
	} else {
		t.Logf("Note: OSS interface is nil, skipping OSS test")
	}
}
