# Session Params API Reference

## Type CreateSessionParams

```go
type CreateSessionParams struct {
	// Labels are custom labels for the Session. These can be used for organizing and filtering sessions.
	Labels	map[string]string

	// ImageId specifies the image ID to use for the session.
	ImageId	string

	// ContextSync is a list of context synchronization configurations.
	// These configurations define how contexts should be synchronized and mounted.
	ContextSync	[]*ContextSync

	// IsVpc specifies whether to create a VPC-based session. Defaults to false.
	IsVpc	bool

	// PolicyId specifies the policy ID to apply when creating the session.
	PolicyId	string

	// ExtraConfigs contains extra configuration settings for different session types
	ExtraConfigs	*models.ExtraConfigs

	// Framework specifies the framework name for tracking (e.g., "langchain"). Empty string means direct call.
	Framework	string

	// EnableBrowserReplay specifies whether to enable browser recording for this session.
	EnableBrowserReplay	bool
}
```

CreateSessionParams provides a way to configure the parameters for creating a new session in the
AgentBay cloud environment.

### Methods

### AddContextSync

```go
func (p *CreateSessionParams) AddContextSync(contextID, path string, policy *SyncPolicy) *CreateSessionParams
```

AddContextSync adds a context sync configuration to the session parameters.

### AddContextSyncConfig

```go
func (p *CreateSessionParams) AddContextSyncConfig(contextSync *ContextSync) *CreateSessionParams
```

AddContextSyncConfig adds a pre-configured context sync to the session parameters.

### GetExtraConfigsJSON

```go
func (p *CreateSessionParams) GetExtraConfigsJSON() (string, error)
```

GetExtraConfigsJSON returns the extra configs as a JSON string.

### GetLabelsJSON

```go
func (p *CreateSessionParams) GetLabelsJSON() (string, error)
```

GetLabelsJSON returns the labels as a JSON string.

### WithContextSync

```go
func (p *CreateSessionParams) WithContextSync(contextSyncs []*ContextSync) *CreateSessionParams
```

WithContextSync sets the context sync configurations for the session parameters.

### WithEnableBrowserReplay

```go
func (p *CreateSessionParams) WithEnableBrowserReplay(enableBrowserReplay bool) *CreateSessionParams
```

WithEnableBrowserReplay sets the browser replay flag for the session parameters and returns the
updated parameters.

### WithExtraConfigs

```go
func (p *CreateSessionParams) WithExtraConfigs(extraConfigs *models.ExtraConfigs) *CreateSessionParams
```

WithExtraConfigs sets the extra configurations for the session parameters and returns the updated
parameters.

### WithImageId

```go
func (p *CreateSessionParams) WithImageId(imageId string) *CreateSessionParams
```

WithImageId sets the image ID for the session parameters and returns the updated parameters.

### WithIsVpc

```go
func (p *CreateSessionParams) WithIsVpc(isVpc bool) *CreateSessionParams
```

WithIsVpc sets the VPC flag for the session parameters and returns the updated parameters.

### WithLabels

```go
func (p *CreateSessionParams) WithLabels(labels map[string]string) *CreateSessionParams
```

WithLabels sets the labels for the session parameters and returns the updated parameters.

### WithPolicyId

```go
func (p *CreateSessionParams) WithPolicyId(policyId string) *CreateSessionParams
```

WithPolicyId sets the policy ID for the session parameters and returns the updated parameters.

### Related Functions

### NewCreateSessionParams

```go
func NewCreateSessionParams() *CreateSessionParams
```

NewCreateSessionParams creates a new CreateSessionParams with default values.

## Type ListSessionParams

```go
type ListSessionParams struct {
	MaxResults	int32			// Number of results per page
	NextToken	string			// Token for the next page
	Labels		map[string]string	// Labels to filter by
}
```

ListSessionParams contains parameters for listing sessions

### Related Functions

### NewListSessionParams

```go
func NewListSessionParams() *ListSessionParams
```

NewListSessionParams creates a new ListSessionParams with default values

## Functions

### NewCreateSessionParams

```go
func NewCreateSessionParams() *CreateSessionParams
```

NewCreateSessionParams creates a new CreateSessionParams with default values.

### NewListSessionParams

```go
func NewListSessionParams() *ListSessionParams
```

NewListSessionParams creates a new ListSessionParams with default values

---

*Documentation generated automatically from Go source code.*
