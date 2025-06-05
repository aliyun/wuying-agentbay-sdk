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
}

// NewCreateSessionParams creates a new CreateSessionParams with default values.
func NewCreateSessionParams() *CreateSessionParams {
	return &CreateSessionParams{
		Labels: make(map[string]string),
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
