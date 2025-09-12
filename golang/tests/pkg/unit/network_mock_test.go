package agentbay_test

import (
	"errors"
	"testing"

	"github.com/alibabacloud-go/tea/tea"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/unit/mock"
	"github.com/golang/mock/gomock"
	"github.com/stretchr/testify/assert"
)

// TestNetwork_*_WithMockClient tests network functionality using mock objects
// These tests focus on business logic without real API calls

// TestNetwork_CreateNetwork_WithMockClient tests network creation with mock
func TestNetwork_CreateNetwork_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Network
	mockNetwork := mock.NewMockNetworkInterface(ctrl)

	// Set expected behavior for successful creation
	expectedResult := &agentbay.CreateNetworkResult{
		Success: true,
		NetworkInfo: &agentbay.NetworkInfo{
			NetworkID:    "nw-mock-12345",
			NetworkToken: "mock-token-67890",
		},
	}
	mockNetwork.EXPECT().CreateNetwork(nil).Return(expectedResult, nil)

	// Test CreateNetwork method call
	result, err := mockNetwork.CreateNetwork(nil)

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.True(t, result.Success)
	assert.Equal(t, "nw-mock-12345", result.NetworkInfo.NetworkID)
	assert.Equal(t, "mock-token-67890", result.NetworkInfo.NetworkToken)
}

// TestNetwork_CreateNetworkWithExistingID_WithMockClient tests network creation with existing ID
func TestNetwork_CreateNetworkWithExistingID_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Network
	mockNetwork := mock.NewMockNetworkInterface(ctrl)

	// Set expected behavior for existing network ID
	existingNetworkID := "nw-existing-12345"
	expectedResult := &agentbay.CreateNetworkResult{
		Success: true,
		NetworkInfo: &agentbay.NetworkInfo{
			NetworkID:    existingNetworkID,
			NetworkToken: "existing-token-67890",
		},
	}
	mockNetwork.EXPECT().CreateNetwork(tea.String(existingNetworkID)).Return(expectedResult, nil)

	// Test CreateNetwork method call with existing ID
	result, err := mockNetwork.CreateNetwork(tea.String(existingNetworkID))

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.True(t, result.Success)
	assert.Equal(t, existingNetworkID, result.NetworkInfo.NetworkID)
	assert.Equal(t, "existing-token-67890", result.NetworkInfo.NetworkToken)
}

// TestNetwork_CreateNetwork_Error_WithMockClient tests network creation error handling
func TestNetwork_CreateNetwork_Error_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Network
	mockNetwork := mock.NewMockNetworkInterface(ctrl)

	// Set expected behavior - return error
	expectedError := errors.New("network creation failed")
	mockNetwork.EXPECT().CreateNetwork(nil).Return(nil, expectedError)

	// Test error case
	result, err := mockNetwork.CreateNetwork(nil)

	// Verify error handling
	assert.Error(t, err)
	assert.Nil(t, result)
	assert.Equal(t, "network creation failed", err.Error())
}

// TestNetwork_DescribeNetwork_WithMockClient tests network description with mock
func TestNetwork_DescribeNetwork_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Network
	mockNetwork := mock.NewMockNetworkInterface(ctrl)

	// Set expected behavior for successful description
	networkID := "nw-test-12345"
	expectedResult := &agentbay.DescribeNetworkResult{
		Success: true,
		NetworkInfo: &agentbay.NetworkInfo{
			NetworkID: networkID,
			Online:    tea.Bool(true),
		},
	}
	mockNetwork.EXPECT().DescribeNetwork(networkID).Return(expectedResult, nil)

	// Test DescribeNetwork method call
	result, err := mockNetwork.DescribeNetwork(networkID)

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.True(t, result.Success)
	assert.Equal(t, networkID, result.NetworkInfo.NetworkID)
	assert.NotNil(t, result.NetworkInfo.Online)
	assert.True(t, *result.NetworkInfo.Online)
}

// TestNetwork_DescribeNetwork_NotFound_WithMockClient tests network description with non-existent network
func TestNetwork_DescribeNetwork_NotFound_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Network
	mockNetwork := mock.NewMockNetworkInterface(ctrl)

	// Set expected behavior for non-existent network
	networkID := "nw-nonexistent-12345"
	expectedResult := &agentbay.DescribeNetworkResult{
		Success:      false,
		ErrorMessage: "Network not found",
	}
	mockNetwork.EXPECT().DescribeNetwork(networkID).Return(expectedResult, nil)

	// Test DescribeNetwork method call
	result, err := mockNetwork.DescribeNetwork(networkID)

	// Verify call success but operation failed
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.False(t, result.Success)
	assert.Equal(t, "Network not found", result.ErrorMessage)
}

// TestNetwork_DescribeNetwork_Error_WithMockClient tests network description error handling
func TestNetwork_DescribeNetwork_Error_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Network
	mockNetwork := mock.NewMockNetworkInterface(ctrl)

	// Set expected behavior - return error
	networkID := "nw-error-12345"
	expectedError := errors.New("network description failed")
	mockNetwork.EXPECT().DescribeNetwork(networkID).Return(nil, expectedError)

	// Test error case
	result, err := mockNetwork.DescribeNetwork(networkID)

	// Verify error handling
	assert.Error(t, err)
	assert.Nil(t, result)
	assert.Equal(t, "network description failed", err.Error())
}
