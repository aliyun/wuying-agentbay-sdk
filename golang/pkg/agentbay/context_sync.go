package agentbay

// UploadStrategy defines the upload strategy for context synchronization
type UploadStrategy string

const (
	// UploadBeforeResourceRelease uploads files before resource release
	UploadBeforeResourceRelease UploadStrategy = "UploadBeforeResourceRelease"
	// UploadAfterFileClose uploads files after file close
	UploadAfterFileClose UploadStrategy = "UploadAfterFileClose"
	// PeriodicUpload uploads files periodically
	PeriodicUpload UploadStrategy = "PERIODIC_UPLOAD"
)

// DownloadStrategy defines the download strategy for context synchronization
type DownloadStrategy string

const (
	// DownloadSync downloads files synchronously
	DownloadSync DownloadStrategy = "DownloadSync"
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

// DownloadPolicy defines the download policy for context synchronization
type DownloadPolicy struct {
	// AutoDownload enables automatic download
	AutoDownload bool `json:"autoDownload"`
	// DownloadStrategy defines the download strategy
	DownloadStrategy DownloadStrategy `json:"downloadStrategy"`
}

// DeletePolicy defines the delete policy for context synchronization
type DeletePolicy struct {
	// SyncLocalFile enables synchronization of local file deletions
	SyncLocalFile bool `json:"syncLocalFile"`
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
	// SyncPaths defines the paths to synchronize
	SyncPaths []string `json:"syncPaths,omitempty"`
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

// NewUploadPolicy creates a new upload policy with default values
func NewUploadPolicy() *UploadPolicy {
	return &UploadPolicy{
		AutoUpload:     true,
		UploadStrategy: UploadBeforeResourceRelease,
		Period:         30, // Default to 30 minutes
	}
}

// NewDownloadPolicy creates a new download policy with default values
func NewDownloadPolicy() *DownloadPolicy {
	return &DownloadPolicy{
		AutoDownload:     true,
		DownloadStrategy: DownloadAsync,
	}
}

// NewDeletePolicy creates a new delete policy with default values
func NewDeletePolicy() *DeletePolicy {
	return &DeletePolicy{
		SyncLocalFile: true,
	}
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
		SyncPaths: []string{""},
	}
}

// NewContextSync creates a new context sync configuration
func NewContextSync(contextID, path string) *ContextSync {
	return &ContextSync{
		ContextID: contextID,
		Path:      path,
		Policy:    NewSyncPolicy(),
	}
}

// NewBasicContextSync creates a basic context sync configuration with default policies
func NewBasicContextSync(contextID, path string) *ContextSync {
	return &ContextSync{
		ContextID: contextID,
		Path:      path,
		Policy:    NewSyncPolicy(),
	}
}

// NewContextSyncWithoutPolicy creates a context sync configuration without any policies
func NewContextSyncWithoutPolicy(contextID, path string) *ContextSync {
	return &ContextSync{
		ContextID: contextID,
		Path:      path,
	}
}

// WithUploadPolicy sets the upload policy
func (cs *ContextSync) WithUploadPolicy(policy *UploadPolicy) *ContextSync {
	if cs.Policy == nil {
		cs.Policy = NewSyncPolicy()
	}
	cs.Policy.UploadPolicy = policy
	return cs
}

// WithDownloadPolicy sets the download policy
func (cs *ContextSync) WithDownloadPolicy(policy *DownloadPolicy) *ContextSync {
	if cs.Policy == nil {
		cs.Policy = NewSyncPolicy()
	}
	cs.Policy.DownloadPolicy = policy
	return cs
}

// WithDeletePolicy sets the delete policy
func (cs *ContextSync) WithDeletePolicy(policy *DeletePolicy) *ContextSync {
	if cs.Policy == nil {
		cs.Policy = NewSyncPolicy()
	}
	cs.Policy.DeletePolicy = policy
	return cs
}

// WithBWList sets the black and white list
func (cs *ContextSync) WithBWList(bwList *BWList) *ContextSync {
	if cs.Policy == nil {
		cs.Policy = NewSyncPolicy()
	}
	cs.Policy.BWList = bwList
	return cs
}

// WithWhiteList sets the white list
func (cs *ContextSync) WithWhiteList(path string, excludePaths []string) *ContextSync {
	whiteList := &WhiteList{
		Path:         path,
		ExcludePaths: excludePaths,
	}
	bwList := &BWList{
		WhiteLists: []*WhiteList{whiteList},
	}
	return cs.WithBWList(bwList)
}

// WithWhiteLists sets multiple white lists
func (cs *ContextSync) WithWhiteLists(whiteLists []*WhiteList) *ContextSync {
	bwList := &BWList{
		WhiteLists: whiteLists,
	}
	return cs.WithBWList(bwList)
}

// WithSyncPaths sets the sync paths
func (cs *ContextSync) WithSyncPaths(syncPaths []string) *ContextSync {
	if cs.Policy == nil {
		cs.Policy = NewSyncPolicy()
	}
	cs.Policy.SyncPaths = syncPaths
	return cs
}
