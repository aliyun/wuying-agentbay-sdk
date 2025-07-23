package agentbay

import "encoding/json"

// UploadStrategy defines the upload strategy for context synchronization
type UploadStrategy string

const (
	// UploadBeforeResourceRelease uploads files before resource release
	UploadBeforeResourceRelease UploadStrategy = "UploadBeforeResourceRelease"
)

// DownloadStrategy defines the download strategy for context synchronization
type DownloadStrategy string

const (
	// DownloadAsync downloads files asynchronously
	DownloadAsync DownloadStrategy = "DownloadAsync"
)

// UploadPolicy defines the upload policy for context synchronization
type UploadPolicy struct {
	// AutoUpload enables automatic upload
	AutoUpload bool `json:"autoUpload"`
	// UploadStrategy defines the upload strategy
	UploadStrategy UploadStrategy `json:"uploadStrategy"`
	// Period defines the upload period in minutes (for periodic upload)
	Period int `json:"period,omitempty"`
}

// NewUploadPolicy creates a new upload policy with default values
func NewUploadPolicy() *UploadPolicy {
	return &UploadPolicy{
		AutoUpload:     true,
		UploadStrategy: UploadBeforeResourceRelease,
		Period:         30, // Default to 30 minutes
	}
}

// DownloadPolicy defines the download policy for context synchronization
type DownloadPolicy struct {
	// AutoDownload enables automatic download
	AutoDownload bool `json:"autoDownload"`
	// DownloadStrategy defines the download strategy
	DownloadStrategy DownloadStrategy `json:"downloadStrategy"`
}

// NewDownloadPolicy creates a new download policy with default values
func NewDownloadPolicy() *DownloadPolicy {
	return &DownloadPolicy{
		AutoDownload:     true,
		DownloadStrategy: DownloadAsync,
	}
}

// DeletePolicy defines the delete policy for context synchronization
type DeletePolicy struct {
	// SyncLocalFile enables synchronization of local file deletions
	SyncLocalFile bool `json:"syncLocalFile"`
}

// NewDeletePolicy creates a new delete policy with default values
func NewDeletePolicy() *DeletePolicy {
	return &DeletePolicy{
		SyncLocalFile: true,
	}
}

// WhiteList defines the white list configuration
type WhiteList struct {
	// Path is the path to include in the white list
	Path string `json:"path"`
	// ExcludePaths are the paths to exclude from the white list
	ExcludePaths []string `json:"excludePaths,omitempty"`
}

// BWList defines the black and white list configuration
type BWList struct {
	// WhiteLists defines the white lists
	WhiteLists []*WhiteList `json:"whiteLists,omitempty"`
}

// SyncPolicy defines the synchronization policy
type SyncPolicy struct {
	// UploadPolicy defines the upload policy
	UploadPolicy *UploadPolicy `json:"uploadPolicy,omitempty"`
	// DownloadPolicy defines the download policy
	DownloadPolicy *DownloadPolicy `json:"downloadPolicy,omitempty"`
	// DeletePolicy defines the delete policy
	DeletePolicy *DeletePolicy `json:"deletePolicy,omitempty"`
	// BWList defines the black and white list
	BWList *BWList `json:"bwList,omitempty"`
}

// NewSyncPolicy creates a new sync policy with default values
func NewSyncPolicy() *SyncPolicy {
	return &SyncPolicy{
		UploadPolicy:   NewUploadPolicy(),
		DownloadPolicy: NewDownloadPolicy(),
		DeletePolicy:   NewDeletePolicy(),
		BWList: &BWList{
			WhiteLists: []*WhiteList{
				{
					Path:         "",
					ExcludePaths: []string{},
				},
			},
		},
	}
}

// ensureDefaults ensures all policy fields have default values if not provided
func (sp *SyncPolicy) ensureDefaults() {
	if sp.UploadPolicy == nil {
		sp.UploadPolicy = NewUploadPolicy()
	}
	if sp.DownloadPolicy == nil {
		sp.DownloadPolicy = NewDownloadPolicy()
	}
	if sp.DeletePolicy == nil {
		sp.DeletePolicy = NewDeletePolicy()
	}
	if sp.BWList == nil {
		sp.BWList = &BWList{
			WhiteLists: []*WhiteList{
				{
					Path:         "",
					ExcludePaths: []string{},
				},
			},
		}
	}
}

// MarshalJSON ensures all fields have default values before marshaling
func (sp *SyncPolicy) MarshalJSON() ([]byte, error) {
	sp.ensureDefaults()

	// Create a temporary struct to avoid infinite recursion
	type SyncPolicyAlias SyncPolicy
	return json.Marshal((*SyncPolicyAlias)(sp))
}

// ContextSync defines the context synchronization configuration
type ContextSync struct {
	// ContextID is the ID of the context to synchronize
	ContextID string `json:"contextId"`
	// Path is the path where the context should be mounted
	Path string `json:"path"`
	// Policy defines the synchronization policy
	Policy *SyncPolicy `json:"policy,omitempty"`
}

// NewContextSync creates a new context sync configuration
func NewContextSync(contextID, path string, policy *SyncPolicy) *ContextSync {
	return &ContextSync{
		ContextID: contextID,
		Path:      path,
		Policy:    policy,
	}
}

// WithPolicy sets the policy and returns the context sync for chaining
func (cs *ContextSync) WithPolicy(policy *SyncPolicy) *ContextSync {
	cs.Policy = policy
	return cs
}
