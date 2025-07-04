package unit

import (
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// TestApiResponseInitialization tests initialization of ApiResponse
func TestApiResponseInitialization(t *testing.T) {
	// Create ApiResponse
	requestID := "test-request-id"
	response := models.ApiResponse{
		RequestID: requestID,
	}

	// Verify attributes
	if response.RequestID != requestID {
		t.Errorf("Expected RequestID to be '%s', got '%s'", requestID, response.RequestID)
	}
	if response.GetRequestID() != requestID {
		t.Errorf("Expected GetRequestID() to return '%s', got '%s'", requestID, response.GetRequestID())
	}
}

// TestApiResponseWithRequestID tests creating ApiResponse with WithRequestID
func TestApiResponseWithRequestID(t *testing.T) {
	// Create ApiResponse using WithRequestID
	requestID := "with-request-id"
	response := models.WithRequestID(requestID)

	// Verify attributes
	if response.RequestID != requestID {
		t.Errorf("Expected RequestID to be '%s', got '%s'", requestID, response.RequestID)
	}
	if response.GetRequestID() != requestID {
		t.Errorf("Expected GetRequestID() to return '%s', got '%s'", requestID, response.GetRequestID())
	}
}

// MockResponse simulates an API response with a RequestId field
type MockResponse struct {
	Body *MockResponseBody
}

// MockResponseBody contains a RequestId field
type MockResponseBody struct {
	RequestId *string
}

// TestExtractRequestIDSuccess tests extracting RequestID from a successful response
func TestExtractRequestIDSuccess(t *testing.T) {
	// Create a mock response with a RequestId
	expectedRequestID := "extracted-request-id"
	response := &MockResponse{
		Body: &MockResponseBody{
			RequestId: &expectedRequestID,
		},
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	// Verify the result
	if requestID != expectedRequestID {
		t.Errorf("Expected RequestID to be '%s', got '%s'", expectedRequestID, requestID)
	}
}

// TestExtractRequestIDMissing tests extracting RequestID when it's missing
func TestExtractRequestIDMissing(t *testing.T) {
	// Create a mock response without a RequestId
	response := &MockResponse{
		Body: &MockResponseBody{
			RequestId: nil,
		},
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	// Verify the result
	if requestID != "" {
		t.Errorf("Expected empty RequestID, got '%s'", requestID)
	}
}

// TestExtractRequestIDNilResponse tests extracting RequestID from a nil response
func TestExtractRequestIDNilResponse(t *testing.T) {
	// Extract RequestID from nil
	requestID := models.ExtractRequestID(nil)

	// Verify the result
	if requestID != "" {
		t.Errorf("Expected empty RequestID, got '%s'", requestID)
	}
}

// TestExtractRequestIDNilBody tests extracting RequestID from a response with nil body
func TestExtractRequestIDNilBody(t *testing.T) {
	// Create a mock response with nil body
	response := &MockResponse{
		Body: nil,
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	// Verify the result
	if requestID != "" {
		t.Errorf("Expected empty RequestID, got '%s'", requestID)
	}
}

// DifferentResponse is a response with a different structure
type DifferentResponse struct {
	// No Body field
	ID string
}

// TestExtractRequestIDDifferentStructure tests extracting RequestID from a different response structure
func TestExtractRequestIDDifferentStructure(t *testing.T) {
	// Create a response with a different structure
	response := &DifferentResponse{
		ID: "some-id",
	}

	// Extract RequestID
	requestID := models.ExtractRequestID(response)

	// Verify the result
	if requestID != "" {
		t.Errorf("Expected empty RequestID, got '%s'", requestID)
	}
}
