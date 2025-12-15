import { ContextService } from "../../src/context";
import * as sinon from "sinon";

describe("ContextService list with sessionId", () => {
    let sandbox: sinon.SinonSandbox;
    let mockClient: any;
    let mockAgentBay: any;
    let contextService: ContextService;

    beforeEach(() => {
        sandbox = sinon.createSandbox();
        mockClient = {
            listContexts: sandbox.stub(),
        };

        mockAgentBay = {
            getAPIKey: sandbox.stub().returns("test-api-key"),
            getClient: sandbox.stub().returns(mockClient),
            getRegionId: sandbox.stub().returns(undefined),
        };

        contextService = new ContextService(mockAgentBay);
    });

    afterEach(() => {
        sandbox.restore();
    });

    it("passes sessionId and type to client.listContexts request", async () => {
        const fakeResponse = {
            body: { data: [], requestId: "r1", success: true },
            statusCode: 200,
        };
        mockClient.listContexts.resolves(fakeResponse);

        const params = { sessionId: "s-123", maxResults: 5 };

        await contextService.list(params as any);

        sinon.assert.calledOnce(mockClient.listContexts);
        const callArg = mockClient.listContexts.getCall(0).args[0];
        // the generated client uses camelCase sessionId on the request object
        expect(callArg.sessionId).toBe("s-123");
        expect(callArg.maxResults).toBe(5);
    });
});
