package agentbay_test

import (
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/stretchr/testify/assert"
)

func TestNewUploadPolicy(t *testing.T) {
	policy := agentbay.NewUploadPolicy()

	assert.NotNil(t, policy)
	assert.True(t, policy.AutoUpload)
	assert.Equal(t, agentbay.UploadBeforeResourceRelease, policy.UploadStrategy)
	assert.Equal(t, 30, policy.Period)
}

func TestNewDownloadPolicy(t *testing.T) {
	policy := agentbay.NewDownloadPolicy()

	assert.NotNil(t, policy)
	assert.True(t, policy.AutoDownload)
	assert.Equal(t, agentbay.DownloadAsync, policy.DownloadStrategy)
}

func TestNewDeletePolicy(t *testing.T) {
	policy := agentbay.NewDeletePolicy()

	assert.NotNil(t, policy)
	assert.True(t, policy.SyncLocalFile)
}

func TestNewSyncPolicy(t *testing.T) {
	policy := agentbay.NewSyncPolicy()

	assert.NotNil(t, policy)
	assert.NotNil(t, policy.UploadPolicy)
	assert.NotNil(t, policy.DownloadPolicy)
	assert.NotNil(t, policy.DeletePolicy)
	assert.NotNil(t, policy.BWList)
	assert.NotNil(t, policy.BWList.WhiteLists)
	assert.Len(t, policy.BWList.WhiteLists, 1)
	assert.Equal(t, "", policy.BWList.WhiteLists[0].Path)
	assert.Empty(t, policy.BWList.WhiteLists[0].ExcludePaths)
	assert.NotNil(t, policy.SyncPaths)
	assert.Len(t, policy.SyncPaths, 1)
	assert.Equal(t, "", policy.SyncPaths[0])
}

func TestNewContextSync(t *testing.T) {
	contextID := "ctx-12345"
	path := "/home/user"
	policy := agentbay.NewSyncPolicy()

	sync := agentbay.NewContextSync(contextID, path, policy)

	assert.NotNil(t, sync)
	assert.Equal(t, contextID, sync.ContextID)
	assert.Equal(t, path, sync.Path)
	assert.Equal(t, policy, sync.Policy)
}

func TestNewContextSyncWithNilPolicy(t *testing.T) {
	contextID := "ctx-12345"
	path := "/home/user"

	sync := agentbay.NewContextSync(contextID, path, nil)

	assert.NotNil(t, sync)
	assert.Equal(t, contextID, sync.ContextID)
	assert.Equal(t, path, sync.Path)
	assert.Nil(t, sync.Policy)
}

func TestContextSyncWithPolicy(t *testing.T) {
	contextID := "ctx-12345"
	path := "/home/user"

	sync := agentbay.NewContextSync(contextID, path, nil)
	assert.Nil(t, sync.Policy)

	// Create a custom policy
	policy := &agentbay.SyncPolicy{
		UploadPolicy: &agentbay.UploadPolicy{
			AutoUpload:     false,
			UploadStrategy: agentbay.PeriodicUpload,
			Period:         15,
		},
		DownloadPolicy: &agentbay.DownloadPolicy{
			AutoDownload:     false,
			DownloadStrategy: agentbay.DownloadSync,
		},
		DeletePolicy: &agentbay.DeletePolicy{
			SyncLocalFile: false,
		},
		BWList: &agentbay.BWList{
			WhiteLists: []*agentbay.WhiteList{
				{
					Path:         "/data",
					ExcludePaths: []string{"/data/temp"},
				},
			},
		},
		SyncPaths: []string{"/data/important"},
	}

	// Apply the policy
	result := sync.WithPolicy(policy)

	assert.NotNil(t, result)
	assert.Same(t, sync, result) // Verify method chaining returns the same instance
	assert.Equal(t, policy, sync.Policy)

	// Verify upload policy
	assert.NotNil(t, sync.Policy.UploadPolicy)
	assert.False(t, sync.Policy.UploadPolicy.AutoUpload)
	assert.Equal(t, agentbay.PeriodicUpload, sync.Policy.UploadPolicy.UploadStrategy)
	assert.Equal(t, 15, sync.Policy.UploadPolicy.Period)

	// Verify download policy
	assert.NotNil(t, sync.Policy.DownloadPolicy)
	assert.False(t, sync.Policy.DownloadPolicy.AutoDownload)
	assert.Equal(t, agentbay.DownloadSync, sync.Policy.DownloadPolicy.DownloadStrategy)

	// Verify delete policy
	assert.NotNil(t, sync.Policy.DeletePolicy)
	assert.False(t, sync.Policy.DeletePolicy.SyncLocalFile)

	// Verify BWList
	assert.NotNil(t, sync.Policy.BWList)
	assert.Len(t, sync.Policy.BWList.WhiteLists, 1)
	assert.Equal(t, "/data", sync.Policy.BWList.WhiteLists[0].Path)
	assert.Equal(t, []string{"/data/temp"}, sync.Policy.BWList.WhiteLists[0].ExcludePaths)

	// Verify sync paths
	assert.NotNil(t, sync.Policy.SyncPaths)
	assert.Equal(t, []string{"/data/important"}, sync.Policy.SyncPaths)
}
