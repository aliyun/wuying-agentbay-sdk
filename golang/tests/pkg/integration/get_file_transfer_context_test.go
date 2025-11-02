package integration

import (
	"fmt"
	"os"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// TestGetFileTransferContext tests the file transfer context fix for the Get method
type GetFileTransferContextTestSuite struct {
	agentBay *agentbay.AgentBay
	session  *agentbay.Session
}

func (suite *GetFileTransferContextTestSuite) SetupTest(t *testing.T) {
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set")
	}

	var err error
	suite.agentBay, err = agentbay.NewAgentBay(apiKey)
	require.NoError(t, err, "Failed to create AgentBay client")

	// Create a test session
	params := agentbay.NewCreateSessionParams()
	params.ImageId = "code_latest"
	result, err := suite.agentBay.Create(params)
	require.NoError(t, err, "Failed to create session")
	require.NotNil(t, result.Session, "Session should not be nil")
	suite.session = result.Session
}

func (suite *GetFileTransferContextTestSuite) TearDownTest(t *testing.T) {
	if suite.session != nil {
		_, err := suite.session.Delete()
		if err != nil {
			t.Logf("Warning: Failed to cleanup session %s: %v", suite.session.SessionID, err)
		}
	}
}

// TestGetMethodCreatesFileTransferContext verifies that the Get method creates
// a file transfer context automatically for recovered sessions
func TestGetMethodCreatesFileTransferContext(t *testing.T) {
	suite := &GetFileTransferContextTestSuite{}
	suite.SetupTest(t)
	defer suite.TearDownTest(t)

	// Get the session_id from the test session
	sessionID := suite.session.SessionID

	// Use Get method to recover the session
	getResult, err := suite.agentBay.Get(sessionID)
	require.NoError(t, err, "Get method failed")
	require.NotNil(t, getResult, "Get result should not be nil")
	require.True(t, getResult.Success, "Get method was not successful: %s", getResult.ErrorMessage)
	require.NotNil(t, getResult.Session, "Session should not be nil")
	assert.Equal(t, sessionID, getResult.Session.SessionID, "Session IDs should match")

	// Verify that the recovered session has a file transfer context ID
	recoveredSession := getResult.Session
	assert.NotEmpty(t, recoveredSession.FileTransferContextID,
		"Recovered session should have a non-empty FileTransferContextID")
}

// TestRecoveredSessionCanPerformFileOperations verifies that a session recovered
// via Get method can actually perform file operations
func TestRecoveredSessionCanPerformFileOperations(t *testing.T) {
	suite := &GetFileTransferContextTestSuite{}
	suite.SetupTest(t)
	defer suite.TearDownTest(t)

	// Get the session_id from the test session
	sessionID := suite.session.SessionID

	// Wait a bit for session to be fully ready
	time.Sleep(5 * time.Second)

	// Use Get method to recover the session
	getResult, err := suite.agentBay.Get(sessionID)
	require.NoError(t, err, "Get method failed")
	require.NotNil(t, getResult, "Get result should not be nil")
	require.True(t, getResult.Success, "Get method was not successful: %s", getResult.ErrorMessage)

	recoveredSession := getResult.Session

	// Create a test file to upload
	testContent := fmt.Sprintf("Test content at %d", time.Now().Unix())
	testFilename := fmt.Sprintf("test_file_%d.txt", time.Now().Unix())
	testPath := fmt.Sprintf("/tmp/%s", testFilename)

	// Try to write the file using file_system operations
	// This should work if file transfer context is properly set up
	// Note: WriteFile in Golang requires a third parameter for write mode ("overwrite" or "append")
	writeResult, err := recoveredSession.FileSystem.WriteFile(testPath, testContent, "overwrite")
	require.NoError(t, err, "File write operation failed")
	require.NotNil(t, writeResult, "Write result should not be nil")
	require.True(t, writeResult.Success,
		"File write was not successful")

	// Read back the file to verify
	readResult, err := recoveredSession.FileSystem.ReadFile(testPath)
	require.NoError(t, err, "File read operation failed")
	require.NotNil(t, readResult, "Read result should not be nil")
	assert.Equal(t, testContent, readResult.Content,
		"Read content doesn't match written content")
}

// TestOriginalAndRecoveredSessionBothWork verifies that both original and
// recovered sessions can perform file operations
func TestOriginalAndRecoveredSessionBothWork(t *testing.T) {
	suite := &GetFileTransferContextTestSuite{}
	suite.SetupTest(t)
	defer suite.TearDownTest(t)

	sessionID := suite.session.SessionID

	// Wait a bit for session to be fully ready
	time.Sleep(5 * time.Second)

	// Test 1: Original session can write files
	testContent1 := fmt.Sprintf("Original session test at %d", time.Now().Unix())
	testFilename1 := fmt.Sprintf("original_test_%d.txt", time.Now().Unix())
	testPath1 := fmt.Sprintf("/tmp/%s", testFilename1)

	writeResult1, err := suite.session.FileSystem.WriteFile(testPath1, testContent1, "overwrite")
	require.NoError(t, err, "Original session file write failed")
	require.NotNil(t, writeResult1, "Write result 1 should not be nil")
	require.True(t, writeResult1.Success,
		"Original session file write was not successful")

	// Test 2: Recover the session
	getResult, err := suite.agentBay.Get(sessionID)
	require.NoError(t, err, "Get method failed")
	require.NotNil(t, getResult, "Get result should not be nil")
	require.True(t, getResult.Success, "Get method was not successful: %s", getResult.ErrorMessage)
	recoveredSession := getResult.Session

	// Test 3: Recovered session can write files
	testContent2 := fmt.Sprintf("Recovered session test at %d", time.Now().Unix())
	testFilename2 := fmt.Sprintf("recovered_test_%d.txt", time.Now().Unix())
	testPath2 := fmt.Sprintf("/tmp/%s", testFilename2)

	writeResult2, err := recoveredSession.FileSystem.WriteFile(testPath2, testContent2, "overwrite")
	require.NoError(t, err, "Recovered session file write failed")
	require.NotNil(t, writeResult2, "Write result 2 should not be nil")
	require.True(t, writeResult2.Success,
		"Recovered session file write was not successful")

	// Test 4: Verify both files exist and have correct content
	readResult1, err := recoveredSession.FileSystem.ReadFile(testPath1)
	require.NoError(t, err, "Failed to read file 1")
	require.NotNil(t, readResult1, "Read result 1 should not be nil")
	assert.Equal(t, testContent1, readResult1.Content, "File 1 content mismatch")

	readResult2, err := recoveredSession.FileSystem.ReadFile(testPath2)
	require.NoError(t, err, "Failed to read file 2")
	require.NotNil(t, readResult2, "Read result 2 should not be nil")
	assert.Equal(t, testContent2, readResult2.Content, "File 2 content mismatch")
}
