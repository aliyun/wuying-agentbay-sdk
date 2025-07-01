import { InstalledApp, Process, Application } from '../../src/application/application';
import { APIError } from '../../src/exceptions';
import * as sinon from 'sinon';

const mockInstalledAppsData: InstalledApp[] = [
    {
        name: "美团",
        start_cmd: "monkey -p com.sankuai.meituan -c android.intent.category.LAUNCHER 1",
        stop_cmd: "am force-stop com.sankuai.meituan",
        work_directory: ""
    },
    {
        name: "小红书",
        start_cmd: "monkey -p com.xingin.xhs -c android.intent.category.LAUNCHER 1",
        stop_cmd: "am force-stop com.xingin.xhs",
        work_directory: ""
    },
    {
        name: "高德地图",
        start_cmd: "monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1",
        stop_cmd: "am force-stop com.autonavi.minimap",
        work_directory: ""
    }
];

const mockProcessData: Process[] = [
    {
        pname: "com.autonavi.minimap",
        pid: 12345,
        cmdline: "monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1"
    }
];

const mockVisibleAppsData: Process[] = [
    {
        pname: "com.autonavi.minimap",
        pid: 12345,
        cmdline: "cmd1"
    },
    {
        pname: "com.xingin.xhs",
        pid: 23456,
        cmdline: "cmd2"
    }
];

