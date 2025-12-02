package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.browser.BrowserContext;
import com.aliyun.agentbay.browser.BrowserOption;
import com.aliyun.agentbay.context.Context;
import com.aliyun.agentbay.context.ContextResult;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.SessionInfoResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

public class BrowserContextLoginPersistenceExample {

    public static void main(String[] args) {
        try {
            String apiKey = System.getenv("AGENTBAY_API_KEY");
            if (apiKey == null || apiKey.isEmpty()) {
                System.err.println("Please set AGENTBAY_API_KEY environment variable");
                return;
            }

            AgentBay agentBay = new AgentBay(apiKey);
            System.out.println("AgentBay client initialized");

            String contextName = "xiaohongshu-login-context-" + System.currentTimeMillis();
            System.out.println("\nStep 1: Creating persistent context: " + contextName);

            ContextResult contextResult = agentBay.getContext().get(contextName, true);
            if (!contextResult.isSuccess() || contextResult.getContext() == null) {
                System.err.println("Failed to create context: " + contextResult.getErrorMessage());
                return;
            }

            Context context = contextResult.getContext();
            System.out.println("Context created with ID: " + context.getId());

            BrowserContext browserContext = new BrowserContext(
                context.getId(),
                true
            );

            System.out.println("\nStep 2: Creating first session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setBrowserContext(browserContext);
            params.setImageId("browser_latest");

            SessionResult result1 = agentBay.create(params);

            if (result1.isSuccess() && result1.getSession() != null) {
                Session session1 = result1.getSession();
                System.out.println("First session created: " + session1.getSessionId());

                SessionInfoResult infoResult = session1.info();
                if (infoResult.isSuccess() && infoResult.getSessionInfo() != null) {
                    System.out.println("\nSession Info:");
                    System.out.println("\nResource URL: " +infoResult.getSessionInfo().getResourceUrl());
                }

                session1.getBrowser().init(new BrowserOption());
                System.out.println("Browser initialized");

                String navigateResult = session1.getBrowser().getAgent().navigate("https://www.xiaohongshu.com");
                System.out.println("Navigated to Xiaohongshu: " + navigateResult);

                System.out.println("\n==============================================");
                System.out.println("Please visit the session and login to Xiaohongshu");
                System.out.println("Waiting 60 seconds for you to login...");
                System.out.println("==============================================");

                Thread.sleep(60000);

                System.out.println("\nDeleting first session WITH context sync...");
                agentBay.delete(session1, true);
                System.out.println("First session deleted, browser data uploaded to cloud storage");

                System.out.println("\nStep 3: Creating second session with same BrowserContext...");
                SessionResult result2 = agentBay.create(params);

                if (result2.isSuccess() && result2.getSession() != null) {
                    Session session2 = result2.getSession();
                    System.out.println("Second session created: " + session2.getSessionId());

                    session2.getBrowser().init(new BrowserOption());
                    System.out.println("Browser initialized");

                    String screenshotData = session2.getBrowser().getAgent().navigate("https://www.xiaohongshu.com");
                    System.out.println("Navigated to Xiaohongshu: " + screenshotData);

                    Thread.sleep(5000);

                    SessionInfoResult infoResult2 = session1.info();
                    if (infoResult2.isSuccess() && infoResult2.getSessionInfo() != null) {
                        System.out.println("\nSession Info:");
                        System.out.println("\nResource URL: " +infoResult2.getSessionInfo().getResourceUrl());
                    }

                    System.out.println("\n==============================================");
                    System.out.println("Check if you are automatically logged in!");
                    System.out.println("==============================================");

                    System.out.println("\nCleaning up second session...");
                    session2.delete();
                    System.out.println("Second session deleted");
                } else {
                    System.err.println("Failed to create second session: " + result2.getErrorMessage());
                }

            } else {
                System.err.println("Failed to create first session: " + result1.getErrorMessage());
            }

            agentBay.getContext().delete(context);
            System.out.println("\nContext cleaned up");
            System.out.println("\nAll done!");

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}