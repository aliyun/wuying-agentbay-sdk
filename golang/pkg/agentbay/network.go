package agentbay

import (
	"fmt"

	"github.com/alibabacloud-go/tea/tea"
	mcp "github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// NetworkInfo represents network information
type NetworkInfo struct {
	NetworkID    string `json:"network_id"`
	NetworkToken string `json:"network_token"`
	Online       *bool  `json:"online,omitempty"`
}

// NewNetworkInfoFromCreateResponse creates NetworkInfo from CreateNetwork response
func NewNetworkInfoFromCreateResponse(data *mcp.CreateNetworkResponseBodyData) *NetworkInfo {
	networkInfo := &NetworkInfo{}
	if data != nil {
		networkInfo.NetworkID = tea.StringValue(data.NetworkId)
		networkInfo.NetworkToken = tea.StringValue(data.NetworkToken)
	}
	return networkInfo
}

// NewNetworkInfoFromDescribeResponse creates NetworkInfo from DescribeNetwork response
func NewNetworkInfoFromDescribeResponse(networkID string, data *mcp.DescribeNetworkResponseBodyData) *NetworkInfo {
	networkInfo := &NetworkInfo{
		NetworkID: networkID,
	}
	if data != nil {
		networkInfo.Online = data.Online
	}
	return networkInfo
}

// ToMap converts NetworkInfo to map
func (ni *NetworkInfo) ToMap() map[string]interface{} {
	result := map[string]interface{}{
		"network_id":    ni.NetworkID,
		"network_token": ni.NetworkToken,
	}
	if ni.Online != nil {
		result["online"] = *ni.Online
	} else {
		result["online"] = nil
	}
	return result
}

// String returns string representation of NetworkInfo
func (ni *NetworkInfo) String() string {
	onlineStatus := "unknown"
	if ni.Online != nil {
		if *ni.Online {
			onlineStatus = "online"
		} else {
			onlineStatus = "offline"
		}
	}
	return fmt.Sprintf("NetworkInfo(network_id='%s', status='%s')", ni.NetworkID, onlineStatus)
}

// CreateNetworkResult represents the result of a create network operation
type CreateNetworkResult struct {
	models.ApiResponse
	Success      bool         `json:"success"`
	NetworkInfo  *NetworkInfo `json:"network_info,omitempty"`
	ErrorMessage string       `json:"error_message,omitempty"`
}

// DescribeNetworkResult represents the result of a describe network operation
type DescribeNetworkResult struct {
	models.ApiResponse
	Success      bool         `json:"success"`
	NetworkInfo  *NetworkInfo `json:"network_info,omitempty"`
	ErrorMessage string       `json:"error_message,omitempty"`
}

// NetworkManager manages network operations
type NetworkManager struct {
	// AgentBay is the AgentBay instance.
	AgentBay *AgentBay
}

// CreateNetwork creates a new network or retrieves token for an existing network
func (nm *NetworkManager) CreateNetwork(networkID *string) (*CreateNetworkResult, error) {
	request := &mcp.CreateNetworkRequest{
		Authorization: tea.String("Bearer " + nm.AgentBay.APIKey),
		NetworkId:     networkID,
	}

	response, err := nm.AgentBay.Client.CreateNetwork(request)
	if err != nil {
		return &CreateNetworkResult{
			ApiResponse:  models.ApiResponse{RequestID: ""},
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to create network: %v", err),
		}, nil
	}

	requestID := models.ExtractRequestID(response.Headers)

	if response.Body != nil && tea.BoolValue(response.Body.Success) {
		networkInfo := NewNetworkInfoFromCreateResponse(response.Body.Data)

		return &CreateNetworkResult{
			ApiResponse: models.ApiResponse{RequestID: requestID},
			Success:     true,
			NetworkInfo: networkInfo,
		}, nil
	}

	errorMessage := "Failed to create network"
	if response.Body != nil && response.Body.Message != nil {
		errorMessage = tea.StringValue(response.Body.Message)
	}

	return &CreateNetworkResult{
		ApiResponse:  models.ApiResponse{RequestID: requestID},
		Success:      false,
		ErrorMessage: errorMessage,
	}, nil
}

// DescribeNetwork queries network details
func (nm *NetworkManager) DescribeNetwork(networkID string) (*DescribeNetworkResult, error) {
	request := &mcp.DescribeNetworkRequest{
		Authorization: tea.String("Bearer " + nm.AgentBay.APIKey),
		NetworkId:     tea.String(networkID),
	}

	response, err := nm.AgentBay.Client.DescribeNetwork(request)
	if err != nil {
		return &DescribeNetworkResult{
			ApiResponse:  models.ApiResponse{RequestID: ""},
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to describe network: %v", err),
		}, nil
	}

	requestID := models.ExtractRequestID(response.Headers)

	if response.Body != nil && tea.BoolValue(response.Body.Success) {
		networkInfo := NewNetworkInfoFromDescribeResponse(networkID, response.Body.Data)

		return &DescribeNetworkResult{
			ApiResponse: models.ApiResponse{RequestID: requestID},
			Success:     true,
			NetworkInfo: networkInfo,
		}, nil
	}

	errorMessage := "Failed to describe network"
	if response.Body != nil && response.Body.Message != nil {
		errorMessage = tea.StringValue(response.Body.Message)
	}

	return &DescribeNetworkResult{
		ApiResponse:  models.ApiResponse{RequestID: requestID},
		Success:      false,
		ErrorMessage: errorMessage,
	}, nil
}
