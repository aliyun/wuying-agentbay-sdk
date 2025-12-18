# Mobile Simulate API Reference

## Type MobileSimulateService

```go
type MobileSimulateService struct {
	agentBay		*AgentBay
	contextService		*ContextService
	simulateEnable		bool
	simulateMode		models.MobileSimulateMode
	contextID		string
	contextSync		*ContextSync
	mobileDevInfoPath	string
	useInternalContext	bool
}
```

MobileSimulateService provides methods to manage persistent mobile dev info and sync to the mobile
device

### Methods

### GetSimulateConfig

```go
func (m *MobileSimulateService) GetSimulateConfig() *models.MobileSimulateConfig
```

GetSimulateConfig gets the simulate config Returns:
  - MobileSimulateConfig: The simulate config
  - Simulate: The simulate feature enable flag
  - SimulatePath: The path of the mobile dev info file
  - SimulateMode: The simulate mode
  - SimulatedContextID: The context ID of the mobile info

### GetSimulateContextID

```go
func (m *MobileSimulateService) GetSimulateContextID() string
```

GetSimulateContextID gets the simulate context id

### GetSimulateEnable

```go
func (m *MobileSimulateService) GetSimulateEnable() bool
```

GetSimulateEnable gets the simulate enable flag

### GetSimulateMode

```go
func (m *MobileSimulateService) GetSimulateMode() models.MobileSimulateMode
```

GetSimulateMode gets the simulate mode

### SetSimulateContextID

```go
func (m *MobileSimulateService) SetSimulateContextID(contextID string)
```

SetSimulateContextID sets a previously saved simulate context id Please make sure the context id is
provided by MobileSimulateService but not user side created context

### SetSimulateEnable

```go
func (m *MobileSimulateService) SetSimulateEnable(enable bool)
```

SetSimulateEnable sets the simulate enable flag

### SetSimulateMode

```go
func (m *MobileSimulateService) SetSimulateMode(mode models.MobileSimulateMode)
```

SetSimulateMode sets the simulate mode mode: The simulate mode
  - PropertiesOnly: Simulate only device properties
  - SensorsOnly: Simulate only device sensors
  - PackagesOnly: Simulate only installed packages
  - ServicesOnly: Simulate only system services
  - All: Simulate all aspects of the device

### UploadMobileInfo

```go
func (m *MobileSimulateService) UploadMobileInfo(mobileDevInfoContent string, contextSync *ContextSync) *MobileSimulateUploadResult
```

UploadMobileInfo uploads the mobile simulate dev info

Args:
  - mobileDevInfoContent: The mobile simulate dev info content to upload
  - contextSync: Optional
  - If not provided, a new context sync will be created for the mobile simulate service and this
    context id will return by the MobileSimulateUploadResult. User can use this context id to do
    persistent mobile simulate across sessions.
  - If provided, the mobile simulate dev info will be uploaded to the context sync in a specific
    path.

Returns:
  - MobileSimulateUploadResult: The result of the upload operation
  - Success: Whether the operation was successful
  - MobileSimulateContextID: The context ID of the mobile info
  - ErrorMessage: The error message if the operation failed

Notes:


If context_sync is not provided, a new context sync will be created for the mobile simulate.

If context_sync is provided, the mobile simulate dev info will be uploaded to the context sync.

If the mobile simulate dev info already exists in the context sync, the context sync will be updated.

If the mobile simulate dev info does not exist in the context sync, the context sync will be created.

If the upload operation fails, the error message will be returned.

### Related Functions

### NewMobileSimulateService

```go
func NewMobileSimulateService(agentBay *AgentBay) (*MobileSimulateService, error)
```

NewMobileSimulateService creates a new MobileSimulateService instance

## Type MobileSimulateUploadResult

```go
type MobileSimulateUploadResult struct {
	Success			bool
	MobileSimulateContextID	string
	ErrorMessage		string
}
```

MobileSimulateUploadResult represents the result of uploading mobile info

## Functions

### NewMobileSimulateService

```go
func NewMobileSimulateService(agentBay *AgentBay) (*MobileSimulateService, error)
```

NewMobileSimulateService creates a new MobileSimulateService instance

---

*Documentation generated automatically from Go source code.*