describe('ApplicationApi', () => {
    let mockApplication: Application;
    let mockSession: any;
    let sandbox: sinon.SinonSandbox;

    beforeEach(() => {
        sandbox = sinon.createSandbox();

        mockSession = {
            getAPIKey: sandbox.stub().returns('test-api-key'),
            getClient: sandbox.stub(),
            getSessionId: sandbox.stub().returns('test-session-id')
        };

        mockApplication = new Application(mockSession);
    });

    afterEach(() => {
        sandbox.restore();
    });

    describe('test_get_installed_apps_success', () => {
        it('should get installed apps successfully', async () => {
            const callMcpToolStub = sandbox.stub(mockApplication as any, 'callMcpTool')
                .resolves({
                    data: {},
                    textContent: JSON.stringify(mockInstalledAppsData),
                    isError: false,
                    statusCode: 200,
                    requestId: 'test-request-id'
                });

            const result = await mockApplication.getInstalledApps();
            expect(result.data).toHaveLength(3);

            expect(result.data[0]).toBeInstanceOf(Object);
            expect(result.data[0].name).toBe("美团");
            expect(result.data[1].name).toBe("小红书");
            expect(result.data[2].name).toBe("高德地图");

            expect(result.requestId).toBe('test-request-id');

            expect(callMcpToolStub.calledOnce).toBe(true);
        });
    });

    describe('test_get_installed_apps_failure', () => {
        it('should handle get installed apps failure', async () => {
            sandbox.stub(mockApplication as any, 'callMcpTool')
                .rejects(new APIError('Failed to get installed apps'));

            await expect(mockApplication.getInstalledApps())
                .rejects.toThrow('Failed to get installed apps');
        });
    });

    describe('test_start_app_success', () => {
        it('should start app successfully', async () => {
            const callMcpToolStub = sandbox.stub(mockApplication as any, 'callMcpTool')
                .resolves({
                    data: {},
                    textContent: JSON.stringify(mockProcessData),
                    isError: false,
                    statusCode: 200,
                    requestId: 'test-request-id'
                });

            const result = await mockApplication.startApp(
                "monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1"
            );

            expect(result.data).toHaveLength(1);
            expect(result.data[0].pname).toBe("com.autonavi.minimap");
            expect(result.data[0].pid).toBe(12345);
            expect(result.data[0].cmdline).toBe(
                "monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1"
            );
            expect(result.requestId).toBe('test-request-id');

            expect(callMcpToolStub.calledOnce).toBe(true);
        });
    });

    describe('test_start_app_failure', () => {
        it('should handle start app failure', async () => {
            sandbox.stub(mockApplication as any, 'callMcpTool')
                .rejects(new APIError('Failed to start app'));

            await expect(mockApplication.startApp(
                "monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1"
            )).rejects.toThrow('Failed to start app');
        });
    });

    describe('test_stop_app_by_cmd_success', () => {
        it('should stop app by command successfully', async () => {
            const callMcpToolStub = sandbox.stub(mockApplication as any, 'callMcpTool')
                .resolves({
                    data: {},
                    isError: false,
                    statusCode: 200,
                    requestId: 'test-request-id'
                });

            const result = await mockApplication.stopAppByCmd("am force-stop com.autonavi.minimap");

            expect(result.requestId).toBe('test-request-id');
            expect(result.data).toBeUndefined(); // void response

            expect(callMcpToolStub.calledOnce).toBe(true);
        });
    });

    describe('test_stop_app_by_cmd_failure', () => {
        it('should handle stop app by command failure', async () => {
            sandbox.stub(mockApplication as any, 'callMcpTool')
                .rejects(new APIError('Failed to stop app'));

            await expect(mockApplication.stopAppByCmd("am force-stop com.autonavi.minimap"))
                .rejects.toThrow('Failed to stop app');
        });
    });

    describe('test_stop_app_by_pname_success', () => {
        it('should stop app by package name successfully', async () => {
            const callMcpToolStub = sandbox.stub(mockApplication as any, 'callMcpTool')
                .resolves({
                    data: {},
                    isError: false,
                    statusCode: 200,
                    requestId: 'test-request-id'
                });

            const result = await mockApplication.stopAppByPName("com.autonavi.minimap");

            expect(result.requestId).toBe('test-request-id');
            expect(result.data).toBeUndefined(); // void response

            expect(callMcpToolStub.calledOnce).toBe(true);
        });
    });

    describe('test_stop_app_by_pname_failure', () => {
        it('should handle stop app by package name failure', async () => {
            sandbox.stub(mockApplication as any, 'callMcpTool')
                .rejects(new APIError('Failed to stop app by pname'));

            await expect(mockApplication.stopAppByPName("com.autonavi.minimap"))
                .rejects.toThrow('Failed to stop app by pname');
        });
    });

    describe('test_stop_app_by_pid_success', () => {
        it('should stop app by PID successfully', async () => {
            const callMcpToolStub = sandbox.stub(mockApplication as any, 'callMcpTool')
                .resolves({
                    data: {},
                    isError: false,
                    statusCode: 200,
                    requestId: 'test-request-id'
                });

            const result = await mockApplication.stopAppByPID(12345);

            expect(result.requestId).toBe('test-request-id');
            expect(result.data).toBeUndefined(); // void response

            expect(callMcpToolStub.calledOnce).toBe(true);
        });
    });

    describe('test_stop_app_by_pid_failure', () => {
        it('should handle stop app by PID failure', async () => {
            sandbox.stub(mockApplication as any, 'callMcpTool')
                .rejects(new APIError('Failed to stop app by pid'));

            await expect(mockApplication.stopAppByPID(12345))
                .rejects.toThrow('Failed to stop app by pid');
        });
    });

    describe('test_list_visible_apps_success', () => {
        it('should list visible apps successfully', async () => {
            const callMcpToolStub = sandbox.stub(mockApplication as any, 'callMcpTool')
                .resolves({
                    data: {},
                    textContent: JSON.stringify(mockVisibleAppsData),
                    isError: false,
                    statusCode: 200,
                    requestId: 'test-request-id'
                });

            const result = await mockApplication.listVisibleApps();

            expect(result.data).toHaveLength(2);
            expect(result.data[0]).toBeInstanceOf(Object);
            expect(result.data[0].pname).toBe("com.autonavi.minimap");
            expect(result.data[1].pname).toBe("com.xingin.xhs");
            expect(result.requestId).toBe('test-request-id');

            expect(callMcpToolStub.calledOnce).toBe(true);
        });
    });

    describe('test_list_visible_apps_failure', () => {
        it('should handle list visible apps failure', async () => {
            sandbox.stub(mockApplication as any, 'callMcpTool')
                .rejects(new APIError('Failed to list visible apps'));

            await expect(mockApplication.listVisibleApps())
                .rejects.toThrow('Failed to list visible apps');
        });
    });
});
