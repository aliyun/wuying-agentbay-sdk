package agentbay

import (
	"encoding/json"
)

// CreateSessionParams provides a way to configure the parameters for creating a new session
// in the AgentBay cloud environment.
type CreateSessionParams struct {
	// Labels are custom labels for the Session. These can be used for organizing and filtering sessions.
	Labels map[string]string

	// ContextID is the ID of the context to bind to the session.
	// The context can include various types of persistence like file system (volume) and cookies.
	//
	// Deprecated: This field is deprecated and will be removed in a future version.
	// Please use ContextSync instead for more flexible and powerful data persistence.
	//
	// Important Limitations:
	// 1. One session at a time: A context can only be used by one session at a time.
	//    If you try to create a session with a context ID that is already in use by another active session,
	//    the session creation will fail.
	//
	// 2. OS binding: A context is bound to the operating system of the first session that uses it.
	//    When a context is first used with a session, it becomes bound to that session's OS.
	//    Any attempt to use the context with a session running on a different OS will fail.
	//    For example, if a context is first used with a Linux session, it cannot later be used
	//    with a Windows or Android session.
	ContextID string

	// ImageId specifies the image ID to use for the session.
	ImageId string

	// ContextSync is a list of context synchronization configurations.
	// These configurations define how contexts should be synchronized and mounted.
	ContextSync []*ContextSync
}

// NewCreateSessionParams creates a new CreateSessionParams with default values.
func NewCreateSessionParams() *CreateSessionParams {
	return &CreateSessionParams{
		Labels:      make(map[string]string),
		ContextSync: make([]*ContextSync, 0),
	}
}

// WithLabels sets the labels for the session parameters and returns the updated parameters.
func (p *CreateSessionParams) WithLabels(labels map[string]string) *CreateSessionParams {
	p.Labels = labels
	return p
}

// WithContextID sets the context ID for the session parameters and returns the updated parameters.
func (p *CreateSessionParams) WithContextID(contextID string) *CreateSessionParams {
	p.ContextID = contextID
	return p
}

// WithImageId sets the image ID for the session parameters and returns the updated parameters.
func (p *CreateSessionParams) WithImageId(imageId string) *CreateSessionParams {
	p.ImageId = imageId
	return p
}

// GetLabelsJSON returns the labels as a JSON string.
func (p *CreateSessionParams) GetLabelsJSON() (string, error) {
	if len(p.Labels) == 0 {
		return "", nil
	}

	labelsJSON, err := json.Marshal(p.Labels)
	if err != nil {
		return "", err
	}

	return string(labelsJSON), nil
}

// AddContextSync adds a context sync configuration to the session parameters.
func (p *CreateSessionParams) AddContextSync(contextID, path string, policy *SyncPolicy) *CreateSessionParams {
	contextSync := &ContextSync{
		ContextID: contextID,
		Path:      path,
		Policy:    policy,
	}
	p.ContextSync = append(p.ContextSync, contextSync)
	return p
}

// AddContextSyncConfig adds a pre-configured context sync to the session parameters.
func (p *CreateSessionParams) AddContextSyncConfig(contextSync *ContextSync) *CreateSessionParams {
	p.ContextSync = append(p.ContextSync, contextSync)
	return p
}

// WithContextSync sets the context sync configurations for the session parameters.
func (p *CreateSessionParams) WithContextSync(contextSyncs []*ContextSync) *CreateSessionParams {
	p.ContextSync = contextSyncs
	return p
}
